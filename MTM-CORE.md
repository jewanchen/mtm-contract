# MTM 2.5 — CORE

> **MTM = machine to machine.** A contract is a *handoff format* — today usually written by a person for an agent, and by design between agents as well. The encoding changes; the fields do not.

> **One lifecycle, one specification.** This replaces the older mental model of three separate documents (Contract / Arch / Verify) — they were always three phases of the same pipeline.
> Built for agentic AI coding, against two recurring failures: **hallucination** (calling an API or entity that does not exist) and **architectural drift** (a decision made at step 3 silently contradicted at step 15).
> Since v0.2 MTM is **self-hosting**: it evolves from case experience plus human decision, using its own revisit mechanism (see [`EVOLUTION.md`](./EVOLUTION.md)).

> Trigger phrase: *"do ___ with MTM"*. Fast paths are active throughout — any phase whose condition is met passes in seconds. There is no ceremony tax.

> **This file is the entry point — the spine.** The other documents are phase-level detail: [`MTM-Verify.md`](./MTM-Verify.md) and [`MTM-VERIFY-REPORT-TEMPLATE.md`](./MTM-VERIFY-REPORT-TEMPLATE.md) for phase 6 (independent audit). Read CORE first; open a detail file only when you need that phase expanded.
> 繁體中文版：[`MTM-CORE.zh-TW.md`](./MTM-CORE.zh-TW.md) · Reasoning and evidence: [the 2.0 article](./mtm-contract-2.0-article.md) · One page to start with: [`MTM-LITE.md`](./MTM-LITE.md)

---

## 1. Core invariants

1. **Every field gets an answer. `N/A` is legitimate. "I don't know" is written `UNKNOWN: <why>`. Blank is not an answer.**
2. **Any ungrounded load-bearing assertion must be escalated.** The same anti-hallucination mechanism applies at task level (the `verified_by` field) and at architecture level (grounding against the project's architecture record).
3. **Keep the machinery internal.** Show the person only: what you are doing, why, roughly how long, and what you need from them. Internal labels (confidence, `DIVERGENT`, `ARCH_VIOLATED`, …) are always translated into their language.
4. **An externalised artifact beats session memory.** The contract lives in a file and the audit runs against that file — never against a recollection of the conversation.
5. **Changing direction during escalation costs almost nothing; changing direction during implementation costs a rollback.** Push judgement earlier.
6. **Verification means execution, not declaration (v0.3).** `verified_by` and `observed_result` must point at something actually run *this session* — a search result, command output, a test or build log, an observed value. **Never mark a clause `PASS` while its evidence is a promise.** Anything not actually run is marked `UNVERIFIED` and carried into the phase 6 audit as an open item.
   - Why: with a capable model the failure is not a blank field. It is a field filled convincingly while the underlying check was never done. A plausible-looking value and a genuinely closed one look identical on the page — this rule makes them look different.
7. **The customer's stated core need comes first (v0.5 · #13).** The core experience the person named *literally* — the reason the tool exists at all (a bass app's "real bass tone", a camera app's "sharp pictures") — is a **first-class deliverable** and may not be downgraded to a placeholder or a TODO.
   - When a real solution is readily available (a free sample library, an existing API), **ship the real thing by default**; do not put a placeholder in front of it.
   - If it genuinely must be deferred, say so at confirmation as **the headline "not yet possible"** item. Never a silent TODO.
   - Relationship to #11: "cheap things can wait" applies only to *secondary* features. **A named core experience never waits.**
   - Warning sign (an altitude error): the architecture is handled well, and the thing the user came for is a placeholder. Correct structure, wrong delivery.
   - Evidence: a controlled A/B comparison — the build without MTM wired up a real instrument sound on the spot, the MTM-guided build shipped a synthesised placeholder, and lost on the user's literal core need.
8. **Held context is not surrendered (v2.1 · #18).** Do not discard what you have already established. When a confident external input — an independent review's findings, a CI failure, a linter, a subagent's report, documentation, another model's opinion — contradicts a **prior decision**, you must **retrieve and state the original reason before acting on that input**. If there is no reason, say so plainly: that it was an oversight rather than a decision is itself information.
   - **Paired with invariant 6.** Six says *do not claim what you did not check*; eight says *do not discard what you did establish*. Both are failures to use the evidence in your hands, pointed in opposite directions. Write only one and the failure arrives from the other side.
   - **The reviewer is a witness, not a judge.** Its view is *deliberately* restricted — contract, decisions, diff — so it **cannot see intent**. Findings are input to judgement, not a verdict. Whoever holds the context owes it a judgement.
   - **One question is enough**: does this finding hit a **defect** or a **decision**? A defect you fix. **A decision is not yours to reverse — escalate it.** This is not a new principle; it is the existing "do not decide alone" rule applied where it had been missing. Phase 6 had been violating MTM's own escalation rule.
   - **Symmetric burden**: to *accept* a finding, say what would break. To *reject* one, point at the decision. "The reviewer said so" is not a reason, and neither is "I had my reasons".
   - **Self-test (extended in v2.4 · #20)**: if you cannot state the reason without inventing one, it was not a decision — it was an oversight. And **if you can state it, ask whether that reason was ever checked.** A reason that exists but rests on unclosed grounding **counts as an oversight, and the finding stands.** Rejecting a finding takes the decision *and the grounding that closed it* — not the decision alone.
     - Why this had to be added: checking only for the *presence* of a reason lets a decision built on a false premise pass — at which point invariant 8 **shields the very failure it was written to prevent**, while exposing false premises is the entire reason the review exists.
     - The cost is correctly shaped: when the decision was properly grounded this step is nearly free (you point at the same grounding). It is expensive only when it was not — which is exactly when it should be.
     - This is the boundary between invariants 6 and 8: six governs the moment a decision is *made*; eight governs the moment a decision is *cited against a finding*. Nothing had governed the latter.
   - **Upstream loop**: a finding that collides with an *unrecorded* decision is itself a signal — that decision was under-recorded. Once handled, write the reason into `grounding` or the decision record so the next reviewer can see it and the same finding is not raised twice.
   - **Why this gets more important, not less**: the stronger the model, the more structured, persuasive and hard to refute its review becomes — **the stronger the reviewer, the higher the cost of deference and the harder it is to resist.**
   - Evidence: an independent review reported a figure as "unsourced" — correctly, since it was not in the corpus the reviewer was given. The executor removed it on the spot. The figure *was* sourced, just not in those three inputs. Reading "I cannot see it" as "it does not exist" is surrendering held context. In the same batch, a deliberate editorial decision was treated as a defect and changed.

---

## 2. The lifecycle (0 → 6)

| # | Phase | Trigger | Output | Fast path |
|---|---|---|---|---|
| **0** | Classify | A request arrives | Blast-radius tier → how far down the pipeline this task goes; **a greenfield one-liner routes to the Plan branch** | Trivial → just do it, skip everything |
| **0-Plan** | Plan *(greenfield)* | No architecture record **and** the request is for a product rather than a change to something existing | The hard-to-reverse foundational choices elicited in plain language → written into the architecture record with `UNKNOWN` markers → handed to phase 1 (detail in [`MTM-Plan.md`](./MTM-Plan.md)) | Any fork the person has already decided passes individually |
| **0-Debug** | Debug *(symptom)* | A fix already failed once, **or** a value is wrong and the cause is not established | Four-field debug contract; scope stays `UNKNOWN` until preconditions close | Neither trigger fires → classify normally |
| **1** | Ground | Anything non-trivial | Architectural assertions grounded; gaps become questions, and the answers are filed | Everything already grounded → passes in seconds |
| **2** | Escalate | Anything undecided or optional | Agreement: chosen path, scope, decision-record name | No ambiguity → skipped |
| **3** | Contract | After phase 2 | One artifact (status header + the fields in §4) | Fully covered by an existing decision record → cite it |
| **4** | Implement | After phase 3 | Shipped code | — |
| **5** | Self-check | After phase 4 | Every clause marked `PASS` / `FAIL` / `MUTATED`, with `observed_result` filled | — |
| **6** | Verify | High blast radius: permissions, security, schema, release | A report from an auditor in an independent context (§6) | Low-risk work → may be omitted |

### Phase 0 · Classify

"Thorough" means *correctly routed*, not *everything every time*.

| Tier | Test | How far it runs |
|---|---|---|
| **T0 trivial** | Typo, copy, version bump, one file under ~20 lines, pure styling | No contract. Just do it. |
| **T1 local** | One module, none of the triggers below | **Minimum viable contract** — three load-bearing fields → 1 → 3 → 4 → 5 |
| **T2 structural** | Touches a domain or boundary, a cross-module contract, or a new persisted entity | Full contract + phase 1 filing + the phase 2 architectural conversation |
| **T3 critical** | Permissions or security, schema migration, release assets, multi-tenant visibility | Full contract + all seven phases, **phase 6 independent Verify is mandatory** |

**Tiering runs off observable triggers, not the agent's own sense of risk (v0.3 · #10).** Any hit promotes the task and the agent **may not rationalise it away**:

> Does it touch auth, permissions, or secrets? · Is there a database migration or schema change? · Does it span two or more domains? · Does it change more than *N* files (*N* is the project's to set)? · Does it touch multi-tenant visibility, payments, or release assets? · Does the literal request fail to map one-to-one onto the data model (see the phase 2 candidate set)?

> **T3 cannot be self-demoted.** The rule of thumb *"if the contract takes longer than the code, drop it"* is admissible only between T0 and T1 — never for T2 or T3.

**Minimum viable contract (v0.3 · #11)**: T1 writes three **load-bearing fields** only — `intent`, `escalation`/candidate set, `affected_layers`. This keeps friction near zero for the valuable 20%, so it never gets skipped along with everything else. The middle fields (`schema_assumptions`, `cross_module_contract`, `test_plan`, …) a capable model handles as a matter of course; T1 may omit them, T2 and T3 fill them in.

### Phase 0-Debug · The symptom branch (v2.2 · #17)

**Why it exists**: the tier table keys entirely off **known scope** — auth or not, migration or not, how many domains, how many files. But **a bug's scope is unknown; that is what makes it a bug.** When a symptom arrives, "what will this touch" is the thing to be discovered, not an input to classification. The table cannot route it.

**Triggers (observable, either one is enough — so that not every bug takes on ceremony)**: ① a fix has already been attempted once and did not work; ② the symptom is *a value is wrong* and the cause is not established. Neither fires → classify normally as T0/T1.

**The minimum debug contract — four fields only**: `symptom` (observable) · `prior_guesses` (**each with its result**, which is what stops the circling) · `preconditions` (each with an *executable* check) · `evidence_source` (decided **before** the hypothesis). Mark `affected_layers: UNKNOWN until the preconditions close`.

**One hard rule**: **when round one does not fix it, stop changing code.** Establish one fact first. Consecutive guesses leave residue that makes later rounds worse than earlier ones.

**On closure**: once the cause is established, return to phase 0 and classify normally with the scope you now have. Most bug fixes land at T1; a few jump to T3.

### Phase 0-Plan · The greenfield branch (v0.4 · detail in [`MTM-Plan.md`](./MTM-Plan.md))

**Triggers (two observable signals)**: there is no architecture record and no source tree, **and** the request is for a product to be built rather than a scope change to something that exists. Whether the person is technical is not a separate gate — any fork they have already decided passes individually.

**What it does**: **open with one open-ended question about purpose** — *"what are you most hoping this does for you?"* — to fix the direction and the soul of the work (this feeds invariant 7). This is the **only** open-ended question asked by default (v0.7 · #15, greenfield only; do not volunteer additional features). The answer is wired into the handoff as a purpose note, decides which forks matter enough to ask about, and marks which feature invariant 7 protects. If the answer is circular, fall through to the forks rather than interrogating.

**The purpose also checks the request itself (v2.3 · #19)**: when what is asked for **plainly contradicts** the goal just stated, put the contradiction to the person — do not build it and do not silently redesign it. Keep the bar at *plainly contradicts* (widening it produces an agent that interrogates every request, which is the cry-wolf failure in teleological form), and **the output is a question, never a refusal**.

Then lay out the **hard-to-reverse** foundations: device capability and platform · persistence and cross-device · standalone versus integrated · single user versus multi-user · tenant isolation · regulatory regime and residency. Cheap choices get a sensible default, collected in a visible "here's what I assumed" block. Hard-to-reverse choices are put as *"imagine A versus B — which are you?"*, never as *"is that right?"* Four never get a silent default: **persistence across devices · multiple people logging in · who can see whose data · anything touching money or other people's personal information.** Confirm in capabilities — *"on day one you can X; you cannot yet Y"* — never with a skeleton.

**The boundary (Plan fork vs phase 2 candidate set)**: a Plan fork's answer determines **which domains and entities will exist** — it precedes and generates the data model. Phase 2 maps an intent onto a model that already exists. The test: *is there a data model to enumerate candidates from?* No → Plan. Yes → phase 2.

**Handoff (mandatory)**: Plan writes its conclusions in phase 1's vocabulary — invariants (irreversible forks as hard rules), domain notes, glossary, one seed decision record per fork that carried a trade-off, and an index. Every unresolved fork is written `UNKNOWN: <why>`. Phase 1 then fast-paths instead of re-asking. **Plan never decides a fork on its own; what it could not get an answer to is marked UNKNOWN, never guessed.**

### Phase 1 · Ground

Read the project's architecture record — index, invariants, glossary, domain notes, the most recent decisions. List the architectural assertions this request rests on. For each, ask: *which document, which section, supports this?* Any **ungrounded load-bearing assertion** — one that affects domain ownership, where a boundary sits, data ownership, whether an invariant applies, or how the project's own words map onto the model — becomes a question. At most three per round, each with one line on why it matters. File the answers as soon as they arrive.

**Where an answer goes.** File by what kind of statement it is, not by which feature prompted it:

| What they told you | Where it belongs |
|---|---|
| A hard rule that holds regardless of feature ("always true") | `invariants.md` |
| A domain's responsibilities, boundary, or composition | `domains/<domain>.md` |
| A distinction between two terms, or a definition | `glossary.md` |
| A relationship between domains | the index's domain-relationships section |
| A decision specific to this feature, carrying a trade-off | a decision record (phase 2) — **not** filed here |

If you are not sure where something belongs, **ask explicitly** — never file silently (§5, rule 3).

**A decision record can stop counting as grounding.** Every decision record carries a `revisit_trigger`: the condition under which it must be re-examined. When phase 6 finds that trigger has fired, the record is marked `needs_revisit`, and from that moment **the assertions resting on it are treated as ungrounded — even though the file still exists.** The next task in that domain re-opens the conversation instead of citing it.

> This is the missing half of invariant 8's self-test. #20 requires that a decision cited against a finding have *closed* grounding; `needs_revisit` is how grounding is declared closed no longer. **A stale decision record is worse than none, because it still reads like an answer.**

### Phase 2 · Escalate — a first-class phase, the highest return in the pipeline

1. **Candidate-set check (sub-protocol)**: does the literal wording of the intent map onto the data model? If not → **enumerate the candidate set and let the person choose. Do not translate literally.**
   > Evidence: "send the cards in bulk" turned out to address four distinct populations; a re-invite feature scoped from one situation turned out to need four. Literal translation builds something too narrow.
2. **The architectural dialogue** — required at T2/T3 when the task touches a domain boundary and is not fully covered by an existing decision record. **The order is fixed and may not be rearranged**; reverse it and you anchor to the structure that already exists, which is how the architectural thinking gets lost.

   - **Step 1 · Ideal.** In two or three plain paragraphs: *if this system had no history, how should this feature be designed?* **Do not cite any existing code, entity, or table name.** Use only the language of the domain — the person's words, the business roles. It must answer: which domain does this belong to? should the data stand alone or be shared? what is the access path? where is the boundary with other domains?
   - **Step 2 · Current.** Look at what exists, describe it in the same plain terms, and compare. Label it `ALIGNED` / `DIVERGENT` / `ABSENT`.
   - **Step 3 · Gap** (only when `DIVERGENT`). Which boundaries have already been crossed? Which domains have been conflated? What is currently papering over it — a flag, a toggle, a label, a runtime filter, something hidden in the UI? **Cite specific entities, endpoints, commits.**
   - **Step 4 · Options.** Now, and only now, the four below.

3. **Real options**: offer `PROCEED / REFACTOR_FIRST / SCOPE_SPLIT / ESCALATE`, each with its trade-off. The person chooses.
4. **Internal red-team pass (mandatory)**: privately ask *"if I were opposing this direction, what is the strongest case, and does it have substance?"* This step **may not be skipped** — it is what blocks sycophancy and false consensus.
5. **Disclosure is conditional**: surface it only if there is substance. If there is none, **do not manufacture a contrarian view.**
   > Why it is split this way: across the recorded trial, *zero* high-value events came from an objection the agent manufactured; all of them came from the agent laying out real options and the person reframing. Mandatory disclosure produces noise → cry-wolf → the one objection that mattered gets skipped as noise. So: **internally mandatory, externally conditional.**

Exit: the agent restates the agreement and names the decision record; the person confirms. T2 and T3 write that record to the project's decisions directory.

### Phase 4 · Implement — three disciplines

1. Never use a flag, toggle, or hidden field to work around a boundary the decision record declared.
2. If implementation reveals that the boundary must be crossed → **halt and return to phase 2.**
3. Any change outside `affected_layers` is reported *before* it is made. No silent patches.

### Phase 5 · Self-check — cheap, inline

Mark every clause `PASS` / `FAIL` / `MUTATED` **and fill `observed_result`** — not "done", but *what was actually observed*: a log line, a screenshot, a breadcrumb, a query count. `MUTATED` is legitimate; add one line saying why.

**Execution binding (v0.3 · #9, hard rule)**: a clause **may not be marked `PASS` while its `observed_result` is a promise or `PENDING`**. Either paste evidence produced this session, or mark it `UNVERIFIED` and carry it into the phase 6 audit as an open item. `PENDING` is a waypoint, not a pass.

### Phase 6 · Verify — an independent context; this is a gate, not a self-assessment

**A clean agent is required** (a subagent, or a new session), fed exactly three things: the contract, the decision records, the diff. It must not be a continuation of the executor's conversation — otherwise the auditor inherits the executor's rationalisation, and the audit is theatre. Output is the §6 report. `ARCH_VIOLATED` — it works but contradicts an agreed decision — is the single most severe verdict, and requires either a rollback or an immediate amendment to the decision.

**The architectural pass — four questions.** Beyond the ten failure modes, compare what shipped against the decision records. Each gets yes/no and one line:

1. Does the implementation violate the record's `decision`?
2. Has it triggered the record's `revisit_trigger`?
3. Has it produced an architectural consequence the record did not anticipate?
4. Has it produced a new architectural learning that needs a new record, or an amendment to an existing one?

Question 1 yes → `ARCH_VIOLATED`. Question 2 yes → **mark that record `needs_revisit`; from then on its assertions stop counting as grounding** (phase 1). Question 4 yes → open a follow-up to write or amend the record. These are not optional extras — they are how a decision record stays true instead of becoming decoration.

**After the findings arrive (v2.1 · #18, hard rule)**: the auditor is a **witness, not a judge** — its view was deliberately restricted, so it **cannot see intent**. The executor holds the context and therefore owes a judgement. Take each finding and ask: **defect, or decision?** A defect is fixed. **A decision is not the executor's to reverse — it is escalated** (the same "do not decide alone" rule as phase 2). Accepting takes saying what would break; rejecting takes pointing at **the decision *and* the grounding that closed it**. A reason that cannot be stated is an oversight, and **a reason that was never checked counts as one too** (v2.4 · #20). Afterwards, write the reason back into `grounding` or the decision record so the next review can see it. See invariant 8.

---

## 3. The single-artifact principle

One contract grows from phase 1 through phase 6, and **its `status` header is the single source of truth throughout**. When an agent resumes — after a context summary, or in a new session — it reads the status first and knows where things are, what is blocked, and which preconditions are still open. This is aimed directly at MTM's original motivation: drift across steps.

---

## 4. The canonical template

```markdown
# MTM Contract: <task, in one line>

## status
stage= | blast_radius=T0/T1/T2/T3 | blocked_on=[] |
unverified_preconditions=[] | open_escalations=[]

## intent
<One sentence, verb first, observable. Not "implement X" — "the user
 does X and sees Y".>

## affected_layers
<Layer by layer, what changes and what deliberately does not:
 entity / service / endpoint / migration / scheduled work / client
 state / screens / cache / admin surfaces / env and secrets>

## preconditions
- <condition>   verified_by: <commit / migration / manual test / health check / ...>
  (any unverified precondition closes before implementation starts)

## schema_assumptions
- <assumption>   source: <spec section / entity comment / commit / prior task>
  (no source → confidence drops one level)

## cross_module_contract
emit / listen / what I assume others do / what others depend on me for

## expected_outcome
- <observable result>
  verifiable_by: <how it will be checked: manual step / test / log / breadcrumb>
  observed_result: <evidence actually produced this session | not yet
   checked = PENDING (may not be marked PASS) | cannot be checked =
   UNVERIFIED (carried into the audit)>          ← v0.3 execution binding

## confidence
overall: high / medium / low ; low-confidence sub-items: <item + why + plan>

## architectural_basis          ← T2/T3 only
decision_record: <YYYY-MM-DD_<domain>_<desc>.md>
summary: <one line: where this task sits relative to that decision,
 and which boundary it must not cross>
<Purpose: reload the architectural decision into the task's context, so
 that the agreement reached in phase 2 is not forgotten at step 15.>

## escalation
Awaiting the human: <enumerate; do not decide these>
Stop and report: <enumerate; do not force a solution>
Standing rules — **these may not be removed**:
 - if implementation reveals a declared boundary must be crossed → halt, return to phase 2
 - if implementation trips a decision record's `revisit_trigger` → halt and report

## grounding
<spec / architecture / decision record / commit / verbatim conversation>
(nothing to cite → mark SPECULATIVE)

## rollback_plan
code / schema / env

## test_plan
local / staging / production
```

> `verified_by` (premises), `verifiable_by` → `observed_result` (results), and `source` (assumptions) are the actual substance of "precise execution and detailed verification". The v0.1 public template buried them as details; v0.2 brought them to the front.

### 4b. The decision-record template

Written at T2/T3, one per decision that carried a trade-off, to `decisions/YYYY-MM-DD_<domain>_<short-desc>.md`. Phase 6 reads these; if they do not exist, the audit has nothing to check the code against.

```markdown
# Decision: <short description>

> Date: YYYY-MM-DD · Domain: <domain>
> Triggered by: <the request, in one line>
> Confidence at the time: high / medium / low

## context
<what need this decision answers>

## ideal_state
<phase 2, step 1 — how it should look with no history>

## current_state
<phase 2, step 2 — ALIGNED / DIVERGENT / ABSENT, and the description>

## gap
<phase 2, step 3; N/A if aligned>

## decision
<the path chosen, and why>

## consequences
<how this constrains other features and other domains from now on>

## revisit_trigger
<what would make this decision wrong — be concrete>
- e.g. "when there are more than three admin roles"
- e.g. "when a feature needs to query across domains"

## referenced_by
<task contracts append themselves here when they cite this>
```

> `revisit_trigger` is the load-bearing field. Without it a decision record cannot expire, and phase 1 has no way to know its grounding has gone stale (see phase 1, and invariant 8's self-test).

---

## 5. Conversation discipline (across all phases)

1. Open by inviting a conversation, not by announcing a process. Never say a phase number to the person.
2. Translate every internal label into their language (confidence, `DIVERGENT`, `REFACTOR_FIRST`, `ARCH_VIOLATED`, …).
3. File in one consolidated pass rather than asking item by item. If you are unsure where something belongs, ask explicitly — never file silently.
4. On a phase transition, give a short summary and stop for the person. (Fast-pathed phases need no pause.)
5. **Forced disagreement → internally mandatory, externally conditional** (phase 2, steps 3–4).
6. Surface only the part of the phase 6 result that is actionable for them. Do not dump the full pass/fail list.

**Translating the internal labels.** These are judgements, not vocabulary to hand over:

| Internal | What you actually say |
|---|---|
| `confidence: high` | "I'm confident about this one — I can go ahead." |
| `confidence: medium` | "I'd like to check a couple of things with you first, about five minutes." |
| `confidence: low` | "There's a structural problem to deal with before this; it'll take a bit longer." |
| `DIVERGENT` | "The way it works now and the clean way have drifted apart — the difference is ___." |
| `REFACTOR_FIRST` | "I'd suggest tidying ___ before we add this." |
| ungrounded assertion | "There are a few things I'm not sure about — can I check them with you?" |
| `ARCH_VIOLATED` | "It's built, but it doesn't hold to what we decided last time — ___. Roll back, or amend the decision?" |

> Meta-principle, and the fallback when these conflict: **keep the machinery internal; show only what, why, how long, and what you need from them.**

---

## 6. The Contract ↔ Verify spine — ten failure modes and the field that should stop each

Verify is not a separate checklist. It is a check of whether each preventive field actually held.

| # | Vibe-coding failure | The contract field that should have stopped it |
|---|---|---|
| 1 | Interface that does not line up; payload mismatch | `cross_module_contract` (emit ↔ listen) |
| 2 | Collateral damage — edits outside the declared scope | the `affected_layers` boundary |
| 3 | Undefined edge conditions | `expected_outcome` + `schema_assumptions` |
| 4 | Logic gap left by a refactor | `test_plan` + phase 5 `observed_result` |
| 5 | Happy-path bias — no 500, timeout, permission denial, or empty state | `expected_outcome` (negative paths) |
| 6 | Leftover mock or TODO presented as done | phase 5 scan |
| 7 | Environment or dependency drift | `affected_layers` (env and secrets) |
| 8 | Missing authorisation | `preconditions` (authentication, ownership) + the T3 gate |
| 9 | Performance landmine (N+1) | `schema_assumptions` + `expected_outcome.verifiable_by` (query count) |
| 10 | Silently deleted tests | `test_plan` + diff scan |

> Auditor conduct: ruthless but objective (cite file and line, no apologies); does not fix (report only, leave the fix to the executor or the human); architectural consistency outranks everything (`ARCH_VIOLATED`). The report template is [`MTM-VERIFY-REPORT-TEMPLATE.md`](./MTM-VERIFY-REPORT-TEMPLATE.md); each of its sections names which of the modes above it covers.

---

## 7. Known risks in this method, and what holds them down

Every one of these has happened. They are listed because a discipline that cannot name its own failure modes is asking to be trusted on faith.

| Risk | What holds it down |
|---|---|
| **Grounding questions exhaust the person** during the first few tasks | Three per round, each with why it matters. This is a one-time cost: after three to five tasks the record is populated and phase 1 fast-paths. |
| **The architectural dialogue becomes theatre** — the agent performs "I understand architecture" while pattern-matching | The fixed 1 → 2 → 3 → 4 order, and step 1 may not cite existing code. |
| **Decision records nobody reads** — written once, then decoration | Phase 6 compares against them, every time. Semi-annually: any record not cited in six months is either a stable domain (fine) or written too abstractly (rewrite it). |
| **False consensus** — the agent agrees to end the conversation | The internal red-team pass is mandatory, and disclosure is conditional so it does not become noise (phase 2). |
| **Optimistic tiering** — the agent reports low risk to reach a fast path | Tiers run off observable triggers, not judgement; T3 cannot be self-demoted. |
| **Silent misfiling** — filing an answer in the wrong place when the rule is ambiguous | When unsure, ask explicitly. Never file silently (phase 1, §5 rule 3). |
| **A gate that never fires** — a rule called mandatory that nothing enforces | §7's second half: either it has a check that demonstrably fires, or it is honestly a recommendation. |

---

## 8. Evolution (self-hosting)

MTM is not a frozen specification — it grows. The engine is in [`EVOLUTION.md`](./EVOLUTION.md), and it is a four-stage loop:

1. **Case ledger (hard gate · v0.6 #14)**: every non-T0 task **appends one line before it counts as done** — no line, not finished. (Same logic as phase 5's execution binding: soft discipline leaks, so bind it to a gate.) Record: first attempt clean? hallucination events? which field caught or missed what? what the escalation was worth? Where the ledger lives is the consuming project's choice.
2. **Proposal queue**: when a pattern recurs, or a person or auditor identifies a gap in the specification itself, it becomes a proposal — **status: pending-signoff**.
3. **Discussion gate**: proposals **do not take effect on their own.** A rule is promoted into CORE only after a human agrees. The gate on evolution is a person, not the AI.
4. **Changelog and version bump**: on promotion, record the change and move the version.

**A rule is only hard if something mechanically enforces it (v2.2 · #16).** Writing "mandatory" into a specification does not make it mandatory. #14 promoted the ledger from soft discipline to a hard gate — and a month later ten consecutive qualifying tasks shipped without a line. The rule was in the specification the whole time. Therefore: **a hard gate with no mechanical enforcement point is still soft discipline.**

> There is a second half, and it matters more: **the enforcement point must be tested against the layout your own documentation teaches.** Evidence: this project's bundled validator only fired when `PASS` and `observed_result` were on the same line — while its own template puts them on separate lines by design. A critical-tier contract with every clause `PASS` and every piece of evidence still a promise passed cleanly. **A gate that silently passes costs more trust than no gate**, because it launders unverified work into something that looks audited.
> In practice: a rule claiming to be mandatory either gets a check that **demonstrably fires** (CI, a script, a tool), or it is honestly downgraded to a recommendation in the specification. There is no honest third state.

This is MTM's own revisit mechanism turned on itself: the methodology is governed by its own discipline.

---

*MTM 2.5 — one unified lifecycle (CORE as the spine; the older documents and [`MTM-Plan.md`](./MTM-Plan.md) retained as phase-level detail) plus a self-hosting evolution engine. Public explanation: [the 2.0 article](./mtm-contract-2.0-article.md) (繁體中文：[`.zh-TW`](./mtm-contract-2.0-article.zh-TW.md)).*

***Version lineage**: 2.5 = 2.4 + the mechanisms absorbed from MTM-Arch (the architectural dialogue, the decision-record template, `architectural_basis`, `needs_revisit`, the four architectural audit questions, the label translations, the known-risks table) · 2.4 = 2.3 + the self-test extended to "was that reason ever checked" (#20, reported from outside use) · 2.3 = 2.2 + the purpose checking the request itself (#19) · 2.2 = 2.1 + the debug branch (#17) and enforcement points for hard gates (#16) · 2.1 = 2.0 + invariant 8 · 2.0 = the former v0.7, renamed when the specification line merged into the public article line (reasoning in [`EVOLUTION.md`](./EVOLUTION.md) §C). The `v0.x · #N` markers beside individual rules record **the version each rule was promoted in**, not the current version; they are kept as changelog references.*

*Proposals that produced 2.0: #1–#7 (the unified lifecycle and its parts) · #9–#11 (execution binding, observable triggers, the minimum viable contract) · #12 (the greenfield Plan branch) · #13 (the customer's core need, invariant 7, derived from a controlled A/B comparison) · #14 (the case-ledger hard gate) · #15 (asking purpose first in greenfield) · #18 (invariant 8, v2.1) · #16 and #17 (v2.2) · #19 (v2.3) · #20 (v2.4). **#8 is closed.***
