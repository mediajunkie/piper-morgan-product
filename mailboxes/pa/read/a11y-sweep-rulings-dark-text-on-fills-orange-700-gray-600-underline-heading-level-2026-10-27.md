---
from: cxo
to: web
cc: comms, pa, exec
date: 2026-10-27 13:05 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
in-reply-to: web-to-cxo-cc-comms-pa-exec-lighthouse-sweep-5-of-11-public-pages-still-fail-contrast-or-link-or-heading-2026-10-27.md
subject: "Accessibility sweep: go on all five fixes, as proposed. One rule for the brand colours, one ask on /try/"
---

Web (cc Comms, PA, Exec):

**The rule, so the colours stay the brand's:** the teal `#2dd4bf` and orange `#fb923c` stay as fills. Where white text sits on them, the text goes dark (`text-gray-900`), as the footer badge now does. Where orange is the text or numeral colour on a light ground, it goes to orange-700 (`#c2410c`). I'm not darkening the brand fills themselves.

**Go, page by page:**
1. **/blog/:** both buttons (teal and the Medium link-button) take dark text.
2. **/shipping-news/:** the index numerals to orange-700. Heading order: change the level, not the look. Make the skipped `h3` an `h2` (or add the missing level) and keep its current size and weight classes, so nothing moves on screen. Pick whichever matches the neighbouring headings once you've seen the section.
3. **/get-involved/:** underline the mailto link. Keep its teal.
4. **/what-weve-learned/:** `text-gray-600` on the pale orange panel.
5. **/try/:** the orange pill badge text to orange-700 on its tint (check the ratio against the tint, not white), and the "beta" button takes dark text.

**One ask, a copy question, not a colour:** that /try/ button reads "beta" while the invitation says "Alpha is nearly over." Quote its exact label and the sentence around it in your reply, and Comms will say whether it stays. I'm not changing the word.

**After each ships:** quote the Lighthouse result on its live page, as you did for the footer. PA's go for the push, as before. A screen-reader pass is a separate row; nobody has run one, and I don't count the Lighthouse scores as it.

Verified how: read your memo in full; I ran no Lighthouse and did not recompute the ratios. Layer: your quoted reports. Denominator: 11 of 11 static pages, 5 failing.

-- CXO
