# MTM EVOLUTION — the engine that changes the specification

> This is where MTM is self-hosting. [`MTM-CORE.md`](./MTM-CORE.md) is the **current** specification; this file is the machinery that lets it grow from case experience plus human decision.
> Four stages, in a loop: **case ledger → proposal queue → discussion gate → changelog and version bump.**
> The iron rule: **a proposal never takes effect on its own. The gate on evolution is a person, not the AI.**
> 繁體中文快照（至 2.4）：[`EVOLUTION.zh-TW.md`](./EVOLUTION.zh-TW.md)

---

## §D The protocol — read this first; it defines how the other three sections move

**When to append to the case ledger (hard gate · v0.6 #14).** Every non-T0 task appends one line to §A after phase 5/6 — **and is not done until it does.** Same logic as phase 5's execution binding: soft discipline leaks, so bind it to a gate. Count honestly: a hallucination event is not a black mark, it is the core observation.

**When to open a proposal (into §B)** — one main mode and three backstops:

- **Main mode — inline opportunism** (decided 2026-06-29). While running *any* task, the moment you see a substantive way to improve the methodology itself, **say so on the spot in plain language**: the claim, and the reason. Do not wait for recurrence; do not wait for a review.
  - **Promotion requires passing two tests, both of them:**
    1. **Substantive** — a real improvement, or a textbook tweak? If there is nothing there, do not raise it.
    2. **General across tasks** (added 2026-06-29) — does this hold for many kinds of future work, or does it patch the hole from *this one incident*? A rule must be cross-task general. **Never add a rule for a single event.**
  - **A single event goes into the §A ledger as a data point, not into the rulebook.** It waits until it shows a cross-task pattern — either argued to be general on its merits, or proven by recurrence via backstop ①.
  - Why: inline opportunism without a generality gate degenerates into **per-incident patching** — the specification grows longer and more fragmented, which is the methodology's own version of "every part is right and the combination is wrong".
- **Backstop ①** — the same class of gap recurs **twice or more** in the ledger without inline catching it → raise it.
- **Backstop ②** — a phase 6 auditor identifies a gap in the specification itself, rather than in the task.
- **Backstop ③** — semi-annual sweep: any rule not cited by a single case in six months → propose deleting or rewriting it.

**The discussion gate — the only path into §C and CORE:**

- The AI proposes in plain language (claim, reason, blast radius). **The person agrees → it is promoted**: written into `MTM-CORE.md`, recorded in §C, version bumped.
- The person wants to think about it, or does not decide → it sits in §B as `pending-signoff` and does **not** enter CORE.
- The person decides **not** to promote, but the proposal is not dead → `⏸ parked-pending-evidence`, and it **must carry a decidable graduation condition** — what would have to happen for it to qualify automatically. This state exists so that "decided against" and "still waiting on you" do not look identical; without it, a settled proposal reads as outstanding and gets asked about again. *(Added 2026-08-02; #8 briefly used it and was closed the same day, so it currently has no live cases — kept, with no position taken.)*
- **The AI never writes an unapproved proposal into CORE.** The gate is always the person.

**Version rules** (renumbered to 2.x on 2026-07-30):

- patch (2.x.y) — wording, examples, added cases. No mechanism change.
- minor (2.x) — a phase, a field, or a discipline added or changed.
- major (3.0) — structural rework of the lifecycle.

> The old specification line v0.1–v0.7 merged into the public article line at 2.0 (see §C). The `v0.x · #N` markers beside rules record **the version each was promoted in**, not the current version.

On promotion: edit `MTM-CORE.md`, record in §C, bump the version, and mark the originating ledger row `→ triggered proposal #N`.

---

## §A Case ledger (append-only)

> Columns: date · task · tier · first attempt clean? · hallucination events · which field caught or missed what · what the escalation was worth · proposal triggered
>
> **Location rule (v0.6 #14)**: §A records only changes to **MTM itself** (dogfooding). A consuming project's task ledger lives in that project, not in this repository (decided 2026-06-30).

**Seed — trial on a consuming project, from 2026-05-14. The full per-task record stays in that project and is not published. 56 contracts in total.**

| Date | Task | Tier | Clean | Halluc. | Key observation | Escalation value | Proposal |
|---|---|---|---|---|---|---|---|
| 05-14 | Push dispatch chain | T2 | ✅ | 0 | `cross_module` caught that an existing helper already did half the work — no duplicate | surfaced three decisions | — |
| 05-14 | Company profile management | T2 | ✅ | 0 | `affected_layers` caught silent drift: fields declared on the entity and used by the client, absent from the update DTO | notify only when actor ≠ owner | — |
| 05-14 | Dashboard redesign | T2 | ✅ | 0 (1 at compile time) | the type checker caught a misused timestamp field | four questions asked up front | — |
| 05-14 | Batch operations | T2 | ✅ | 0 | **the literal intent did not map onto the data model** → four candidate populations enumerated | highest: scope made precise | → #6 candidate set |
| 05-14 | Recovered-customer database | T3 | ✅ | 0 | new entity + migration | **the largest redesign** (one-way recipient → a shared store) cost nothing because it happened during escalation | → #6 |
| 05-16 | Scheduled status change | T2 | ✅ | 0 | — | **the person overturned the escalation structure itself**, replacing it with a unified design | → #5 forced-disagreement |
| 05-16 | Universal re-invite | T3 | ✅ | 0 | acceptance path made idempotent | escalation triggered two architectural decisions outside the task's own scope | → #6 |

**Rollup that seeded the v0.2 proposals**: 12 build-mode samples, **zero hallucination events** (the few that occurred were caught at compile time), **12 of 12 landed on the first attempt**. The highest value landed in the escalation phase every time, and always as "the agent laid out real options and the person reframed" — **never from an objection the agent manufactured.**

---

**2026-06-29 · MTM self-optimisation to v0.2** — T3 · in progress · 0 hallucinations
Running MTM on MTM. First live use of the status header and `observed_result`. → **#1**

**2026-06-29 · Three independent evaluations of MTM** (adoption / methodology / adversarial) — T2
The evaluations converged: the load-bearing parts are escalation and the candidate set, the independent audit, and artifact-over-memory. The largest gap: verification where "declared" is treated as "executed", and self-tiering being self-defeating. → **#9 / #10 / #11**

**2026-06-29 · Designing MTM Plan + three-way review** — T2
Gap confirmed real. Reinforcements folded in: the standalone-versus-integrated fork, the imagination-first phrasing, the four never-silent defaults, and a handoff written in phase 1's vocabulary. → **#12**, promoted v0.4

**2026-06-29 · A controlled A/B comparison** (with MTM versus without, from the same one-sentence request) — T2
**MTM's first genuine control.** A neutral agent judged intent-fit at roughly 5/5 versus 2 solid, 1 partial, 2 missed. MTM got the highest-risk decision right (native versus web) and the primary interaction model right — **but shipped a placeholder for the "real instrument sound" while the unguided build wired up a real one on the spot, and lost there.** Honest reading: a win on points, not a knockout. → **#13**, promoted v0.5

**2026-06-30 · MTM self-optimisation to v0.6** (ledger hard gate + version-label fix) — T2 · ✅ · 0
A six-week benefit analysis on the consuming project found the trial log's settlement table had never been filled in — "soft discipline leaks" is a cross-task pattern. CORE and the README were also still carrying a stale v0.2 label: **MTM drifts too.** → **#14**, promoted v0.6

**2026-07-05 · Purpose-first discovery added to MTM Plan** — T2 · ✅ · 0
The existing Plan jumped straight to the forks with no anchor on *why*. The person's ruling: do not volunteer extended features; greenfield only. → **#15**, promoted v0.7

---

**2026-07-30~31 · Publishing specification 2.0** (article in English and Chinese, `MTM-LITE.md`, the version renumber) — T3 · ⚠️ three rounds of independent review, all with findings, all fixed · 0 hallucinations

A documentation task takes escalation the same way code does: the first outline was positioned wrongly, and it was overturned and rebuilt *before* drafting — the cost was one conversation instead of a rewrite. Precondition checks turned up two pieces of bad news about this project and both were written into the article rather than hidden: ① #14's ledger hard gate had already broken (ten qualifying tasks shipped with no entry after it stopped); ② the article's flagship debugging case **has no contract** — it is the time the discipline was skipped.

**The biggest finding was not in the deliverable but around it.** An adopter-perspective review returned "would not adopt", and every reason sat outside the article: the English path dead-ended at a Chinese specification, the quick start pointed at a superseded template, the integration guide taught the self-audit that §9 refutes, and there was no light-tier example. After adding `MTM-LITE.md`, raising the template to 2.0, rewriting the integration guide and repointing the entry, the same perspective re-run returned "would adopt".

The evidence audit separately caught six untrue or unsourced statements — including one **inside the honesty section** that described two hallucinations as caught at the verification step when they were caught during implementation, one of them produced by the audit itself.

*Escalation value: very high — one sentence about positioning rebuilt the whole outline, and it settled "no efficiency estimates; the reader judges".* → **#16, #17**

> **Two portable lessons from this row.** ① **Scanning the deliverable for leaks is not enough — scan one hop out.** The article leaked nothing; the files it linked to contained private paths and an environment variable name. ② **An adopter-perspective review has to be re-run after the fixes.** Every reason for the first rejection lay outside the deliverable; without re-running you never learn whether the additions actually connected.

**2026-08-01 · Packaging MTM as an installable Claude Skill** (behaviour + references + a bundled validator) — T3 · ⚠️ two independent reviews (specification fidelity / adversarial install-and-use), both with blocking findings, all fixed · 0

**The bundled enforcement script did not fire in the layout its own template teaches.** With `PASS` and `observed_result` on separate lines it never triggered — so a critical-tier contract with every clause passing and every piece of evidence still a promise exited cleanly. **Both reviewers hit this independently**, and one framed it decisively: this is worse than shipping no script, because it **launders unverified work into something that looks audited**, and the user stops reading the contract. Now evaluated per clause, across lines.

Also fixed in the same round: the untouched template passed after two word edits (placeholder detection was whole-line only); genuine observations were flagged as promises; non-UTF-8 input crashed with a traceback mid-CI-batch; Chinese headings matched nothing; and critical work self-labelled `tier=local` passed silently (now warned on content keywords). The fidelity review separately found 11 divergences from CORE — invariant 7, the grounding step, the mandatory internal red-team, decision records, the cross-domain trigger — all closed.

*Escalation value: very high — **adversarial "install it, use it, then try to break it" hit the fatal problem sooner than clause-by-clause fidelity checking.** The latter found the same defect, but the former also found that the install command itself was dead.*

> **Portable lesson**: when you bundle an enforcement script, the first thing to test is not whether the rules are right — it is **whether the script fires in the layout your own documentation teaches**. A gate that passes silently costs more trust than no gate.

**2026-08-02 · invariant 8, prompted and promoted (#18)** — T2 · ✅ · 0

Surfaced by the person's observation: after an independent review comes back, the main model mostly agrees from the auditor's angle, does not think from the original purpose or the discussion history, and goes straight to recommending a reversal. **The executor's own evidence**: it removed a figure as "unsourced" because the auditor could not find it (it was sourced, just not in the auditor's three inputs), and changed a deliberate editorial decision as though it were a defect. The first version of the proposal was rejected — it offered "add an adjudication step to the process", and the person pointed out the actual issue: **the main model holds the context and should be thinking**; proceduralising it is avoidance.

*Escalation value: very high — it lifted a patch aimed at phase 6 up to the invariant layer, because the same failure exists at every boundary where a confident input meets a model holding context: CI, subagents, documentation, another model.* → **#18**, promoted 2.1

**2026-08-02 · #16 and #17 promoted; #8 given a graduation condition (2.2)** — T2 · ✅ · 0

**The value of this round was a self-correction.** The earlier recommendation to drop #8 rested on "five weeks parked and nobody reached for it" — which commits the exact error invariant 8 had just been written against (reading *I have not seen it used* as *it is not needed*). Re-asked as "have the failures it targets actually occurred": yes, repeatedly — scope underestimated, five probe rounds to converge, work that had to be split into five batches. **But the second question failed**: the underestimate happened at grounding, and the probe rounds were empirical investigation of an unknown process. So: neither dropped nor promoted — given a decidable graduation condition instead. #16 gained its decisive second half on promotion: the enforcement point must be tested against the layout the documentation teaches.

*Escalation value: high — the person asked in the direction of "all three are worth doing", the executor did not comply, and corrected its own earlier reasoning on the spot. Invariant 8 tested in both directions.* → **#16 · #17**, promoted 2.2

**2026-08-02 · #19 promoted (2.3): purpose becomes a checkpoint, not just a direction** — T1 · ✅ · 0

**The executor checked before answering.** Half of what was asked for **already existed** in the specification (asking purpose first in greenfield, #15 / discipline 0); after confirming by search, it said so rather than building it a second time — invariant 8 used positively. The genuinely new half was the other one (discuss it when the purpose and the request contradict), and it closed the hole an independent reviewer had named in #15: all three wirings used the purpose to steer what came next, none used it to check the request.

*Escalation value: high — a request mixing "already exists" with "new"; checking item by item saved a duplicate build and stopped the specification growing a second discipline 0.* → **#19**, promoted 2.3

**2026-08-02 · Plugin install verified end to end** — T1 · ✅ · 0

The one item carried as unverified through the batch is closed: `/plugin marketplace add` and `/plugin install` were run for real, the skill entered the registry, and the plugin-installed validator exited 1 on the adversarial fixture. **The executor cannot run slash commands, marked it `UNVERIFIED` throughout, and never let "the structure is correct" stand in for the test** — invariant 6 used positively. Side effect: an earlier manual copy coexisting with the plugin caused a duplicate registration; the test copy was removed.

**2026-08-02 · #20 promoted (2.4): the specification's first revision driven from outside** — T1 · ✅ · 0

Less than a day after invariant 8 was promoted, **another agent running it on a real task hit its edge and reported back**: rejecting a finding only required pointing at the decision, so a decision whose reason proved false passed the check — the rule shielded the failure it was written to prevent. The reporter's self-assessment was sharper than the executor's own (they identified precisely which step they had skipped). **The executor did not accept it wholesale**: two rounds of internal red-teaming (does this make rejection too expensive? is a false reason simply a defect?) failed to overturn it, and only then was promotion recommended.

*Escalation value: very high — **the first field report from outside use**, and it produced a specification change directly. That carries more weight than any internal derivation, and it is exactly the kind of evidence §13 of the article keeps asking for.* → **#20**, promoted 2.4

**2026-08-03 · Verifying how the plugin updates (updatability of the distribution channel)** — T1 · ✅ · 0

**The executor gave the wrong answer first**: it told the person to re-run install to get the new version. In practice `install` only handles the first install and returns "already installed". The truth is two steps, and the first is not obvious: the marketplace is a git clone that **stops fetching** after it is added, and `installed_plugins.json` separately pins the plugin to the commit it came from — so updating the plugin alone does nothing; the marketplace must be updated first. Also found: the CLI has non-interactive subcommands, so the executor could have done this without handing it back at all. After updating, the new cache directory's rules and validator were **actually run** (adversarial fixture exits 1, false-positive fixture exits 0) rather than trusting the success message.

*Escalation value: medium — **updatability of the distribution channel is a failure surface outside the specification.** On a day with four version bumps, anyone who installed in the morning is holding stale rules and does not know it, and the documentation only covered installing. Same shape as #16: a gate that cannot fire and a channel that cannot update both manufacture a false sense of being current.*

**2026-08-06 · The English specification, and absorbing MTM-Arch (2.5)** — T2 · ✅ · 0

The claim that "CORE already covers MTM-Arch" was asserted from memory and **was wrong**. The person asked whether it was true, a full read followed, and seven mechanisms turned out to be missing — two of them load-bearing: `needs_revisit` (a decision record whose trigger has fired stops counting as grounding) and the four-step architectural dialogue with step one forbidden from citing existing code. **Had the recommendation been accepted as given, `needs_revisit` would have been discarded along with 457 lines** — and it is the piece that closes #20's gap.

*Escalation value: very high — a question, asked at the right moment, prevented a mechanism from being deleted on the strength of an unverified claim. This is invariant 8 exercised by the person against the executor, and #20's rule applied to the executor's own recommendation: the reason offered for a decision must itself have been checked.*

<!-- append new cases above this line -->

---

## §B Proposal queue

> Each entry: evidence → proposed change → blast radius → status.

### #1 — One unified lifecycle (CORE as the spine; the older documents retained as phase detail) `✅ promoted v0.2 (2026-06-29)`
- Evidence: in practice only one workflow was ever running; the audit was split across two documents.
- Change: `MTM-CORE.md` becomes the single 0→6 entry point; the architectural audit merges into phase 6.
- Decided: CORE is the spine; the other documents are kept with headers pointing back, so existing references do not break.

### #2 — The `observed_result` field (closing the verification chain) `✅ promoted v0.2 (2026-06-29)`
- Evidence: `verifiable_by` is a promise, not a record. One contract said "check the outbound call count" and had nowhere to put the number.
- Change: every outcome gains `observed_result` — what was actually seen, with its evidence.

### #3 — The Contract ↔ Verify spine (ten modes ↔ fields) `✅ promoted v0.2 (2026-06-29)`
- Evidence: a table mapping failure types to the fields that should stop them had already proven itself in practice.
- Change: generalised to ten modes in CORE §6; each report section names which modes it covers.
- Effect: Verify stops being a separate checklist and becomes "did each preventive field hold?"

### #4 — The blast-radius classifier (phase 0) `✅ promoted v0.2 (2026-06-29)`
- Evidence: tiering was being done on instinct.
- Change: the T0–T3 table routes depth. **"Thorough" is redefined as "correctly routed".**

### #5 — Forced disagreement split into "internally mandatory, externally conditional" `✅ promoted v0.2 (2026-06-29)`
- Evidence: zero high-value events came from an objection the agent manufactured. Forcing one every time produces cry-wolf.
- Change: phase 2 steps 4–5.

### #6 — Escalation raised to a first-class phase, with the candidate-set sub-protocol `✅ promoted v0.2 (2026-06-29)`
- Evidence: "the literal intent versus the data model" is a recurring source of bugs — the four-population batch case, and a re-invite scoped too narrowly.
- Change: phase 2 becomes first-class and candidate-set enumeration is written as a sub-protocol.

### #7 — A machine-readable status header (resumability) `✅ promoted v0.2 (2026-06-29)`
- Evidence: the original motivation — step 3 contradicted at step 15 — needs a single point of truth after a context summary.
- Change: a `status` block at the top of the template.

### #8 — A second axis in phase 0: complexity / decomposability `✕ closed (2026-08-02, decided by the person)`
- Evidence: blast radius and complexity are orthogonal. One task was high blast *and* high complexity (a redesign); another was T2 blast with low complexity (one search closed the single unknown). High blast with low complexity — changing one line of auth — is the cell pure complexity analysis misses.
- Proposed change: phase 0 goes from one axis to two — blast decides **verification depth**, complexity decides **decomposition and grounding depth** — with the output bound to a split-or-don't decision.
- Signals were to be **countable** (anti-theatre): how many domains, does the literal request match the model, how many independent unknowns, is it reversible.
- Risk noted at the time: scoring complexity out of ten would become theatre — hence counting signals, not scoring.
- **2026-08-02 re-examination** (correcting the earlier reasoning of "unused, therefore drop"): the right question is not whether anyone cited the proposal, but **whether the failures it names actually occurred**. They did, repeatedly: scope underestimated, five probe rounds before convergence, work that had to be split into five batches — and that split was **a human's judgement; the specification did not help.** **But** the second question fails: the underestimate happened at grounding (not for want of counting signals), and the probe rounds were empirical investigation of an unknown process that no tiering would shorten. Conclusion: **the phenomenon is real; the mechanism is unproven against it.**
- **Closed (2026-08-02)**: the full analysis is kept here. It is closed **not because it is wrong, but because its mechanism was never shown to intervene on the failures it names.**
- **Reopening condition (kept)**: one case where **explicitly counting complexity signals changed a split-or-don't decision at the time** — hindsight does not count. With that evidence it can be reopened directly.

### #9 — Execution binding: give `verified_by` and `observed_result` teeth `✅ promoted v0.3 (2026-06-29)`
- Evidence: an adversarial review plus the project's own 12-of-12 cases, where `observed_result` was uniformly left at `PENDING`. With a strong model the failure is a convincingly filled field with no check underneath, and a plausible value looks identical to a closed one.
- Change: CORE invariant 6 plus the phase 5 hard rule.
- Both tests: substantive ✅ (closes the largest maturity gap) / general ✅ (holds for every contract).

### #10 — Blast radius by observable trigger, not by the agent's own judgement `✅ promoted v0.3 (2026-06-29)`
- Evidence: self-tiering is self-defeating — the judgement being asked for is exactly the unreliable one that rigour exists to backstop, and it degrades under deadline pressure.
- Change: the trigger list; any hit promotes, and T3 cannot be self-demoted.

### #11 — The minimum viable contract (three load-bearing fields at T1) `✅ promoted v0.3 (2026-06-29)`
- Evidence: a strong model handles the middle fields anyway; the full ceremony has diminishing returns at T1, and heaviness means the valuable 20% gets skipped along with everything else.
- Change: T1 defaults to `intent` + `escalation`/candidate set + `affected_layers`.

### #12 — MTM Plan: the greenfield phase 0 branch `✅ promoted v0.4 (2026-06-29)`
- Evidence: phase 1 bootstrap, phase 2's candidate set and the old Stage 0 all assume the agent asks when *it* is ungrounded, in developer language. Greenfield forks (platform, cloud, multi-user, payments) have no source to ground against, and a non-technical person cannot answer a domain question.
- Change: a new `MTM-Plan.md`, plus the phase 0-Plan branch in the spine.
- A three-way independent review returned GO-with-additions; all eight additions were folded in.

### #13 — The customer's core need comes first `✅ promoted v0.5 (2026-06-29)`
- Evidence: the **A/B comparison**. MTM handled the architecture and left the named core experience as a placeholder; the unguided build delivered the real thing on the spot — **on the user's literal core need, the unguided build won.**
- Change: CORE invariant 7 and Plan discipline 8.
- Coexists with #11: "cheap things can wait" applies to secondary features only.

### #14 — The case-ledger append becomes a hard completion gate `✅ promoted v0.6 (2026-06-30)`
- Evidence: §D's "append per non-trivial task" was soft discipline with nothing binding it. A six-week analysis found the settlement table had never been filled and the log stopped after the first twelve entries — the same "meta-record leaks" hole. **The document meant to cure it had the disease.**
- Change: not appended, not done.

### #15 — Ask purpose first in greenfield, plus discovery coverage `✅ promoted v0.7 (2026-07-05)`
- Evidence: the greenfield opening jumped straight to hard-to-reverse forks with **no anchor on what the person is actually hoping for.**
- Change: Plan discipline 0. **CORE's 0→6 is untouched**; only the Plan opening protocol widens.
- The person's ruling: extended features are not volunteered; the trigger stays greenfield-only.
- Risk control: apart from purpose, everything stays "cheap → assume, expensive → make them choose". No stacking open questions — that would return to the interview hell this document exists to kill.
- **Independent methodology review (2026-07-05, after promotion)**: conditional yes, 6/10. It agreed the placement was right and correctly scoped, and found three holes, all since closed — ① the purpose answer had no downstream wiring (posture, not mechanism) → discipline 0 now wires it into the glossary, the fork order, and invariant 7's protected item; ② "cover it all in the opening" smuggled ceremony back in → changed to asking only the purpose up front; ③ no fallback for a vague answer → added.
- **Self-assessed evidence level (raised by the reviewer, recorded honestly)**: #15 is the **weakest-evidence promotion** in the series — no control (unlike #13), no recurrence count (unlike #14). It passed the gate on argued generality plus aspiration. **Backstop**: the next two greenfield runs each record whether the purpose answer actually changed a downstream decision; two consecutive misses trigger a re-examination.

### #16 — A hard gate needs a mechanical enforcement point, or it is still soft discipline `✅ promoted v2.2 (2026-08-02)`
- Evidence: #14 promoted the ledger append from soft discipline to a **hard gate**. **A month later the gate itself was ignored** — ten consecutive qualifying contracts with no entry. The rule was in the specification the whole time.
- Diagnosis: #14 changed the word "soft" to "hard" and **added no mechanical trigger.** Declaring something mandatory in a document is not enforcement. This was the **third** occurrence of the same class of gap.
- Source: turned up by a precondition check during a T3 task. Published in §12 of the article as an honest case.
- **The second half, added on promotion (the most important correction)**: an enforcement point is not enough — **it must be tested against the layout your own documentation teaches.** Demonstrated by this project's own validator, whose headline check only fired when `PASS` and `observed_result` shared a line while the template puts them on separate lines by design. **A gate that passes silently costs more trust than no gate.** So CORE §7 is written in two halves: either a check that demonstrably fires, or an honest downgrade to a recommendation. There is no honest third state.

### #17 — A debug branch in phase 0, for symptoms whose scope is not yet known `✅ promoted v2.2 (2026-08-02)`
- **Evidence, from four independent directions:**
  1. The tier table keys **entirely off known scope**. But **a bug's scope is unknown — that is what makes it a bug.** The table cannot route it.
  2. `MTM-LITE.md` said a one-line fix whose cause you have established can be skipped — **that is the easy case.** What eats an afternoon is *not yet established*, and the specification had no phase for it.
  3. The article's flagship debugging case **admits it has no contract**. The methodology's most expensive failure is precisely the class it had no shape for.
  4. An **adopter-perspective review** named it the thing most wanted and not delivered: debug loops are what cost time and money, and the specification offered one habit and no artifact.
- The consuming project already had this as local practice, never promoted: stop after round one, write a contract with `prior_guesses` including each result, and for a wrong value make the first move a search for every producer.
- Change: a debug branch in phase 0, triggers bound to two observable signals, a four-field contract, one hard rule.
- **Scope deliberately kept small on promotion**: three reviews all named the specification's bulk as the main adoption blocker; a patch that fattens it can be net negative.

### #18 — invariant 8: held context is not surrendered `✅ promoted v2.1 (2026-08-02)`
- **Evidence**: an independent review's value comes from a deliberately restricted view — and the same restriction means it **systematically cannot see intent**. Observed: a figure was reported as unsourced (correctly, for the corpus the reviewer had) and removed on the spot; it was sourced elsewhere. In the same batch a deliberate editorial decision was treated as a defect.
- **Diagnosis** — not a random slip, three structural biases: ① the burden is asymmetric (a finding is a concrete assertion; defending requires reconstructing context, so agreeing is far cheaper) ② the report carries the authority of its form, while the prior reasoning is scattered through a conversation ③ deference to the most recent confident input. **#5 caught the mirror image of this bias** (manufactured objections are worthless); nobody had caught this direction.
- **Key insight**: the problem is **not in phase 6**. The same failure occurs at every boundary where a confident external input meets a model holding context — CI, a linter, a subagent's report, documentation, another model, even the person's own later sentence contradicting a decision from three days ago. Patch phase 6 and the hole reopens elsewhere. **Fixed at the invariant layer.**
- **Not made into a procedure**: the person explicitly rejected "add an adjudication step" — **the main model holds the context and should be thinking**; needing a rule to prompt "consider why we decided this" is itself the failure. What a rule *can* do is force retrieval of what is already in hand. Hence one question, symmetric burden, and a self-test.
- **What this means for vibe coding**: the person has given up reading every line and verifying, but not *what they want*. Any mechanism that quietly transfers **intent-level decisions** to automation erodes the one thing they were still contributing — and deference to a reviewer is the hardest kind to notice, because it **looks like rigour**. The general rule: **automation may generate and may challenge, but it may not decide what a person decided.**
- **Counter-risk**: taken too far this becomes "I had my reasons" as a universal shield, which is worse than compliance. Hence symmetric burden and the self-test.

### #19 — The purpose also checks the request itself `✅ promoted v2.3 (2026-08-02)`
- **Evidence (a gap in the specification's own design)**: #15 wired the purpose answer into three places — a note in the glossary, which forks get asked first, which feature invariant 7 protects. **All three use the purpose to steer what comes next; none uses it to check the request.** That is exactly the hole the independent methodology review named after #15: the purpose was **posture, not mechanism**.
- Change: a fourth wiring in Plan discipline 0, mirrored in CORE's phase 0-Plan branch.
- **Two guards, neither optional**: ① the bar stays at **plainly contradicts** — widened, it becomes the teleological form of the cry-wolf failure #5 already dealt with; ② **the output is a question, never a refusal** — the decision stays theirs.
- **Side effect**: #15 carries a backstop asking whether the purpose answer ever changes a downstream decision. A check that can block a contradictory request gives that backstop something observable to measure.
- Scope: greenfield only, as #15 is. It plausibly generalises, but there is no instance yet — and widening a rule without one is why #8 was parked.

### #20 — The self-test extended: rejecting a finding takes the decision **and its closed grounding** `✅ promoted v2.4 (2026-08-02)`
- **Source (recorded plainly)**: **a field report from outside this project** — another agent, running 2.3 on a real task, hit the edge and reported back. Not derived internally. Less than a day after invariant 8 was promoted.
- **Evidence (their instance)**: they ruled out an option in writing on the grounds that "the other party sees nothing before installing the app" — a recorded decision with a stated reason. The review found the code path in question does send name, company, title and phone. **The reason was invented.**
- **The hole**: 2.3's self-test caught only *"cannot state a reason"*. It did not catch *"a reason exists and is false"*. And since rejecting a finding only required pointing at the decision, the check passed.
- **The ugly part**: invariant 8 was written to stop decisions being quietly reversed by a reviewer, and it ended up **shielding a decision built on a false premise** — while exposing false premises is the entire reason the review exists. **A rule protecting the failure it was built to prevent.**
- **Placement**: the boundary between invariants **6 and 8**. Six governs the moment a decision is *made*; eight governs the moment it is *cited against a finding*. Nothing governed the latter.
- **Internal red-team (two rounds, neither overturned it)**: ① does this make rejection so expensive that everything gets accepted again? No — nearly free when the decision was properly grounded, expensive only when it was not, and **that asymmetry is correct**. ② Is a false reason simply a defect? Yes, but **the mislabel happens before that can be noticed** — the executor sees "a recorded decision" and stops — so the fix belongs at the labelling step.
- **Observation from the reporter, worth keeping**: 2.1, 2.2 and 2.3 all landed on the same day, and §12 had already recorded that the engine fires in bursts under external critique. That day's pressure was a conversation; the previous one was three commissioned reviews. **The pattern held again** — supporting "schedule adversarial review rather than waiting for cases to accumulate".

<!-- append new proposals above this line -->

---

## §C Changelog — only what passed the gate

- **2.5** (2026-08-06): the specification becomes English-first, and **the mechanisms still live in `MTM-Arch.md` are absorbed into CORE**. The prior claim that CORE already covered Arch was asserted from memory and was wrong; a full read found seven, two of them load-bearing — **`needs_revisit`** (a decision record whose trigger has fired stops counting as grounding, which is the missing half of #20: that rule requires *closed* grounding and nothing said how grounding is declared closed no longer) and **the four-step architectural dialogue** with step one forbidden from citing existing code, which is what stops pattern-matching from passing as architectural thinking. Also absorbed: the decision-record template, `architectural_basis` and two standing escalation rules in the contract template, the four architectural audit questions with their automatic follow-ups, phase 1's filing rules, the internal-label translations, and a known-risks section naming seven ways this method fails and what holds each down. `MTM-Arch.md` is marked superseded with a table saying where each part went. `MTM-CORE.zh-TW.md` is labelled a 2.4 snapshot rather than an equal mirror — maintaining two specifications is how the drift in this repository began.
- **2.4** (2026-08-02): promotes **#20**. Rejecting a finding requires **the decision *and* its closed grounding**, not the decision alone. 2.3's self-test blocked only a missing reason, not a false one — so invariant 8 could shield a decision built on a false premise, which is what the review exists to expose. Placed at the boundary of invariants 6 and 8. **The specification's first revision driven by outside use.**
- **2.3** (2026-08-02): promotes **#19**. The purpose now checks the request itself: when what is asked for plainly contradicts the stated goal, put the contradiction to the person rather than building it or silently redesigning it. Two guards — the bar stays at *plainly contradicts*, and the output is a question, never a refusal. Greenfield only.
- **2.2** (2026-08-02): promotes **#17** (the phase 0 debug branch — the tier table keys off known scope, and a bug's scope is what is unknown; triggers bound to two observable signals, a four-field contract, and "when round one fails, stop changing code"; deliberately kept small) and **#16** (a rule is only hard if something mechanically enforces it, **and the enforcement point must be tested against the layout the documentation teaches** — this project's own validator did not fire in its own template's layout). **#8 not promoted**; given a decidable graduation condition instead.
- **2.1** (2026-08-02): promotes **#18, invariant 8 — held context is not surrendered**, paired with invariant 6 (six: do not claim what you did not check; eight: do not discard what you did establish). Establishes that **the auditor is a witness, not a judge** — its view is deliberately restricted, so it cannot see intent — and that findings are input to judgement rather than a verdict. On receiving findings: *defect, or decision?* Decisions escalate rather than being reversed by the executor. Deliberately **not** a procedure: the main model holds the context and should think; the rule only forces retrieval of what is already in hand.
- **2.0** (2026-07-30): **renumbering and publication.** ① The v0.1–v0.7 specification line merges into the public article line; the current version is **2.0** everywhere. (The first article published as `Methodology v1.0` while the specification ran v0.x, so an outside reader saw "v1.0 in May → v0.7 in July" and read it as a regression.) Per-rule `v0.x · #N` markers are kept as promotion history and **not** rewritten — rewriting them would falsify the changelog. ② Published the 2.0 article and its Chinese version, converging on one claim: **put the cheap checks before the expensive generation.** Honesty carried in full: tokens were never measured (proxies only), "12 of 12, zero hallucinations" does not extrapolate, the controlled comparison was partly lost, the flagship debugging case has no contract, and #14's hard gate broke within a month. **No mechanism changed in 2.0** — no phase, field or discipline was added.
- **v0.7** (2026-07-05): promotes **#15** — the greenfield opening asks one open question about purpose before any fork.
- **v0.6** (2026-06-30): promotes **#14** — the ledger append becomes a hard completion gate, fixing the "soft discipline leaks" hole. Same batch: corrected stale version labels, and established that a consuming project's task ledger lives in that project.
- **v0.5** (2026-06-29): promotes **#13**, derived from the **A/B comparison** — MTM's first genuine control. Honest conclusion: a win on points, and a loss on the user's literal core need, which is what produced the rule.
- **v0.4** (2026-06-29): adds **MTM Plan**, the greenfield branch. Promotes #12.
- **v0.3** (2026-06-29): focus — **make MTM more efficient for a capable model** (refocused away from selling a product or writing a paper). Promotes **#9** (execution binding), **#10** (observable triggers), **#11** (the minimum viable contract). Diagnosis: what MTM corrects is the systematic bias capability does not remove — literal-mindedness, scope drift, forgetting earlier context, agreeableness. Those are what is worth having; the middle fields a strong model does anyway.
- **v0.2** (2026-06-29): promotes #1 unified lifecycle, #2 `observed_result`, #3 the Contract ↔ Verify spine, #4 the blast classifier, #5 the forced-disagreement split, #6 escalation as a first-class phase, #7 the status header. Also settled the evolution gate itself: inline opportunism, two tests (substantive and cross-task general), single events into the ledger rather than the rulebook, and promotion on the person's nod.
- **v0.1.2** / **v0.1.1** / **v0.1**: the conversation-discipline rules; forced disagreement as originally written (later replaced by #5); and the initial eleven-field build/review trial.

<!-- append new versions at the top of §C -->
