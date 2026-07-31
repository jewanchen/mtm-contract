# Using MTM Contract with Claude Code

> **Updated for specification 2.0.** Start from
> [`MTM-LITE.md`](../MTM-LITE.md) — one page, English, with the
> tier triggers and the three fields. This guide covers wiring that
> into a Claude Code session.

Claude Code is Anthropic's CLI for agentic coding. It works well
with MTM Contract because the contract file lives in your repo and
Claude Code reads files natively — no plugin required.

---

## The 3-step flow

### 1. Create the contract before delegating work

```bash
# In your project root
mkdir -p contracts
# Ordinary task: three fields. Copy the light version.
cp /path/to/mtm-contract/MTM-LITE.md /tmp/mtm-lite-reference.md
# Structural or critical task: the full template.
cp /path/to/mtm-contract/TEMPLATE.md \
  contracts/$(date +%Y-%m-%d)_your-task-name.md
```

How much you fill in depends on the tier — see the trigger table in
[`MTM-LITE.md`](../MTM-LITE.md) §1. For an ordinary task that is
`intent`, `escalation`/candidate set, and `affected_layers`, and
nothing else. For structural or critical work, add `preconditions`
and `expected_outcome` and fill the rest of the template. Either
way, write it *before* you describe the task to Claude Code.

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

### 3. Self-check, then review in a clean context

These are two different steps and merging them destroys the second.

**Self-check** — in the working session:

```
Walk each clause of the contract and mark PASS / FAIL / MUTATED with
a one-line reason. For every expected_outcome, fill observed_result
with what you actually ran this session — command output, query
result, log line. Do not mark anything PASS while its evidence is
still a promise; mark those UNVERIFIED.
```

**Review** — mandatory for critical work, and it must **not** be the
session that wrote the code. Use a subagent or a fresh session, and
give it only the contract, the decisions it cites, and the diff:

```
You are reviewing this change in a clean context. You did not write it.
Read only: contracts/<file>.md, the decisions it cites, and the diff.
Report whether the diff delivers what the contract promised, what it
changed outside the declared scope, and anything that works but
contradicts a recorded decision. Report only — do not fix anything.
```

The author cannot perform the second step. The reasoning that
produced a gap is the reasoning that would review it. In one week of
critical batches on the authors' own codebase, four consecutive
changes passed static analysis, unit tests, and self-review — and a
clean-context reviewer returned *do not ship* on all four.

Then review the findings yourself, decide what to fix, and commit the
contract alongside the code change in the same PR.

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

Before writing implementation code on any non-trivial task, write a
contract at contracts/YYYY-MM-DD_<task>.md.

How much to write — decide by trigger, not by feel. Promote on any
hit, never argue it back down:
- Ordinary task, one module, no trigger below → three fields only:
  intent (what will be observably true), escalation/candidate set
  (what is not yours to decide; if the request's wording could point
  at more than one thing in the data, list the candidates and ask),
  affected_layers (what changes and what deliberately does not).
- Auth/permissions/secrets · schema change · more than one domain ·
  tenant visibility · payments · release assets · literal request
  does not map one-to-one onto the data model → full contract, and
  a clean-context review before merge.

While implementing:
1. Resolve any UNKNOWN precondition by actually running the check.
2. Do not cross a declared boundary with a flag, a toggle, or a
   hidden field. If you must cross it, stop and say so.
3. Do not change anything outside affected_layers without reporting
   first.
4. On an escalation halt-condition, stop and report rather than
   improvise.

After implementation:
- Mark each clause PASS / FAIL / MUTATED with a one-line reason.
- Fill observed_result with what you actually ran this session.
  Never mark PASS while the evidence is still a promise — mark it
  UNVERIFIED and carry it into review.
```

This system-prompt anchor reminds Claude Code to consult the
contract on every relevant task without needing to be told each
time.

---

## What tooling would add

The flow above is the methodology. What a tool could add is
*enforcement* — the parts that are mechanically checkable and that
discipline alone has repeatedly failed to hold:

- no empty fields (`N/A` and `UNKNOWN: <why>` are valid; blank is not),
- no clause marked PASS while its `observed_result` is a promise,
- no task closed without its ledger line.

That is deliberately downstream of the specification rather than
bundled with it: it belongs in continuous integration, not in the
path of someone trying this for the first time. Section 12 of the
[2.0 article](../mtm-contract-2.0-article.md) explains why it matters
more than we originally thought — a rule the specification itself
called mandatory stopped being honoured within a month.

---

*See the main repository for the full methodology:
[github.com/jewanchen/mtm-contract](https://github.com/jewanchen/mtm-contract).*
