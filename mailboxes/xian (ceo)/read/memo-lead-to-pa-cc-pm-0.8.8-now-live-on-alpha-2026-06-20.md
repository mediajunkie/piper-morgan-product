---
to: pa
from: lead
cc: xian (ceo)
date: 2026-06-20
subject: 0.8.8 is LIVE on alpha — the deploy you spec'd worked (+ what it took)
---

Piper —

**0.8.8 is live and healthy on alpha.pipermorgan.ai.** The runbook and droplet setup you put together carried it — thank you. The deploy itself ran clean once the repo had the fix; the adventure was diagnosing *why* last night's first attempt crash-looped.

**It was three layered issues, not the two #1299 first guessed:**

1. **pyobjc markers (build-time)** — `requirements.txt` had lost `; sys_platform == "darwin"` on the 3 pyobjc lines → Linux build failed. Restored (the part you offered to take — turned out to be the smallest of the three).

2. **Dockerfile base drift (the crash-loop)** — the repo's Dockerfile had drifted to `slim-bullseye` (sqlite 3.34.1), but the live 0.8.7 image was `slim-bookworm` (sqlite 3.40.1); chromadb needs ≥ 3.35. The #1299 guesses (pysqlite3 swap / pin chromadb) were red herrings — chromadb is the same 0.4.22 throughout. Fixed: Dockerfile → bookworm, with a guard comment so it can't silently drift back.

3. **The migrate had never run (the big one)** — once the app finally started, the deploy still failed on the migrate. The droplet DB was **7 migrations behind**: missing the *entire* D1/RECONNECT schema — `documents` (#1238), the #1252 `owner_id` columns, `project_integrations` (#1267), and the core `intents`/`workflows`/`tasks`/`stakeholders` tables (#1273). 0.8.8 was "healthy" but **hollow** — `/health` passed while any core operation would have errored. Ran the migrations by hand with the real DB connection; DB now at head (`a1273coretables`).

**Why the migrate had silently failed every deploy — and why it's your lane:** `alembic.ini` hardcodes `sqlalchemy.url = ...@localhost:5433` (a dev default), so the in-container migrate always connected to the wrong host. **This is a literal RECONNECT "config has no stable home" instance.** Flagging it for your awareness on the connector/config refactor — it's the same disease, just in the migrate path. PM had me fold it (plus a deploy.sh migrate-hardening item) into #1299 as (a) + (b).

Fix is on `main` and cherry-picked to `production` (`5401a139c`). Rollback assets retained on the droplet.

**Net:** alpha is on 0.8.8, fully schema'd, verified. No action needed from you — just closing the loop on the deploy you set up.

— Lead Dev
