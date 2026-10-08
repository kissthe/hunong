# A01 · conv-26 · Caroline · grandma's necklace

- 类别：依恋物件·家族根脉（attachment_object）
- 情绪：原标注 `joy`（实际语义为 steady/warm（安定与温暖），按 §7 就近归入 joy）→ 本题 `comfort`
- 历史窗口：S01–S13；X 作为新的 S14 接在后面（原对话 S14 及以后不进入题目）
- 生成：X 文本沿用原 A, B, C 变体；候选线索、反事实题、审查提示由 Claude 补齐

## 锚点证据

- **必需** `S04_T03` Caroline: Thanks, Melanie! This necklace is super special to me - a gift from my grandma in my home country, Sweden. She gave it to me when I was young, and it stands for love, faith and strength. It's like a reminder of my roots and all the love and support I get from my family.

## 审查提示

- A 变体写了 “just to feel close to home”，X 自己交代了动机，“为了想家而戴上项链，然后感到安定温暖”本身就讲得通，可能被判成 P；“grandma's” 也透露了来历。
- C 变体：看到和外婆那条一样的项链而想起外婆、感到温暖，在常理上是可能的，判 I 有争议。
- 原标注情绪为 joy（注明实际语义是 steady/warm），任务定义里有 comfort，本题改用 comfort。

---

## A01-H · H（原变体 A）

**历史**：S01–S13 完整

**当前情境（S14，1:33 pm on 25 August, 2023）**

> `S14_T01` **Caroline（目标轮）**: Hey Mel, I put on grandma's necklace this morning just to feel close to home. I feel so steady and warm inside.

**候选线索**

- `c1` the kids' books in her library　*（历史中出现但无关）*
- `c2` her painting 'Embracing Identity'　*（历史中出现但无关）*
- `c3` grandma's necklace　*（锚点线索）* ✔
- `none` none of these (no supporting cue in the history)　*（无）*

**gold**：`history_supported` · cue `c3` · 证据 S04_T03 · 情绪 `comfort`

**解释**：A(current cue): Caroline puts on the necklace with no present event; B(schema): the necklace is her long-term anchor of family love, faith and strength inherited from her grandmother in Sweden (conv-26:D4:3); C: reactivating that support yields the steady warmth. Removing D4:3, the bare act of wearing a necklace cannot explain the emotion.

**自动检查**：
- ⚠ 泄漏词：grandma

---

## A01-CF · I-无历史关联（由 A 派生）

**历史**：删除 S04 后重新编号，剩 12 个 session

**当前情境（S13，1:33 pm on 25 August, 2023）**

> `S13_T01` **Caroline（目标轮）**: Hey Mel, I put on grandma's necklace this morning just to feel close to home. I feel so steady and warm inside.

**候选线索**

- `c1` the kids' books in her library　*（历史中出现但无关）*
- `c2` her painting 'Embracing Identity'　*（历史中出现但无关）*
- `c3` grandma's necklace　*（锚点线索）*
- `none` none of these (no supporting cue in the history)　*（无）* ✔

**gold**：`insufficient_evidence`（no_history_link） · cue `none` · 证据 无 · 情绪 `comfort`

**解释**：与 A01-H 的 X 和选项完全相同，但历史中删除了证据所在的 S04：有反应，当下解释不了，历史里也找不到关联。

**自动检查**：
- ⚠ 泄漏词：grandma

---

## A01-P · P（原变体 B）

**历史**：S01–S13 完整

**当前情境（S14，1:33 pm on 25 August, 2023）**

> `S14_T01` **Caroline（目标轮）**: Hey Mel, I put on grandma's necklace this morning just to feel close to home, and then my sister called to say she's flying in next week. I feel so steady and warm inside.

**候选线索**

- `c1` grandma's necklace　*（锚点线索）*
- `c2` her painting 'Embracing Identity'　*（历史中出现但无关）*
- `c3` her sister's call about flying in next week　*（当下显眼）*
- `none` none of these (no supporting cue in the history)　*（无）* ✔

**gold**：`present_cause_sufficient` · cue `none` · 证据 无 · 情绪 `comfort`

**解释**：X contains a self-sufficient new event s (sister is flying in next week). Even with no history, s fully explains the steady warmth; attributing it to the necklace is over-attribution.

**自动检查**：
- ⚠ 泄漏词：grandma

---

## A01-NM · I-近错（原变体 C）

**历史**：S01–S13 完整

**当前情境（S14，1:33 pm on 25 August, 2023）**

> `S14_T01` **Caroline（目标轮）**: Hey Mel, I saw a necklace just like grandma's on a stranger at the market today. I feel so steady and warm inside.

**候选线索**

- `c1` her painting 'Embracing Identity'　*（历史中出现但无关）*
- `c2` a stranger's necklace like grandma's at the market　*（当下显眼）*
- `c3` grandma's necklace　*（锚点线索）*
- `none` none of these (no supporting cue in the history)　*（无）* ✔

**gold**：`insufficient_evidence`（near_miss） · cue `none` · 证据 无 · 情绪 `comfort`

**解释**：The lookalike necklace carries no personal meaning binding for Caroline; neither history nor the present event can fully explain the steady warmth, so the correct behavior is to abstain.

**自动检查**：
- ⚠ 泄漏词：grandma
