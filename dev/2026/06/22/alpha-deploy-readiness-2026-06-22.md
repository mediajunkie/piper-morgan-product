# Alpha deploy readiness — 0.8.8 → next (RECONNECT + security + design)

**Author**: Lead Dev · **Date**: 2026-06-22 · **Status**: DRAFT for PM review (no-production-touch prep; the deploy itself is PM-coordinated)
**Mechanism**: per `docs/internal/operations/alpha-deployment-runbook.md` (current, I wrote it 06-19/20). This doc is the *delta* on top of that runbook for this specific cut.

## TL;DR — lower-risk than it looks
The alpha droplet's DB is **empty** (0 conversations, 0 documents, no github-prefs file), so **all three backfills are no-ops** — there's no data-migration risk. The deploy reduces to two real prereqs: **(1) cut a release to the `production` branch** (it's 314 commits behind main), and **(2) add `ENCRYPTION_MASTER_KEY` to the droplet `.env`** (the #358-B encryption code raises hard without it). Then the standard runbook deploy, running the **2 new migrations via the #1299 mitigation** (not deploy.sh's known-broken in-container migrate).

## Current state (verified read-only, 2026-06-22 08:xx)
| | Droplet (`alpha.pipermorgan.ai`, 146.190.151.63) | Staged (`origin/main`) |
|---|---|---|
| App version | **0.8.8** | HEAD (0.8.8 + 314 commits) |
| `production` branch | tip = `5401a139c` (v0.8.8) | main is **314 commits ahead** |
| DB alembic head | **`a1273coretables`** (0.8.8 RECONNECT schema — the 7-behind backlog was caught up in the 0.8.8 deploy) | code head = `000baa96d800` |
| DB data | **0 conversations, 0 documents** (empty) | — |
| `ENCRYPTION_MASTER_KEY` in `.env` | **ABSENT** | required by `services/security/field_encryption.py` |
| Containers | all healthy (app Up 2d, caddy 2wk, pg/redis/chroma healthy) | — |

## What's shipping (0.8.8 → HEAD, the highlights)
- **RECONNECT WS-1** (#1199/#1226): DB-backed connector config, honest-degrade no-repo UX, honest standup (#1289).
- **Security**: #358 + #358-B (AES-256-GCM field encryption + encrypted content columns + per-user LLM key #1185), #1307 (admin_compose removal), #1308 (auth-exempt-list lint), #1232 (connector protocol).
- **Design**: #1286 D2 (token system, responsive shell, mobile nav), #1238 (documents→Radar), #1269/#1239 (standup/work-item Radar sources).
- **Infra**: #1299 (Dockerfile bookworm for chromadb sqlite).

## Migrations to run on deploy (2, since v0.8.8)
`a358encsecret` (encrypted secret column on user_api_keys) + `000baa96d800` (connector_configs table). `alembic upgrade head` from `a1273coretables` applies both. **Run via the #1299 `_run_migrate.py` mitigation in the runbook** — deploy.sh's `docker compose exec app alembic upgrade head` silently connects to `localhost:5433` (nothing) and no-ops.

## Backfills — ALL NO-OPS this deploy (empty DB), but the scripts exist for when there's data
- `backfill_encrypt_content_358b.py` — encrypts existing plaintext content; **no-op** (0 rows). (Idempotent + key-refusing; safe to run.)
- `backfill_connector_configs_1226.py` — github_preferences.json → DB; **no-op** (no json on droplet).
- `backfill_documents_1238.py` — ChromaDB docs → documents table; **no-op** (0 docs).

## Prereqs / decisions for PM
1. **`ENCRYPTION_MASTER_KEY`** — generate a fresh 32-byte base64 key, add to `/opt/piper/.env`, and **back it up somewhere durable** (password manager / keychain). Since alpha has no encrypted data yet, generating fresh is zero-risk now — but once data exists, losing this key = unreadable data. Generate: `python -c "import os,base64; print(base64.b64encode(os.urandom(32)).decode())"` (or `openssl rand -base64 32`).
2. **Version number** — 0.8.8 → ? Given the payload (whole RECONNECT sprint + encryption + design system), **0.9.0** fits a minor bump. Your call; the release-runbook drives the bump.
3. **MCPB clean-machine test** — the third batten-down item; separate from this deploy (does not block it).

## Deploy sequence

### Phase A — RELEASE (local git; per `release-runbook.md`)
Version bump → merge `main` → `production` → tag. Brings `production` to the new release so the droplet's `git archive origin/production` pulls the right code. (Exact steps: release-runbook.)

### Phase B — DEPLOY (droplet; per `alpha-deployment-runbook.md` "Full safe deploy procedure")
1. **SSH + backup** (.env / Caddyfile / override + tag the working image + tar the code) — runbook step 1.
2. **Add the master key** to `/opt/piper/.env`: `ENCRYPTION_MASTER_KEY=<generated>` (do this BEFORE deploy.sh so the new app starts with it).
3. **Push code**: `git fetch origin production && git archive origin/production | ssh root@alpha.pipermorgan.ai 'tar -x -C /opt/piper'`.
4. **Restore config + deploy**: restore .env/Caddyfile/override, `cd /opt/piper && ./deploy.sh`.
5. **Run migrations via the #1299 mitigation** (the `_run_migrate.py` block in the runbook) — NOT a bare `alembic upgrade`. Verify head = `000baa96d800`.
6. **Backfills**: skip (all no-ops on empty DB) — or run `backfill_encrypt_content_358b.py` once for good measure (idempotent, instant on 0 rows).
7. **Restart app** clean against the complete schema: `docker compose restart app`.

## Verification (post-deploy)
- `docker exec piper-app grep -m1 '^version' /app/pyproject.toml` → new version.
- `docker compose exec -T postgres psql -U piper -d piper_morgan -tAc "TABLE alembic_version"` → `000baa96d800`.
- `curl -s -o /dev/null -w '%{http_code}' https://alpha.pipermorgan.ai/` → 200/302 (not 5xx).
- Smoke: log in, send a chat (exercises the encrypted-write path → confirms the master key works), check the standup (honest path) + a "what should I work on?" (honest-degrade no-repo).

## Rollback
Per runbook: `tar xzf "$B/opt-piper-code.tar.gz" -C /opt/piper` → retag the `rollback-*` image → `docker compose up -d app`. (Empty DB → no data-rollback concern; the 2 new migrations are additive.)
