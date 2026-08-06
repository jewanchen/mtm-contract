---
name: Field report
about: You used MTM on real work. Tell us what happened — this is the evidence the method does not have.
title: "Field report: "
labels: field-report
---

<!--
The article is honest that every number in it comes from one codebase and one
human-AI pair. A report from outside is worth more than any amount of internal
reasoning — the last one changed the specification within a day.

Nothing here is required. Even one answer is useful. There is no telemetry in
this project and never will be; this form is the only channel.
-->

**How long, and on what?**
<!-- e.g. "two weeks, a Go/Postgres backend and a React console" -->

**1. Which rule actually caught something?**
<!-- The specific one. What would have happened without it? -->

**2. Which part was pure tax?**
<!-- What have you already started skipping? This is the most useful answer. -->

**3. Where did you get stuck, or not know what to do?**
<!-- Especially on first contact. Anything ambiguous, circular, or missing. -->

**Optional — a de-identified summary of your contracts**

Run this and paste the output. It reads only structure: counts, tiers, how many
clauses are unverified. No file names, no content, nothing from your codebase.

```bash
python3 <path-to>/validate.py --report contracts/
```

**Anything else**
<!-- Including "I read it and did not adopt it, because ___". That is also data. -->
