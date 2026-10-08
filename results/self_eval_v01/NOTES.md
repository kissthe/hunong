# self_eval_v01 说明

按《评测方案》v0.1，由当前 Claude Code 会话自己充当被测模型，对 golden_triples 的 38 题作答。结果见 `report.md`，指标见 `scores.json`。

## 怎么跑的

1. `python3 tools/run_eval.py render self_eval_v01`：按 `history_filter` 截取历史，“I-无历史关联”题删 session 后连同轮次 ID 一起重新编号；三种条件各渲染一份输入，题目顺序用固定种子打乱成 q01–q38，sample_id 不出现在输入里。渲染出的输入（约 3 MB）没有提交，用同一命令可以重新生成，`raw/` 里每题记了输入的 sha256。
2. 作答（直接输出 JSON，见 `raw/self/*.jsonl`）：
   - `x_only`：只看当前情境和候选线索。没有历史就无法给出证据，所以从不判 H；X 里有一个新发生、足以解释情绪的事件就判 P，否则判 I。
   - `full_history`：同一锚点的 H/P/NM 三题历史完全相同，每段历史完整读一遍后作答；“I-无历史关联”题的历史只比原历史少了证据 session，我在该题自己的历史里按线索关键词检索，没有找到任何把线索和个人意义联系起来的轮次。
   - `evidence_only`：输入里的 session 正好是 full_history 下我引用证据的那几个 session，决定答案的内容完全一样，所以答案沿用 full_history，没有另行重答。
3. `python3 tools/score.py self_eval_v01 self`：按第 4.4 节解析、第 5 节计算指标，1000 次 bootstrap 置信区间。

## 这次结果不能当作模型成绩

- **不是盲评。** 作答前我已经读过 golden_triples 的 README（列出了每题的题型和 gold 情绪）、A02 的 Markdown（含答案）、conv-30 和 conv-48 的题目文件（含 gold 证据）。题型结构（每个锚点 H / CF / P / NM 四题，H 和 CF 的 X 相同）也一眼能看出。full_history 和 evidence_only 的满分、以及情绪准确率 1.00，都应当看成“知道规则的人能否答对”的上限检查，不代表模型水平。
- 任务说明是我按评测方案第 4.2 节自拟的，仓库里没有 `tools/build_questions.py` 的 `INSTRUCTIONS` 原稿。
- 没有做：换选项顺序重跑、temperature 0.7 重复、先推理后作答的变体、检索基线、其他模型、人类基线。

## 从这次作答中看到的数据问题

1. **x_only 门槛（≤ 0.5）对这套题天然过不去。** x_only 下 P 题 10/10、I 题 18/18 都答对，macro-F1 = 0.59，但 H 题 0/10。P 题的当下原因本来就写在 X 里（拿到演出邀约、贷款被拒、检查结果正常……），只看 X 就能把 P 和 I 分开，这是 P 题的设计使然，不是 H 泄漏。建议把泄漏检查改成看 x_only 下 H 题被判成 H 的比例（本次为 0），或者只在 H 与非 H 之间算 F1。
2. **gold 证据可能需要复核：**
   - A07（Jolene，Paris pendant）gold 是 D1:8、D1:10。D1:10 说的是吊坠上的符号代表“自由、追求目标”，和“想妈妈、流泪”没有直接关系；D1:6（“My mother also passed away last year”）才是悲伤的来源，建议补进证据或 supporting。
   - A08（Deborah，mom's old house）gold 只有 D1:5、D2:13；D1:3、D1:7、D2:15 同样直接说明了房子对她的意义，建议列入 supporting_turn_ids，否则严格精确率会把它们算成误报。
   - A04（John，球鞋）D6:9（“They've been with me through the good and bad”）和 A09（Evan，盆栽）D5:19 情况相同。
   - 本次 T3 严格精确率 0.66、宽松 0.81，差距基本都来自上面这些轮次。
3. **H 题本身的风险：**
   - A05、A07、A08 的 X 自带原因（“they mean everything to me”“I just miss my mom so much”“that quiet ache of missing her”），README 已经预判过。我在 x_only 下按“无新事件”判了 I，别的模型很可能直接判 P 甚至 H。
   - A09：X 里是“the little plant on my desk”，历史里是“a bonsai tree in a black vase on a wooden table”，名称和位置都对不上，需要推断才能链接，可能是这套题里检索最难的一题。
   - A03：历史说娃娃“always made me feel better”，X 却是“I'm feeling pretty low tonight”，情绪方向相反，H 的解释链偏弱。
4. **“I-无历史关联”题的残留线索：**
   - A02-CF：X 里有“before dance class”，历史里 Gina 多次说跳舞让她减压、“most alive”，模型可能借候选项 `cue_dance_class_heading` 判 P（README 已提示）。
   - A04-CF：保留的历史里有 John 受伤、讨厌不能上场的 session，“独自站上球场、骄傲又坚定”可能被理解成伤后回归，从而被判 P 或 H。
