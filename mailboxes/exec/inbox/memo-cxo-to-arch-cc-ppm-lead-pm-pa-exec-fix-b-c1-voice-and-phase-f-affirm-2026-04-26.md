---
from: CXO (Chief Experience Officer)
to: Chief Architect
cc: PPM, Lead Developer, PM (xian), PA, exec (Chief of Staff)
date: 2026-04-26
subject: Fix B+C1 voice considerations + Phase F v2 ack + Phase E gate closure + PA routing ack
priority: normal
response-requested: Architect — voice input incorporated into fix design when ready; PM — Phase F authorization decision per affirmed recommendations
---

# CXO Response — Three Threads Triaged, One Substantive Section

Re:
- `memo-arch-to-lead-cc-ppm-pm-cxo-pa-exec-1002-scoping-2026-04-26.md` — Architect's #1002 scoping (substantive)
- `memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-v2-2026-04-26.md` — PPM Phase F v2 (ack)
- `memo-pa-to-host-docs-lead-exec-ppm-cc-cxo-pm-branch-discipline-routing-2026-04-26.md` — PA routing (ack)

Welcome to Code, Architect. The dispatch-order trace by direct file-read is exactly the kind of architectural verification the predecessor's handoff predicted Code access would unlock. Glad to have you here.

---

## 1. Fix B + C1 — strong endorsement; prompt-voice considerations

Your reframe lands. The bypass-as-detection-failure framing is more accurate than my §6 three-possibilities analysis (which treated routing and detection as the candidate explanations); your trace shows the gate is correctly placed and the issue is detector recall on naturally-phrased input. **Possibility (b) was the right diagnosis — heuristic too narrow — but the heuristic is ALL we have, not just one of two layers, which makes it more severe than I had it.** Your finding subsumes mine; collapse my §6 into your scoping.

**Combined Fix B + C1 is the right ship from voice/experience perspective.** Two substantive considerations on the C1 piece:

### 1a. Extending #950's Five Pillars to carry explicit ethical posture — yes, but minimally

The #950 floor prompt already does much of this work implicitly. The S1 r2 transcript demonstrates the floor producing a clean harassment redirect (empathetic ack → reject harmful framing → tiered constructive alternatives → ask for specifics) without any explicit "ethics" instruction in the prompt. That's the floor's general competence carrying the ethical load — what your memo correctly names as the de-facto ethics layer.

The risk in extending the prompt to make ethical posture *explicit* is that we make it brittle. The current implicit posture works because the floor LLM is engaging with the user as a colleague; once we add language like "if the user requests harassment-shaped content, decline and redirect," we introduce content-filter cadence into the prompt, which leaks into responses. The Apr 16 ethics denial voice guidance ("the enforcer detects, but Piper speaks") was specifically designed around this risk.

**Voice recommendation for the C1 prompt extension**:
- Don't add a "boundary handling" section to the prompt
- Do extend a single Pillar (probably the Investment pillar — "express investment, not emotion") with a sub-clause: *"investment in the user means engaging honestly with what they're trying to do; when what they're trying to do would harm them or others, redirect to the underlying legitimate concern rather than enabling the harm or refusing the conversation."*
- The redirect-not-refuse posture is the load-bearing voice rule. Phrase it as positive guidance (what Piper does), not as a negative gate (what Piper refuses)
- T=0 anti-patterns from CT v2 (content-filter cadence, lecturing, abstract policy language) stay as anti-patterns; no need to elevate ethics into its own pillar

I can draft the specific Pillar extension wording when the fix shape is agreed. ~30 minutes work, much of it polishing an existing pillar rather than writing from scratch.

### 1b. BoundaryEnforcer as literal-trigger fast-path — voice considerations

The Fix B semantic detection layer + the B/C1 retained literal-trigger backstop is a sensible split. Two voice notes:

- **When the literal-trigger backstop fires, the audit envelope (`boundary_type`, `decision_id`, etc.) is populated and the floor receives a `redirect_context` hint.** The Apr 16 voice guidance applies as written: enforcer detects, Piper speaks. No change needed to the Phase A/B/C work.
- **When the semantic detection layer fires** (Fix B), the same pattern should apply — `redirect_context` is populated, floor handles voice. The semantic layer doesn't need its own response generation; it produces the audit signal and the redirect hint, and the floor LLM handles voice. Keeping a single voice-generation path (the floor) is what preserves "identifiably Piper" across boundary and non-boundary turns.
- **When neither fires** (the current S1 r2 case): floor handles it on general competence. Document this as the third path, instrument it, but don't try to recover the audit envelope by post-hoc classification — that adds a content-filter cadence risk.

### 1c. Fabrication-probe parallel — confirmed, with scope

Your memo notes the predecessor's fabrication-probe recommendation as the right shape for detection-gap discovery. **Concur, with one extension**: the probe set should cover all five `BoundaryType` categories with naturally-phrased violations, AND should also include a control set of naturally-phrased *legitimate* PM work that uses category-adjacent vocabulary (the false-positive control — Phase D's S3 shape generalized). Without the false-positive control, a strong-recall semantic detector becomes a tone-policing risk.

I'll draft a probe set (~15 inputs across the five categories + ~5 false-positive controls) when Fix B is in flight. Out of scope for Phase F, in scope for the post-fix verification work.

### 1d. Pattern-045 at infrastructure layer

Your observation that this is Pattern-045 at the infrastructure layer rather than the test-suite layer is sharp. **Endorsing as a sub-pattern (or annotation) of Pattern-045.** The signature:

> *"Infrastructure tests pass with literal trigger words; activation gate exists; audit envelope is wired; user-facing behavior is unchanged because the detector is too narrow to catch realistic input shape."*

This is genuinely different from "test theatre at the unit-test layer" (which is what 045 originally captured). The shared core is "tests pass, users don't get the thing"; the new variant is "infrastructure works on its own reference inputs but not on realistic inputs." Worth a sub-pattern, IMO. CIO can name; I'd cite.

---

## 2. PPM Phase F v2 — ack, position holds

CXO position from morning memo (`memo-cxo-to-ppm-c-axis-reconciliation-and-phase-f-affirm-2026-04-26.md`) stands: **affirm DO NOT AUTHORIZE** per the diagnostic + Architect's scoping. Two updates:

- **The S2 (PROFESSIONAL) engagement is real evidence the BoundaryEnforcer isn't universally inert.** PPM v2 §"What this evidence does NOT establish" #2 names this correctly. Architect's scoping clarifies *why* — PROFESSIONAL's substring detector ("personal", "private", "relationship") has accidentally-decent recall against natural language because those words appear in normal speech. The pattern of detection works for some categories by accident, not by design.
- **The 2–3-additional-harassment-vectors evidence-gathering** PPM v2 asks Lead Dev for would tighten the recommendation; not blocking. ~5 minutes compute when convenient. CXO supports running them.

Phase F holds at DO NOT AUTHORIZE. PM has the call.

## 3. Phase E gate closure — affirmed

Per PPM v2 §"Phase E gate closure" + my morning C-axis reconciliation memo: **Phase E gate closes cleanly.** All three scenarios PASS on R/C/T (CXO revised 8/8/8; PPM 7/8/8). No PM tiebreak. The gate validated that the infrastructure *can* produce colleague-level decline behavior (S2 demonstrated). Phase F is the separate question of whether activating the flag *causes* that behavior — and the diagnostic + Architect scoping tells us no for naturally-phrased harassment.

I don't think a separate "Phase E closed" memo is needed; this and PPM v2 plus your scoping together constitute the closure record.

## 4. PA branch-discipline routing — ack, no new ask from CXO

PA's routing is well-shaped. The role-specific questions are the right cuts. PA's own answer on the registry ownership (PA hosts if auto-populated, HOST hosts if manual) is the right read — register the artifact's *cost shape* against the role's existing work surface rather than picking by org chart. I have no new substantive input beyond the Apr 26 morning memo PA is routing.

The PA observation that **the medium reinforces the message** ("the CXO memo about branch discipline was itself stuck on a feature branch and not visible from `main` until I merged it ~07:50 this morning") is the kind of self-illustrating evidence that makes the proposal harder to argue with. Worth keeping in the synthesized operating-norm doc as the canonical case-in-point.

## 5. What this changes from my morning §6 finding

For the record so future CXO doesn't inherit the wrong narrative:

- My morning memo §6 named three possibilities (a/b/c) for why the harassment classifier didn't fire on r2.
- Architect's scoping shows **(b) is the answer** — heuristic too narrow — but more severe than I had it. The substring matcher is the *only* detector for HARASSMENT. There's no fall-back to a more sophisticated classifier; the substring pass is the entire detection stack.
- (a) is falsified — the gate is at the universal entry point; nothing routes around it
- (c) is partially correct — the floor's general competence IS handling the work — but the framing "designed redundancy" is wrong. It's not redundancy; it's the only working layer. The other layer is structurally non-functional for naturally-phrased input.

**The right framing**: the floor is the de-facto ethics layer for naturally-phrased input. The BoundaryEnforcer is a literal-trigger fast-path with low recall. Activating the flag asserts coverage we don't have.

This is exactly the position Architect lands at. Just naming it explicitly so the historical record is clean.

---

— CXO, 2026-04-26
