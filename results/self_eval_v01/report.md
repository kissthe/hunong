# 评测结果 · self_eval_v01 · self

## 主表

| 条件 | 题数 | T1 macro-F1 (95% CI) | T1 准确率 (95% CI) | T2 线索 | T3 召回 | T3 精确(严/宽) | T3 session 命中 | 联合正确 | 误归因率 (95% CI) | 情绪准确率 |
|---|---|---|---|---|---|---|---|---|---|---|
| x_only | 38 | 0.59 [0.54, 0.63] | 0.74 [0.61, 0.87] | 0.00 | 0.00 | 0.00/0.00 | 0.00 | 0.00 | 0.00 [0.00, 0.00] | 1.00 |
| full_history | 38 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 | 0.95 | 0.66/0.81 | 1.00 | 1.00 | 0.00 [0.00, 0.00] | 1.00 |
| evidence_only | 30 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 | 0.95 | 0.66/0.81 | 1.00 | 1.00 | 0.00 [0.00, 0.00] | 1.00 |

## 条件差值

- Δ(full_history − x_only) T1 macro-F1 = **+0.41**（38 题）
- Δ(evidence_only − full_history) T1 macro-F1 = **+0.00**（同一批 30 题）
- 成对一致率（H 与对应 I-无历史关联都答对）：full_history 1.00（8 对）

## 每类 P/R/F1 与混淆矩阵

**x_only**

| 类 | P | R | F1 | 支持数 |
|---|---|---|---|---|
| H | 0.00 | 0.00 | 0.00 | 10 |
| P | 1.00 | 1.00 | 1.00 | 10 |
| I | 0.64 | 1.00 | 0.78 | 18 |

| gold \ 预测 | H | P | I | parse_fail |
|---|---|---|---|---|
| H | 0 | 0 | 10 | 0 |
| P | 0 | 10 | 0 | 0 |
| I | 0 | 0 | 18 | 0 |

**full_history**

| 类 | P | R | F1 | 支持数 |
|---|---|---|---|---|
| H | 1.00 | 1.00 | 1.00 | 10 |
| P | 1.00 | 1.00 | 1.00 | 10 |
| I | 1.00 | 1.00 | 1.00 | 18 |

| gold \ 预测 | H | P | I | parse_fail |
|---|---|---|---|---|
| H | 10 | 0 | 0 | 0 |
| P | 0 | 10 | 0 | 0 |
| I | 0 | 0 | 18 | 0 |

**evidence_only**

| 类 | P | R | F1 | 支持数 |
|---|---|---|---|---|
| H | 1.00 | 1.00 | 1.00 | 10 |
| P | 1.00 | 1.00 | 1.00 | 10 |
| I | 1.00 | 1.00 | 1.00 | 10 |

| gold \ 预测 | H | P | I | parse_fail |
|---|---|---|---|---|
| H | 10 | 0 | 0 | 0 |
| P | 0 | 10 | 0 | 0 |
| I | 0 | 0 | 10 | 0 |

## 误归因率（按题型）

| 题型 | x_only | full_history | evidence_only |
|---|---|---|---|
| I_near_miss | 0.00 (n=10) | 0.00 (n=10) | 0.00 (n=10) |
| I_no_history | 0.00 (n=8) | 0.00 (n=8) | — |
| P_same_cue | 0.00 (n=10) | 0.00 (n=10) | 0.00 (n=10) |
| all_P_or_I | 0.00 (n=28) | 0.00 (n=28) | 0.00 (n=20) |

## 逐题结果

| sample_id | 题型 | gold | x_only | full_history | evidence_only | full_history 线索 / 证据 |
|---|---|---|---|---|---|---|
| conv-26_A01-CF | I_no_history | I | I ✓ | I ✓ | — |  |
| conv-26_A01-H | H | H | I ✗ | H ✓ | H ✓ | cue_caroline_grandma_s_necklace / D4:3（gold D4:3） |
| conv-26_A01-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-26_A01-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |
| conv-30_A02-CF | I_no_history | I | I ✓ | I ✓ | — |  |
| conv-30_A02-H | H | H | I ✗ | H ✓ | H ✓ | cue_gina_tattoo_arm / D5:13, D5:15（gold D5:15） |
| conv-30_A02-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-30_A02-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |
| conv-41_A03-CF | I_no_history | I | I ✓ | I ✓ | — |  |
| conv-41_A03-H | H | H | I ✗ | H ✓ | H ✓ | cue_john_little_childhood_doll / D5:13（gold D5:13） |
| conv-41_A03-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-41_A03-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |
| conv-43_A04-CF | I_no_history | I | I ✓ | I ✓ | — |  |
| conv-43_A04-H | H | H | I ✗ | H ✓ | H ✓ | cue_john_old_basketball_shoes / D6:9, D6:11（gold D6:11） |
| conv-43_A04-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-43_A04-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |
| conv-44_A05-H | H | H | I ✗ | H ✓ | H ✓ | cue_audrey_tattoos_four_dogs / D3:26, D3:28, D3:30（gold D3:26, D3:28） |
| conv-44_A05-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-44_A05-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |
| conv-47_A06-CF | I_no_history | I | I ✓ | I ✓ | — |  |
| conv-47_A06-H | H | H | I ✗ | H ✓ | H ✓ | cue_john_old_drum_set / D24:15, D24:17（gold D24:15） |
| conv-47_A06-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-47_A06-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |
| conv-48_A07-CF | I_no_history | I | I ✓ | I ✓ | — |  |
| conv-48_A07-H | H | H | I ✗ | H ✓ | H ✓ | cue_jolene_paris_pendant / D1:6, D1:8（gold D1:8, D1:10） |
| conv-48_A07-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-48_A07-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |
| conv-48_A08-H | H | H | I ✗ | H ✓ | H ✓ | cue_deborah_mom_s_old / D1:3, D1:5, D1:7, D2:13, D2:15（gold D1:5, D2:13） |
| conv-48_A08-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-48_A08-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |
| conv-49_A09-CF | I_no_history | I | I ✓ | I ✓ | — |  |
| conv-49_A09-H | H | H | I ✗ | H ✓ | H ✓ | cue_evan_little_plant_desk / D5:17, D5:19（gold D5:17） |
| conv-49_A09-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-49_A09-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |
| conv-50_A10-CF | I_no_history | I | I ✓ | I ✓ | — |  |
| conv-50_A10-H | H | H | I ✗ | H ✓ | H ✓ | cue_calvin_octopus_guitar / D16:14, D16:16（gold D16:14, D16:16） |
| conv-50_A10-NM | I_near_miss | I | I ✓ | I ✓ | I ✓ |  |
| conv-50_A10-P | P_same_cue | P | P ✓ | P ✓ | P ✓ |  |

## 数据可用性检查（第 8 节）

- x_only T1 macro-F1 = 0.59（门槛 ≤ 0.5）：未通过
- x_only 下答对的 H 题：无
- Δ(full − x_only) = +0.41（门槛 ≥ 0.15）：通过
- evidence_only ≥ full_history（同批题）：成立
- 情绪：gold 情绪全部落在 4.3 节枚举内：是

