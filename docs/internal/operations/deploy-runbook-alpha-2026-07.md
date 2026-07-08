# Alpha Deploy Runbook — the July 2026 "big-bang" deploy

**Written**: 2026-07-07 evening (Lead Dev), for the deploy PM cleared earlier today.
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

## Phase 2 — Promote main → production branch (from your machine or the droplet)

```bash
git fetch origin
git checkout production && git pull origin production
git merge origin/main --no-edit     # expect a LARGE merge; no conflicts expected (production is strictly behind)
git push origin production
```

## Phase 3 — Set the new environment variables on the droplet (BEFORE the app restarts)

Into however `/opt/piper` injects env (compose env_file / .env — verify which exists):

```
ENCRYPTION_MASTER_KEY=<the base64 key from Phase 0>   # 358/1305 encryption (fail-closed reads need it)
# Optional usage-cap tuning — defaults are fine for the cohort (100 req/min, 10 concurrent):
# USAGE_CAP_RATE_PER_MINUTE=100
# USAGE_CAP_MAX_CONCURRENT=10
```

Redis is already on the droplet (#1311) — the usage-cap middleware needs it running; it's
in the compose stack, no action expected. **If Redis were somehow down, every request would
503 by design (fail-closed)** — that's the tell.

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
