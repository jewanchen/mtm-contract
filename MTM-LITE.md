# MTM Lite — one page, in English

**The version you can start with on Monday.** Paste this into your agent's rules file (`CLAUDE.md`, `.cursorrules`, or your project's system prompt), or just keep it open while you work.

> Using Claude Code? `/plugin marketplace add jewanchen/mtm-contract` then `/plugin install mtm@mtm-contract` installs all of this as agent behaviour, with a validator that enforces the mechanical parts. See [`plugins/mtm/`](./plugins/mtm/).

MTM is *machine to machine*: a contract is a handoff format — today usually written by a person for an agent, and by design between agents as well. The encoding changes; the fields do not.

Why it exists: agent-assisted work is not usually limited by how fast the agent writes code. It is limited by how often it writes the *wrong* code, and by what it costs to discover that afterwards. Everything below moves the cheap checks in front of the expensive generation.

Full reasoning: [`mtm-contract-2.0-article.md`](./mtm-contract-2.0-article.md). Full specification: [`MTM-CORE.md`](./MTM-CORE.md) — currently written in Traditional Chinese. Heavy template: [`TEMPLATE.md`](./TEMPLATE.md).

---

## 0. The rules block — paste this and nothing else

This is the whole method at working scale. Put it in `CLAUDE.md`, `.cursorrules`, or your system prompt. The rest of this page explains it; your agent does not need the explanation in context.

```markdown
## Contract-first workflow

Before writing implementation code, classify the task by trigger — not by
how risky it feels. Any hit promotes it; never argue a task back down.

- Typo, copy, styling, version bump, one small file → just do it.
- One module, no trigger below → write three fields first (see below).
- Crosses a module boundary / changes a shared contract / adds a
  persisted entity → also write preconditions, assumptions, outcomes.
- Auth, permissions, secrets · schema migration · tenant visibility ·
  payments · release assets · more than 5 files · the literal request
  does not map one-to-one onto the data model
  → full contract AND an independent review in a clean context before merge.

The three fields, written before any code:
1. intent — one sentence, what will be observably true when this is done.
2. escalation / candidate set — what is not mine to decide alone. If the
   request's wording could point at more than one thing in the data, list
   the candidates and ask; do not pick the likeliest one.
3. affected_layers — what I am changing, and what I am deliberately not.

While implementing: do not cross a declared boundary with a flag, toggle,
or hidden field. If I must cross it, stop and say so. Do not change
anything outside affected_layers without reporting first.

Verification: nothing is marked verified on the strength of a promise.
Record what I actually ran — command output, query result, log line,
observed value — or write UNVERIFIED. "Pending" is never a pass.
A green build is a prediction, not an observation.

When a fix does not work on the first attempt: stop changing code and
establish one fact first.
```

---

## 1. How much ceremony does this task get

Decide by **observable triggers**, not by how risky it feels. Feelings degrade exactly when you are in a hurry.

| Tier | Test | What you write |
|---|---|---|
| **Trivial** | Typo, copy, styling, version bump, one small file | Nothing |
| **Local** | One module, and none of the triggers below | **The three fields in §2** |
| **Structural** | Crosses a module boundary, changes a shared contract, adds a persisted entity | Three fields + preconditions, assumptions, outcomes ([`TEMPLATE.md`](./TEMPLATE.md)) |
| **Critical** | Auth, permissions, secrets · schema migration · tenant visibility · payments · release assets · more than *n* files (you pick *n*) · **the literal request does not map one-to-one onto your data model** | Full template **+ a clean-context review before merge (§4)** |

Any trigger hit promotes the task. **The agent may not argue it back down**, and critical never self-demotes.

The old rule of thumb — *if writing the contract takes longer than writing the code, skip the contract* — still applies, but only between Trivial and Local. A migration does not become Local because the contract felt long.

## 2. The three fields

For anything above trivial, write these before the agent writes code. Three lines each is normal.

```markdown
## intent
<One sentence. What will be observably true when this is done.
 Not "implement X" — "the user does A and sees B".>

## escalation / candidate set
<What is NOT yours to decide alone. And: if the request's wording
 could point at more than one thing in your data, list the
 candidates and make a human pick. Do not translate literally.>

## affected_layers
<What you are changing — and what you are deliberately NOT
 changing. The second half is the one that prevents collateral
 edits.>
```

If you adopt only one of the three, adopt the candidate set. A one-sentence request like "resend the invitations in bulk" routinely addresses four different populations; picking the likeliest one produces correct code aimed at the wrong target, and you find out after it exists.

## 3. The one rule

> **Nothing is marked verified on the strength of a promise.**

If a check has not run, it says so. Write what you actually saw — command output, a query result, a log line, an observed value — or write `UNVERIFIED` and carry it forward as an open item. "Pending" is a waypoint, not a pass.

This matters more with capable models than it did with weak ones. A strong agent rarely fails by leaving a field blank; it fails by filling one convincingly without doing the underlying work. `verified_by: searched the callers — no other call sites` reads identically whether the search ran or not. This rule is what makes the two look different.

Two cheap corollaries worth adopting whole:

- **A green build is a prediction, not an observation.** For anything deployed, ask the running service which commit it is on. For a new persisted entity, start the service against a real database before calling it done.
- **When round one does not fix a bug, stop changing code.** Establish one fact first. Consecutive guesses leave residue that makes later rounds worse than earlier ones.

## 4. The review that pays for itself

For anything critical: before merge, have a **fresh context** — a subagent, a second session, a colleague — read the contract, the relevant decisions, and the diff, and report whether the plan and the result agree.

Not the author, and not a continuation of the conversation that produced the code. This is not about honesty. The reasoning that produced a gap is the same reasoning that would review it; reviewing from inside your own model of the change finds spelling mistakes.

Two rules make it useful rather than decorative: **the reviewer reports and does not fix**, and its most severe verdict is not "this is broken" but **"this works and contradicts what we agreed."**

A prompt that works:

```
You are reviewing this change in a clean context. You did not write it.
Read only: the contract at <path>, the decisions it cites, and the diff.
Report whether the diff delivers what the contract promised, what it
changed outside the declared scope, and anything that works but
contradicts a recorded decision. Report only — do not fix anything.
```

## 5. A complete Local-tier contract

This is the whole thing. It took about four minutes to write and it changed the design once, at §escalation.

```markdown
# MTM Contract: filter the members list by name

## status
stage=3 | tier=local | blocked_on=[]
<!-- The specification writes this key as `blast_radius=T0/T1/T2/T3`.
     `tier=trivial|local|structural|critical` is the same thing in
     English; use either, consistently. -->


## intent
Typing in the list's search box narrows the visible rows to members
whose name contains what was typed; clearing it restores every row.

## escalation / candidate set
"Name" is ambiguous here — the row can show a card name or an
account display name, and for a meaningful share of members those
differ. Candidates: card name only / display name only / either.
Decided by the human: either.
Not mine to decide: whether email should also match. (Answer: no.)

## affected_layers
Changing: one list screen and its in-memory filter.
Deliberately not changing: the endpoint, the query, paging, or any
other list in the app.
```

Notice what is absent: no preconditions, no schema assumptions, no rollback plan, no test plan. At this tier a capable agent handles those as a matter of course. The three fields are the ones it will skip unless asked.

## 5b. The ledger line

One line per non-trivial task, appended when the task closes, in whatever file you keep for it (`docs/mtm-ledger.md` is fine). Columns: date · task · tier · did it pass on the first attempt · were there hallucination events · which field caught or missed something · what the escalation was worth.

It exists because the method improves from cases rather than from opinion — a rule only earns its place when the ledger shows the same gap twice. The specification calls this mandatory. Be warned that mandatory-in-a-document is not the same as mandatory: the authors' own ledger went unwritten for ten consecutive qualifying tasks a month after the rule was promoted, which is reported in §12 of the article and is the strongest argument in this repo for enforcing it mechanically rather than by discipline.

If you are adopting this solo and only want what pays for itself immediately, skip the ledger. Adopt it when you start wanting to change the rules, because without cases you will be changing them on vibes.

## 6. When to skip all of this

Typos, copy and styling, version bumps, a one-line fix whose cause you have already established, and exploratory work that will not produce a commit.

And the honest part: this reduces wrong turns, it does not eliminate them. First-draft contracts tend to over-engineer — expect to write a simpler second version. Being thorough can delay shipping. See §11 of the article for what got through anyway.

---

*Apache 2.0 — Vast Intelligence Limited, 2026. Attribution required in derivative works; see [`NOTICE`](./NOTICE).*
