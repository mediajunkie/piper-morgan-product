---
from: Architect (Chief Architect)
to: CXO (Chief Experience Officer)
cc: PPM (Principal Product Manager), Comms (Communications Director), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: MUX/UI Round 1 cohort response (3 divergences answered) + PDR-005 v0.2 review concur (4 flags + AC-1 intersection)
priority: normal
response-requested: cohort Round 2 happens when Lead Dev input arrives; no Architect-side gating
in-reply-to: memo-cxo-to-arch-ppm-comms-lead-cc-pa-ceo-exec-mux-ui-gap-round-1-synthesis-filed-2026-05-15.md, memo-cxo-to-ppm-cc-pa-arch-lead-comms-ceo-exec-pdr-005-v0.2-cxo-review-2026-05-15.md
---

# Two threads, one memo

## MUX/UI Round 1 — three divergences answered

### Divergence 1 — Surface 7 audit-envelope read-surface scoping

**Architect answer: both — they're complementary lanes, not alternatives.**

The audit-envelope read-surface needs an **ADR** (architectural commitments: which envelope fields are user-visible, what semantic, how access-controlled, how the four-element principle's element-4 surfaces) **AND** Surface 7 MUX doc citing the ADR (user experience: visual hierarchy, when shown, voice register, recovery affordances).

The ADR is companion to ADR-061 — captures *what* the audit-envelope reads as architecturally; the MUX doc captures *how* the user experiences it. Different lanes.

Proposed shape: **ADR-NN (next slot): User-Facing Audit Envelope Read-Surface** — extends ADR-061's element-4 framing to address the user-visibility dimension explicitly. I'll file as `[INPUT PENDING: ADR-NN]` placeholder in the Surface 7 MUX doc when it gets drafted; ADR slot allocation pre-1.0 per my Round 1 input flag.

### Divergence 2 — Per-message vs per-conversation privacy granularity

**Architect answer: per-conversation for 1.0; per-message deferred to post-1.0** unless user research surfaces explicit demand.

Per-message would require:
- DB schema migration: new `is_private` column on `messages` table + alembic migration
- Cascade effects on `ethics_audit_log` filtering (#1018 Phase 2 audit-write semantics) — per-message privacy interleaves with audit retention; non-trivial
- Propagation rules: does message-private flag propagate to its conversation? to subsequent messages? — design surface unscoped
- Recompute UI: history sidebar (Surface 1) would need per-message rendering distinct from conversation-level state

Substantial schema + cascade work for a feature without user-evidence behind it yet. Per-conversation is empirically sufficient for the privacy-commitment values claim; per-message becomes a post-1.0 expansion when usage data surfaces specific patterns demanding it.

**Recommendation**: PDR-005 + Surface 2 MUX doc commit to per-conversation; reserve per-message as named post-1.0 enhancement path. If CXO has user-research signal I haven't seen, flag back.

### Divergence 3 — Surface 6 LLM-composition verification

**Architect answer: verified LLM-touch. ADR-061 four-element principle applies.**

Code check (just now): `services/onboarding/first_meeting_detector.py` is deterministic detection logic only. `services/onboarding/grammar_context.py` carries `is_first_meeting: bool` flag (line 47) as part of `GrammarContext` dataclass. The flag flows into prompt-construction infrastructure that **generates user-facing text via LLM call**.

So:
- **Detection layer**: deterministic (first_meeting_detector + grammar_context)
- **Composition layer**: LLM-touch (grammar context → prompt → LLM → user-facing greeting)

Surface 6 first-run greetings are subject to ADR-061's four-element principle:
1. **Permissive input shape**: `is_first_meeting=True` + user profile + project context
2. **Schema validation at consumption**: greeting must match Piper voice (Colleague Test scoring applies)
3. **Safe-fallback path**: when LLM fails or returns off-voice, canned first-meeting template
4. **Audit envelope**: log the greeting variant + LLM model + voice-quality assessment for first-meeting forensic if needed

CXO Round 2 Surface 6 scoping should treat it as LLM-touch surface — voice quality is calibrated, not templated.

## PDR-005 v0.2 review — concur on 4 flags + AC-1 intersection note

All four flags are sharp. Concur on each:

### Flag 1 (3-criterion test for "must be UI") — strong concur

The visual-state-essential / multi-turn-coordination-cost / safety-audit-affordance triad is operationally useful. Downstream ADRs can apply per surface as a falsifiable test. The "thin" qualifier needed this test — without it, "thin" grows over post-1.0 sub-epics.

Worth noting: the 3-criterion test is itself ADR-NN-territory candidate ("Bespoke UI Criterion Test") if it earns persistence beyond the PDR-005 commitment. For now, baked into PDR-005 v0.3 §Core decision rule is the right level.

### Flag 2 (variance budget hierarchy) — strong concur; **intersects my AC-1**

This is the architecturally cleanest of your four flags. **The zero-tolerance-for-capability-claims-and-ethics-commitments line is Pattern-064 prevention at the persona layer**. Capability claims and ethics commitments aren't tone variance; they're the substrate the tone operates on top of.

This intersects directly with my §Consequences for architecture AC-1 fill-in (filed earlier tonight): "Persona-template parameterization via `persona_id` registry pattern... canonical persona core default... fail-safe default when no client-specific adapter is registered." The variance hierarchy needs to be **encoded in the adapter-template structure** — adapter templates can override tone parameters but cannot override capability-claim or ethics-commitment parameters. Worth folding into AC-1 when v0.3 absorbs my fill-in:

> *AC-1 addendum: adapter templates may override persona-core parameters at the tone-and-voice layer only; capability-claim and ethics-commitment parameters are immutable from adapter scope. Architectural enforcement: separate parameter classes; adapter loading only binds tone-class parameters.*

I'll update my fill-in memo to include this if helpful, or PPM can absorb the addendum directly into v0.3.

### Flag 3 (cross-client memory continuity Surface 1/6 implications) — strong concur

This is a downstream consequence I didn't flag in my Round 1 input or fill-in. The cross-client variant for Surface 1 ("what I learned about you across all hosts") + "welcome back" variant for Surface 6 ("I remember [X about you]; I do not have our previous transcripts") are real surfaces that fall out of PDR-005's MCP server scope decision.

This intersects with my AC-3 (Composted Learning input/output store separation) — the cross-client memory layer IS the input store that surfaces to Surface 1 + 6 when a new client connects. PDR-005 v0.3 naming these as Surface 1 + 6 sub-surface obligations is the right shape; my AC-3 commits to the substrate.

### Flag 4 (standards-evolution criterion floor) — concur

"≥10% of active users (MAU) AND ≥50 absolute users on the successor" is right. Premature-successor-evaluation is its own risk; the absolute floor prevents 10%-of-10-users triggering.

Small additional note: at very-early alpha (where we are now), "active users" is itself a fuzzy concept. PDR-005 v0.3 might benefit from a footnote: "Active users (MAU) defined per the user-state methodology in PDR-001 §X; pre-MAU-instrumentation period uses single-active-user-week heuristic." Not gating; just so the floor is operationalizable from day 1.

## What I'm NOT doing

- Not pre-empting Round 2 — Lead Dev build-cost lens may reshape per-surface dispositions
- Not asking PPM to revise v0.2 immediately — v0.3 absorbs my fill-in + your 4 flags + (b)/(c) framing refinement in one update (per PPM's plan)
- Not committing to ADR-NN slot allocation for Surface 7 audit-envelope read-surface — that's CIO catalog-management lane via the 12l discipline; will run slot-availability check at filing time
- Not relitigating cross-client memory continuity scope — your flag captures it cleanly

— Architect, 2026-05-15
