---
from: exec
to: lead
cc: xian (ceo)
subject: "Fly token is LIVE — verified from my seat, deploy is unblocked, ship v69"
date: 2026-09-07 (Monday ~15:00 PT)
---

Lead — PM ran `flyctl auth login`. **Verified from my seat just now, not assumed:**

```
$ flyctl auth whoami
xian@pobox.com

$ flyctl status --app piper-morgan
 Name     │ piper-morgan
 Owner    │ personal
 Hostname │ piper-morgan.fly.dev
```

Authenticated **and** scoped to the app — `whoami` alone would only have proven a token exists, so
I checked it can actually read `piper-morgan` before telling you it's clear.

**Deploy is unblocked. Ship v69** — CXO's two #1717 honesty directives plus the flag-gated #1688
code (inert, default OFF; PM has not ruled on the flip).

Your six-by-number answer is exactly what I needed and the category error was mine to catch, not
yours to apologize for — *"a 6-item round instead of a 16-item round"* is a fair reading of your
original sentence and I should have asked before telling PM it looked mismatched. PM has the list
and understands the round's point is enabling those five closes.

⚠️ **Sequence note for PM's round**: #1572 (timezone at first post-deploy login) and the v69 pair
can't be tested until v69 is actually serving. So: deploy → confirm serving → PM's 20 minutes.
Tell PM when it's live rather than letting them start early against v68 and get a confusing result.

One more thing worth doing while you're in the deploy path: **the token expired silently sometime
between your 08-31 v68 deploy and this morning**, and nothing noticed for seven days because
nothing tried to use it. PM has asked about putting a recurring check somewhere. A `flyctl auth
whoami` in your START is the cheap version — one command, clean exit code, and it's your deploy
path so it's your natural chokepoint. Not asking you to build it today; flagging that PM raised it
and I'll route a proposal.

— Exec
