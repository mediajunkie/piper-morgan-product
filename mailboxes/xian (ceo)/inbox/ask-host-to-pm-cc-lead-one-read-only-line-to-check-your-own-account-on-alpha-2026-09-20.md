---
from: host
to: xian (ceo)
cc: lead
subject: "One read-only line, whenever convenient: check your own account row on alpha (the #1599 admin-grant question)"
date: 2026-09-20
---

PM — Lead found the #1599 admin-grant migration matched zero rows for your account on the newly-
upgraded alpha DB, meaning your alpha login may not carry the flags it does elsewhere. Neither Lead
nor I can check this ourselves without crossing a trust-zone line each of us has held all weekend
(Lead would see your identity data; I'd be touching the DB) — so this one's genuinely just yours to
run, whenever you have a minute, not urgent:

```
ssh root@146.190.151.63
docker compose -f /opt/piper/docker-compose.yml exec -T postgres psql -U piper -d piper_morgan -t -c "SELECT username, role FROM users ORDER BY created_at;"
```

Just checking what your actual username/role look like on that box before you (or anyone) treats a
live drive there as representative. No action needed from you beyond running it and saying what
came back, if/when you get to it.

— HOST
