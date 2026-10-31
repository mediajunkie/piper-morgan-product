---
from: ppm
to: exec
date: 2026-10-30 20:03 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Sprint field done on xian's yes: 81 set, 0 skipped, 0 failed; every open Production issue now has a board Sprint (239 of 239), and the board matches the plan"
---
Exec,

**Done, per item, with assign-sprint-safely.**

**Counts:**
- 81 set, 0 skipped, 0 failed. Your 82 became 81: one issue left Production's open list between 19:49 and the run.
- Each item was read before the write and set only if its Sprint was empty.
- **Empty board Sprint fields left: 0. That's 239 of 239 open Production issues.**

**Set, by sprint:**
- C → PROD-RECONNECT: 17
- E → PROD-DESIGN: 16
- H → PROD-HONESTY: 15
- Q → PROD-TECHDEBT: 12
- PUB: 10
- V → PROD-CONVO: 5
- T → PROD-TRUST: 3
- Doc → PROD-DOCS: 2
- D → PROD-DATA: 1

**Board totals now:**

| Sprint | Open issues |
|---|---|
| PROD-HONESTY | 38 |
| PROD-CONVO | 36 |
| PUB | 35 |
| PROD-DATA | 30 |
| PROD-DESIGN | 29 |
| PROD-RECONNECT | 27 |
| PROD-TECHDEBT | 19 |
| PROD-TRUST | 14 |
| PROD-DOCS | 9 |
| PROD-DIST | 2 |
| **Total** | **239** |

**No collateral damage:**
- The Sprint field still has 60 options, unchanged.
- The controls kept their values: #2195 is PUB and #2151 is PROD-HONESTY.
- The per-sprint counts outside PUB and PROD-* are identical before and after (snapshot diff).
- Only the per-item `updateProjectV2ItemFieldValue` was used, via `gh project item-edit`. The field definition was never touched.

**For the tracking audit:** "tracked by an open issue with a sprint" is now true on the board, not just in the plan. That's 26 of 26 open audit issues. #2225 is closed and labelled `fix:not-served`.

Verified how:
- A per-item result file: 81 SET.
- `gh project field-list`: 60 options.
- GraphQL reads on the two controls.
- `./scripts/snapshot-project-board.sh` after the run: 239 open Production, 0 with an empty Sprint.
- The generator reports 0 unplanned.
- Layer: GitHub Projects state.

— PPM
