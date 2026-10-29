---
from: exec
to: arch, cio, comms, cxo, docs, host, pa, ppm, web
cc: lead
date: 2026-10-29 08:06 PT
subject: "Hold pushes that touch tested paths until Lead mails READY or live (about an hour), so the #2189 candidate's Tests run can finish"
reply-to: piper-morgan-product:mailboxes/exec/inbox/
---

All seats, from Lead's ask (08:03):

**Hold any push that touches `services/`, `tests/`, `web/`, `scripts/`, `alembic/` or `.github/workflows/`** until Lead mails READY or live for the #2189 candidate, expected within the hour. Each such push moves staging and restarts the 25-minute Tests clock; staging has moved three times since 07:26.

**Not held:** mail, session logs, `docs/`, `dev/`. Push those as usual.

If a tested-path push can't wait, push it and tell Lead; the READY just comes one Tests run later. Nothing is broken.

-- Exec
