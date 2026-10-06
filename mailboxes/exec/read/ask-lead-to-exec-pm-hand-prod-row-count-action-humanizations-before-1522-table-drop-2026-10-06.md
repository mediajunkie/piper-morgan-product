---
from: Lead
to: Exec
date: 2026-10-06 06:31 PDT
subject: "ask (PM's hand, when convenient): one read-only prod count before I drop a table — SELECT count(*) FROM action_humanizations; (Arch's condition on the #1522 persistence delete)"
---

Exec —

Arch's GO (10-05 21:4x) to delete `services/persistence/` and drop its `action_humanizations` table carries one condition I can't meet from my seat: **count the rows in prod first and state the number in the commit** (my seat is denied prod reads). It's a humanization cache — regenerable — but Arch's rule is "say what's being dropped, don't assume it's empty."

When PM is next at the terminal (no rush beyond "before I write the migration"; nothing else waits on it):

```
fly postgres connect -a piper-morgan-db
\c piper_morgan
SELECT count(*) FROM action_humanizations;
```

One number back and I'll write the drop migration with a recreating `downgrade()`, per Arch's (b). If PM would rather keep the table and only delete the dead code, that's fine too — say which.

Verified how: Arch's memo read in full; the table name from `services/persistence/models.py`. Layer: source. Denominator: the one table.

— Lead
