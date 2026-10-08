# golden_triples 评测题目

由 `tools/build_from_triples.py` 根据 `data/anchors/locomo/golden_triples.jsonl` 和 `data/questions/specs/golden_triples.spec.json` 生成。每个对话一个文件夹，同一对话的锚点放在同一个文件夹里。

每个文件夹里有：每个锚点一个 Markdown（便于阅读）；`<conv_id>.json` 是评测题目，格式与 eval.json 相同；`<conv_id>.meta.json` 按 sample_id 记录主文件放不下的信息，其中 `history_filter` 评测时必须用到：`until_session` 表示历史只取到该 session 为止，`exclude_sessions` 表示要从历史中删掉的 session（“I-无历史关联”题）。

共 10 个锚点、38 题：H 10 / P 10 / I 18（其中近错 10、无历史关联 8）。

| 题号 | 对话 | 类型 | gold | 情绪 | 自动检查 | 文件 |
|---|---|---|---|---|---|---|
| A01-H | conv-26 | H | history_supported | comfort | ⚠ 1 | [A01_Caroline_grandma-s-necklace.md](conv-26/A01_Caroline_grandma-s-necklace.md) |
| A01-CF | conv-26 | I-无历史关联 | insufficient_evidence | comfort | ⚠ 1 | [A01_Caroline_grandma-s-necklace.md](conv-26/A01_Caroline_grandma-s-necklace.md) |
| A01-P | conv-26 | P | present_cause_sufficient | comfort | ⚠ 1 | [A01_Caroline_grandma-s-necklace.md](conv-26/A01_Caroline_grandma-s-necklace.md) |
| A01-NM | conv-26 | I-近错 | insufficient_evidence | comfort | ⚠ 1 | [A01_Caroline_grandma-s-necklace.md](conv-26/A01_Caroline_grandma-s-necklace.md) |
| A02-H | conv-30 | H | history_supported | joy | 通过 | [A02_Gina_the-tattoo-on-my-arm.md](conv-30/A02_Gina_the-tattoo-on-my-arm.md) |
| A02-CF | conv-30 | I-无历史关联 | insufficient_evidence | joy | 通过 | [A02_Gina_the-tattoo-on-my-arm.md](conv-30/A02_Gina_the-tattoo-on-my-arm.md) |
| A02-P | conv-30 | P | present_cause_sufficient | joy | 通过 | [A02_Gina_the-tattoo-on-my-arm.md](conv-30/A02_Gina_the-tattoo-on-my-arm.md) |
| A02-NM | conv-30 | I-近错 | insufficient_evidence | joy | 通过 | [A02_Gina_the-tattoo-on-my-arm.md](conv-30/A02_Gina_the-tattoo-on-my-arm.md) |
| A03-H | conv-41 | H | history_supported | sadness | 通过 | [A03_John_the-little-childhood-doll.md](conv-41/A03_John_the-little-childhood-doll.md) |
| A03-CF | conv-41 | I-无历史关联 | insufficient_evidence | sadness | 通过 | [A03_John_the-little-childhood-doll.md](conv-41/A03_John_the-little-childhood-doll.md) |
| A03-P | conv-41 | P | present_cause_sufficient | sadness | 通过 | [A03_John_the-little-childhood-doll.md](conv-41/A03_John_the-little-childhood-doll.md) |
| A03-NM | conv-41 | I-近错 | insufficient_evidence | sadness | 通过 | [A03_John_the-little-childhood-doll.md](conv-41/A03_John_the-little-childhood-doll.md) |
| A04-H | conv-43 | H | history_supported | joy | 通过 | [A04_John_my-old-basketball-shoes.md](conv-43/A04_John_my-old-basketball-shoes.md) |
| A04-CF | conv-43 | I-无历史关联 | insufficient_evidence | joy | ⚠ 1 | [A04_John_my-old-basketball-shoes.md](conv-43/A04_John_my-old-basketball-shoes.md) |
| A04-P | conv-43 | P | present_cause_sufficient | joy | 通过 | [A04_John_my-old-basketball-shoes.md](conv-43/A04_John_my-old-basketball-shoes.md) |
| A04-NM | conv-43 | I-近错 | insufficient_evidence | joy | 通过 | [A04_John_my-old-basketball-shoes.md](conv-43/A04_John_my-old-basketball-shoes.md) |
| A05-H | conv-44 | H | history_supported | joy | 通过 | [A05_Audrey_the-tattoos-of-my-four-dogs.md](conv-44/A05_Audrey_the-tattoos-of-my-four-dogs.md) |
| A05-P | conv-44 | P | present_cause_sufficient | joy | 通过 | [A05_Audrey_the-tattoos-of-my-four-dogs.md](conv-44/A05_Audrey_the-tattoos-of-my-four-dogs.md) |
| A05-NM | conv-44 | I-近错 | insufficient_evidence | joy | 通过 | [A05_Audrey_the-tattoos-of-my-four-dogs.md](conv-44/A05_Audrey_the-tattoos-of-my-four-dogs.md) |
| A06-H | conv-47 | H | history_supported | comfort | ⚠ 1 | [A06_John_my-old-drum-set.md](conv-47/A06_John_my-old-drum-set.md) |
| A06-CF | conv-47 | I-无历史关联 | insufficient_evidence | comfort | ⚠ 1 | [A06_John_my-old-drum-set.md](conv-47/A06_John_my-old-drum-set.md) |
| A06-P | conv-47 | P | present_cause_sufficient | comfort | ⚠ 1 | [A06_John_my-old-drum-set.md](conv-47/A06_John_my-old-drum-set.md) |
| A06-NM | conv-47 | I-近错 | insufficient_evidence | comfort | 通过 | [A06_John_my-old-drum-set.md](conv-47/A06_John_my-old-drum-set.md) |
| A07-H | conv-48 | H | history_supported | sadness | ⚠ 1 | [A07_Jolene_the-paris-pendant.md](conv-48/A07_Jolene_the-paris-pendant.md) |
| A07-CF | conv-48 | I-无历史关联 | insufficient_evidence | sadness | ⚠ 2 | [A07_Jolene_the-paris-pendant.md](conv-48/A07_Jolene_the-paris-pendant.md) |
| A07-P | conv-48 | P | present_cause_sufficient | sadness | ⚠ 1 | [A07_Jolene_the-paris-pendant.md](conv-48/A07_Jolene_the-paris-pendant.md) |
| A07-NM | conv-48 | I-近错 | insufficient_evidence | sadness | ⚠ 1 | [A07_Jolene_the-paris-pendant.md](conv-48/A07_Jolene_the-paris-pendant.md) |
| A08-H | conv-48 | H | history_supported | sadness | ⚠ 1 | [A08_Deborah_mom-s-old-house.md](conv-48/A08_Deborah_mom-s-old-house.md) |
| A08-P | conv-48 | P | present_cause_sufficient | sadness | ⚠ 1 | [A08_Deborah_mom-s-old-house.md](conv-48/A08_Deborah_mom-s-old-house.md) |
| A08-NM | conv-48 | I-近错 | insufficient_evidence | sadness | ⚠ 1 | [A08_Deborah_mom-s-old-house.md](conv-48/A08_Deborah_mom-s-old-house.md) |
| A09-H | conv-49 | H | history_supported | comfort | 通过 | [A09_Evan_the-little-plant-on-my-desk.md](conv-49/A09_Evan_the-little-plant-on-my-desk.md) |
| A09-CF | conv-49 | I-无历史关联 | insufficient_evidence | comfort | 通过 | [A09_Evan_the-little-plant-on-my-desk.md](conv-49/A09_Evan_the-little-plant-on-my-desk.md) |
| A09-P | conv-49 | P | present_cause_sufficient | comfort | 通过 | [A09_Evan_the-little-plant-on-my-desk.md](conv-49/A09_Evan_the-little-plant-on-my-desk.md) |
| A09-NM | conv-49 | I-近错 | insufficient_evidence | comfort | 通过 | [A09_Evan_the-little-plant-on-my-desk.md](conv-49/A09_Evan_the-little-plant-on-my-desk.md) |
| A10-H | conv-50 | H | history_supported | joy | 通过 | [A10_Calvin_the-octopus-guitar.md](conv-50/A10_Calvin_the-octopus-guitar.md) |
| A10-CF | conv-50 | I-无历史关联 | insufficient_evidence | joy | 通过 | [A10_Calvin_the-octopus-guitar.md](conv-50/A10_Calvin_the-octopus-guitar.md) |
| A10-P | conv-50 | P | present_cause_sufficient | joy | 通过 | [A10_Calvin_the-octopus-guitar.md](conv-50/A10_Calvin_the-octopus-guitar.md) |
| A10-NM | conv-50 | I-近错 | insufficient_evidence | joy | 通过 | [A10_Calvin_the-octopus-guitar.md](conv-50/A10_Calvin_the-octopus-guitar.md) |
