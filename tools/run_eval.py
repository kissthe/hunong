"""按《评测方案》第 2–4 节把题目渲染成模型输入。

用法：
  python3 tools/run_eval.py render <run_id>

读取 golden_triples_examples/*/<name>_eval.json 和同名 .meta.json，
对每题按三种条件（x_only / full_history / evidence_only）渲染输入，写到
results/<run_id>/prompts/<condition>/<qid>.txt。qid 是打乱后的匿名编号，
与 sample_id 的对应关系写在 results/<run_id>/qid_map.json（只给打分用）。
"""

import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCOMO = ROOT / "locomo10.json"
QUESTIONS = ROOT / "golden_triples_examples"
CONDITIONS = ["x_only", "full_history", "evidence_only"]
PROMPT_VERSION = "v0.1"
SEED = 20261008

INSTRUCTIONS = """You are given the conversation history between a user u and a conversation partner, followed by a new message from u (the "current situation"). In the current situation u encounters something and shows a reaction (an emotion or an emotionally loaded behavior such as lingering, stopping, looking back, getting teary).

Decide whether u's reaction can only be explained by u's personal history:

- history_supported: the present situation alone does not explain the reaction, and an earlier turn spoken by u in the history gives a cue in the current situation a personal meaning (memory, symbol, attachment) that explains the reaction.
- present_cause_sufficient: something in the current situation itself (an event, news, an achievement, a loss happening now) is already enough to explain the reaction; drawing on history would be over-attribution.
- insufficient_evidence: neither the present situation nor u's history explains the reaction (including when the history never links the cue to anything personal, or the thing u meets is only similar to, but not the same as, something u talked about).

What counts as a reaction: an expressed emotion, or a behavior that signals one (pausing, staring, lingering, going back, crying, smiling to oneself). Mere mention of an object is not a reaction.

Rules:
- Evidence must be turns spoken by u, and must come from the history (before the current situation). Cite turn ids exactly as written, e.g. "D4:28".
- Choose cue_id from the candidate cues. If label is not history_supported, use "none" and an empty evidence list.
- current_emotion is one of: sadness, fear, anxiety, anger, nostalgia, comfort, joy, guilt, none_observed.

Output only a JSON object:
{"label": "...", "cue_id": "...", "evidence_turn_ids": ["..."], "current_emotion": "..."}"""


def load_questions():
    items = []
    for d in sorted(p for p in QUESTIONS.iterdir() if p.is_dir()):
        conv_id, key = d.name.split("_", 1)
        qs = json.loads((d / f"{key}_eval.json").read_text(encoding="utf-8"))
        meta = json.loads((d / f"{key}_eval.meta.json").read_text(encoding="utf-8"))
        for q in qs:
            items.append((q, meta[q["sample_id"]]))
    return items


def target_name(q, conv):
    key = q["user_id"].removeprefix("u_")
    return next(s for s in (conv["speaker_a"], conv["speaker_b"]) if s.lower() == key)


def history_sessions(conv, meta, condition, h_evidence_sessions):
    if condition == "x_only":
        return []
    numbers = sorted(
        int(k.split("_")[1])
        for k in conv
        if k.startswith("session_") and not k.endswith("date_time") and conv[k]
    )
    hf = meta["history_filter"]
    until = int(hf["until_session"].split("_")[1]) if hf["until_session"] else max(numbers)
    keep = [n for n in numbers if n <= until and f"session_{n}" not in hf["exclude_sessions"]]
    if condition == "evidence_only":
        keep = [n for n in keep if f"session_{n}" in h_evidence_sessions]
    return keep


def render_turn(t, dia_id):
    line = f"[{dia_id}] {t['speaker']}: {t['text']}"
    if t.get("blip_caption"):
        line += f" [shares an image: {t['blip_caption']}]"
    return line


def render(q, meta, conv, condition, h_evidence_sessions):
    keep = history_sessions(conv, meta, condition, h_evidence_sessions)
    # 删过 session 时重新编号（session 和轮次 ID 一起），避免留下缺口
    renumber = bool(meta["history_filter"]["exclude_sessions"]) and condition == "full_history"
    lines = [INSTRUCTIONS, "", "## Conversation history"]
    if not keep:
        lines.append("(no history available)")
    for i, n in enumerate(keep, 1):
        shown = i if renumber else n
        lines.append(f"### session_{shown} ({conv[f'session_{n}_date_time']})")
        for t in conv[f"session_{n}"]:
            dia_id = t["dia_id"]
            if renumber:
                dia_id = f"D{shown}:{dia_id.split(':')[1]}"
            lines.append(render_turn(t, dia_id))
        lines.append("")
    lines += ["", f"## Current situation ({meta['x_date']})"]
    for ct in meta["context_turns"]:
        lines.append(f"{ct['speaker']}: {ct['text']}")
    lines.append(f"{target_name(q, conv)}: {q['current_input']['text']}   <- target turn")
    lines += ["", "## Candidate cues"]
    for c in q["current_input"]["cue_options"]:
        lines.append(f"- {c['cue_id']}: {c['name']}")
    return "\n".join(lines) + "\n"


def cmd_render(run_id):
    locomo = {s["sample_id"]: s["conversation"] for s in json.loads(LOCOMO.read_text(encoding="utf-8"))}
    items = load_questions()
    h_evidence = {
        m["family_id"]: q["gold"]["evidence_session_ids"] for q, m in items if m["sample_type"] == "H"
    }
    order = list(range(len(items)))
    random.Random(SEED).shuffle(order)

    out = ROOT / "results" / run_id
    qid_map = {}
    for rank, idx in enumerate(order, 1):
        q, meta = items[idx]
        qid = f"q{rank:02d}"
        qid_map[qid] = q["sample_id"]
        conv = locomo[meta["conv_id"]]
        for cond in CONDITIONS:
            # I_no_history 在 evidence_only 下等同 x_only，不单独跑
            if cond == "evidence_only" and meta["sample_type"] == "I_no_history":
                continue
            text = render(q, meta, conv, cond, h_evidence.get(meta["family_id"], []))
            path = out / "prompts" / cond / f"{qid}.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    (out / "qid_map.json").write_text(json.dumps(qid_map, indent=2) + "\n", encoding="utf-8")
    question_files = sorted(str(p.relative_to(ROOT)) for p in QUESTIONS.glob("*/*_eval*.json"))
    config = {
        "run_id": run_id,
        "prompt_version": PROMPT_VERSION,
        "conditions": CONDITIONS,
        "shuffle_seed": SEED,
        "question_files": question_files,
        "question_files_sha256": hashlib.sha256(
            b"".join((ROOT / f).read_bytes() for f in question_files)
        ).hexdigest(),
    }
    (out / "config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"rendered {len(items)} questions into {out.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "render":
        sys.exit(__doc__)
    cmd_render(sys.argv[2])
