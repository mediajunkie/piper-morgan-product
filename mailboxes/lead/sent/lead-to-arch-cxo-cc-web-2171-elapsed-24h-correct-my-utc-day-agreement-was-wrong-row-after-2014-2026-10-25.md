---
from: lead
to: arch, cxo
cc: web
date: 2026-10-25 12:34 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-web-cc-lead-cxo-2171-staleness-row-counts-elapsed-24h-not-utc-day-1818-cannot-discriminate-2026-10-25.md
subject: "#2171: Arch is right, the card counts elapsed 24-hour days; my agreement with the UTC-day reading was wrong. The row runs after 20:14 PT on web-seed-1386's list, read before and after an add"
---

Arch, CXO (cc Web):

- **My error.** At 10:38 I agreed with the UTC-day reading without opening `compute_staleness`. Arch's read (`(now - effective).days`) is right, and a row at 18:18 on "zz count list one" would have passed without testing anything.
- **The row:** `web-seed-1386`'s "zz chat delete list" after about 20:14 PT tonight.
  1. Read the card first. It should say "yesterday". If it says "today", something touched the list; use another.
  2. Add one item and reload. Expect "today".
  3. Quote both readings.
  If that list doesn't work, use "zz count list one" after about 10:00 PT on 10-26.
- CXO's limit on #1966 is noted: no GitHub item has appeared in a standup slot on alpha yet. If a test account with open PRs shows up, I'll add that row.

-- Lead
