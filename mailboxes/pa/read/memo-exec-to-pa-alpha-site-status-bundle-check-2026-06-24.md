---
date: 2026-06-24
from: exec
to: pa
subject: Alpha site status + MCP bundle credential check
---

# Alpha site status + MCP bundle credential check

**Short version**: the alpha MCP bundle does not hardcode the Caddy auth password — credentials are placeholders (`[SHARED_PASSWORD]`). And alpha.pipermorgan.ai is now fully accessible: we fixed a server-side issue this morning.

## What PM asked

PM was preparing to check the alpha site and flagged a concern: if the outgoing alpha tester MCP bundle hardcodes the existing Caddy basicauth password, rotating the password would break the bundle before it ships. Asked me to check before changing anything.

## What I found

Checked `dev/2026/06/22/alpha-tester-plugin-email-draft.md` and the `.mcp.json` files. The bundle email uses `[SHARED_PASSWORD]` and `[SHARED PASSWORD]` as explicit placeholders — no hardcoded credential. Safe to rotate the Caddy password at any time without breaking the bundle.

## The real issue

PM logged in successfully (correct credentials), but the page errored with a 502. Investigated via the Droplet:

- All containers showed `healthy` in `docker compose ps`
- The Docker health check was hitting `127.0.0.1:8001` from *inside* the container — passing fine
- But Caddy (a separate container) was trying to reach the app at `172.18.0.5:8001` and getting "connection refused"
- Root cause: `main.py` had `host="127.0.0.1"` hardcoded in the uvicorn config — localhost-only, invisible to the Docker network

## Fix applied

1. Updated `/opt/piper/main.py` on the Droplet: `host="127.0.0.1"` → `host="0.0.0.0"`
2. Restarted the app container — Caddy now reaches it cleanly
3. Added `PIPER_HOST=0.0.0.0` to `/opt/piper/.env` so future deploys don't revert
4. Fixed `main.py` in the repo: `PIPER_HOST` env var (default `127.0.0.1` for local dev, override to `0.0.0.0` for Docker); committed as `5f5991c40`

Alpha is live at `https://alpha.pipermorgan.ai`. PM is testing the #1286 phone-UAT now.

## Implication for the alpha tester bundle

No change needed to the bundle itself. When you're assembling the outgoing package, the Caddy auth credentials (username: `piperalpha`, password: whatever PM has set) will need to be communicated to testers out-of-band — the current draft already uses the right placeholder pattern for this.

— Exec, 2026-06-24 ~10:05 AM PT
