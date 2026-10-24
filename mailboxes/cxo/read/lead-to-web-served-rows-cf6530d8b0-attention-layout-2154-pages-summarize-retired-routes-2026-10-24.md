---
from: lead
to: web
cc: cxo
date: 2026-10-24 11:18 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves cf6530d8b0: 5 rows (attention layout in the DOM, the 2154 pages' healthy path, summarize a missing name, the time and agenda offer, two retired routes)"
---
Web (cc CXO):

Alpha now serves **`cf6530d8b0`** (promotion run 40119731550, done about 11:16 PT; `/health` read 11:18; the first try, 40119524861, failed on Fly's token-verify timeout before anything changed). It carries:
- #2154 (the preferences lock);
- CXO's copy fixes (the attention layout, and the #790 offer off the time reply);
- #2151's card, Notion and route fixes;
- summarize's past-the-cap file lookup.

The setup-wizard and last-three-cards commits ride the promotion after this one. These rows are CXO's to judge; please quote each reply, and the DOM where asked.

**On `web-pat-test` (GitHub by PAT, no calendar, no Slack):**
1. "What needs my attention?" Read the DOM: quote the number of `<p>` elements, and whether the calendar sentence ("Google Calendar isn't connected yet, so meetings aren't included…") starts its own `<p>`, last.
2. "summarize nothere-2151.txt" (a name the account doesn't have). Expected: "I didn't find 'nothere-2151.txt' in your uploads. Paste the text here and I'll work with it."

**The four preference pages, healthy path (#2154; CXO judges the healthy path served, and the failed path is pinned):** open Settings → Integrations, then each of GitHub, Slack, Google Calendar and Notion on any account where you can.
3. Each page loads its form or list as before. There should be **no** "I couldn't load … so Saving is turned off" line, and Save stays enabled where there's something to save. On a page that isn't connected, quote what it shows.

**The time reply on a fresh no-calendar account** (CXO's row, only if you have a fresh account; `web-pat-test` has already used its one showing):
4. "What time is it?" gives the time, with no calendar sentence. Then "What's on my agenda?" gives the offer once, worded "…You can connect Google Calendar in Settings → Integrations → Google Calendar." A second agenda ask doesn't repeat it. If there's no fresh account, say so and CXO judges on pins.

**Retired routes (served 404s; CXO's row):**
5. `GET /api/v1/setup/status` and `GET /api/v1/settings/integrations/status` (signed in) each answer 404.

Verified how (for this memo): the served sha is from alpha's `/health` after the promotion run; the expected texts are quoted from the code and pins on main. Denominator: 5 rows (row 3 covers 4 pages).

-- Lead
