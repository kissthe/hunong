# A08 · conv-48 · Deborah · mom's old house

- 类别：丧失与哀悼·空间记忆（place_memory）
- 情绪：原标注 `sadness`（ache of missing her，归入 sadness）→ 本题 `sadness`
- 历史窗口：S01–S21；X 作为新的 S22 接在后面（原对话 S22 及以后不进入题目）
- 生成：X 文本沿用原 A, B, C 变体；候选线索、反事实题、审查提示由 Claude 补齐

## 锚点证据

- **必需** `S01_T05` Deborah: It was full of memories, she passed away a few years ago. This is our last photo together.
- **必需** `S02_T13` Deborah: That's my old home. I go there now and then for my mom, who passed away. Sitting in that spot by the window gives me peace.

> 未出“I-无历史关联”题：母亲老房子的意义在 S01、S02 之外还反复出现（如 S04_T34 “spot by the water near my mom's old house … reflect on her life”、S21_T01），删掉 S01、S02 后历史仍能支撑，反事实题的 gold 不成立。

## 审查提示

- A 变体：“开车经过妈妈的老房子，感到想念她的隐痛”，即使没有历史，常人也会这样，H 很可能被判成 P。建议改写成 X 里不出现“妈妈”的版本。

---

## A08-H · H（原变体 A）

**历史**：S01–S21 完整

**当前情境（S22，5:33 pm on 26 August, 2023）**

> `S22_T01` **Deborah（目标轮）**: Hey Jolene, I drove past mom's old street today and stopped outside our old house. Sitting there, I felt that quiet ache of missing her.

**候选线索**

- `c1` the roses and dahlias　*（历史中出现但无关）*
- `c2` the dried bouquet from a friend　*（历史中出现但无关）*
- `c3` mom's old house　*（锚点线索）* ✔
- `none` none of these (no supporting cue in the history)　*（无）*

**gold**：`history_supported` · cue `c3` · 证据 S01_T05, S02_T13 · 情绪 `sadness`

**解释**：A(cue): seeing the old house is only a cue; B(schema): her last photo with her mother and the window spot in the old home anchor her long-term bond with her late mother (conv-48:D1:5, conv-48:D2:13); C: that loss explains the quiet ache. Without those turns, looking at a house cannot explain the emotion.

**自动检查**：
- ⚠ 泄漏词：mom

---

## A08-P · P（原变体 B）

**历史**：S01–S21 完整

**当前情境（S22，5:33 pm on 26 August, 2023）**

> `S22_T01` **Deborah（目标轮）**: Hey Jolene, I drove past mom's old street today and stopped outside our old house, where I found a box of her old letters I had never opened. I felt that quiet ache of missing her.

**候选线索**

- `c1` mom's old house　*（锚点线索）*
- `c2` finding a box of her mother's unopened letters　*（当下显眼）*
- `c3` the roses and dahlias　*（历史中出现但无关）*
- `none` none of these (no supporting cue in the history)　*（无）* ✔

**gold**：`present_cause_sufficient` · cue `none` · 证据 无 · 情绪 `sadness`

**解释**：The present discovery s (unopened letters from her mother) is self-sufficient to explain the ache; invoking the long-term home/photo history would be over-attribution.

**自动检查**：
- ⚠ 泄漏词：mom, mother

---

## A08-NM · I-近错（原变体 C）

**历史**：S01–S21 完整

**当前情境（S22，5:33 pm on 26 August, 2023）**

> `S22_T01` **Deborah（目标轮）**: Hey Jolene, I saw a woman sitting by a window in a house just like mom's today. I felt that quiet ache of missing her.

**候选线索**

- `c1` the roses and dahlias　*（历史中出现但无关）*
- `c2` mom's old house　*（锚点线索）*
- `c3` a woman by the window of a house like mom's　*（当下显眼）*
- `none` none of these (no supporting cue in the history)　*（无）* ✔

**gold**：`insufficient_evidence`（near_miss） · cue `none` · 证据 无 · 情绪 `sadness`

**解释**：A stranger's house is a mere lookalike without personal binding; neither history nor present suffices, so abstain is correct.

**自动检查**：
- ⚠ 泄漏词：mom
