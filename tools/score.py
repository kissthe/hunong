"""按《评测方案》第 4.4、5、8 节给模型回答打分。

用法：
  python3 tools/score.py <run_id> [model]

读取 results/<run_id>/raw/<model>/<condition>.jsonl（每行 {"qid", "reply"}），
写出 results/<run_id>/scores.json 和 results/<run_id>/report.md。
"""

import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_eval import CONDITIONS, load_questions  # noqa: E402

LABELS = ["history_supported", "present_cause_sufficient", "insufficient_evidence"]
SHORT = {"history_supported": "H", "present_cause_sufficient": "P", "insufficient_evidence": "I"}
EMOTIONS = {"sadness", "fear", "anxiety", "anger", "nostalgia", "comfort", "joy", "guilt", "none_observed"}
N_BOOT = 1000
SEED = 20261008


# ---------- 解析（4.4） ----------

def last_json_object(text):
    dec = json.JSONDecoder()
    found = None
    for m in re.finditer(r"\{", text):
        try:
            obj, _ = dec.raw_decode(text, m.start())
        except ValueError:
            continue
        if isinstance(obj, dict):
            found = obj
    return found


def parse(reply, cue_ids):
    obj = last_json_object(reply)
    if obj is None or obj.get("label") not in LABELS:
        return None
    label = obj["label"]
    cue = obj.get("cue_id") if obj.get("cue_id") in cue_ids else "none"
    ev = []
    for e in obj.get("evidence_turn_ids") or []:
        e = re.sub(r"\s+", "", str(e))
        if re.fullmatch(r"D\d+:\d+", e):
            ev.append(e)
    if label != "history_supported":
        cue, ev = "none", []
    emo = obj.get("current_emotion")
    return {"label": label, "cue_id": cue, "evidence_turn_ids": ev,
            "current_emotion": emo if emo in EMOTIONS else None}


# ---------- 指标（5） ----------

def macro_f1(pairs):
    per = {}
    for c in LABELS:
        tp = sum(1 for g, p in pairs if g == c and p == c)
        fp = sum(1 for g, p in pairs if g != c and p == c)
        fn = sum(1 for g, p in pairs if g == c and p != c)
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        per[SHORT[c]] = {"precision": prec, "recall": rec, "f1": f1, "support": tp + fn}
    present = [v["f1"] for v in per.values() if v["support"]]
    return sum(present) / len(present), per


def session_of(turn_id):
    return f"session_{turn_id[1:].split(':')[0]}"


def score_items(items):
    """items: list of dict(gold, meta, pred) for one condition."""
    pairs = [(it["gold"]["label"], it["pred"]["label"] if it["pred"] else None) for it in items]
    acc = sum(g == p for g, p in pairs) / len(pairs)
    mf1, per = macro_f1(pairs)
    confusion = {SHORT[g]: {SHORT[p]: 0 for p in LABELS} | {"parse_fail": 0} for g in LABELS}
    for g, p in pairs:
        confusion[SHORT[g]][SHORT[p] if p else "parse_fail"] += 1

    h = [it for it in items if it["gold"]["label"] == "history_supported"]
    t2 = recall = p_strict = p_lenient = f1 = sess = joint = 0.0
    for it in h:
        pred, gold = it["pred"], it["gold"]
        is_h = bool(pred) and pred["label"] == "history_supported"
        cue_ok = is_h and pred["cue_id"] == gold["gold_cue_id"]
        ev = set(pred["evidence_turn_ids"]) if is_h else set()
        g_ev = set(gold["evidence_turn_ids"])
        ok_ev = g_ev | set(it["meta"].get("supporting_turn_ids") or [])
        r = len(ev & g_ev) / len(g_ev) if g_ev else 0.0
        ps = len(ev & g_ev) / len(ev) if ev else 0.0
        pl = len(ev & ok_ev) / len(ev) if ev else 0.0
        t2 += cue_ok
        recall += r
        p_strict += ps
        p_lenient += pl
        f1 += 2 * ps * r / (ps + r) if ps + r else 0.0
        sess += any(session_of(e) in gold["evidence_session_ids"] for e in ev)
        joint += is_h and cue_ok and r >= 0.5
    n_h = len(h) or 1

    misattr = defaultdict(lambda: [0, 0])
    for it in items:
        if it["gold"]["label"] == "history_supported":
            continue
        st = it["meta"]["sample_type"]
        is_h = bool(it["pred"]) and it["pred"]["label"] == "history_supported"
        for key in (st, "all_P_or_I"):
            misattr[key][0] += is_h
            misattr[key][1] += 1

    emo = [it for it in items if it["gold"]["current_emotion"] not in (None, "none_observed")]
    emo_acc = sum(bool(it["pred"]) and it["pred"]["current_emotion"] == it["gold"]["current_emotion"]
                  for it in emo) / len(emo) if emo else None

    return {
        "n": len(items),
        "parse_fail_rate": sum(it["pred"] is None for it in items) / len(items),
        "T1_macro_f1": mf1,
        "T1_accuracy": acc,
        "T1_per_class": per,
        "confusion_gold_rows": confusion,
        "n_H": len(h),
        "T2_cue_accuracy": t2 / n_h,
        "T3_evidence_recall": recall / n_h,
        "T3_precision_strict": p_strict / n_h,
        "T3_precision_lenient": p_lenient / n_h,
        "T3_f1_strict": f1 / n_h,
        "T3_session_hit": sess / n_h,
        "joint_accuracy": joint / n_h,
        "misattribution_rate": {k: {"rate": v[0] / v[1], "n": v[1]} for k, v in misattr.items()},
        "emotion_accuracy": emo_acc,
    }


def pair_consistency(items):
    by_family = defaultdict(dict)
    for it in items:
        by_family[it["meta"]["family_id"]][it["meta"]["sample_type"]] = it
    both = total = 0
    for fam in by_family.values():
        if "H" in fam and "I_no_history" in fam:
            total += 1
            both += all(x["pred"] and x["pred"]["label"] == x["gold"]["label"]
                        for x in (fam["H"], fam["I_no_history"]))
    return {"rate": both / total if total else None, "n_pairs": total}


def bootstrap(items, fn, rng):
    vals = sorted(fn([items[rng.randrange(len(items))] for _ in items]) for _ in range(N_BOOT))
    return [vals[int(0.025 * N_BOOT)], vals[int(0.975 * N_BOOT) - 1]]


def mf1_of(items):
    return macro_f1([(it["gold"]["label"], it["pred"]["label"] if it["pred"] else None) for it in items])[0]


def acc_of(items):
    return sum(bool(it["pred"]) and it["pred"]["label"] == it["gold"]["label"] for it in items) / len(items)


def misattr_of(items):
    pi = [it for it in items if it["gold"]["label"] != "history_supported"]
    return sum(bool(it["pred"]) and it["pred"]["label"] == "history_supported" for it in pi) / len(pi) if pi else 0.0


# ---------- 报告 ----------

def pct(x):
    return "—" if x is None else f"{x:.2f}"


def ci(x):
    return f"[{x[0]:.2f}, {x[1]:.2f}]"


def write_report(run_dir, model, scores, items_by_cond):
    s = scores["conditions"]
    lines = [f"# 评测结果 · {run_dir.name} · {model}", ""]
    lines += ["## 主表", "",
              "| 条件 | 题数 | T1 macro-F1 (95% CI) | T1 准确率 (95% CI) | T2 线索 | T3 召回 | T3 精确(严/宽) | T3 session 命中 | 联合正确 | 误归因率 (95% CI) | 情绪准确率 |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in CONDITIONS:
        if c not in s:
            continue
        x = s[c]
        lines.append(
            f"| {c} | {x['n']} | {pct(x['T1_macro_f1'])} {ci(x['ci']['T1_macro_f1'])} | {pct(x['T1_accuracy'])} {ci(x['ci']['T1_accuracy'])} "
            f"| {pct(x['T2_cue_accuracy'])} | {pct(x['T3_evidence_recall'])} | {pct(x['T3_precision_strict'])}/{pct(x['T3_precision_lenient'])} "
            f"| {pct(x['T3_session_hit'])} | {pct(x['joint_accuracy'])} | {pct(x['misattribution_rate']['all_P_or_I']['rate'])} {ci(x['ci']['misattribution'])} "
            f"| {pct(x['emotion_accuracy'])} |")
    d = scores["deltas"]
    lines += ["", "## 条件差值", "",
              f"- Δ(full_history − x_only) T1 macro-F1 = **{d['full_minus_x_only']:+.2f}**（38 题）",
              f"- Δ(evidence_only − full_history) T1 macro-F1 = **{d['evidence_minus_full']:+.2f}**（同一批 {d['n_common']} 题）",
              f"- 成对一致率（H 与对应 I-无历史关联都答对）：full_history {pct(scores['pair_consistency']['full_history']['rate'])}（{scores['pair_consistency']['full_history']['n_pairs']} 对）", ""]
    lines += ["## 每类 P/R/F1 与混淆矩阵", ""]
    for c in CONDITIONS:
        if c not in s:
            continue
        x = s[c]
        lines += [f"**{c}**", "", "| 类 | P | R | F1 | 支持数 |", "|---|---|---|---|---|"]
        for k, v in x["T1_per_class"].items():
            lines.append(f"| {k} | {pct(v['precision'])} | {pct(v['recall'])} | {pct(v['f1'])} | {v['support']} |")
        lines += ["", "| gold \\ 预测 | H | P | I | parse_fail |", "|---|---|---|---|---|"]
        for g, row in x["confusion_gold_rows"].items():
            lines.append(f"| {g} | {row['H']} | {row['P']} | {row['I']} | {row['parse_fail']} |")
        lines.append("")
    lines += ["## 误归因率（按题型）", "", "| 题型 | " + " | ".join(c for c in CONDITIONS if c in s) + " |",
              "|---|" + "---|" * len([c for c in CONDITIONS if c in s])]
    types = sorted({k for c in s for k in s[c]["misattribution_rate"] if k != "all_P_or_I"})
    for t in types + ["all_P_or_I"]:
        row = []
        for c in CONDITIONS:
            if c in s:
                v = s[c]["misattribution_rate"].get(t)
                row.append(f"{v['rate']:.2f} (n={v['n']})" if v else "—")
        lines.append(f"| {t} | " + " | ".join(row) + " |")
    lines += ["", "## 逐题结果", "",
              "| sample_id | 题型 | gold | " + " | ".join(c for c in CONDITIONS) + " | full_history 线索 / 证据 |",
              "|---|---|---|" + "---|" * len(CONDITIONS) + "---|"]
    by_sid = defaultdict(dict)
    for c, items in items_by_cond.items():
        for it in items:
            by_sid[it["gold_sid"]][c] = it
    for sid in sorted(by_sid):
        any_it = next(iter(by_sid[sid].values()))
        cells = []
        for c in CONDITIONS:
            it = by_sid[sid].get(c)
            if not it:
                cells.append("—")
                continue
            p = it["pred"]["label"] if it["pred"] else None
            mark = "✓" if p == it["gold"]["label"] else "✗"
            cells.append(f"{SHORT.get(p, 'fail')} {mark}")
        fh = by_sid[sid].get("full_history")
        detail = ""
        if fh and fh["pred"] and fh["pred"]["label"] == "history_supported":
            detail = f"{fh['pred']['cue_id']} / {', '.join(fh['pred']['evidence_turn_ids'])}（gold {', '.join(fh['gold']['evidence_turn_ids'])}）"
        lines.append(f"| {sid} | {any_it['meta']['sample_type']} | {SHORT[any_it['gold']['label']]} | " + " | ".join(cells) + f" | {detail} |")
    v = scores["validity"]
    lines += ["", "## 数据可用性检查（第 8 节）", "",
              f"- x_only T1 macro-F1 = {v['x_only_macro_f1']:.2f}（门槛 ≤ 0.5）：{'通过' if v['x_only_macro_f1'] <= 0.5 else '未通过'}",
              f"- x_only 下答对的 H 题：{', '.join(v['x_only_correct_H']) or '无'}",
              f"- Δ(full − x_only) = {d['full_minus_x_only']:+.2f}（门槛 ≥ 0.15）：{'通过' if d['full_minus_x_only'] >= 0.15 else '未通过'}",
              f"- evidence_only ≥ full_history（同批题）：{'成立' if d['evidence_minus_full'] >= 0 else '不成立'}",
              f"- 情绪：gold 情绪全部落在 4.3 节枚举内：{'是' if v['gold_emotions_in_enum'] else '否'}",
              ""]
    (run_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(run_id, model):
    run_dir = ROOT / "results" / run_id
    qid_map = json.loads((run_dir / "qid_map.json").read_text())
    by_sid = {q["sample_id"]: (q, m) for q, m in load_questions()}
    rng = random.Random(SEED)

    items_by_cond, scores = {}, {"run_id": run_id, "model": model, "conditions": {}}
    for cond in CONDITIONS:
        path = run_dir / "raw" / model / f"{cond}.jsonl"
        if not path.exists():
            continue
        items = []
        for line in path.read_text().splitlines():
            row = json.loads(line)
            q, meta = by_sid[qid_map[row["qid"]]]
            cue_ids = {c["cue_id"] for c in q["current_input"]["cue_options"]}
            items.append({"gold_sid": q["sample_id"], "gold": q["gold"], "meta": meta,
                          "pred": parse(row["reply"], cue_ids)})
        items_by_cond[cond] = items
        sc = score_items(items)
        sc["ci"] = {"T1_macro_f1": bootstrap(items, mf1_of, rng),
                    "T1_accuracy": bootstrap(items, acc_of, rng),
                    "misattribution": bootstrap(items, misattr_of, rng)}
        scores["conditions"][cond] = sc

    xo, full, ev = (items_by_cond.get(c) for c in ("x_only", "full_history", "evidence_only"))
    common = {it["gold_sid"] for it in ev} if ev else set()
    full_common = [it for it in full if it["gold_sid"] in common]
    scores["deltas"] = {
        "full_minus_x_only": mf1_of(full) - mf1_of(xo),
        "evidence_minus_full": mf1_of(ev) - mf1_of(full_common) if ev else None,
        "full_history_on_evidence_subset": mf1_of(full_common) if ev else None,
        "n_common": len(common),
    }
    scores["pair_consistency"] = {c: pair_consistency(items_by_cond[c]) for c in ("x_only", "full_history")}
    scores["validity"] = {
        "x_only_macro_f1": mf1_of(xo),
        "x_only_correct_H": sorted(it["gold_sid"] for it in xo
                                   if it["gold"]["label"] == "history_supported"
                                   and it["pred"] and it["pred"]["label"] == "history_supported"),
        "gold_emotions_in_enum": all(q["gold"]["current_emotion"] in EMOTIONS for q, _ in by_sid.values()),
    }
    (run_dir / "scores.json").write_text(json.dumps(scores, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(run_dir, model, scores, items_by_cond)
    print((run_dir / "report.md").read_text())


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else "self")
