# MTM Contract 2.0 — Put the Cheap Checks Before the Expensive Generation

**An ordering discipline for building software products with AI agents.**
Fewer wrong turns, less rework, more of the work correct on the first pass, and less spend on re-deriving what you had already decided.

---

**Published:** July 30, 2026
**Author:** Vast Intelligence Limited
**The name:** MTM is *machine to machine*. A contract is a handoff format — today usually written by a person for an agent, and by design between agents as well. The encoding changes; the fields do not.
**Specification version:** 2.0 — one lifecycle, a greenfield branch, and an evolution engine. Reference implementation: [`MTM-CORE.md`](./MTM-CORE.md) (currently in Traditional Chinese; English readers start with [`MTM-LITE.md`](./MTM-LITE.md))
**Repository:** github.com/jewanchen/mtm-contract
**License:** Apache 2.0 ([`LICENSE`](./LICENSE)), attribution required ([`NOTICE`](./NOTICE))
**繁體中文版本：** [`mtm-contract-2.0-article.zh-TW.md`](./mtm-contract-2.0-article.zh-TW.md)
**Prior work:** the [first article](./mtm-contract-technical-article.md) (May 2026) introduced the eleven-field contract. This one presents the 2.0 architecture and the reasoning behind it. You do not need to have read it.

> **Evidence base.** Everything described here was developed while shipping one commercial product: mobile clients, a backend service, and two web consoles, with AI agents doing most of the implementation. About a hundred contracts over eleven weeks, plus one controlled comparison on a separate greenfield build. The limits of that evidence are in §13, not buried.

---

## 0. The claim

If you build products with AI agents, your throughput is not limited by how fast the agent writes code. It is limited by how often the agent writes the *wrong* code — and by how much of your budget goes into discovering that, undoing it, and re-establishing what you had already worked out.

MTM Contract is a discipline that reorders the work. One sentence:

> **Move the cheap checks in front of the expensive generation.**

Ordering is the spine, but it does not act alone. Two other properties carry weight and are named where they appear: the artifact lives in a file rather than in the conversation (§2), and a *claimed* check is never accepted as a *performed* one (§6.4). Four things follow from the three together. Each has a mechanism, and each has a boundary where it stops being true:

| What you get | The mechanism that produces it | Where it does not hold |
|---|---|---|
| **Higher throughput** | Ambiguity is resolved while it is still a sentence, not after it is a diff. Direction changes during a five-minute conversation instead of a rollback. | On work small enough that the whole change is smaller than its own description. The routing rules in §5 exist to keep you from paying here. |
| **Fewer wrong turns** | Before implementation, the agent must enumerate what it is assuming and how each assumption was checked. Assumptions that cannot cite a check are the first thing you look at. | It reduces wrong turns; it does not eliminate them. §11 lists the ones that got through anyway. |
| **More correct on the first pass** | Every claimed outcome has to be tied to something observed, not something promised. A separate reader, with no memory of writing the code, checks the result against the plan before it counts as done. | The audit is a fresh context, not an independent team. §9 states that limit plainly. |
| **Less total spend** | Wrong turns are the expensive part, and re-deriving context is the silent part. A short written artifact is read; a conversation is reconstructed. | We measured retries, rebuilds, and guess rounds — not token counts. No multiplier is claimed anywhere in this article. §13. |

The rest of this article is: where the waste actually is (§1), the ordering fix (§2), the architecture that implements it (§3–§5), why it is shaped that way (§6), one task from start to finish (§7), and then the honest parts — what it does not do, what it costs, and what the evidence does and does not support.

---

## 1. Where the waste actually is

The first generation is not the expensive part. Watch a day of agent-assisted work and the cost concentrates in five places, none of which is "the model wasn't smart enough."

**1. Generation before discovery.** The agent writes an implementation, and only while writing it discovers the shape of the thing it is working on: that a field is nullable, that a helper already exists, that the endpoint returns a different envelope than assumed. Discovery is not the problem. Discovery *after* generation is, because it invalidates work that already exists. The same lookup performed sixty seconds earlier would have cost a search and changed nothing else.

**2. Unverified premises fan out.** A single unchecked assumption at the start does not stay one mistake. It shapes the data model, then the endpoint, then the client, then the tests written to confirm it. When it finally fails, the cost is not the assumption; it is everything downstream that was built to be consistent with it. Cheap to check at step one, expensive to unwind at step ten.

**3. Re-derivation.** Decisions that live only in the conversation have to be paid for again. After a long session, a context summary, or a handoff to a new session, the agent reconstructs where things stand by re-reading source and re-inferring intent — and sometimes reconstructs it slightly differently, which is how work from step three ends up contradicted at step fifteen. Anything you decided and did not write down, you will buy twice.

**4. The guess loop.** A symptom appears. The agent forms a plausible hypothesis, changes code, rebuilds, and tries again. Round two starts from round one's residue, so wrong assumptions accumulate and later rounds are worse than earlier ones. This is the most expensive pattern in agentic development and the easiest to fall into, because every individual round looks like progress.

One case from this period: a members list rendered email addresses where names belonged. Round after round of entirely plausible theories — the sign-in provider stopped returning a name, the client stopped sending it, existing accounts need backfilling — with rebuilds after each. What ended it was one search for that field across the service: a shared helper resolved the name with a fallback, and several other places built the same string inline without ever calling the helper. There was also a second apparent bug, a prompt that should have fired and didn't. It did not exist; the list was simply overwriting what it displayed.

**5. Declaration without execution.** This one is specific to capable models, and it is why the specification version moved. Strong agents rarely fail by leaving a field blank. They fail by filling it convincingly without doing the underlying work. A line reading `verified_by: searched the callers — no other call sites` looks exactly the same whether the search ran or not. Downstream work then rests on a claim rather than a fact, and the failure surfaces at the most expensive possible moment.

Two shapes of this from the same period. A feature merged, the pipeline reported success, and the running service kept serving the previous commit. The natural reading was "the deploy is slow." It wasn't: the process was crash-looping because a nullable column had been declared without an explicit type and the data layer could not infer one at startup. Type checking passed, the build passed, a dependency-injection smoke test passed; only starting the service against a real database reproduced it. In the second, a batch of response-header hardening was called done on a green pipeline — and asking the live service which commit it was running returned the old one.

Notice what all five have in common. None of them is a capability failure. They are **ordering failures**: the check that would have prevented each one was available, cheap, and performed too late or not at all.

---

## 2. The ordering fix

Take one non-trivial task and write out both orderings.

**The default ordering.** Describe the task → the agent generates → discovery happens during generation → regenerate → discovery happens again → ship → find out what you actually got. Every discovery lands *after* something depends on it, so each one costs unwinding as well as learning. The verification, if it happens, happens last — where it is most expensive and least likely to be done.

**The MTM ordering.**

1. State the outcome as something observable. Not "implement bulk resend," but "an administrator selects these people and each one receives exactly one new invitation."
2. List what must be true for that to work, and next to each, how you checked it. A search, a query, a request against the running service, a line in a log.
3. List the choices that are not yours to make, and stop. Ambiguous scope, product judgement, anything where two readings of the request lead to different software.
4. *Then* generate — once, against a written target.
5. Check each claimed outcome against something you actually observed, and mark honestly what you have not observed.
6. Have a reader with no memory of writing the code compare the plan to the diff before it counts as done.

Two things about this ordering matter more than the individual steps.

**The checks are cheap only because of where they sit.** A search, a schema query, one question to a human — each is trivial in isolation. Performed before anything depends on them, they cost almost nothing and frequently change the plan. Performed after generation, the identical checks are expensive, because now they invalidate work. The discipline is not "verify more." It is "verify earlier," which usually means verifying *less* in total.

**The artifact has to be a file.** Steps 1–3 produce something written down, outside the conversation, that the agent re-reads instead of reconstructing. A conversation is re-derived every time context is compacted; a short file is read. This is why the methodology ships as markdown rather than as tooling — see §6.1.

Everything else in this article is the machinery that makes this ordering practical rather than aspirational: how much of it to run for a given task, what exactly gets written down, and what stops the agent from writing "verified" when it verified nothing.

---

## 3. The architecture: one lifecycle

Version 2.0 collapses what used to be three separate documents into a single pipeline with a single artifact. Seven phases, of which most tasks run three or four.

| # | Phase | What happens | Output | Typical cost | Skipped when |
|---|---|---|---|---|---|
| **0** | **Classify** | Decide how much of the pipeline this task gets, from observable triggers rather than a feeling (§5) | A tier | Seconds | Never — but it routes most tasks to almost nothing |
| **0-P** | **Plan** *(greenfield only)* | No codebase yet: elicit the hard-to-reverse foundational choices in plain language (§8) | Seed architecture notes | One conversation | Any existing project |
| **1** | **Ground** | List the architectural assertions this task rests on; for each, name the document or code that supports it. Unsupported assertions get asked about, not assumed | Grounded assertions, or questions | Minutes | Everything already documented |
| **2** | **Escalate** | Enumerate candidate interpretations where the request does not map cleanly onto the data; lay out real options with trade-offs; let the human choose | Agreement, recorded | Minutes | Nothing is ambiguous |
| **3** | **Contract** | Write the artifact (§4) | One file | 15–30 minutes at the heaviest tier; three fields at the lightest | Fully covered by an existing decision record |
| **4** | **Implement** | Build it, inside the declared boundary | Shipped code | The actual work | — |
| **5** | **Self-check** | Mark each clause pass, fail, or mutated-with-reason, and record what was *observed* | Amended contract | Minutes | — |
| **6** | **Verify** | A reader in a clean context compares contract, decisions, and diff (§9) | Audit report | One pass | Low-risk work |

Three properties of the pipeline are worth naming, because they are what make it usable day to day.

**One artifact, from phase 1 to phase 6.** The same file grows through the task and carries a status header at the top: which stage, what it is blocked on, which preconditions are still unverified, which questions are still open. When a session is summarized or handed off, that header is the single place to look. This is the direct countermeasure to waste #3.

**Fast paths everywhere.** Every phase has a condition under which it takes seconds. A task whose assumptions are all already documented passes phase 1 immediately; a task with no ambiguity skips phase 2 entirely. The pipeline is designed to be mostly skipped — which only works if the skipping is decided by rule rather than by mood, hence §5.

**Implementation has three hard rules.** Do not use a flag, a toggle, or a hidden field to work around a boundary the contract declared. If you discover mid-implementation that you must cross that boundary, stop and go back to phase 2. If you change something outside the declared scope, say so before doing it. These exist because the most damaging drift is not a bad decision; it is a good decision quietly overridden later.

---

## 4. What you write down

The artifact is a markdown file. Its fields are not a form; they are three verification chains plus the context needed to make them meaningful.

**Chain 1 — premises.** `preconditions`, each with `verified_by`: the executable thing that established it. "The invitation acceptance path is idempotent — verified by reading it at this commit." Writing this line forces a search, a query, or an honest `UNKNOWN: what I would need to check`. This is where hallucinated APIs die.

**Chain 2 — results.** `expected_outcome`, each with `verifiable_by` (how it will be checked) and then `observed_result` (what was actually seen). The second half is the 2.0 addition, and it carries the rule that gives the whole method teeth:

> A clause may not be marked passing while its evidence is still a promise. Either record what you ran this session — command output, query result, log line, observed value — or mark it `UNVERIFIED` and carry it into the audit as an open item. "Pending" is a waypoint, not a pass.

Without that rule, a capable agent produces a document that is indistinguishable from diligence. With it, the two look different on the page.

**Chain 3 — assumptions.** `schema_assumptions`, each with `source`: where the belief about a data shape, default, or invariant comes from. No source means the assumption is marked speculative and reviewed first.

Around those three chains:

| Field | What it stops |
|---|---|
| `intent` | One observable sentence. Stops "done when I say it's done." |
| `affected_layers` | What changes *and what deliberately does not*. Stops collateral edits. |
| `cross_module_contract` | What this emits, listens to, assumes of others, and promises callers. Stops the silent interface break. |
| `confidence` | Overall, plus enumerated low-confidence sub-items. Gives uncertainty a legal place to live so the agent neither bluffs nor stalls. |
| `escalation` | What the agent must not decide alone, and what should halt it. Stops both the confident wrong answer and the silent stop. |
| `grounding` | Citations for the contract's own claims. Unsourced claims are labelled, not laundered. |
| `rollback_plan` | Code, schema, environment. Also forces thinking about ship order (§10.5). |
| `test_plan` | Local, staging, production. Pairs with phase 5 to make "it works" mean something. |
| `status` header | Stage, blocked-on, unverified preconditions, open questions. The resume point after any context loss. |

At the lightest tier you write three of these, not twelve. Which brings us to the part that decides whether the whole thing is an asset or a tax.

---

## 5. Routing: what gets the full treatment

A methodology that applies uniformly is a tax. The routing rules are the efficiency guarantee, and they are deliberately mechanical.

| Tier | What it looks like | What it gets |
|---|---|---|
| **Trivial** | Typo, copy change, version bump, one small file, pure styling | Nothing. Just do it. |
| **Local** | One module, none of the triggers below | Three load-bearing fields only: `intent`, `escalation`/candidate set, `affected_layers` |
| **Structural** | Touches a domain boundary, a cross-module contract, or a new persisted entity | Full contract, grounding, and the escalation conversation |
| **Critical** | Permissions, security, schema migration, release assets, multi-tenant visibility, money | Full contract plus a mandatory independent audit |

**The tier is decided by observable triggers, not by the agent's sense of risk.** Does it touch authentication, permissions, or secrets? Is there a schema change? Does it span more than one domain? More than *n* files, where you pick *n*? Does it touch tenant visibility, payments, or store assets? Does the literal request fail to map one-to-one onto the data model? Any hit promotes the task, and the agent is not allowed to argue its way back down. The critical tier cannot be self-demoted at all.

This looks like bureaucracy and is the opposite. Self-assessment is the one thing that cannot be trusted here, because the judgement being asked for — "is this risky enough to be careful about?" — is exactly the judgement that carefulness exists to backstop. Under deadline pressure it degrades precisely when it matters. A short list of observable triggers is both cheaper to apply and harder to rationalize around.

The rule of thumb still holds and is worth stating plainly: **if writing the contract takes longer than writing the code, you don't need a contract.** But note its scope — it is admissible only at the two lightest tiers. A schema migration does not become local because the contract felt long, and the specification says so explicitly: the critical tier cannot be self-demoted, and neither can the structural one on this argument. The tier table exists so that call is made by rule, once, rather than ad hoc every time you are in a hurry.

---

## 6. Why it is shaped this way

Five design decisions carry most of the weight. Each came from an observation, not a preference.

### 6.1 A file, not a tool

The methodology ships as markdown with no dependencies, and tooling is deliberately second. Two reasons. The first is that the artifact's job is to survive the agent's context: it has to be short enough to re-read, scannable enough to resume from, and plain enough that any tool or any model can consume it. A file does that; a database row or an IDE plugin does not, and a conversation certainly does not. The second is that locking a methodology into tooling before it stabilizes produces tooling debt that outweighs the adoption benefit. Enforcement is valuable — see §14 — but it belongs after the shape stops moving.

### 6.2 Escalation is a first-class phase

In practice, the single highest-value moment is not the contract, the audit, or any field. It is the point before implementation where the agent lays out what the request could mean and a human picks. Two recurring shapes:

- The literal request does not map one-to-one onto the data. "Resend invitations in bulk" turns out to address at least four different populations: never invited, invited but never accepted, expired, and accepted-then-removed. An agent that picks the statistically likeliest reading ships correct code aimed at the wrong target — the most expensive kind of mistake, because nothing is broken and everything is wrong.
- The design itself is up for reconsideration. In one case a first draft proposed copying recovered records into an individual's personal address book; the human, reading the plan before implementation, rejected the shape entirely in favour of a shared store. That conversation cost minutes. The same realization after implementation costs a migration.

So escalation is not a sub-rule inside contract writing. It is its own phase, with its own output, and it is the last phase where changing direction is free.

### 6.3 Internal challenge, conditional disclosure

An earlier version required the agent to surface a dissenting view on every task. That rule was removed, and the reason is instructive. Across the tasks where a challenge produced real value, **none came from an objection the agent manufactured.** They came from the agent laying out genuine options and the human reframing the problem. Mandatory disclosure produces noise; noise trains you to skip the section; and then the one time the objection is real, it gets skipped too.

The rule in 2.0 is asymmetric: internally, the agent must always run the challenge — "if I were arguing against this direction, what is the strongest case, and does it have substance?" Externally, it raises the objection only if the answer is yes. This keeps the check that catches agreeable-but-wrong behaviour without paying for a performance on every task.

### 6.4 Verification means execution, not declaration

Covered in §1.5 and §4. It is listed here as a design decision because it inverts an assumption in the first version of this methodology. That version assumed the failure was an agent that would not do the work. With capable models the failure is an agent that does not do the work *and reports otherwise* — not from dishonesty, but because producing a plausible verification sentence is a much easier task than performing the verification. The fix is not more fields. It is one rule that makes an unexecuted check look different on the page from an executed one.

### 6.5 The minimum has to be genuinely minimal

The eleven-field version was appropriate for high-risk work and too heavy for everything else. Heaviness has a specific failure mode: when the whole thing feels expensive, it gets skipped entirely — and what you lose is not the middle fields you would not have missed, but the two or three that carry almost all of the value. So the lightest tier is three fields, chosen for load-bearing capacity rather than completeness: what will be observably true when this is done, what am I not allowed to decide alone, and what am I touching. A capable agent handles most of the middle fields as a matter of course. Those three it will skip unless asked.

---

## 7. One task, end to end

Abstracted from a real task. The product context is removed; the shape is intact.

**The request.** "Add a per-user language preference so the backend can send messages in the user's language." One nullable column on a heavily-read table, a lookup table of message strings, and a header to read on incoming requests. It reads like an afternoon.

**Phase 0 — classify.** Schema change, more than one module, touches every read of the user table: critical tier. Full contract, mandatory independent audit. Note that no judgement was involved — a schema change alone was enough.

**Phase 1 — ground.** The assertions this rests on, each needing a source: message strings are currently produced in one place (they were not — they were produced in many); the push-notification path can carry a language (it could, at one point that had to be found); a default language exists somewhere authoritative (it did not — it had to be decided).

**Phase 2 — escalate.** Two questions that were not the agent's to answer: what happens for a user whose language is unknown, and whether unknown should mean the product's origin language or the international default. Both were decided by the human in under a minute. Recorded, because they will be asked again in three months.

**Phase 3 — contract.** Abbreviated:

```markdown
## status
stage=3 | tier=critical | blocked_on=[] | unverified_preconditions=[]

## intent
A user whose preference is set to their second language receives system
messages in that language; every existing user's behaviour is unchanged.

## affected_layers
entity: + one nullable column ·  service: message lookup, notification send
endpoint: read the request's language header ·  migration: yes
client: reports its language on sign-in ·  admin consoles: not touched

## preconditions
- Every read of the user table goes through the data layer's default
  selection   verified_by: searched all query builders at this commit
- The notification path can carry a per-recipient language
  verified_by: read the dispatch signature; it accepts a recipient object

## expected_outcome
- An existing user sees no change
  verifiable_by: compare produced strings before/after, byte for byte
  observed_result: PENDING
- A user with the preference set receives the second language
  verifiable_by: integration test asserting both languages
  observed_result: PENDING

## escalation
Decided by the human: default for unknown; whether unknown means origin
language or international default.

## rollback_plan
Column is nullable and excluded from default selection, so the code is
safe to ship before or after the migration. Reverting is a code revert.
```

**Phase 4 — implement.** Straightforward, because the ambiguity was gone before it started.

**Phase 5 — self-check.** Each clause marked; the byte-for-byte comparison run and recorded as an observation rather than a promise; the two outcomes that could not be observed until deployment left explicitly unverified.

**Phase 6 — audit.** This is where the task earned its cost. A reader in a clean context, given only the contract, the prior decisions, and the diff, raised the thing nobody in the implementing context had thought about: **ship order**. If the code deployed before the migration, the data layer would begin selecting a column that did not exist yet — and since it is the user table, every read would fail. Every login. Type checking, building, and startup tests all pass, because none of them query the production schema.

The interesting part is the fix that was chosen. Not "remember to run the migration first" — a procedure that depends on remembering — but excluding the column from default selection, which makes the dangerous order harmless. The audit also required a contract test pinning the unknown-language decision, so that reversing it later fails loudly instead of silently.

**What the process actually bought.** The ambiguity was priced at one minute instead of a rewrite. The ordering landmine was found by a reader who was not the author, before deployment rather than during an outage. And the fix moved from a procedure someone has to follow to a design in which the mistake cannot occur — which is the general form of the best outcome this method produces.

---

## 8. Starting from nothing

The pipeline above assumes a codebase. If you are starting from a sentence — "I want an app that does X" — there is a branch for that, because the failure mode is different: there is nothing to ground against, and the choices that matter most are the ones the person asking does not know they are making.

The branch has one opening question and then a short list of forks.

**Ask the purpose first.** Before any fork: what are you most hoping this does for you? This is the only open-ended question the process asks by default, and its answer does real work downstream — it names the experience that must not be quietly downgraded to a placeholder, and it determines which forks matter enough to ask about. If the answer is circular, do not press; fall through to the forks.

**Then only the choices that are expensive to reverse**, phrased as consequences rather than architecture. Not "do you want a backend database," but "when you get a new phone, should your work still be there, or is starting over fine?" Not "do you need multi-tenancy," but "should your partner be able to log in and see only their own part?" The forks that are cheap to change later — styling, naming, list versus cards, notification defaults — get a sensible default, collected in a visible "here's what I assumed" block rather than asked about.

**Four forks never get a silent default,** because guessing wrong means a rewrite, a privacy incident, or a legal problem: does the data persist across devices; do multiple people log in; who can see whose data; does it touch money or other people's personal information.

**Confirm in terms of capability, not structure.** Not an entity diagram — "on day one you will be able to do A, B, and C; you will not yet be able to do D or E." The exclusion list is what makes someone say *wait, my partner can't log in?*, which is exactly the sentence you want to hear before implementation rather than after.

The output is written as the architecture notes the main pipeline reads, with every unresolved fork explicitly marked unknown, so phase 1 fast-paths instead of asking the same questions again in developer vocabulary.

---

## 9. The gate that pays for itself

At the critical tier, one phase is mandatory: a reader in a clean context, given only the contract, the architectural decisions, and the diff, checking whether the plan and the result agree.

Not the author. Not a continuation of the conversation that produced the code. The reason is not honesty; it is that the reasoning which produced a gap is the same reasoning that would review it. Someone who just spent an hour building something has a working model in which it is correct, and reviewing from inside that model finds spelling mistakes.

What this actually catches, from four consecutive high-risk batches in one week — every one of which had passed static analysis, unit tests, and self-review, and every one of which came back as *do not ship*:

- The backend was complete and the client entry point had never been wired to it. Working code, unreachable feature.
- A layout crashed at runtime. The reviewer reproduced it with a test the author had never written; static analysis cannot see it.
- "Clear the deadline" silently did nothing, because omitting the field and sending it as null were indistinguishable to the endpoint.
- A new notification type was missing from a whitelist — the second time that same omission had occurred, which is how it became a standing checklist item.

Two disciplines make the audit useful rather than decorative. It reports and does not fix, so findings go back to whoever owns the work instead of being quietly patched by the reviewer. And its most severe verdict is not "this is broken" but **"this works and violates the design that was agreed"** — because code that works while contradicting a recorded decision is the failure that compounds.

**The honest bound:** this independence is context-level, not organizational. A fresh agent context with no memory of the implementation is demonstrably good at finding gaps the author cannot see. It is not a second team, and it is not immune to the blind spots of the model family it belongs to.

---

## 10. Seven situations where it pays

Recurring shapes, in the form you actually encounter them. Three in full, four in brief.

### 10.1 The value on the screen is wrong

Something displays the wrong thing. Nothing crashed, nothing logged. The tempting move is to reason about the data flow, and the reasoning is plausible every round — which is why it can absorb an entire afternoon (see §1.4).

The rule that replaces the reasoning: **for a wrong-value bug, the first action is to enumerate every place that value is produced, and read all of them.** Not one hypothesis, all producers. Two corollaries earned the hard way: adding a fallback to a shared helper does not fix the copies that never call it; and when you see a helper with a fallback, assume inline duplicates exist until you have looked. A related trap is that one wrong value can masquerade as a second, unrelated bug.

*Honest note: this case has no contract. It is the one where the discipline was skipped round after round, and the search happened only after someone insisted. A methodology's failure to be followed is a real failure mode, and this is what it costs.*

### 10.2 Everything compiled and the types still didn't match

A join returns nothing for records that visibly exist. Three consecutive hypotheses — a stale cache, the wrong identity, the data layer inferring a column type incorrectly — each produced a change, a rebuild, and no information. The answer came from one query against the database's own catalogue of columns: the two sides of the join were different types. No amount of application-layer reasoning would have surfaced it, because every layer above the database was internally consistent.

The field is `preconditions` with `verified_by`, but the discipline is smaller than the field: **when round one does not fix it, stop changing code.** Establish one fact first. Consecutive guesses do not just waste their own cost; they leave residue that makes later rounds worse.

### 10.3 What the request says isn't what the data means

The request is one sentence and reads unambiguous. The data model says it addresses four different populations. Whatever the agent picks, the code will be correct and aimed at the wrong target, and you will find out after it exists.

The move is to enumerate the candidate set in writing and have the human choose — before implementation, when the enumeration is the whole cost. This is §6.2, and it is the single highest-value habit in the entire method. If you adopt one thing from this article, adopt this one.

### 10.4 The pipeline was green and the change wasn't live

Covered in §1.5. A green build is a prediction, not an observation. The cheap countermeasures: for a new persisted entity, start the service against a real database before calling it done; for anything deployed, ask the running service what commit it is on.

### 10.5 The change is fine; the order you ship it in is not

Covered in §7. The general form: whenever a change spans code and schema, the question "which lands first, and what happens in between" is a separate design question. Prefer making the dangerous order harmless over writing down the correct order.

### 10.6 It works on one platform and quietly not on the other

Same feature, same shared code path, one platform subtly worse. In one case, orientation detection scored recognition results at four rotations: on one platform the recognizer is orientation-sensitive so the correct rotation wins clearly, on the other it is rotation-robust so the scores don't separate and the winner is noise. Shared code is not evidence of shared behaviour when the layer underneath differs. List platforms separately in `affected_layers` and observe each.

### 10.7 Choosing the evidence source is part of the work

One authentication failure consumed a day. Every textbook check was performed and eliminated — certificate fingerprints, scopes, consent state, stale credentials, project ownership. The answer was one line in the device's own log, stating plainly that a credential was of the wrong type. It had been there the whole time. **Decide where the evidence will come from before forming the hypothesis;** five preconditions verified against the weakest available source produce a confidently wrong contract.

---

## 11. When to skip it, and what it doesn't fix

**Skip it** for typos, copy and styling changes, version bumps, a one-line fix whose cause you have already established, and exploratory work that will not produce a commit. The test is unchanged, and so is its scope: if the contract takes longer than the code, you don't need the contract — at the two lightest tiers only (§5).

**What it did not fix**, from the same period that produced everything above:

- **First drafts over-engineer.** More than one initial contract proposed a heavier design than the problem needed, and was cut down during review or escalation. The value is in the iteration; the first version is not scripture. Expect to write a simpler v2.
- **Thoroughness delays shipping.** One temporary workaround lived in production for weeks while the proper design converged. That is a real cost, and "we were being careful" does not refund it.
- **Large efforts are still underestimated.** A localization effort was scoped as a client-side task and turned out to require substantial backend work. A contract makes assumptions explicit; it does not make you good at estimating.
- **Hidden dependencies still get through.** One thorough contract missed a call made at screen-mount time, and it surfaced after shipping. The lesson became a standing check in that codebase's own contracts — draw the mount-time dependency graph. Note what did *not* happen: it did not become a rule in the specification. One incident is data, not a rule; §12 explains why it takes more than that.
- **The instrument itself drifts.** Our own record-keeping has now degraded three times (§12). If a methodology cannot keep its own logs current, be suspicious of any of its claims that depend on complete logs. Ours do, and §13 says so.

---

## 12. It keeps changing itself

Version 2.0 is not the specification we started with, and the mechanism that changed it is part of the design.

Four steps. Every non-trivial task appends one line to a case ledger: did it pass on the first attempt, were there hallucination events, which field caught or missed something, what the escalation was worth. When a pattern recurs, or a reviewer finds a hole in the specification rather than the code, it becomes a proposal. Proposals do not take effect by themselves — a human decides. Promotion means editing the specification, recording the change, and moving the version.

The step that does the most work is the pair of tests a proposal must pass:

1. **Substantive** — a real improvement, not a wording change.
2. **General across tasks** — true for future work of many kinds, not a patch for the single incident that prompted it.

The second test is the important one. Without it, opportunistic improvement degenerates into per-incident patching, and the specification grows into a pile where every rule is locally justified and the combination is incoherent — which is precisely the failure this methodology exists to prevent, applied to itself. A single incident goes into the ledger as data. It becomes a rule only when it can be argued to be general, or when it recurs.

Two honest observations about how this engine has actually behaved.

**It fires in bursts, not steadily.** Four versions were promoted in a single day — the day three independent reviews were commissioned. Cases accumulated for weeks without producing proposals, and then a concentrated critique produced several at once. Scheduled adversarial review appears to do more for a methodology than passive accumulation.

**A rule that was promoted to fix decaying discipline then decayed itself.** The ledger requirement was originally soft: "append a line when you finish a task." It stopped happening. So it was promoted to a hard gate — a task is not complete until the line exists — on the argument that soft discipline reliably leaks. Within a month, the gate was being ignored: ten consecutive qualifying tasks shipped with no ledger entry. The rule was in the specification the whole time.

The conclusion is uncomfortable and worth publishing: **a "hard" gate with no mechanical enforcement point is still soft discipline.** Calling a rule mandatory in a document does not make it mandatory. This is the strongest available argument for the enforcement tooling in §14, and it is an argument produced by the methodology failing rather than by it working.

---

## 13. Evidence, and its limits

**What this is based on.** Around a hundred pre-execution contracts over eleven weeks, on one commercial codebase — mobile clients, a backend service, two web consoles — with AI agents doing most of the implementation. Plus one controlled comparison on a separate greenfield build.

**The controlled comparison, including the part we lost.** The same one-sentence product request was given to two independent builds, one using this method and one not, then judged by a neutral agent shown both results and the original sentence. The method won where the decisions were hardest to reverse: it chose a native application over a web one, which the requester confirmed was the decision they cared about, and it got the primary interaction model right. It **lost** on something more embarrassing: the requester had named a specific core experience in their sentence, and the method-guided build shipped a placeholder for it while the unguided build wired up a real implementation immediately. Architecture correct, and the thing the person actually came for was not delivered. That result produced a new rule — a core experience the user named explicitly is a first-class deliverable and may not be downgraded to a placeholder — which is now part of the specification.

**What we did not measure.** Tokens. This article claims no numbers and no multipliers about token spend, because we never instrumented it. What was recorded is retries, rebuilds, and rounds-before-resolution — proxies, and readers should treat the §1 argument as reasoning about cost structure rather than as measurement.

**What cannot be extrapolated.** The first twelve tasks were fully instrumented: twelve of twelve landed on the first attempt with no hallucination events. Those numbers are real and they **do not extend to the remaining tasks**, which were not counted the same way. Two hallucination events were recorded later, both involving assertions about third-party SDK surfaces that did not exist at the pinned version. Both were caught during the task, at the point where somebody actually ran the check — and one of them was produced by the audit phase itself, which is its own lesson about where verification has to bite. A stricter measure on a wider surface produces worse-looking numbers, and that is the honest direction of the correction.

**Other limits.** One codebase, so domain effects cannot be separated from method effects. One human-AI pair throughout, so the audit's independence is context-level rather than organizational (§9). No benchmark suite: there is no reproducible task set with hidden traps that would let someone else measure this against a control. That remains the most valuable thing we cannot do alone.

---

## 14. Starting today

**The smallest version that works.** Take your next task that is not a typo. Before the agent writes anything, write three things: what will be observably true when this is done; what you are not allowed to decide alone; what you are touching, and what you are deliberately not touching. Then add one rule to how you work: **nothing is marked verified on the strength of a promise.** If the check has not run, it says so.

That is the whole minimum. It fits in a few lines, and in our experience it captures most of the value of the full method. It is written out, with the trigger list and one complete worked example, in [`MTM-LITE.md`](./MTM-LITE.md) — one page, and the only file you need to start.

**Wrapping it around your existing tools.** The specification is a markdown file, so the delivery mechanism is whatever your setup reads: instructions to your agent about how to behave, a rules file your editor loads automatically, or a starting prompt you paste once per project. Same core, different envelope. Nothing to install.

For Claude Code specifically there is a packaged version — `/plugin marketplace add jewanchen/mtm-contract` then `/plugin install mtm@mtm-contract`, or copy one folder if you would rather read it first. The behaviour above becomes the default, with the validator described below bundled alongside it. See [`plugins/mtm/`](./plugins/mtm/).

**Enforcement.** Some parts of this are mechanically checkable — no empty fields, no clause marked passing while its evidence is a promise, no task closed without a ledger line — and §12 is the argument for why checking them matters more than documenting them. That tooling is deliberately downstream of the specification rather than bundled with it: it belongs in continuous integration and in advanced setups, not in the path of someone trying the method for the first time.

**If you would like to test it properly.** The most useful contribution is not adoption — it is a replication we cannot run ourselves: the same tasks, on a different codebase, with and without the discipline, judged by someone who did not write it.

---

## 15. License, citation, contact

Licensed under the **Apache License, Version 2.0**. See [`LICENSE`](./LICENSE) for the full text and [`NOTICE`](./NOTICE) for attribution requirements: free for commercial and non-commercial use, modification, and redistribution, with attribution to Vast Intelligence Limited in derivative works — including tools, libraries, and adapted documentation implementing this specification.

```
Vast Intelligence Limited. (2026).
MTM Contract 2.0: An Ordering Discipline for Building Software Products
with AI Agents.
https://github.com/jewanchen/mtm-contract
Published: July 30, 2026.
```

**Vast Intelligence Limited**
Email: jeremy.chen@vastitw.com
Website: vastitw.com/mtm

For replication studies, integration partnerships, or enforcement tooling collaboration, use the channels above.

---

*Specification reference: [`MTM-CORE.md`](./MTM-CORE.md) (lifecycle, triggers, fields) · [`MTM-Plan.md`](./MTM-Plan.md) (greenfield branch) · [`MTM-Verify.md`](./MTM-Verify.md) (audit protocol) · [`EVOLUTION.md`](./EVOLUTION.md) (how this specification changes)*
