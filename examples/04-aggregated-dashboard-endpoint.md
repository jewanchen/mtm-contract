# Example 04 — Aggregated Dashboard Endpoint (N+1 to Single Endpoint)

> Anonymised contract from a production multi-tenant SaaS application.
> Real commit hash: `3ed38cd` in the source repository.
> Trial date: 2026-05-14. First-pass commit. One type drift caught
> by the type checker pre-commit (counted as zero hallucinations).

---

## intent

The tenant-admin dashboard home page is currently slow and noisy:
four separate HTTP requests, plus an N+1 loop fetching scheduled
changes per-member (capped at 20 members in the loop, with the
remaining never queried). Replace with a single aggregated endpoint
returning all stats in one shot, with all backend queries running
in parallel.

Additionally surface stats the previous page did not — derived
employee-status distribution (active / suspended / resigned),
quota usage, plan status, verification status, pending action
items.

---

## affected_layers

- `backend.entity:` no schema changes.
- `backend.service:` add `getDashboardSnapshot(tenantId, userId)`
  returning a single aggregated object; `getUpcomingSchedules(...)`
  for a separate full-list page; `getVerificationStatus(...)` as a
  stub endpoint for a future paid-feature integration.
- `backend.endpoint:` three new `GET` routes; existing routes left
  in place.
- `backend.migration:` NO.
- `backend.cron / queue / push:` none.
- `app:` not affected.
- `web-admin:` `/dashboard` page rewritten to use the single
  aggregated endpoint; new `/dashboard/upcoming-schedules` page
  for the full schedule list; the import and invite pages add a
  paywall ("at quota") guard reading the new dashboard endpoint.
- `env / secrets:` none.

---

## preconditions

- The existing per-page queries (members, invitations, admins,
  admin-invitations) are stable and can be reused as ground-truth
  references during testing.
  verified_by: grep.
- The three-state employment status enum is live in production
  (added in example 03).
  verified_by: entity declaration.
- Plan and quota fields exist on the tenant entity.
  verified_by: entity grep.
- The verification request entity is registered with the ORM but
  has no service yet — the new stub endpoint will be the first
  service to use it.
  verified_by: grep.

---

## schema_assumptions

- Employee distribution counts use a single `GROUP BY` query, not
  a loop of single-status counts.
  source: standard SQL.
- Quota usage counts `active + suspended`; `resigned` members do
  not consume quota.
  source: prior decision-log on quota semantics.
- "Expiring soon" plan threshold is 30 days from now, computed
  client-side to avoid coupling backend to a UI threshold.
  source: self-defined.
- "Failed invitation" includes both invitations with
  `status = expired` and invitations with `status = pending` whose
  `expiresAt` has passed.
  source: prior invitation entity.

---

## cross_module_contract

**emit:** none (queries-only endpoint).

**listen:** none.

**Depends on:** previous tasks' write paths producing rows of the
right shape (the three-state employment enum, the plan/quota
fields, the verification entity).

**Others depend on this to:** continue to surface plan and quota
state in a way that the import and invite pages can read.
Specifically, the "at quota" boolean and quota usage count must
remain on the response for the paywall to work.

---

## expected_outcome

- A single HTTP request returns all stats; the dashboard first-paint
  is < 1 second on staging.
  verifiable_by: Chrome devtools Network panel.
- Employee distribution shows three counts (active / suspended /
  resigned) and a quota fraction (quota used / quota max).
  verifiable_by: manual inspection.
- At quota (used == max for a tenant on the free plan), the import
  page locks (full page guard with a CTA) and the invite "+" button
  is disabled.
  verifiable_by: manual test at 50/50.
- Verification status section renders either "verified," "pending,"
  "needs revision," or "not submitted" based on the stub endpoint.
  verifiable_by: manual test on tenants with each status.

---

## confidence

- **overall:** medium-high

Low-confidence sub-items:

- The verification entity's `submittedAt` column may be named
  `createdAt` from the prior schema. Resolve by reading the entity
  source before writing the query.

---

## escalation

Decisions deferred to operator (resolved 2026-05-14):

- Single endpoint vs. multiple endpoints — chose single endpoint.
- Free-tier quota warning policy — chose "warn only at hard cap;
  do not nag at soft thresholds."
- Stub the verification status endpoint now (for forward
  compatibility) vs. defer entirely — chose stub now.
- "Upcoming changes" presentation — chose single top-N list with
  a "see all" link to a dedicated page.

Halt conditions:

- Single-endpoint query latency > 50ms in staging on a populated
  tenant — would indicate N+1 leak in the new query.

---

## grounding

- Prior milestone commits introducing the entities, the RBAC table,
  and the three-state employment enum.
- Direct user conversation, dated 2026-05-14, resolving four
  escalation items.

---

## rollback_plan

- code: single commit, `git revert` safe. New endpoint and pages
  are additive.
- schema: no migration.
- env: no new variables.

---

## test_plan

- local: backend logs show a small constant number of SQL queries
  per dashboard load (no N+1 leak).
- staging: full flow as described in `expected_outcome`.
- prod: deferred.

---

# Audit (post-implementation, 2026-05-14)

## clause-by-clause results

- **intent:** PASS — single aggregated endpoint replaces 4-query
  page + N+1 schedule loop.
- **affected_layers:**
  - Backend service: PASS — `Promise.all` runs queries in parallel;
    `GROUP BY` for distribution counts.
  - Backend endpoint: PASS — three new `Get` routes; existing
    routes unchanged.
  - Web-admin dashboard rewrite: PASS — one fetch, new card
    components for plan / verification / quota / action items.
  - Web-admin upcoming-schedules page: PASS — new dedicated page
    with `Promise.all` fetch.
  - Web-admin paywall on import + invite: PASS — both pages query
    the dashboard endpoint and guard at quota.
- **preconditions:** all PASS.
- **schema_assumptions:** PASS — quota counts `active + suspended`;
  resigned excluded.
- **cross_module_contract:** PASS — `atQuota` and quota fraction
  surface on the response and are read by the paywall pages.
- **expected_outcome:**
  - Code-level: all PASS.
  - Observation-level: UNVERIFIED-IN-STAGING.
- **confidence:** PASS — the one type drift (`createdAt` vs.
  `submittedAt`) was caught by the type checker within seconds and
  fixed inline. Zero hallucination at commit.
- **escalation:** PASS — all four items resolved.
- **grounding:** PASS.
- **rollback_plan:** PASS.
- **test_plan:** UNVERIFIED — batched.

## MUTATED summary

| Clause | Original | Actual | Reason |
|---|---|---|---|
| Endpoints | "Single dashboard endpoint" | Three endpoints (dashboard + upcoming-schedules + verification-status) | The "see all" link from the dashboard needs its own listing endpoint; the verification status stub serves a future paid feature integration. Both surfaced during the user's resolution of escalation item 4. |
| Free-tier paywall scope | Banner-only on the dashboard | Banner + functional locks on the import page (full-page guard) and the invite page (disabled button) | Without functional locks, the banner would be advisory only; the user explicitly required hard locks at the over-quota boundary. |

## MISSING / Follow-up

1. Staging end-to-end timing measurement (the < 1 second claim).
2. Once the verification feature ships (later milestone), the stub
   endpoint should grow into a full status endpoint without
   breaking the dashboard frontend that already consumes it.

## Overall

- **Code-level:** PASS — N+1 eliminated; `GROUP BY` + `Promise.all`
  produce a single-shot query pattern.
- **Observation-level:** INCOMPLETE — staging timing unverified.
- **Contract completeness:** high — escalation handled four open
  questions before implementation; two MUTATEDs were precising
  rather than drifting.

**Note on type drift:** During implementation, the agent wrote
`order: { createdAt: 'DESC' }` for the verification entity. The
actual column is `submittedAt` (declared with `@CreateDateColumn`).
The type checker reported the mismatch within seconds; the fix
was four characters. We count this as zero hallucinations: nothing
reached commit. This is the working failure mode — caught at the
cheapest possible point — that contract-level discipline aims for.
