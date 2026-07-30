# MTM v0.7 — CORE

> **一條 lifecycle 的單一規格。** 取代「Contract / Arch / Verify 三份各自為政」的心智模型——它們其實是同一條 pipeline 的三個 phase。
> 為 agentic AI coding 設計，對治兩個復發失效：**hallucination**（叫不存在的 API/entity）與 **architectural drift**（step 3 的決定被 step 15 默默推翻）。
> v0.2 起 MTM **self-hosting**：它用自己的 `revisit_trigger` 機制隨案件經驗 + user 討論而進化（見 `EVOLUTION.md`）。

> 觸發詞：「用 MTM 做 ___」。fast-path 全程啟用——條件滿足的 phase 在數十秒內通過，不收 ceremony tax。

> **本檔是入口（脊椎）。** 舊三份保留為各 phase 的延伸細節：`MTM-Arch.md` = phase 1-2（grounding / 架構對話 / ADR）細節、`MTM-Verify.md` + `MTM-VERIFY-REPORT-TEMPLATE.md` = phase 6（獨立 audit）細節。先讀 CORE，需要展開某 phase 再翻對應細節檔。

---

## 1. 核心不變式（invariants）

1. **每一欄必填；`N/A` 合法；「不知道」寫成 `UNKNOWN: <為什麼>`，不准留空。**
2. **任何 ungrounded 的關鍵斷言 → 必須 escalate。** 同一套 anti-hallucination 機制，套在 task 層（欄位 `verified_by`）與架構層（`project-architecture/` grounding）。
3. **machinery 留在內部。** 對 user 只顯露：現在做什麼 / 為什麼 / 大概多久 / 需要你做什麼。內部標籤（confidence / DIVERGENT / ARCH_VIOLATED…）一律轉 user 語言。
4. **artifact 外部化優於 session memory。** contract 落檔、audit 對著檔案跑——不靠對話記憶（證據：nicemeet E7.1「audit 不再依賴 session memory」）。
5. **escalation 階段改方向，成本趨近於零；implementation 階段改方向，成本是 rollback。** 把判斷往前推。
6. **驗證是「執行」不是「宣告」（v0.3）。** `verified_by` / `observed_result` 必須指向**本 session 真的跑過的東西**（grep/read 結果、指令輸出、測試或 build log、實際觀察值），**不准在 promise 上標 PASS**。沒真正執行的 → 醒目標 `UNVERIFIED` 並讓它活進 phase 6 audit。理由：對強模型，失效不是「不填欄位」，是「把欄位填得很有說服力、底下的查根本沒做」——填了 plausible 值的欄位跟真閉合的欄位長得一樣，這條讓它們**長不一樣**。
7. **客戶核心需求優先（v0.5 · #13）。** 使用者**字面講出來的核心體驗需求**——那個「工具之所以存在的理由」（例：貝斯 App 的「真實貝斯音色」、相機 App 的「拍得清楚」）——是**一等交付物**，不可降級成佔位 / TODO。
   - 現成的真實方案唾手可得時（免費取樣庫 / soundfont / 現成 API），**預設直接交付真的**，不先擺佔位。
   - 真的必須延後 → 在 confirm 階段當**頭條「還不能做」明示**，不准默默 TODO 掉。
   - 與 #11 的關係：「便宜的可延後」只適用**次要**功能；**核心體驗需求永不延後**。
   - 警訊（altitude error）：架構顧得很好、卻把使用者「來就是為了這個」的東西擺成 placeholder——結構對、但沒交付他真正要的。
   - 證據：bass-app A/B 對照——無 MTM 版用線上 soundfont 當場交付「真實音色」，MTM 版只擺合成佔位，在使用者字面核心需求上輸了。

---

## 2. Lifecycle（0 → 6）

| # | Phase | 觸發 | 產出 | fast-path |
|---|---|---|---|---|
| **0** | Classify | 需求進來 | blast-radius 分級 → 決定跑到哪層；**綠地一句話 → 走 Plan 分支** | trivial → 直接做，跳全部 |
| **0-Plan** | Plan（綠地分支） | `project-architecture/` 空 **且** 一句話要一個產品 | 把難回頭的地基 fork 用生活語言問清 → 寫 `project-architecture/` + UNKNOWN 標記 → 交棒 phase 1（細節見 `MTM-Plan.md`） | 使用者已自己定的 fork 逐條 fast-path 跳過 |
| **1** | Ground | 非 trivial | 架構斷言 grounded；不足則對話建檔進 `project-architecture/` | 全 grounded → 30 秒過（Plan 已寫好 invariants/domains/glossary 時即走此路） |
| **2** | Escalate | 有未定 / 有選項 | 共識（選定路徑、scope、ADR 檔名） | 無歧義 → 跳過 |
| **3** | Contract | phase 2 後 | 單一 artifact（status header + 11 欄，§4） | 完全落在既有 ADR → 引用即可 |
| **4** | Implement | phase 3 後 | shipped code | — |
| **5** | Self-check | phase 4 後 | 對 clause 標 PASS/FAIL/MUTATED + 填 `observed_result` | — |
| **6** | Verify | 高 blast-radius / 動權限/安全/schema/上架 | 獨立 context 的 auditor 報告（§6） | 低風險 task → 可省略 |

### Phase 0 · Classify（blast-radius 分級——「完整」= 正確分級，不是每次全做）
| 級別 | 判準 | 跑到哪 |
|---|---|---|
| **T0 trivial** | typo / 字串 / bump / 單檔 <20 行 / 純樣式 | 不寫 contract，直接做 |
| **T1 local** | 單模組、不碰下列任一觸發 | **最小可行 contract**（只 3 條承重欄，見下）→ 1→3→4→5 |
| **T2 structural** | 碰 domain / boundary / 跨模組契約 / 新 entity | 完整 contract + phase 1 建檔 + phase 2 架構對話 |
| **T3 critical** | 動權限·安全 / schema migration / 上架 / 多租戶可見性 | 完整 contract + 全 7 phase，**phase 6 強制獨立 Verify** |

**分級靠可觀察觸發、不靠 AI 主觀判斷（v0.3 · #10）**——命中任一即升級，AI **不准合理化掉**：
碰 auth/權限/secret? · 有 DB migration / schema 變動? · 跨 ≥2 個 domain? · 改 ≥N 檔(專案自訂門檻)? · 動到多租戶可見性 / 金流 / 上架資產? · intent 字面 ≠ 資料模型(phase 2 候選集合)?
> **T3 不可自降。** 「寫 contract 比寫 code 久 → 降級」只適用 T0↔T1，不適用 T2/T3。

**最小可行 contract（v0.3 · #11）**：T1 預設只填三條**承重欄**——`intent` + `escalation/candidate-set` + `affected_layers`——讓高價值的 20% 摩擦趨近零、永遠不會因嫌麻煩連它一起跳過。其餘欄位（schema_assumptions / cross_module / test_plan…）強模型本來就會做，T1 可省，T2/T3 才補滿。

### Phase 0-Plan · 綠地分支（v0.4 · 細節見 `MTM-Plan.md`）
**觸發（可觀察雙訊號）**：`project-architecture/` 空且無 source tree **且** 請求是「要做一個產品」而非「對既有東西的範圍變更」。小白與否不另設 gate——使用者已自定的 fork 逐條 fast-path 跳過。
**做什麼**：**開場第一步先問一個開放的目的題**（「你做這個最想達成什麼?」）定靈魂與方向（接 invariant 7）；此為**唯一**預設開放問的題（v0.7 · #15，僅綠地、不主動提延伸功能），答案接線進 handoff 當「靈魂註記」並決定哪些 fork 先問、哪個 feature 受 invariant 7 保護，答得空泛就退回 fork 機制不盤問。再攤**難回頭**的地基 fork（裝置能力·平台 / 資料持久·跨裝置 / 孤島vs整合 / 單人vs多人 / 租戶隔離 / 法規·落地），便宜的自己推 default 收進「我先這樣假設」區塊；難回頭的用「想像 A vs B 你是哪個」逼使用者選、不用「對嗎」逼點頭；4 個永不靜默 default（持久·跨裝置 / 多人登入 / 誰看得到誰 / 碰錢或他人個資）。確認用「第一天能做/還不能做」而非骨架。
**分界線（Plan fork vs phase-2 candidate-set）**：Plan fork 的答案決定**會有哪些 domain/entity**（先於、生成資料模型）；phase-2 是把 intent 對映到**已決定的模型**上。測試：「有資料模型可列舉候選嗎？」沒有→Plan、有→phase-2。
**Handoff（硬性）**：Plan 把結論寫成 phase 1 的詞彙——`invariants.md`（不可逆 fork 寫成硬規則）/ `domains/` / `glossary.md` / `decisions/`（每個帶 trade-off 的 fork 一份 seed ADR）/ `INDEX.md`，未解 fork 一律 `UNKNOWN: <why>`。phase 1 於是 fast-path，不重問。**Plan 絕不自決 fork，問不出來就標 UNKNOWN，不准猜。**

### Phase 1 · Ground
讀 `project-architecture/`（INDEX / invariants / glossary / domains/* / 最近 5 份 decisions）。列本需求的「架構斷言」。對每條問：依據在哪份文件哪一段？**ungrounded 的關鍵斷言**（影響 domain 歸屬 / boundary / 資料 ownership / invariant 適用 / domain language 對應）→ escalate，每輪最多 3 題、每題附「為什麼要釐清」，答完即建檔（規則見舊 Arch §Stage 0，已併入此處）。

### Phase 2 · Escalate（一等 phase——投報率最高，別埋）
1. **Candidate-set 檢查（子協議）**：intent 的字面，跟資料模型對得上嗎？對不上 → **列舉候選集合讓 user 精選，不准直譯**。
   > 證據：E9.7「批次發名片」→ 攤開 ABCD 四類候選人；D-reinvite v1 過窄 → 攤開 lost/lazy/deleted/account-switch。直譯會做出過窄的東西。
2. **真實選項**：給 `PROCEED / REFACTOR_FIRST / SCOPE_SPLIT / ESCALATE`，每個講 trade-off。由 user 選。
3. **內部 red-team pass（強制）**：內心過一遍「我要反對 user 方向，最強的反對是什麼？有實質嗎？」——這步**不可省**，它擋 sycophancy（共識假達成）。
4. **外露條件式**：有實質才 surface；沒實質**不准**硬擠 contrarian。
   > 拆解理由：TRIAL_LOG 12 筆裡，零筆高價值事件來自「AI 製造的反對」；全部來自「AI 攤真實選項 + user reframe」。強制外露會製造噪音 → cry-wolf → 真該擋的那次被當噪音跳過。所以**內部強制、外露條件**。

出口：AI 複述共識 + ADR 檔名，user 確認。T2/T3 寫 ADR 到 `project-architecture/decisions/YYYY-MM-DD_<domain>_<desc>.md`。

### Phase 4 · Implement（三條紀律）
1. 不准用 flag / toggle / 隱藏欄位蓋過 ADR boundary。
2. 實作中發現必須穿越 boundary → halt，回 phase 2。
3. 超出 `affected_layers` 的修改，先回報後動作（no silent patch）。

### Phase 5 · Self-check（便宜、inline）
對 contract 每條 clause 標 `PASS / FAIL / MUTATED`，**並填 `observed_result`**（不是「做完了」，是「實際觀察到 X：log 行 / 截圖 / Sentry breadcrumb / query 數」）。MUTATED 合法，附一行為什麼。
**執行綁定（v0.3 · #9，硬規則）**：一條 clause **不准在 `observed_result` 還是 promise / `PENDING` 時標 `PASS`**。要嘛貼上本 session 真跑出來的證據才 PASS，要嘛標 `UNVERIFIED` 並把它帶進 phase 6 audit 當未閉合項。`PENDING` 是「尚未驗」的中繼狀態，**不是通過**。

### Phase 6 · Verify（獨立 context——這是 gate，不是自評）
**必須換一個乾淨的 agent**（subagent / 另開 session），只餵三樣：contract、ADR、git diff。不准是 executor 對話的延續（否則 auditor 帶著 executor 的 rationalization = 表演）。產出 §6 報告。`ARCH_VIOLATED`（能跑但違反 ADR/contract）是唯一最重判定，需 rollback 或立即 ADR 修訂。
> v0.1 的「Stage E Layer 2 自評四題」併入此處：self-check（phase 5）留給 executor，audit（phase 6）交獨立 agent。同一個「audit」不再分裂在兩份文件。

---

## 3. 單一 artifact 原則
一份 contract 從 phase 1 長到 phase 6，**`status` header 全程是單一真相**。agent resume（context summary 後）先讀 status，就知道「現在在哪、卡在哪、哪些 precondition 還沒閉合」。這直接對接 MTM 的原始動機：對抗跨 step 的 drift。

---

## 4. Template（canonical——實戰 11 欄，含驗證鏈）

```markdown
# MTM Contract: <task + 一句話>

## status
stage= | blast_radius=T0/T1/T2/T3 | blocked_on=[] |
unverified_preconditions=[] | open_escalations=[]

## intent
<一句話、動詞開頭、可觀察。不是「實作 X」，是「user 點 X 看到 Y」>

## affected_layers
<逐層列改 / 不動：entity / service / endpoint / migration / cron·push /
 provider / screen / cache / web-admin·platform-admin / env·secrets>

## preconditions
- <條件>   verified_by: <commit / migration / 手測 / staging health / ...>
  （任一 unverified → 動手前先閉合）

## schema_assumptions
- <假設>   source: <SPEC §X / entity 註解 / commit / TD-Y>  （無 source → confidence 降一級）

## cross_module_contract
emit / listen / 我假設別人做 / 別人假設我做

## expected_outcome
- <可觀察結果>
  verifiable_by: <怎麼驗：手測步驟 / 測試 / log / breadcrumb>
  observed_result: <本 session 真跑出的證據 | 尚未驗 = PENDING(不得標 PASS) | 無法驗 = UNVERIFIED(帶進 audit)>   ← v0.3 執行綁定

## confidence
overall: high/medium/low ；低信心子題：<子題 + 為何不確定 + 怎麼處理>

## escalation
等 user 拍板：<列舉，不自決> ；立刻停下回報：<列舉，不硬解>

## grounding
<SPEC / ARCHITECTURE / ADR / commit / 對話原文>  （無 → 標 SPECULATIVE）

## rollback_plan
code / schema / env

## test_plan
local / staging / prod
```
> `verified_by`（前提）、`verifiable_by`→`observed_result`（結果）、`source`（假設）這三組才是「精密執行 + 詳細驗證」的本體。v0.1 公開 TEMPLATE 把它們藏成細節——v0.2 foreground。

---

## 5. 對話 UX 紀律（跨所有 phase）
1. 起手 invite 對話、不報流程；不對 user 講 phase 代號。
2. 內部標籤全轉 user 語言（confidence/DIVERGENT/REFACTOR_FIRST/ARCH_VIOLATED…）。
3. 歸檔一次性歸納、不逐條問；不確定歸哪 → 明示問，不 silent 歸檔。
4. phase 切換給 summary 後停下等 user（fast-path 跳過的不必等）。
5. **Forced disagreement → 內部強制 red-team、外露條件式**（見 phase 2 step 3-4）。
6. phase 6 結果只 surface 對 user actionable 的部分，不 dump 全部 YES/NO。
> Meta 原則（衝突時 fallback）：machinery 留內部，對 user 只露 what / why / how-long / need-from-you。

---

## 6. Contract ↔ Verify 脊椎（10 失效 ↔ 該擋它的欄位）
Verify 不是另一張獨立 checklist——它是「每個預防欄位實際有沒有守住」。原型是 nicemeet WORKFLOW §1 的 TD 表，這裡泛化到 10 modes：

| # | Vibe-coding 失效 | 本該擋住的 contract 欄位 |
|---|---|---|
| 1 | API 假串接 / payload 對不齊 | `cross_module_contract`（emit/listen 對齊） |
| 2 | 連帶損害（偷改 affected_layers 外） | `affected_layers` 邊界 |
| 3 | 邊界條件未定義 | `expected_outcome` + `schema_assumptions` |
| 4 | 重構遺留 bug / 斷層 | `test_plan` + phase 5 `observed_result` |
| 5 | Happy-path 偏誤（漏 500/timeout/權限/empty） | `expected_outcome`（負路徑） |
| 6 | 殘留 mock / TODO（phantom code） | phase 5 髒話掃描 |
| 7 | 環境/依賴脫節 | `affected_layers.env·secrets` |
| 8 | 權限/安全遺漏 | `preconditions`（requireAuth/isOwner）+ T3 gate |
| 9 | 效能地雷（N+1） | `schema_assumptions` + `expected_outcome.verifiable_by`（query 數） |
| 10 | 偷刪測試 | `test_plan` + diff 掃描 |
> auditor 行為：無情但客觀（列檔名行數即可）、不越俎代庖（只報不修，把 fix 留給 executor/human）、架構一致性最重（`ARCH_VIOLATED`）。報告模板見 `MTM-VERIFY-REPORT-TEMPLATE.md`，每個 section 標註它涵蓋上表哪幾個 mode。

---

## 7. 進化（self-hosting）
MTM 不是凍結的規格，是**會長大的**。引擎在 `EVOLUTION.md`，四段閉環：
1. **Case ledger（硬 gate · v0.6 #14）**：每個非 T0 task **append 一行才算 done**——未 append 不算完成（與 phase 5「執行綁定」同邏輯：軟紀律會開天窗，故綁硬 gate；nicemeet trial log 結算表從沒填即前例）。記：一次過？幻覺數？哪個欄位抓到/漏掉什麼？escalation 價值？ledger 位置由消費端專案自訂（§A）。
2. **Proposal queue**：當一個 pattern 復發、或 user/auditor 點出規格缺口 → 提案進 queue（**status: pending-signoff**）。
3. **討論 gate**：提案**不自動生效**。跟 user 討論後才 promote 進 CORE——進化的 gate 在人，不在 AI。
4. **Changelog + 版本 bump**：promote 時記 changelog、bump 版本。

這就是 MTM 自己的 `revisit_trigger / needs_revisit` 反身套用：方法論被它自己的紀律治理。

---

*MTM v0.7 — 統一 lifecycle（CORE 當脊椎、舊三份 + `MTM-Plan.md` 保留為 phase 細節）+ self-hosting 進化引擎（`EVOLUTION.md`）。*
*v0.2 #1–#7 / v0.3 #9–#11 / v0.4 #12（綠地 Plan）/ v0.5 #13（客戶核心需求優先，invariant 7，由 bass-app A/B 對照實驗得出）/ v0.6 #14（case-ledger append 硬 gate）/ v0.7 #15（綠地 Plan 開場「先問目的」+ discovery 覆蓋）。#8 仍 pending。*
