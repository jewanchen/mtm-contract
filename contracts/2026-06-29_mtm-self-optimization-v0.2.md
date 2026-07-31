# MTM Contract: MTM 自我優化 → v0.2（self-hosting / evolving）

> 這份 contract 是 MTM 跑在 MTM 自己身上的範例。它同時是 v0.2 的第一筆 case ledger 紀錄。

---

## status
```
stage          = DONE（Q1/Q2 拍板、v0.2 promoted）
blast_radius    = HIGH（動到方法論本體 + 公開 repo）
depth_selected  = Classify + Ground + Escalate + Contract + Implement + Self-check + Verify
blocked_on      = []
unverified_preconditions = []
open_escalations = []
resolved        = Q1=CORE 當脊椎、舊三份保留 ｜ Q2=inline 機會主義 + 兩道測試(實質+通用) + 點頭才升
```

## intent
把 MTM 三份文件（Contract / Arch / Verify）優化成**單一 lifecycle 的 v0.2**，並讓它能「隨案件經驗累積 + 跟 user 討論後」持續進化——也就是把 MTM 自己的 `revisit_trigger / needs_revisit` 機制反身套用到方法論本體上。可觀察結果：repo 多出 `MTM-CORE.md`（v0.2 規格）+ `EVOLUTION.md`（進化引擎）+ 本 contract。

## affected_layers
- `MTM-CORE.md`：新增（v0.2 統一 lifecycle，吸收舊三份的內容）
- `EVOLUTION.md`：新增（case ledger + proposal queue + changelog + 進化協議）
- `contracts/2026-06-29_*.md`：新增（本檔，示範 + 第一筆 ledger）
- `MTM-Arch.md` / `MTM-Verify.md` / `TEMPLATE.md` / `README.md`：**暫不動**（unify 與否是 Q1，等拍板）
- examples / integrations / LICENSE / NOTICE：不動

## preconditions
- 已讀 nicemeet 56 份 contract + WORKFLOW + TRIAL_LOG（12 build-mode 樣本）
  verified_by: 本 session 直讀消費端專案本地的 contract 目錄、workflow 與 trial log
- 7 項調整方向 + forced-disagreement 拆解已在前兩輪對齊
  verified_by: 本 session 對話

## schema_assumptions
- 「實戰 template（11 欄含 verified_by / verifiable_by / test_plan / rollback）」比公開 TEMPLATE 強
  source: 消費端專案本地 workflow 文件 §3
- escalation 是投報率最高的 phase
  source: TRIAL_LOG E7.2 / E9.5 / D-reinvite 三筆最大價值事件皆發生於 escalation

## cross_module_contract
- emit：v0.2 不刪舊三份，舊讀者引用不斷
- 別人依賴我：未來每個 task 的 contract 會 append 一行進 `EVOLUTION.md` 的 case ledger
- 我假設 user 做：proposal queue 的條目由 user 討論後才 promote 進 CORE（進化的 gate 在人，不在 AI）

## expected_outcome
- v0.2 把舊三份收斂成「0 Classify → 6 Verify」一條線，audit 邊界不再分裂
  verifiable_by: `MTM-CORE.md` lifecycle 表 + Verify 併入 phase 6
  observed_result: ✅ CORE §2 lifecycle 表成形；Stage E Layer2 改為觸發 phase 6 Verify
- 7 項調整全部落地、forced-disagreement 拆成「內部強制 / 外露條件」
  verifiable_by: CORE 對照表逐條
  observed_result: ✅ 見本檔末「7 項落地對照」
- 進化引擎可運轉：case → proposal → 討論 → 版本 bump 四段閉環
  verifiable_by: `EVOLUTION.md` §A/§B/§C/§D
  observed_result: ✅ 已建；v0.2 自己列為 proposal queue 第一筆（status: pending-signoff）

## confidence
overall: medium
低信心子題：
- 打包方式（替換舊三份 vs 並存 vs 漸進 deprecate）= 影響 README/Arch/Verify 動不動 → **escalate Q1**
- promote 門檻（pattern 重複幾次才進 proposal）= 影響進化節奏 → **escalate Q2**

## escalation
等 user 拍板（不自決）：
- **Q1**：v0.2 跟舊三份的關係——CORE 取代三份 / CORE 當脊椎三份保留為 phase 細節 / CORE superset 後漸進 deprecate
- **Q2**：case ledger 的 pattern 要重複幾次、或由誰判定，才 promote 成 proposal
立刻停下回報：若 user 要的是「改進舊三份」而非「收斂成單一 lifecycle」——方向不同，停手重對。

## grounding
- 消費端專案本地 workflow 文件 §1（TD↔欄位表，phase 6 脊椎的原型）、§3（實戰 template）
- 該專案本地 ledger（escalation 最高價值的證據）
- 前兩輪對話：7 項調整 + forced-disagreement 判準

## rollback_plan
- code：三個檔皆新增，`git rm` 即還原，舊三份未動
- 無 schema / env

## test_plan
- 自查：本 contract 逐條 PASS/observed_result（見上）
- 討論：Q1/Q2 拍板後，依答案決定是否動舊三份 + 寫進 EVOLUTION changelog v0.2 正式 entry

---

## Self-check（對 clause 標記）
| clause | 標記 | observed_result |
|---|---|---|
| 統一 lifecycle | PASS | CORE §2 成形 |
| 7 項調整落地 | PASS | 見 CORE 對照 |
| forced-disagreement 拆解 | PASS | CORE §5 Rule 5 + 風險表改寫 |
| 進化引擎 | PASS | EVOLUTION 四段閉環 |
| 動舊三份 | MUTATED→HELD | 改為 escalate Q1，不自決 |

## 7 項落地對照
1. 實戰 template 升 canonical → CORE §3 + §4
2. observed_result 欄閉合驗證 → CORE §4 template（本檔已示範）
3. Verify 10-modes ↔ 欄位脊椎 → CORE §6
4. Stage E Layer2 → 觸發獨立 Verify → CORE §2 phase 5/6
5. blast-radius classifier 在最前 → CORE §2 phase 0
6. machine-readable status header → CORE §4（本檔頂部已示範）
7. escalation 升一等 phase + candidate-set 子協議 → CORE §2 phase 2 + §5
