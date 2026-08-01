# The full contract — field by field

Load this when a task reaches **structural** or **critical** tier. Below that, the three fields in `SKILL.md` §2 are the whole thing.

Three verification chains carry the weight; everything else is the context that makes them meaningful.

- **Premises** — `preconditions` + `verified_by`
- **Results** — `expected_outcome` + `verifiable_by` → `observed_result`
- **Assumptions** — `schema_assumptions` + `source`

Copy the block below to `contracts/YYYY-MM-DD_<task>.md`.

```markdown
# MTM Contract: <task + one line>

## status
stage=<0-6> | tier=<trivial|local|structural|critical> | blocked_on=[] |
unverified_preconditions=[] | open_escalations=[]

## intent
<One observable sentence, verb first. Not "implement X" — "the user does
 A and observes B".>

## affected_layers
<Layer by layer: what changes and what deliberately does not.
 entity / service / endpoint / migration / scheduled work / client state /
 screens / cache / admin surfaces / env and secrets>

## preconditions
- <condition>
  verified_by: <the executable thing that established it — a search at a
  named commit, a query, a request against the running service, a log line.
  If you have not run it: UNKNOWN: <what you would need to check>>

## schema_assumptions
- <assumption about a data shape, default, or invariant>
  source: <spec section / entity comment / commit / prior decision>
  <no source → the assumption is SPECULATIVE and gets reviewed first>

## cross_module_contract
emit: <events, payloads, responses this produces>
listen: <what it subscribes to>
I assume others will: <dependencies outside this work>
Others depend on me to: <invariants callers rely on — the silent breakage lives here>

## expected_outcome
- <externally observable result>
  verifiable_by: <how it will be checked>
  observed_result: <what you actually saw this session — or UNVERIFIED>

## confidence
overall: <high|medium|low>
low-confidence sub-items: <item — why uncertain — what you will do about it>

## escalation
Not mine to decide: <enumerate; do not resolve these yourself>
Stop and report if: <conditions that should halt the work>

## grounding
<Where the claims in this contract come from. Anything uncited is SPECULATIVE.>

## rollback_plan
code: <revert path>   schema: <reversible? forward-fix?>   env: <what to remove>

## test_plan
local: <steps>   staging: <steps>   production: <smoke step>
```

## After it ships

**Self-check** — you do this. Mark every clause `PASS` / `FAIL` / `MUTATED` with a one-line reason, and fill `observed_result` with what you actually observed.

`MUTATED` is the most informative of the three: it records that the plan did not anticipate a constraint, rather than that the work missed the plan. Those reasons are what future contracts should have contained.

> A clause may not be marked `PASS` while its `observed_result` is still a promise or `PENDING`. Either paste evidence you produced this session, or mark it `UNVERIFIED` and carry it into review as an open item.

**Review** — mandatory at critical tier, and it cannot be you. See `SKILL.md` §5.

## Two rules that decide how the artifact behaves

**Every field is answered.** `N/A` is a legitimate answer. "I don't know" is written `UNKNOWN: <why>` so it surfaces instead of hiding. Blank is not an answer, and the validator fails on it.

**One artifact, from start to finish.** The same file grows through the task, and its `status` header is the single source of truth. After a context summary or a handoff, that header is the only thing that needs to be read to know where things stand. Decisions that live only in the conversation get paid for twice.
