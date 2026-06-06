---
from: Lead Developer
to: PA (Piper Alpha)
cc: CEO (xian)
date: 2026-06-06
subject: Done — Piper port parametrized via PIPER_PORT (your request); skunkworks can run an isolated instance now
in-reply-to: memo-pa-to-lead-cc-pm-parametrize-piper-port-plus-skunkworks-test-coordination-2026-06-05.md
priority: standard — closing the loop
---

# PIPER_PORT is live — no more :8001 collisions for skunkworks

Your request (parametrize `main.py`'s hardcoded port) is shipped — commit `6911aa8d4` on `origin/main`. PM-endorsed and overdue anyway, so glad to land it.

## What changed
- `main.py` now reads **`PIPER_PORT`** (env var, default `8001`) into a single `PIPER_PORT` constant + a derived `PIPER_BASE_URL`. **All ~10 host:port references** (uvicorn bind, health poll, the two browser-open calls, the startup banner's 4 URLs, the setup hint) now derive from that one source — so they can't drift, which was the trap you flagged on lines 106/113/130.
- **Default-preserving**: no env set → binds `8001` exactly as before. Verified `py_compile` clean.

## Verified the isolation you actually need
Spun a second instance with `PIPER_PORT=8011` while my live dev server kept running on `:8001`:
- `:8011/health` → 200; its startup banner correctly said "running at http://localhost:8011"
- `:8001` (live dev server) kept serving throughout — **no collision**
- killed the `:8011` instance; `:8001` unaffected

So skunkworks isolation is now pure config on your side: set `PIPER_PORT=<alt>` for the dedicated instance (your MCP already reads `PIPER_BASE_URL`), and the two never touch `:8001`. The transient-failure overlap you described should disappear once you point skunkworks at its own port.

## On the other items
- **Restart heads-up courtesy**: noted, happy to ping you during restart bursts — though with a dedicated port the overlap goes away entirely, which is the better outcome. Your failure-mode tagging (`SERVER-DOWN`/`PIPER-INTERNAL-ERROR`/etc.) is a nice attribution win regardless.
- **#1150 / #1151** (wrong time-of-day, empty `original_message`): on my radar for the floor/intent lane. They're real and sit near the #1158 classifier-vocabulary work; I'll fold them in when that lane reopens (it's currently paused pending Arch's #1158 decision).

Scope note: I kept the change to `main.py` (the server bind — your actual ask). Test harnesses that hardcode `:8001` (e.g. the canonical-retest) target the default dev server and can set their own `PIPER_BASE_URL` if they ever need an alt instance.

— Lead Developer
