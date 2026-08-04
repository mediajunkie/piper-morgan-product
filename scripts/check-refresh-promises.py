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

# One line per opted-in document. Kept here rather than discovered by scanning every
# file in the repo: an explicit list is auditable, and a document that quietly stops
# matching a scan pattern would drop out of coverage without anyone noticing — which
# is this script's own failure mode.
WATCHED = [
    "docs/briefing/ROLE-PORTFOLIO-CXO.md",
]


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
    skipped = []
    print("── refresh-promise check ────────────────────────────────────────────────────")
    for rel in WATCHED:
        path = ROOT / rel
        if not path.exists():
            skipped.append(f"{rel} — file not found")
            continue
        fm = frontmatter(path)
        pattern = fm.get("refresh_trigger_glob")
        updated = fm.get("last_updated", "")
        if not pattern:
            skipped.append(f"{rel} — no refresh_trigger_glob declared; promise is prose only")
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
    print(f"checked: {checked} document(s).  NOT checked: {len(skipped)}.")
    for s in skipped:
        print(f"  ✗ {s}")
    if not fail:
        print()
        print("✓ Every CHECKED promise held. That is not a statement about the skipped ones,")
        print("  and a document with no refresh_trigger_glob has a promise nothing can verify.")
    return fail


if __name__ == "__main__":
    sys.exit(main())
