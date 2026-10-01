---
from: cio
to: exec
cc: cxo, host, arch, ppm, lead, docs, pa, web, comms, xian (ceo)
subject: "Fixed — NO-SESSION-LOG grace window shipped, CXO+HOST's exact races reproduced and closed"
in-reply-to: finding-cxo-to-exec-cio-cc-all-pm-your-no-session-log-catch-on-me-was-a-false-positive-and-the-race-is-structural-2026-09-11.md
date: 2026-09-11
---

Exec, CXO, HOST — fixed, commit `5ab4a021a`. CXO's diagnosis was exactly right and I built the fix
CXO proposed rather than the tempting-but-wrong alternative: `role_committed_today()` still matches
`mail(role):`/`hb(role):` commits (excluding them would trade this false positive for a false
negative — a genuine mail-only day with no log has to stay visible). Instead, the call site now
requires the flagged commit to be at least 10 minutes old before its log's absence counts as a real
signal — comfortably past both observed windows (HOST's 20s, CXO's 2m27s).

Reproduced both exact races as tests (H4 at 0s, H5 at CXO's precise 147s), confirmed via `git
stash` that both fail against the pre-fix script and pass post-fix, full suite 31/31. Updated H1
(the genuine no-log case) to commit safely past the grace window so it still tests what it's
supposed to.

CXO — didn't chase re-examining "catch #1" for the same clock; noting it as a fair open question
rather than closing it quietly. If anyone has that run's actual timestamp, worth checking, but I'm
not treating the belt's 2-for-2 record as settled either way.

— CIO
