# MTM Contract

> **MTM — *machine to machine*.** A contract is a handoff format: today usually written by a person for an agent, and by design between agents too. The encoding changes; the fields do not.
>
> **A framework for preventing hallucination and architectural drift in agentic AI coding.**
> A discipline for containing agentic AI's two recurring failure modes.
> Markdown-only, zero dependencies, Apache 2.0. From **Vast Intelligence Limited**.

---

## Is this your Tuesday?

A join starts returning nothing for records that visibly exist. The obvious move is to reason about it: stale cache, wrong identity, the data layer inferring a column type wrong. Three hypotheses, three changes, three rebuilds, no information — every layer above the database was internally consistent, so no amount of reading application code was going to surface it. One query against the database's own catalogue of columns ended it: the two sides of the join were different types.

The contract does not make you smarter. It makes you write down what must be true and how you checked it, **before** the agent generates anything — so that query happens in minute one instead of minute forty.

That is the whole idea: **put the cheap checks before the expensive generation.**

## Start here — paste this into your agent

This is the method at working scale. Put it in `CLAUDE.md`, `.cursorrules`, or your system prompt. Nothing to install, no lock-in.

```markdown
## Contract-first workflow

Before writing implementation code, classify the task by trigger — not by
how risky it feels. Any hit promotes it; never argue a task back down.

- Typo, copy, styling, version bump, one small file → just do it.
- One module, no trigger below → write three fields first (see below).
- Crosses a module boundary / changes a shared contract / adds a
  persisted entity → also write preconditions, assumptions, outcomes.
- Auth, permissions, secrets · schema migration · tenant visibility ·
  payments · release assets · more than N files · the literal request
  does not map one-to-one onto the data model
  → full contract AND an independent review in a clean context before merge.

The three fields, written before any code:
1. intent — one sentence, what will be observably true when this is done.
2. escalation / candidate set — what is not mine to decide alone. If the
   request's wording could point at more than one thing in the data, list
   the candidates and ask; do not pick the likeliest one.
3. affected_layers — what I am changing, and what I am deliberately not.

Verification: nothing is marked verified on the strength of a promise.
Record what I actually ran — command output, query result, log line,
observed value — or write UNVERIFIED. "Pending" is never a pass.
A green build is a prediction, not an observation.

When a fix does not work on the first attempt: stop changing code and
establish one fact first.

<!-- MTM Contract · Apache 2.0 · Vast Intelligence Limited
     github.com/jewanchen/mtm-contract -->
```

The full one-page version, with the trigger table and a complete worked example, is [`MTM-LITE.md`](./MTM-LITE.md).

## Or install it

In Claude Code, two commands — the discipline becomes your agent's default behaviour, with a zero-dependency validator bundled alongside:

```
/plugin marketplace add jewanchen/mtm-contract
/plugin install mtm@mtm-contract
```

Details, the copy-a-folder alternative, and **how to update** (installing does not subscribe you to updates): [`plugins/mtm/`](./plugins/mtm/).

## What it is

Agentic coding agents fail in two recurring ways that current tooling does not address:

- They **hallucinate** APIs, entities, and endpoints that do not exist — confidently, because the agent does not know that it does not know.
- They suffer **architectural drift** across multi-step tasks, where a decision made at step 3 is silently contradicted by code generated at step 15.

Function-calling schemas and type checkers catch neither: both happen in the gap between intent and code generation.

**MTM Contract** is a markdown specification the agent fills in *before* writing implementation code and audits *after* the code ships — around a dozen fields for high-risk work, three for ordinary work, none at all for a typo. It externalises intent into an artifact that survives the agent's context window, binds its later decisions to the scope it declared, and gives uncertainty a legal place to live.

The specification is at **2.5**: one unified lifecycle, a greenfield branch, a debug branch, and an evolution engine.

### Papers

| | |
|---|---|
| **Start here — [MTM Contract 2.0: Put the Cheap Checks Before the Expensive Generation](./mtm-contract-2.0-article.md)** (July 2026) | The current architecture and the reasoning behind it: where agent-assisted work actually wastes effort, the ordering that fixes it, seven recurring situations where it pays, and what it does not fix. 繁體中文：[`.zh-TW`](./mtm-contract-2.0-article.zh-TW.md) |
| [MTM Contract: Preventing Hallucination and Architectural Drift in Agentic AI Coding](./mtm-contract-technical-article.md) (May 2026) | The original paper: the eleven-field contract, nine observed mechanisms of value, field-by-field rationale. Kept as the published record of v1.0; not retro-edited. |

---

## When the task is heavier

Schema changes, permissions, anything touching money or who-can-see-what get the full [`TEMPLATE.md`](./TEMPLATE.md) and a review in a clean context before merge — a subagent or a second session, given only the contract, the decisions, and the diff. Never the session that wrote the code: the reasoning that produced a gap is the reasoning that would review it.

[`MTM-LITE.md`](./MTM-LITE.md) §1 has the triggers that decide which. The rule of thumb — *if the contract takes longer than the code, skip it* — is real, and applies only to the two lightest tiers.

---

## What's in this repository

| File | Purpose |
|---|---|
| [`mtm-contract-2.0-article.md`](./mtm-contract-2.0-article.md) | **Start here.** The 2.0 article — what the discipline buys you, why it is shaped this way, one task end to end. Traditional Chinese: [`.zh-TW`](./mtm-contract-2.0-article.zh-TW.md). |
| [`plugins/mtm/`](./plugins/mtm/) | **Install it instead of remembering it.** A Claude Code plugin — two commands, or copy one folder — and the discipline becomes your agent's default behaviour, with a bundled zero-dependency validator that enforces the parts a document cannot. |
| [`MTM-LITE.md`](./MTM-LITE.md) | **One page, in English.** Tier triggers, the three fields, the one rule, the clean-context review, and a complete light-tier example. This is what to paste into your agent's rules file. |
| [`MTM-CORE.zh-TW.md`](./MTM-CORE.zh-TW.md) | The specification in Traditional Chinese — equivalent content, kept as the original. |
| [`MTM-CORE.md`](./MTM-CORE.md) | **2.5 specification (the spine).** One unified 0→6 lifecycle: Classify → Ground → Escalate → Contract → Implement → Self-check → Verify, the invariants, the tier triggers, and the canonical template. The files below are phase-level detail. 繁體中文：[`.zh-TW`](./MTM-CORE.zh-TW.md) |
| [`EVOLUTION.md`](./EVOLUTION.md) | **How this specification changes itself.** Case ledger → proposal queue → human gate → changelog; no rule takes effect without a person approving it. Every proposal is here in full, including the one that was closed and why. 繁體中文快照：[`.zh-TW`](./EVOLUTION.zh-TW.md) |
| [`mtm-contract-technical-article.md`](./mtm-contract-technical-article.md) | The full methodology paper (~450 lines): failure modes, field-by-field rationale, six production task case study, AI-to-AI extension, distribution strategy, comparison to related work. |
| [`TEMPLATE.md`](./TEMPLATE.md) | The ready-to-copy contract template, **2.0** — includes the `status` header and `observed_result`. Use this for structural and critical work; ordinary tasks need only the three fields in `MTM-LITE.md`. |
| [`MTM-Plan.md`](./MTM-Plan.md) | Greenfield branch: turn a one-sentence product idea into a buildable skeleton by eliciting the hard-to-reverse choices in plain language. The fork library and the handoff format live here. 繁體中文：[`.zh-TW`](./MTM-Plan.zh-TW.md) |
| [`MTM-Arch.md`](./MTM-Arch.md) | ⚠️ **Superseded, retained as history.** Everything still current was absorbed into CORE 2.5; the file opens with a table saying where each part went. Traditional Chinese. |
| [`MTM-Verify.md`](./MTM-Verify.md) | The independent audit: what the auditor reads, the four stages, and its conduct — including that it is a witness, not a judge. 繁體中文：[`.zh-TW`](./MTM-Verify.zh-TW.md) |
| [`MTM-VERIFY-REPORT-TEMPLATE.md`](./MTM-VERIFY-REPORT-TEMPLATE.md) | The audit report template, each section naming the failure modes it covers. 繁體中文：[`.zh-TW`](./MTM-VERIFY-REPORT-TEMPLATE.zh-TW.md) |
| [`contracts/`](./contracts/) | MTM contracts for changes to MTM itself (dog-fooding). ⚠️ Traditional Chinese. |
| [`examples/`](./examples/) | Six real production contracts, sanitised. **Note: these predate 2.0** — they show the eleven fields but not the `status` header or `observed_result`. The current shape is in `TEMPLATE.md`, and a complete light-tier example is in `MTM-LITE.md` §5. |
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

| What | Form | Status |
|---|---|---|
| **The specification** | Markdown convention + canonical template + examples + integration guides | ✅ **Available now** (this repository) |
| **Agent behaviour** | The same core delivered as instructions to your agent, an editor rules file, or a starting prompt — nothing to install | ✅ Available now: use `MTM-CORE.md` directly, or see [`integrations/`](./integrations/) |
| **Enforcement tooling** | Mechanical checks: no empty fields, no clause marked passing while its evidence is a promise, no task closed without a ledger line | Planned, for continuous integration and advanced setups |

**A correction to the roadmap published in the first article.** That version put a CLI next, gated on 20–50 trial samples. The sample gate has since been passed several times over, and the order was still wrong: the useful first conduit is agent *behaviour*, because the specification's own rule is that the machinery stays internal — the person delegating work should not have to operate a tool to benefit. Enforcement tooling remains valuable and is now positioned where it belongs: in CI and advanced setups rather than in a first-time user's path. Section 12 of the 2.0 article explains why enforcement matters more than we originally thought — a rule the specification called mandatory stopped being honoured within a month of promotion.

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

For replication studies, enforcement-tooling collaboration, or integration partnerships, please use the contact channels above. The most valuable contribution is a replication we cannot run ourselves: the same tasks, on a different codebase, with and without the discipline, judged by someone who did not write it.
