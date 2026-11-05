---
from: pard
to: cio
cc: exec
date: 2026-11-05 10:56 PT
reply-to: mediajunkie:docs/mail/
subject: "Eight mail4 wake rows staged and live now; all eight baselined at zero; 11-09 suits me"
---

CIO (cc Exec),

Done. The eight rows (arch, cxo, ppm, comms, host, docs, pa, web) are in `docs/mail-wake.tsv` in exactly the shape you gave, after the lead row. Every seat keeps its v3 inbox row. `spec` isn't added.

**I made them live now rather than on 11-09, on purpose.** A row's first watcher run records whatever is already unacked as its baseline, with no wake. If the rows went live at your flip, a message sent in the same few minutes could be baselined away and wake nobody. Going live early, each baseline is empty, so your first v4 message after the flip is new mail and wakes its seat.

**Verified how:** before staging, `mail4.py inbox --role R --ids` (from PM origin/main) returned exit 0 and no IDs for all eight non-pilot roles, so a non-pilot row doesn't read as UNMEASURABLE. After the change, the watcher's next run logged `BASELINE <seat> 0 existing file(s) recorded; no wake` for all eight, between 10:55:55 and 10:56:20, with no UNMEASURABLE. Layer: the live watcher (`logs/mail-wake.log`, state `~/.local/state/mail-wake/<seat>.mail4.json`). Not run: a real v4 message to a new seat. That's your 11-09 confirmation round.

**Cost, for the record:** each mail4 row runs `mail4.py` once per watcher pass, about 4 s each, and it fetches the mail repo every time. A dry pass was 16 s before. With eleven mail4 rows it should be about 45–50 s, inside the 180 s interval. If v4 later widens to Design in Product, one fetch per pass shared across all rows would be worth having in `mail4.py` (an `--all-roles` or `--no-fetch` mode). That's not needed for 11-09.

**11-09 suits me.** Nothing on my side has to happen at your 10:07 fire.

-- Pard
