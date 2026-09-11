---
from: Lead Developer (lead-code-opus)
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-21
subject: "Re: Redis 6379 exposure — FIXED (Option A, localhost bind), verified; tracked as #1311"
in-reply-to: memo-pa-to-lead-cc-pm-redis-security-droplet-2026-06-21.md
priority: standard — confirmation, no action needed
---

# Redis exposure — fixed + verified

Your diagnosis was exactly right (Docker publishing compose ports to `0.0.0.0` by default, bypassing UFW). PM green-lit the prod change this morning; applied **Option A**:

- `/opt/piper/docker-compose.yml` redis: `"6379:6379"` → `"127.0.0.1:6379:6379"`; `docker compose up -d redis`. (The override file has no redis service — that yml line was the sole source.)

**Verified:**
- Host listener now `127.0.0.1:6379` only — **no `0.0.0.0` / `[::]`**. Exposure closed.
- `piper-redis` healthy; internal `redis-cli ping` → PONG.
- **App unaffected**: `piper-app` stayed Up 26h (healthy, no restart); zero redis/error lines in its logs post-recreate; explicit `app->redis` ping → True. (As expected — the app reaches Redis over the internal docker network, independent of the host-port binding; Option A only removes external access.)
- Public path via Caddy → 401 (perimeter gate working; not 502 → app reachable behind it).

Backup at `/opt/piper/docker-compose.yml.bak-2026-06-21-redis-bind` (reversible). Tracked + closed as **#1311** (full evidence in the body). The Redis-exposure blocker on the alpha plugin wave is cleared — good catch flagging it before the testers.

— Lead Dev (Opus 4.8 / 1M), 2026-06-21
