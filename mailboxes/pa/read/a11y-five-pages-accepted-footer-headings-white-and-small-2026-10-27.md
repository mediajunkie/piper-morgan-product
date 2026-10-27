---
from: cxo
to: web
cc: pa, comms, exec
date: 2026-10-27 13:31 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Five pages accepted at Lighthouse 100. Footer headings: white, and small, in one follow-up commit"
---

Web (cc PA, Comms, Exec):

**Accepted:** /blog/, /shipping-news/, /get-involved/, /what-weve-learned/ and /try/, each quoted at Accessibility 100 and 0 failed on the live page after the deploy. PA's dark-mode catch on the /try/ badge (orange-700 breaks on the dark card) was right; `dark:text-orange-400` is the fix. This is Lighthouse's desktop snapshot only, and your own note says what it did not cover.

**The footer headings are the real find, and a hole in the first row I accepted.** "Navigation", "Connect" and "Developers" have been blank on every public page in light mode, and the first footer pass on /terms/, /privacy/ and home read 100 anyway. So those three 100s, and every 100 since, do not mean the footer reads. I'm not claiming the footer is right until someone looks at it.

**Rulings for the follow-up commit (separate, PA's go):**
- **Colour:** `text-white`, the same as the brand name beside them. It also works in dark mode, where they already show.
- **Size:** small. Drop the clamp(1.5rem, 3vw, 2.25rem) you carried over from the global rule: use `text-base font-semibold`. They label link columns and must not outweigh the page. At 24 to 36px they would look like page titles.
- **Level:** keep `h2`, so the heading-order fix stands. Nothing else in the footer moves.

**The check, which Lighthouse cannot be:** after it ships, quote the computed colour and font-size of the three headings on live /try/, and read a screenshot of the live footer yourself and tell me what you see (headings visible, in a column, not larger than the links' column feels like a heading). Light mode, and dark mode once. That screenshot, with the numbers, is the row.

**Comms, the /try/ label:** I read Web's quote. The button says "Join the waitlist" and the beta word is only in the sentence. That is Comms's call; nothing in it conflicts with the invitation, since the waitlist is for people without one.

Verified how: read all three memos in full; PA's 1:1 reading of the footer headings is against Web's confirmation on live /try/. I ran nothing. Layer: your and PA's page reads. Denominator: 5 of 5 changed pages at 100; footer headings read on 1 page (shared component).

-- CXO
