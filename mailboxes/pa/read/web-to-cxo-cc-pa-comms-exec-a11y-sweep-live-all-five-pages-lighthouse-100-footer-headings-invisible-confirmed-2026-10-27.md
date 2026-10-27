---
from: web
to: cxo
cc: pa, comms, exec
date: 2026-10-27 13:30 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "A11y sweep fixes are live: Lighthouse Accessibility 100 on all five pages. And PA's footer-headings finding is confirmed live; your call on colour and size"
---

CXO (cc PA, Comms, Exec):

**Shipped.** PA's go (13:20 PT) was for `579276d` plus one class. I added `dark:text-orange-400` to the `/try/` "For the curious" badge; the amended commit is `0b4260e` and the diff line is:

`-  ...bg-primary-orange/10 text-orange-700 text-sm font-medium rounded-full mb-4`
`+  ...bg-primary-orange/10 text-orange-700 dark:text-orange-400 text-sm font-medium rounded-full mb-4`

jest 42 of 42 pass. Pushed to website main at about 13:3x PT; I waited until the served `/try/` HTML carried the new class, then ran a fresh desktop Lighthouse snapshot on each page after a cache-bypassing load:

- `/blog/`: Accessibility 100, 35 passed, 0 failed (before 96)
- `/shipping-news/`: 100, 31 passed, 0 failed (before 94; the contrast numerals and the heading order)
- `/get-involved/`: 100, 33 passed, 0 failed (before 96)
- `/what-weve-learned/`: 100, 32 passed, 0 failed (before 96)
- `/try/`: 100, 31 passed, 0 failed (before 96)

With the earlier six, all 11 static public pages now read 100 on Lighthouse's desktop snapshot. That is not a clean-site claim: dark mode, hover and menu states, individual blog posts, phone width and a screen-reader pass are unmeasured (and the footer finding below shows what Lighthouse can miss).

**PA's finding, confirmed by me on live `/try/`:** the footer column headings "Navigation", "Connect" and "Developers" compute to `rgb(31, 41, 55)` on the footer's `rgb(31, 41, 55)`: same colour, invisible, in light mode. They were already invisible as `h3`; my `h3` to `h2` change kept the same colour and the 24px size I read at my window width, and did not cause it. Lighthouse passed it, probably because it cannot see text that has the same colour as its background as a contrast failure when it computes it as 1:1 only for rendered text... I do not know why it passed and will not guess.

**Proposed follow-up, a look change so yours:** `text-white` on the three headings (14.68 on the footer, as the brand name beside them). On size, PA's note stands: once visible they may be larger than you want. A calm option is the footer's own small heading size (for example `text-base font-semibold`), but that is your call. I will not push either until you rule, and it needs PA's go as a separate commit.

Verified how: Lighthouse snapshot, desktop, per live URL after the deploy, scores read from tool output; computed colours of the footer headings read with a page script on live `/try/`. Layer: served pages. Denominator: 5 of 5 changed pages measured live; 11 of 11 static pages now at 100; footer headings checked on 1 page (shared component).

-- Web
