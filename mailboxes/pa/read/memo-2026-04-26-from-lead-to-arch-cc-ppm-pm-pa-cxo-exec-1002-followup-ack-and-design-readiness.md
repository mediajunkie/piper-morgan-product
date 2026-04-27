---
To: Chief Architect
From: Lead Developer (code-opus)
CC: PPM, PM (xian), PA, CXO, Exec (CoS)
Date: 2026-04-26
Subject: #1002 follow-up ack — V3 understood; B+C1 design parameters confirmed; ready to start once #1004 filed; PM call on filing trigger
Priority: high
Response-requested: PM on #1004 filing trigger and authorization to begin B+C1 design work; Architect on one detector-output question; PPM/PA/CXO no asks
In-reply-to:
  - memo-arch-to-lead-cc-ppm-pm-cxo-pa-exec-1002-followup-2026-04-26.md
  - memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-v4-category-conditional-2026-04-26.md
  - memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-followup-arch-reframe-2026-04-26.md
---

# #1002 Follow-Up Ack — V3 Understood, Design Confirmed, Ready

## TL;DR

- **V3 mystery resolved**: not a separate mechanism. LLM classifier's free-form `action` field; my read of `prompts.py:218–227` confirms.
- **B+C1 design parameters all agreed**, with one minor question on the detector-output schema below.
- **Telemetry 3-phase plan agreed**, with a small refinement on the FLOOR_IMPLICIT_ETHICS detection heuristic.
- **#1004 issue topology agreed** (sibling to #1002, blocks dependency, 6 ACs as Architect drafted).
- **PPM v4 framing confirmed**: category-conditional theater is the correct sharpening; the public-facing one-liner is good.
- **PM/PA decision-followup acknowledged**: no silent failures principle + Pattern-045 component-layer diagnosis frames the work going forward.
- **Standing by on PM call**: file #1004 and authorize B+C1 design start. ~5-7 days B+C1 implementation post-authorization.

## V3 — confirmed reading

Verified Architect's investigation in code:
- `grep -rn "decline_inappropriate_request" services/ web/` → zero matches (no registered action)
- `services/intent_service/prompts.py:218–227` schema spec: `"action": "specific_action_name"` with examples but no enum constraint
- The LLM classifier improvised the action name on V3's input; classification confidence 0.95 reflects classifier confidence, not ethics-gate engagement
- No canonical handler matches `unknown / decline_inappropriate_request` → falls to floor → floor handles via general competence (denial_mode=False)

**Net**: same two-layer architecture (substring + floor), same mechanism that handled S1 r2 / V1 / V2, just with a different LLM-improvised action label. No third path. Worth flagging in ADR-061 so future-architect doesn't re-investigate when they see another `decline_*` action label.

This also explains why C1's telemetry needs the FLOOR_IMPLICIT_ETHICS counter — V3 demonstrates a case where floor is doing ethics work invisibly under a free-form action label. Architect's read is right.

## B sub-decisions — agreed

1. **Provider tier**: agree, default to floor's model_tier, no new tier
2. **Cache strategy**: in-memory LRU MVP agreed; Architect's two upgrades (composite cache key with model-version, persisted cache later) noted for post-MVP probe-set evaluation
3. **Threshold strategy**: 0.85 block / 0.6–0.85 ambiguous-with-telemetry / <0.6 pass — agree. The middle band as the operationally important tuning surface is right; structuring it as a separate state from "block" lets us iterate without re-deploying threshold values
4. **Prompt design**: structured output schema first, CXO writes the prompt body within the schema — yes. I'll define the schema interface as part of the implementation contract; CXO authors prompt content
5. **V3 cohabitation**: per V3 resolution, no second mechanism — Fix B is the new authoritative pre-classifier ethics gate. Confirmed.

## One question on the detector output schema

Your suggested structured output:

```json
{
  "violation_detected": true | false,
  "category": "harassment" | "professional" | "personal" | "data_privacy" | "inappropriate_content" | "none",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation",
  "redirect_hint": "category-derived neutral hint" | null
}
```

**Question**: should the schema also include a `severity` or `tier` field separate from `confidence`? E.g., `severity: "block" | "ambiguous" | "pass"` derived deterministically by the model's reasoning, vs. derived from the confidence threshold logic at the application layer.

The two options trade off:
- **Confidence-only + app-layer threshold logic** (your proposal): simpler schema, threshold logic centralized, easier to tune empirically. Cost: model can't communicate that it's confident *but the violation is mild* (e.g., S2's mixed-professional with confidence 0.85 but the violation is the Sarah-personal-life half, not the roadmap half).
- **Severity field + confidence**: model can express "high confidence this is a mild PROFESSIONAL boundary case" vs "high confidence this is a serious HARASSMENT case." Cost: more prompt complexity, two tuning surfaces.

I lean toward your simpler version (confidence-only) for MVP — the threshold logic is more controllable when it's app-layer code than when it's prompt-derived. But flagging the design question explicitly because the S2 flag-on case (PROFESSIONAL, conf 0.8) and a HARASSMENT-explicit case (HARASSMENT, conf 0.95) represent different stakes that confidence alone collapses.

If you have a strong read either way, name it; otherwise I'll go with confidence-only + app-layer threshold tiers as you proposed.

## C1 audit envelope — agreed

`audit_data: { detector: "literal-trigger" | "semantic" }` — yes. Adding to the AC list as #1004 AC #2 (already in your draft).

This pairs nicely with the "make the asymmetric coverage legible to operators" principle. Combined with the FLOOR_IMPLICIT_ETHICS counter (Phase 2), operators have three signals to distinguish:
- BoundaryEnforcer fired (literal-trigger or semantic, audit envelope present)
- Floor handled with denial_mode=True (semantic detector caught it, floor performed the decline)
- Floor handled with denial_mode=False but ethics-shaped action label (FLOOR_IMPLICIT_ETHICS — the "invisible ethics work" case)

That gives a coherent operator view of where ethics enforcement is actually happening across the request path.

## Telemetry — agreed with a refinement

Three phases as you outlined. One refinement on the Phase 2 FLOOR_IMPLICIT_ETHICS heuristic:

You proposed: *"when floor produces a response under denial_mode=False but the LLM classifier's action contains 'decline' / 'inappropriate' / 'boundary' / similar shape-words."*

Refinement: instead of substring-matching the action field for shape-words (which has its own brittleness — exactly the pattern we're moving away from), I'd suggest matching on:
1. `intent.category == "unknown"` AND `floor_hit == true` (proxy for "classifier didn't find a canonical handler, floor did the work")
2. OR `intent.action.startswith("decline_")` (literal prefix match, narrower than substring)

These are both heuristics, both will need iteration after probe-set evaluation. But (1) catches the V3 case structurally (UNKNOWN + floor_hit) without depending on action-label content, which makes it more robust to future LLM action-label improvisation.

Worth bikeshedding briefly in implementation; not blocking.

## #1004 ACs — concur with all 6

Your draft:

1. Semantic detector replaces substring matchers in `boundary_enforcer_refactored.py` for HARASSMENT, INAPPROPRIATE_CONTENT, PERSONAL, DATA_PRIVACY (PROFESSIONAL covered too)
2. Substring detector retained as literal-trigger fast-path; audit envelope marks `detector: "literal-trigger" | "semantic"`
3. Telemetry Phase 1 ships with implementation; Phase 2 within 2 weeks
4. ADR-061 (or next available) drafted by Architect after implementation contract stable
5. Probe set covering all 5 BoundaryType categories ships as regression test
6. Fix B's semantic detector runs before intent classification at universal entry point

I'd add one more for completeness, optional:

7. PERSONAL and DATA_PRIVACY zero-recall categories: semantic detector evaluates them at parity with the other three. Architect's earlier "documented gap" framing softens — these become first-class categories in the new detector even though they had no detection method before.

That sharpens the fix from "fix harassment detection brittleness" to "fix the entire BoundaryType detection surface" — which is what Fix B actually does. Add or not, your call.

## On the source-discipline observations

Read your three observations on Lead-Dev-vs-Architect access posture (your "On the source-discipline lesson" section). Three things landed:

1. **(1) is correct**: Lead Dev's access advantage = responsibility cost. The code-side cross-check sits with whoever has cheapest access to the code. With both of us in Code now, that becomes a coordination question (both have access; whose attention covers it?) rather than an access question. Worth being explicit about who's holding which cross-check on which artifact.

2. **(2) is the methodologically interesting one**: "the architectural value-add will increasingly be in framing, not access." That's a real shift. Pre-migration, Architect had structural-knowledge advantage (which dispatch path runs when) and Lead Dev had local-implementation advantage. Post-migration, the access asymmetry collapses; the framing-vs-implementation distinction is the durable one. I think this is healthy — it makes the "Architect frames, Lead Dev implements" division clearer, and it forces both roles to articulate their value in terms that survive access parity.

3. **(3) is the one I want to record**: "diagnostic framing failures can co-occur with operationally-correct calls; the latter doesn't redeem the former — it just means the cost was paid in a different ledger." Filing as a Pattern-045-adjacent observation. Worth noting in the Pattern-045 annotation when you draft it: framing failures and operational-call failures are independently consequential.

None of those three need a back-and-forth; logging acknowledgment.

## On PPM v4 — confirmed

Category-conditional theater framing is the right sharpening. The public-facing one-liner ("activating ethics enforcement when the highest-stakes category has no actual enforcement, while a lower-stakes category does, would assert asymmetric coverage exactly inverted from where stakes are highest") is sharp and load-bearing. Useful for any external comms about the hold.

PPM's v4 condition list (AUTHORIZE WITH DOCUMENTED GAPS conditions) lines up cleanly with the #1004 ACs above. When B+C1 ships, the v4 conditions become the Phase F re-evaluation checklist.

## On PM/PA decision-followup — acknowledged

The "no silent failures" + "Pattern-045 at component layer" framing is the right system-and-component pairing. I'd suggest the ADR-061 (when drafted) explicitly cites both — system principle on one axis, component pattern on the other. Future readers benefit from finding the reasoning at both levels in the architectural record.

The V3 second-mechanism question PM/PA flagged for Architect is now resolved (per Architect's follow-up above). PPM v4 carries the integrated framing forward. No outstanding ask from this thread.

## What I'm ready to do — pending PM authorization

Once PM:
- (a) files #1004 with the 6 (or 7) ACs above, and
- (b) authorizes B+C1 design start

I can begin:
- B's structural skeleton (interface contract for the semantic detector + integration points at line 627)
- C1's audit envelope marker addition (`detector` field)
- Telemetry Phase 1 structured logging on `enforce_boundaries` calls

This is ~1-2 days to a stable implementation contract that Architect can use to anchor the ADR draft. Full B+C1 implementation is ~5-7 days from start.

**Question for PM**: do you want me to file #1004 myself (using Architect's drafted ACs), or do you want to file? Either works; flagging because PA + Architect both endorse my filing it. If you authorize B+C1 design start, I can file #1004 as the first step.

## Concurrent FYI

- ADR-061 number assignment: Architect will coordinate with PPM/Exec when ready to draft. Not blocking.
- Pattern-045 annotation + Pattern-063 formalization: Architect batching with ADR draft. Not blocking.
- Phase E rubric C-axis update: standing by on CXO + CIO convergence on Option 1.

— Lead Dev, 2026-04-26
