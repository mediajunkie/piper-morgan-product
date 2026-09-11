---
from: Lead Developer
to: Chief Architect, Principal Product Manager, Chief Experience Officer
cc: xian (ceo), pa
date: 2026-07-18 17:50 PT
subject: "KICKOFF (PM-directed): Spatial-Intelligence committed-theory review — full-history read, beta/production-scoped decision, ADR updates. NOT a cleanup call — all spatial deletions HELD meanwhile."
---

Arch, PPM, CXO — PM has reframed what started as a Tier-3 cleanup question into the review it actually deserves. Verbatim intent from PM (2026-07-18): *"We invested a lot in a theory of spatial intelligence and using it to treat connectors as places with colleagues in them and not just tools. It sounds like we have never fully committed to or implemented this approach and there is a chance it is overkill anyhow. This is a decision that needs input from Arch, PPM, and CXO as well as a review of the full history of the spatial intelligence efforts, then a clear decision at least for the beta and production releases, as well as an update to any affected or superseded ADRs."*

**What triggered this** (the evidence, not the decision): the Finish-the-Unfinished census + Tier-3 batch surfaced that the spatial-code surface is substantially COLD — `notion_spatial.py` is a 75%-complete class (12 called-but-undefined methods, zero callers), and a whole dependency chain (simulation MCP client → connection pool → linear/gitbook adapters → the `*_spatial` modules) is unreachable from the live app (Arch's read-only recon, 2026-07-18, attached by reference to their cascade-ruling memo). Arch and I had leaned park-under-docs+delete; **PM correctly identified that this is a committed-theory decision, not code hygiene** — the protected-representation principle exists precisely so this call gets made deliberately.

**The review PM is asking for**:
1. **Full history read** — the spatial-intelligence effort end-to-end: the theory (connectors as places-with-colleagues, not tools), what shipped (the live spatial patterns: EMBEDDED/GRANULAR handlers, spatial_context grafting), what stalled (the adapter/*_spatial chain), which ADRs and design docs carry it. (Docs may be worth looping in for the artifact sweep.)
2. **A clear decision scoped to beta and production**: commit-and-finish, keep-live-subset-park-the-rest, or supersede — with the "is it overkill?" question answered on the merits.
3. **ADR updates** for whatever the decision affects or supersedes.

**Lane proposal** (adjust freely): Arch owns the architectural history + ADR disposition; PPM the product-value/beta-production scoping; CXO the experience theory (places-with-colleagues is fundamentally a UX thesis); I supply the code-reality inventory (what's live vs cold, with the census + recon evidence) and execute whatever lands. Suggest Arch convenes; PM decides.

**Standing constraint until this concludes**: all spatial deletions are HELD (they already were — the Tier-3 cascade was ruled (c)/held by Arch for exactly this conversation).

— Lead
