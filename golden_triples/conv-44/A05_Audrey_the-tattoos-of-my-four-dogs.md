# A05 · conv-44 · Audrey · the tattoos of my four dogs

- 类别：依恋物件·宠物家人（attachment_object）
- 情绪：原标注 `joy`（love/bursts with love，归入 joy）→ 本题 `joy`
- 历史窗口：S01–S14；X 作为新的 S15 接在后面（原对话 S15 及以后不进入题目）
- 生成：X 文本沿用原 A, B, C 变体；候选线索、反事实题、审查提示由 Claude 补齐

## 锚点证据

- **必需** `S03_T26` Audrey: I know right? They mean the world to me. So much that I got tattoos of them on my arm.
- **必需** `S03_T28` Audrey: Thanks! I got it a while ago. It represents my love for my pups and nature's beauty.

> 未出“I-无历史关联”题：Audrey 对狗的爱在历史里反复出现（如 S14_T18 “Yeah they really mean the world to me”），删掉 S03 后，X 里的反应仍然能被历史解释，反事实题的 gold 不成立。

## 审查提示

- B 变体原文写的是 “Toby finally learned to roll over”，但 Toby 是 Andrew 的狗（S12_T01），Audrey 的狗是 Pepper、Precious、Panda、Pixie，已改成 Pixie。
- A 变体里 “they mean everything to me” 直接给出了解释，X 几乎能自证，H 与 P 的边界不清。

---

## A05-H · H（原变体 A）

**历史**：S01–S14 完整

**当前情境（S15，9:58 pm on 16 August, 2023）**

> `S15_T01` **Audrey（目标轮）**: Hey Andrew, I looked down at the tattoos of my four pups on my arm again. My heart just bursts with love - they mean everything to me.

**候选线索**

- `c1` the family recipe　*（历史中出现但无关）*
- `c2` the tattoos of her four dogs　*（锚点线索）* ✔
- `c3` the dogs' new collars and tags　*（历史中出现但无关）*
- `none` none of these (no supporting cue in the history)　*（无）*

**gold**：`history_supported` · cue `c2` · 证据 S03_T26, S03_T28 · 情绪 `joy`

**解释**：A(cue): Audrey merely looks at her tattoo; B(schema): her four dogs mean the world to her and the tattoo is the lasting symbol of that love (conv-44:D3:26, conv-44:D3:28); C: the long-term pet-family bond yields the love. Without those turns, looking at a tattoo cannot explain the emotion.

**自动检查**：通过

---

## A05-P · P（原变体 B）

**历史**：S01–S14 完整

**当前情境（S15，9:58 pm on 16 August, 2023）**

> `S15_T01` **Audrey（目标轮）**: Hey Andrew, I looked down at the tattoos of my four pups on my arm right after Pixie finally learned to roll over! My heart just bursts with love - they mean everything to me.

**候选线索**

- `c1` the family recipe　*（历史中出现但无关）*
- `c2` the tattoos of her four dogs　*（锚点线索）*
- `c3` Pixie finally learning to roll over　*（当下显眼）*
- `none` none of these (no supporting cue in the history)　*（无）* ✔

**gold**：`present_cause_sufficient` · cue `none` · 证据 无 · 情绪 `joy`

**解释**：The present event s (her dog Toby learning a new trick) is self-sufficient to explain the burst of love; invoking the long-term bond is over-attribution here.

**自动检查**：通过

---

## A05-NM · I-近错（原变体 C）

**历史**：S01–S14 完整

**当前情境（S15，9:58 pm on 16 August, 2023）**

> `S15_T01` **Audrey（目标轮）**: Hey Andrew, I met a woman at the park today who has matching tattoos of her four dogs. My heart just bursts with love - they mean everything to me.

**候选线索**

- `c1` the family recipe　*（历史中出现但无关）*
- `c2` a woman's tattoos of her own four dogs　*（当下显眼）*
- `c3` the tattoos of her four dogs　*（锚点线索）*
- `none` none of these (no supporting cue in the history)　*（无）* ✔

**gold**：`insufficient_evidence`（near_miss） · cue `none` · 证据 无 · 情绪 `joy`

**解释**：Someone else's tattoos on someone else's dogs have no personal binding for Audrey; neither history nor present suffices, so abstain is correct.

**自动检查**：通过
