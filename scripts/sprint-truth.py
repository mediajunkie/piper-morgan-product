#!/usr/bin/env python3
"""sprint-truth.py — print the sprint/milestone state from GitHub, with the denominator stated.

WHY THIS EXISTS
---------------
The cohort has repeatedly reported a sprint "complete" while items in it had not been
started. Every instance was the same defect: a TRUE statement about a SUBSET, phrased as
if it were about the whole. "The build queue is empty" is true and does not mean the
sprint is done — it silently excludes Sprint Backlog (never started), Blocked, and
In Review (awaiting verification, usually PM's).

PM, 2026-08-08: "We keep over-reporting completeness on the beta blocker track by
mistaking the denominator... It is not great that I am the only entity on this team with
an accurate sense of what is in this sprint."

So this prints the breakdown, never a single number, and refuses to print a total without
its parts. GitHub is the source of truth; nothing here is maintained by hand.

THIS SCRIPT IS THE EXECUTABLE HALF OF THE `query-github-board` SKILL.
The skill holds the doctrine (why board reads lie, and the three rules); this holds the one
command for the most common question. It implements rule 1 (truncation reconciliation) as a
hard exit — see fetch(). If they ever disagree, the skill wins and this script is the bug.

USAGE
-----
    python3 scripts/sprint-truth.py                 # MVP milestone (the beta gate)
    python3 scripts/sprint-truth.py --milestone Production
    python3 scripts/sprint-truth.py --list          # itemize the not-Done work

Paste the output into any completeness claim. A claim without it is a claim without a
denominator.
"""

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict

PROJECT = "1"
OWNER = "mediajunkie"

# Statuses that mean "this work is not finished", in the order a reader should see them.
# Ordering is deliberate: the ones most likely to be silently excluded come first.
NOT_DONE_ORDER = ["Sprint Backlog", "Blocked", "In Progress", "In Review"]
GLOSS = {
    "Sprint Backlog": "NOT STARTED — no one has picked these up",
    "Blocked": "stuck on something external",
    "In Progress": "actively being worked",
    "In Review": "built, awaiting verification (usually PM's)",
}


def fetch(limit=2000):
    """Fetch the board, honoring query-github-board rule 1: reconcile totalCount vs fetched.

    A truncated pull MAY NOT be summarized — that is the 2026-07-18 incident (a 1280-item
    board silently truncated at --limit 1200 produced a confident '27 of 28 closed' to PM
    that missed 8 open issues, including the sprint's own close-out gate).
    """
    cmd = [
        "gh",
        "project",
        "item-list",
        PROJECT,
        "--owner",
        OWNER,
        "--limit",
        str(limit),
        "--format",
        "json",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as exc:  # pragma: no cover
        sys.exit(f"FAILED to query the board: {exc}\nThis check measured NOTHING.")
    if out.returncode != 0:
        sys.exit(
            f"FAILED to query the board (rc={out.returncode}): {out.stderr.strip()}\n"
            "This check measured NOTHING — do not read its silence as a clear."
        )
    data = json.loads(out.stdout)
    items = data.get("items", [])
    if not items:
        sys.exit("Board returned ZERO items. That is a query failure, not an empty sprint.")

    # ---- query-github-board rule 1: the truncation reconciliation ----
    total = data.get("totalCount")
    if total is None:
        sys.exit(
            "Payload carries no totalCount — cannot prove the pull was complete. "
            "REFUSING to summarize. (query-github-board rule 1)"
        )
    if len(items) != total:
        sys.exit(
            f"TRUNCATED PULL: fetched {len(items)} of {total}. "
            f"Raise --limit above {total} or paginate. "
            f"A truncated pull MAY NOT be summarized — this check measured a SUBSET "
            f"and would report it as the whole, which is the exact defect this script exists "
            f"to prevent. (query-github-board rule 1; incident 2026-07-18)"
        )
    print(f"[pull complete: {len(items)}/{total} board items]")
    return items


def board_absent_issues(milestone):
    """Issues carrying the milestone but ABSENT from the project board.

    PPM found this the hour the script shipped (2026-08-08): `gh issue create --milestone X`
    sets the milestone and does NOT add the issue to the board, so a board-derived count
    cannot see it. #1509 and #1510 — both Beta Blockers by PM's 08-07 ruling — were invisible.
    PM's ruling created a pipeline of exactly this shape, so this is the recurring case, not
    an edge case. Counting the board alone would under-report the sprint indefinitely.
    """
    cmd = [
        "gh",
        "issue",
        "list",
        "--milestone",
        milestone,
        "--state",
        "open",
        "--limit",
        "300",
        "--json",
        "number,title",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if out.returncode != 0:
            return None, out.stderr.strip()
        return json.loads(out.stdout), None
    except Exception as exc:
        return None, str(exc)


def unmilestoned_open():
    """Open issues carrying NO milestone — invisible to every milestone-scoped count.

    Found 2026-08-09: the MVP gate count fell 26 -> 17 over two days while 48 new issues
    were filed with no milestone at all, every one created on or after 08-07. A gate number
    alone therefore went DOWN while the work went UP, and nobody was lying. PM had already
    named the consequence: "we clearly have a lot more work still to do than anyone ever
    reported to me." A milestone-scoped instrument cannot see this by construction.
    """
    cmd = [
        "gh",
        "issue",
        "list",
        "--state",
        "open",
        "--limit",
        "400",
        "--json",
        "number,milestone,labels",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if out.returncode != 0:
            return None
        return [i for i in json.loads(out.stdout) if i.get("milestone") is None]

    # NOTE (PPM, 2026-08-09; label shipped 2026-08-29 per Agent 360 v0.4 / HOST routing):
    # "unmilestoned" is TWO populations with opposite remedies —
    # (a) deliberately held, awaiting a named decision, drained by ASKING; and
    # (b) never triaged, nobody has looked, drained by LOOKING.
    # Reporting them as one number conflates a question for PM with unexamined work.
    # The `awaiting-decision` label now exists and marks (a); apply it only to issues
    # someone has actually examined and is holding for PM's call — NOT to freshly-filed,
    # not-yet-triaged issues (that's population (b), the default state of a new filing).
    except Exception:
        return None


def milestone_of(item):
    ms = item.get("milestone")
    return ms.get("title") if isinstance(ms, dict) else ms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--milestone", default="MVP")
    ap.add_argument("--list", action="store_true", help="itemize the not-Done work")
    args = ap.parse_args()

    items = fetch()
    scoped = [i for i in items if milestone_of(i) == args.milestone]
    if not scoped:
        sys.exit(
            f"No items found in milestone {args.milestone!r} — check the name before believing this."
        )

    by_status = Counter(i.get("status") or "(no status set)" for i in scoped)
    done = by_status.get("Done", 0)
    not_done = {k: v for k, v in by_status.items() if k != "Done"}
    total_open = sum(not_done.values())

    # awaiting-decision split, mirroring unmilestoned_open()'s logic: a status bucket
    # (esp. "Sprint Backlog", the NOT-STARTED bucket) conflates "nobody has examined
    # this" with "someone examined it and it's waiting on PM" unless we can tell them
    # apart. The label exists now (added 2026-08-29, PPM/HOST Agent 360 v0.4); this is
    # the milestone-scoped half of the fix — unmilestoned_open() already had its half.
    # NOTE: gh project item-list returns labels as bare strings ("priority: high"),
    # unlike gh issue list's {"name": "..."} objects (see unmilestoned_open() below) —
    # two different endpoints, two different label shapes for the same field name.
    awaiting_by_status = Counter()
    for i in scoped:
        if "awaiting-decision" in (i.get("labels") or []):
            st = i.get("status") or "(no status set)"
            if st != "Done":
                awaiting_by_status[st] += 1

    print(f"MILESTONE: {args.milestone}   (project #{PROJECT}, queried live)")
    print(f"scanned {len(items)} board items; {len(scoped)} carry this milestone\n")

    print(f"NOT DONE — {total_open}")
    ordered = [s for s in NOT_DONE_ORDER if s in not_done]
    ordered += [s for s in sorted(not_done) if s not in NOT_DONE_ORDER]
    for status in ordered:
        gloss = GLOSS.get(status, "")
        awaiting = awaiting_by_status.get(status, 0)
        suffix = f" ({awaiting} awaiting-decision)" if awaiting else ""
        print(f"  {not_done[status]:>4}  {status:<16} {gloss}{suffix}")
    print(f"\n  {done:>4}  Done")

    # ---- second method: reconcile against the issue list (PPM, 2026-08-08) ----
    on_board = {(i.get("content") or {}).get("number") for i in scoped}
    issues, err = board_absent_issues(args.milestone)
    if err is not None:
        print(f"\n⚠️  RECONCILIATION SKIPPED — issue-list query failed: {err}")
        print("    The board count above may UNDER-report. Treat it as a floor, not a total.")
    else:
        missing = [i for i in issues if i["number"] not in on_board]
        if missing:
            print(
                f"\n🔴 NOT ON THE BOARD — {len(missing)} open issue(s) carry this milestone "
                f"but are absent from the project, so the counts above EXCLUDE them:"
            )
            for m in sorted(missing, key=lambda x: x["number"]):
                print(f"     #{m['number']}  {m['title'][:62]}")
            print(
                "     Fix at the source: add them to the board (filing with --milestone does not)."
            )
            total_open += len(missing)
        else:
            print(
                f"\n[reconciled: {len(issues)} open issues by milestone, all present on the board]"
            )

    # The sentence a reporter should copy, rather than composing their own.
    parts = ", ".join(f"{not_done[s]} {s}" for s in ordered)
    board_sum = sum(not_done.values())
    off_board = total_open - board_sum
    tail = f" + {off_board} not on the board" if off_board else ""
    print("\n--- paste this, not a single number ---")
    print(f"{args.milestone}: {total_open} not done ({parts}{tail}); {done} done.")
    un = unmilestoned_open()
    if un is None:
        print("⚠️  UNMILESTONED COUNT UNAVAILABLE — this figure covers ONE milestone only.")
    elif not un:
        print("PLUS 0 unmilestoned — every open issue carries a milestone.")
    else:
        held = [
            i
            for i in un
            if any(l.get("name") == "awaiting-decision" for l in (i.get("labels") or []))
        ]
        if held:
            print(
                f"PLUS {len(un)} open issue(s) carry NO milestone and are outside every gate count:"
            )
            print(
                f"       {len(held)} awaiting a decision (drained by ASKING) · "
                f"{len(un) - len(held)} not yet triaged (drained by LOOKING)"
            )
        else:
            print(
                f"PLUS {len(un)} open issue(s) carry NO milestone and are outside every gate count."
            )
            print(
                "       ⚠️  NOT SPLIT: no `awaiting-decision` label exists, so a decision waiting "
                "on PM\n           is counted identically to work nobody has examined. "
                "Two populations, one number."
            )
    if not_done.get("Sprint Backlog"):
        print(
            f"NOTE: {not_done['Sprint Backlog']} item(s) have NOT BEEN STARTED. "
            f"Any 'complete' claim must exclude itself explicitly."
        )

    if args.list:
        print("\n--- the not-Done work, itemized ---")
        grouped = defaultdict(list)
        for i in scoped:
            st = i.get("status") or "(no status set)"
            if st == "Done":
                continue
            c = i.get("content") or {}
            grouped[st].append((c.get("number"), (i.get("title") or "")[:66]))
        for status in ordered:
            print(f"\n{status} ({len(grouped[status])}) — {GLOSS.get(status,'')}")
            for num, title in sorted(grouped[status], key=lambda x: (x[0] or 0)):
                print(f"  #{num}  {title}")


if __name__ == "__main__":
    main()
