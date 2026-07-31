# MTM Contract: A Framework for Preventing Hallucination and Architectural Drift in Agentic AI Coding

**A discipline for containing agentic AI's two recurring failure modes.**

**An open-source methodology from Vast Intelligence Limited. Observed across 9 production scenarios — hallucination prevention, mid-task architectural drift correction, user intent disambiguation, and emergent design-pattern crystallization.**

---

**Published:** May 14, 2026
**Author:** Vast Intelligence Limited
**Contact:** jeremy.chen@vastitw.com
**Repository:** github.com/jewanchen/mtm-contract
**License:** Apache 2.0 (see LICENSE), attribution required (see NOTICE)
**Version:** Methodology v1.0 · 6 production trial samples · 11-field contract specification
**Continued by:** [*MTM Contract 2.0 — Put the Cheap Checks Before the Expensive Generation*](./mtm-contract-2.0-article.md) (July 2026; 繁體中文：[`.zh-TW`](./mtm-contract-2.0-article.zh-TW.md)). The current specification is **2.0** — see [`MTM-CORE.md`](./MTM-CORE.md). This article remains the published record of the methodology as of May 2026 and is not retro-edited.

---

## Abstract

Agentic AI coding agents fail in two recurring ways that current tooling does not address. They **hallucinate** APIs, entities, and endpoints that do not exist — confidently, because token prediction landed in a plausible neighborhood and the agent does not know it does not know. And they suffer **architectural drift** across multi-step tasks — where decisions made in step 3 are silently contradicted by code generated in step 15, because the long context window dilutes earlier commitments rather than preserving them. Function-calling schemas and type checkers do not catch these failures: both occur in the gap between intent and code generation, before any token the runtime can validate.

We present **MTM Contract**, a specification framework that agents fill out *before* writing implementation code. It externalizes intent, preconditions, schema assumptions, cross-module obligations, and escalation triggers into a markdown artifact that survives the agent's context window and binds the agent's future decisions to its declared scope. Contracts are audited clause-by-clause after the change ships — marking each as `PASS`, `FAIL`, or `MUTATED` with a reason — closing the loop between declared intent and observable outcome.

Across nine production scenarios on a multi-tenant SaaS application, MTM Contract demonstrated nine distinct mechanisms of value: hallucination prevention through mandatory `verified_by` references, mid-task architectural drift correction through persistent markdown anchors, cross-module discovery during the contract phase, user intent disambiguation through structured escalation, methodology overrides of stale planning documents, decision-graph reuse through a logged paywall framework, and emergent meta-pattern crystallization. One scenario produced a fundamental `v1` → `v2` redesign during the contract's escalation phase — at five minutes of conversation cost, compared with the production rollback and migration the wrong-shaped `v1` would have required.

The same 11-field structure, observed working for human-AI clarification, maps directly onto the requirements for AI-to-AI agent coordination, multi-agent state handoff, and structured function-calling schemas — suggesting MTM Contract is not a workflow but a substrate.

This article documents the pattern, the nine observed mechanisms, the reasoning that connects each contract field to a specific class of agentic failure, and a phased distribution strategy (markdown convention → CLI toolchain → MCP server + IDE plugins).

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

## 5. Empirical Validation: Nine Mechanisms of Value

We applied MTM Contract on a production multi-tenant SaaS application during the build-out of its enterprise feature set. Across nine distinct production scenarios, we observed **nine distinct mechanisms** by which the methodology delivered value. We document the mechanisms rather than the task count: the persuasive evidence is the *kinds* of failure the contract intercepted, not the cumulative number of intercepts.

All commit hashes are real and live in the application's repository; business specifics are abstracted to preserve operational confidentiality. Each mechanism is documented in detail in `examples/`, with full original contract + audit text.

### 5.1 Methodology of observation

- **Scope of work:** nine production scenarios over a working period, ranging from single-endpoint refactors to multi-entity workflows spanning backend, web-admin dashboard, and mobile clients.
- **What we tracked:** for each scenario, we recorded (a) the contract text before implementation, (b) the implementation diff, (c) the audit text after shipping. The triple — pre-plan, code, post-review — makes each scenario auditable in perpetuity.
- **What we did not measure:** we did not run a matched-pair control without contracts. The claims in this section are therefore about *the kinds of value* the methodology produced, not about a quantitative reduction relative to a control group. We discuss this limitation explicitly in §9.

### 5.2 The nine mechanisms

| # | Mechanism | Scenario | What the contract caught that an unstructured prompt would have missed |
|---|---|---|---|
| **1** | **Hallucination prevention through forced grounding** | Multi-tenant entity update (Ex. 02) | DTO drift bug — fields declared on the entity and used by frontend code but absent from the update DTO. The PATCH endpoint had been silently dropping them. The contract's `schema_assumptions` field forced a grep that surfaced the gap before the agent referenced the missing fields in implementation. |
| **2** | **Cross-module discovery during the contract phase** | Push notification dispatcher (Ex. 01) | An existing private helper that did half the work for one of the two callers was discovered during the contract's `affected_layers` grep. The two adjacent tasks merged into one commit and removed the duplicate helper, instead of shipping a parallel implementation. |
| **3** | **Architectural decision inheritance** | Status lifecycle transitions (Ex. 03) | A prior architectural decision (banner-vs-silent push policy from a previous task) was carried over into the new task because `cross_module_contract` explicitly cited the prior decision-log entry. Resignation events would otherwise have re-litigated whether the resigning employee should be banner-notified ("you were resigned") — a decision already settled and recorded. |
| **4** | **Design-time architectural reasoning** | Aggregated dashboard endpoint (Ex. 04) | An N+1 query pattern was identified at the contract stage, not at the implementation stage. The replacement (single aggregated endpoint with `Promise.all` parallel queries) was treated as the design itself rather than a refactoring follow-up. Three new endpoints, one new query pattern, one paywall guard — all reasoned about as a unit. |
| **5** | **Direction correction at the escalation step** | Recovered-entity database (Ex. 05) | The agent's `v1` contract proposed copying recovered customer records into a chosen recipient admin's personal address book on the mobile client. The user, reading the contract before implementation, rejected `v1` outright: it would pollute an admin's personal contacts with a former employee's customer history. `v2` shifted to a dedicated enterprise-owned dashboard store with CSV export. **Five minutes of escalation conversation prevented a multi-day migration to extract personally-owned rows back into a shared store.** This is the canonical case for the methodology. |
| **6** | **Methodology overrides stale planning** | Concurrency lock (Ex., commit `5e9198d`) | The project's planning document specified the conflict-lock feature as paid-only. The contract's escalation phase walked through the engineering cost (one int compare) and the failure mode it addresses (silent data overwrite), and the user reversed the planning decision: always-on, every tier. The contract surfaced a question the planning document had not asked, and the answer overrode the planning document. |
| **7** | **User intent disambiguation** | Batch operations (Ex. 06) | The user-facing task description was "bulk send invitations." The contract enumerated four candidate populations the phrase could refer to (never-invited, pending, expired, deleted-card-after-accept) and asked the user to choose. The user selected two of the four for this scope, with a separate single-flow planned for the fourth. Without the four-way enumeration, the agent would have shipped whichever subset its tokens-leaning predicted, and the user would have discovered the wrong subset after the change shipped. |
| **8** | **Knowledge-graph reuse across tasks** | Audit log (Ex., commit `958e04b`) | The contract directly referenced a previously-logged decision (a typology of paywall strategies, see mechanism 9) instead of re-deriving the paywall posture from scratch. The escalation question "should this feature be Premium-only or always-on?" became a one-line lookup into the decision log rather than a fresh five-option enumeration. |
| **9** | **Emergent meta-pattern crystallization** | Paywall framework (decision log entry D-5) | Three earlier audits had each made an ad-hoc paywall decision (do-not-nag, actively-upsell, always-on hygiene). After the third audit, the implicit pattern was crystallized into a three-strategy framework with explicit conditions of use. Future Premium tasks now pick A / B / C from the framework instead of re-deriving from scratch — a methodology that improves with use. |

### 5.3 What these nine mechanisms add up to

Reading the mechanisms in sequence, a structural observation emerges:

- **Mechanisms 1–4** are the *direct* value the contract delivers in a single task: it forces a grep, it surfaces a cross-cutting helper, it carries forward a prior decision, it lets architecture be reasoned about before code.
- **Mechanism 5** is the *highest-leverage* moment: a contract escalation rerouted a multi-day mistake into a five-minute conversation. This single case alone justifies the discipline.
- **Mechanism 6** is *the contract overruling the planning document*. The plan said one thing; the contract surfaced a question the plan had not asked; the answer reversed the plan. A planning document is a checkpoint; the contract is an exception-raising mechanism that can override it.
- **Mechanisms 7, 8, and 9** are *compounding effects*: as more contracts accumulate, the decision log accumulates, and future contracts reuse rather than re-derive. The methodology is not a flat overhead; it has a positive feedback loop.

We do not claim the methodology is statistically validated. We claim that across nine production scenarios, nine distinct kinds of value were observable, each documented with original contract text, implementation diff, and audit text — and that the cost of the methodology (~5–20 minutes of contract writing per non-trivial task) was, in each case, recovered many times over by the specific mechanism the contract triggered.

### 5.4 What the methodology did not catch

Equally important — what fell through:

- **Every audit closed with "code-level PASS, observation-level UNVERIFIED-IN-STAGING."** The contract closed the loop between intent and code, but not between code and observable production behaviour. Closing that second loop requires staging discipline that the methodology does not itself provide.
- **Self-evaluation bias:** the trial author, implementer, and reviewer were the same human-AI pair. The MUTATED reasons in each audit are honest, but they are not independent. Replication studies are needed to test whether contracts written by Team A and audited by Team B produce the same quality of insight.

These two limitations are revisited in §9.

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

- **Single-codebase observation.** All nine documented mechanisms were observed on a single multi-tenant SaaS application. The mechanisms are described and individually traceable through the artifacts in `examples/`, but independent replication on additional codebases — different domains, different team compositions, different AI agent stacks — is the most valuable next step for the methodology, and the one we cannot perform alone.
- **The methodology is phenomenological, not statistical.** This article does not claim a measured reduction in hallucination rate or in iteration count. It claims that nine distinct kinds of value were observable across nine scenarios, each with auditable artifacts. Readers who require a statistically powered control study should treat this article as motivation for one, not as one.
- **No matched-pair control.** We did not run the same nine scenarios without contracts. We mitigate the absence of a control by documenting each mechanism specifically: scenario 5 (direction correction) in particular describes a `v1` design the user rejected at the contract stage that, in our judgement, would not have surfaced from an unstructured prompt — the contract artifact itself is the evidence.
- **Self-evaluation bias.** The trial author, implementer, and reviewer were the same human-AI pair. The `MUTATED` reasons in each audit are honest but not independent. We treat this as a fundamental limitation that only external replication can resolve.
- **Single-agent observation.** All nine scenarios were executed by a single AI coding agent in conversation with a single human decision-maker. AI-to-AI claims in Section 6 are structural extrapolation, not measurement.
- **Observation-level verification is incomplete.** Every audit in the trial closes with "code-level PASS, observation-level UNVERIFIED-IN-STAGING." The methodology closes the loop between intent and code, but not between code and observed production behaviour. Closing that second loop requires staging discipline that the methodology does not itself provide; we record the gap explicitly in every contract's `Overall` summary.
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
