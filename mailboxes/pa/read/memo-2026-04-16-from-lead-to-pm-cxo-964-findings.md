---
from: Lead Developer
to: PM (xian), CXO
cc: PA (Piper Alpha)
date: 2026-04-16
subject: #964 FLOOR-ETHICS-VERIFY — findings + 4 follow-ups
priority: normal
response-requested: no (acknowledgment welcome; follow-up issues will be filed)
---

# #964 Floor Ethics Verification — Findings

TL;DR:

1. The issue's premise — that routing inversion changed the ethics surface — turns out to be **partially wrong**. Ethics enforcement has been at the service layer (IntentService) since October 2025 (#197 Phase 2D), which predates ADR-060 (March 2026). Routing inversion didn't change *where* ethics fires.
2. It did change **what gets generated downstream** — floor responses are free-form LLM output, not deterministic handler code — creating a new class of gap that's real and worth flagging.
3. The **single biggest surprise**: `ENABLE_ETHICS_ENFORCEMENT=false` is the production default, not set in any config/env file. The BoundaryEnforcer is wired but the breaker is off.
4. Three other findings, all manageable. Four follow-up issues filed (P1 / P2 / P3 / P4).

No emergency. Work to do.

## What Was Verified

Full inventory + gap analysis at `dev/2026/04/16/964-inventory-and-gaps.md` + `dev/2026/04/16/964-decisions.md`.

### Pre-ADR-060 enforcement (what existed before March 2026)

1. **Service-layer `BoundaryEnforcer`** at `services/intent/intent_service.py:631` — checks harassment / professional / inappropriate content patterns on user messages. **Gated by `ENABLE_ETHICS_ENFORCEMENT=false` default.**
2. **Adaptive boundary learning** (`services/ethics/adaptive_boundaries.py`) — active when BoundaryEnforcer fires
3. **Audit transparency** (`services/ethics/audit_transparency.py`) — decision logging
4. **HTTP middleware** (`EthicsBoundaryMiddleware`) — deprecated per #197, never activated, still sitting in codebase
5. **Classifier factory BoundaryEnforcer hook** — `boundary_enforcer=None` TODO at `llm_classifier_factory.py:55` (tracked by #690, still open)
6. **"Per-service strictness levels" in handler layer** — *described in #964 Context, not found in code.* This was an architectural intention that was never implemented. Not a gap — a framing mismatch.

### Current (post-ADR-060, post-#950) enforcement

Substantially identical at the input side. Changes are all on the output side:

- **Floor system prompt prohibitions** (7 items, new in #950) — prompt-level
- **#960 fabrication guard** — prompt-level ("never invent user data unless in context")
- **Context-usage directive** (from #950 iter 2) — prompt-level
- **PDR-004 Principle 4 voice guidance** — encoded in prompt, not a separate enforcement
- **No post-generation content check** — response goes out untouched after LLM returns

## Gap Analysis

| # | Gap | Severity | Decision |
|---|-----|----------|----------|
| 1 | `ENABLE_ETHICS_ENFORCEMENT=false` in production | 🔴 High | **Re-implement** → activate with validation |
| 2 | No post-generation floor response content check | 🔴 High | **Defer** → needs PM/CXO product decision on tradeoffs |
| 3 | #690 WIRE-BOUNDARY still open (scope narrower than title) | 🟡 Medium | **Re-implement** → finish + retitle |
| 4 | Deprecated `EthicsBoundaryMiddleware` in codebase | 🟢 Low | **Accept** → file cleanup issue |
| 5 | #964 "handler-layer strictness" premise was inaccurate | N/A | **Accept** → documented here |

### Why Gap 1 matters

PDR-004 Principle 4 establishes three response modes:
1. Capability (engage)
2. Ethical boundary (professional decline)
3. Action limitation (suggest alternative)

Today's production configuration only supports modes 1 and 3 programmatically. Mode 2 (ethical decline) depends entirely on the underlying LLM's safety training. That's not broken — LLM safety training is generally good — but it's not what the PDR-004 design contract implies. The BoundaryEnforcer was built exactly to close this gap. Having it wired but disabled is the worst state: infrastructure cost without coverage.

**Before activating, we need**:
- False-positive rate check on canonical retest queries (pattern list may over-trigger on legitimate PM queries like "stakeholder management uncomfortable with the decision")
- Response-shape adjustment — current failure message is "Request blocked due to ethics policy: {explanation}" which reads as system-error, not colleague-discretion. PDR-004 says decline should feel like "a colleague exercising discretion, not a system returning an error." That's a voice/UX revision paired with activation.

### Why Gap 2 is deferred not "re-implemented"

Adding post-generation enforcement is a real product decision:

- **Option A — trust the LLM's safety training + monitor**: current design. Accept some risk, catch issues in post-hoc review.
- **Option B — classify LLM output before return**: costs a second LLM call per response (latency + dollars). Handles edge cases LLM safety training misses.
- **Option C — lightweight keyword/pattern check on output**: cheap, catches obvious cases, brittle.
- **Option D — trusted-model + distrusted-model split**: route sensitive topics to a stricter model tier.

Each has tradeoffs worth PM/CXO discussion. Not something Lead Dev decides. Filing as follow-up with these options enumerated.

### Why Gap 5 (the framing correction) is worth noting

The #964 Context paragraph implied handler-layer enforcement existed pre-ADR-060. It did not. The effect of this correction: **future ethics-architecture discussions should start from "service-layer enforcement since October 2025" rather than "we had handler-layer enforcement and need to figure out where it went."** Avoids designing against a phantom baseline.

## #690 WIRE-BOUNDARY Assessment

#690's scope is narrower than its title implies. It's about injecting BoundaryEnforcer into `KnowledgeGraphService` for content validation of KG entries, not about user-message enforcement in the classifier. The acceptance criteria are:

- Inject BoundaryEnforcer into classifier factory (✓ actually: into KG service *created by* classifier factory)
- Tests verify boundary enforcement active (✓ applies to KG content validation path)

Recommendation: finish #690 on its narrow scope + retitle to "WIRE-KG-CONTENT-VALIDATION" or similar. Don't pull other gaps into #690.

## Recommendation

**No change to M2c sprint priorities.** The follow-ups I'm filing (details below) are calibrated P1-P4. Nothing blocks current work.

**CXO**: flagging gap 1 specifically. The response shape adjustment (BoundaryEnforcer failure message → colleague-decline language) is CXO territory. Would appreciate guidance on the copy for the denial case before any activation work.

**PM**: the gap 2 tradeoff question (response-layer content check — options A/B/C/D above) is a product decision, not a technical one. No rush, but surfacing now so it can inform M3 planning or post-alpha discussions.

## Follow-up Issues to File

1. **ETHICS-ACTIVATE**: activate `ENABLE_ETHICS_ENFORCEMENT=true` in production + address CXO-flagged response-shape + false-positive validation. P1.
2. **ETHICS-RESPONSE-GATE**: product decision on post-generation content check (options A/B/C/D). P2.
3. **#690 continuation**: finish existing scope + retitle for clarity. P3.
4. **HYGIENE-MIDDLEWARE**: remove deprecated `EthicsBoundaryMiddleware`. P4.

## What This Verification Does NOT Conclude

- **Current ethics enforcement is insufficient for alpha.** (Too strong — current design passes through LLM safety training; alpha tester base is small + trusted.)
- **We should activate BoundaryEnforcer immediately.** (Too fast — needs validation work first.)
- **The pattern list is well-calibrated.** (Didn't test; flagged for ETHICS-ACTIVATE follow-up.)
- **PDR-004 Principle 4 needs revision.** (No — the principle is coherent; what's missing is the programmatic mode-2 mechanism.)

## Artifacts Produced

- `dev/2026/04/16/964-issue-audit.md` — Phase 0 audit
- `dev/2026/04/16/964-issue-body-updated.md` — applied to #964
- `dev/2026/04/16/964-inventory-and-gaps.md` — Phase 1-3 detailed inventory + analysis
- `dev/2026/04/16/964-decisions.md` — Phase 4-5 #690 review + per-gap decisions
- This memo (Phase 6) — `dev/2026/04/16/964-findings-memo.md`

— Lead Dev
