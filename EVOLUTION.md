# MTM EVOLUTION — 進化引擎

> MTM self-hosting 的所在。`MTM-CORE.md` 是**當前**規格；這份檔案是讓它**隨案件經驗 + user 討論**長大的機器。
> 四段閉環：**Case ledger → Proposal queue → 討論 gate → Changelog + bump**。
> 鐵則：**proposal 不自動進 CORE。進化的 gate 在 user，不在 AI。**

---

## §D 進化協議（先讀這段——它定義另外三段怎麼動）

**何時 append case ledger（硬 gate · v0.6 #14）**：每個非 T0 的 task 跑完 phase 5/6 後，append §A 一行**才算 done——未 append 不算完成**（與 phase 5 執行綁定同邏輯；軟紀律會開天窗，nicemeet trial log 結算表從沒填即前例）。誠實計，幻覺數不算錯、是核心觀察值。

**何時開 proposal（進 §B）**——主模式 + 三條 backstop：
- **主模式（inline 機會主義 · Q2 拍板 2026-06-29）**：AI 在**執行任何 task 的過程中**，一看到方法論本身有實質改善機會，就**當場用白話**提出「論點 + 原因」給 user。不必等復發、不必等盤點。
  - **升規則必過兩道測試（缺一不可）**：
    1. **實質**（繼承 phase 2 Rule 5）：真改善，還是教科書式微調？沒料不提。
    2. **通用 / 跨任務**（2026-06-29 補）：這條對**未來各類 task 都成立**，還是只在補**這一次單一事件**的洞？規則必須是 cross-task general，**不准針對單一事件就加規則**。
  - **單一事件 → 進 §A case ledger 當資料點，不升成規則。** 要等它顯出跨任務 pattern（用論證說明它本來就通用、或 backstop① 復發證明）才提案。
  - 理由：inline 機會主義若無「通用性」閘門，會退化成**逐事件打補丁**——規格越長越碎，正是 MTM 自己要防的「每段都對、組合方式錯」之方法論版。
- backstop ①：同型 gap 在 ledger **復發 ≥ 2 次**仍沒被 inline 抓到 → 補提。
- backstop ②：phase 6 auditor 指出 CORE 規格本身（非 task）的缺口。
- backstop ③：半年盤點 >6 個月沒被任何 case 引用的規則 → 提案「刪或重寫」。

**討論 gate（進 §C / CORE 的唯一路徑）**：
- AI 白話提案（論點 + 原因 + 影響面），**user 點頭 → 即升為規則**：promote 進 `MTM-CORE.md` + 記 §C changelog + bump 版本。
- user 想再想 / 沒當場拍 → 進 §B `pending-signoff` 停著，不入 CORE。
- **AI 不准自己把未點頭的 proposal 寫進 CORE。** gate 永遠在 user。

**版本規則**：
- patch（v0.2.x）：措辭 / 範例 / 補 case，不改機制。
- minor（v0.x）：加/改 phase、欄位、紀律。
- major（vX）：lifecycle 結構性重構。
promote 時：改 `MTM-CORE.md` + 記 §C changelog + bump 版本號 + 在被改的 case ledger 行標 `→ 觸發 proposal #N`。

---

## §A Case Ledger（append-only）

> 欄位：Date | Task | Tier | 一次過? | 幻覺數 | 哪個欄位抓到/漏掉什麼 | escalation 價值 | → proposal?

> **位置規則（v0.6 #14）**：本 §A 只記**對 MTM 本身的改動**（dogfooding）；**消費端專案的 task ledger 放各自專案本地**（如 NiceMeet → 該專案本地 ledger，user 2026-06-30 拍板）。

**Seed（nicemeet 試行，2026-05-14 起，完整見 該專案本地 ledger；總計 56 份 contract）**

| Date | Task | Tier | 一次過 | 幻覺 | 關鍵觀察 | escalation 價值 | proposal |
|---|---|---|---|---|---|---|---|
| 05-14 | E3.2 推播鏈路 | T2 | ✅ | 0 | `cross_module` 抓到 `notifyContactsOfUpdate` 已存在、免重複 | 浮現 D-1/2/3 | — |
| 05-14 | E5 公司資料管理 | T2 | ✅ | 0 | `affected_layers` 抓到 entity+types 有但 DTO 漏接的 silent drift | actor≠owner 才寄信 | — |
| 05-14 | E8 Dashboard 重設計 | T2 | ✅ | 0(1 compile-time) | tsc 抓到 `submittedAt` vs `createdAt` 誤用 | 4 題前置 escalation | — |
| 05-14 | E9.7 批次操作 | T2 | ✅ | 0 | **intent 字面 vs 資料模型對不上** → 攤開 ABCD 候選人 | 最高：scope 精準化 | → #6 candidate-set |
| 05-14 | E9.5 離職名單回收 | T3 | ✅ | 0 | 新 entity+migration | **最大 redesign**（單向→資料庫）在 escalation 零成本 | → #6 |
| 05-16 | E7.2 預告變更 | T2 | ✅ | 0 | — | **user 推翻我的 escalation 結構本身**、unified 設計 | → #5 forced-disagree |
| 05-16 | D-reinvite | T3 | ✅ | 0 | acceptInvitation idempotent | escalation 觸發架構決定 D-6 + AI-1 | → #6 |

**觀察彙整（→ 種出 v0.2 的 proposal）**：12 build-mode 樣本，**幻覺事件 0**（少數 compile-time 即抓）、**一次過 commit 12/12**。最高價值一律落在 escalation phase，且皆為「AI 攤真實選項 + user reframe」，**無一來自 AI 製造的反對**。

| Date | Task | Tier | 一次過 | 幻覺 | 關鍵觀察 | proposal |
|---|---|---|---|---|---|---|
| 2026-06-29 | MTM 自我優化 v0.2 | T3 | 進行中 | 0 | 用 MTM 跑 MTM；status header + observed_result 首次實戰 | = #1（本批） |

| 2026-06-29 | 三方獨立評價 MTM(adoption/方法論/對抗) | T2 | — | — | 評價收斂:承重樑=escalation/candidate-set + 獨立 audit + artifact>memory;最大缺口=驗證「宣告≠執行」、自分級 self-defeating | → #9/#10/#11 |

| 2026-06-29 | MTM Plan 設計 + 三方評審 | T2 | — | — | gap 確認真;補強=孤島vs整合 fork + 想像式問法 + 4 永不default + handoff 寫 phase-1 詞彙 | → #12 promoted v0.4 |

| 2026-06-29 | **bass-app A/B 對照**(MTM vs 無 MTM,同一句話) | T2 | — | — | **MTM 首個真正 control**。中立 agent 裁:意圖吻合 ≈5/5 vs 2穩1半2失;MTM 翻對「原生vs網頁」(最高風險決定)、「音階格vs指板";但「真實音色」MTM 擺佔位、無 MTM 接 soundfont 當場交付→輸。誠實:點數獲勝非 KO | → #13 promoted v0.5 |

| 2026-06-30 | MTM 自我優化 v0.6(ledger 硬 gate + 版本標籤修) | T2 | ✅ | 0 | nicemeet 6 週效益分析發現 trial log 結算從沒填→「軟紀律會開天窗」是跨任務 pattern；CORE/README 殘留 v0.2(MTM 自己也 drift) | ledger append 從軟紀律升硬 gate | → #14 promoted v0.6 |

| 2026-07-05 | MTM-Plan 加開場「先問目的」discovery(#15) | T2 | ✅ | 0 | 現有 Plan 直接跳 fork、缺目的(靈魂)錨點;user 裁:延伸功能不提、僅綠地 | 目的先問=接 #13 靈魂的開場錨點 → #15 promoted v0.7 |

<!-- 新 case append 在這行之上 -->

---

## §B Proposal Queue（pending-signoff）

> 每筆：證據 → 提案改動 → 影響面 → 狀態。**v0.2 自身就是第一批提案**，等你拍板後才從 draft 轉正、寫進 §C。

### #1 — 統一 lifecycle（CORE 當脊椎、舊三份保留為 phase 細節）  `✅ promoted v0.2 (2026-06-29)`
- 證據：實戰只有一份 WORKFLOW 在跑，Stage E/F 是長出來的；舊三份的「audit」分裂在 Arch §Stage E 與 Verify。
- 改動：`MTM-CORE.md` 0→6 lifecycle 為單一入口；Stage E Layer2 併入 phase 6 獨立 Verify。
- **Q1 拍板**：CORE 當脊椎，`MTM-Arch.md`（phase 1-2 細節）/ `MTM-Verify.md`（phase 6 細節）/ `TEMPLATE.md` **保留**，加 header 指回 CORE，舊引用不斷。

### #2 — `observed_result` 欄（閉合驗證鏈）  `✅ promoted v0.2 (2026-06-29)`
- 證據：`verifiable_by` 是承諾不是紀錄；E3.2 寫了「看 outbound call 數」卻無欄位收那個數字。
- 改動：template 每個 outcome 加 `observed_result`（實際看到什麼 + 證據）。
- 影響：低、純增量。

### #3 — Contract↔Verify 脊椎（10 modes ↔ 欄位）  `✅ promoted v0.2 (2026-06-29)`
- 證據：WORKFLOW §1 的 TD↔欄位表已證明可行（TD-18/19/20/21）。
- 改動：CORE §6 泛化到 10 modes；report 每 section 標涵蓋哪幾個 mode。
- 影響：中，Verify 從獨立 checklist 變「欄位有沒有守住」。

### #4 — blast-radius classifier（phase 0）  `✅ promoted v0.2 (2026-06-29)`
- 證據：實戰憑直覺分級（pure-doc D-5 輕、three-domain-isolation 全 Stage E）。
- 改動：CORE phase 0 的 T0–T3 表，route 深度。
- 影響：中，「完整」重定義為「正確分級」。

### #5 — forced-disagreement 拆成「內部強制 / 外露條件」  `✅ promoted v0.2 (2026-06-29)`
- 證據：TRIAL_LOG 零筆高價值來自 AI 製造的反對；硬擠 contrarian → cry-wolf。
- 改動：phase 2 step 3-4；舊「已知風險」表那行的 mitigation 改指「內部 red-team pass」。
- 影響：低，但修掉 v0.1.1↔Rule 5 的殘留矛盾。

### #6 — escalation 升一等 phase + candidate-set 子協議  `✅ promoted v0.2 (2026-06-29)`
- 證據：E9.7 ABCD、D-reinvite 四類——「intent 字面 vs 資料模型」是反覆出現的 bug 來源。
- 改動：CORE phase 2 為一等 phase，candidate-set enumerate 寫成子協議。
- 影響：中，把最高價值步驟從 sub-rule 提為 phase。

### #7 — machine-readable status header（resumability）  `✅ promoted v0.2 (2026-06-29)`
- 證據：原始動機 step3≠step15；agent context summary 後需單一真相入口。
- 改動：template 頂 `status` 塊（stage/blocked_on/unverified/open）。
- 影響：低、純增量，對 agentic 長任務價值高。

### #8 — phase 0 加第二條軸:複雜度/可拆解性(與 blast-radius 並列)  `pending-signoff`
- 證據:blast-radius 與複雜度正交。E9.5 高 blast **且** 高複雜度(redesign);E3.2 T2 blast 但複雜度低(grep 完單一 unknown 即清)。高 blast/低複雜度(改一行 auth)是純複雜度分析會漏、blast-radius 才抓的格子。
- 改動:phase 0 從一條軸(T0–T3 blast)變 2 軸——blast 決定**驗證深度**、複雜度決定**拆解 + grounding 深度**;輸出綁死「拆 or 不拆」決定。
- 訊號**具體可數**(反表演化):跨幾個 domain / intent 字面≠資料模型? / 幾個獨立 unknown / 可逆否——這四個現已散在 `confidence`+candidate-set+`SCOPE_SPLIT`,本提案是**收斂為顯式第二軸**,非新增 ceremony。
- 風險:做成「複雜度=X 分」會變表演(Arch 自警的 Stage A 表演)→ 故只數訊號、不給分數。
- 影響:中。CORE phase 0 表改 2 軸;與 #4(blast classifier)同源,一起 promote。
- 來源:user 2026-06-29 提問「用 core 是否該做任務複雜度分析」。

### #9 — 驗證欄「執行綁定」（verified_by / observed_result 要有牙齒）  `✅ promoted v0.3 (2026-06-29)`
- 證據：對抗 agent + 自家 12/12 案例 `observed_result` 全停 PENDING；強模型失效是「把欄位填得有說服力、底下沒查」，plausible 值與真閉合長一樣。
- 改動：CORE invariant 6 + phase 5 硬規則——不准在 promise/PENDING 標 PASS;沒驗的標 UNVERIFIED 帶進 phase 6。
- 兩道測試:實質✅(補最大成熟度缺口) / 通用✅(對每份 contract 都成立)。來源:user 2026-06-29「夠強的 AI 用 MTM 是否成熟」討論。

### #10 — blast-radius 改「可觀察觸發」（非 AI 自分級）  `✅ promoted v0.3 (2026-06-29)`
- 證據:自分級 self-defeating——決定要不要嚴謹的，正是嚴謹要 backstop 的不可靠判斷;趕進度會自降。
- 改動:CORE phase 0 改觸發清單(auth/migration/跨domain/檔數/多租戶/字面≠資料模型)，命中即升、T3 不可自降。取代 #4/#8 的自判定部分。
- 兩道測試:實質✅ / 通用✅。

### #11 — 最小可行 contract（T1 只填 3 承重欄）  `✅ promoted v0.3 (2026-06-29)`
- 證據:強模型本來就會做中段欄位(schema/cross_module/test_plan)，全 11 欄儀式在 T1 邊際遞減;摩擦大→連高價值 20% 一起被跳過。
- 改動:CORE phase 0 — T1 預設 intent + escalation/candidate-set + affected_layers 三欄;T2/T3 才補滿。
- 兩道測試:實質✅ / 通用✅。

### #12 — MTM Plan：綠地 phase 0 分支（小白一句話 → 地基 fork）  `✅ promoted v0.4 (2026-06-29)`
- 證據：CORE phase 1 bootstrap / phase 2 candidate-set / Arch Stage 0 全是「AI ungrounded 才問」+ 開發者語言;綠地 fork(平台/雲端/多人/收費)無 source 可 ground、小白也答不出 domain 問題。gap 經邊界 agent 引 CORE 原文確認為真。
- 改動：新增 `MTM-Plan.md`(觸發/分界線/紀律/岔路庫/handoff/worked example)+ CORE phase 0-Plan 分支(spine 載觸發·分界·handoff)。
- 三方獨立評審(完整性/小白UX/邊界)GO-with-additions,已併入：①「孤島vs整合」fork ②裝置能力併平台 ③法規升級成 regime+residency ④難回頭 fork 改「想像 A/B」非「對嗎」⑤4 個永不靜默 default ⑥確認用「第一天能做/不能做」⑦handoff 必寫 phase-1 詞彙+UNKNOWN ⑧#8 規模降成推測 default。
- 兩道測試:實質✅(填真 gap) / 通用✅(所有綠地+一句話起手)。來源:user 2026-06-29「MTM Plan 值不值得做」。

### #13 — 客戶核心需求優先（核心體驗不可降級成佔位）  `✅ promoted v0.5 (2026-06-29)`
- 證據:bass-app **A/B 對照實驗**(MTM vs 無 MTM,同一句話)。MTM 把架構顧好但「真實貝斯音色」擺合成佔位;無 MTM 版用線上 soundfont **當場交付真音色**——在使用者**字面核心需求**上,無 MTM 反而贏。
- 改動:CORE invariant 7 + MTM-Plan 紀律 #8。使用者字面講出的核心體驗=一等交付物;現成真實方案可得就直接交付、別佔位;非延後不可就在 confirm 當頭條「還不能做」明示。
- 與 #11 共存:「便宜的可延後」只適用次要功能,核心體驗永不延後。
- 兩道測試:實質✅(對照組證明是真短板) / 通用✅(任何「使用者點名核心體驗」的專案)。來源:user 2026-06-29「確實要以客戶核心需求作為主要」。

### #14 — case-ledger append 綁成 phase 完成硬 gate  `✅ promoted v0.6 (2026-06-30)`
- 證據:§D「每個非 T0 task append」只是軟紀律、無觸發綁定。nicemeet 6 週效益分析發現:trial log 結算表從沒填、前 12 筆後停更——同個「meta 紀錄開天窗」洞。治本檔(MTM 自身)也會犯。
- 改動:CORE §7 step1 + §D「何時 append」改硬 gate——未 append 不算 task done(與 phase 5 執行綁定 invariant 6 同邏輯)。
- 兩道測試:實質✅(補已咬過兩次的 meta-record 洞) / 通用✅(每個非 T0 task 都成立)。來源:user 2026-06-30「C: 同意修」。

### #15 — MTM-Plan 開場「先問目的」+ discovery 覆蓋清單（延伸功能不提、僅綠地）  `✅ promoted v0.7 (2026-07-05)`
- 證據：user 實測 AI 未完整 follow MTM;綠地開場少了「資深團隊主動補問使用者沒講但該想」的深度。現有 Plan 直接跳難回頭 fork,**沒有先問「你最想達成什麼」的錨點**——目的(靈魂)沒被顯式問。
- 改動：MTM-Plan §3 加紀律 0「開場先問目的」(唯一預設開放問的題,定方向接 invariant 7)+ 開場一次涵蓋「目的→呈現/平台→誰用/情境」(後二用既有 §4a fork);§6 worked example 補目的問句。**不動 CORE 0→6**,只擴 Plan 開場協議。
- user 裁決(2026-07-05):**延伸功能整格拿掉**(不主動提,留 §4c/phase 2)、**trigger 僅限綠地**(不變)、其餘照提案。
- 風險控制:除「目的」外一律「便宜→假設、貴→逼選」,禁止一次丟多個開放問句 → 不回 MTM-Plan 當初要根除的面試地獄/ceremony tax。
- 兩道測試:實質✅(新增「目的必問」錨點,補「開場不夠 consultative + 直接跳建」的真 gap,非措辭微調)/ 通用✅(所有綠地「幫我做一個 ___」成立;scope 限 Plan phase)。來源:user 2026-07-05「想讓 AI 更深入跟使用者聊、像團隊先問使用者沒提但該考慮的」。
- **獨立 AI 方法論專家評審(2026-07-05,promote 後)**:有條件同意、6/10。承認原子位置對(=#13 的 elicitation 互補、便宜、正確限縮綠地);抓三洞已於 promote 後補上——①目的答案缺 downstream wiring(posture 非 mechanism)→ 紀律 0 加「答案接線:寫進 glossary/invariants 當靈魂註記 + 決定哪些 fork 先問 + 標 invariant 7 保護對象」;②「開場一次涵蓋」措辭偷渡 ceremony 且與 §4a 重述 → 改成「開場只主動問目的一題,其餘走 §4a 遇到才問」;③缺空泛答案 fallback → 加「答得同義反覆就退回 fork、不追第二輪開放題」。
- **證據等級自評(專家點出、誠實記錄)**:#15 是本系列**證據最弱**的一次 promote——無 A/B control(對比 #13)、無復發計數(對比 #14),靠「論證通用 + user aspiration」過 gate。**Backstop**:接下來 2 個綠地實跑各記一行「目的答案是否真的改變了任何 downstream 決定」;連 2 次沒有 → 觸發 §D backstop 重審 #15。

<!-- 新 proposal append 在這行之上 -->

---

## §C Changelog（版本史——只有 promote 過 gate 的才進這）

- **v0.7**（2026-07-05）：promote **#15 MTM-Plan 開場「先問目的」+ discovery 覆蓋**——綠地起手第一步改成問一個開放的目的題(你最想達成什麼,定靈魂/方向,接 invariant 7),再攤既有 fork;開場只主動問目的一題,其餘走 §4a 遇到才問。user 裁決:延伸功能不主動提(留 §4c/phase 2)、trigger 僅限綠地。機制仍「便宜→假設、貴→逼選」,只有目的開放問,不回面試地獄。**證據等級最弱的一次 promote(無 control/無復發計數)→ 已掛 backstop:接下來 2 個綠地各記一行「目的答案是否真的改變 downstream 決定」,連 2 次沒有就重審。**
- **v0.6**（2026-06-30）：promote **#14 case-ledger append 硬 gate**——未 append ledger 不算 task done(與 phase-5 執行綁定 invariant 6 同邏輯)，修「軟紀律→開天窗」的跨任務洞(nicemeet 6 週分析發現結算表從沒填)。同批:修正 CORE 標題/§7/README 殘留 v0.2 版本標籤漂移、確立「消費端 task ledger 放各自專案本地」(nicemeet→該專案本地 ledger)。
- **v0.5**（2026-06-29）：promote **#13 客戶核心需求優先**(invariant 7)——由 **bass-app A/B 對照實驗**得出(MTM 第一個真正 control:同一句話、有問 vs 沒問)。結論誠實:MTM 在「原生vs網頁」「音階格vs指板」翻對方向(點數獲勝),但在「真實音色」字面核心需求上輸給無 MTM 版(它接 soundfont 當場交付、MTM 只擺佔位)→ 直接催生 #13。
- **v0.4**（2026-06-29）：新增 **MTM Plan**（綠地 phase 0 分支，`MTM-Plan.md`）——把小白一句話的不夠清晰計畫，用生活語言問清難回頭的地基 fork(平台/雲端/多人/租戶/整合/法規)，產出骨架 seed `project-architecture/` 交棒 phase 1。三方獨立評審 GO-with-additions 後定稿。promote #12。
- **v0.3**（2026-06-29）：焦點=**讓夠強的 AI 用 MTM 跑更有效率**（user 重新對焦：非賣產品/論文，而是實際開發助力）。三方獨立評價收斂出核心訊號 → promote **#9 驗證執行綁定**(補最大成熟度缺口：宣告→執行)、**#10 分級靠可觀察觸發**(修自分級漏洞)、**#11 最小可行 contract**(高價值 20% 零摩擦)。診斷:MTM 矯正的是「能力修不掉的系統性偏誤」(挑字面/scope漂移/忘前文/討好)——這幾條最值錢;中段欄位強模型本來就會做、調輕。
- **v0.2**（2026-06-29，draft 轉正）：
  - ✅ **Q1 已拍板**：CORE 當脊椎、舊三份保留為 phase 細節（加 header 指回 CORE）。
  - ✅ **Q2 已拍板**：進化 gate = inline 機會主義（執行中白話提論點+原因）+ 升規則必過兩道測試【實質 + 通用跨任務】+ 單一事件只進 ledger 不升規則 + 點頭即升。已寫入 §D。
  - **promoted into CORE**：#1 統一 lifecycle、#2 observed_result、#3 Contract↔Verify 脊椎、#4 blast classifier、#5 forced-disagreement 拆解、#6 escalation 一等 phase、#7 status header。
  - ⏳ **still pending**：#8（複雜度第二軸）——已討論未明確點頭，留 §B 等 signoff。
- **v0.1.2**（Arch）：加「對話 UX 紀律」六條 + meta 原則。
- **v0.1.1**（Arch）：forced-disagreement 強制 surface（**已被 #5 取代**）。
- **v0.1**（2026-05-14）：nicemeet 試行啟用，11 欄 build/review 雙模式。

<!-- 新版本 append 在 §C 最上方（本清單新→舊） -->
