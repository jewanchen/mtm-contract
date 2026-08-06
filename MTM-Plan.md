# MTM Plan — greenfield: turning one sentence into something buildable

> **Phase 0-Plan detail for [`MTM-CORE.md`](./MTM-CORE.md) (current specification: 2.4).** This is the branch for "someone has one sentence and no codebase": before any code, surface **the foundational decisions they do not know they are making**, in the language of consequences, and write the result into the project's architecture record so phase 1 can fast-path.
> 繁體中文原稿：[`MTM-Plan.zh-TW.md`](./MTM-Plan.zh-TW.md)

**The whole idea in one line**: open by asking what they are hoping for, then surface only the forks that are expensive to reverse — and when you ask, make them **point at a future they can picture**, not nod at an architecture word they do not understand.

---

## 1. When this branch triggers

Two observable signals, both required:

1. **Greenfield** — no architecture record, and no source tree (or an empty one).
2. **One sentence, one product** — the request describes *a thing to be built* ("I want an app that can…"), not a scope change to something that exists ("add X to Y", "fix Z").

Whether the person is technical is **not** a separate gate. It is handled per fork: anything they have already decided in their own prompt ("a multi-tenant Rails API") counts as grounded and is skipped. You do not interrogate someone who has already decided.

**Edge cases:**
- *Greenfield + technical user* → still triggers, but collapses to almost nothing: every fork they settled themselves passes, and you ask only about the rest.
- *Existing project + a vague sentence* ("add community features", "make it look better") → **does not trigger.** That is phase 2's candidate-set territory.

---

## 2. The boundary: a Plan fork versus a phase-2 candidate set

> **A Plan fork's answer determines which domains and entities will exist — it precedes and generates the data model. A phase-2 candidate set maps one intent onto a model that already exists.**

The operational test: **is there a data model to enumerate candidates from?** No → Plan fork (greenfield, before the model). Yes → phase 2.

Cost of being wrong, as corroboration: a Plan fork guessed wrong means tearing it down and rebuilding (platform, local versus cloud, tenancy). A phase-2 miss means rolling back a feature.

**Guardrails in both directions**: Plan **never decides a fork itself** — it lays out the fork and its downstream consequences and **the person chooses** (the same rule as phase 2). Anything you could not get an answer to is written `UNKNOWN: <why>`; **it is never filled in with a guess.** Plan also does not make feature-scope decisions — those belong to phase 2.

---

## 3. Disciplines — what makes this feel like a helpful colleague rather than a form to abandon

**0 · Ask the purpose first.** Before any fork, ask one open question: **"What are you most hoping this does for you? What would it solve?"** Use the answer to set direction and to identify the soul of the thing (this feeds invariant 7). This is the **only** open-ended question asked by default. At the opening you ask **this one question and nothing else** — presentation and platform, who uses it and in what situation still go through the §4a "ask only when it is hard to reverse" mechanism, and are **not** all laid out up front (that turns straight back into the form this document exists to kill). **Do not volunteer additional features** — those belong in §4c or phase 2.

- **The answer has to be wired in, not just collected** (otherwise it degenerates into a ceremonial opening question): (a) write it into the handoff's glossary and invariants as a **purpose note**; (b) use it to decide which §4a forks matter enough to ask about; (c) mark which feature invariant 7 protects — the one that may not be downgraded to a placeholder.

- **(d) Turn the purpose back on the request itself (v2.3 · #19).** If what they are asking for **plainly contradicts** the goal they just stated, do not build it and do not quietly redesign it — put the contradiction to them: *"You said the point was X, but what you're asking for leads to Y — have I misread it, or is there something here I don't know about?"*
  - **Keep the bar at "plainly contradicts".** Widened to "could align better", this produces an agent that asks "does this really serve your goal?" about every request — which is the teleological form of the cry-wolf failure #5 already dealt with (manufactured objections → noise → the one that mattered gets skipped).  **Speak up on a plain contradiction; otherwise stay quiet and build.**
  - **The output is a question, never a refusal.** You do not get to decline because it feels contradictory. Surface it, ask, and the decision stays theirs (same as phase 2's "do not decide alone").
  - This is what turns the purpose from *a sense of direction* into *a checkpoint* — (a), (b) and (c) all use the purpose to steer what comes next; only this one uses it to check the request.

- **Fallback for a vague answer**: if they cannot articulate it, or it comes back circular ("it's for keeping track of things"), **do not ask a second open question.** Fall through to the fork mechanism below. Do not turn the purpose question into an interrogation.

**1 · Infer the cheap ones; ask only the expensive ones.** Any fork that can be added or reskinned later → infer a default from the persona, **do not ask**, and collect them in a visible "here's what I assumed" block they can read at a glance and change. **Ask** only about what is hard to reverse.

**2 · For hard-to-reverse forks, make them point — do not make them nod.** Not *"I assume you want this in the cloud, right?"* (a non-technical person will nod to look competent — the user-level version of invariant 6's failure). Instead: **"Picture this: you get a new phone. Should your work still be there (A), or is starting over fine (B)? Which are you?"** Give them a future they can imagine and let them choose it.

**3 · Consequences, not systems.** Not "do you need a backend database" but "when you change phones, is your data still there". Not "do you need multi-tenancy" but "should your partner be able to log in and see only their own part".

**4 · Four forks never get a silent default** — guessing wrong here means a rewrite, a leak, or a legal problem: **persistence across devices · single versus multiple people logging in · who can see whose data (tenant isolation) · anything touching money or other people's personal information.** All four are always presented with their trade-off.

**5 · At most three questions per round**, ordered by downstream blast radius, largest first.

**6 · Stopping condition**: you can draw the skeleton **and** every hard-to-reverse fork is either confirmed by the person or explicitly listed in the assumptions block. Being able to draw a skeleton is not enough on its own — that only means you have enough assumptions, not that you surfaced the right ones.

**7 · Confirm in capabilities, not in structure.** Restate as **"on day one you will be able to ___"** plus **"you will not yet be able to ___"** (the exclusion list), using their verbs. The exclusion list is what makes a non-technical person catch the mistake — *"wait, my partner can't log in?"* Entity diagrams and screen lists are machine language; do not hand those over for confirmation.

**8 · The customer's core need comes first (v0.5 · CORE invariant 7).** The core experience stated **literally** in their one sentence — the soul of the tool ("it has to sound like a real bass") — is a **first-class deliverable**. If a real solution is readily available, **ship the real thing rather than a placeholder**; if it genuinely must wait, put it at the top of the "not yet" list explicitly. Discipline 1's "cheap things can wait" **does not apply to the core experience.**

---

## 4. The fork library

### 4a. Always ask — hard to reverse, show the trade-off, the person chooses

| Fork | How to ask it (in consequences) | What it decides | Where it is written |
|---|---|---|---|
| **Device capability** (decides whether the platform is reversible) | "Do you need the camera, background location, Bluetooth or NFC, face or fingerprint login? **By default, no** — which means one web build covers iOS and Android at once. If you do need them, it has to be a real native app, which is a different piece of engineering." | Whether native is forced; deployment | invariants + decision record |
| **Persistence across devices** | "When you get a new phone, should the work **still be there (A)**, or is starting over fine (B)?" | Whether there is a backend and a cloud database | invariants + decision record |
| **Standalone versus integrated** 🔑 | "I'll assume it holds what you type into it. But most of what you want to track already lives somewhere else — email, a calendar, a spreadsheet, a CRM. Should it **pull those in (A)**, or be **a fresh notebook of its own (B)**? Default is B; if it has to connect to [X], the foundations are different." | OAuth, sync, reconciliation model | invariants + decision record |
| **Single versus multiple users** | "**Only you (A)**, or do **other people log in separately (B)**?" (A solo persona often has an unspoken need to share with a partner or an investor.) | Authentication and identity | invariants + domains |
| **Who can see whom** (only if multi-user) | "Does everyone see **everything (A)**, or does each person **see only their own, with customers invisible to each other (B)**?" | Multi-tenancy and data isolation — privacy is irreversible | invariants (hard) + decision record |
| **Regulatory and residency** (only if the data is sensitive) | "Is any of this regulated — medical, financial or cap-table, EU personal data? Does it have to stay in a particular country? Default assumption: confidential but unregulated. If there is a regime, auditing, encryption and region get baked in now." | Compliance, encryption, audit log, residency | invariants (hard) + decision record |

### 4b. Infer a default — collect in the "here's what I assumed" block, show but do not ask

- **Platform**: default to web/PWA, one build covering both mobile platforms — **unless** 4a's device-capability fork forces native.
- **Tool versus product**: default to "a personal tool for now, structured so it can grow into a product".
- **Scale**: default small. A standard stack handles millions of rows; surface this only if the persona genuinely implies high volume.
- Styling · naming · list versus cards · notification defaults.

### 4c. Defer — cheap to add later, do not touch now

Payments (unless 4a established "a product for customers"), offline-first (unless the setting implies no network), real-time collaboration and conflict resolution (unless simultaneous editing of one record *is* the point), AI features, importing from spreadsheets, internationalisation and accessibility.

---

## 5. Handoff — what Plan must write so phase 1 fast-paths instead of re-asking

Phase 1 only recognises grounding in the files it reads: the index, invariants, glossary, domain notes and decisions. **A standalone `spec.md` will not be treated as grounding, and phase 1 will re-escalate the same forks in developer vocabulary — which is rework.** So Plan translates its conclusions into that vocabulary:

- **`invariants.md`** ← irreversible forks written as "always true" rules. For example: *single-user, local-only: no auth, no server, no tenancy*; *health data → encryption at rest is mandatory*; *multi-tenant: each customer's data is physically isolated*. This directly grounds the tenancy, ownership and visibility assertions phase 1 would otherwise ask about.
- **`domains/<domain>.md`** ← the domains the one sentence decomposes into, with their responsibility boundaries. Grounds "which domain owns this" and "where the boundary sits".
- **`glossary.md`** ← the person's product words mapped to formal terms. Grounds the domain-language mapping and prevents translation drift.
- **`decisions/YYYY-MM-DD_*.md`** ← one seed decision record per resolved fork that carried a trade-off (decision, consequences, what would make you revisit). This lets phase 2 **cite** rather than re-escalate.
- **`INDEX.md`** ← the index plus domain relationships. The first thing phase 1 reads.
- **`UNKNOWN` markers (mandatory)** ← every fork Plan did **not** resolve is written `UNKNOWN: <why>`, never silently omitted. This is the insurance against Plan fabricating grounding: phases 1 and 2 then correctly treat an unresolved fork as still open.

The result: phase 1 reads grounded invariants, domains and glossary and fast-paths. What Plan resolved is not asked again; what it marked `UNKNOWN` flows into normal escalation. Clean.

---

## 6. Worked example — "I'm a VC associate; I want to manage all my portfolio companies from my phone"

**Plan opens by asking the purpose (to set direction):**
> What are you most hoping this does for you? Spend less time on it, or stop missing a key moment on one of the companies? — the answer decides what "progress" needs to record, and which feature is the soul of the thing.

**Inferred from the persona, collected in the assumptions block (not asked):** multiple projects (so the model has a `Project`), wants it on a phone at any time → default web/PWA, cloud (so it is not tied to one handset), a personal tool for now but structured to extend, small scale on a standard stack.

**Plan asks only these three (hard to reverse, imagination-first):**
> 1. When you get a new phone, should your portfolio still be there, or is starting over fine? *(I expect "still there" → cloud.)*
> 2. Most of this progress already lives in your email, or a spreadsheet, or some tool — should the app **pull it in**, or is a **notebook you type into yourself** enough?
> 3. Only you, or do **partners / LPs log in separately** too? (If yes → follow up: does everyone see everything, or does each person see only their own?)

**Confirmation (capabilities, no skeleton):**
> "On day one you'll be able to: add and edit your companies on your phone, see progress on each one, and pick up any device and still have it all.
> You will **not** yet be able to: let anyone else log in (right now it's just you), pull progress automatically out of email (you'll type it), or take payment.
> Does that sound right? Whichever line is wrong, now is the cheapest time to change it."

After confirmation → write invariants (cloud / single-user / standalone-v1) + domains (`Project`, `Progress`) + glossary (their "project" = a portfolio company) + two decision records (cloud-vs-local, standalone-vs-integrated) + `UNKNOWN` markers (payments, multi-user) → hand off to CORE phase 1.

---

*MTM Plan, tracking CORE 2.4. Opening purpose question and discovery coverage added in #15; the purpose turned back on the request itself in #19. Greenfield trigger only. Extended features are not volunteered — they belong to §4c or phase 2. Full history: [`EVOLUTION.md`](./EVOLUTION.md).*
