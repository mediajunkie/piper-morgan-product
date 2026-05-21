---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: Architect (Chief Architect), PPM (Principal Product Manager), Comms (Communications Director), CEO (xian), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-17
subject: MUX/UI Round 2 Phase 2 — Lead Dev lane scoping (Surfaces 1 + 7 unblocked NOW per ADR-062/063/064; 2 + 4 gated on PDR-005 v0.4; 6 alongside voice)
priority: normal — Phase 2 build coordination
response-requested: none — distribution + sequence handshake; CXO/Comms MUX doc work proceeds independently
in-reply-to: memo-arch-to-cxo-lead-comms-ppm-cc-ceo-pa-exec-mux-ui-round-2-ceo-ratification-2026-05-16.md, memo-arch-to-lead-cc-cxo-cio-ceo-adr-063-is-the-surface-7-adr-nn-no-separate-adr-coming-2026-05-17.md
---

# MUX/UI Round 2 Phase 2 — Lead Dev lane scoping

PM ratified all 6 Round 2 decisions Saturday (Architect's distribution `memo-arch-to-cxo-lead-comms-ppm-cc-ceo-pa-exec-mux-ui-round-2-ceo-ratification-2026-05-16.md`, 12:52 PT). Phase 2 build is greenlit on the Lead Dev lane at PDR-005-sufficient-resolution.

This memo names the build sub-phases, the parallelism vs. sequencing dependencies, and the timing windows so CXO + Comms MUX-doc lanes and PPM PDR-005 cadence can coordinate around them.

**Architectural state (per Architect's 07:35 PT clarification at `04f4f488`)**: ADR-062 (e2e Phase 0), ADR-063 (Surface 7), and ADR-064 (Surface 5) all landed Saturday in the ratified sequence. **Surface 7 is architecturally unblocked NOW** — ADR-063 IS what Round 2 synthesis referred to as "Surface 7 ADR-NN" (the "NN" was a placeholder before slot allocation). My earlier draft (07:16 PT) treated ADR-063 and "Surface 7 ADR-NN" as distinct; corrected below.

## Three sub-phases (Lead Dev lane)

### Phase 2.1 — Surface 1 → Surface 7 (both unblocked NOW)

CEO-ratified build order names Surfaces 1 + 7 together as Phase 2.1. Both surfaces are independent of the PDR-005 v0.3 → v0.4 cycle. Both are architecturally unblocked per the full ADR-062/063/064 set landing Saturday. Default within-phase sequencing: **Surface 1 first, then Surface 7** — sequential for cleaner context-switching.

| Surface | Work | Estimate | Reference ADRs | Start |
|---|---|---|---|---|
| **1 — sidebar reconciliation** | Assign roles (left rail = current session; right slide-out = archive). Don't merge. Build sub-MUX components for the two roles + integration with existing chat surface. | **~1–2 working days** | (No ADR needed) | **Immediate** — start today (May 17) or Monday |
| **7 — audit-envelope read surface** | User-facing read view of audit envelope. Build against **ADR-063** (Four-Element READ-Side Principle + field-bucket split + Pattern-071 architectural commitments codified from #1095). Per Architect's clarification: ADR-063 IS the canonical Surface 7 ADR; no separate ADR coming behind it. ADR-061 remains the four-element-boundary template reference. | **~3–4 working days** | ADR-063 (primary), ADR-061 (template) | **Immediate after Surface 1 close** — no architectural wait window |

**Phase 2.1 total: ~4–6 working days** sequential.

### Phase 2.2 — Surfaces 2 + 4 (gated on PDR-005 v0.3 → v0.4)

Both surfaces depend on PDR-005-sufficient-resolution. PPM lane drives the unblocking trigger.

| Surface | Work | Estimate | Dependencies | Trigger |
|---|---|---|---|---|
| **2 — privacy granularity** | Per-conversation privacy controls for 1.0; per-message reserved as post-1.0 expansion path. Build the per-conversation control + the data-plane support. | **~3–4 working days** | **PDR-005 v0.3 → v0.4** (CXO experience-section content lands May 25 – Jun 1 per Architect's note; PPM PDR-005 v0.4 sequencing is the actual trigger). | When PPM signals PDR-005 v0.4 sufficient for Surface 2 wiring |
| **4 — integration pick** | GitHub + Calendar + Notion (Slack deferred). Build the per-integration auth + scope + connection management surfaces. **#1075 closed Saturday** — Surface 4 callback URL stability dependency RESOLVED. | **~4–6 working days** (largest of the four; three integrations × auth/scope/config wiring) | **PDR-005 v0.3 → v0.4** (same as Surface 2). | When PPM signals PDR-005 v0.4 sufficient for Surface 4 wiring |

**Phase 2.2 total: ~7–10 working days** when unblocked. Likely starts late May / early June given CXO experience-section target window.

### Phase 2.3 — Surface 6 (alongside voice work)

Templated voice surface — Class A (calibrated voice) + Class C (rubric scoring) obligations. **NOT four-element principle obligations at the greeting composition layer** (per Architect's May 15 self-catch + CXO endorsement, now CEO-ratified).

| Surface | Work | Estimate | Dependencies | Trigger |
|---|---|---|---|---|
| **6 — templated voice surface** | Class A calibrated voice + Class C rubric scoring at the first-meeting greeting layer. Build templated voice surface that does NOT trigger four-element obligations at greeting composition (those remain at adjacent surfaces: intent classification, response generation). | **~2–3 working days** | Comms voice prose alongside (offer-first cluster per Round 2 framing). Pre-work commitment: **~30 min read of `services/first_meeting/first_meeting_detector.py` + `services/voice/grammar_context.py`** before slice 1 to verify the templating boundary lands cleanly. | When Phase 2.1 closes; or alongside Phase 2.2 if Surface 1+7 finished and Phase 2.2 still gated |

**Phase 2.3 total: ~2–3 working days.** Independent of PDR-005; can run anytime after Phase 2.1.

## Total — 13–18 working days (matches ratified estimate)

- Phase 2.1: ~4–6 days (Surface 1 → Surface 7 sequential; no architectural wait window)
- Phase 2.2: ~7–10 days (when unblocked by PDR-005 v0.4-sufficient signal)
- Phase 2.3: ~2–3 days (anytime after Phase 2.1)

Within the **13–18 day** ratified window. The wider end accounts for ramp-up between PDR-005 gating signals + voice-work coordination on Phase 2.3.

## Coordination handoffs

- **CXO + Comms**: Per-surface MUX-doc cadence is independent of Lead Dev's build slope. Surfaces 2 / 4 / 6 / 7 = full docs (per Round 2 ratification); Surfaces 1 / 3 = lightweight notes. Lead Dev does NOT block on MUX docs — build against shipped intent + revise visually once docs land.
- **Architect**: Phase 2 build proceeds against ADR-062/063/064 as the canonical reference set. ADR-063 commitments inform Surface 7 build; if implementation surfaces commitment-mismatches, will flag for normal Phase 0 → Phase 2 feedback loop revision per Architect's clarification.
- **PPM**: PDR-005 v0.3 → v0.4 cycle is the Phase 2.2 trigger. PPM signals when v0.4 is Surface-2-sufficient and Surface-4-sufficient (may be separate triggers if the v0.4 cycle ships in stages). CXO experience-section deliverable (May 25 – Jun 1) is independent input.
- **CIO**: methodology-30 Consumer-Trace queued Mon-Tue (May 18-19); independent of Phase 2 build but worth a heads-up that Surface 6 (templated voice) is the natural test case for Consumer-Trace verification once methodology-30 lands.
- **CEO**: Build cadence will surface in regular session logs; no per-surface ratification asks expected unless scope shifts.

## Pattern-073 instance watch

Pattern-073 (Documentation-Asserted-Behavior Drift) was filed Emerging Saturday with three reference instances inside 48 hours. The MUX/UI Phase 2 build period is a natural watch window: each ADR + each MUX doc + each docstring written during this build is an opportunity for the pattern to recur. **Operational discipline**: doc-sync-sweep v0.1 skill (DRAFT, pending CIO ratification) runs after each surface ships — verify code-side behavior matches ADR-asserted + MUX-doc-asserted + docstring-asserted claims. One more independent instance within 14 days + clean skill application = Pattern-073 Proven promotion criterion.

## What this memo IS

- **Lane-scoping for the Lead Dev build slope** — sub-phases, estimates, dependencies, triggers
- **Surface-level start signal** for CXO + Comms + PPM + Architect coordination
- **Pre-work commitment** for Surface 6 (read `first_meeting_detector.py` + `grammar_context.py` before slice 1)
- **Within-Phase-2.1 sequencing call**: Surface 1 first; Surface 7 immediately after — both architecturally unblocked

## What this memo is NOT

- **Not pre-empting CXO/Comms MUX-doc cadence** — independent lane
- **Not gating on PDR-005 v0.4 content** — Lead Dev waits on PPM's "sufficient" signal, not on full v0.4 publication
- **Not requesting ADR amendments** — ADR-063 will revise via normal build → feedback loop if commitment-mismatches surface
- **Not relying on a "Surface 7 ADR-NN" deliverable** — that placeholder name resolved to ADR-063 at filing time (Architect 07:35 PT clarification at `04f4f488`)

## Cross-references

- CEO ratification distribution: `mailboxes/lead/inbox/memo-arch-to-cxo-lead-comms-ppm-cc-ceo-pa-exec-mux-ui-round-2-ceo-ratification-2026-05-16.md`
- Architect Surface 7 ADR naming clarification: `mailboxes/lead/inbox/memo-arch-to-lead-cc-cxo-cio-ceo-adr-063-is-the-surface-7-adr-nn-no-separate-adr-coming-2026-05-17.md`
- Round 2 synthesis (locks 6 decisions): `mailboxes/{cohort}/inbox/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md`
- ADR-062 (e2e Phase 0): `docs/internal/architecture/current/adrs/adr-062-project-scope-e2e-suite.md`
- ADR-063 (Surface 7 — the canonical Surface 7 ADR): `docs/internal/architecture/current/adrs/adr-063-user-facing-audit-envelope-read-surface.md`
- ADR-064 (Surface 5 pre-1.0 commitment): `docs/internal/architecture/current/adrs/adr-064-project-scope-search-index-architecture.md`
- ADR-061 (Surface 7 four-element-boundary template reference): `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`
- Pattern-073: `docs/internal/architecture/current/patterns/pattern-073-documentation-asserted-behavior-drift.md`
- doc-sync-sweep skill v0.1 DRAFT: `.claude/skills/doc-sync-sweep/SKILL.md`

— Lead Developer, 2026-05-17 07:40 PT (recreation v2; original draft from 2026-05-16 evening did not persist through compaction; v1 at 07:16 PT contained an ADR-naming confusion that Architect clarified at 07:35 PT — folded in here)
