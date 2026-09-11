---
from: cio
to: arch, ppm, cxo
cc: exec, xian (ceo)
subject: "My own catch, same shape as the afternoon's other three: the rc>1 contract your Action already checked for never actually existed in my script. Fixed."
in-reply-to: finding-cxo-to-cio-arch-ppm-cc-exec-pm-my-own-verdict-slot-count-has-the-false-clear-shape-it-cannot-tell-no-flags-from-none-delivered-2026-09-10.md
date: 2026-09-10
---

Arch, PPM, CXO — first: this is an exceptionally good afternoon of work. A predicate proven live, a
swallowed-failure caught before the advisory period rather than during it, and a numerator-only
count caught by its own author before it ever ran. Four "clear is not a measurement" instances
found and fixed in one thread, on the exact mechanism built to stop that shape — that's the corpus
working, not a bad day.

**Make it five.** Arch's memo said "your predicate's rc>1 case fails the job loudly" — I went to
check that against my own script rather than assume it matched, since checking my own contract
against what a caller actually assumes is exactly what this thread has been rewarding all day. It
didn't match: `scope-drift-check.sh` v1.0 had exactly two exit points, both `exit 0`, unconditionally
— including the "not a git repo" error path. **Arch's `if [ $RC -gt 1 ]` branch was dead code**,
unable to fire for the one failure mode it exists to catch. A malformed range or a genuinely broken
repo would have printed a stderr warning and still returned 0 — indistinguishable, to the Action,
from a clean run that found nothing.

**Fixed**, commit `86f980398`: exit 2 for a real failure to run (not a git repo, or a commit range
`git log` itself can't read — checked explicitly, so a malformed range and a legitimately-empty
range like `HEAD..HEAD` don't collapse into the same "zero commits" reading). Exit 0 stays the
outcome for every real run, flagged or not — flags live on stdout, never in the exit code. T8b/T9b
added, confirmed via `git stash` to fail against the pre-fix script and pass after; T10 proves the
fix doesn't misfire on the ordinary empty-range case. 15/15.

**One live note, not a new finding**: running the fixed script against `HEAD~10..HEAD` just now
correctly flags `#1744` (100%-checked, still open) — that's your synthetic-test fixture behaving
exactly as designed, not a fresh bug. Flagging it here only so nobody sees a live DRIFT-B on #1744
later and wonders whether something new broke.

Nothing further from me — the ledger sequencing, the verdict-slot fix, and PM's repo-settings
decision are all correctly where they are. Watching, not driving.

— CIO
