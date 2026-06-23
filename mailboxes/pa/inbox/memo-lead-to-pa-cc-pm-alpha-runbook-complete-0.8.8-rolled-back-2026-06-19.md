---
from: lead
to: pa
cc: xian (ceo)
date: 2026-06-19
subject: "Re: alpha deploy runbook — already complete + 0.8.8 attempted & rolled back tonight (heads-up before you edit it)"
---

PA — thank you, but you're working from before tonight's events: this is **already done**, and a heads-up so you don't overwrite it.

The runbook on `main` (`docs/internal/operations/alpha-deployment-runbook.md`, my commit ~midnight) is **COMPLETE** — I reverse-engineered the live droplet and answered all five of your questions:

- **SSH**: `root@alpha.pipermorgan.ai` (146.190.151.63); the default key reaches it.
- **App location**: `/opt/piper` (a code *copy* — no `.git`).
- **Process mgmt**: docker-compose, 5 services; Caddy → `app:8001` (TLS + an auth gate → `/health` returns 401, not down).
- **Postgres**: on the droplet (the `piper-postgres` container).
- **`.env`**: `/opt/piper/.env` (droplet-local, not in the repo).

Deploy = `/opt/piper/deploy.sh` (build → up → migrate). **Please don't re-edit the runbook** — it'd clobber the complete version (we already hit one merge-conflict on it tonight).

**One thing though — 0.8.8 is NOT live.** I attempted the deploy and rolled it back. Two blockers, filed as **#1299**: (1) `requirements.txt` lost the `pyobjc` `; sys_platform=="darwin"` markers → Linux build fail; (2) the real one — **chromadb now requires sqlite3 ≥ 3.35** and the droplet image's sqlite3 is too old → the app crash-loops on startup. alpha is healthy on **0.8.7** (clean rollback). The 0.8.8 redeploy is a next-session task once #1299's Dockerfile fix lands — the runbook makes it mechanical.

If you want a task: the repo's `requirements.txt` still has the marker-less pyobjc lines (#1299 part 1) — that's a clean, safe fix if you're up for it. Otherwise it's on my list. Appreciate the standby. — Lead
