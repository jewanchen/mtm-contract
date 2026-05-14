# Using MTM Contract with Cursor

> **Status:** Phase 1 — manual integration. Phase 3 will add a
> Cursor extension that automates this flow.

Cursor is an AI-first code editor with several agent-mode features
(Composer, Agent mode, etc.). MTM Contract integrates naturally
because Cursor's agent reads files in the workspace.

---

## The 3-step flow

### 1. Generate the contract before invoking Composer / Agent

In Cursor's file tree:

- Create `contracts/` if it doesn't exist.
- Duplicate `TEMPLATE.md` (from this repository) into a new file
  named `YYYY-MM-DD_<task>.md`.

Open the new contract and fill in `intent`, `affected_layers`,
`preconditions`, `expected_outcome`, and `escalation` *before* you
open Composer or invoke Agent mode on the task.

### 2. Reference the contract in your Cursor request

In Cursor's prompt:

```
Implement the work specified in @contracts/2026-05-14_<task>.md.

Honour the contract:
- Verify each precondition before writing implementation code.
- Stay within affected_layers; do not edit other subsystems.
- If you hit an escalation halt-condition, stop and ask.
- After implementation, suggest PASS / FAIL / MUTATED marks
  for each clause.
```

The `@filename` syntax in Cursor pins the contract file to the
agent's context window so it does not get evicted during long
tasks.

### 3. Audit the contract before commit

After Cursor's agent reports the work complete, ask:

```
Walk through each clause of @contracts/2026-05-14_<task>.md and
propose PASS / FAIL / MUTATED marks. For each MUTATED, give a
one-line reason.
```

Review the proposed audit, edit if needed, and commit the contract
alongside the code change.

---

## Cursor-specific tips

### Use `.cursorrules` to enforce the workflow

Add this to your project's `.cursorrules` file:

```
## MTM Contract workflow

For non-trivial tasks (more than one file affected), check whether
a contract exists in contracts/YYYY-MM-DD_<task>.md before
proposing changes.

If a contract exists:
- Honour its affected_layers, preconditions, and
  cross_module_contract.
- Stop at escalation halt-conditions.
- After implementation, propose audit marks for each clause.

If no contract exists and the task affects more than one file or
subsystem, suggest creating one from TEMPLATE.md before
proceeding.
```

This anchor ensures the workflow is followed even on long sessions
where the system prompt drifts.

### Pin the contract in Composer

In Cursor Composer's file picker, drag the contract file into the
context panel. This keeps the contract anchored on every turn,
not just the first.

### Use the contract as the work plan

When Composer is uncertain about scope, point at the contract's
`expected_outcome` section as the ground truth for "done." This
short-circuits the common drift where Composer proposes additional
changes that aren't on the contract.

---

## Future Phase 3: a Cursor extension

A planned Cursor extension will:

- Add a "New MTM Contract" command in the command palette.
- Auto-anchor the contract in Composer's context when opened.
- Lint contracts in real-time for missing fields and
  unverifiable references.
- Surface the audit walk-through at task completion.

Until that ships, the 3-step flow above gives most of the value.

---

*See the main repository for the full methodology:
[github.com/jewanchen/mtm-contract](https://github.com/jewanchen/mtm-contract).*
