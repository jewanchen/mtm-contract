# MTM as a Claude Skill

If the [2.0 article](../mtm-contract-2.0-article.md) made sense to you, this is the version you install rather than remember.

Copy one folder. After that you keep delegating work in plain language — the agent classifies the task itself, writes down what must be true before it generates anything, refuses to mark a check passed on a promise, and pulls in a clean-context reviewer before merging anything risky. You never see a field name unless you go looking.

## Install

```bash
git clone https://github.com/jewanchen/mtm-contract.git
mkdir -p ~/.claude/skills
cp -r mtm-contract/skill/mtm ~/.claude/skills/
```

Verify it landed:

```bash
python3 ~/.claude/skills/mtm/scripts/validate.py --help
```

That is the whole installation. Nothing to build, nothing to configure, no dependencies — the bundled validator is Python 3 standard library only.

- `~/.claude/skills/` makes it available in every project.
- `<your-project>/.claude/skills/` scopes it to one repository, if you would rather try it somewhere contained first.

## Using it

Mostly you don't. The skill loads when the work looks like it needs it — a task spanning several files, a schema change, anything touching authentication or payments or who-can-see-what, a bug that survived its first fix. You will notice it as the agent asking a sharper question before it starts, and as it declining to call something verified that it did not actually run.

To invoke it deliberately, type `/mtm`.

To check a contract by hand, or wire the check into CI:

```bash
python3 ~/.claude/skills/mtm/scripts/validate.py contracts/*.md
```

It exits non-zero on: a missing or unfilled `status` header, a required section left blank or still holding template placeholders, a precondition with no `verified_by`, a clause marked `PASS` whose `observed_result` is empty or still a promise, and implementation begun with preconditions open. It warns when the declared tier looks understated for the contract's own content. Warnings do not fail the run.

**What it cannot do**, stated plainly because the alternative is worse: it cannot tell whether you actually ran a check. Nothing can. It tells you whether a pass was claimed without an observation recorded next to it — which is the specific way a capable model fails, and the thing a human reviewer skims past. A clean run means "nothing is obviously unclosed". It does not mean the work was verified, and it is not a substitute for the clean-context review.

## What's inside

| | |
|---|---|
| `mtm/SKILL.md` | The behaviour. Tier triggers, the three load-bearing fields, execution binding, the clean-context review. |
| `mtm/references/contract-template.md` | The full contract, field by field — loaded only when a task is structural or critical. |
| `mtm/references/failure-modes.md` | Ten recurring failure modes and which field is supposed to stop each one. |
| `mtm/scripts/validate.py` | The mechanical check. Zero dependencies. |

## If you don't use Claude Code

The skill is one packaging of the method, not the method. [`MTM-LITE.md`](../MTM-LITE.md) is the same content as a page you can paste into any agent's rules file — Cursor, Windsurf, a system prompt, whatever you use. The validator works standalone on any contract file, whatever produced it.

## Why a skill rather than a document

Section 12 of the article reports a rule this project promoted from "please do this" to "mandatory", and then failed to honour for ten consecutive tasks a month later — in its own repository, with its own authors watching. The conclusion published there is that **a hard gate with no mechanical enforcement point is still soft discipline.**

A document cannot enforce itself. A skill can carry a script and run it without asking you to open a terminal. That is the entire argument for this packaging, and it is an argument the method produced by failing rather than by working.

---

Apache 2.0 — Vast Intelligence Limited. Attribution required in derivative works; see [`NOTICE`](../NOTICE).
