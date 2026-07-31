# MTM Contract — `<task ID + one-line description>`

> **This is the full template, for structural and critical work.**
> For ordinary tasks you write three fields, not all of these — see
> [`MTM-LITE.md`](./MTM-LITE.md) for the light version and the
> triggers that decide which one a task gets.
>
> Copy this file to `contracts/YYYY-MM-DD_<task>.md` and fill it in
> before writing implementation code. Empty sections are not
> acceptable; `N/A` is a valid answer; "I don't know" must be
> written as `UNKNOWN: <reason>` so it surfaces in review.

---

## status

Single source of truth when a session is summarized or handed off.
Read this first on resume.

```
stage=<0-6> | tier=<trivial|local|structural|critical> |
blocked_on=[] | unverified_preconditions=[] | open_escalations=[]
```

---

## intent

One sentence. Verb-first. Externally observable.

Example: "Admin marks employee X as resigned in the dashboard;
within 30 seconds, all contact-card holders' address books reflect
the new grey-check archived state."

---

## affected_layers

What changes, what stays the same, and where.

- `backend.entity:` <which entities; new fields; new tables; or none>
- `backend.service:` <which services; new methods; or none>
- `backend.endpoint:` <new / modified / unchanged routes>
- `backend.migration:` <YES + filename / NO>
- `backend.cron / queue / push:` <YES + trigger / NO>
- `app.provider:` <which client-side stores or providers>
- `app.screen:` <which screens render the change>
- `app.cache:` <cache version bump? defaults safe for old caches?>
- `web-admin / platform-admin:` <YES + which pages / NO>
- `env / secrets:` <new variables? which environments?>

---

## preconditions

Conditions that must be true before implementation can proceed.
Each must include how it has been verified.

- `<condition 1>`
  verified_by: `<commit / migration / staging health / manual test>`
- `<condition N>`

If any precondition is unverified, close it before writing code.
The pattern `UNKNOWN: <what to grep / verify first>` is acceptable
and signals "5-minute grep before keyboard touches code."

---

## schema_assumptions

What you assume about data shapes, defaults, or invariants.

- `<assumption 1>`
  source: `<spec section / entity comment / commit ABC / past task ref>`
- `<assumption N>`

Assumptions without a source automatically lower the contract's
`confidence` rating by one level.

---

## cross_module_contract

What this work emits, listens to, and assumes others will or will
not do.

- **emit:** `<events / push payloads / API responses I produce>`
- **listen:** `<events I subscribe to>`
- **I assume others will:** `<list things outside this work that
  this work depends on>`
- **Others depend on me to:** `<list invariants I must preserve so
  upstream callers do not break>`

---

## expected_outcome

Externally observable results, not "implementation complete." Phrase
as "user does X, observes Y."

- `<outcome 1>`
  verifiable_by: `<manual step / automated test / log line / trace>`
  observed_result: `<what you actually saw this session — command
  output, query result, log line, observed value>`
- `<outcome N>`

Outcomes are the audit checklist. Every clause here must map to a
PASS / FAIL / MUTATED mark after implementation.

**Execution binding — the rule that makes the rest of this real:**
a clause may not be marked PASS while its `observed_result` is
still a promise or `PENDING`. Either paste evidence you actually
produced this session, or mark it `UNVERIFIED` and carry it into
the audit as an open item. `PENDING` is a waypoint, not a pass.

---

## confidence

- **overall:** `<high / medium / low>`

Low-confidence sub-items (must be enumerated):

- `<sub-item>` — `<why uncertain>` — `<plan: escalate / spike /
  proceed with documented assumption>`

---

## escalation

Decisions the implementer should NOT make alone:

- `<decision 1>`
- `<decision N>`

Conditions that should stop work and report:

- `<condition 1>`
- `<condition N>`

---

## grounding

Where the content of this contract comes from. Any clause without
a citable source is `SPECULATIVE` and should be reviewed first.

- Spec: `<section ref>`
- Architecture: `<section ref>`
- Prior commits / entities: `<refs>`
- Progress / decision logs: `<refs>`
- User conversation: `<verbatim quote with date>`

---

## rollback_plan

- **code:** `<git revert / branch swap / forward-fix>`
- **schema:** `<migration reversible? forward-fix path?>`
- **env:** `<which variables to remove?>`

---

## test_plan

- **local:** `<steps>`
- **staging:** `<curl / build / manual flow>`
- **prod:** `<smoke step>`

---

# Audit Section

Append this section after implementation ships. Mark every clause
above as PASS / FAIL / MUTATED with a one-line reason.

> **Two different things happen here, and they must not be merged.**
> *Self-check* is done by whoever did the work: mark the clauses,
> fill in `observed_result`, be honest about what is `UNVERIFIED`.
> *Verify* — mandatory at critical tier — is done by a reader in a
> **clean context** who did not write the code, given only this
> contract, the relevant decisions, and the diff. The author cannot
> perform the second one; the reasoning that produced a gap is the
> reasoning that would review it. The reviewer reports and does not
> fix. Its most severe verdict is `ARCH_VIOLATED`: the code works
> and contradicts what was agreed.

## clause-by-clause results

- **intent:** PASS / FAIL / MUTATED — `<reason>`
- **affected_layers / preconditions / schema_assumptions /
  cross_module_contract / expected_outcome / confidence / escalation
  / grounding / rollback / test_plan:** same.

## MUTATED summary

| Clause | Original | Actual | Reason |
|---|---|---|---|

## MISSING / Follow-up

- `<item 1>` — `<owner / when>`

## Overall

- **Code-level:** `<PASS / FAIL>`
- **Observation-level:** `<PASS / INCOMPLETE>` — `<what's staging-
  verified, what's still UNVERIFIED>`
- **Contract completeness:** `<high / medium / low>` — `<reasons>`

---

*Template version: 2.0 — Vast Intelligence Limited, 2026.*
*Light version: [`MTM-LITE.md`](./MTM-LITE.md). Rationale per field:
[`mtm-contract-2.0-article.md`](./mtm-contract-2.0-article.md) §4.
Full specification: [`MTM-CORE.md`](./MTM-CORE.md) (written in
Traditional Chinese).*
