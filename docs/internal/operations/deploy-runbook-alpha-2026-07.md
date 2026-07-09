# Alpha Deploy Runbook — the July 2026 "big-bang" deploy

**Written**: 2026-07-07 evening (Lead Dev). **EXECUTED 2026-07-08 evening (PM + Lead) — v0.8.10
live on alpha. AS-RUN ANNOTATIONS below marked ▶AS-RUN; this doc is now the verified droplet
deploy reference** (the "annotate with what you actually see" promise, kept). Key as-run facts
a future deploy needs:

- **SSH**: `ssh root@146.190.151.63` (`root@piper-alpha`; alpha.pipermorgan.ai resolves there).
  ⚠️ PM's `~/.ssh/config` alias `droplet` points at a DIFFERENT machine (146.190.46.184) — don't use it.
- **deploy.sh does NOT refresh code.** Refresh from the Mac first:
  `git archive origin/production | ssh root@146.190.151.63 'tar -x -C /opt/piper'`
  (droplet-local `.env` / `docker-compose.override.yml` / `Caddyfile` / `deploy.sh` are untracked → survive).
- **The container gets DB env from docker-compose.override.yml**, which now carries
  `POSTGRES_HOST=postgres` + `POSTGRES_PORT=5432` (added 2026-07-08 — this was the ROOT CAUSE of
  every historical BUILD_FAIL: alembic/backfills in-container fell back to localhost:5433; it was
  never a startup race, #1299 closed on this). deploy.sh's up-line now includes `github-mcp`.
- **ENCRYPTION_MASTER_KEY already exists on the droplet** (v0.8.9-era) — NEVER replace it;
  existing ciphertext dies with it. Phase 0's key generation applies only to a fresh box.
- **The 4b chain repair was executed** (deploy.sh's migrate ran first and skipped b1229bindings
  exactly as predicted; repaired with the stamp sequence; one-time — the pointer is clean now).
- **Backfill results (2026-07-08)**: #1305 encrypted 2 conversations + 4 turns (+4 leaf-split
  patterns); 358-B and #1306 were no-ops (young DB). All idempotent-clean.
- **Post-deploy findings wave**: #1380 (no Settings LLM-key UI), #1381 (UTC-as-local-time),
  #1382 (keychain layer dead on hosted Linux — tier-1 fixed + redeployed same night; tier-2
  OAuth-token storage gates GitHub connect). Tester dry-run PASSED end-to-end otherwise
  (invite consumed, wizard key save, chat on the per-user key) — #358 closed on it.
**Why this deploy matters**: it gates invite-sending (the invite-token system, the wizard
registration fix, password reset, the personalization-leak fix, and the usage caps are ALL
on `main` but none on the alpha instance — production's DB doesn't even have the
`invite_tokens` table yet). **Do not send batch-1 invite codes before this completes.**

**Honesty note on scope**: `deploy.sh` lives on the droplet (`/opt/piper`), not in this repo,
so steps 4–5 describe the known mechanism with verify-as-you-go framing rather than
invented specifics. This runbook doubles as the in-repo deploy documentation we've been
missing — annotate it with what you actually see and we'll correct it after this run.

---

## Phase 0 — Pre-flight (5 min, from your machine)

1. **Confirm the gate is green on main's tip**: the `Security Test Suite (Postgres)` check
   (now required) — visible on the latest code commit on GitHub. (Verified green 2026-07-07
   afternoon; re-check if new code lands overnight.)
2. **Generate the encryption master key** (if not already done) and have it ready to paste
   on the droplet — do NOT commit it anywhere:
   ```bash
   openssl rand -base64 32
   ```

## Phase 1 — Backup (10 min, on the droplet — NON-NEGOTIABLE for a migration chain this long)

```bash
ssh <droplet>
cd /opt/piper
# Dump the production DB before anything touches it:
docker compose exec -T postgres pg_dump -U piper piper_morgan > ~/piper-backup-$(date +%Y%m%d-%H%M).sql
ls -lh ~/piper-backup-*.sql   # confirm it's non-trivially sized
```

## Phase 2 — Promote main → production branch — ✅ DONE EARLY (Lead, 2026-07-08 ~12:15)

**The cut is frozen at `d1256e0ac` on `origin/production`.** Production was NOT strictly
behind (the 7/3 v0.8.9.x hotfixes were cherry-picks); the merge had 9 conflicts, all
resolved (main's code won everywhere; production kept VERSION 0.8.9.2 + its release
notes + alpha-tester docs; verified: `git diff origin/main` on the result shows ONLY
those intended artifacts). **Skip this phase during the deploy.** Work continues landing
on `main` without touching the cut; if we deliberately want something else in the deploy,
re-promote the same way (Lead can redo it in minutes).

**One decision surfaced for you (not blocking)**: the cut carries VERSION `0.8.9.2`. If
this deploy should be a visible version bump (`0.8.10`?), say so and it's a one-line
commit to `production` before deploy — your release call. `0.9.0` stays reserved for beta.

## Phase 3 — Set the new environment variables on the droplet (BEFORE the app restarts)

Into however `/opt/piper` injects env (compose env_file / .env — verify which exists):

```
ENCRYPTION_MASTER_KEY=<the base64 key from Phase 0>   # 358/1305 encryption (fail-closed reads need it)
PIPER_BASE_URL=https://alpha.pipermorgan.ai           # #1324: printed URLs, health check, AND the
                                                      # Slack/Google OAuth redirect fallbacks all
                                                      # derive from this now (localhost otherwise)
# Optional usage-cap tuning — defaults are fine for the cohort (100 req/min, 10 concurrent):
# USAGE_CAP_RATE_PER_MINUTE=100
# USAGE_CAP_MAX_CONCURRENT=10
```

**#1324 environment-name check (while you're in the .env)**: see whether `ENVIRONMENT` or
`PIPER_ENVIRONMENT` is already set to `production` there.
- If YES: the new dev-default-password guard is armed — startup will log CRITICAL if
  `POSTGRES_PASSWORD` is still the dev default (that's a real finding, not noise).
- If NO: you MAY set `ENVIRONMENT=production`, but **only if `JWT_SECRET_KEY` is also set in
  that .env** — production mode makes a missing JWT secret a hard startup failure by design
  (`services/auth/jwt_service.py`). If neither is set today, note it and we'll wire both
  deliberately after this deploy rather than improvising mid-run.

Redis is already on the droplet (#1311) — the usage-cap middleware needs it running; it's
in the compose stack, no action expected. **If Redis were somehow down, every request would
503 by design (fail-closed)** — that's the tell.

**NEW since 2026-07-08 morning**: the github-mcp-server sidecar is now IN docker-compose.yml
(#1220's hosting half — the Droplet-sidecar decision, implemented). `deploy.sh`'s compose up
starts it automatically; the app reaches it at `http://github-mcp:8082/mcp` via compose DNS
(already wired in the app's environment). Smoke check after deploy: 
`curl -s -m 5 -X POST localhost:8082/mcp -H 'Content-Type: application/json' -d '{}' ` →
**"Unauthorized" is the HEALTHY response** (the server enforces per-user OAuth per
connection — a tokenless probe SHOULD be refused; connection-refused/timeout = actually down).

## Phase 4 — Deploy (on the droplet)

```bash
cd /opt/piper
# Pull the promoted production branch / refresh the code copy (verify which mechanism
# deploy.sh expects — /opt/piper has historically been a copy, not a checkout):
./deploy.sh
```

**Known footgun (#1299b — this deploy IS its verification)**: the migrate step
(`docker compose exec -T app python -m alembic upgrade head` after a `sleep 30`) has
historically raced app startup and written `BUILD_FAIL` even when the app is fine.
**A BUILD_FAIL here may be a false alarm** — check the app directly before reacting:

```bash
curl -s localhost:8001/health          # 200 = app is actually fine
docker compose exec -T app python -m alembic current   # confirm head reached: f1305encjson
```

If the migrate genuinely failed mid-chain: the DB is transactional per-migration —
note the failing revision, do NOT retry blindly; ping me with the error.

### ⚠️ Phase 4b — MIGRATION-CHAIN REPAIR (REQUIRED this deploy — found 2026-07-08 during the promote)

The 7/3 hotfix chained `c1344invite` directly onto `000baa96d800` on production, but this
cut carries main's chain, where **`b1229bindings` (connector_bindings — the #1220 per-user
grant store) sits between them**. The droplet's `alembic_version` says `c1344invite`, so
alembic assumes `b1229bindings` already ran and **silently skips it** — `upgrade head`
"succeeds" while never creating the table. (The hotfix migration's own header documented
this exact merge moment; the repair below is order-independent — d075/e441/f1305 don't
depend on connector_bindings — so run it AFTER deploy.sh regardless of what its migrate did.)

```bash
# 1. Did the skip happen? (NULL/empty = table missing = repair needed — expected)
docker compose exec -T postgres psql -U piper piper_morgan -tc \
  "SELECT to_regclass('public.connector_bindings');"

# 2. Apply the one skipped migration, surgically:
docker compose exec -T app python -m alembic stamp 000baa96d800
docker compose exec -T app python -m alembic upgrade b1229bindings

# 3. Re-point the version to reality — did deploy.sh's migrate already apply the tail?
docker compose exec -T postgres psql -U piper piper_morgan -tc \
  "SELECT to_regclass('public.personalization_contexts');"
#   present → the tail (d075/e441/f1305) already ran:
docker compose exec -T app python -m alembic stamp f1305encjson
#   absent  → tail never ran (e.g. BUILD_FAIL was real this time):
#   docker compose exec -T app python -m alembic stamp c1344invite
#   docker compose exec -T app python -m alembic upgrade head

# 4. Verify end state — all four must hold:
docker compose exec -T app python -m alembic current        # → f1305encjson
docker compose exec -T postgres psql -U piper piper_morgan -tc \
  "SELECT to_regclass('public.connector_bindings'), to_regclass('public.personalization_contexts'), to_regclass('public.password_reset_tokens'), to_regclass('public.invite_tokens');"
# → all four non-NULL
```

## Phase 5 — The three backfills (yes, three now — #1306 landed 7/08) (on the droplet, key now present)

```bash
# 1. #358-B content columns:
docker compose exec -T app python -m scripts.backfill_encrypt_content_358b
# 2. #1305 JSON columns:
docker compose exec -T app python -m scripts.backfill_encrypt_json_1305
# 3. #1306 uploaded files (added 2026-07-08):
docker compose exec -T app python -m scripts.backfill_encrypt_files_1306
# All three print counts; all are idempotent (re-run = no-op); all REFUSE
# to run if the key is missing (that refusal = go back to Phase 3).
```

## Phase 6 — Smoke verification (10 min, from a browser)

1. `https://alpha.pipermorgan.ai/health` → 200.
2. **Login page** shows "Username or email" + a "Forgot password?" link.
3. **Log in as yourself — with your EMAIL** (the #1261 fix, live).
4. **Setup wizard** (`/setup`, step 3) shows the **Invite code** field.
5. Send Piper one chat message → normal response (personalization + usage-cap middleware
   in the request path, both silent when healthy).
6. **#358's dimension-A live check** (closes that issue): create/touch a doc or send a
   message, then confirm the newest row is ciphertext at rest:
   ```bash
   docker compose exec -T postgres psql -U piper piper_morgan -c \
     "SELECT left(content,10) FROM artifacts ORDER BY created_at DESC LIMIT 1;"
   # Expect: PMENC1:...
   ```
7. Optional cap check: hammer `/health`… actually health is exempt — skip; the caps were
   load-verified locally 2026-07-07, trust the middleware.

## Phase 7 — Aftermath

- Tell me the outcome (any step's real output if something looked off) — I close **#358**
  on the dimension-A evidence and update **#1299b** with the migrate-step verification.
- **Invites are now unblocked** — batch-1 sending is you + HOST.
- Rollback, if ever needed: restore the Phase-1 dump + redeploy the previous production tip.

---

## NOT this deploy: #1278 (Fly.io)

Fly is a **separate migration**, not part of this deploy — this run updates the existing
droplet. When #1278's turn comes (after #1306/#1220 per the agreed order), I'll need from
you, async, ~10 minutes: a Fly.io account/org with payment attached, a deploy token I can
use, region preference (sjc vs iad), and the app-name/DNS blessing (e.g.
`beta.pipermorgan.ai`). Nothing needed tonight.
