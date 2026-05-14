# Example 01 — Push Notification Dispatcher with Tiered UX

> Anonymised contract from a production multi-tenant SaaS application.
> Real commit hash: `9d1b42e` in the source repository.
> Trial date: 2026-05-14. First-pass commit. Zero hallucinations.

---

## intent

When a record is mutated through the multi-tenant admin path, two
audiences must learn about it: the record's owner sees a banner-level
notification ("your data was updated"), and every subscriber holding
a saved copy of that record silently re-syncs their local store. The
admin who performed the edit must not be banner-notified about their
own action.

---

## affected_layers

- `backend.entity:` no schema changes
- `backend.service:` new shared dispatcher `broadcastRecordUpdate(record, actorUserId)`; remove a duplicate private helper that did half the job for one of the two callers
- `backend.endpoint:` two existing PATCH endpoints hook the new dispatcher; no new routes
- `backend.migration:` NO
- `backend.cron / queue / push:` FCM banner for owner; FCM silent (content-available: 1, data-only) for subscribers
- `app.provider:` existing push handler routes `record_updated` → wallet refresh and `subscriber_updated` → address-book refresh
- `app.cache:` no version bump (response shape unchanged)
- `web-admin:` form-based save button already in place; no UI change
- `env / secrets:` none

---

## preconditions

- FCM end-to-end pipeline reaches the device.
  verified_by: prior TestFlight build's push-diagnostics all-green.
- One of the two callers already had a private helper that did half
  the work (subscriber fanout). The new dispatcher unifies both paths.
  verified_by: grep of the prior helper, found in service file.
- App push handler has cases for both payload types.
  status: UNKNOWN — confirm before keyboard touches code.

---

## schema_assumptions

- Record's `userId` is the owner.
  source: entity definition.
- Subscriber rows reference the source record by `recordId` and have
  their own `ownerId`. Subscriber fanout queries `DISTINCT ownerId
  WHERE recordId = ?` and excludes the record's own owner.
  source: subscriber entity comments and prior commit.
- Silent push payload type-string convention is `subscriber_updated`
  (matches the existing app router case).
  source: app push handler grep.

---

## cross_module_contract

**emit:**

- Owner banner push: `{ type: 'record_updated', recordId }` (only if
  `actorUserId !== ownerId`)
- Subscriber silent push: `{ type: 'subscriber_updated', recordId }`
  (every distinct subscriber ownerId, excluding owner)

**listen:** none

**Depends on:** App's existing foreground-push handler skipping silent
payloads from showing as SnackBars (already guarded by null-title
check).

**Others depend on this to:** Continue invoking the dispatcher on
every record mutation path. The dispatcher is now the only place
that emits these payloads; bypassing it would silently lose
notifications.

---

## expected_outcome

- Staging: admin changes an editable field on a target record. Within
  30 seconds, the record's owner's device receives a banner reading
  "Your data was updated."
  verifiable_by: manual test on staging build + push-receipt trace.
- Staging: a device holding a saved copy of the same record receives
  the silent push, refreshes its local copy automatically, no
  SnackBar.
  verifiable_by: manual test + push-receipt trace.
- Owner editing their own record: no self-banner (short-circuit on
  `actorUserId === ownerId`).
  verifiable_by: code-level inspection + manual test.

---

## confidence

- **overall:** medium-high

Low-confidence sub-items:

- Whether the app push router has a case for both payload types —
  resolved during initial grep (5 minutes).

---

## escalation

Decisions to defer to operator:

- None at design time. The handful of UX decisions (banner copy,
  silent vs. banner for subscribers) had been settled in a prior
  decision log entry referenced under `grounding`.

Halt conditions:

- Subscriber-fanout query returning > 1000 rows in staging — would
  indicate quota or batching design needed before prod.

---

## grounding

- Prior commit introducing the entity model.
- Prior decision-log entry on UX-tiered notifications (banner vs.
  silent), recorded as a separate decision before this work began.
- App push handler source, grep'd for existing case branches.

---

## rollback_plan

- code: single commit, `git revert` safe.
- schema: no migration.
- env: no new variables.

---

## test_plan

- local: backend logs show "broadcastRecordUpdate fired (N silent
  pushes)" after admin edits a record.
- staging: full flow as described in `expected_outcome`.
- prod: rely on push-diagnostics remaining green.

---

# Audit (post-implementation, 2026-05-14)

## clause-by-clause results

- **intent:** PASS — dispatcher unifies both callers; owner-banner
  short-circuit holds.
- **affected_layers:** PASS — service file diff shows the duplicate
  helper removed and the new dispatcher added.
- **preconditions:** PASS — initial grep confirmed app router cases.
- **schema_assumptions:** PASS — query uses `DISTINCT ownerId` with
  `<> selfId`.
- **cross_module_contract:** PASS — both payloads ship with the
  documented type strings.
- **expected_outcome:**
  - Owner banner: PASS at code level. **UNVERIFIED-IN-STAGING.**
  - Subscriber silent: PASS at code level. **UNVERIFIED-IN-STAGING.**
  - Self-edit no-banner: PASS at code level.
- **confidence:** PASS — the one UNKNOWN resolved cleanly.
- **escalation:** PASS — no escalation triggered.
- **grounding:** PASS — all citations verifiable in repo.
- **rollback_plan:** PASS — single-commit revert validated by
  reviewer.
- **test_plan:** UNVERIFIED — staging walkthrough deferred to a
  batch test pass at end of week.

## MUTATED summary

| Clause | Original | Actual | Reason |
|---|---|---|---|
| Silent push helper | "Use existing API" | Added new `sendSilentToUser` helper | Existing helper sent a notification block (banner); silent requires APNs `content-available: 1` with no notification block — different payload structure. |
| Scope | Single task | Merged with adjacent task | Grep revealed both adjacent tasks would touch the same dispatcher function; merging them avoided shipping an intentionally-incomplete PR. |

## MISSING / Follow-up

1. Staging end-to-end verification (batched at week's end).

## Overall

- **Code-level:** PASS.
- **Observation-level:** INCOMPLETE — three expected_outcome clauses
  staging-unverified.
- **Contract completeness:** high — two MUTATED entries, both moving
  in the right direction.
