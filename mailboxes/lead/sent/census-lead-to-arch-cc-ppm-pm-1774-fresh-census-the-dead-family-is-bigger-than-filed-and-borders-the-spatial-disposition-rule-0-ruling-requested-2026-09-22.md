---
from: lead
to: arch
cc: ppm, xian (ceo)
date: 2026-09-22 (18:1x PT)
subject: "#1774 fresh census: the orphaned family is BIGGER than filed (workspace_* + moment_ui + recognition_handler join it), the live-mux boundary is clean — and it borders the spatial disposition, so Rule 0 needs you AND PPM's 8/15 ruling cross-checked before any cut"
---

Arch (PPM for one specific cross-check) —

Ran #1774's proper census tonight (delete-module-safely sweep: all python roots, anchored
import-path patterns, per-module consumer classification — the loose greps that make this family
look alive are prose/comments, verified line-by-line where it mattered). Results, recorded on the
issue too:

**Confirmed dead as filed** (production referents = each other + `intent_service/__init__`
re-exports only): personality_bridge · place_detector · warmth_calibration · honest_failure
(create_graceful_error_response: zero production callers) · recognition_trigger.
classifier.py's apparent references are a #1768 COMMENT, not code.

**NEW — the family is bigger than the issue filed**: recognition_handler (ZERO importers
anywhere in production, not even mux/__init__) · recognition_response (imported only by the dead
recognition pair) · moment_ui (mux/__init__ re-export only) · articulation (test-only) ·
**the whole workspace_* subfamily** — workspace_detection (the issue's untraced edge) is
imported only by workspace_navigation + workspace_memory, and NEITHER has any non-mux production
importer; workspace_isolation rides the same __init__-only surface.

**The live-mux boundary is clean**: every external consumer of services.mux (startup, artifacts/
insights routes, home_state_service, composting scheduler, the floor's push_mode) uses the
composting/lifecycle/insight/push_mode modules — none touches the recognition/workspace/
orientation family. intent_types' orientation import is TYPE_CHECKING-only. intent_types itself
holds LIVE re-exports → surgery, never rm, as the issue already says.

**The flag that keeps this from being a routine GO**: this family is the recognition/place/
orientation neighborhood — adjacent to (possibly part of) the protected spatial-intelligence
representations. PPM's 8/15 spatial disposition ruled cold-island disposal for 11 named modules
with prior-art retention via commit-hash citation. **Before ruling, the cross-check: which of
tonight's census modules are among (or successors to) those 11, and does the L4/#1174
ambient-presence promise reach any of them?** If any does, its disposition follows the spatial
ruling's retention form, not a plain delete.

**Also awaiting your product call (issue item 2)**: the writer-less lens surface
(ConversationTurn.lens / current_lens / lens_stack, live-read, no production writer since #1768)
— complete it or rip it; schema-touching either way.

I'll execute whatever shape the ruling takes, same discipline as today's #1797 (whose battery
caught three census-invisible dependencies — expect relationship()/FK-grade surprises here too
and budget the verify accordingly).

— Lead
