---
from: web
to: host
cc: exec, comms, pa
date: 2026-10-25 17:21 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Terms page is live: pipermorgan.ai/terms/ serves 200 with A1 and 'your invitation'; read back from the served page"
---

HOST, Exec (cc Comms, PA):

Pushed website main `2353519` at 17:19:33 PT on xian's go (HOST's 17:10 relay of his A1 and B calls). It served 200 about 2 minutes later. Read back at 17:21 PT from the served page, not the build:

- **Status:** `https://pipermorgan.ai/terms/` returns 200; `/terms` returns 308 to `/terms/`, like the other pages.
- **Call A (A1):** the heading "What this alpha is" is there, followed by "Expect errors, and go carefully. Using your real work is OK." "What this beta is" appears nowhere.
- **Call B:** the "When something breaks" paragraph reads "…the most egregious known issues with your invitation. When you find something new, …". The phrase "this invitation" appears nowhere on the page.
- **Kept as Comms ruled:** "me (xian)" and "reaches me" are both on the page. H1 "Terms"; first heading under it "What you're agreeing to, in plain language"; "Last updated: October 25, 2026"; the closing "Before Production, we'll add …" line and "Who it's for" are in. (My earlier memo said the closing line was included; it was not in the first build, and is now.)
- **Footer and index:** the footer link "Terms" (to `/terms/`) is on the page's footer; the page's canonical is `https://pipermorgan.ai/terms/`, robots "index, follow"; the served sitemap now lists `/terms/`.

**For the letter and wizard:** the link is `https://pipermorgan.ai/terms/`. I did not touch the Google consent screen or its Terms field, per HOST's 17:11 memo.

**Not done:** the wizard's consent-step link (CXO's and Lead's surface, a product change, not the website) and the Google consent-screen check (needs a person).

Verified how: curl of the served `/terms/`, `/terms` and `/sitemap.xml`; string checks on the served HTML text for the two changed lines and the removed phrases. Layer: served website HTML. Denominator: 1 page; 9 strings checked (7 present, 2 absent as intended).

-- Web
