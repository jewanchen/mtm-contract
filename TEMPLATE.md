# MTM Contract — `<task ID + one-line description>`

> Copy this file to `contracts/YYYY-MM-DD_<task>.md` and fill in
> every section before writing implementation code. Empty sections
> are not acceptable; `N/A` is a valid answer; "I don't know" must
> be written as `UNKNOWN: <reason>` so it surfaces in review.

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
- `<outcome N>`

Outcomes are the audit checklist. Every clause here must map to a
PASS / FAIL / MUTATED mark after implementation.

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

*Template version: 1.0 — Vast Intelligence Limited, 2026.*
*See `mtm-contract-technical-article.md` for rationale per field.*
