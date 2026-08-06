# MTM Verify Report

> **Task / Contract Reference**: [填入本次查核的任務或合約檔案連結]
> **Executor Agent**: [執行本次任務的 Agent 識別]
> **Auditor Agent**: [負責本次審計的 Agent 識別]
> **Date**: YYYY-MM-DD

---

## 總結結論 (Executive Summary)

* **整體判定**: `[PASS / REWORK_REQUIRED / ESCALATE]`
* **發現的嚴重漏洞 (Blockers)**: `[數字]`
* **建議修正項 (Warnings)**: `[數字]`

---

## 1. 架構一致性 (Architecture Alignment)
> 是否遵守了 MTM Arch 與 ADR 的邊界？

* [ ] `PASS` / `FAIL`: **邊界檢查 (Boundary Check)**
  * *原因 / 證據：* (例如：未發現超越 `affected_layers` 的檔案修改)
* [ ] `PASS` / `FAIL`: **架構承諾 (Architectural Commitment)**
  * *原因 / 證據：*

## 2. 連帶影響 (Collateral Damage Check)
> 任務範圍外的是否被意外更動？環境設定是否脫節？

* [ ] `PASS` / `WARN` / `FAIL`: **非預期檔案修改**
  * *原因 / 證據：*
* [ ] `PASS` / `WARN` / `FAIL`: **環境與依賴 (Env & Dependencies)**
  * *原因 / 證據：* (例如：新增了 `axios` 但未更新 README 說明)

## 3. 完整性與例外處理 (Completeness & Edge Cases)
> 任務是否「真的」完成，還是只有 Happy Path？

* [ ] `PASS` / `FAIL`: **API 串接對齊 (Interface Alignment)**
  * *原因 / 證據：*
* [ ] `PASS` / `FAIL`: **錯誤處理 (Error Handling / Happy Path Bias)**
  * *原因 / 證據：* (例如：`userController.js` 第 45 行抓取 Exception 但未回傳正確 HTTP Status)
* [ ] `PASS` / `FAIL`: **髒話掃描 (Phantom Code / TODOs)**
  * *原因 / 證據：* (例如：發現一處 `return mockData`)

## 4. 安全性與效能 (Security & Performance)

* [ ] `PASS` / `WARN` / `FAIL`: **權限檢查 (Auth & Security Bypass)**
  * *原因 / 證據：*
* [ ] `PASS` / `WARN` / `FAIL`: **效能風險 (Performance Traps)**
  * *原因 / 證據：* (例如：未發現明顯的 N+1 query 迴圈)

---

## 🎯 待辦修復清單 (Action Required)

*(如果上方有任何 FAIL 或 WARN，請列在這裡交由 Executor Agent 重工)*

1. [ ] **修復點 1**: [具體檔案與行數] - [問題描述與修復建議]
2. [ ] **修復點 2**: [具體檔案與行數] - [問題描述與修復建議]

## ❓ 釐清點 (Questions for Human)

*(如果有任何邊界條件模糊或不確定的邏輯，列在這裡等待人類決策)*

1. 關於 [某個功能] 的極端情況 (如使用者無頭貼時)，是否應顯示預設圖片？目前程式碼未處理。
