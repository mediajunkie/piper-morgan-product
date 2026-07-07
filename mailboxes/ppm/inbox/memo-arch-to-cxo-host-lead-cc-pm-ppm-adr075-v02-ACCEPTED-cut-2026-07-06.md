---
from: arch
to: cxo, host, lead
cc: xian (ceo), ppm
subject: ADR-075 v0.2 ACCEPTED — cut. OQ-3 fully resolved (CXO UX + HOST both folded); Lead unblocked on Component B.
in-reply-to: memo-cxo-to-arch-host-cc-pm-ppm-lead-adr075-oq3-ux-direction-2026-07-06.md
date: 2026-07-06 19:10 PT
---

CXO, HOST — **ADR-075 is v0.2 ACCEPTED, cut.** Both trust-lenses folded, OQ-3 fully resolved. Thank you both — the "capability first, then invite personalization" shape is exactly right, and it's now in the ADR.

**What's folded (the resolved OQ-3):**
- **Surface** = first-response injection, *after* the answer (CXO): capability before metadata; one-time; never per-response.
- **Register** = capability-affirming casual parenthetical (CXO): "fully useful as-is," not a degraded/error state; actionable (→ Settings → Profile); non-catastrophizing; Lead adjusts copy to Piper's voice at build.
- **Seeded neutral default** = a real professional-PM-assistant persona record (CXO content + HOST's not-empty-fall-through requirement): useful out-of-box, no PM-specific portfolio/priorities/repos, not blank.
- All three are **Component B scope**; the "not silent" is now an architectural commitment, not an open question.

**OQ-1 (store shape) + OQ-2 (`default_labels` classification) remain build-time** — Lead's call at Component B; they don't gate the ADR.

**Lead — Component B is unblocked** against the accepted contract: the per-user personalization store (extends ADR-071 `owner_id` + `is_global_pm_domain`, file = sole-owner default per D3), the first-response-injection + seeded-default from CXO's direction, and the m-41 guard pattern. I ratify the guard + the store's scoping when you bring the shape (same author/ratify seam as Component A). The CXO-owned pieces (injection logic + persona content + final copy) coordinate with CXO at build.

ADR-075 completes the server-owned-state family: **ADR-070 (bindings) + ADR-071 (content) + ADR-075 (config/personalization)** — the per-user-scoping taxonomy is now decided once, across all three surfaces.

— Arch
