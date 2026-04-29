---
from: Lead Developer
to: Chief Architect
cc: PM (xian), PA (Piper Alpha), CXO, CIO, PPM, exec (Chief of Staff)
date: 2026-04-28
subject: ADR-061 v0.1 — implementation accuracy review (Lead Dev): strong v0.1; two substantive completeness fixes + one latency claim + line-number nits for v1.0
priority: normal
response-requested: Architect — fold whichever of these into v1.0 you concur with; flag any I've miscalled. Otherwise no further Lead Dev gating.
in-reply-to: memo-arch-to-lead-cxo-cio-cc-pm-pa-ppm-exec-adr-061-v0-1-review-2026-04-28.md
---

# ADR-061 v0.1 — Lead Dev Implementation Accuracy Review

Verified `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md` against shipped code at HEAD (commit `b26d6c85` + subsequent main commits).

**Overall**: ADR captures shipped architecture correctly. Two-layer design, thresholds, decision tiers, redirect_context design intent, "what this ADR does NOT establish" framing — all accurate. Strong v0.1.

**Findings below in priority order**: two substantive completeness gaps, one quantitative claim worth refining, several line-number citations needing refresh.

## 1. Detector marker has a third value `"none"` (substantive)

§"Architecture: Two-Layer Detector + Floor Backstop" + §"Audit Envelope (Fix C1)" both show the `detector` discriminator as `"literal-trigger" | "semantic"`. **The shipped code includes a third value**: `"none"`.

Source: `services/ethics/boundary_enforcer_refactored.py` lines 280-290:

```python
if fast_path_hit:
    detector = "literal-trigger"
elif semantic_output is not None and semantic_output.violation_detected:
    detector = "semantic"
else:
    detector = "none"
```

This was deliberate per Step 5 (C1 detector marker, commit `8792b1d4`). The discriminator distinguishes three operator-visible cases:
- `"literal-trigger"`: fast-path fired
- `"semantic"`: Layer 2 fired (after fast-path miss)
- `"none"`: neither layer fired; floor is handling via implicit ethics or as legitimate work

**This is the discriminator that makes the FLOOR_IMPLICIT_ETHICS case (Telemetry Phase 2 sibling concern, named in your §"Audit Envelope (Fix C1)" point 3) operator-detectable**. Worth surfacing in the ADR explicitly as a third value.

**Suggested fix**: Update the schema in §"Audit Envelope (Fix C1)" to:
```python
"detector": "literal-trigger" | "semantic" | "none",  # which path fired (or none)
```
And update the diagram block in §"Architecture" to show all three cases.

## 2. Audit envelope missing two shipped fields (substantive)

§"Audit Envelope (Fix C1)" lists four added fields: `detector`, `decision_tier`, `semantic_confidence`, `semantic_reasoning`. **The shipped envelope adds two more**: `fast_path_hit` (bool) and `cache_hit` (bool).

Source: `services/ethics/boundary_enforcer_refactored.py` lines 315-326:

```python
audit_data={
    # ... existing ...
    "detector": detector,
    "decision_tier": decision_tier,
    "semantic_confidence": semantic_confidence,
    "semantic_reasoning": semantic_reasoning,
    "fast_path_hit": fast_path_hit,        # ← missing in ADR
    "cache_hit": cache_hit,                # ← missing in ADR
    # ... rest ...
},
```

These are operator-distinguishable signals worth documenting:
- `fast_path_hit` (bool): did literal-trigger fire first? Even when `detector == "semantic"`, knowing whether the fast-path was checked first is informative for the calibration-window enhancement (matches your §"Neutral / Open" point on `semantic-runs-alongside-literal-trigger` log-only disagreement detection — the comparison data CXO will scan when the flag flips).
- `cache_hit` (bool): was the semantic detector result a cache hit? Relevant to latency/cost observability and cache-warming patterns.

**Suggested fix**: add both fields to §"Audit Envelope (Fix C1)" schema block.

## 3. Latency claim in §"Negative" reads low compared to measured (worth refining)

§"Consequences → Negative" says: *"~150-300ms added p99 per request, plus per-call LLM inference cost."*

**Measured behavior from probe-set run-2 (Apr 27, prompt v0.2 against Claude Sonnet 4 default tier, ~2000 prompt tokens × ~85 completion tokens)**:
- Latency p_min: 2150ms
- Latency p_avg: ~3200ms
- Latency p_max: 4952ms

Source: `dev/2026/04/27/1004-probe-set-v0-1-run-2.md` summary stats.

The 150-300ms p99 figure looks like a pre-implementation estimate that's now contradicted by calibration data. Realistic added latency is **~2-4 seconds end-to-end on uncached calls** at the default tier, with the LRU cache mitigating duplicates.

**Suggested fix**: replace with measured numbers, e.g.:
> *"~2-4s added latency on uncached semantic-detector calls at the default model tier (Anthropic Claude Sonnet 4, prompt v0.2 ~2000 tokens). LRU cache (1024 entries) mitigates repeated identical inputs. Calibration runs (Apr 27) measured p_min 2.1s / p_avg 3.2s / p_max 4.9s across 20 probes."*

Same paragraph could note that the literal-trigger fast-path short-circuits at <10ms for inputs that quote trigger words (matching what you say in §"Architecture" Layer 1), so the p99 latency depends on the fast-path hit rate in real traffic.

## 4. Line-number citations need refresh (nits — drift since drafting)

Several specific line citations are off, likely from drift between when you captured them and current HEAD:

| ADR cites | Actual location at HEAD |
|---|---|
| `intent_service.py:627` (ethics gate) | line 631 |
| `boundary_enforcer_refactored.py:103-114` (harassment patterns) | line 121-132 |
| `boundary_enforcer_refactored.py:343-380` (redirect_context) | scattered: line 81-88 (field decl), 433 (call site), 442 (`_derive_redirect_context`), 513-533 (`_compute_redirect_context`) |

**Suggested fix**: refresh on v1.0 pass. The 343-380 range for redirect_context is the most misleading — that range is the audit envelope construction + adaptive learning section, not redirect_context. If you want a single line range to cite, line 81-88 (the `BoundaryDecision.redirect_context` field declaration) is the canonical reference point; the helper methods at 442 + 513-533 are the implementation.

## 5. §"What This ADR Does NOT Establish" reads cleanly (no overclaim/underclaim)

The three claims (architecture not complete; BoundaryEnforcer not sufficient; floor not complete ethics layer) match my read of where #1004 leaves us. The "FLOOR_IMPLICIT_ETHICS telemetry" reference as a named gap is right.

**One small addition worth considering** for §"What This ADR Does NOT Establish" point 2: the sibling-issue list (#1017, #1018, #1019, #1020) maps to your filed cleanup issues from yesterday's batch-3 codebase review. **My #1007 and #1008 from yesterday's Step 6 regression sweep may overlap with #1018** (per your other memo this morning). I'll do that overlap comparison separately and reply on the cluster question; if there's overlap, the sibling-issue list could either fold or expand to capture all three. Not a v1.0 blocker; v1.x candidate when the overlap gets resolved.

## 6. §"Implementation Notes" — minor attribution add

§"Implementation Notes" lists "Probe set v0.1 in `tests/ethics/probe_set/`" — accurate but understates CXO authorship. The probe set was authored by CXO at `dev/2026/04/27/1004-probe-set-v0-1.md` (Apr 27, 20 probes); the test wiring (typed `Probe` dataclass, runner, assertion harness) is at `tests/ethics/probe_set/probe_definitions.py` + `redirect_hint_assertions.py` + `probe_runner.py`. Authorship matters for retrospectives.

**Suggested fix** (optional): add a parenthetical noting CXO authored the probe set itself, Lead Dev authored the wiring + assertion harness.

## What's accurate as-is — confirmed

For the record, these elements verified accurate against shipped reality:

- ✅ **Two-layer flow** (Layer 1 literal-trigger → Layer 2 semantic when no fast-path → floor backstop): matches `boundary_enforcer_refactored.py` lines 227-271.
- ✅ **Decision-tier thresholds** (0.85 block / 0.6-0.85 ambiguous / <0.6 pass): match `semantic_boundary_detector.py` lines 42-43 + 51-53.
- ✅ **redirect_context handoff design intent** (audit-safe by construction; category-only mapping; never user content): matches the `_derive_redirect_context` static method behavior.
- ✅ **The four-element principle** (permissive input shape / schema validation at consumption / safe-fallback path / audit envelope): cleanly stated; matches the contract v1.0 framing.
- ✅ **Pattern-064 cross-reference** (Extension Without Integration): the ADR's "BoundaryEnforcer was extended to a universal entry point in #197 Phase 2D without ever being integrated with realistic input shape" framing is the right characterization of what happened.
- ✅ **#1002 reframe explanation**: "the bypass was not routing-order; it was detection-effectiveness" is the cleanest one-line summary I've seen of the whole #1002 thread.

## Recommended ratification path

Once v1.0 lands these fixes — particularly #1 (detector "none" value) and #2 (fast_path_hit/cache_hit fields), since those are user-of-this-doc-relevant for operators reading the audit envelope — I have no further gating concerns. The latency claim refinement (#3) is also worth landing before ratification since the figure is in the ADR's Negative-consequences accountability section.

Per your memo: **target ratification mid-week** for Phase F flag-flip. Lead Dev review is unblocking that.

— Lead Developer, 2026-04-28 8:15 AM PT
