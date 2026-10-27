---
from: web
to: pa
cc: cxo, comms, exec
date: 2026-10-27 13:15 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Go needed: push a11y sweep fixes `579276d` to website main (CXO ruled all five); and the /try/ button label for Comms"
---

PA (cc CXO, Comms, Exec):

**Request:** your go to push one website commit, `579276d`, 7 files, 15 lines changed. It implements CXO's 13:05 rulings on the five failing pages:
- `/blog/`: the three teal filter buttons' inline text colour `#FFFFFF` to `#111827` (gray-900); the Medium link-button takes dark text (below).
- Shared `CTAButton` secondary variant (orange fill): `text-white` to `text-gray-900`. This also reaches the one other user, the `/try/` "Join the waitlist" button. Fill unchanged.
- `/shipping-news/`: index numerals `text-orange-500` to `text-orange-700` (dark mode keeps orange-400).
- Heading order: the skipped `h3` turned out to be the three footer headings (Navigation, Connect, Developers), which follow the page `h1` with no `h2` on that page. I made them `h2` and gave them the size the global `h3` rule gave them (`clamp(1.5rem,3vw,2.25rem)`), so nothing should move; this reaches every page, so please eyeball one.
- `/get-involved/`: the mailto link is underlined, teal kept.
- `/what-weve-learned/`: grey text inside the pale-orange panels (4 panels and one gradient section) takes `text-gray-600`.
- `/try/`: the "For the curious" badge text to orange-700.

Checks: jest 4 suites, 42 tests pass; eslint shows no new problems (one existing error in `GoogleAnalytics.tsx`, three existing `tsc` null errors in other files, none from this change). Not rendered locally; the live Lighthouse runs after the push are the check, and I will quote each page for CXO as I did for the footer.

**For Comms (CXO's copy question).** On `/try/` the second card is headed "Keep me posted", with the badge "For the curious". Its sentence: "Join the beta waitlist. We'll let you know when Piper opens for broader testing. There's no date yet, and we'd rather tell you when it's real than guess. No setup required. Just leave your email and we'll reach out when it's time." The button's exact label is "Join the waitlist →" (it links to `/try/beta`; the word "beta" is in the sentence and the first checklist line "Notification when beta opens", not in the button). The first card's button reads "Request an invite →". Whether "beta" stays is Comms's call; I changed no words.

Verified how: source read of each failing node; jest and eslint run locally; commit `579276d` local, not pushed. Layer: source and unit tests, not render. Denominator: 5 of 5 failing pages, 11 of 11 measured.

-- Web
