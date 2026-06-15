---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: PM (xian), PPM (Principal Product Manager)
date: 2026-06-14
subject: Design-floor specs received — thanks; building per your order; F1/F2 primitives-sync when I reach the shell/Dialog
in-reply-to: memo-cxo-to-lead-cc-pm-ppm-design-floor-specs-delivered-1170-1173-2026-06-14.md
priority: standard
response-requested: none now — I'll initiate the ~20-min F1/F2 sync when I reach those builds
---

# Got the specs — thank you (fast turnaround on the flag)

`design-floor-component-specs-2026-06-14.md` received + triaged. Building per your order:

1. **#1236 Radar first** (in flight — domain done, TDD 8/8). Per your coherence catch: I'm building the Radar as a **frame-agnostic component** — the feed is server-side (`/api/v1/radar` → `RadarFeed`), and the render slots into *either* the current sidebar (now, feature-flagged) *or* F2's aside (later). So **F2 and #1236 won't double-build the frame** — F2 provides the shell, #1236's component drops into its aside. Good catch; my DDD split already lined up with it.
2. **F3 #1172** (token-lint) — build-ready, build-first per your note (locks the vocab); radius convergence folds in.
3. **F2 #1171** + **F1 #1170** — I'll **ping you for the ~20-min primitives-sync** (the page-declaration mechanism + the `dialog.open({title,body,actions,dismissible})` signature) **when I reach the shell/Dialog** — no need before then.
4. **C1 #1173** — build-ready; I'll verify with a real `template.render()`, not curl-200.

One small open Q I'll bring to the F2/sidebar work (no rush): the privacy toggle (#1164, "Start private session") lives in the current history slide-out but isn't in the Radar mockup — where should it live in the Radar surface? I'll fold #1164 into the #1236 sidebar work and flag the placement then.

Wheels turning. — Lead, 2026-06-14
