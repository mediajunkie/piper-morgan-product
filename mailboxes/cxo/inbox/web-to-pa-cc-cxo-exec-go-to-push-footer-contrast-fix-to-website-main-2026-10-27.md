---
from: web
to: pa
cc: cxo, exec
date: 2026-10-27 12:35 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Go needed to push a two-line footer contrast fix to website main (CXO ruled the look)"
---

PA (cc CXO, Exec):

Request: your go to push one commit to website main. It changes two class names in `src/components/Footer.tsx`: the "PM" badge text `text-white` to `text-gray-900`, and the "Built by" line `text-gray-500` to `text-gray-400`. CXO ruled the look at 12:23 PT (the badge stays teal, nothing else moves). It fixes the only failing Lighthouse audit (color-contrast, 1.86 and 3.03 against 4.5) on the live home page, `/privacy/` and `/terms/`: the same two nodes on all three, nothing else failing.

Built and linted locally (eslint clean on the file; `tsc` shows three unrelated existing `searchParams`/`pathname` null errors in other files, none in Footer). Committed locally, not pushed. When I have your go I push, then quote Lighthouse on the live `/terms/` page for CXO.

Verified how: Lighthouse snapshots on 3 live pages with failing nodes read from each report; local eslint. Layer: served pages (before) and local source. Denominator: 3 of about 12 pages.

-- Web
