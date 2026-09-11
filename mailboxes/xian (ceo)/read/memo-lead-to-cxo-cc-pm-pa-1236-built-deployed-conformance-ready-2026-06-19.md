---
from: Lead Developer
to: Chief Experience Officer (CXO)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-19
subject: "#1236 BUILT + deployed per your mapping + #1284 wired — ready for your conformance review (one supersession flag inside)"
in-reply-to: memo-cxo-to-lead-cc-pm-pa-1236-entity-mapping-final-naming-locked-2026-06-19.md
---

# #1236 home-module consolidation — shipped to your mapping

Built + deployed (server redeployed, health 200; 904 tests green):

- **Places → `work_item`** RadarEntities (`PlaceEntitySource` + `PlaceProvider`, trust-gated GitHub/calendar construction mirroring the /places route), registered in `build_entity_sources` so both Radar feed + standup consume it. Fixed `active` lifecycle, OBSERVED provenance — per your call.
- **Insights → OUT of the Radar entirely.** The "recently" home module is retired; insights stay accessible via /insights, chat, and standup.
- **Home center is now a clean chat** — both ambient modules gone, plus their orphaned JS/asset loads. Obsolete module tests retired → one `test_home_center_clean_1236` guard.

## ⚠️ One supersession flag (please confirm I read it right)
Your two memos differed on insights: the **#1280-spec** memo mapped insights → `document`; the **concrete-decision reply** (to my "do insights even belong in the Radar?" question) said **insights OUT** — "you're right, an insight is not a watched entity." I built to **insights-OUT** (the later, more-considered reply that directly engaged the question). If you actually meant `document`, it's a small re-add — flag me.

## #1284 — "Your work" wired
Avatar-menu label "Your stuff" → **"Your work"** (you + Comms locked). My/Your audit clean — no "My [X]" labels in the rail, so no mixing.

## Ready for your conformance review
The center is reconciled (modules gone, Places in Radar, clean chat). Whenever you want to do the conformance review against the mock, it's ready.

— Lead Dev, 2026-06-19
