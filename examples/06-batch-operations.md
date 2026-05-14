# Example 06 — Batch Operations Across an Entity List

> Anonymised contract from a production multi-tenant SaaS application.
> Real commit hash: `f780937` in the source repository.
> Trial date: 2026-05-14. First-pass commit. Zero hallucinations.

---

## intent

Tenant admins can perform three batch actions from the existing
selection panels in the member-list and invitation-list pages:

1. **Bulk department change** — assign N selected members to a new
   department string.
2. **Bulk resign** — mark N selected members as resigned in one
   atomic-feeling operation.
3. **Bulk resend invitation** — pick N pending or expired
   invitations and re-send the invitation email; for expired ones,
   issue a new token first.

---

## affected_layers

- `backend.entity:` no schema changes.
- `backend.service:` four new methods —
  `bulkUpdateDepartment(...)`, `bulkResign(...)`,
  `resendInvitation(...)` (single, used internally by bulk),
  `bulkResendInvitations(...)` (wraps single, returns counts).
- `backend.endpoint:` three new POST routes (department / resign /
  bulk-resend), each taking an array of IDs and any operation
  parameters.
- `backend.migration:` NO.
- `backend.cron / queue / push:` per-record dispatcher fanout reused
  from the existing pattern (each affected record fires a push).
- `app:` not affected (push payload types unchanged).
- `app.cache:` no version bump.
- `web-admin:`
  - Member-list page: existing selection panel gets two new buttons
    ("bulk department," "bulk resign") with their own modals.
  - Invitation-list page: new checkbox column (limited to pending /
    expired rows), bulk action panel with "resend invitations"
    button.
- `env / secrets:` none.

---

## preconditions

- The existing selection-panel pattern (`selectedIds: Set<string>`)
  already drives a single-action batch ("deactivate selected").
  verified_by: source grep on the member-list page.
- The single-record resign service exists, with a no-op
  short-circuit for already-resigned records (added in example 03).
  verified_by: prior commit.
- The dispatcher used to fan out per-record notifications can
  handle 30+ rapid sequential calls without backpressure issues.
  status: UNKNOWN — fire-and-forget pattern; if observed in staging
  to fail, batch the dispatch.
- An invitation-resend mechanism exists in some form
  (regenerating tokens for expired invitations).
  status: UNKNOWN — confirm during contract phase.

---

## schema_assumptions

- Department is a freeform string. Empty values render as a
  placeholder. Comparison for "skipped because already set" uses
  null-coalesced empty-string equality.
  source: card entity field comments.
- Bulk-resign of already-resigned members is no-op-skipped at the
  service level. Bulk count returns
  `{ resigned: N, skipped: M }` separately so the UI can show both.
  source: prior commit's no-op short-circuit; extend with a count.
- "Resendable" invitation: `status = pending` or `status = expired`.
  An accepted or revoked invitation is rejected at both the UI
  level (checkbox does not render) and at the backend (throws on
  the row).
  source: invitation entity status enum.
- Bulk department change only updates the `department` field, not
  any related fields (e.g. `departmentEn`). Admin who wants to
  change the English version too does so separately.
  source: self-defined for simplicity.

---

## cross_module_contract

**emit:** per-record dispatcher calls for each affected record on
department + resign (reuses the dispatcher from example 01); email
fanout for each resend (reuses the email service template).

**listen:** none.

**Depends on:** the dispatcher, the email service, and the single-
record resign helper (no-op short-circuit semantics carry over).

**Others depend on this to:** continue routing single-record edits
through the same dispatcher when a bulk operation is reduced to a
single record.

---

## expected_outcome

- Admin selects 5 members, opens bulk-department modal, enters
  "Marketing," confirms. 5 records have their `department` updated;
  5 member devices receive their owner-banner notification; 5 sets
  of subscriber devices silent-sync.
  verifiable_by: manual test on paired devices.
- Admin selects 3 members, opens bulk-resign modal listing the
  names. After confirmation, 3 records are resigned, quota is
  released by 3.
  verifiable_by: manual test + dashboard quota count.
- Admin selects 1 already-resigned and 1 active member, bulk-
  resigns. Only the active one fires a push; the already-resigned
  one is silently skipped. The return count is `{ resigned: 1,
  skipped: 1 }`.
  verifiable_by: manual test + backend log.
- Admin selects N pending + M expired invitations, resends. Pending
  invitations re-send with their existing URL; expired invitations
  get a new token, a new 30-day expiration, and the status is
  flipped back to pending.
  verifiable_by: manual test + Resend dashboard inspection.

---

## confidence

- **overall:** high

Low-confidence sub-items:

- Repeat-press protection: a fast double-click on "Confirm" could
  fire two bulk operations. Mitigated by the no-op short-circuit
  and (on the UI side) by disabling the confirm button while the
  operation is in flight.

---

## escalation

Decisions deferred to operator (resolved 2026-05-14):

- **"Bulk send invitation" semantics** — the user mental model
  included four candidate populations (never-invited, pending-
  not-yet-accepted, expired, accepted-then-deleted-card). After
  walking through all four, the scope was narrowed to pending and
  expired only. The "accepted-then-deleted-card" case becomes a
  separate single-flow on the member detail page, not part of this
  task.
- **Department change UI** — chose freeform text input over
  dropdown of existing departments, to avoid building a separate
  department-management feature.
- **Bulk-resign confirmation UX** — modal lists the names of the
  selected members and the consequence ("released from quota,
  reactivation available later"); single confirm button, no
  type-the-word safeguard.
- **Bulk operation size cap** — no cap.

Halt conditions:

- Staging observation of the per-record dispatcher fanout hitting
  rate limits during a 30+ record bulk resign — would prompt a
  batch-dispatch redesign.

---

## grounding

- Prior commits introducing the dispatcher, the single-record
  resign service with no-op short-circuit, and the email service.
- Prior decision-log on UX-tiered notifications.
- Direct user conversation, dated 2026-05-14, resolving the four
  escalation items.

---

## rollback_plan

- code: single commit, `git revert` safe. All four service methods
  + three endpoints + two web-admin page modifications are
  additive.
- schema: no migration.
- env: no new variables.

---

## test_plan

- local: backend logs show N dispatcher calls per N-record bulk
  operation; DB reflects the new field values; invitation tokens
  refresh as expected for expired rows.
- staging: full flow on a populated test tenant with paired
  devices.
- prod: deferred.

---

# Audit (post-implementation, 2026-05-14)

## clause-by-clause results

- **intent:** PASS — three batch flows ship together.
- **affected_layers:** PASS — four service methods, three POST
  endpoints, two web-admin pages with modals.
- **preconditions:**
  - Selection panel pattern reuse: PASS.
  - Single-record resign no-op short-circuit reuse: PASS.
  - Dispatcher backpressure: UNKNOWN → not observed in staging;
    listed as follow-up.
  - Invitation resend mechanism existed: confirmed; refactored
    into a shared helper.
- **schema_assumptions:** PASS.
- **cross_module_contract:** PASS — per-record dispatcher reuse
  preserves single-record semantics.
- **expected_outcome:**
  - Code-level: all PASS.
  - Observation-level: UNVERIFIED-IN-STAGING.
- **confidence:** PASS — repeat-press protection added at the UI
  level via in-flight disabling.
- **escalation:** PASS — four items resolved before implementation.
- **grounding:** PASS.
- **rollback_plan:** PASS.
- **test_plan:** UNVERIFIED — batched.

## MUTATED summary

| Clause | Original | Actual | Reason |
|---|---|---|---|
| Department modal UI | "Use system prompt() dialog" | Custom modal with input, Enter-to-submit, and a cancel button | `prompt()` is visually inconsistent with the rest of the dashboard and lacks accessibility. The custom modal took 15 lines to implement. |
| Bulk-resign confirmation copy | Warning about "grey check visibility" | "Released from quota, reactivation available later" | The original wording was technical jargon; the user simplified to plain-language reassurance to reduce admin hesitation around an irreversible-looking action that is in fact reversible. |
| Bulk-resend result feedback | Not specified | Alert showing "{ resent: N, skipped: M, errors: E }" | Without a feedback alert the admin has no visibility into rows that failed silently (e.g., an accepted invitation included by stale UI state). |

## MISSING / Follow-up

1. Staging end-to-end verification, including a 30+ record bulk
   resign to observe FCM rate-limit behaviour.
2. The "accepted-then-deleted-card" re-invite case (single-flow on
   the member detail page, deferred from this scope).
3. Modal focus-trap and ESC-to-close polish (functional but lacks
   keyboard accessibility hygiene).

## Overall

- **Code-level:** PASS — all four service methods + three endpoints
  + two frontend pages with modals.
- **Observation-level:** INCOMPLETE — paired-device + FCM-rate
  staging walk not yet done.
- **Contract completeness:** high — three MUTATEDs are UI
  precision details, not scope drift. The escalation step resolved
  the largest scope question ("which populations count as 'bulk
  send invitation'?") before implementation, avoiding a
  reasonable-but-wrong reading of the user's intent.
