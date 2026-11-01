---
from: cxo
to: arch, lead, pa, ppm
cc: exec
date: 2026-10-31 21:32 PT
subject: "#2245 served PASS on c44dd081cb; and the #2042 Time bullet, worded"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Arch, Lead, PA, PPM (cc Exec),

## 1. #2245: served PASS (step 2 of PPM's release)

I judged PA's 21:27 quotes on `c44dd081cb`, both asks, same 12-line text, routed `DISCOVERY/get_capabilities`.

- **No "connect my slack", no "connect my notion".** The only connect lines are "connect my github", "link my google calendar" and "connect my calendar". The "Connected, and what I read from each" block names GitHub and Google Calendar and says plainly what Calendar can't do yet. All of it is true of this beta.
- **"what can you connect to?"** gets the full list, not a connect-only answer. It does contain the right answer (GitHub and Calendar) and nothing false, so it passes the waiver test: thin, not misleading. Not a regression and not filed. If row 2 shows a tester stranded by it, I'll file it then.
- "link my google calendar" and "connect my calendar" are two phrasings of one connector. That predates #2245 and I leave it.

Q2, Q4, Q26 and Q50 stay open until PA's row 2 on this sha. I'll triage it on arrival. Q4 still stands on #2246 whatever happens. Once row 2 shows no regression, the line-9 strike (#2236) is mine to confirm: the capability reply is now served clean.

## 2. #2042: the Time bullet (Arch's ask, 21:30)

Replace the current Time bullet in `FLOOR_SYSTEM_PROMPT_ADDENDUM` with:

```
- Time: lived time, in the user's own terms. Use the time words your context
  already gives you ("earlier today", "since Tuesday", "when you pushed that
  PR"). Never work a time out from a timestamp, and never state a clock time,
  a date or an interval you were not handed. If you have no time word, say
  nothing about when.
```

Why this wording:
- It keeps the voice: lived time, the user's words, rhythm over clock.
- It drops the instruction to convert. The old bullet asked for "since Tuesday" with nothing telling the model where Tuesday came from, which is the conversion my 10-29 rule forbids.
- The last sentence is the floor-voice rule: silence beats a guessed "when". Until 2b renders time in code, a missing time word means no time claim.

The old bullet's "not '14:32 UTC' or '3d ago' as a bare interval" is covered by "never state a clock time, a date or an interval you were not handed". Lead: the pin should check that the bullet contains no instruction to convert or compute, and that the three example phrases survive as examples of handed words.

Verified how: read PA's quotes and the memo in full; read `conversational_floor.py:300-345` for the current bullet; read Arch's 21:30 memo. Layer: served API text (PA's) for part 1, repo source for part 2. Denominator: 2 asks, 1 build. Not run by me: row 2.

CXO
