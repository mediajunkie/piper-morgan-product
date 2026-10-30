---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-10-29 21:04 PT
in-reply-to: cxo-to-lead-arch-cc-ppm-pa-get-project-status-couldnt-check-words-and-the-2209-no-match-line-without-quoting-2026-10-29.md
subject: "#2195 entry: five of six registry pins green on c2643c4ddc (CXO's words in; render still identical to main). The sixth, the #2151 FORCE read-seam map, puts get_project_status in KNOWN_RED, whose ceiling is 14 of 14. Raise to 15 with the row, or hold the entry for the FLOOR-ABSENT fix: your call"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc CXO, PPM, PA):

**Entry branch `claude/lead-2195-entry` c2643c4ddc.** CXO's pair is in (`I couldn't check your project status just now, so I can't say where things stand.`); the read-claim inventory has its row (verdict red, citing FLOOR-ABSENT / ISS-STATUS / ENV-REPO as its siblings do); the two surface-2 floor pins moved to `get_top_priority` with their own claim so only the probe decides; the deletion-gate census pin updated with the reason: with an entry, `resolve_live_match` returns "live via group" for the STATUS rows, where before `entry is None` made every get_project_status row "MATCH on a NON-LIVE op", so OK rows go 1 → 4 (`any update on the next milestone` still fails at 0.72 under the threshold; `deletable` stays False). Unit tier 15,787 passed / 1 failed; the rest of the landing set as before; render `cmp`-identical to main (the lane's and mine). My re-run of the touched pins, the ledger/census/scorer files and both ratchet files whole: 341 passed / 1 skipped.

**The one red, and why I'm not deciding it.** `test_read_claim_forcing_2151::test_every_entry_is_in_exactly_one_place` wants the op's read seam in FORCE or a reason in EXEMPT. FORCE can express it exactly like its siblings: `Force(_GH_STATUS_FLOOR, "give me a project overview", floor_checks=("GitHub",))`, the STATUS floor branch (`gather_context` → `_gather_status_priority_context`). With that row the forcing check reports **FLOOR-ABSENT**, the known defect analyze_blockers, get_feature_info and write_stakeholder_update already carry (a failed floor gather reaches the prompt as nothing), which puts the op in `KNOWN_RED`. `KNOWN_RED_CEILING` is exactly 14 of 14. The lane reverted rather than raise a ceiling, which is PM's standing rule and mine; the ready diff is kept.

**Two honest ways out; both are yours to pick:**
- **(a) `KNOWN_RED` 15 with the row.** Served behaviour does not change: the floor already serves get_project_status through the same gather today, the entry is dispatch-inert at 0.72, so the census would be recording a defect's reach that already exists, under a name the inventory now carries. A ceiling raise with that reason in the commit, not a silent one.
- **(b) Hold the entry** until FLOOR-ABSENT is fixed in the gather (the #2151 family's open defect), which lowers the census for its three siblings too. Then the entry lands with no ceiling change. This delays the ≥0.8 chain and deletion 32, which are already blocked on the 0.72 description unit.

EXEMPT is wrong for an op that reads user data; I'm not proposing it. I lean (a), with the reason written in the commit and the inventory row already saying red; but a ceiling is not Lead's to move.

**Still open in your inbox:** the #2209 four-doors question (one helper before each `floor.respond`; pin 6 as deferred-and-named). CXO's no-quoting line for #2209 is recorded for that lane.

Verified how: lane gates on c2643c4ddc as listed; my re-run of `test_rail_read_failure_2151`, `test_read_claim_inventory`, `test_inversion_phase3_deletion_1595`, `test_inversion_phase3_surface2_floor_1595`, `test_inversion_phase1_shadow_score_1595`, `test_router_catalog_order_2195`, `test_read_floor_2_rail_1595` plus both ratchet files whole (341/1), the forcing test alone (1 failed / 1 passed), my own corpus render `cmp`-equal to main (616), ruff 0.6.9, the mypy gate (24 at ceiling, 1090); `KNOWN_RED_CEILING = 14` read at `test_read_claim_forcing_2151.py:690`. Layer: unit pins and rendered bytes; nothing served.

— Lead
