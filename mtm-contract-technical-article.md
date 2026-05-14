# MTM Contract: A Pre-Execution Specification Layer for Reliable AI Software Engineering

**An open-source methodology from Vast Intelligence Limited.**
**Observed in production: 6/6 first-pass success, zero compile-time hallucinations, one v1→v2 redesign caught before implementation.**

---

**Published:** May 14, 2026
**Author:** Vast Intelligence Limited
**Contact:** jeremy.chen@vastitw.com
**Repository:** github.com/jewanchen/mtm-contract
**License:** Apache 2.0 (see LICENSE), attribution required (see NOTICE)
**Version:** Methodology v1.0 · 6 production trial samples · 11-field contract specification

---

## Abstract

We present **MTM Contract**, a specification pattern that AI coding agents fill out *before* writing implementation code, enforcing explicit declaration of intent, preconditions, schema assumptions, cross-module obligations, and escalation triggers. Contracts are persisted as plain markdown alongside source code, then audited clause-by-clause after the change ships — marking each as `PASS`, `FAIL`, or `MUTATED` with a reason.

In a six-task production trial on a multi-tenant SaaS application, every task committed on the first attempt with zero compile-time hallucinations, and one task underwent a fundamental redesign (`v1` → `v2`) during the contract's escalation phase — at a fraction of the cost of catching that redesign after implementation. The same 11-field structure, observed working for human-AI clarification, maps directly onto the requirements for AI-to-AI agent coordination, multi-agent state handoff, and structured function-calling schemas — suggesting MTM Contract is not a workflow but a substrate.

This article documents the pattern, the trial results, the reasoning that connects each contract field to a specific class of AI failure, and a phased distribution strategy (markdown convention → CLI toolchain → MCP server + IDE plugins).

---

## 1. The Failure Modes We Keep Seeing

AI coding agents — whether driving a full repository, generating a single function, or executing a multi-step plan — fail in patterns that recur across model families, tasks, and tool integrations. We catalogue five.

### 1.1 Hallucinated APIs and Entities

The agent confidently invokes a function name, database column, or endpoint that does not exist. The agent does not know that it does not know. The token prediction landed in a high-probability neighborhood, and the agent took that as licence to commit.

This is not solved by better prompts. It is solved by forcing the agent to write down what it is assuming the API surface looks like, and by giving validation cheap feedback to surface mismatches before code runs.

### 1.2 Silent Cross-Module Overwrites

The agent edits a function whose behaviour is depended upon by callers it has never read. The compiler is happy; tests are absent; the production change ships; a downstream service breaks. The agent never declared, "I am modifying the contract this function offered to other modules."

Type systems catch *signature* changes. They do not catch *semantic* changes ("this function used to return results sorted by date; now it does not"). Cross-module contracts must be declared in prose, not inferred from diffs.

### 1.3 Context Drift Across a Long Task

A multi-step task accumulates decisions: "I'll use Redis here." "I'll add a `version` column for optimistic locking." "I'll skip rate-limiting for now." By step 15, the agent has forgotten step 3, and the new code contradicts the earlier decision. Long context windows do not solve this; they dilute it.

Decisions need to be persisted *outside* the model context as load-bearing artifacts. A markdown contract works because it is short, scannable, and re-readable. The model re-encounters the same constraints every time it returns to the file.

### 1.4 Unscoped Escalation

The agent encounters ambiguity — a precondition it cannot verify, a business rule it cannot derive, a third-party API behaviour it cannot probe — and does one of two failing things: bullshits a plausible answer, or stops without saying what it needed.

The right behaviour is to escalate, *with the specific question*. But this requires the agent to have *enumerated, in advance*, which categories of decision are not its to make. Without that enumeration, the agent has no schema for "this is when I stop and ask."

### 1.5 No Post-Hoc Verification Discipline

Code ships. Tests pass. The compiler is happy. The task is declared "done." Two weeks later, a user reports that the change does not actually do what was intended — it does something *almost* like what was intended.

The gap is between "code-level correctness" (tsc passes, tests green) and "observation-level correctness" (the user behaviour described in the original intent has been observed in staging or production). The latter requires somebody — agent or human — to walk back through the original intent and check each clause against shipped reality. Without a contract recording the original intent in structured form, this audit is impossible.

---

## 2. The Pattern: MTM Contract in One Page

An MTM Contract is a markdown file with **eleven required sections**, written *before* implementation begins, and amended with an audit section *after* implementation ships.

| Field | Purpose | Failure Mode It Addresses |
|---|---|---|
| **intent** | One observable sentence stating what the user will be able to do, see, or experience. | 1.5 No post-hoc verification |
| **affected_layers** | Enumeration of which subsystems change and which deliberately do not. | 1.2 Silent cross-module overwrites |
| **preconditions** | Conditions that must be true before work proceeds, each with a `verified_by` reference. | 1.1 Hallucinated APIs |
| **schema_assumptions** | Beliefs about data shapes, defaults, invariants, each with a `source`. | 1.1 + 1.3 (assumption drift) |
| **cross_module_contract** | What this work emits, what it listens to, what it assumes others do, what others depend on it doing. | 1.2 Cross-module overwrites |
| **expected_outcome** | Externally observable end-states phrased as "user X observes Y," each with a `verifiable_by`. | 1.5 Post-hoc verification |
| **confidence** | High / medium / low, plus enumerated low-confidence sub-items with plans. | 1.4 Unscoped escalation |
| **escalation** | Decisions outside the agent's authority and conditions that should halt the work. | 1.4 Unscoped escalation |
| **grounding** | Citations for every claim in the contract — spec sections, prior commits, user quotes. | 1.1 Hallucinated facts |
| **rollback_plan** | Code, schema, and environment rollback paths for the change. | Risk hygiene |
| **test_plan** | Local, staging, and production smoke steps. | 1.5 Verification |

After the change ships, the contract is amended:

- Every clause is marked `PASS`, `FAIL`, or `MUTATED`.
- A `MUTATED` table records each deviation from plan with a one-line reason.
- `MISSING / Follow-up` lists items deferred to later tasks.
- `Overall` reports code-level result, observation-level result, and contract completeness.

The contract is the artifact. The discipline of filling it out — and the discipline of auditing it afterward — is the methodology.

---

## 3. Quick Start: Try It in 10 Minutes

The fastest way to evaluate MTM Contract is to apply it to a task you were about to delegate to an AI coding agent anyway. Here is the 10-minute procedure.

**Minute 0–1.** Clone or download `TEMPLATE.md` from this repository. Place a copy at `contracts/YYYY-MM-DD_<task>.md` in your project.

**Minute 1–4.** Fill in `intent`, `affected_layers`, `expected_outcome`. These are the cheapest three fields and the highest-leverage. Already, you have stated *what the user will observe* — a check most prompts skip.

**Minute 4–7.** Fill in `preconditions` and `schema_assumptions`. Each entry needs a `verified_by` or a `source`. If you can't write one, write `UNKNOWN: <what to grep before writing code>`. The five-minute grep that follows is the entire point.

**Minute 7–9.** Fill in `cross_module_contract`, `confidence`, `escalation`. If you find yourself writing `confidence: low` for the overall task, *stop and re-scope* before implementing.

**Minute 9–10.** Hand the contract to the AI coding agent as the work specification. After the work ships, return to the file and write the audit section.

If, at any point in minutes 0–9, you find a contract field you cannot fill in honestly, the contract has already paid for itself: it has surfaced a hidden ambiguity that would have produced rework after implementation.

---

## 4. Why It Works: Mapping Fields to Failure Modes

The eleven fields are not arbitrary. Each addresses a specific failure mode with a specific mechanism.

### 4.1 `intent` and `expected_outcome` make verification possible

A typical prompt says "implement the resignation flow." A typical MTM intent says "Admin marks employee X as resigned; within 30 seconds, all contact-card holders' address books reflect the new grey-check archived state, and the employee's account quota is released."

The second sentence cannot be subjectively interpreted to mean different things by different people. It states an *externally observable* outcome. A reviewer can check it; staging traffic can verify it. The first sentence cannot be verified at all — implementation is "done" whenever the implementer says so.

`expected_outcome` extends this by listing every observable end-state with a `verifiable_by` reference. The audit section then walks back through and asks: *Is this observable, in staging, today?* When the answer is "we shipped, but we haven't observed it yet," that is now a tracked gap rather than a silent assumption.

### 4.2 `preconditions` and `schema_assumptions` interrupt hallucination

The agent cannot proceed past `preconditions` without writing `verified_by: <commit / migration / health check>` for each item. The act of writing that reference forces a grep, a database probe, or an admission of `UNKNOWN: <what to verify>`. Hallucinated APIs cannot survive this step.

`schema_assumptions` does the same for data: every belief about field types, defaults, and invariants must cite a source. In trial task 02 (Section 6.2 below), this single discipline caught two production-blocking drifts — fields declared in the entity but missing from the validation DTO. The agent's first instinct had been to use those fields freely; the contract step forced a grep that surfaced the gap.

### 4.3 `cross_module_contract` makes the implicit explicit

Most function changes are described in terms of what the function does internally. MTM forces the agent to describe what the function *promises to callers* and what it *requires of dependencies*. The "emit" / "listen" / "I assume others will" / "others depend on me to" four-line block produces, in roughly thirty seconds of writing, a more honest interface contract than the function signature itself.

When this field is honest, two phenomena recede:

- The downstream caller break ("you changed the return shape and didn't tell me"), because the change is now declared at write time.
- The duplicate-work loss ("we already had a helper that does this"), because the `emit` line surfaces existing infrastructure during the grep that follows.

### 4.4 `confidence` + `escalation` legitimise uncertainty

The agent has no native vocabulary for "I am not sure." It will either pretend, or stop without explanation. `confidence: low` plus an enumerated escalation list gives uncertainty a *legal* place to live in the workflow. The agent reports its confidence in writing, and reports specifically *what it is uncertain about* and *what plan it would propose if not escalated*.

In trial task 05 (Section 6.5 below), the agent's `confidence` was `medium-high` overall, with one specific low-confidence sub-item: "the user's intended scope for recipient routing." That single flag triggered the escalation that produced a v1 → v2 redesign — at the cost of one five-minute conversation, not a one-day rewrite.

### 4.5 `grounding` defeats fabricated rationale

The audit log of any AI-assisted PR is full of plausible-sounding justifications that turn out, on inspection, to cite nothing. `grounding` requires every clause to name its source — a spec section, a prior commit, a verbatim user quote with a date. If the source does not exist, the clause is marked `SPECULATIVE` and reviewed first.

This is uncomfortable. It surfaces, in writing, exactly how much of the contract is the agent's invention rather than received fact. We consider this a feature.

### 4.6 The audit completes the loop

Without a post-hoc audit, the contract is a planning aid that decays into noise once the code ships. The audit closes the loop. Every clause earns one of three marks:

- **`PASS`** — implementation matches plan.
- **`FAIL`** — implementation does not match plan; explain why and create a follow-up.
- **`MUTATED`** — implementation deviated from plan, but with a reason recorded on the spot.

`MUTATED` is the most informative of the three. It captures *contract incompleteness* (the plan didn't anticipate a constraint) rather than *implementation failure* (the work missed the plan). Over time, the `MUTATED` reasons become training data for what to put in *future* contracts — a self-improving spec, in the same epistemic shape as iterative bug-fixing of code.

---

## 5. Empirical Validation: Six Production Tasks

We applied MTM Contract for two weeks on a production multi-tenant SaaS application during the build-out of its enterprise feature set. Six tasks of varying scope completed under the methodology. All commit references are real and live in the application's repository; business specifics are abstracted to preserve operational confidentiality.

### 5.1 Trial setup

- **Sample size:** Six build-mode tasks plus two retroactive audits of two earlier (pre-trial) commits.
- **Scope range:** From single-endpoint refactors to multi-entity workflows spanning backend, web admin dashboard, and mobile clients.
- **Failure mode definition:** A "hallucination" is a call to a non-existent entity, field, or endpoint, *or* a violation of a schema invariant that should have been visible from prior commits.
- **One-pass commit definition:** First commit attempt passes type checking, build, and static analysis on every affected codebase (backend tsc + framework build + frontend tsc + mobile analyze).

### 5.2 The six tasks at a glance

| Task | Domain | Scope | Code-level result | Hallucinations |
|---|---|---|---|---|
| **01: Push dispatcher** | Notification fanout with two-tier UX (banner vs silent) | Backend service + mobile push router | First-pass PASS | 0 |
| **02: Entity update with broadcast and email** | Multi-tenant write path adds push fanout + audit email | Backend DTO + service + email template + mobile push router + web admin | First-pass PASS | 0 |
| **03: Status lifecycle transitions** | Three state-machine endpoints with derived UI (paid-feature-aware) | Backend service + endpoints + web admin + mobile derived field | First-pass PASS | 0 |
| **04: Aggregated dashboard endpoint** | Replace 4-query + N+1 page with single endpoint, parallel queries | Backend service + endpoint + web admin rewrite | First-pass PASS | 0 |
| **05: Recovered-entity database (paid)** | New entity, migration, paid-feature paywall, dashboard query page, CSV export | Backend entity + migration + service + endpoints + web admin (2 pages + sidebar nav) | First-pass PASS | 0 |
| **06: Batch operations** | Three batch flows on existing selection panels | Backend service + endpoints + web admin (2 pages, modals) | First-pass PASS | 0 |

**Aggregate trial metrics:**

- **One-pass commit rate:** 6 / 6 (100%)
- **Compile-time hallucinations:** 0 / 6 (one *resolved* schema-name mismatch on task 04 was caught by the type checker within seconds; we count it as zero because it never reached commit).
- **Contracts that surfaced cross-module work the agent had not anticipated:** 4 / 6 (tasks 01, 02, 04, 05)
- **Contracts that produced a major redesign during escalation:** 1 / 6 (task 05, see below)
- **Contracts that produced architectural decisions worth recording separately:** 4 distinct decisions over 6 tasks

### 5.3 The most informative result: task 05's v1 → v2 redesign

We highlight task 05 because it is the case that justifies the contract's existence.

The task was to let admins recover a list of customers exchanged via a former employee's enterprise card, after that employee resigned. The agent wrote a `v1` contract proposing to *copy* the recovered records into a chosen recipient admin's personal address book on the mobile client. The contract surfaced this routing decision as an explicit `escalation` question with three options.

The user, reading the contract before implementation, rejected `v1` outright: routing recovered customers into anyone's personal address book would pollute that admin's contacts with a former employee's customer history, and would not survive that admin's own future departure. The user proposed a `v2`: dedicated enterprise-owned data store, queryable on the dashboard, CSV-exportable.

The escalation conversation took roughly five minutes. The implementation, redesigned, took the same time it would have taken in `v1`. Had the work shipped in `v1`, the cost to discover the same issue would have been one production deploy plus a non-trivial migration to extract personally-owned rows back into a shared store — a substantial loss that the contract converted into a no-op.

The full text of both `v1` and `v2` is preserved in the contract artifact (see `examples/05-recovered-entity-database.md`), making the deviation auditable in perpetuity.

### 5.4 Architectural decisions surfaced during the trial

Four decisions emerged from contract-phase discussion that would not have surfaced from the original task description:

- **D-1 (continuous-edit handling):** Conflict between concurrent admins editing the same record was deferred to a UX-level "confirm-save" button rather than backend deduplication. The decision was reached by enumerating three options in `escalation`; the chosen option turned out to be the cheapest and most reviewable.
- **D-2 (commit-boundary merge):** Two adjacent tasks (push-to-employee and push-to-contact-holder) collapsed into a single commit after `affected_layers` revealed they would touch the same dispatcher function. The decision avoided shipping a deliberately-incomplete PR that a follow-up PR would patch.
- **D-3 (notification tiering):** Mandatory `expected_outcome` per audience surfaced an industry-UX question: should employees be notified differently from contact-holders, and should resignation events be silent for privacy? The decision became a documented invariant followed by every subsequent push-dispatching task.
- **D-4 (race-latest concurrency):** A bug in a mobile-client cache layer, discovered during review-mode audit of an earlier commit, escalated to a refactor of the concurrency primitive across four providers. The decision (`fetchGen` race-latest replacing inflight-future gating) was named, debated, and recorded as a class-of-bug ruling rather than a one-off fix.

Decisions of this kind, recorded in a dated log, become institutional memory rather than tribal knowledge.

### 5.5 Retroactive audit on pre-trial commits

Two earlier commits, made before the trial began, were audited backwards. Reconstructing the contract from session memory plus commit messages plus shipped code surfaced:

- **Drift between declared and shipped behaviour:** in one case the contract's `expected_outcome` declared three observable end-states; on retroactive review, *zero* of them had been verified in staging. The shipped behaviour was "compile-time correct, observation-untested."
- **Workflow gap:** contracts written conversationally were not persisted as artifacts and were lost when the session ended. The retroactive audit could only reconstruct them imperfectly. This led to a process change: **contracts must be written to disk before implementation begins.**

This gap — between "code-level shipped" and "observation-level shipped" — appeared in every audit. We do not yet have a clean mechanism for closing it short of staging discipline; we record the gap explicitly in every contract's `Overall` summary.

---

## 6. The Two Layers: Human-AI Now, AI-to-AI Next

MTM Contract was observed working as a *human-AI clarification* tool: a human-readable markdown file mediating between an engineering decision-maker and an AI agent doing implementation. We claim the same eleven-field shape applies, with minor encoding changes, to *AI-to-AI* coordination — and that the trial's success is therefore a lower bound on the methodology's scope, not the full story.

### 6.1 Why the same shape applies upward

Multi-agent systems — whether autonomous planner-executor pairs, orchestrated frameworks like LangGraph or CrewAI, or future agentic OS architectures — face exactly the failure modes documented in Section 1, but at higher frequency and lower visibility:

- One agent **hallucinates** an output schema that the receiving agent then chokes on.
- Agents **silently overwrite** each others' state because no agent declared what it was committing to.
- Long agent chains **drift** as each handoff loses fidelity; by hop 10, the original intent is no longer recoverable.
- An agent **escalates by stopping silently** because it has no schema for what to escalate or to whom.
- Multi-agent runs **finish without verification**, because no agent owns the verification step.

The cure is structurally identical: every handoff between agents should carry a contract. The medium changes — markdown becomes JSON, escalation triggers become structured event types, audit marks become run-end annotations on a trace — but the eleven fields map cleanly.

### 6.2 An MTM contract as a function-call schema

A direct translation of the markdown contract into a JSON schema usable by OpenAI function-calling, Anthropic tool-use, or any MCP-compatible client:

```json
{
  "name": "execute_task",
  "description": "Execute a task with MTM Contract pre-conditions.",
  "input_schema": {
    "type": "object",
    "required": ["intent", "preconditions", "expected_outcome",
                 "confidence", "escalation"],
    "properties": {
      "intent": { "type": "string" },
      "affected_layers": { "type": "array", "items": { "type": "string" } },
      "preconditions": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["condition", "verified_by"],
          "properties": {
            "condition": { "type": "string" },
            "verified_by": { "type": "string" }
          }
        }
      },
      "schema_assumptions": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["assumption", "source"],
          "properties": {
            "assumption": { "type": "string" },
            "source": { "type": "string" }
          }
        }
      },
      "cross_module_contract": {
        "type": "object",
        "properties": {
          "emit": { "type": "array", "items": { "type": "string" } },
          "listen": { "type": "array", "items": { "type": "string" } },
          "depends_on": { "type": "array", "items": { "type": "string" } },
          "guaranteed_to_callers": { "type": "array", "items": { "type": "string" } }
        }
      },
      "expected_outcome": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["outcome", "verifiable_by"],
          "properties": {
            "outcome": { "type": "string" },
            "verifiable_by": { "type": "string" }
          }
        }
      },
      "confidence": {
        "type": "object",
        "required": ["overall"],
        "properties": {
          "overall": { "enum": ["high", "medium", "low"] },
          "low_confidence_subitems": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      },
      "escalation": {
        "type": "object",
        "properties": {
          "decisions_to_defer": { "type": "array", "items": { "type": "string" } },
          "halt_conditions": { "type": "array", "items": { "type": "string" } }
        }
      },
      "grounding": { "type": "array", "items": { "type": "string" } }
    }
  }
}
```

In a multi-agent system, the planner agent emits this schema's instance as its hand-off to the executor agent. The executor agent's first step is precondition verification — calling external tools to confirm each `verified_by` clause is satisfiable. Confidence below a configured threshold triggers a documented escalation path. The output annotates each `expected_outcome` with an observation.

The system's logs are now auditable: every agent decision is preceded by a contract and followed by an audit, in the same shape as the human-readable trial documented in Section 5.

### 6.3 What changes between layers, and what does not

| Concern | Human-AI markdown | AI-to-AI JSON |
|---|---|---|
| Field semantics | Identical | Identical |
| Storage | File in `contracts/` directory | Trace event in run log |
| Validation | Code review, conversation | JSON-schema validator, runtime |
| Escalation channel | Conversation back to operator | Structured event to orchestrator |
| Audit timing | Post-merge | Post-run, automated |
| Compliance enforcement | Discipline | Schema-rejection at runtime |

The methodology is invariant. The medium is plug-replaceable.

---

## 7. Distribution Strategy

We deliberately ship MTM Contract as a **methodology** first and tooling second. The order matters: locking the methodology into tooling before it stabilises produces tooling debt that outweighs adoption benefit.

### 7.1 Phase 1: Markdown convention (current state)

Available immediately. Zero dependencies. The full pattern is `TEMPLATE.md` and this article. Adoption requires only that a team agree to fill in the template before AI-delegated work. We strongly encourage forks: rename it, modify field names to match your domain, drop fields you don't need, add fields you do. The license permits this; the attribution clause asks only that the lineage be cited.

### 7.2 Phase 2: CLI toolchain (planned)

A language-agnostic CLI (`mtm`) is planned for release once the methodology has accumulated approximately 20–50 trial samples across multiple teams and codebases:

```bash
mtm new <task-name>             # create contract from template
mtm validate <file>             # enforce 11-field completeness
mtm audit <file>                # walk through PASS/FAIL/MUTATED prompts
mtm metrics                     # one-pass rate, hallucinations caught, MUTATED frequency
mtm list                        # index of contracts in the repo, status
mtm search <keyword>            # find prior similar contracts
```

The CLI consumes markdown — the source of truth remains the file. The CLI enforces, indexes, and reports.

### 7.3 Phase 3: Editor and orchestrator integrations (planned)

Once the CLI is stable:

- **MCP server** — exposes `mtm` commands as Model Context Protocol tools. Anthropic-compatible clients (Claude Desktop, MCP-aware IDEs, agent frameworks adopting MCP) get MTM integration without code changes.
- **Claude Code skill** — invokes the CLI via Claude Code's skill system; surfaces contracts in the editor's slash-command palette.
- **Cursor extension** — same integration pattern, surfaced as a Cursor command.
- **Aider edit-block annotation** — Aider's edit-block protocol gets a `mtm:` annotation for contract-bound edits.
- **OpenAI function-calling schema** — published as a JSON schema, ready to register as a function in the OpenAI Assistants API or as a tool in any function-calling-aware orchestrator.

These are conduits, not new methodology. Each is a thin wrapper around the CLI; the CLI is a thin enforcement layer around the markdown specification.

### 7.4 Open adoption path

The Phase 2 and Phase 3 work is published as the maintainers complete it. Pull requests from external implementers are accepted under Apache 2.0. We do not gate Phase 1 on internal Phase 2 progress: the methodology is usable today, and any team adopting it now is producing the trial data that Phase 2 needs.

---

## 8. Comparison to Related Work

| Feature | MTM Contract | Pydantic / Instructor | Aider edit blocks | OpenAI tool-use / Anthropic MCP | Plain prompts |
|---|---|---|---|---|---|
| Pre-execution intent declaration | ✓ required | ✗ | ✗ | △ via function description | ✗ |
| Cross-module obligations explicit | ✓ first-class | ✗ | ✗ | ✗ | ✗ |
| Confidence + escalation in schema | ✓ first-class | ✗ | ✗ | △ ad hoc | ✗ |
| Grounding citations required | ✓ first-class | ✗ | ✗ | ✗ | ✗ |
| Post-hoc audit linked to plan | ✓ first-class | ✗ | ✗ | ✗ | ✗ |
| Schema validation of output | △ via audit | ✓ runtime | ✗ | ✓ runtime | ✗ |
| Tool integration | △ (Phase 3 planned) | ✓ Python-only | ✓ Aider-only | ✓ within ecosystem | n/a |
| Zero-dependency adoption | ✓ markdown only | ✗ Python | ✗ Aider | ✗ SDK | ✓ |
| Cross-agent compatibility | ✓ medium-agnostic | △ tied to Python | ✗ | △ within vendor | ✗ |

MTM Contract is **complementary** to Pydantic, function-calling, and MCP. The latter validate *output shape*; MTM validates *intent and constraint shape* before output is generated. A mature pipeline uses both: an MTM contract pre-execution to bound the work, and runtime schema validation post-execution to check that the output conforms to the contract's declared cross-module obligations.

We are not aware of prior published work that combines (a) pre-execution declared intent, (b) mandatory cross-module obligations, (c) first-class confidence and escalation fields, (d) mandatory grounding citations, and (e) a post-hoc audit clause-by-clause linked back to the original plan. MTM Contract is, to our knowledge, the first to package these as a single methodology.

---

## 9. Limitations and Honest Caveats

We deliberately list this article's limitations rather than burying them.

- **Sample size is small.** Six tasks on one application over two weeks is suggestive, not statistically conclusive. Independent replication on additional codebases is the most valuable next step.
- **The trial was single-agent.** All six tasks were executed by a single AI agent in conversation with a single human decision-maker. AI-to-AI claims in Section 6 are extrapolation, not measurement.
- **No A/B comparison.** We do not have matched-pair data for the same six tasks performed *without* contracts. The one-pass commit rate (6/6) could in principle reflect easy tasks rather than effective methodology. We mitigate this by including task 05 — a task where the v1 contract was clearly inadequate and required a redesign that, in our judgement, would not have surfaced from a plain prompt.
- **Observation-level verification is incomplete.** Every audit in the trial closes with "code-level PASS, observation-level UNVERIFIED-IN-STAGING." The trial recorded the gap honestly but did not close it. Closing this gap is part of the team's next two weeks of work and not part of this article's claims.
- **`grounding` requires honest reporting.** The methodology assumes the agent (or the human) does not fabricate citations. We have no automated guard against fabricated `verified_by` references. CLI-stage tooling (Phase 2) will validate at least file-existence and commit-hash-existence; deeper semantic grounding remains a discipline question.
- **Audit discipline decays in absence of pressure.** Without external review of the audit (e.g., a code review reviewer who checks audit clauses against the contract), the audit becomes self-reported by the implementer. We recommend pairing MTM Contract with code review that examines the audit section before merge.
- **Bureaucratic cost on trivial work.** A typo fix or one-line config bump does not benefit from an eleven-field contract. The methodology is appropriate when the agent would otherwise touch multiple files, multiple subsystems, or any novel API surface. We codify this as: "if writing the contract takes longer than writing the code, skip the contract."

---

## 10. Future Work

- **Larger-N empirical study.** A formal study on 50+ tasks across 3+ codebases, with matched-pair plain-prompt controls, will produce the data the present article is too small to support.
- **Phase 2 CLI release.** Validation, indexing, audit-walk, and metrics commands. Open-source under Apache 2.0.
- **Phase 3 integrations.** MCP server, Claude Code skill, Cursor extension, Aider annotation, OpenAI function-calling schema. Each as a thin wrapper over the CLI.
- **Benchmark suite.** A reproducible benchmark — a set of canonical AI-coding tasks with hidden traps designed to trigger the five failure modes from Section 1 — measuring agent performance with and without MTM Contract overhead.
- **Multi-agent contract specification.** Extension of the eleven fields to handle agent handoff semantics: how does agent A's `expected_outcome` become agent B's `intent`? What does `escalation` look like when there is no human in the loop?
- **Contract evolution patterns.** Documented templates for common task shapes — schema migrations, API additions, refactors, paid-feature gating, batch operations. Today, every team rewrites these from `TEMPLATE.md`; mature templates per task family will shorten time-to-first-contract.

---

## 11. License and Citation

This work is licensed under the **Apache License, Version 2.0**. See `LICENSE` for the full text and `NOTICE` for attribution requirements. Briefly: free for commercial and non-commercial use, modification, redistribution, with attribution to Vast Intelligence Limited required in derivative works (including tools, libraries, and adapted documentation that implement the MTM Contract specification).

If you build on this work, please cite:

```
Vast Intelligence Limited. (2026).
MTM Contract: A Pre-Execution Specification Layer for
Reliable AI Software Engineering.
https://github.com/jewanchen/mtm-contract
Published: May 14, 2026.
```

---

## 12. Contact

**Company:** Vast Intelligence Limited
**Email:** jeremy.chen@vastitw.com
**Phone:** +886 2 2706 7590
**Website:** vastitw.com/mtm

For collaboration on Phase 2 and Phase 3 tooling, replication studies, or integration partnerships with AI coding tools and orchestrators, please use the contact channels above.

---

*This document is published to establish a public record of the MTM Contract methodology as of May 14, 2026. All methodological descriptions, trial data, and architectural designs are the intellectual property of Vast Intelligence Limited and are released for public use under the Apache 2.0 license with the attribution requirements specified in `NOTICE`.*
