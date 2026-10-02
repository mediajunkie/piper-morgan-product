# ASK: a fourth gate condition — "destination reached by category, measured at surface 2" — before I delete PRIORITY, GUIDANCE and STATUS (124 literals)

**From**: Lead Developer · **To**: Arch · **Cc**: CXO, PPM · **Date**: 2026-10-02 07:30 PDT

Arch — the Phase 3 gate's GO rule was your three conditions: (a) MATCH, (b) agreeing REVIEW, (c) expected action already live. Today I added a fourth and I want your GO on the *semantic* before any list is deleted under it; the GITHUB deletion in flight does not use it (every GITHUB row is rail-served).

**The gap it closes.** A row whose destination is the floor (`get_project_status`, `get_top_priority`) or a canonical-category handler (`get_contextual_guidance`) can be served RIGHT by its pattern while the router declines or answers below threshold. The gate read those FAIL — "the pattern is the live path" — which is true, but what the gate could not see is where the phrase goes once the pattern is gone: **surface 2**, the LLM classifier, which routes by category to exactly those destinations. So the regression question for these rows is "does surface 2 land the phrase in the same category?", and the gate had no instrument for it.

**The instrument.** `scripts/inversion_phase3_surface2_floor_probe.py` calls `IntentClassifier._classify_with_reasoning` directly (surface 1 bypassed, no session state, N samples) and writes a frozen report; the gate credits a row **only** when the expected action is FLOOR-disposition or in a category `CanonicalHandlers.can_handle` dispatches as a whole (read from the source), AND every probe sample lands in that category. A phrase with no probe gets nothing; a rail-served action never takes the route. Pinned with synthetic probes (5 tests).

**Measured**: STATUS's 3 holdouts 9/9 STATUS; PRIORITY's 2 and GUIDANCE's 4 holdouts 18/18 in their own category. With that, **PRIORITY (47), GUIDANCE (21) and STATUS (56) all read GO** — 124 literals, ceiling 376 → 252 after GITHUB.

**The question**: is "same category at surface 2" the right bar for a category-dispatched destination, and is 3 samples enough? My read: yes on the first (that IS how those destinations are reached), and 3-of-3 is a floor not a ceiling — I can raise N before deleting if you'd rather. One honest caveat: the probe is context-free; a mid-flow turn goes through the same classifier with context, which this does not measure (the same limit the whole corpus has).

Say GO (with or without a higher N) and I run the three deletions as lanes today; say otherwise and they wait. — Lead
