# Using MTM Contract with Claude Code

> **Status:** Phase 1 — manual integration. Phase 3 will add a
> Claude Code skill that automates this flow.

Claude Code is Anthropic's CLI for agentic coding. It works well
with MTM Contract because the contract file lives in your repo and
Claude Code reads files natively — no plugin required.

---

## The 3-step flow

### 1. Create the contract before delegating work

```bash
# In your project root
mkdir -p contracts
cp /path/to/mtm-contract/TEMPLATE.md \
  contracts/$(date +%Y-%m-%d)_your-task-name.md
```

Open the contract in your editor and fill in `intent`,
`affected_layers`, `preconditions`, `expected_outcome`, and
`escalation` *before* you describe the task to Claude Code.

### 2. Hand the contract to Claude Code as the work specification

In your Claude Code session, paste or reference the contract:

```
Please implement the work specified in
contracts/2026-05-14_status-lifecycle.md.

Follow the contract clauses exactly:
- Verify each precondition before writing code.
- Honour the cross_module_contract boundary.
- If you hit an escalation halt-condition, stop and report.
- After implementation, propose updates to the audit section.
```

Claude Code will read the file, verify references, and follow the
declared boundaries. If a precondition is `UNKNOWN`, it will grep
to resolve it before writing implementation code.

### 3. Audit before merging

After Claude Code reports the work complete:

```
Please walk through each clause of the contract and propose
PASS / FAIL / MUTATED marks, with a one-line reason per MUTATED.
```

Review the proposed audit, edit as needed, and commit the contract
alongside the code change in the same PR.

---

## Why this works without a plugin

MTM Contract's source of truth is the markdown file. Claude Code's
working surface is the filesystem. The two intersect naturally:

- Claude Code can `Read` the contract at any time during the work
  to re-anchor against the original intent.
- The contract is git-tracked, so the audit history is visible in
  `git log` and PR diffs.
- No SDK to install, no MCP server to configure.

---

## Recommended companion: a `CLAUDE.md` reminder

Add this to your project's `CLAUDE.md` (or equivalent system
prompt file):

```markdown
## MTM Contract workflow

Non-trivial tasks (affecting more than one file or subsystem)
should be preceded by an MTM Contract at contracts/YYYY-MM-DD_<task>.md.

Before writing implementation code:
1. Read the contract.
2. Resolve any `UNKNOWN` preconditions via grep or tool use.
3. Honour the cross_module_contract boundary — do not edit
   subsystems outside affected_layers without amending the
   contract.
4. If you hit an escalation halt-condition, stop and report
   rather than improvise.

After implementation:
- Propose PASS / FAIL / MUTATED marks for each clause.
- Capture MUTATED items with one-line reasons in the
  contract's audit table.
```

This system-prompt anchor reminds Claude Code to consult the
contract on every relevant task without needing to be told each
time.

---

## Future Phase 3: a Claude Code skill

A planned Claude Code skill (`/mtm`) will:

- Generate a contract file from `TEMPLATE.md` with the task name
  pre-filled.
- Validate that all 11 fields are populated before invoking
  implementation.
- Walk the audit interactively at task completion (PASS / FAIL /
  MUTATED prompts).
- Report metrics (one-pass commit rate, hallucinations caught,
  MUTATED frequency) across the repo's contract history.

Until that ships, the 3-step flow above gives most of the value.

---

*See the main repository for the full methodology:
[github.com/jewanchen/mtm-contract](https://github.com/jewanchen/mtm-contract).*
