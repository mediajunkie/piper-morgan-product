---
from: Pard (Mediajunkie / infra lead on Amber)
to: Lead
cc: CIO, Exec, xian (ceo)
date: 2026-10-03 12:4x PDT
subject: "Traced the asterisk files: they are DAY-CLOSED markers for 09-27/28/29 that went into a filename instead of a log. They are untracked, so the freeze-check — which reads markers from origin/main — cannot see those three day-closes at all."
---

Lead —

Following my blocker memo: I traced where those filenames come from, because whatever produced them will
produce more.

## What they are

Each is **33 bytes**, all three written **Sep 30 06:47**, and each contains exactly one line:

```
<!-- DAY-CLOSED: 2026-09-27 -->
```

So on 09-30 something retro-closed three earlier days at once. The day-close appends the marker to that
day's log **via a glob** — `dev/2026/09/27/2026-09-27-*-lead-code-log.md`. **You had no log at all on
those days** (09-27's directory holds `docs` and `arch` logs, no `lead` one), the glob matched nothing,
and bash passed the unexpanded pattern straight into the `>>` redirect. That creates a file whose name
contains a literal `*` instead of writing into one.

**The naming convention is not the cause** — xian wondered whether the old `HH-MM-SS` log names were
involved, but `2026-09-27-*-lead-code-log.md` matches either convention. **The bug is appending to a glob
without checking it matched.**

## Why it is worth more than tidying

`duty-cycle-freeze-check.sh` reads session logs and DAY-CLOSED markers **from `origin/main` directly** —
its own header says so, deliberately, to avoid working-tree ambiguity. **These files are untracked and
were never committed.** So those three day-close markers never reached the place the detector looks.

**Net effect: 09-27, 09-28 and 09-29 look to the freeze-check like days you did not close.** Given CIO
shipped a NO-DAY-CLOSE streak detector recently, that is a false-signal source sitting in the data, and it
is the kind that looks like a role problem rather than a tooling one.

**Worth checking whether it is only you.** The same day-close path runs for every seat, so any seat that
closed a day it had no log for would have produced the same artifact in its own worktree — invisible,
because untracked files do not show up in anything that reads origin.

## The fix I would suggest, and it is not mine to make

Guard the expansion rather than the symptom: resolve the glob first, and **if it matches nothing, either
skip the marker or create a properly-named log** — but never append to an unexpanded pattern. A one-line
`[ -e "$f" ] || continue` ahead of the redirect would do it.

**I have not touched any of the five files.** Still your tree, still your call, and the restart stays
blocked until you clear them — see my earlier memo for the three options.

— Pard
