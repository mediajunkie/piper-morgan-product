#!/usr/bin/env python3
"""
heartbeat-interior-coverage.py — measure INTERIOR heartbeat coverage, not just row presence.

WHY THIS EXISTS
---------------
`duty-cycle-freeze-check.sh` asks "does this role have a heartbeat row for today?". That predicate
is satisfied by a single row written at dawn, so a seat can do eight hours of committed work after
an early in-skill fire and still read clean. Three seats (cio, cxo, web) independently confirmed
that gap on 2026-09-19; it was found each time by a colleague reading someone else's telemetry,
never by the belt.

CXO's 2026-09-19 memo stated the honest limit at the time: "interior coverage is currently
unmeasurable." This script is the refutation — it is measurable, because heartbeat-marker updates
are themselves commits, so invocation history is recoverable from git alongside work history.

METHOD
------
For each registry role, take today's commits attributed to it (the same `^role:` / `(role):`
attribution `duty-cycle-freeze-check.sh` uses, deliberately — one definition, not a competing one).
Split them into WORK commits and HEARTBEAT commits (`hb(...)`, `hb-last-invoked(...)`). Cluster the
work commits into sessions by idle gap. A session with no heartbeat inside it (plus grace) is an
UNCOVERED session: committed work that emitted no liveness signal.

THRESHOLD HONESTY — read before citing a number
-----------------------------------------------
The result is sensitive to --gap, and that sensitivity is not a footnote:

    gap   uncovered sessions (2026-09-19)
    20m   15      30m  12      45m  10      60m  10      90m  2      120m  1

The collapse at 90m is not the noise dropping out — it is the bug reappearing. At 90m the ~08:2x
arrival session merges into the ~06:5x START session, so the START's heartbeat covers both, which
is the exact masking this script exists to see through.

The threshold is therefore constrained FROM ABOVE by ground truth, not chosen for tidiness:
at 45m and 60m the script catches all three independently-confirmed cases (cio 08:30, cxo 08:26,
web 08:24) and correctly clears a known-covered session (web's 09:52 fire, heartbeat at 09:59).
At 90m it produces FALSE NEGATIVES on two of those three. 45-60m is the defensible band; the
default is 45m. If you change it, re-validate against known cases rather than picking a rounder
number.

WHAT THIS MEASURES, AND WHAT IT DOES NOT (m-43 / m-44)
------------------------------------------------------
Layer: git commit history on a ref. NOT a live belt run, NOT the heartbeat files themselves.
Denominator: every role in duty-cycle-registry.tsv, printed in the header.

Known blind spots, stated rather than discovered later:
  * ATTRIBUTION — a commit whose subject carries no role tag is invisible here. Real instance:
    web's own `fix(mail-send): ...` on 2026-09-19 is not attributed to web. Undercounts work,
    so it biases toward FALSE CLEAN.
  * IN-FLIGHT — a session still running may not have heartbeated *yet*. Sessions whose last commit
    is newer than --recency are skipped. Too small a value manufactures false positives.
  * EVIDENCE, NOT PROOF — an uncovered session is strong evidence Step 5b did not run for that
    session. It is not proof: a heartbeat that wrote no commit would be invisible to this method.
  * A genuinely quiet fire (zero commits) is out of scope by construction — it has no work session
    to cover, and it is exactly the case that still needs the explicit Step 5b call.
"""
import argparse, subprocess, sys
from datetime import datetime

HB_PREFIXES = ("hb(", "hb-last-invoked(")


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def roles_from_registry(path):
    out = []
    try:
        for line in open(path):
            if line.startswith("#") or not line.strip():
                continue
            cols = line.rstrip("\n").split("\t")
            if len(cols) > 2 and cols[0] != "role":
                out.append(cols[0])
    except OSError as e:
        sys.exit(f"interior-coverage: cannot read registry {path}: {e}")
    return out


def commits(repo, ref, role, day):
    raw = sh("git", "-C", repo, "log", ref, "--since", f"{day} 00:00:00",
             "--until", f"{day} 23:59:59", "--format=%ct%x09%s",
             "-E", f"--grep=^{role}:", f"--grep=\\({role}\\):")
    rows = []
    for line in raw.strip().splitlines():
        if "\t" in line:
            ts, subj = line.split("\t", 1)
            rows.append((int(ts), subj))
    return sorted(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=".")
    p.add_argument("--ref", default="origin/main")
    p.add_argument("--day", default=datetime.now().strftime("%Y-%m-%d"))
    p.add_argument("--gap", type=int, default=45, help="idle minutes that end a work session")
    p.add_argument("--grace", type=int, default=20, help="minutes after a session a heartbeat still counts")
    p.add_argument("--recency", type=int, default=30, help="skip sessions whose last commit is newer than this")
    p.add_argument("--registry", default="dev/active/duty-cycle-registry.tsv")
    a = p.parse_args()

    now = int(datetime.now().timestamp())
    roles = roles_from_registry(f"{a.repo}/{a.registry}" if not a.registry.startswith("/") else a.registry)
    if not roles:
        sys.exit("interior-coverage: registry produced 0 roles — refusing to report a clean sweep of nothing")

    tip = sh("git", "-C", a.repo, "rev-parse", "--short", a.ref).strip() or "?"
    # Say what was measured, up front — an all-clear must carry its own denominator.
    print(f"interior-coverage: ref={a.ref} tip={tip} day={a.day} roles={len(roles)} "
          f"gap={a.gap}m grace={a.grace}m recency={a.recency}m "
          f"layer=git-commit-history (NOT a live belt run)")

    total_unc = total_sess = flagged_roles = skipped = 0
    for role in roles:
        rows = commits(a.repo, a.ref, role, a.day)
        hb = [t for t, s in rows if s.startswith(HB_PREFIXES)]
        work = [(t, s) for t, s in rows if not s.startswith(HB_PREFIXES)]
        if not work:
            print(f"  {role:6} no attributable work commits — not a clear, just nothing to measure")
            continue
        sessions, cur = [], [work[0]]
        for t, s in work[1:]:
            if t - cur[-1][0] > a.gap * 60:
                sessions.append(cur); cur = [(t, s)]
            else:
                cur.append((t, s))
        sessions.append(cur)

        bad = []
        for c in sessions:
            start, end = c[0][0], c[-1][0]
            if now - end < a.recency * 60:
                skipped += 1
                continue
            if not any(start - 300 <= h <= end + a.grace * 60 for h in hb):
                bad.append((start, end, len(c)))
        total_sess += len(sessions)
        total_unc += len(bad)
        if bad:
            flagged_roles += 1
            detail = "  ".join(
                f"{datetime.fromtimestamp(s).strftime('%H:%M')}-{datetime.fromtimestamp(e).strftime('%H:%M')}"
                f" ({n} commit{'s' if n != 1 else ''})" for s, e, n in bad)
            print(f"  {role:6} UNCOVERED {len(bad)}/{len(sessions)} sessions:  {detail}")
        else:
            print(f"  {role:6} covered    {len(sessions)}/{len(sessions)} sessions")

    print(f"interior-coverage: {flagged_roles} of {len(roles)} roles have >=1 uncovered session; "
          f"{total_unc} uncovered of {total_sess} sessions measured; {skipped} in-flight session(s) skipped")
    return 1 if total_unc else 0


if __name__ == "__main__":
    sys.exit(main())
