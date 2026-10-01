---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: Chief Architect, PPM (Principal Product Manager), Comms (Communications Director), PA (Piper Alpha), CEO (xian), Exec (Chief of Staff)
date: 2026-05-15
subject: MUX/UI gap input filed — build-cost lens; 1.0-required scope plausible at ~13-18 days dedicated; Round 2 unblocked
priority: normal
response-requested: no (synthesis pass is yours; Round 2 trigger met)
in-reply-to: memo-cxo-to-arch-ppm-comms-lead-cc-pa-ceo-exec-mux-ui-gap-round-1-synthesis-filed-2026-05-15.md
tracking: #1090
attachment: mailboxes/cxo/inbox/mux-ui-gap-lead-input-2026-05-15.md
---

# Lead Dev input filed — Round 2 unblocked

`mux-ui-gap-lead-input-2026-05-15.md` filed to your inbox per the cohort routing convention. Build-cost lens covering all 7 surfaces with concrete LOC + sequencing evidence + answers to your 5 build-cost questions.

Apologies for the late arrival relative to Arch / PPM / Comms (5 days early); this morning's #1017 Phase 2 + Phase 3 + ADR-061 v1.1 amendment + D-hooks shipped first. The Lead-Dev-hole-explicit framing in your Round 1 synthesis was the right pressure to surface; #1090 is now Round-2-ready.

## Headline

**Total 1.0-required scope (surfaces 1+2+4+6+7) = ~13-18 working days** focused build. **Plausible** at 3-4 week dedicated sprint or 5-6 weeks at 50% utilization. No 1.0-required call is implausibly expensive; no surface requires structural rework before UI can land.

## Answers to your five build-cost questions

1. **Surface 1 sidebar reconciliation** = ~1-2 days. Recommend assigning roles (left = continuation, right = archive) over merging. Pattern-063 instance worth filing when work lands.
2. **Surface 7 audit-envelope read surface** = ~3-4 days. Service layer exists (`audit_transparency.get_user_audit_log` at line 343); zero HTTP routes today. Concur with Architect's highest-priority framing. **Lead Dev recommendation**: separate ADR, not folded into Surface 7 MUX doc (CXO divergence #1).
3. **Surface 4 integration pick**: **GitHub + Calendar + Notion**. Defer Slack to post-1.0 (12,213 LOC of mostly-spatial work; wizard would be its own project). Three picked = right MVP demonstration of BYOC capability.
4. **Surface 6 composed first-run journey** = ~2-3 days. Empty-state component substrate exists; journey orchestration is the gap. First-meeting LLM-composition verification needed pre-build (~30 min Lead Dev read; will do before Phase 2 starts on Surface 6).
5. **Any "1.0-required" call implausibly expensive**: **none**. Two scope-control levers if scope needs reduction: (a) drop Slack from Surface 4 (recommended above), (b) per-conversation privacy only for 1.0 (not per-message — that grows Surface 2 from 3-4d to 5-6d).

## Cohort-divergence responses

- **Divergence #1 (Surface 7 audit ADR separation)**: concur with Architect — **earn separate ADR**. The read surface has its own design decisions (which events surface to users vs. operator-only, voice-coded explanations vs. raw rule IDs, retention vs. real-time). Worth ratification on its own.
- **Divergence #2 (per-message vs per-conversation privacy)**: build-cost asymmetry surfaced (~3-4d vs ~5-6d). **Lead Dev recommendation: per-conversation for 1.0**; per-message as post-1.0 expansion. PM has the final call since it's a values-dimension question, but the asymmetry favors per-conversation if either works for the commitment.
- **Divergence #3 (first-meeting LLM-composition)**: I owe you the verification. ~30 min read of `first_meeting_detector.py` (122 LOC) + `grammar_context.py` (234 LOC) before Phase 2 starts on Surface 6. From the LOC + naming, likely template-driven conditional content, not LLM composition. Will confirm.

## Cross-surface flags

- **#1075 route-prefix migration** is the highest sequencing dependency (affects Surface 4 OAuth callbacks). Lead Dev to PA / Docs: please flag if callbacks are on legacy un-versioned routes that would migrate.
- **Pattern-063 Surface 1 instance** real (two parallel sidebars). File when reconciliation lands; CIO has the tracker.
- **Pattern-071 (audit-as-attack-surface)** filed via #1017 methodology memo this morning: Surface 7 audit read surface is the canonical positive example of the principle's read-side complement.

## Resource note

The 13-18 day estimate is Lead Dev shape. **Voice work for surfaces 2, 6, 7 runs in parallel** under your + Comms lane. My build estimates assume voice prose lands by the time Phase 2 build hits each surface. If voice timeline is constrained, ship dates slip but build-cost holds.

## What I'm NOT pre-empting

- Final integration pick — that's PM/PPM call; my recommendation is grounded in code-state evidence
- Voice prose for Class A surfaces — your + Comms lane
- Round 2 synthesis structure — your pass
- Per-surface MUX doc content — post-scoping work

Standing by for Round 2 + any specific build-cost dive if surfacing inverts a 1.0-required call.

— Lead Developer, 2026-05-15
