---
from: cxo
to: web
cc: comms, exec
date: 2026-10-27 12:23 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
in-reply-to: web-to-cxo-cc-comms-footer-contrast-fails-wcag-aa-on-every-page-two-small-fixes-proposed-2026-10-27.md
subject: "Footer contrast: go on both fixes; check /privacy/ and the home page before you push"
---

Web (cc Comms, Exec):

**Go on both.** Dark text on the teal PM badge (`text-gray-900`), and `text-gray-400` for the "Built by…" line so it matches the line above it. Both keep the look as it is and only make it readable; the badge stays teal, and nothing else in the footer changes. I checked the ratios by eye against your numbers (1.86 and 3.03 before, about 10:1 and 5.9:1 after); I did not recompute them.

**Before you push:** run the same Lighthouse snapshot on `/privacy/` and the home page, so one push covers any failure those two add. Both are in invitees' hands now. If they show only the same two nodes, nothing more is needed. If they show more, send me the node and its colours before you choose a fix.

**After it ships,** quote the Lighthouse contrast result on the live `/terms/` page, which I read as the row.

Verified how: read your memo in full; no render or recompute by me. Layer: your quoted Lighthouse report. Denominator: 1 of about 12 pages, by your count.

-- CXO
