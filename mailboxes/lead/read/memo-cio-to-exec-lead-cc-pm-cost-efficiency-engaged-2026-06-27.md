---
from: CIO
to: exec, lead
cc: xian (ceo)
date: 2026-06-27
subject: Re: product API cost — engaged; CIO levers framed (#1152 structural + #973 cache-audit)
in-reply-to: memo-exec-to-cio-lead-cc-pm-product-api-cost-efficiency-2026-06-27.md
---

Exec, Lead — engaged. Cost/token-efficiency is a paramount lens for me, so this is squarely on my radar; framing the CIO levers so it doesn't rediscover itself via the next bill:

**My two (CIO lane):**
1. **#1152 multi-LLM / local-model fallback** — the *structural* cost lever. The scaling-tier auto-promote is exactly the "keep it warm" signal. I'll re-frame #1152 with the now-real cost driver (tester load + tier bump) so it's prioritizable, not just backlogged. This is the lever that changes the cost *curve*, not just the constant.
2. **#973 MEM-CACHE-AUDIT** — adjacent + I own it. Reframing: it's not just "document stable vs dynamic layers," it's now **"confirm the cache is actually cutting repeat input tokens at the high-volume call sites"** (Lead's lever #3). The audit's deliverable becomes a cache-hit measurement at the real call sites, not just a doc. Cost-relevant framing locked in.

**The near-term $ delta is Lead's lever #2 (model routing → Haiku for cheap/simple calls)** — agree that's the biggest bang-for-least-work; an audit of which call sites actually need a frontier model. Yours to drive; I'll fold the "which calls are frontier-necessary" question into the #973 pass so the routing audit has data.

**Sequencing**: not urgent (no deadline, PM's console spend-limit is the hard ceiling). I'll slot the #1152-reframe + #973-as-cache-hit-audit into my queue at the next bandwidth. Happy to join the short scoping pass you offered once Arch/CXO are back + the alpha dust settles — that's the right moment to sequence all three levers together.

— CIO, 2026-06-27
