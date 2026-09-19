---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: Chief Architect, CEO (xian)
date: 2026-05-15
subject: methodology-core docbase drift fixed — 3 docs referenced deleted engine post-#1094; staleness banners added
priority: normal
response-requested: FYI; no action needed unless you want a deeper rewrite later
in-reply-to: (none — surfacing from a forest-view drift check requested by PM)
---

# methodology-core drift surfaced + fixed

PM asked for a quick "forest view" drift check this evening (post-#1094 close-out), worried that recent issues had revealed outdated premises (the Apr 27 framing of #1015 RequestContext was materially obsolete against current code). An Explore-subagent sweep across domain models / UX-MUX / architecture / tests / docs landed clean in 4 of 5 areas. **One area: methodology-core docbase has 3 files referencing `services/orchestration/engine.py`, which was deleted today in #1094 (ENGINE-DELETION, γ-preserve).**

Surgically fixed; surfacing for your awareness because methodology-core is your docbase.

## The three files

| File | What references the engine | Fix applied |
|------|---|---|
| `docs/internal/development/methodology-core/MULTI_AGENT_INTEGRATION_GUIDE.md` | ~15 references throughout (engine integration is the guide's core target) | Deprecation banner at top + status line marker; body preserved for historical/illustrative reference |
| `docs/internal/development/methodology-core/HOW_TO_USE_MULTI_AGENT.md` | ~6 references (engine import + `engine.create_workflow_from_intent` + `engine.execute_workflow` examples) | Same shape: deprecation banner + status line marker |
| `docs/internal/development/methodology-core/claude-code-workflow.md` | 1 reference at line 412 in a worked-example narrative ("Integration with OrchestrationEngine complete") | Inline historical-note comment added (`# [historical: engine deleted #1094, 2026-05-15]`) |

Commit: `19b33a89`.

## What the banners say

For the two integration/usage guides, the banner explains:
- Engine + WorkflowFactory deleted in #1094 (γ-preserve)
- EXECUTION-intent dispatch now flows through `intent_service.process_intent` direct dispatch via the `task_type` registry (Pattern-072, promoted to Proven via #1094)
- `MultiAgentCoordinator` (`services/orchestration/multi_agent_coordinator.py`) + `chain_of_draft.py` survive and remain the concrete multi-agent surfaces
- Code samples below are no longer copy-pasteable; the high-level concept (decompose-coordinate-execute) remains illustrative
- Extend `intent_service` handler dispatch instead of `OrchestrationEngine` task handlers

For `claude-code-workflow.md`, the inline note flags the single comment without rewriting the worked-example narrative around it.

## Why banner-not-rewrite

Two considerations:
1. **Minimal-fix discipline**: PM asked for "fix" not "rewrite." Banners surface the staleness without requiring a from-scratch rewrite of multi-agent integration patterns under the new architecture (which would be a separate substantive effort).
2. **Concept survives even if dispatch layer changed**: the multi-agent CONCEPT (decompose tasks → assign to specialized agents → coordinate) is unchanged. The engine was the DISPATCH layer; deleting it doesn't invalidate the methodology of multi-agent coordination, just the specific integration sample code. Banner + concept-preservation is the proportional response.

## If you want a deeper rewrite

Two scoping options to consider — neither is urgent:

- **Option α — Re-write the guides under the new architecture**: produce updated code samples showing `MultiAgentCoordinator` integration via `intent_service` handler dispatch. ~1-2 hours of focused doc work. Worth doing if multi-agent coordination is about to be exercised again; less worth doing if it's dormant.
- **Option β — Move to `methodology-core/archived/`**: if multi-agent coordination work is genuinely not on the near-term roadmap, archive the guides + leave a one-line pointer. Smaller surgery; signals "this isn't current methodology anymore."

I'll happily do either if you flag it as worth doing; defaulting to "banners are sufficient" until then.

## Pattern note (for your catalog)

This drift instance is **Pattern-064-adjacent in a specific shape**: scaffolding documentation (i.e., methodology-core docs) describing code that no longer exists. The compliance/scaffolding-shape that Pattern-064 names ("alive scaffolding that does the opposite") has a documentation-flavor variant: *"living documentation describing dead code,"* where the doc presents a working integration that engineers can't actually instantiate. The Apr 27 risk framing for #1015 (route-handler bodies vs. current code) is a similar shape at the issue-tracking layer. Worth a brief methodology note if you see other doc-vs-code drift surface — the trigger is "doc commits to specific code references; code moves underneath it."

I'm not filing this as a Pattern candidate yet — single instance, and we already have Pattern-064 covering the broader shape. Just flagging the resonance.

## Awareness ask only

No action required from you. Surfacing because methodology-core is your domain; PM may also want awareness (CC'd). Architect cc'd because they were the #1094 ratifier and the engine-deletion ripple is theirs to absorb at the architecture layer.

## References

- Drift audit summary: this session's Explore subagent report (not committed; embedded in PM conversation context)
- Doc fix commit: `19b33a89` (3 files, +7 / -3 lines)
- #1094 close-out: `d48bc1d0` (merge, 2026-05-15 14:38 PST)
- Pattern-072 promotion-to-Proven memo (filed earlier today): `31f7abbd`

— Lead Developer
