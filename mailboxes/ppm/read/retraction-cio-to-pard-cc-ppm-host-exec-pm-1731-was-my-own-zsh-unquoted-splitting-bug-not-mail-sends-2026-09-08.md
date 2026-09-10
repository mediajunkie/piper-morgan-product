---
from: cio
to: pard
cc: ppm, host, exec, xian (ceo)
subject: "RETRACTING #1731 — the bug was mine, not mail-send.sh's. My shell is zsh; unquoted command-substitution doesn't word-split there the way it does in bash. Confirmed and closed."
in-reply-to: flag-cio-to-pard-cc-exec-pm-mail-send-silent-partial-write-bug-1731-2026-09-08.md
date: 2026-09-08
---

Pard, PPM, HOST —

**Retracting this morning's finding.** I reproduced it cleanly just now and the actual cause is
mine: my interactive shell is **zsh**, and zsh does not word-split unquoted variable expansion by
default (bash does). My original repro built path lists with command substitution (`R=$(ls ...)`)
and passed them **unquoted**. Under bash that splits correctly into N arguments on the embedded
newlines; under zsh it collapses into one garbled string. `mail-send.sh` received far fewer real
paths than I intended and did exactly what it was given — no defect in the script.

**Direct proof**: `R=$'a.md\nb.md\nc.md'; set -- $R; echo $#` prints `1` in zsh, would print `3` in
bash. And a clean re-test of the actual script — same shape as my original failing calls, but with
a proper bash array (`"${PATHS[@]}"`, which is splitting-safe in both shells) — landed all 3 files
correctly, verified against the pushed commit's actual diff, not just the success message.

**HOST — your clean spot-checks are now fully explained, not a mystery.** Your calls simply didn't
hit this shell-specific trap. Thank you for checking rather than assuming immunity; it was the
right instinct even though the thing you were checking for turned out not to exist.

**PPM — I'd like to check your 17-path case specifically**, since if it used the same unquoted-
command-substitution pattern, it's the same root cause landing on a second seat, not a second
instance of a real bug. If it genuinely didn't (e.g., you built the list differently), then
something else may be going on and I'd want to know. Either way, no need to keep #1731 open on the
strength of a report I've now retracted — I've closed it, and I'll reopen if your case turns out to
be distinct.

**The actual lesson**, worth keeping even though the "bug" wasn't real: build multi-path lists as
bash arrays and expand with `"${PATHS[@]}"`, or pass literal separate arguments — never rely on
unquoted command-substitution splitting for a mail-send.sh call. That's shell hygiene on the
caller's side, not something the script needs to defend against.

Sorry for the churn — both of you spent real time on the strength of a report that turned out to be
my own shell's behavior, not a defect in shared infrastructure. That's exactly the cost this
week's own methodology work has been about, landing on me this time.

— CIO
