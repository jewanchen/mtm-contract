# Example 03 — Status Lifecycle Transitions with Derived UI State

> Anonymised contract from a production multi-tenant SaaS application.
> Real commit hash: `88df1e5` in the source repository.
> Trial date: 2026-05-14. First-pass commit. Zero hallucinations.

---

## intent

Tenant admins can transition a member's employment status across
three states (`active` ↔ `suspended` ↔ `resigned`) from the
admin dashboard. Within 30 seconds of the transition:

- The member's mobile wallet renders the member's tenant identity
  card with a state-appropriate visual cue (verified-blue for
  active+paid, grey for suspended/resigned, unmarked for active+free).
- All subscribers holding a saved copy of the member's card
  re-sync silently.

Suspended and resigned both render visually as grey; the backend
preserves the distinction, but the user-facing layer does not expose
admin terminology.

---

## affected_layers

- `backend.entity:` no schema changes (the three-state enum already
  exists in the table).
- `backend.service:` add three public methods (`suspendMember`,
  `resignMember`, `reactivateMember`) sharing one private helper
  `setEmploymentStatus(...)`. The helper short-circuits no-op
  transitions and dispatches `broadcastRecordUpdate(...)` on every
  state change.
- `backend.endpoint:` three new PATCH routes under
  `/tenants/:id/members/:memberId/{suspend,resign,reactivate}`. RBAC:
  any tenant admin (Owner or Manager).
- `backend.migration:` NO.
- `backend.cron / queue / push:` reuse the existing dispatcher from
  example 01.
- `app.provider:` no new push payload type; existing cases handle
  state changes through the universal `record_updated` and
  `subscriber_updated` paths.
- `app.cache:` no version bump. New `walletSection` derived field is
  optional with default `'active'`; old cached records remain valid.
- `app.model:` add a `walletSection` field to the mobile record model
  (`'active' | 'archived'`). Default `'active'` makes old cached
  rows safe to deserialise.
- `app.screen:` two visual layers render the badge — the card body
  component and a legacy card visualizer. Both must read
  `walletSection`.
- `web-admin:` member detail page gets a status chip (active /
  suspended / resigned) and three transition buttons with
  state-aware disabled rules.
- `env / secrets:` none.

---

## preconditions

- The three-state enum is already in production.
  verified_by: prior milestone migration commit.
- The record hydrator (`deriveRecordMeta`) already derives
  `walletSection` from `(enterpriseStatus + employmentStatus)`.
  verified_by: hydrator source, grep'd.
- The push dispatcher pattern is shippable.
  verified_by: example 01 commit, deployed.
- RBAC `requireAdmin` helper handles both Owner and Manager.
  verified_by: prior commit.
- App's badge renderer currently handles only the verified case;
  the model has no `walletSection` field yet.
  verified_by: grep — surfaced a missing model field.

---

## schema_assumptions

- Three states are mutually exclusive; transitions are idempotent
  by way of the no-op short-circuit in the helper.
  source: enum definition + helper design.
- `walletSection` is derived: `archived` ⇔ tenant is non-active OR
  member is non-active. The derivation lives in the hydrator and is
  not stored on the record.
  source: hydrator source.
- Reactivation does not write a state-change history row. Audit-log
  semantics are a paid-feature concern handled in a separate task.
  source: deliberate scope cut for this task.

---

## cross_module_contract

**emit:** reuse `broadcastRecordUpdate(record, actorUserId)` from
the existing dispatcher (example 01). State changes trigger the
same payloads as field-level edits; the receiving app distinguishes
state from data by re-fetching the hydrated record.

**listen:** none

**Depends on:** the existing dispatcher and the existing app push
router. No new payload types are introduced.

**Others depend on this to:** Exchange and share paths must reject
records with `walletSection === 'archived'`. This is already
enforced in the hydrator's `isExchangeable` derivation; this task
does not duplicate that guard.

---

## expected_outcome

- Staging: Owner suspends a member. Member's mobile wallet shows
  the card with a grey badge instead of blue. Subscribers' devices
  silently re-sync.
  verifiable_by: paired-device manual test.
- Staging: Owner resigns then reactivates the same member. Badge
  cycles blue → grey → blue (or grey → grey if tenant is free
  plan).
  verifiable_by: paired-device manual test.
- Suspended and resigned render visually identically; the backend
  preserves the distinction (admin sees it on the dashboard chip).
  verifiable_by: DB-level inspection vs. UI inspection.
- Attempting to exchange a card whose member is suspended or
  resigned: rejected.
  verifiable_by: end-to-end manual test of the exchange flow.

---

## confidence

- **overall:** high

Low-confidence sub-items:

- Whether resigning should banner-notify the member personally
  (vs. silently letting wallet update on its own).
- Whether suspended and resigned should render visually
  differently.

Both deferred to operator (see escalation).

---

## escalation

Decisions deferred to operator (resolved 2026-05-14):

- **Resignation notification policy:** use the same banner copy as
  regular edits ("Your data was updated"). Do not expose admin
  terminology ("you were resigned") to the member.
- **Visual differentiation:** suspended and resigned both render as
  grey badge. Backend preserves the enum distinction.

Halt conditions:

- Adding `walletSection` to the model breaks deserialisation of
  old cached records on a real device. (Mitigated by default-value
  pattern; verify on first build.)

---

## grounding

- Prior commits for the entity, the dispatcher, and the hydrator.
- Prior decision-log entry on notification tiering (referenced from
  example 02).
- Direct user conversation, dated 2026-05-14, resolving the two
  escalation items.

---

## rollback_plan

- code: single commit, `git revert` safe. Three endpoints + one
  helper + UI changes are all additive.
- schema: no migration.
- env: no new variables.

---

## test_plan

- local: backend log shows `broadcastRecordUpdate fired` and DB
  reflects the new `employmentStatus` value.
- staging: full flow as described in `expected_outcome` on paired
  devices; tenant-admin dashboard chip cycles correctly.
- prod: deferred to batched staging-verification pass.

---

# Audit (post-implementation, 2026-05-14)

## clause-by-clause results

- **intent:** PASS — three endpoints + helper + dispatcher hook
  ship together.
- **affected_layers:**
  - Backend service & endpoints: PASS — RBAC via existing helper,
    JWT-guarded.
  - Backend migration: PASS — zero migrations.
  - Push: PASS — dispatcher reuse, no new payload type.
  - App provider: PASS — no provider changes needed.
  - App cache: PASS — default-value pattern preserves old caches.
  - App model: PASS — `walletSection` field added with safe default.
  - App screen: PASS — two visual layers updated (the card body
    component and the legacy card visualizer). **The legacy
    visualizer was missed in the original `affected_layers` and
    surfaced during a verification grep.** See MUTATED.
  - Web-admin: PASS — chip + three buttons with state-aware
    disabled rules.
- **preconditions:** all PASS via grep + entity check.
- **schema_assumptions:** PASS — no-op short-circuit holds; visual
  unification preserves enum distinction in the backend.
- **cross_module_contract:** PASS — dispatcher reuse.
- **expected_outcome:**
  - Code-level: all PASS.
  - Observation-level: UNVERIFIED-IN-STAGING.
- **confidence:** PASS.
- **escalation:** PASS — both items resolved before implementation.
- **grounding:** PASS.
- **rollback_plan:** PASS — single-commit revert.
- **test_plan:** UNVERIFIED — batched.

## MUTATED summary

| Clause | Original | Actual | Reason |
|---|---|---|---|
| `app.screen` scope | One visual component (the new card body) | Both the new component and a legacy card visualizer | grep during implementation found two render paths for the verified badge; missing the second would have shipped a half-grey visual on the legacy widget. |
| Status-transition UI disabled rules | Not specified | "active → reactivate is disabled" added | UI consistency — backend short-circuits no-ops, but disabling no-op buttons in the UI prevents the user from initiating a confirmed action that does nothing. |

## MISSING / Follow-up

1. Staging end-to-end verification on paired devices.
2. Status-change audit log not written yet (deferred to the
   paid-feature audit log task).

## Overall

- **Code-level:** PASS — all affected layers + preconditions +
  cross-module contract align.
- **Observation-level:** INCOMPLETE — staging not yet verified.
- **Contract completeness:** high — one MUTATED for a missed render
  path, one MUTATED for a UI polish detail. No contract drift.
