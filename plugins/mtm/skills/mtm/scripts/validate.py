#!/usr/bin/env python3
"""
MTM contract validator — the mechanical half of the discipline.

WHAT THIS CAN AND CANNOT DO
---------------------------
It cannot tell whether you actually ran a check. Nothing can. What it can
tell is whether you claimed a clause passed *without recording what you
observed* — which is the specific failure a capable model produces, and the
one a human reviewer skims past. Treat a clean run as "nothing is obviously
unclosed", never as "this was verified".

Checks:
  1. a `status` header exists and names a tier
  2. the sections that tier requires are present, and answered
     (`N/A` and `UNKNOWN: <why>` are answers; blank and unfilled
      <template placeholders> are not)
  3. no clause is marked PASS while its evidence is still a promise —
     evaluated per clause, across lines, not per line
  4. implementation has not begun with preconditions still open
  5. every precondition carries a `verified_by`
  6. warns when the declared tier looks understated for the contract's
     own content (a label is not a classification)

Zero dependencies. Python 3.8+, standard library only.

    python3 validate.py contracts/2026-08-01_my-task.md
    python3 validate.py contracts/*.md
    python3 validate.py --quiet contracts/*.md    # errors only, for CI
    python3 validate.py --report contracts/       # de-identified summary

--report reads structure only — counts, tiers, how many clauses are closed.
It emits no file names and nothing from your code, so the output is safe to
paste into a field report. There is no telemetry in this tool; nothing is
sent anywhere.

Exit status: 0 if every file passes, 1 if any file has an error, 2 on a
usage problem (no files matched, unreadable path). Warnings never fail.

Part of MTM Contract. Apache 2.0, Vast Intelligence Limited.
https://github.com/jewanchen/mtm-contract
"""

import os
import re
import sys

# --- what each tier is required to answer ----------------------------------

BASE = ["intent", "escalation", "affected_layers"]
STRUCTURAL = BASE + ["preconditions", "schema_assumptions", "expected_outcome",
                     "cross_module_contract"]
CRITICAL = STRUCTURAL + ["grounding", "rollback_plan", "test_plan"]

REQUIRED = {
    "trivial": [], "t0": [],
    "local": BASE, "t1": BASE,
    "structural": STRUCTURAL, "t2": STRUCTURAL,
    "critical": CRITICAL, "t3": CRITICAL,
}

# Headings are matched by substring against these keys, in either language.
ALIASES = {
    "intent": ["intent", "意圖", "目的"],
    "escalation": ["escalation", "candidate", "升級", "候選", "escalate"],
    "affected_layers": ["affected_layers", "affected layers", "影響層", "影響範圍"],
    "preconditions": ["precondition", "前提"],
    "schema_assumptions": ["schema_assumptions", "schema assumptions", "假設"],
    "expected_outcome": ["expected_outcome", "expected outcome", "預期結果", "預期產出"],
    "cross_module_contract": ["cross_module", "cross module", "跨模組"],
    "grounding": ["grounding", "依據", "接地"],
    "rollback_plan": ["rollback", "回退", "回滾"],
    "test_plan": ["test_plan", "test plan", "測試"],
    "status": ["status", "狀態"],
    "confidence": ["confidence", "信心"],
}

# A value that is a promise rather than an observation. Deliberately narrow:
# a false positive trains people to ignore the validator. "Expected 3 rows,
# saw 3" and "N/A" are observations and must NOT match.
PROMISE_WHOLE = re.compile(
    r"^\s*(pending|tbd|todo|待驗|待測|未驗|待確認|—|-|\?+)\s*$", re.IGNORECASE)
PROMISE_START = re.compile(
    r"^\s*(will\b|going to\b|to be (verified|checked|confirmed)\b|"
    r"pending\b|預計|之後再|待.{0,4}驗|尚未)", re.IGNORECASE)

MARK = re.compile(r"\b(PASS|FAIL|MUTATED|UNVERIFIED)\b")
PLACEHOLDER_SPAN = re.compile(r"<[^<>\n]{2,}>")


def is_promise(value):
    v = value.strip().strip("`*_ ")
    if not v:
        return False
    if "unverified" in v.lower() or "UNVERIFIED" in value:
        return False
    return bool(PROMISE_WHOLE.match(v) or PROMISE_START.match(v))


def strip_placeholders(text):
    """Remove <angle-bracket placeholders>; what's left is the real answer."""
    return PLACEHOLDER_SPAN.sub("", text)


class Finding:
    def __init__(self, kind, line, message, hint=""):
        self.kind, self.line, self.message, self.hint = kind, line, message, hint


def read_lines(path):
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        return None, f"cannot read file: {exc}"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, (f"not valid UTF-8 at byte {exc.start} — "
                      "contracts must be UTF-8")
    return text.splitlines(), None


def split_sections(lines):
    """[(heading, line_no, body_lines)] for each `## heading`, fences ignored."""
    sections, current, in_fence = [], None, False
    for i, raw in enumerate(lines, start=1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            if current:
                current[2].append(raw)
            continue
        m = None if in_fence else re.match(r"^##\s+(.+?)\s*$", raw)
        if m:
            current = (m.group(1).strip().lower(), i, [])
            sections.append(current)
        elif current is not None:
            current[2].append(raw)
    return sections


def matches(heading, key):
    return any(a in heading for a in ALIASES.get(key, [key]))


def body_is_unanswered(body):
    """True if the section is blank, or still only template placeholders."""
    meaningful = []
    for line in body:
        s = line.strip()
        if not s or s.startswith(">") or s.startswith("```"):
            continue
        s = strip_placeholders(s)
        s = re.sub(r"^[-*\d.\s|:]+", "", s).strip()
        if s:
            meaningful.append(s)
    return not meaningful


def read_status(sections):
    for heading, line_no, body in sections:
        if matches(heading, "status"):
            text = " ".join(body)
            tier = stage = None
            m = re.search(r"(?:tier|blast_radius)\s*=\s*([A-Za-z0-9_\-]+)", text)
            if m:
                tier = m.group(1).strip().lower()
            m = re.search(r"stage\s*=\s*([0-9]+)", text)
            if m:
                stage = int(m.group(1))
            elif re.search(r"stage\s*=\s*\S*done", text, re.IGNORECASE):
                stage = 6
            return tier, stage, text, line_no
    return None, None, "", 0


def iter_clauses(body, start_line):
    """Yield (line_no, [lines]) per `-` bullet, continuation lines included."""
    clause, first = None, None
    for offset, raw in enumerate(body):
        line_no = start_line + offset + 1
        if re.match(r"^\s*[-*]\s+\S", raw):
            if clause is not None:
                yield first, clause
            clause, first = [raw], line_no
        elif clause is not None and (raw.strip() == "" or raw.startswith((" ", "\t"))):
            clause.append(raw)
        elif clause is not None:
            yield first, clause
            clause = None
    if clause is not None:
        yield first, clause


def check_outcomes(sections):
    """Rule 3, evaluated per clause so multi-line layout is covered."""
    out = []
    for heading, line_no, body in sections:
        if not (matches(heading, "expected_outcome") or "self-check" in heading
                or "自查" in heading):
            continue
        for first, clause in iter_clauses(body, line_no):
            text = "\n".join(clause)
            marks = MARK.findall(text)
            m = re.search(r"observed_result\s*[:：]\s*(.*)", text, re.IGNORECASE)
            observed = m.group(1).strip() if m else None
            if observed is not None:
                observed = strip_placeholders(observed).strip()

            if "PASS" in marks:
                if observed is None or not observed:
                    out.append(Finding(
                        "error", first,
                        "marked PASS with no observed_result",
                        "record what you actually ran, or mark UNVERIFIED"))
                elif is_promise(observed):
                    out.append(Finding(
                        "error", first,
                        f"marked PASS while observed_result is a promise "
                        f"({observed[:40]!r})",
                        "PENDING is a waypoint, not a pass"))
            elif observed is not None and not observed:
                out.append(Finding(
                    "warn", first, "observed_result is empty",
                    "record what you ran, or write UNVERIFIED"))

        # a self-check table row: | clause | PASS | <evidence> |
        for offset, raw in enumerate(body):
            if raw.lstrip().startswith("|") and "PASS" in raw:
                cells = [c.strip() for c in raw.strip().strip("|").split("|")]
                if len(cells) >= 3:
                    ev = strip_placeholders(cells[-1]).strip()
                    if not ev or is_promise(ev):
                        out.append(Finding(
                            "error", line_no + offset + 1,
                            "clause marked PASS with no observed evidence",
                            "the evidence column must say what you saw"))
    return out


def check_preconditions(sections):
    out = []
    for heading, line_no, body in sections:
        if not matches(heading, "preconditions"):
            continue
        for first, clause in iter_clauses(body, line_no):
            text = "\n".join(clause)
            if body_is_unanswered(clause):
                continue
            m = re.search(r"verified_by\s*[:：]\s*(.*)", text, re.IGNORECASE)
            if not m:
                out.append(Finding(
                    "error", first, "precondition has no verified_by",
                    "name the executable check, or write UNKNOWN: <what to check>"))
            else:
                val = strip_placeholders(m.group(1)).strip()
                if not val:
                    out.append(Finding(
                        "error", first, "verified_by is empty",
                        "name the check you ran"))
    return out


# Words whose presence in a contract's own text suggests the tier is understated.
RISK = [("auth", r"\bauth|permission|權限|secret|token\b"),
        ("schema", r"\bmigrat|schema|ALTER TABLE|新增欄位|資料表\b"),
        ("money", r"\bpayment|billing|invoice|訂閱|金流|付款\b"),
        ("visibility", r"\btenant|multi-?tenant|visibility|租戶|可見性\b")]


def check_tier_plausibility(tier, lines, status_line):
    if tier not in ("trivial", "t0", "local", "t1"):
        return []
    text = "\n".join(lines)
    hits = [name for name, pat in RISK if re.search(pat, text, re.IGNORECASE)]
    if hits:
        return [Finding(
            "warn", status_line,
            f"tier={tier} but this contract mentions {', '.join(hits)}",
            "the tier is decided by trigger, not by label — check §1 of the skill")]
    return []


def validate(path):
    lines, err = read_lines(path)
    if err:
        return [Finding("error", 0, err)]

    sections = split_sections(lines)
    if not sections:
        return [Finding("error", 0, "no `## sections` found — is this a contract?")]

    findings = []
    tier, stage, status_text, status_line = read_status(sections)

    if tier is None:
        findings.append(Finding(
            "error", status_line or 1,
            "no `## status` section naming a tier"
            if not status_line else "`## status` does not name a tier",
            "add: stage=<n> | tier=<trivial|local|structural|critical>"))
        required = BASE
    elif tier not in REQUIRED:
        findings.append(Finding(
            "warn", status_line, f"unrecognised tier {tier!r} — checked as structural",
            "expected trivial / local / structural / critical (or T0-T3)"))
        required = STRUCTURAL
    else:
        required = REQUIRED[tier]
        if not required:
            print(f"{path}: trivial — no contract needed.")
            return []

    for key in required:
        hit = next(((h, ln, b) for h, ln, b in sections if matches(h, key)), None)
        if hit is None:
            findings.append(Finding(
                "error", status_line or 1, f"missing required section: {key}"))
        elif body_is_unanswered(hit[2]):
            findings.append(Finding(
                "error", hit[1], f"`{key}` is unanswered",
                "`N/A` and `UNKNOWN: <why>` are answers; a blank or an "
                "unfilled <placeholder> is not"))

    findings.extend(check_outcomes(sections))
    findings.extend(check_preconditions(sections))
    findings.extend(check_tier_plausibility(tier, lines, status_line or 1))

    m = re.search(r"unverified_preconditions\s*=\s*\[(.*?)\]", status_text, re.DOTALL)
    if m and strip_placeholders(m.group(1)).strip() and stage is not None and stage >= 4:
        findings.append(Finding(
            "error", status_line,
            "implementation started with preconditions still unverified",
            "close them, or move them into escalation"))

    return findings


def build_report(paths):
    """Structure-only summary. No file names, no content — safe to share."""
    tiers, n, errs, warns = {}, 0, 0, 0
    pass_marks = unver = pending = pc_total = pc_no_verified = 0
    sections_seen = {}
    for path in paths:
        lines, err = read_lines(path)
        if err:
            continue
        n += 1
        sections = split_sections(lines)
        tier, _, _, _ = read_status(sections)
        tiers[tier or "unstated"] = tiers.get(tier or "unstated", 0) + 1
        for heading, _, _ in sections:
            for key in ALIASES:
                if matches(heading, key):
                    sections_seen[key] = sections_seen.get(key, 0) + 1
                    break
        body = "\n".join(lines)
        pass_marks += len(re.findall(r"\bPASS\b", body))
        unver += len(re.findall(r"\bUNVERIFIED\b", body))
        pending += len(re.findall(r"\bPENDING\b", body))
        for heading, line_no, sec in sections:
            if matches(heading, "preconditions"):
                for _, clause in iter_clauses(sec, line_no):
                    if body_is_unanswered(clause):
                        continue
                    pc_total += 1
                    if not re.search(r"verified_by", "\n".join(clause), re.IGNORECASE):
                        pc_no_verified += 1
        f = validate(path)
        errs += sum(1 for x in f if x.kind == "error")
        warns += sum(1 for x in f if x.kind == "warn")

    out = ["MTM contract summary — structure only, no file names or content", ""]
    out.append("contracts               : %d" % n)
    if tiers:
        out.append("tiers                   : " + ", ".join(
            "%s=%d" % (k, v) for k, v in sorted(tiers.items())))
    out.append("clauses marked PASS     : %d" % pass_marks)
    out.append("marked UNVERIFIED       : %d" % unver)
    out.append("still PENDING           : %d" % pending)
    out.append("preconditions           : %d (%d without verified_by)"
               % (pc_total, pc_no_verified))
    out.append("validator errors        : %d" % errs)
    out.append("validator warnings      : %d" % warns)
    if sections_seen:
        out.append("")
        out.append("field usage (how many contracts carry each):")
        for k in ("intent", "escalation", "affected_layers", "preconditions",
                  "schema_assumptions", "expected_outcome",
                  "cross_module_contract", "grounding", "rollback_plan",
                  "test_plan", "confidence"):
            if k in sections_seen:
                out.append("  %-22s %d" % (k, sections_seen[k]))
    out.append("")
    out.append("Nothing above identifies your project. Paste it into a field")
    out.append("report if you like: github.com/jewanchen/mtm-contract/issues")
    return "\n".join(out)


def expand(paths):
    """Accept directories as well as files."""
    out = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                out += [os.path.join(root, f) for f in sorted(files)
                        if f.endswith(".md")]
        else:
            out.append(p)
    return out


def main(argv):
    flags = {a for a in argv[1:] if a.startswith("--")}
    paths = [a for a in argv[1:] if a not in flags]
    quiet = "--quiet" in flags

    if "--help" in flags or "-h" in flags:
        print(__doc__.strip())
        return 0
    if not paths:
        print("usage: validate.py [--quiet|--report] <contract.md|dir> [...]",
              file=sys.stderr)
        return 2

    if "--report" in flags:
        found = expand(paths)
        if not found:
            print("no .md files found", file=sys.stderr)
            return 2
        print(build_report(found))
        return 0

    failed = False
    for path in paths:
        findings = validate(path)
        errors = [f for f in findings if f.kind == "error"]
        if errors:
            failed = True
        for f in (errors if quiet else findings):
            where = f"{path}:{f.line}" if f.line else path
            print(f"{where}: {'error' if f.kind == 'error' else 'warn '}: {f.message}")
            if f.hint:
                print(f"    → {f.hint}")
        if not errors and not quiet:
            warns = len(findings)
            note = f" ({warns} warning{'s' if warns != 1 else ''})" if warns else ""
            print(f"{path}: ok{note}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
