# Example 02 — Multi-Tenant Entity Update with Broadcast and Audit Email

> Anonymised contract from a production multi-tenant SaaS application.
> Real commit hash: `38420dd` in the source repository.
> Trial date: 2026-05-14. First-pass commit. Zero hallucinations.
>
> **This contract caught two silent drift bugs before implementation
> began** — fields declared in the entity but missing from the update
> DTO, and a write path with zero broadcast hook despite having
> downstream subscribers.

---

## intent

Admins (Owner or Manager role) edit tenant-level configuration data
through the dashboard. On save:

1. All tenant members with relevant subscriptions silently re-sync.
2. If the actor is *not* the Owner, the Owner receives an email
   notifying them which fields were changed and by whom.

Owner editing their own configuration does not produce a self-email.

---

## affected_layers

- `backend.entity:` two fields (`displayName`, `bannerImageUrl`) exist
  on the entity and on shared types but are missing from the update
  DTO. **The PATCH endpoint silently drops them today.** Fix the DTO.
- `backend.service:` `tenant.update()` currently has no broadcast hook
  despite downstream subscribers. Add `broadcastTenantUpdate(...)`
  in the notification service and wire `tenant.update()` to call it.
- `backend.service:` add `sendTenantInfoChangedEmail(...)` template
  in the email service.
- `backend.endpoint:` existing PATCH endpoint; DTO additions only.
- `backend.migration:` NO.
- `backend.cron / queue / push:` silent FCM fanout to active and
  suspended tenant members (resigned members deliberately excluded
  for privacy posture).
- `app.provider:` push router needs a new case for `tenant_updated`
  → refresh wallet and address-book caches.
- `app.cache:` no version bump.
- `web-admin:` profile page needs the two missing field inputs and
  one new image-upload section.
- `env / secrets:` none.

---

## preconditions

- `displayName` and `bannerImageUrl` exist on the prod schema.
  verified_by: entity declaration committed in prior milestone.
- `UpdateTenantDto extends PartialType(CreateTenantDto)` — adding the
  two fields to `Create` propagates to `Update` automatically.
  verified_by: DTO file grep.
- Email service Resend pattern is extensible.
  verified_by: prior email templates for invitation flow.
- App push router can dispatch a new payload type without breaking
  existing cases.
  status: UNKNOWN — first action: grep the foreground push handler.
- Owner identification: use the role-based admin table, not the
  legacy `adminUserId` column on the tenant entity.
  verified_by: RBAC migration commit.

---

## schema_assumptions

- The two missing fields are nullable.
  source: entity definitions.
- "Active members" for the silent push fanout: members WHERE
  tenant_id matches AND employment_status IN ('active', 'suspended');
  resigned members are deliberately excluded.
  source: prior decision-log entry on resignation privacy posture.
- "Actor is not Owner" check uses `EnterpriseAdmin.role === OWNER`,
  not the legacy `Enterprise.adminUserId` field.
  source: RBAC migration commit.
- `changedFields` for the email body is computed by diffing
  `before` vs `after` and listing only keys whose value actually
  changed (not every key in the DTO that happened to be sent).
  source: self-defined; documented to avoid spam.

---

## cross_module_contract

**emit:**

- FCM silent push: `{ type: 'tenant_updated', tenantId, changedFields, actorUserId }` to each active/suspended member.
- Email via Resend to Owner, only if `actorUserId !== ownerUserId`.

**listen:** none

**Depends on:** app's existing foreground-push handler skipping
silent payloads from showing as SnackBars (already guarded by
null-title check).

**Others depend on this to:** continue calling the broadcast hook
on every tenant-config mutation path. Bypassing the hook would
silently miss the email and the cache refresh.

---

## expected_outcome

- Owner self-edit: no self-email. Code-level short-circuit.
  verifiable_by: code inspection and manual staging walk.
- Manager edit: Owner receives email with subject "[App] Your tenant
  data was edited by an administrator," body listing actor name and
  changed-field labels, plus a link back to the dashboard.
  verifiable_by: manual staging walk + Resend dashboard log.
- All active/suspended tenant members re-sync silently within 30
  seconds.
  verifiable_by: manual on a paired-device test.
- Resigned members' devices do *not* receive the push.
  verifiable_by: backend log inspection of the fanout list.
- The two previously-dropped fields persist correctly after PATCH.
  verifiable_by: re-load the dashboard profile page after save.

---

## confidence

- **overall:** medium-high

Low-confidence sub-items:

- App push router extension point — resolved in the first 5 minutes
  by grep.
- Source of "actor name" — User entity has no name field; need to
  derive from the actor's default identity card (last+first) with a
  fallback to email. Resolved with a small inline helper.

---

## escalation

Decisions deferred to operator:

- Email subject phrasing — defer to operator.
- Whether to show actor name or actor email in the email body —
  defer to operator. (Resolved: actor name with email fallback.)
- Send synchronously or via queue — defer to operator. (Resolved:
  synchronous; Resend latency < 200ms; would not block the PATCH
  response.)

Halt conditions:

- Fanout query exceeds 1000 rows in staging — would indicate FCM
  rate-limit risk and warrant a batch strategy before prod.

---

## grounding

- Prior milestone commits introducing the entity and the RBAC table.
- Prior commit introducing the broadcast dispatcher pattern
  (example 01 of this trial).
- Prior decision-log entry on UX-tiered notifications.
- Direct user conversation, dated 2026-05-14, specifying that the
  Owner should be emailed by Manager edits and that the email should
  include the actor's name.

---

## rollback_plan

- code: single commit, `git revert` safe.
- schema: no migration.
- env: no new variables.

---

## test_plan

- local: start backend with dev Resend key; Owner edits via
  dashboard; verify no email (self-edit short-circuit).
- staging: invite a Manager, switch to Manager account, edit, verify
  Owner email arrives in inbox; verify member-device silent push
  triggers cache refresh on a paired test device.
- prod: deferred to batched staging-verification pass.

---

# Audit (post-implementation, 2026-05-14)

## clause-by-clause results

- **intent:** PASS — three expected outcomes (silent fanout, email-on-
  manager-edit, no-self-email) are all implemented and grounded in
  service-level logic.
- **affected_layers:**
  - DTO drift fix: PASS — both fields added to Create, propagate via
    PartialType.
  - Broadcast hook in `tenant.update()`: PASS.
  - Email template: PASS.
  - App push router new case: PASS.
  - Web-admin form additions: PASS.
- **preconditions:**
  - App push router extension point: UNKNOWN → RESOLVED-PASS via
    grep in first 5 minutes.
  - Owner email lookup via role-based admin table: PASS.
- **schema_assumptions:** PASS — diff-based `changedFields`
  implemented correctly; resigned members excluded.
- **cross_module_contract:** PASS — both emit paths wired and
  guarded.
- **expected_outcome:**
  - Code-level: all PASS.
  - Observation-level: UNVERIFIED-IN-STAGING for all 4 observable
    clauses.
- **confidence:** PASS — the two enumerated low-confidence items
  resolved during implementation.
- **escalation:** PASS — three deferred decisions resolved
  conversationally before implementation.
- **grounding:** PASS — verbatim user quote with date cited.
- **rollback_plan:** PASS — single-commit revert.
- **test_plan:** UNVERIFIED — batched.

## MUTATED summary

| Clause | Original | Actual | Reason |
|---|---|---|---|
| Email subject phrasing | "...was changed..." | "...was edited..." | Operator preference during escalation; "edited" is the more user-friendly term for tenant admins. |
| `changedFields` payload encoding | Implied as array | String, comma-joined | FCM data payload values must be strings (FCM platform constraint). Caught during integration; encoding documented. |

## MISSING / Follow-up

1. Staging end-to-end verification (batched).
2. **Document FCM data-payload string-only constraint in
   ARCHITECTURE.md** so future push-payload designs don't re-learn
   this through a build error.
3. **Email rate-limit dedup observation** — if a Manager saves N
   times in rapid succession, the Owner receives N emails. Watch
   in staging; if observed, add 5-minute dedup window.

## Overall

- **Code-level:** PASS — all 4 affected layers + DTO drift fix +
  preconditions hold.
- **Observation-level:** INCOMPLETE — 4 observable outcomes
  staging-unverified.
- **Contract completeness:** high — two MUTATED entries with sound
  reasons, two follow-ups recorded.

**Note on contract value:** This contract caught two silent drift
bugs before implementation began:
1. The two entity fields (`displayName`, `bannerImageUrl`) were
   declared and used by frontend code but missing from the update
   DTO. The dashboard had been silently dropping them on PATCH.
2. The `tenant.update()` service had no broadcast hook at all
   despite downstream subscribers. Tenant configuration changes
   were not reaching member devices until manual refresh.

Neither would have been caught by an unstructured prompt; both
were exposed by the discipline of writing `affected_layers` and
`schema_assumptions` honestly.
