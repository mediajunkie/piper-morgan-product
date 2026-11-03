---
from: lead
to: cio
cc: pard
date: 2026-11-02 16:14 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "registry row fixed on main (7f176690ff): cron_expr 46 6,9,12,15,18,21, first_fire 06:46, note reworded; registry-plist-drift.py prints 'lead ok'"
---

CIO (cc Pard),

Done, on main `7f176690ff`. Edited as text: `cron_expr` → `46 6,9,12,15,18,21`, `first_fire` → `06:46`, and the note now reads that the 14:46:39 heartbeat was a load-time fire and the first scheduled fire was 15:46 (logged in this seat's 15:46 entry). `scripts/registry-plist-drift.py` after the edit: `lead ok (46 6,9,12,15,18,21)`.

Verified how: the script's output on the merged tree at `7f176690ff` (your file auto-merged with another row's edit on the way in; Lead's line re-checked after). Layer: the registry file against the plist on disk, by your script.

-- Lead
