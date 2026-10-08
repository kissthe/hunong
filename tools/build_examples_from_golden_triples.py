"""把 golden_triples 中的题目整理成 example/ 的形式。

对 golden_triples/<conv_id>/<conv_id>.json 里出现的每个目标人物（按 user_id 区分）：
  - <name>_dialogue.json  从 locomo10.json 抽出该人物所在的完整对话，结构同 example/deborah_dialogue.json
  - <name>_eval.json      该人物的全部题目，结构同 example/deborah_eval.json
  - <name>_eval.meta.json 对应题目的 meta（含评测时必须用到的 history_filter）

用法：python3 tools/build_examples_from_golden_triples.py
"""

import hashlib
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCOMO = ROOT / "locomo10.json"
TRIPLES = ROOT / "golden_triples"
OUT = ROOT / "golden_triples_examples"

SCHEMA_VERSION = "pamta.locomo_single_conversation.original.v1"
EXTRACTION_NOTE = (
    "Extracted from the official LoCoMo conversation object. "
    "QA, event_summary, observation, and session_summary are intentionally excluded."
)
EVAL_KEYS = ["sample_id", "user_id", "current_input", "gold"]


def dump(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def build_dialogue(sample, target, sha256):
    conv = sample["conversation"]
    speaker_a, speaker_b = conv["speaker_a"], conv["speaker_b"]
    partner = speaker_b if target == speaker_a else speaker_a

    numbers = sorted(
        int(m.group(1))
        for k in conv
        if (m := re.fullmatch(r"session_(\d+)", k)) and conv[k]
    )
    sessions, target_turns = [], []
    for n in numbers:
        sid = f"session_{n}"
        date_time = conv[f"{sid}_date_time"]
        turns = conv[sid]
        sessions.append(
            {"session_id": sid, "session_number": n, "date_time": date_time, "turns": turns}
        )
        for t in turns:
            if t["speaker"] == target:
                target_turns.append(
                    {**t, "session_id": sid, "session_number": n, "date_time": date_time}
                )

    return {
        "schema_version": SCHEMA_VERSION,
        "source_dataset": "LoCoMo",
        "source_sample_id": sample["sample_id"],
        "source_file": LOCOMO.name,
        "source_file_sha256": sha256,
        "source_extraction_note": EXTRACTION_NOTE,
        "target_user": target,
        "conversation_partner": partner,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "session_count": len(sessions),
        "full_turn_count": sum(len(s["turns"]) for s in sessions),
        "target_user_turn_count": len(target_turns),
        "sessions": sessions,
        "target_user_turns": target_turns,
    }


def main():
    raw = LOCOMO.read_bytes()
    sha256 = hashlib.sha256(raw).hexdigest()
    locomo = {s["sample_id"]: s for s in json.loads(raw)}

    for conv_dir in sorted(p for p in TRIPLES.iterdir() if p.is_dir()):
        conv_id = conv_dir.name
        questions = json.loads((conv_dir / f"{conv_id}.json").read_text(encoding="utf-8"))
        meta = json.loads((conv_dir / f"{conv_id}.meta.json").read_text(encoding="utf-8"))
        sample = locomo[conv_id]
        speakers = {
            s.lower(): s
            for s in (sample["conversation"]["speaker_a"], sample["conversation"]["speaker_b"])
        }

        by_user = OrderedDict()
        for q in questions:
            by_user.setdefault(q["user_id"], []).append(q)

        for user_id, qs in by_user.items():
            key = user_id.removeprefix("u_")
            target = speakers[key]
            out_dir = OUT / f"{conv_id}_{key}"
            dialogue = build_dialogue(sample, target, sha256)
            dump(dialogue, out_dir / f"{key}_dialogue.json")
            dump([{k: q[k] for k in EVAL_KEYS} for q in qs], out_dir / f"{key}_eval.json")
            dump({q["sample_id"]: meta[q["sample_id"]] for q in qs}, out_dir / f"{key}_eval.meta.json")
            print(
                f"{out_dir.relative_to(ROOT)}: {target} vs {dialogue['conversation_partner']}, "
                f"{dialogue['session_count']} sessions, {dialogue['full_turn_count']} turns "
                f"({dialogue['target_user_turn_count']} by {target}), {len(qs)} questions"
            )


if __name__ == "__main__":
    main()
