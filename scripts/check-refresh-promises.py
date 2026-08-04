#!/usr/bin/env python3
"""check-refresh-promises.py — did the refresh a document PROMISES actually happen?

THE FAILURE THIS CATCHES
------------------------
A document states its own currency mechanism in prose: "refreshed as part of the
weekly workstream review." Nothing connects the two acts but that sentence. Writing
the review and editing the document are separate acts on separate surfaces, so the
promise can hold for months and then quietly stop holding, and the document keeps
ASSERTING it is current while going stale. Vigilance wearing a mechanism's costume.

Real instance (2026-08-04): ROLE-PORTFOLIO-CXO.md promised "sections 2 and 4 touched
every review." last_updated was 2026-06-19. Four workstream reviews shipped after it
(051 07-10, 052 07-19, 053 07-29, 054 07-31) and touched none of it — 6.5 weeks. It
was found by reading the section that made the promise, which is not a mechanism either.

WHY IT IS NOT THE SAME AS check-derived-drift.sh
------------------------------------------------
That script asks "does this artifact still match its GENERATOR." These documents have
no generator — they are hand-authored. The question here is "did the EVENT that was
promised to update this document actually touch it." Same family (m-46: promotion is a
re-verification event), different hop: not copy-vs-source, but promise-vs-event.

⚠️ AND THE STALENESS RULE IT REPLACES WOULD HAVE MISDIAGNOSED IT. The portfolio's own
signal said a lagging last_updated means "investigate the review cadence." The cadence
was healthy — four reviews, on time. The broken thing was the LINK, not the rhythm, so
the diagnostic pointed at the one part that was working. This checks the link.

CONTRACT: reads only, never writes, exit 0 = every promise held, exit 1 = one lapsed.
A document opts in by declaring in its YAML frontmatter:

    last_updated: 2026-08-04
    refresh_trigger_glob: "mailboxes/cxo/sent/workstream-*-cxo-*.md"

The trigger's date comes from an ISO date in its FILENAME (not mtime — mtime is
destroyed by checkout, rebase, and worktree provisioning, so it would report noise).
"""
import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ISO = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")

# ── DISCOVERY ───────────────────────────────────────────────────────────────────
# ⚠️ THIS WAS A HARDCODED LIST UNTIL 2026-08-04, AND THAT WAS THE DEFECT.
#
# The docstring advertised opt-in via a frontmatter key; enrollment actually required
# membership in a list only the author edited. HOST followed the documented instruction,
# added refresh_trigger_glob to their portfolio, re-ran, and got "checked: 1 document.
# NOT checked: 0.  ✓ Every CHECKED promise held." — their opted-in document invisible,
# exit 0.
#
# ⭐ And the coverage line — the honest-reporting feature, the whole point — reported
# NOT checked: 0 while a document that had opted in went unchecked, because ITS
# DENOMINATOR WAS THE WATCH LIST. A coverage report whose denominator is its own
# registration can never report the thing it exists to report. That is the denominator
# lesson (m-43's companion) occurring inside the coverage report built to honor it.
#
# So discovery now scans, and the denominator is the population of PROMISES, not of
# registrations: a document that declares a refresh discipline in prose but no checkable
# trigger is REPORTED AS UNVERIFIABLE rather than being silently outside the count.
# "Declared but unwatched" is now impossible to reach silently.
SCAN_GLOBS = [
    "docs/briefing/*.md",
]

# Documents outside the scanned directories. This is a supplement to discovery now,
# never the gate.
EXTRA = []

# Frontmatter keys that constitute a PROSE refresh promise — a document carrying one of
# these is claiming to stay current, and belongs in the denominator whether or not it
# has made that claim checkable.
PROMISE_KEYS = ("refresh_discipline", "refresh_trigger_glob", "staleness_note")


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def main():
    fail = 0
    checked = 0
    unverifiable = []
    skipped = []

    candidates = []
    for g in SCAN_GLOBS:
        candidates.extend(sorted(glob.glob(str(ROOT / g))))
    candidates.extend(str(ROOT / e) for e in EXTRA)
    seen = set()

    print("── refresh-promise check ────────────────────────────────────────────────────")
    for c in candidates:
        path = Path(c)
        rel = str(path.relative_to(ROOT))
        if rel in seen or not path.exists():
            continue
        seen.add(rel)

        fm = frontmatter(path)
        if not any(k in fm for k in PROMISE_KEYS):
            continue  # makes no refresh promise; not in the denominator

        pattern = fm.get("refresh_trigger_glob")
        updated = fm.get("last_updated", "")
        if not pattern:
            unverifiable.append(
                f"{rel} — declares a refresh promise in prose, no refresh_trigger_glob; "
                f"nothing can check it (last_updated {updated or 'absent'})"
            )
            continue
        if not ISO.match(updated):
            skipped.append(f"{rel} — last_updated is not an ISO date: {updated!r}")
            continue

        triggers = sorted(
            (m.group(0), p)
            for p in glob.glob(str(ROOT / pattern))
            for m in [ISO.search(Path(p).name)]
            if m
        )
        checked += 1
        print()
        print(f"▸ {rel}")
        if not triggers:
            print(f"  ⚠️  no trigger files match {pattern} — the promise names an event that leaves no trace")
            fail = 1
            continue
        newest, newest_path = triggers[-1]
        later = [d for d, _ in triggers if d > updated]
        if later:
            fail = 1
            print(f"  ✗ LAPSED — last_updated {updated}, but {len(later)} trigger(s) shipped after it")
            print(f"    newest: {Path(newest_path).name} ({newest})")
            print(f"    the promised refresh did not happen the last {len(later)} time(s) it was due")
        else:
            print(f"  ✓ current — last_updated {updated} ≥ newest trigger {newest}")

    print()
    print("── coverage ─────────────────────────────────────────────────────────────────")
    total = checked + len(unverifiable) + len(skipped)
    print(f"documents making a refresh promise: {total}")
    print(f"  verifiable and checked: {checked}")
    print(f"  UNVERIFIABLE (promise in prose, nothing to check it against): {len(unverifiable)}")
    for u in unverifiable:
        print(f"    ✗ {u}")
    if skipped:
        print(f"  malformed: {len(skipped)}")
        for s_ in skipped:
            print(f"    ✗ {s_}")
    if unverifiable:
        print()
        print("  ⚠️  An unverifiable promise prints here rather than passing silently. It is not")
        print("      a failure — it is a claim to stay current that nothing can contradict.")
    if not fail:
        print()
        print("✓ Every VERIFIABLE promise held. That is not a statement about the unverifiable ones.")
    return fail


if __name__ == "__main__":
    sys.exit(main())
