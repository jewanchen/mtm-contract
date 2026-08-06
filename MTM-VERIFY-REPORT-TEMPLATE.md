# MTM Verify Report

> **Task / contract**: [link to the contract file this audit covers]
> **Executor**: [which agent did the work]
> **Auditor**: [which agent is auditing]
> **Date**: YYYY-MM-DD
>
> 繁體中文原稿：[`MTM-VERIFY-REPORT-TEMPLATE.zh-TW.md`](./MTM-VERIFY-REPORT-TEMPLATE.zh-TW.md) · Protocol: [`MTM-Verify.md`](./MTM-Verify.md)

---

## Executive summary

* **Verdict**: `[PASS / REWORK_REQUIRED / ESCALATE]`
* **Blockers found**: `[n]`
* **Warnings**: `[n]`

> Findings are **input to the executor's judgement, not a verdict on the work**. The auditor cannot see intent — it was given the contract, the decisions and the diff, and nothing else. For each finding the executor asks: *defect, or decision?* Defects get fixed; decisions go to the human. See CORE invariant 8.

---

## 1. Architecture alignment
> Were the boundaries in the contract and the decision records respected?
> *(Covers failure mode 2.)*

* [ ] `PASS` / `FAIL` — **Boundary check**
  * *Evidence:* e.g. "no file changed outside the declared `affected_layers`"
* [ ] `PASS` / `FAIL` — **Architectural commitment**
  * *Evidence:*

## 2. Collateral damage
> Was anything outside the task's scope changed? Has the environment drifted?
> *(Covers failure modes 2 and 7.)*

* [ ] `PASS` / `WARN` / `FAIL` — **Unintended file changes**
  * *Evidence:*
* [ ] `PASS` / `WARN` / `FAIL` — **Environment and dependencies**
  * *Evidence:* e.g. "a new package was added without updating the manifest"

## 3. Completeness and edge cases
> Is the task *actually* finished, or only the happy path?
> *(Covers failure modes 1, 3, 5, 6.)*

* [ ] `PASS` / `FAIL` — **Interface alignment**
  * *Evidence:* does the request the client builds match the shape the endpoint accepts?
* [ ] `PASS` / `FAIL` — **Error handling / happy-path bias**
  * *Evidence:* e.g. "`userController.js:45` catches the exception but does not return the right status"
* [ ] `PASS` / `FAIL` — **Phantom code / TODOs**
  * *Evidence:* e.g. "one `return mockData` remains in the core path"

## 4. Security and performance
> *(Covers failure modes 8 and 9.)*

* [ ] `PASS` / `WARN` / `FAIL` — **Authentication and ownership**
  * *Evidence:* authentication and ownership are two separate checks — say which was verified
* [ ] `PASS` / `WARN` / `FAIL` — **Performance traps**
  * *Evidence:* e.g. "no N+1 pattern found in the new query paths"

## 5. Verification integrity
> Did the contract's own claims close?
> *(Covers failure modes 4 and 10, and CORE invariant 6.)*

* [ ] `PASS` / `FAIL` — **Execution binding**
  * *Evidence:* is any clause marked `PASS` while its `observed_result` is still a promise or `PENDING`?
* [ ] `PASS` / `FAIL` — **Tests**
  * *Evidence:* were any assertions removed, skipped, or weakened in this diff?

---

## Action required

*(Anything marked FAIL or WARN above, for the executor to rework.)*

1. [ ] **Finding 1** — [file and line] — [what is wrong, and what would close it]
2. [ ] **Finding 2** — [file and line] — [what is wrong, and what would close it]

## Questions for the human

*(Ambiguous boundaries or logic the auditor cannot resolve. Also: anything that appears to contradict a recorded decision — that goes here, not into the action list.)*

1. e.g. "For a user with no avatar, should a default image be shown? The code does not handle it, and I could not find a decision either way."
