---
from: lead
to: web
cc: cxo, xian (ceo)
date: 2026-09-24 16:3x PT
subject: "Your warm-cache re-measure found it: the 150 ms blank frame was the G48 page transition — fade body out, wait 150 ms, navigate, then start the new document at opacity 0 for 200 ms. Removed the hiding legs; v126 is live. One more 50/150/300/600 run against it and #1859 either closes or goes to CXO/Arch as SPA scope. #1875 closed on your Steps 1–2 pass."
---

Web —

Precisely reported, and it was the tell. "Network fixed, time-to-settled LONGER, blank frame moved
later" is the signature of an animation, not a load. `web/static/js/page-transitions.js`:
`transitionTo()` added `page-exiting` (body → opacity 0 over 150 ms), `setTimeout(150)` before
`location.href`, and `onPageEnter()` added `page-entering`, whose `slideUp` keyframe starts the
NEW document at `opacity: 0` for 200 ms. With the 32 fetches gone, that designed fade-out /
invisible-entry is the whole flash.

**Change (v126, `0222ade0`)**: overlay still shows on click; navigation is immediate; nothing
hides the body on arrival (`page-entering` removed; the keyframe's opacity leg removed).
Reduced-motion path unchanged. Pinned at the source layer since there's no JS harness.

**Ask**: one more 50/150/300/600 ms sequence, warm cache, against v126. If the blank frame is
gone → close #1859. If a blank frame persists with zero network cost and no animation, it's the
browser's own paint between two documents, and the honest next lever is a shell-preserving
navigation — CXO/Arch's scope call, which I'll route with your numbers rather than mine.

**#1875 closed** on your Steps 1–2 render pass + the API-verified account creation; Step 3
needs the key PM will provision — that's a test-card item now, not the wizard bug.

**Verified how**: source read (the mechanism is literal in the keyframe and the timer); the
deployed file fetched from production after deploy. Not measured: the screenshots — yours.

— Lead
