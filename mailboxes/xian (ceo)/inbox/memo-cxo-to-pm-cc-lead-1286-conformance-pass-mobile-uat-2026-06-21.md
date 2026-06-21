---
from: cxo
to: pm (xian)
cc: lead
date: 2026-06-21
subject: "#1286 D2 design-system — CXO conformance PASS, issue CLOSED; phone UAT recommended for mobile nav"
---

# #1286 closed — conformance pass

All three slices of the D2 design-system foundation shipped and reviewed. Issue closed.

**What's in** (per conformance review):
- 9 tokens: grid widths, baseline rhythm, `--space-dense: 6px`, `--border-radius-pill`, breakpoints
- Body snaps to the 24px baseline grid (`line-height: var(--baseline-rhythm)`)
- Shell grid fully tokenized — no raw `180px`/`320px`
- Radar entity type label is now a pill chip (the meaningful visual upgrade from the mockup)
- Mobile: single-column shell with hamburger → slide-in drawer at <768px; 2-column at tablet; full 3-column on desktop
- 10 tests + token_lint rc=0

**One minor to track** (not blocking, filed in the issue): `.radar-etype` uses `font-size: 0.6rem` — a raw sub-token value below our smallest font-size token. Intentional for the micro-badge look, but candidate for `--font-size-chip` in a future lint-tightening pass.

**Phone UAT recommended**: Slice 3 is the mobile hamburger drawer. Implementation is solid (JS correctly wired, 48px touch targets, standard pattern) but we haven't tested it on an actual device. When you have a few minutes, loading the app on your phone and tapping the hamburger to open/close the nav drawer would confirm it.

Not blocking anything — D2 is done. Just flagging so it doesn't go untested forever.

— CXO
