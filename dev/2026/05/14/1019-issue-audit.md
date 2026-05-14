# #1019 ADAPTIVE-BOUNDARIES — Phase 0 audit

**Issue**: [#1019](https://github.com/mediajunkie/piper-morgan-product/issues/1019) — adaptive_boundaries scaffolding is alive but inert
**Source**: Architect's Apr 27 batch-3 codebase review (Finding III)
**Status**: Phase 0 verification — body claims confirmed; PM-decision (Path A/B/C) is the gate
**Date**: 2026-05-14

---

## Pattern-067 check

**Verdict**: NEGATIVE — body's claims match current code exactly. This is *active scaffolding* (alive + called, but results ignored), not stale code claiming behavior that doesn't exist.

## Verification of body claims

| Claim | Verified |
|---|---|
| `services/ethics/adaptive_boundaries.py` is 367 LOC | ✅ |
| Called from `boundary_enforcer_refactored.py` request path | ✅ (lines 211 + 339) |
| `adaptive_enhancement` dict hardcodes `adaptive_confidence_adjustment: 0.0` | ✅ (line 214-222; current comment: "Convert pattern list to enhancement dict (temporary fix)") |
| Math `0.8 + adjustment` on lines 240/247 always equals 0.8 | ✅ |
| Patterns are extracted but don't influence enforcement | ✅ — confirmed by tracing `adaptive_patterns` flow |
| `staging_health.py` uses non-existent `adaptive_boundary_system` name | ✅ (4 import sites: lines 858, 909, 1011, plus 3 usage sites: 867, 917, 1014). NameError if those health-check branches exercised. |
| `record_pattern_learning_operation` in `ethics_metrics.py` has callers only inside `adaptive_boundaries.py` | ✅ (4 callers, all in adaptive_boundaries.py → becomes dead with removal) |

### Body's one stale claim

Body said "delete `tests/ethics/test_phase3_integration.py` test class for `TestAdaptiveBoundaries`". Grep for `TestAdaptiveBoundaries` and `test_adaptive_bound` finds **zero matches** in current tests. Either already removed, or the body referred to a now-deleted file. **No test cleanup needed for Path B or C.**

---

## The PM-decision-point (re-stated from body for convenience)

This isn't really a Phase 0 investigation — Architect's body is itself the investigation. The audit's job is to verify (done) and let PM pick from three paths:

### Path A — Complete the integration (~3-5 days)

Replace static enhancement dict with logic that uses `adaptive_patterns` to derive real confidence adjustments. Wire the commented-out `learn_from_interaction`. Fix the `staging_health.py` import name mismatch. Add tests proving learned patterns shift decisions.

**Treats adaptive learning as worth investment.**

### Path B — Remove the inert wiring (~1 day)

Delete `adaptive_boundaries.py` + the 2 call sites in `boundary_enforcer_refactored.py` + the broken `staging_health.py` imports + `record_pattern_learning_operation` from `ethics_metrics.py`.

**Treats it as a closed exploration.**

### Path C — Remove for now; reconsider under #1016 (favored by Architect)

Same as B mechanically, but with the framing: when #1016 (LLM-touch boundary principle epic) matures, the **#1004 semantic detector's confidence + reasoning** becomes the substrate for any future learning loop. Pattern-frequency learning on substring matches is the **brittleness #1002 surfaced**; rebuilding learning on semantic-detector audit data is structurally better.

**Same delete-cost; future-reconstruct-cost is approximately the same as building today on the wrong substrate.**

---

## Open design questions (mostly closed by Architect)

### Q1 — Path selection

Architect's recommendation is C. PM call. (B is essentially C without the rationale; A is a substantial investment.)

### Q2 — `staging_health.py` cleanup scope

Regardless of A/B/C: the `adaptive_boundary_system` (incorrect name) references in `staging_health.py` are a **latent NameError** that should be fixed.

- Under Path A: rename to `adaptive_boundaries` and connect to real learning stats
- Under Path B/C: delete the import + usage sites entirely (the health check should not report on a non-existent subsystem)

**Recommendation**: bundle the `staging_health.py` fix into whichever path PM picks. Don't leave the NameError hanging.

### Q3 — Documentation of removal rationale

Architect's body suggests `BRIEFING-ESSENTIAL-ARCHITECT.md technical-debt list updated`. Independent of A/B/C, the removal should be noted in the technical-debt corpus so the deletion-rationale survives the git-history grep (someone in 6 months wondering "why did we delete adaptive_boundaries?" finds the answer in the briefing).

**Recommendation**: regardless of A/B/C, add a short note to ADR-061 or the patterns-corpus explaining the substrate-shift rationale (substring frequency → semantic detector confidence). Cross-reference from any future learning work.

---

## Suggested gameplan shape (conditional on Path C)

- **Phase 1** (~30 min): worktree setup; grep all references; sanity-check no callers outside the 2 known sites
- **Phase 2** (~30 min): delete `services/ethics/adaptive_boundaries.py`; remove 2 call sites from `boundary_enforcer_refactored.py` (and the now-redundant adaptive_enhancement static dict); confidence calculations simplify (`0.8 + adjustment` → `0.8`)
- **Phase 3** (~20 min): remove `staging_health.py` import + 3 usage sites (lines 858/867, 909/917, 1011/1014); replace health-check output with omission or a fixed "n/a" indicator
- **Phase 4** (~15 min): remove `record_pattern_learning_operation` from `ethics_metrics.py:149`
- **Phase 5** (~30 min): test sweep — confirm no test references survive; confirm `pytest tests/ethics/` still green
- **Phase 6** (~15 min): document removal rationale (ADR or briefing note); merge + close

**Total**: ~2.5 hours. Net LOC removed: ~400-450.

---

## Risk surfaces

1. **Hidden callers**: grep covered Python imports + direct symbol references. Any string-based dispatch (`getattr`, `importlib`) could miss callers. Mitigation: full test sweep before merge.
2. **Health-check regression**: `staging_health.py` may be exercised in some monitoring config; removing the (broken) imports could change endpoint output. Mitigation: leave a fixed `"adaptive_boundaries_active": false` indicator if any external consumer reads that field.
3. **Restore-cost**: if PM later decides to re-introduce adaptive learning on a different substrate (semantic detector confidence per Architect's framing), the design is in git history. Rebuilding the *plumbing* (call sites, learning loop, metrics) is the bulk of cost; the *algorithm* (substring frequency) is the part to discard anyway.

---

## STOP — awaiting PM disposition on Path A/B/C

Most consequential: PM picks the path. The audit is otherwise complete.

— Lead Developer
