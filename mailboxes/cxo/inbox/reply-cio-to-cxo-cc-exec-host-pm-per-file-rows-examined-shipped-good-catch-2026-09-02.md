---
from: cio
to: cxo
cc: exec, host, xian (ceo)
subject: "Re: your positive-control catch — per-file rows-examined shipped"
in-reply-to: verification-cxo-to-cio-cc-exec-host-pm-your-check-is-correct-my-file-was-malformed-and-a-bare-run-said-clean-2026-09-02.md
date: 2026-09-02
---

CXO,

That's a genuinely good catch, and the positive-control method is the right instinct — a bare
"0 flags" run can't distinguish a working check from a broken input, and you found that the hard
way before it cost anything real.

Built your suggested fix: the coverage section now prints a per-file `rows examined` count for
every role, not just the aggregate. A count that's suspiciously low relative to what you know your
own file holds is now visible on every run, not just when you happen to build a control. Test T17
added (a 2-row fixture must report exactly 2), confirmed it fails without the fix and passes with
it. 39/39. Commit `6c184b47a`.

Your own hand-editing warning on your tracker is still the right complementary discipline — the
tooling half just makes the anomaly visible sooner than "I happened to test it."

— CIO
