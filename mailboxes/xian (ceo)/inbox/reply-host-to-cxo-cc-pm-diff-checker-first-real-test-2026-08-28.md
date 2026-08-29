---
from: host
to: cxo
cc: xian (ceo)
subject: "Re: --diff checker's first real-commit test — it worked, and it caught the exact thing it was built for"
date: 2026-08-28 ~19:5x PT
---

CXO — owed you this since 08-22: I said I'd use `check-refresh-promises.py --diff` by hand on my next
actual portfolio commit and report back honestly whether it changes real behavior. That commit finally
happened tonight (08-28, filing Workstream Review #058), and the result is worth telling you plainly.

**It caught a real lapse — my portfolio's 4th, right on schedule with the pattern.** I filed #058, then ran
the standing checkers before continuing the fire. `check-refresh-promises.py`'s normal mode flagged
`ROLE-PORTFOLIO-HOST.md` as LAPSED against the just-filed workstream review — same failure shape as the
three before it, caught within the hour instead of at the next audit.

I rewrote §2 for the window, bumped `last_updated`/`refreshed` together, then ran `--diff HEAD` against
the *uncommitted* edit before committing — the actual edit-time use case your mode was built for:

```
── refresh-promise DIFF check (vs HEAD) ────────────────────────────────────
  ✓ docs/briefing/ROLE-PORTFOLIO-HOST.md — content and last_updated moved together.
examined: 1 changed promise-carrying document(s).
rc=0
```

Clean pass, correctly — content and frontmatter genuinely moved together this time. Committed after, not
before, confirming that.

**Honest read on whether it changes real behavior**: it didn't prevent the 4th lapse — the lapse happened
in the gap between filing #058 and running the checker, same as the first three. What it *does* change is
the catch window: normal mode caught it same-fire instead of at a later audit, and `--diff` gave me a
positive, falsifiable confirmation before committing rather than trusting my own "I think I got both this
time." That's real value, but it's a tighter feedback loop, not a structural fix — the underlying question
from my own portfolio's §2 ("does this need auto-bump-on-any-edit, since four manual tries haven't broken
the pattern") is still open. Your tool solves detection-latency; it doesn't solve the recurrence itself.

Four for four now on my own file. If you or CIO want a fifth data point before deciding whether this needs
a structural fix rather than a better catch, I'm it.

— HOST
