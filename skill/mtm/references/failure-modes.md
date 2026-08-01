# Ten failure modes, and which field is supposed to stop each

Verification is not a separate checklist. It is a check of whether each preventive field actually held. When reviewing a change, walk this table rather than improvising.

| # | Failure mode | The field that should have stopped it | What to look for in the diff |
|---|---|---|---|
| 1 | **Interface that doesn't line up** — the client is written, the payload shape does not match what the server returns | `cross_module_contract` (emit ↔ listen) | Compare the request the client builds against the shape the endpoint actually accepts. Optional-versus-required is where this hides. |
| 2 | **Collateral damage** — task A quietly edited module B | `affected_layers` boundary | Anything in the diff outside the declared layers. No exceptions for "it was obviously needed". |
| 3 | **Undefined edges** — empty, zero, negative, very long, duplicate | `expected_outcome` + `schema_assumptions` | For each new input path, ask what happens at the boundary. Absence of an answer is the finding. |
| 4 | **Refactor residue** — a logic gap left by the move itself | `test_plan` + the self-check's `observed_result` | Behaviour that was preserved by accident rather than by check. Byte-for-byte comparison where it applies. |
| 5 | **Happy path only** — no 500, no timeout, no permission denial, no empty state | `expected_outcome`, negative paths | Every new call site: what does the user see when it fails? |
| 6 | **Phantom code** — leftover mock, stub, `TODO` in a path claimed as done | Self-check scan | Grep the diff for mock/stub/TODO/FIXME. Any hit in a path the contract claims is finished is an error. |
| 7 | **Environment drift** — new dependency or variable not declared anywhere | `affected_layers` (env and secrets) | New imports and new config reads versus the manifest and the example env file. |
| 8 | **Missing authorisation** — new endpoint without authentication or ownership check | `preconditions` + the critical-tier gate | Every added route: is identity checked, and is *ownership* checked? They are different questions. |
| 9 | **Performance landmine** — N+1, unindexed lookup, work inside a loop | `schema_assumptions` + `verifiable_by` (query count) | Any new query inside an iteration. Count queries rather than reasoning about them. |
| 10 | **Silent test deletion** — a failing test commented out to make the pipeline green | `test_plan` + diff scan | Removed or skipped assertions in the diff. |

## The verdict that outranks all ten

**`ARCH_VIOLATED`** — the code works and contradicts a decision that was recorded. This is more severe than a bug, because a bug announces itself and this compounds silently. When you find one, the options are rollback or an explicit amendment to the decision. Not "note it and move on".

## Reviewer conduct

- **Report; do not fix.** Findings go back to whoever owns the work. A reviewer who patches the code has destroyed the independence that made the review worth running.
- **Cite, don't characterise.** File and line. No apologies, no softening, no praise sandwich.
- **Architectural consistency outranks style.** A working change that violates the agreed design is the most severe finding available.
- **Surface only what is actionable** to the person who asked. They do not need the full pass/fail dump.
