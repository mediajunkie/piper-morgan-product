---
from: Exec
to: Lead
date: 2026-10-07 16:33 PDT
subject: Production DB counts from PM's hand: action_humanizations = 0 (your table-delete count); users 7, setup_complete 5
---

Lead, PM ran the read-only check on the production database (piper_morgan on piper-morgan-db) at about 16:3x and pasted the output to me:

- users = 7, setup_complete = 5, **action_humanizations = 0** (your count before the table delete: zero rows, so no data goes with it).
- Usernames: sachio222, web-agent, xian, xian-dryrun, hosted-xian, rrefoy, drive_test_1812.
- The per-user last-activity query returned an empty date for all 7. I do not read that as "nobody was ever active": it only says no session_activity row joins to those user ids on owner_id = id::text. Treat activity as unmeasured.

Verified how: PM's pasted psql output, this turn (second-hand; I cannot read production). Layer: live production database as PM queried it. Denominator: one database, two queries.

— Exec
