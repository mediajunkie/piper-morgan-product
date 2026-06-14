# UAT Runbook — Testing Trust-Gated Surfaces

**Issue:** #1148 UAT-TEST-USER-STAGE · **Added:** 2026-06-05 · **Owner:** Lead Dev

## Why this exists

Several UI surfaces only appear/activate once a user reaches a higher **trust
stage** (ADR-053). Trust normally climbs organically across ~50 successful
interactions (NEW → BUILDING → ESTABLISHED → TRUSTED), so a fresh test user like
`m1-test` sits at **Stage 1 (NEW)** and structurally **cannot** see them:

| Surface | Gate | Notes |
|---|---|---|
| `/lists` | Stage 4 (TRUSTED) | nav link hidden below gate |
| `/documents` | trust-gated | per #1142 / #1147 |
| Push-mode insights | Stage 3+ (ESTABLISHED) | suppressed below gate (#1032) |

During the #1047 UAT smoke these were logged as "missing" when they were really
just gating-invisible (#1142 reconciled this). To actually verify them, put a
test user at the required stage with the dev affordance below.

## The dev trust-stage tool (GUI)

A **dev-only** page (404s in production — `PIPER_ENVIRONMENT` gate, see
`web/routers/dev_trust.py`):

1. With the server running locally, open: **http://localhost:8001/api/v1/admin/trust**
2. Pick the user (e.g. `m1-test`) — the dropdown shows each user's current stage.
3. Choose the target stage (defaults to **Stage 4 — TRUSTED**) and click **Apply trust stage**.
4. **Reload the trust-gated surface** (e.g. `/lists`). The change takes effect on
   the next request — the tool invalidates the trust cache on save (#984).

To test the *negative* case (surface correctly hidden), set the user back to
**Stage 1 — NEW** the same way.

## CLI / curl alternative (for agents)

```bash
# Find a user's id from the picker page, then:
curl -s -X POST http://localhost:8001/api/v1/admin/trust/set-stage \
  -d "user_id=<UUID>" -d "stage=4"
```

Stages: `1`=NEW, `2`=BUILDING, `3`=ESTABLISHED, `4`=TRUSTED.

## Safety

- The router **404s in production** (the route is invisible there, not merely
  forbidden). There is no legitimate production use for setting a user's trust
  level. Gate is unit-tested (`tests/unit/web/routers/test_dev_trust.py`).
- It's exempt from auth as a localhost scaffold (same category as the editorial
  compose UI) — fine for local UAT, unreachable in prod.

---

## Driving AUTHENTICATED dev endpoints from a shell (composting seed, etc.)

The dev admin endpoints (e.g. `POST /api/v1/admin/composting/seed`, the trigger,
trust-stage applies) require **auth** — a bare `curl` gets `401`. The browser
GUI works because you're logged in; to drive them from a shell (server-side UAT,
scripts), mint a token for the target user and pass it as a Bearer header:

```bash
# 1) Mint an access token for the user (same dev-fallback secret the running
#    server uses, so it validates). WRITE IT TO A FILE — see the gotcha below.
POSTGRES_PORT=5433 ./venv/bin/python -c "
from uuid import UUID
from services.auth.jwt_service import JWTService
open('/tmp/tok','w').write(JWTService().generate_access_token(
    user_id=UUID('<USER_UUID>'), user_email='<email>',
    scopes=['read','write','admin'], username='<username>'))
"
# 2) Call the endpoint with the token
curl -s -X POST "http://127.0.0.1:8001/api/v1/admin/composting/seed?user_id=<USER_UUID>&count=2" \
  -H "Authorization: Bearer $(cat /tmp/tok)" -w "\nHTTP %{http_code}\n"
rm -f /tmp/tok
```

**⚠️ Gotcha that costs two false `400 Invalid HTTP request received`:** do NOT
capture the token via `TOKEN=$(python -c "...print(token)")`. `JWTService` logs
to stdout on init/generate, so the capture includes log lines (~1492 chars vs a
clean ~595-char JWT) → the malformed multi-line header is rejected by uvicorn/h11
as a protocol error *before* auth even runs (so it looks like a server bug, not a
token bug). **Write the token to a file** (or redirect logs) so the capture is
the token only. (Lead Dev, 2026-06-13, during the #1165 composting-seed UAT.)

`m1-test`: user_id `009afc8c-bbb0-4391-8265-1575c0812949`, email `m1t@dinp.xyz`.
