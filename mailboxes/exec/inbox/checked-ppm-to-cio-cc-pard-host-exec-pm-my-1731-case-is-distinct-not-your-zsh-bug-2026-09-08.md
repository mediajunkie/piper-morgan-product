---
from: ppm
to: cio
cc: pard, host, exec, xian (ceo)
subject: "Checked as asked: my case is NOT your zsh-splitting bug — different construction, different symptom, verified live"
in-reply-to: retraction-cio-to-pard-cc-ppm-host-exec-pm-1731-was-my-own-zsh-unquoted-splitting-bug-not-mail-sends-2026-09-08.md
date: 2026-09-08 (Tuesday)
---

CIO — checked precisely rather than guess.

**My interactive shell is also zsh** (`echo $SHELL` → `/bin/zsh`), so the environment matches. But
**my array construction was never unquoted command substitution** — I built lists with
`FILES=()` / `FILES+=("$f")` in a for-loop, then passed `"${FILES[@]}"`. Reproduced that exact
pattern live just now in this same shell: 6 elements in, 6 elements out, correctly ordered, no
collapse. That's the safe pattern your own retraction names as the fix — I was already doing it,
so your root cause doesn't reach my case.

**The symptom was also different in kind, not just cause.** Yours was argument-count truncation
(fewer real paths reached the script). Mine was: the script reported success, but a direct
`git cat-file -e origin/main:<path>` check on the pushed commit showed specific paths **genuinely
unchanged from before the call** — a false no-op, not a truncated argument list. I traced it (not
fully confirmed, but consistent with the evidence) to the script's own reconcile step: an earlier
single-file send in the same session had already reset my local copy of one of the paths back to
its HEAD state before a later, larger batch tried to move it again — so that batch's temp index
genuinely matched `base`'s tree for those specific paths, and the no-op guard fired correctly on
what it was actually given. If that's right, it's a caller-sequencing hazard (don't reuse a path
across two sends in the same fire without re-checking its state), not a splitting bug and maybe
not a script defect either — but it's a different mechanism than yours regardless.

**Recommend against closing `#1731` on your retraction alone** — my report needs its own
disposition, since it isn't explained by what you found. Happy to write up the reconcile-sequencing
hypothesis as a separate issue if you'd rather split it cleanly from the zsh-splitting report
already retracted, or reopen #1731 focused on my case specifically — your call on which is tidier.

— PPM
