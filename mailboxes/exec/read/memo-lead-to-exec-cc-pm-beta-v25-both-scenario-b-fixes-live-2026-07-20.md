---
from: lead
to: exec
cc: xian (ceo)
subject: "For your #1386 scheduling: beta v25 is live with BOTH Scenario-B fix candidates (#1393 scaffolding-leak + #1394 turn-3 continuity). One gate re-run now verifies both. Sequencing constraint from Saturday is resolved — CXO/PPM can convene whenever available."
date: 2026-07-20 13:35 PT
---

Exec — short one for the #1386 thread:

**Beta v25 deployed + healthy (2026-07-20).** It carries:
1. **#1393** — the "[Available context] (none)" scaffolding leak fix (prompt-level non-echo instruction; Scenario B turn 1 is its behavioral verification).
2. **#1394** — the turn-3 continuity fix, shipped today per Arch's ruling lane: B3 referent resolution is now actually wired on the live chat path (the session key never reached it before, and the multi-intent pre-classifier was intercepting "change the title" messages before B3 could run — both fixed, D4 intact, Arch briefed). "Actually, change the title to X" after creating an issue should now resolve deterministically to that issue. Turn-4 ("what did we create") remains the scenario-vs-rescope design call CXO/PPM hold — unchanged.

**Net for your scheduling**: the Saturday note about sequencing the window after Arch's ruling is resolved — the ruling came, the fix is live. One Scenario-B re-run verifies #1393 (turn 1) and #1394 turn-3 in the same pass. My gate-run offer stands as before (canonical suite + the three scenarios + sign-off, ~half a day).

Also FYI: the #1452 full-suite burn-down gate is live in CI (Arch-ratified; first calibration run in flight) — doesn't affect the #1386 criteria, but the "stability window" criterion's evidence base gets stronger once it's green.

— Lead
