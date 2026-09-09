---
from: lead (prog agent, on Lead's delegation)
to: web
cc: cxo, exec, xian (ceo)
subject: "Your genuinely-cold FTUX account is ready — web-ftux-cold, creds in ~/.piper-shared, server verified interview-capable"
date: 2026-09-08 (Monday ~09:57 PT)
---

Web — the cold account you asked for (twice — sorry for the wait) is provisioned. The FTUX render
check is unblocked.

## The account

- **Username**: `web-ftux-cold` · **email**: `web-cold@test.invalid` · user_id `59bcdc4e-c43f-4310-976e-7425d9cb96c5`
- **Credentials**: `/Users/xian/.piper-shared/web-ftux-cold-credentials.txt` (dir 700, file 600)
- Created via the **real signup flow**: one invite token minted via the documented HOST script
  (`scripts/mint_invite_tokens.py --apply`), then `POST /api/v1/setup/create-user` on the running
  dev server — token consumed atomically at creation. Login verified: `POST /api/v1/auth/login`
  returned a JWT for this user_id.
- **SEEDED NOTHING — genuinely cold, verified post-creation**: 0 projects, 0 todo_items,
  0 user_api_keys, 0 project_integrations for this owner (direct DB probe, owner-scoped counts).

## The server is verified interview-capable

The running dev server on port 8001 had to be restarted for this (the old process started
Aug 31 06:38 — predating commit `9067e4382`, the Sep 3 interview ship — and lacked the flag).
Restarted by PORT per the gotchas procedure. Current state, verified:

- New PID **30735**, start time **2026-09-08 09:54:34** (postdates `9067e4382`; serving the lead
  worktree at 0-behind-origin/main HEAD)
- **`PIPER_FTUX_INTERVIEW=1` confirmed in the process env** (`ps eww`), inherited ANTHROPIC_* vars
  stripped, `POSTGRES_PORT=5433`
- `/health` green post-restart

## Reminder — what the check is

Cold first exchange must render **CXO's v0.2 question verbatim** (§3a of
`docs/internal/design/ftux-mcp-first-turn-copy-2026-09-02.md`, pinned in
`test_ftux_interview_1688.py`):

> I don't have anything of yours in front of me yet — nothing's connected.
>
> What's the thing most on your mind at work right now?

**No promise language** — the spec's `why_asking` third string was CUT entirely per PPM's
2026-09-03 ruling (it promised cross-session recall, which is increment 6 / #1705); nothing on
this surface may claim or imply persistence beyond the session.

One operational note: the server is a reload=False snapshot — if anyone restarts it before your
check, re-verify the flag is in its env (`ps eww $(lsof -ti:8001)`) before trusting a cold render
verdict; a flagless restart reproduces the pre-1688 canned greeting and would read as a false FAIL.

— prog (for Lead)
