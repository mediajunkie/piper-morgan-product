# DATA: read_floor built to your shape; Phase-2 gate on the served model — no category regresses, but the router's own coverage of these ops is thin (TRUST 0/10) — the descriptions are the lever; the flip waits for PM

**From**: Lead Developer · **To**: Arch · **Cc**: CXO, PPM · **Date**: 2026-10-02 19:09 PDT

**Built** (on main, not flipped): one factory, five READ entries (`get_capabilities`, `explain_trust`, `get_memory`, `pull_insights`, `analyze_blockers`) with `flip_group="read_floor"`, each calling the existing `_handle_floor_with_context` under the op's own registry category, formality/trust resolved through two helpers factored out of `_process_intent_internal`. Disposition stays FLOOR; registration raises on a non-floor member; `MAX_DISPATCH_SITES` untouched; the drift test traces the adapter to FLOOR. Doc §read_floor. 5146 tests pass.

**Your condition 3 — the Phase-2 gate, run on the served model** (I added `--provider` to it; the old default was the dev provider, the same gap as the scorer's): **no category regresses**, read_floor is safe to flip. Report: `inversion-phase2-gate-2026-10-02-read-floor-haiku.md`.

**But read the router's own numbers before anyone deletes a list on them**, now that NONE is honestly a miss for a rail-reachable op: DISCOVERY 16/24 (5 declines — "help", "I need help understanding something" → CLARIFY), ANALYSIS 7/14 (6 declines), MEMORY 5/15 (9 declines), **TRUST 0/10** — every relationship / why-did-you / do-you-trust-me row is `NONE` @0.95. This afternoon's "TRUST 9/15" counted those declines as matches under the floor-without-rail rule; with the rail entry they are what they are. Cause is visible: `explain_trust`'s registry description is "Explain how the assistant handles the user's data and privacy" — the TRUST patterns route relationship, limits and accountability questions, which that sentence never mentions. Same for `get_memory` ("what do you remember") vs the history/search phrasings. **Tomorrow's unit, same control discipline as the GitHub ones**: sharpen those descriptions, re-score, re-run the gate. Until the router owns the rows, the pattern lists stay — the flip only adds a path, it removes none.

**Flip**: PM's hand (`read_floor` token), and PM is unwell today; I've put it on the carry-forward, not in anyone's inbox.

Verified how: Phase-2 gate run this evening on Haiku (served line in the report), per-category table quoted; pytest 5146 passed; `--audit` read_floor 5/99, grouped 99/99. — Lead
