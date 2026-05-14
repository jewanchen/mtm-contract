# Example 05 — Recovered-Entity Database (Paid Feature, v1 → v2 Redesign)

> Anonymised contract from a production multi-tenant SaaS application.
> Real commit hash: `c75d5b0` in the source repository.
> Trial date: 2026-05-14. First-pass commit. Zero hallucinations.
>
> **This is the case study from Section 5.3 of the main paper.**
> The v1 contract proposed an architecture that the user rejected
> in roughly five minutes of escalation conversation. The v2 contract
> shipped instead. The contract artifact preserves both versions; the
> deviation is auditable.

---

# v1 contract (original proposal — REJECTED at escalation step)

## v1 intent

When a tenant member resigns, their accumulated record of customer
exchanges via their tenant identity card represents tenant business
value. Paid-tier tenants can recover this list — but the value was
mediated through the member's personal NiceMeet account, so the
records currently live in the member's personal address book.

**Proposal v1:** the recovery operation *copies* selected customer
records from the resigned member's personal address book into a
chosen recipient admin's personal address book, preserving the
exchange context as metadata.

## v1 affected_layers

- `backend.entity:` add `recoveredFromUserId` + `recoveredAt`
  columns to the existing personal-contact table.
- `backend.service:` `listRecoverableContacts(...)` and
  `recoverContacts(..., recipientUserId, contactIds[])`.
- `backend.endpoint:` two new endpoints.
- `web-admin:` recovery section on the resigned-member detail page
  with a recipient-picker dropdown.

## v1 escalation questions

1. Schema boundary: add two tracking columns to the existing
   contact table, or use the freeform `notes` field for
   provenance?
2. Repeat-recovery protection: if Owner has already routed a
   member's customers to Manager A, can they also route the same
   set to Manager B?
3. Recipient scope: only admins, or admins plus active members?
4. Free-tier paywall: hide section entirely, or show it disabled
   with an upgrade prompt?

---

# v2 contract (post-escalation, IMPLEMENTED)

## v2 intent

When a tenant member resigns, paid-tier admins can snapshot the
customers that member exchanged through their tenant identity card
into a **tenant-owned recovered-customers store**. The store is
queryable from a new dashboard page and exportable as CSV. **No
recovered data flows into anyone's personal address book.** Free-tier
admins see the section but with a disabled CTA and an upgrade
tooltip.

## v2 affected_layers

- `backend.entity:` new entity `TenantRecoveredCustomer` —
  enterprise-owned table with a frozen-at-recovery-time snapshot of
  the customer's identity, plus exchange context (event, location,
  timestamp) and recovery metadata (recovered-by-user, recovered-at).
- `backend.migration:` YES — new table with a unique constraint on
  `(tenantId, originalExchangeId)` to defend against double-recovery
  races.
- `backend.service:` three methods —
  `listRecoverableCustomers(...)` (preview, free-tier accessible to
  show the upgrade tooltip), `recoverCustomers(...)` (paid-tier
  gated), `listRecoveredCustomers(...)` (paged listing with keyword
  and source-member filters).
- `backend.endpoint:` three new routes, one supporting `?format=csv`
  for direct CSV download.
- `backend.paywall:` the recovery endpoint throws on free-tier
  callers; the listing and preview endpoints remain accessible to
  drive the upgrade tooltip.
- `web-admin:` recovery section on the resigned-member detail page
  (visible when `employmentStatus === 'resigned'`, with the button
  disabled and a "Upgrade to Premium" tooltip for free-tier); new
  page `/dashboard/customers` with search + source filter +
  download CSV; sidebar nav entry.

## v2 preconditions

- Exchange entity records the sender's card and the recipient
  member, enabling the "tenant-card exchanges only" filter.
  verified_by: entity definition.
- Personal contact table can be queried for the snapshot at recovery
  time (the member's "as I saw them at exchange" view).
  verified_by: contact entity definition.
- Tenant plan field can be checked for the paid-tier gate.
  verified_by: tenant entity field.
- Resigned status is shippable.
  verified_by: example 03 commit.

## v2 schema_assumptions

- Separate table, not extension of contact table. **Rationale: a
  user's personal contact table should not contain
  tenant-owned data**; mixing them creates a confusing UX surface
  where the admin's personal contacts include other people's
  customers.
  source: user-led redesign during escalation.
- "Tenant card" definition: a card whose `tenantId` matches the
  enterprise's, irrespective of the member's current
  `employmentStatus`.
- Same exchange recovered twice: prevented by the unique constraint
  on `(tenantId, originalExchangeId)`. A 23505 PostgreSQL error
  during a race-condition retry is silently skipped.
- Customer snapshot is read from the resigned member's contact
  row for that customer (the "as I saw them at exchange" view); if
  the contact row was deleted, a future enhancement may fall back
  to the customer's default card.
- A customer whose user account is deleted is *not* automatically
  excluded; their snapshot remains valuable for the tenant. This
  is a known edge case for future polish.

## v2 cross_module_contract

**emit:** none (storage-only operation).

**listen:** none.

**Depends on:** the plan field being set correctly to gate the
write endpoint; the resigned-status precondition being live so the
UI section becomes visible.

**Others depend on this to:** preserve the recovered records as
read-only snapshots; subsequent member-side card edits do *not*
propagate into recovered records.

## v2 expected_outcome

- Paid-tier admin views a resigned member's detail page and sees
  a recovery section with a count of recoverable customers and a
  preview of the first 10.
  verifiable_by: manual test on a paid-tier tenant with prior
  exchanges.
- Free-tier admin sees the same section but with the button
  disabled and a "Upgrade to Premium" tooltip; the upgrade prompt
  doubles as advertising for the feature.
  verifiable_by: manual test on a free-tier tenant.
- Clicking the button on paid-tier writes N rows to the
  recovered-customers table.
  verifiable_by: manual test + DB inspection.
- The new `/dashboard/customers` page lists all recovered rows
  with keyword search, source-member filter, and CSV download.
  verifiable_by: manual test + downloaded CSV inspection.

## v2 confidence

- **overall:** medium-high

Low-confidence sub-items:

- CSV download UX (`fetch` + blob trick) — confirmed during
  implementation.

## v2 escalation (all resolved before implementation)

Decisions deferred to operator:

- **Schema boundary** — resolved: dedicated entity, not extension
  of contact table.
- **Repeat-recovery semantics** — resolved: not relevant under
  the dedicated-table design; the unique constraint enforces
  idempotency naturally.
- **Recipient routing** — resolved: not relevant; recovered data
  lives in the tenant-owned store, not anyone's personal address
  book.
- **Free-tier paywall** — resolved: show section with disabled CTA
  and upgrade tooltip. This is a deliberate inversion of the
  general "do not nag" policy used elsewhere; this *is* the
  premium feature, so the upgrade prompt is the message.

Halt conditions:

- JOIN-driven query for the preview list exceeds 200ms on a
  populated tenant in staging.
- Snapshot fields miss a critical customer attribute, breaking
  CSV completeness.

## v2 grounding

- Prior commit introducing the `Exchange` entity.
- Prior commits introducing the personal contact table.
- Prior commit introducing the resigned-status feature
  (example 03).
- Direct user conversation, dated 2026-05-14, redesigning the
  routing model from "personal-inbox copy" to "tenant-owned
  store."

## v2 rollback_plan

- code: single commit, `git revert` safe.
- schema: forward-fix migration; `DROP TABLE recovered_customers` is
  safe if rolled back before users have written data.
- env: no new variables.

## v2 test_plan

- local: insert fake exchanges via a resigned member's tenant card;
  verify the preview endpoint returns the expected list; trigger
  the write; verify the table has N rows; trigger again; verify
  the unique constraint prevents duplicates.
- staging: full flow on a paid-tier test tenant.
- prod: deferred.

---

# Audit (post-implementation, 2026-05-14)

## clause-by-clause results (v2 only)

- **intent:** PASS — dedicated tenant-owned store; dashboard query
  page; CSV download.
- **affected_layers:** PASS — entity + migration + 3 service methods
  + 3 endpoints + 2 web-admin pages + sidebar nav.
- **preconditions:** PASS.
- **schema_assumptions:** PASS — separate table; unique constraint
  enforces idempotency; snapshot from member's contact row with
  `relations: ['phones']` for phone number.
- **cross_module_contract:** PASS.
- **expected_outcome:**
  - Paid-tier and free-tier UI states: PASS at code level.
  - Recovery write: PASS at code level.
  - Dashboard customer-database page: PASS at code level.
  - All four observable outcomes UNVERIFIED-IN-STAGING (the trial's
    persistent gap).
- **confidence:** PASS.
- **escalation:** PASS — four items resolved at the design step.
- **grounding:** PASS.
- **rollback_plan:** PASS.
- **test_plan:** UNVERIFIED — batched.

## MUTATED summary

| Clause | Original | Actual | Reason |
|---|---|---|---|
| Routing model | v1: personal-inbox copy | v2: tenant-owned store | User-led redesign during escalation; v1 would have polluted an admin's personal address book with the resigned member's customers, an unacceptable UX outcome. |
| Schema | v1: extend contact table | v2: new dedicated entity | Direct consequence of the routing-model change; the new entity is the source of truth for tenant-owned recovered data. |
| Paywall posture | v1 considered "hide section entirely" | v2: visible with disabled CTA and upgrade tooltip | Deliberate inversion of the general "do not nag" rule. This is the premium feature; the upgrade prompt is part of the value proposition. |
| CSV download mechanism | Not specified in v1 | `fetch` + blob trick via the API helper, not the JSON wrapper | The repository's API wrapper is JSON-only; CSV requires a raw fetch. Caught during implementation. |

## MISSING / Follow-up

1. Staging end-to-end verification on a paid-tier test tenant.
2. The "customer whose user account is deleted" edge case is not
   actively filtered; documented as a future polish item.
3. The dashboard customer list is paginated only by client; if
   tenants accumulate thousands of recovered rows, server-side
   pagination becomes necessary.

## Overall

- **Code-level:** PASS — migration + 3 endpoints + 2 frontend pages
  + sidebar nav + paywall guard.
- **Observation-level:** INCOMPLETE — paid-tier toggle and staging
  walkthrough not yet done.
- **Contract completeness:** medium — v1 was inadequate and required
  redesign during escalation. **This is the success case for the
  methodology:** the redesign cost five minutes of conversation and
  one rewrite of the contract, not a production deploy plus a
  migration to extract personally-owned rows back into a shared
  store.

---

## Reflection: why this case justifies the contract

The v1 contract was *plausible*. The recipient-routing model is a
reasonable interpretation of "recover the customers a former
employee handled." It would have shipped without errors.

It would have been *wrong* — wrong in a way that becomes visible
only when one imagines a Manager taking over the resigned
member's accounts, and discovering that their personal address book
is now polluted with the former employee's customer history,
including customers that have since been migrated to other team
members.

The contract surfaced the routing decision as an explicit escalation
question. The user, reading the question, recognised the issue
within five minutes. The redesign cost a paragraph rewrite, not a
production rollback.

This is the working case. The contract is worth keeping precisely
*because* it enables this kind of cheap correction at the design
step, where corrections cost paragraphs instead of migrations.
