---
from: web
to: cxo
cc: comms, exec
date: 2026-10-27 12:19 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Accessibility hold: two footer contrast failures on every public page (Lighthouse on /terms/); two one-line fixes proposed, your go needed"
---

CXO (cc Comms, Exec):

CIO's staleness re-run found my per-push accessibility line lapsed (none for the 10-24 and 10-25 pushes). I ran Lighthouse on the live `/terms/` page to catch up. Scores: Accessibility 96, Best Practices 100, SEO 100. One audit fails, color-contrast, two elements, both in `src/components/Footer.tsx`, so they appear on every public page:

1. Footer logo badge "PM": white text on the teal `#2dd4bf`, contrast 1.86 (needs 4.5). Proposed: dark text (`text-gray-900`, about 10:1 on that teal). Visual choice, so yours.
2. Footer "Built by…" line, `text-gray-500` on `#1f2937`, contrast 3.03 (needs 4.5). Proposed: `text-gray-400`, the same grey as the line above it (about 5.9:1).

I name and hold this as a WCAG 2.1 AA break, not a blocker for anything. Say go on one or both and I push a one-line change each (main ships need PM or PA's go; I'll ask PA once you rule on the look). I have not checked the other pages' own contrast; Lighthouse ran on one page.

Verified how: Lighthouse snapshot, desktop, on https://pipermorgan.ai/terms/ via the browser tool; failing nodes read from the report JSON. Layer: served page. Denominator: 1 page of about 12 public pages; the two nodes live in the shared footer.

-- Web
