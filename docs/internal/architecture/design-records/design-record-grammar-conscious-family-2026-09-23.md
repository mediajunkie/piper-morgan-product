# Design record — the grammar-conscious / recognition / workspace family (deleted 2026-09-23, #1774)

**Why this record exists**: delete-module-safely's extract-before-delete rule (PM-033d precedent)
— git history holds code; it doesn't surface ideas. **Retrieve any of it from commit `67adfc2023`**
(the last tree holding all thirteen modules), e.g.
`git show 67adfc2023:services/mux/orientation.py`.

**Ruling**: Arch, 2026-09-22 (memo `rule-arch-to-lead-…-1774-go-on-the-full-family…`) — GO on the
full family after the spatial-disposition cross-check came back clean (the spatial record's
"place_detector" is an informal name for `place_service`'s role; the only `class PlaceDetector`
in the repo was this dead one). Census: Lead 2026-09-22/23 (all python roots, anchored import
paths, package-path re-export sweep, test-side referents; on #1774). Zero production consumers
outside the family and the two `__init__` re-export surfaces, which themselves had zero
consumers for these names.

## What the family was (one paragraph each — the ideas, not the code)

**The "grammar-conscious" intent layer** (`services/intent_service/`, #410-era, ADR-055):
- `personality_bridge.py` (290 lines) — transformed a raw `Intent` into an `IntentUnderstanding`:
  the same classification wrapped in an *experiential narrative* ("I think you want to search…",
  a confidence expression, place-awareness) so responses read as a colleague who understood you
  rather than a system that parsed you. The `IntentUnderstanding` / `IntentClassificationContext`
  dataclasses lived in `intent_types.py` (deleted in the same commit; the module's live
  `Intent`/`IntentCategory` re-exports survive).
- `place_detector.py` (142) — *Place* in MUX grammar = WHERE the interaction happens (Slack DM vs
  channel vs web), and the claim that place should shape register (casual / concise-others-
  watching / full). The live successor for the channel dimension is the Slack-vs-web surface
  handling in the floor and #1466's identity binding; register-by-place was never wired.
- `warmth_calibration.py` (382) — the thesis that warmth is *removing coldness where it creates
  distance*, not adding personality everywhere: calibrated error phrases, formality levels,
  per-space defaults. Its live descendant is the floor's honest-copy contract (CXO's four-bucket
  LLM-error copy, #1824; honest-empty family #1717/#1730) — the same instinct, owned by copy
  contracts rather than a calibrator class.
- `honest_failure.py` (206) — turn "IntentClassificationFailedError: LLM response malformed" into a
  graceful admission with follow-up suggestions. Superseded outright by the honest-degrade rail
  (`DegradationResponse`, #1231) and the floor's not-recognized fallback — which is *why* its
  `create_graceful_error_response` had zero callers.

**The recognition system** (`services/mux/`, #410/#411/#412, ADR-046):
- `orientation.py` (949) — `OrientationState`: how Piper (Entity) perceives the current Situation
  through several lenses at once; `ChannelType`, `TrustContext`, `RecognitionOptions`,
  `ArticulationConfig`. The grammar-aligned "perception" model behind everything below.
- `recognition_trigger.py` (278) — *recognition > recall*: ~50% of users can't articulate a precise
  query, so on uncertain intent, offer options to recognize instead of acting. Decided WHEN to
  offer.
- `recognition_response.py` (428) — formatted those options per channel.
- `recognition_handler.py` (302) — consumed the user's selection; #412 added feedback recording
  (`recognition_feedback.py` — NOT deleted; it has its own live surface).
  The idea survived in a different body: the first-contact block (#1655/#1683 era `first_contact.py`),
  the offer/arming seam (#846 one-slot store, #1694 bare-affirmative binding) and CLARIFY routing
  are the shipped forms of "offer options when uncertain" — with the arming discipline this family
  lacked (see #1855 for the general-case gap that still exists).

**Moment UI** (`moment_ui.py`, 668, #418, ADR-046) — ten Moment types, urgency/visual-weight
rendering of situations into interface moments. The live "moment" surface became the attention
board / composting pipeline (`services/mux/composting_*`, `insight_*`, `push_mode.py`), which
never imported this renderer.

**Workspace family** (#416 epic: #658 detection, #659 navigation, #660 isolation, #661 memory):
- `workspace_detection.py` (198) — detect a context switch from message signals → `WorkspaceContext`.
- `workspace_navigation.py` (212) — natural-language templates narrating the switch
  ("switching from X to Y; last time you were…"), `humanize_duration`.
- `workspace_isolation.py` (272) — boundary rules (HARD/SOFT/OPEN) between work / personal / client
  contexts; filtering for isolation. The one idea here with a live cousin: ADR-071's owner/global
  domain fields and #1532's session ownership do isolation at the *data* layer instead.
- `workspace_memory.py` (301) — context-relevant memory retrieval on switch.
  The user-facing successor is per-project scoping (ProjectDB, default repo, #1042) — explicit,
  not inferred.

## Why it died, in one line

The product routed around inference-heavy ambient framing toward explicit, honest, cheaper
mechanisms (floor copy contracts, honest-degrade rails, explicit project/repo scoping, offer
arming). Nothing here was wrong; nothing here was reached.

## What was deliberately NOT deleted

`intent_types.py` (surgery: live re-exports kept) · `recognition_feedback.py` · `consciousness.py`
(different, live package `services/consciousness` is what the app uses; the mux one was not
ruled) · the lens surface (`ConversationTurn.lens` / `current_lens` / `lens_stack`) — Arch ruled
"rip, not complete" but as its OWN Rule-0 item with its own reader census (schema-touching); filed
separately.
