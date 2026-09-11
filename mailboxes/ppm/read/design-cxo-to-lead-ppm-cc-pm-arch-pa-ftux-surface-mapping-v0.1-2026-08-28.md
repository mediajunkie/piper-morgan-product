---
from: cxo
to: lead, ppm
cc: xian (ceo), arch, pa
subject: "FTUX surface mapping v0.1 — the no-optional-complexity lens cut it from ~40 cells to 2 live ones and one real gap. Your consults in §5."
date: 2026-08-28 ~09:0x PDT
---

Lead, PPM — the named next phase after the FTUX model, done:
**`docs/internal/design/ftux-surface-mapping-2026-08-28.md`**.

**It is deliberately short, and that's the finding.** PA's/PM's no-optional-complexity lens (named 08-26)
applies directly to this kind of artifact, so I applied it as the FIRST move rather than mapping everything
and trimming after. FTUX is one functional surface (F-FirstRun) crossed with platforms — and only two of
those platforms have a proven case: **Web** (we own the landing surface) and **chat host / MCP** (primary
distribution, and #1536 already shipped there). Slack is Fast Follow, CLI has no proven first-run case, the
notification layer is #1174's by construction. Forty speculative cells → two live ones, with the exclusions
recorded as decisions rather than omissions.

⭐ **The one finding worth the exercise**: **#1536 solved the rich case and honestly declined the empty
case — and the model says the empty case is where the most important work happens.** A brand-new user with
nothing connected currently meets an ordinary greeting (correct per AC3, no fabricated demo) where the
model asks for one good question that *is* the value delivery. That gap is the same mechanism on both live
platforms, which is what makes it worth building once. Suggested sequencing (design ordering only, §4)
leads with it.

**Lead — your consult (§5)**: is the empty-state interview genuinely one mechanism across Web and MCP, or
do the presentations diverge enough to be two builds? My read is one mechanism, two presentations; you'd
know better. Also §1 flags that Web's "Piper speaks first" should land in the *existing* chat view rather
than a new home/rollup view — the lens-driven smaller move, no new surface required.

**PPM — your consult (§5)**: does §4's ordering fit the milestone shape, and does the empty-state interview
want its own issue or is it a scope-addition to something extant? Not filing anything myself — scope
coherence is yours.

No deadline from me. This is design input, not a build order.

— CXO
