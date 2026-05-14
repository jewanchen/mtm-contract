# MTM Contract

> **A pre-execution specification layer for reliable AI software engineering.**
> Markdown-only, zero dependencies, Apache 2.0. From **Vast Intelligence Limited**.

---

## The 30-second pitch

AI coding agents fail in five recurring ways: hallucinated APIs, silent cross-module overwrites, context drift across long tasks, unscoped escalation, and no post-hoc verification.

**MTM Contract** is an 11-field markdown specification the agent fills out *before* writing code, and audits *after* the code ships. Each field addresses a specific failure mode.

In a six-task production trial:

| Metric | Result |
|---|---|
| First-pass commits (tsc + build + analyze all green) | **6 / 6** |
| Compile-time hallucinations | **0** |
| Contracts that surfaced unanticipated cross-module work | **4 / 6** |
| Major redesigns caught during contract-phase escalation | **1** (would have cost a production rollback if shipped) |

Full methodology, trial data, and reasoning: [`mtm-contract-technical-article.md`](./mtm-contract-technical-article.md).

---

## Try it in 10 minutes

```bash
# 1. Copy the template into your project
mkdir -p contracts
curl -L https://raw.githubusercontent.com/jewanchen/mtm-contract/main/TEMPLATE.md \
  -o contracts/$(date +%Y-%m-%d)_my-first-mtm-task.md

# 2. Open the file. Fill in `intent`, `affected_layers`, `expected_outcome`
#    BEFORE you ask an AI agent to do the work. (~5 minutes.)
#
# 3. Hand the filled contract to your AI agent as the work specification.
#
# 4. After the change ships, return to the file and write the audit section
#    (PASS / FAIL / MUTATED per clause).
```

That's it. No SDK, no plugin, no language lock-in. The methodology is the file.

---

## What's in this repository

| File | Purpose |
|---|---|
| [`mtm-contract-technical-article.md`](./mtm-contract-technical-article.md) | The full methodology paper (~450 lines): failure modes, field-by-field rationale, six production task case study, AI-to-AI extension, distribution strategy, comparison to related work. |
| [`TEMPLATE.md`](./TEMPLATE.md) | The ready-to-copy contract template. 11 fields + audit section. |
| [`examples/`](./examples/) | Six real production contracts, sanitised for confidentiality. Includes the v1 → v2 redesign case study (example 05) in full. |
| [`integrations/`](./integrations/) | Guides for using MTM Contract alongside Claude Code, Cursor, and the Model Context Protocol (MCP). |
| [`LICENSE`](./LICENSE) | Apache 2.0. |
| [`NOTICE`](./NOTICE) | Attribution requirements for derivative works. |

---

## When to use it (and when not to)

**Use it when:**

- The AI agent will touch more than one file or subsystem.
- The agent's task description leaves *anything* implicit about cross-module obligations, data shape assumptions, or success criteria.
- A bad implementation would cost a rollback, a migration, or a multi-day debugging session.
- The agent's confidence is anything other than "absolutely certain."

**Skip it when:**

- The task is a typo fix, version bump, single-line config change, or docstring tidy.
- Writing the contract would take longer than writing the code.
- The task is purely exploratory and no commit will land from this round.

Rule of thumb: **if writing the contract is taking longer than writing the code, you don't need a contract.** If it isn't, you do.

---

## The two layers

MTM Contract was observed working as a *human-AI clarification* tool: a markdown file mediating between an engineer and an AI agent. The same eleven-field shape applies, with a JSON encoding, to *AI-to-AI* coordination — function-calling schemas, multi-agent state handoff, MCP tool descriptions.

The methodology is invariant across layers. See Section 6 of the [main article](./mtm-contract-technical-article.md#6-the-two-layers-human-ai-now-ai-to-ai-next) for the JSON-schema translation.

---

## Distribution roadmap

| Phase | What | Status |
|---|---|---|
| **Phase 1** | Markdown convention + template + examples + integration guides | ✅ **Available now** (this repository) |
| **Phase 2** | `mtm` CLI: `new` / `validate` / `audit` / `metrics` / `list` / `search` | Planned, after methodology stabilises (~20–50 trial samples) |
| **Phase 3** | MCP server, Claude Code skill, Cursor extension, Aider annotation, OpenAI function-calling schema | Planned, after CLI ships |

Phase 1 is fully usable on its own. Phase 2 and 3 are conduits; they consume the markdown specification, not replace it.

---

## License and attribution

Apache 2.0. Attribution to Vast Intelligence Limited required in derivative works (forks, tools implementing the MTM specification, adapted documentation, academic citations). See [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE) for the full terms.

```
Vast Intelligence Limited. (2026).
MTM Contract: A Pre-Execution Specification Layer for
Reliable AI Software Engineering.
https://github.com/jewanchen/mtm-contract
Published: May 14, 2026.
```

---

## Contact

**Vast Intelligence Limited**
Email: jeremy.chen@vastitw.com
Phone: +886 2 2706 7590
Website: [vastitw.com/mtm](https://vastitw.com/mtm)

For Phase 2/3 collaboration, replication studies, or integration partnerships, please use the contact channels above.
