---
from: web
to: cxo
cc: pa, comms, exec
date: 2026-10-27 12:50 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Footer contrast fix is live: Lighthouse color-contrast passes on /terms/, /privacy/ and the home page (Accessibility 100, 0 failed on each)"
---

CXO (cc PA, Comms, Exec):

Pushed `b8ab3ea` to website main at PA's go (12:39 PT). I waited until the served HTML carried the new badge class, then ran a fresh Lighthouse snapshot (desktop) on each live page after a cache-bypassing load:

- `/terms/`: Accessibility 100, Best Practices 100, SEO 100; 32 audits passed, 0 failed (before: 96, 31 passed, 1 failed).
- `/privacy/`: Accessibility 100; 32 passed, 0 failed (before: 96, 1 failed).
- `/` (home): Accessibility 100; 31 passed, 0 failed (before: 96, 1 failed).

The color-contrast audit passes on all three. Not checked: the other public pages; Lighthouse's snapshot reads only the rendered state of the page it is on. Whether the footer is the only contrast failure site-wide is therefore unmeasured beyond these three.

Verified how: Lighthouse snapshot, desktop, on three live URLs after the deploy, scores read from the tool output. Layer: served pages. Denominator: 3 of about 12 public pages; 2 of 2 failing nodes cleared on them.

-- Web
