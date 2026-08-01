---
name: mtm
description: Contract-first discipline for delegating implementation to an agent — classify the task by observable triggers, ground your assumptions before generating any code, never mark a check passed on a promise, and get a clean-context review before merging risky work. Use when starting a non-trivial implementation task (several files, a schema change, auth or permissions, payments, tenant visibility), when a fix has already failed once, when a request's wording may not map one-to-one onto the data model, or when the user asks for MTM.
---

# MTM — put the cheap checks before the expensive generation

You are implementing work on someone's behalf. The expensive failure is not writing code slowly; it is writing the *wrong* code and finding out after something depends on it. This skill reorders the work so the cheap checks happen first.

Specification: `MTM-CORE.md` at <https://github.com/jewanchen/mtm-contract>. Reasoning: the [2.0 article](https://github.com/jewanchen/mtm-contract/blob/main/mtm-contract-2.0-article.md).

**Keep the machinery internal.** Never narrate phases, tiers, or field names at the user. Tell them: what you are doing, why, roughly how long, what you need from them. Everything below is how you work, not what you say.

**Two rules that hold everywhere.** Every field gets an answer — `N/A` is legitimate, "I don't know" is written `UNKNOWN: <why>` so it surfaces, and blank is not an answer. And the thing the user named as the point of the work is a first-class deliverable: if they said "it has to sound like a real bass", a synthesised placeholder is a failure even if the architecture is perfect. If it genuinely must be deferred, say so in the confirmation as the headline, never as a silent TODO.

---

## 1. Classify first — by trigger, not by feeling

Any hit promotes the task. **Never argue one back down.**

| Tier | Test | What you do |
|---|---|---|
| **Trivial** | Typo, copy, styling, version bump, one small file | Just do it |
| **Local** | One module, no trigger below | The three fields in §3 |
| **Structural** | Crosses a module boundary · changes a contract other code relies on · adds a persisted entity | Full contract, plus §2 grounding and the escalation conversation |
| **Critical** | Auth, permissions, secrets · schema migration · tenant or customer visibility · payments · release assets · **spans two or more domains** · more than *N* files (see below) · **the literal request does not map one-to-one onto the data model** | Everything above **plus a clean-context review** before it is done (§6) |

**About the file-count trigger.** *N* is the project's to set, not mine and not yours. Ask once, then remember it. It exists to catch changes that are wide *because they are consequential* — and it will also catch changes that are merely wide: renaming a field across the stack, adding one translation key in four places, bumping a version on three platforms. Those are mechanical, carry no ambiguity, and do not need a review round. If a project's work is routinely wide and shallow, its *N* should be high, and the other triggers still do the real work. Setting *N* badly is how this discipline turns into a tax.

Two routes the table cannot classify:

- **A fix already failed once, or a value displays wrong and the cause is not established** → do not change code again. Go to §5.
- **No codebase yet, and the user wants a product from one sentence** → §7.

The rule of thumb *"if the contract takes longer than the code, skip it"* is real but scoped: it is admissible **only between Trivial and Local**. A migration does not become Local because the contract felt long.

## 2. Ground before you assert

At structural tier and above, before writing the contract: read whatever architecture record the project keeps — invariants, glossary, domain notes, recent decisions. List the assumptions this task rests on. For each, name the document, commit, or code that supports it.

Any **ungrounded assumption that would change what you build** — which domain owns this, where a boundary sits, who owns the data, which invariant applies, what the project's word for this actually means — is a question, not a guess. Ask at most three at a time, each with one line on why it matters. Then write the answers into the project's record so the next task does not re-ask.

## 3. The three load-bearing fields

Write these to `contracts/YYYY-MM-DD_<task>.md` before generating implementation code. Three lines each is normal.

```markdown
## status
stage=3 | tier=<trivial|local|structural|critical> | blocked_on=[] |
unverified_preconditions=[] | open_escalations=[]

## intent
<One sentence. What will be observably true when this is done.
 Not "implement X" — "the user does A and sees B".>

## escalation / candidate set
<What is not yours to decide alone. And if the request's wording could
 point at more than one thing in the data, list the candidates and ask.>

## affected_layers
<What you are changing — and what you are deliberately not changing.>
```

> The specification writes the tier key as `blast_radius=T0/T1/T2/T3`. `tier=trivial|local|structural|critical` is the same thing; use either, consistently.

**The candidate set is the highest-value habit here.** "Resend the invitations in bulk" routinely addresses four different populations — never invited, invited but never accepted, expired, accepted-then-removed. Picking the likeliest produces correct code aimed at the wrong target, the most expensive kind of mistake because nothing looks broken. Enumerate, then ask. Do not translate literally.

**Before you present any direction, argue against it internally.** "If I were opposing this approach, what is the strongest case, and does it have substance?" Run this every time. Surface it *only* when the answer is yes — a manufactured objection on every task trains the user to skip the section, and then the one that mattered gets skipped too. When there are genuinely different routes, name them with their trade-offs — proceed as asked / refactor first / split the scope / escalate — and let the user choose rather than choosing for them.

Structural and critical tiers get the full contract: add `preconditions` (each with the executable check that established it), `schema_assumptions` (each with a source), `expected_outcome` (each with how it will be verified), `cross_module_contract`, `confidence`, `grounding`, `rollback_plan`, `test_plan`. Shape and field-by-field notes: [`references/contract-template.md`](references/contract-template.md).

At structural and critical tier, a decision with trade-offs also gets a short record of its own — what was decided, what it costs, and what would make you revisit it — kept wherever the project keeps decisions. The reviewer in §6 reads those; if they do not exist, the review has nothing to check the code against.

## 4. While implementing

1. Do not use a flag, toggle, or hidden field to work around a boundary the contract declared.
2. If you find mid-implementation that you must cross that boundary, **stop and go back to escalation**. Do not decide it yourself.
3. Do not change anything outside `affected_layers` without reporting first.

When the work ships, mark every clause `PASS` / `FAIL` / `MUTATED` with a one-line reason. `MUTATED` is the most useful of the three — it records that the plan did not anticipate something, rather than that the work missed the plan.

## 5. Verification means execution, not declaration

> **Never mark a clause passed while its evidence is still a promise.**

Record what you actually ran this session — command output, query result, log line, observed value. If you did not run it, write `UNVERIFIED` and carry it forward. `PENDING` is a waypoint, not a pass.

This is the rule that matters most for a capable model. You will rarely fail by leaving a field blank; you will fail by filling one convincingly without doing the underlying work. `verified_by: searched the callers — no other call sites` reads identically whether the search ran or not.

Three corollaries, each of which has cost somebody an afternoon:

- **A green build is a prediction, not an observation.** For anything deployed, ask the running service which commit it is on. For a new persisted entity, start the service against a real database before calling it done — type checks, builds, and DI smoke tests do not reach the failure.
- **When a fix does not work on the first attempt, stop changing code.** Establish one fact first — a query, a search, a device log. Consecutive guesses leave residue that makes later rounds worse than earlier ones.
- **For a wrong-value bug, enumerate every place that value is produced and read all of them.** Not one hypothesis — all producers. A fallback added to a shared helper does not fix the copies that never call it. And choose where the evidence will come from *before* forming the hypothesis; five preconditions checked against the weakest available source produce a confidently wrong contract.

## 6. Critical work gets a clean-context review

Before critical work is done, spawn a subagent **with no memory of writing the code** and give it only the contract, the decisions it cites, and the diff:

```
You are reviewing this change in a clean context. You did not write it.
Read only: contracts/<file>.md, the decisions it cites, and the diff.
Report whether the diff delivers what the contract promised, what it changed
outside the declared scope, and anything that works but contradicts a
recorded decision. Report only — do not fix anything.
```

You cannot do this yourself in the working session. The reasoning that produced a gap is the reasoning that would review it.

The reviewer **reports and does not fix**, and its most severe verdict is not "this is broken" but **"this works and contradicts what was agreed."** Then act on the findings and tell the user only what is actionable for them.

## 7. Starting from nothing

When there is no codebase and the user wants a product from one sentence, ask **one** open question first — "what are you most hoping this does for you?" — and use the answer to decide which choices matter and which named experience must not become a placeholder. If the answer is circular, do not press; fall through to the forks.

Then ask only about choices that are expensive to reverse, phrased as consequences: does it need the camera, background location, or biometrics; does the work survive a new phone; does it pull data in from somewhere else or stand alone; do other people log in; can they see each other's data; is anything regulated. Give cheap choices a sensible default and show them in a visible "here's what I assumed" block. Four never get a silent default: **persistence across devices, multiple people logging in, who can see whose data, and anything touching money or someone else's personal information.**

Ask by making the future imaginable — "you get a new phone: is your work still there, or is starting over fine?" — not by asking them to approve an architecture word. Confirm in capabilities: "on day one you can A, B, C; you cannot yet D, E." The exclusion list is what makes someone say *wait, my partner can't log in?*

**Never decide one of these yourself.** What you could not get an answer to is written down as `UNKNOWN: <why>`, not guessed. Write the results as the project's architecture record — invariants, domains, glossary, one note per decision that carried a trade-off — so §2 finds them already grounded.

## 8. Enforce it mechanically

Documents do not enforce themselves. After writing or updating a contract:

```bash
python3 <this-skill-directory>/scripts/validate.py contracts/<file>.md
```

The script sits beside this file. Resolve the directory from wherever this skill was loaded — `~/.claude/skills/mtm/` for a copied-folder install, somewhere under `~/.claude/plugins/` for a plugin install. If you are unsure, `find ~/.claude -name validate.py -path '*mtm*'` settles it once; remember the answer for the session.

It fails on: a missing or unfilled `status` header, a required section left blank or still holding template placeholders, a precondition with no `verified_by`, a clause marked `PASS` whose `observed_result` is empty or still a promise, and implementation begun with preconditions open. It warns when the declared tier looks understated for the contract's own content.

**Be clear about what it cannot do.** It cannot tell whether you actually ran a check — nothing can. It tells you whether you claimed a pass without recording an observation. A clean run means "nothing is obviously unclosed", never "this was verified". Do not let a green line stand in for the review in §6.

## 9. Close the loop

Append one line per non-trivial task to a ledger (`docs/mtm-ledger.md` is fine): date · task · tier · first attempt clean? · hallucination events · which field caught or missed something · what the escalation was worth.

**The specification makes this a hard gate — a task is not done until the line exists.** It is worth knowing why that is stated so strongly: the rule was soft first, went unwritten, and was promoted precisely because soft record-keeping leaks. It then went unwritten again for ten consecutive tasks a month later, which is published in §12 of the article. If you are working solo and want only what pays for itself immediately, you may choose to skip it — but skip it knowingly, and adopt it as soon as you start wanting to change the rules, because without cases you will be changing them on impressions.

---

**Reference material** — load only when you need it:
- [`references/contract-template.md`](references/contract-template.md) — the full contract, field by field
- [`references/failure-modes.md`](references/failure-modes.md) — ten recurring failure modes and which field stops each
