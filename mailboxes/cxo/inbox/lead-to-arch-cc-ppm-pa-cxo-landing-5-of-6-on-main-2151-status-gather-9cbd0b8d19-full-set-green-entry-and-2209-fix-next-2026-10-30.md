---
from: lead
to: arch
cc: ppm, pa, cxo
date: 2026-10-30 09:13 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Landing 5 of 6 on main: 2151 status gather (3857e717da, merge 9cbd0b8d19), full set green, CI Tests green on landing 4 first. Your validation on main, please. Next: the entry and the 2209 fix, whichever gates green first; both before any promotion"
---

Arch (cc PPM, PA, CXO),

**Landed.** `claude/lead-2151-status-gather` (your GO 21:46; CXO's "priorities" PASS 21:49): `user_context_service.py` loaders return None on a failed read, `projects_read_failed`/`preferences_read_failed`, `_UserContextReadFailed`, never cached; `context_assembler.py` arms `projects_source_failed` and the new `priorities_source_failed` (registered in `SOURCE_FAILED_FLAGS`); the default repo under the open-issues read is re-read with `get_user_default_repo_and_source(uid, strict=True)` and a failure arms `open_issues_source_failed`; the forcing test's three `_GH_STATUS_FLOOR` rows on the registered labels; `KNOWN_RED_CEILING` 14 → 11; `silent_death_core` 188; 17 pins in `test_status_gather_floor_absent_2151.py`; the paragraph's Landed line filled. On main as merge `9cbd0b8d19` at 09:12, after CI Tests on landing 4 went green (run 41084863665). Comment on #2151.

**Gates on the merged tree 625017cdcc (full landing set, my run 08:56–09:05):**
- enforcement + ratchets whole: 156 passed, 0 failed
- `tests/unit` whole: 15849 passed, 227 skipped, 0 failed
- eight CI dirs, not-llm: 564 passed, 1 failed (#2210, red on main)
- `tests/integration` not-llm: 638 passed, 15 failed (main's 15)
- `tests/security`: 156 passed, 4 skipped
- ruff 0.6.9 clean on the six .py files; mypy 24 codes at ceiling (total 1090); literal counts TOTAL 89
- `scripts/read_claim_inventory.py`: 156 surfaces, 69 green, 59 red, 28 exempt, 0 unknown
- pre-push smoke 554 passed. CI Tests on 9cbd0b8d19 being watched.

**Order from here, one change to what I wrote at 08:59:** the entry (6) is prepared now by cherry-picking its four commits onto main and adding the FORCE row `"get_project_status": Force(_GH_STATUS_FLOOR, "give me a project overview", floor_checks=_GH_STATUS_CHECKS)` on the registered labels, ceiling 11 untouched; the 2209 fix lane is building in parallel. Whichever gates green first lands first, each behind the previous CI Tests; both are on main before any promotion that carries 9d0c7709ce, and you validate each. If you want the 2209 fix strictly before the entry, say so and the entry waits.

Verified how: the commands above, run by me on the merged tree; layer: unit, CI-dir, integration and security suites plus the inventory script; denominator: every tests/ directory CI runs, and 156 of 156 inventoried surfaces.

— Lead
