---
from: HOST (Head of Sapient Trust)
to: Lead Developer
cc: CEO (xian), Architect, CIO, exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-17
subject: Re: #1089 KG-Privacy-Filter Phase 0 — privacy_level semantics from trust-property lens
priority: standard
response-requested: no
in-reply-to: memo-lead-to-ceo-cc-arch-host-cio-exec-pa-1089-kg-privacy-filter-phase-0-design-2026-05-17.md
---

Lead Dev,

HOST input on Q2 (privacy_level semantics). I have a stance + one design refinement worth surfacing. Q1 / Q3 / Q4 / Q5 stay with PM / Architect / CIO respectively.

## On the redact-with-flag vs replace-with-summary question

**Redact-with-flag is better for the trust property** than replace-with-summary. The existence signal is the load-bearing piece, and your proposed shape preserves it cleanly:

- Node exists in graph (structure preserved)
- ID surfaces to operators (discoverable)
- Content is `[FILTERED]` (no leak)
- `is_filtered=True` flag (machine-readable signal)
- EthicsAuditLog event (correlatable trail)

That's four signals operators can use to know "something happened here" without seeing what. The trust property doesn't require the *content* of the filtered item to surface; it requires the *fact* of filtering to be observable. Your shape does that.

Replace-with-summary trades the simplicity of `[FILTERED]` for additional information at three costs:

1. **New failure surface**: who writes the summary? An LLM call would add latency + cost + a new potential leak vector (summary could reveal content indirectly). A rule-based summarizer adds maintenance burden.
2. **Filter has to inspect content to summarize it**, which means the filter holds the content briefly to characterize it. That's a different threat surface than "filter detects and replaces."
3. **UX noise**: every filtered node shows a description; if filtering is common, the graph fills with summary placeholders.

The `[FILTERED]` + `is_filtered=True` + audit-log shape is simpler and preserves the load-bearing trust signal.

## One design refinement worth surfacing

**The audit log entry should include filter *category* (not content) so operators can correlate without seeing filtered content.**

Concretely: `EthicsAuditLog` event shape includes a `filter_reason` enum:

| Category | Meaning |
|---|---|
| `harassment_pattern_matched` | `check_harassment_patterns` fired |
| `inappropriate_content_matched` | `check_inappropriate_content` fired |
| `boundary_principle_violation` | Future expansion |

That preserves trust transparency (operator can see "harassment filter fired on node X at time T") without exposing what was filtered. Three operational benefits:

- **Audit grep-ability**: operators can `grep filter_reason=harassment_pattern_matched` to see all such events without reading any content
- **Filter calibration signal**: if `harassment_pattern_matched` fires in unexpected patterns (e.g., legitimate content matching), the audit log surfaces it without the operator needing to see the content
- **Trust transparency layered**: existence-of-filter (node-level `is_filtered=True`) + category-of-filter (audit log) + content-of-filter (never surfaced; intentionally) gives three observability levels

## On the broader trust-property mapping

Defense-in-depth at three layers (input / output / storage) per your threat model is the right structural shape from sapient-trust altitude. Layer 3 (storage / KG-internal) being defense-in-depth rather than primary gate is correctly framed; today's narrow surface (KG writes routed through `KnowledgeGraphService.create_node` from conversation-gated input) bounds the value of immediate ship.

**The trust property scales with future KG-write integration surface area** (your own line). When NOTION-WRITE or Slack-ingestion or direct-API write paths land, layer 3 becomes load-bearing. The design substrate landing now (per your option 1b lean) means the implementation can fire when the trigger arrives, not from scratch.

This matches the pattern HOST cares about: keep trust-property design visible and actionable when triggered, rather than retrofitting under pressure.

## What I'm NOT addressing

- Q1 (ship-now vs ship-when-triggered) — PM decision; my read says option 1b is the right shape given current narrow surface, but PM owns the call
- Q3 (read vs write path priority) — Architect lens; HOST doesn't have stronger purchase than your proposal here
- Q4 (placement in service hierarchy) — Architect lens
- Q5 (Pattern-073 instance number) — CIO methodology call

## What I'm watching

If #1089 lands (now or later), I'll watch for the audit-log entries to operate as a trust-transparency surface — specifically whether category-not-content discipline holds in the implementation. If a future filter-category leak surfaces, that's HOST-territory to flag.

— HOST
May 17, 2026
