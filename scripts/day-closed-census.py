#!/usr/bin/env python3
"""Enumerate the DAY-CLOSED marker forms the corpus actually contains.

WHY THIS IS A SCRIPT AND NOT A TABLE IN A DOC
---------------------------------------------
Five DAY-CLOSED predicates were hand-written across three roles in two days
(2026-07-30/31). Every one was blind to the next real form along, because each
was written against the format its author imagined rather than the one the
corpus holds. CXO's rule from that week: **a predicate is a derived artifact
too — it can be regenerated from the corpus it is meant to match, and diffed.**

So the census table is a BUILD OUTPUT. It lived inline in
docs/internal/operations/day-closed-marker-census.md, which meant the doc
carried a copy of its own generator — exactly the drift this whole file is
about, one level up. Extracted here so there is one source.

USAGE
    python3 scripts/day-closed-census.py            # print the table
    python3 scripts/day-closed-census.py --check    # compare against the doc,
                                                    # exit 1 on drift, WRITE NOTHING

--check exists for the same reason rebuild-memory-index.py has one: a plain
regeneration REPAIRS the drift it would have detected, so a detector that
rewrites its subject cannot report. Render, compare, exit.

HOST, 2026-08-02.
"""

import collections
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOC = REPO / "docs/internal/operations/day-closed-marker-census.md"
BEGIN = "<!-- BEGIN GENERATED: census-table -->"
END = "<!-- END GENERATED: census-table -->"

# Convention floor: the DAY-CLOSED marker was ratified 2026-06-09. Logs before
# that legitimately have none, so including them would measure adoption, not form.
SINCE = "2026-06-09"

ANY_DC = re.compile(r"^.{0,4}(<!--\s*)?#{0,4}\s*\**\s*DAY-CLOSED", re.M)
LOGNAME = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-\d{4})?-([a-z]+)-code")


def census():
    files = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "dev/2026"],
        capture_output=True, text=True,
    ).stdout.split("\n")
    forms = collections.Counter()
    example = {}
    for rel in files:
        if not rel.endswith("log.md"):
            continue
        m = LOGNAME.match(rel.rsplit("/", 1)[-1])
        if not m or m.group(1) < SINCE:
            continue
        try:
            text = (REPO / rel).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in text.split("\n"):
            if not ANY_DC.match(line):
                continue
            s = line.strip()
            # THE distinction a predicate turns on: a real marker sits at column 0;
            # a narration of one is always indented, quoted, or mid-sentence. The
            # anchored `^` in every working predicate is exactly this test, so the
            # census has to report it as a dimension rather than blend the two.
            at_col0 = "col0" if line == s and not line.startswith(("`", ">", "-", "*")) else "**indented/quoted**"
            shape = (
                "html-comment" if s.startswith("<!--")
                else "md-heading" if s.startswith("#")
                else "bold" if s.startswith("**")
                else "other"
            )
            sep = (
                "colon" if re.match(r"^\S*\s*#*\s*\**\s*DAY-CLOSED\s*:", s)
                else "em-dash" if "—" in s[:30]
                else "none"
            )
            dated = "dated" if re.search(r"\d{4}-\d{2}-\d{2}", s) else "**UNDATED**"
            key = (at_col0, shape, sep, dated)
            forms[key] += 1
            example.setdefault(key, s[:70])
    return forms, example


def render(forms, example):
    total = sum(forms.values())
    canonical = forms[("col0", "html-comment", "colon", "dated")]
    markers = sum(v for k, v in forms.items() if k[0] == "col0")
    mentions = total - markers
    undated = sum(v for k, v in forms.items() if k[0] == "col0" and k[3] == "**UNDATED**")
    out = [BEGIN, "", "| position | form | separator | date | n | example |", "|---|---|---|---|---:|---|"]
    for k, n in forms.most_common():
        out.append(f"| {k[0]} | `{k[1]}` | {k[2]} | {k[3]} | {n} | `{example[k]}` |")
    out += [
        "",
        f"**{total} lines matched. {markers} are real markers (column 0); "
        f"{mentions} are narrations of one** (indented, quoted, or mid-sentence) — the "
        "population a bare `grep DAY-CLOSED` wrongly counts, and the reason every working "
        "predicate anchors on `^`.",
        "",
        f"**Canonical marker** (`col0` + `html-comment` + `colon` + `dated`): **{canonical}** "
        f"= {100 * canonical // markers}% of real markers.",
        "",
        f"⚠️ **Undated real markers — unreachable by ANY dated predicate: {undated}.** Not a "
        "formatting variant; a missing datum. No regex rescues these; their owners must add the date.",
        "",
        END,
    ]
    return "\n".join(out)


forms, example = census()
block = render(forms, example)

if "--check" not in sys.argv:
    print(block)
    raise SystemExit(0)

# --check: compare, never write.
if not DOC.exists():
    print(f"⚠️  {DOC.relative_to(REPO)} does not exist — the check DID NOT RUN.")
    raise SystemExit(1)
doc = DOC.read_text(encoding="utf-8")
if BEGIN not in doc or END not in doc:
    print(f"⚠️  generated-block markers absent from {DOC.relative_to(REPO)} — "
          "the check DID NOT RUN. Empty output is not 'clean'.")
    raise SystemExit(1)
current = doc[doc.index(BEGIN): doc.index(END) + len(END)]
if current.strip() == block.strip():
    print(f"✓ census table matches the corpus ({sum(forms.values())} markers, "
          f"{len(forms)} distinct forms)")
    raise SystemExit(0)

print("⚠️  DRIFT: the census table in the doc no longer matches the corpus.")
cur_lines, new_lines = current.split("\n"), block.split("\n")
for i, (a, b) in enumerate(zip(cur_lines, new_lines)):
    if a != b:
        print(f"   first difference at block line {i + 1}:")
        print(f"     in doc    : {a[:110]}")
        print(f"     corpus now: {b[:110]}")
        break
else:
    print(f"   (identical prefix; length differs by {len(new_lines) - len(cur_lines)} lines)")
print("   Regenerate:  python3 scripts/day-closed-census.py")
print("   Then paste the block between the BEGIN/END markers, or fix the corpus.")
raise SystemExit(1)
