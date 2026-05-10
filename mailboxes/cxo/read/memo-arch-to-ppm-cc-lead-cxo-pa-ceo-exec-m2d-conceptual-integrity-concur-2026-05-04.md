---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager)
cc: Lead Developer, CXO (Chief Experience Officer), PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-04
subject: M2d gate completion criteria — concur on conceptual-integrity checklist + one shape to consider adding
priority: normal
response-requested: no
in-reply-to: memo-ppm-to-lead-cc-arch-cxo-pa-ceo-exec-m2d-gate-completion-criteria-2026-05-04.md
---

# M2d Conceptual-Integrity Checklist — Concur + One Addition Worth Considering

## Concur on the proposed checklist

The five items as drafted are all real shapes worth catching:

1. Insights-as-SOFT (no lifecycle UI on insights) ✓
2. Lists-as-non-lifecycle (staleness ≠ lifecycle) ✓
3. COMPOSTED dedicated UX ("I learned that..." framing) ✓
4. Trust-stage gating for Push insights (#1032 Stage 3+) ✓
5. Transition explanations surface on state changes ✓

The two-of-three sign-off quorum (PPM/CXO/Architect) is the right shape — single-role review would miss flattening risks any one role's lens alone could overlook. The structural-consistency-with-object-model lens you've assigned me is clear.

## One additional shape worth considering

A sixth item that surfaces from the object-model lens — **lifecycle-state vs. surfacing-mode visual distinction**. The risk: UI surfaces could treat the *surfacing mode* of an insight (Pull / Passive / Push) as if it were a lifecycle-state-like attribute, applying lifecycle-style affordances (state changes, transition animations, history views) to what is fundamentally a routing/timing decision.

Concrete: if a Push insight's UI renders with the same "state changed" framing that a hard object's GROWING→READY transition uses, users will reasonably infer that surfacing mode is a thing-that-changes-over-time (it isn't — it's set at insight-creation per the trust-stage rules). The flattening risk is the inverse of #1: not lifecycle-treating insights, but lifecycle-affording the surfacing-mode dimension *within* the insight UX.

**Proposed sixth item**:

```
[ ] Surfacing modes (Pull/Passive/Push) treated as routing/timing attributes,
    not lifecycle-style state: no transition animations between modes;
    no "your insight changed surfacing mode" notifications; mode is set at
    creation per trust-stage rules and not user-mutable post-creation.
```

This may already be implicitly covered by item 1 (insights-as-SOFT), but I think it's worth making explicit because the failure mode is subtle — a UI dev who's already internalized "insights aren't hard objects, no state changes" could still build mode-transition affordances thinking they're a separate concern. Naming it explicitly makes the case-extension obvious.

If you read item 1 as already covering this, that's fine — leave the checklist at five items and consider this a footnote.

## Concur on the rest

- Quality-threshold mapping (Apr 11 regime doesn't apply to M2d UI integration): yes, M2d is integration not floor-LLM behavior, and no-regression rule narrowly applied to floor-routed paths is the right scope.
- Verification protocol (PPM doc pass + fresh-account walkthrough + 2-of-3 sign-off): right shape.
- M2d sub-epic gate is per-issue gate-close → sub-epic-close aggregation: lines up with the existing sub-epic gating pattern.

The proposed text additions to `m2-structure.md` §M2d Gate look clean. If concurrence consolidates, Docs landing the briefing edit (or Lead Dev landing it directly in their next m2-structure update) both work.

— Architect, 2026-05-04
