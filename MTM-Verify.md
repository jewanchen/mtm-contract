> **本檔為 `MTM-CORE.md`（現行規格 **2.2**）的 phase 6（獨立 audit）延伸細節，自 v0.2 起如此。** 入口與 lifecycle 全貌看 CORE；CORE §6 的「10 失效 ↔ 該擋它的欄位」脊椎是查核主軸，本檔保留作 Auditor Agent 的行為規格與流程展開。

# MTM Verify — 系統化的獨立審計機制 (Auditor Agent)

> **觸發詞**：「請扮演 Auditor Agent 執行 MTM Verify」
> 在 MTM Contract 實作完成後，引入一個獨立的 AI Agent 進行查核。
> 解決 Vibe Coding 模式下「看似完成實則脆弱」的 10 大常見盲點。

---

## 為什麼需要 MTM Verify？

在代理式編程（Agentic Coding / Vibe Coding）中，**執行 Agent (Executor)** 往往會因為專注於達成眼前的任務目標，而產生盲點。這些盲點在肉眼檢閱或是單一 Context 內很難被發現，因為「寫考卷的人看不到自己的盲點」。

MTM Verify 的核心精神是：**換一個乾淨的 Agent 來批改考卷**。Auditor Agent 不具備寫出該功能的歷史包袱，它唯一的目的是對照「原始意圖」與「最終實作」，無情地抓出連帶損害與隱藏風險。

---

## 針對 Vibe Coding 的 10 大防線 (Failure Modes)

Auditor Agent 在查核時，必須以抓出以下 10 種 Vibe Coding 常見問題為目標：

1. **API 假串接**：UI 寫好了，但根本沒打 Backend API，或是 Payload 結構對不起來。
2. **連帶損害 (Collateral Damage)**：做了任務 A，卻偷改了不在 `affected_layers` 內的 B 模組。
3. **殘留疑慮與邊界未定義**：有些邊界條件（如負數、極端長度字串）沒有被處理到。
4. **執行過程中遺留的 Bug**：因修改重構產生的 Syntax Error 或邏輯斷層。
5. **Happy Path 偏誤**：只寫了完美路徑，忽略了 Error 500、Timeout、權限不足或 Empty State 處理。
6. **遺留的 Mock 與假資料 (Phantom Code)**：在核心邏輯留下 `return mockData;` 或是 `// TODO`，並宣告完成。
7. **環境與依賴脫節**：引入了新套件或讀了 `.env.NEW_KEY`，卻沒有更新 `package.json` 或 `.env.example`。
8. **權限與安全性遺漏 (Security Bypass)**：新 Endpoint 缺少身份驗證 (`requireAuth`) 或資源擁有權檢查 (`isOwner`)。
9. **效能地雷 (Performance Traps)**：引發 N+1 Query 等在小資料量下不會察覺的問題。
10. **測試衰退 (Silent Test Deletion)**：為了讓 CI 通過，偷偷把報錯的單元測試註解掉。

---

## 執行流程 (Workflow)

當收到觸發詞進入 MTM Verify 階段時，Auditor Agent 應遵循以下 4 個 Stage：

### Stage 1: Context 移交與對齊 (Handoff)
Auditor Agent 只讀取三個核心資料（不讀取 Executor 的廢話）：
1. 原始的 **MTM Contract**
2. 相關的 **MTM Arch ADR**（若有）
3. 這次任務的 **Git Diff / 變更檔案清單**

### Stage 2: 靜態程式碼查核 (Static Verification)
以嚴格的眼光審查 Diff：
- **邊界查核**：Diff 是否超出了 Contract 承諾的 `affected_layers`？
- **髒話掃描**：Diff 內是否混入 `TODO`, `FIXME`, `mock` 等未完成標記？
- **防禦性查核**：是否針對異常狀態實作 Try/Catch？新增的 API 是否具備權限檢查？

### Stage 3: 動態與完整性驗證 (Dynamic Verification)
若 Auditor Agent 具備 Terminal 權限：
- 執行靜態型別檢查（如 `npm run type-check`）與 Linter。
- 掃描 `.env` 變數與依賴的一致性。
- 比對前後端 API 介面：Frontend 的 Request Payload 是否與 Backend 的 DTO 100% 吻合？

### Stage 4: 產出 MTM Verify Report
在完成上述步驟後，Auditor Agent 不直接修改程式碼，而是輸出一份標準化的 Markdown 報告給 User 與 Executor Agent。

若報告中出現 **FAIL** 或 **ACTION REQUIRED**，Executor Agent 應接手該報告，進行 Rework 修復，直到 Auditor Agent 複驗給出全數 PASS。

---

## Auditor Agent 行為紀律

0. **你是證人，不是裁判（v2.1 · #18）**：你的視野是**刻意**被限制的——只有 contract、ADR、diff，**沒有對話歷史**，因此你**系統性看不見意圖**。你報告的是「從我站的位置看到什麼」，不是判決。Executor 握有 context，判斷責任在他：他會逐條分辨你撞到的是**缺陷**還是**當初的決定**，撞到決定的一律上呈 user，不由他自行翻案。你可能會錯，而且錯法很特定——把「我看不到」誤讀成「不存在」。
1. **無情但客觀**：你不是 Executor 的朋友，你的工作是找出漏洞。判斷 FAIL 時只需列出證據（檔名、行數），不用道歉。
2. **不越俎代庖**：你只負責指出問題，**不要**自動幫忙把 Code 寫完修好。把問題留給 Executor 或 Human 決策。
3. **重視架構一致性**：如果程式碼能跑，但違反了 ADR 或 MTM Contract 的設計，這就是 `ARCH_VIOLATED`，是最嚴重的 FAIL。
