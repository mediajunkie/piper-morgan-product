# Alpha Deployment Runbook

**Status**: COMPLETE — mechanism reverse-engineered from the live droplet by Lead Dev, 2026-06-19 (was a STUB; PA flagged the gap in `memo-pa-to-lead-cc-pm-alpha-deploy-runbook-gap-2026-06-19`).
**Created**: June 19, 2026 (PA)
**Last Updated**: June 22, 2026 (Lead Dev — **0.8.9 deployed live**; corrected the #1299 migrate script for 0.8.9 [db singleton, not `engine`; POSTGRES_PASSWORD unset]; added the secrets-must-be-named-in-app gotcha + the encryption round-trip smoke). Prior: June 20 (migrate-never-ran, #1299; 0.8.8); June 19 (full mechanism + safe procedure)

---

## TL;DR

`alpha.pipermorgan.ai` is a **Digital Ocean droplet** running a docker-compose stack. Deploy = get new code into `/opt/piper` → run `/opt/piper/deploy.sh` (builds the app image, brings the stack up, runs migrations). It is **manual** — there is no CI auto-deploy.

---

## Architecture

| Thing | Value |
|---|---|
| Host | Digital Ocean droplet, `146.190.151.63`, `root@piper-alpha` |
| Domain | `alpha.pipermorgan.ai` (DNS A → 146.190.151.63) |
| Orchestration | docker-compose at `/opt/piper` (`docker-compose.yml` + `.override.yml` + `.staging.yml`) |
| Services | `piper-caddy` (TLS + auth gate), `piper-app` (the FastAPI app, `:8001`), `piper-postgres` (`:5433`), `piper-redis` (`:6379`), `piper-chromadb` (`:8000`) |
| Reverse proxy | Caddy: `alpha.pipermorgan.ai { reverse_proxy app:8001 }` — auto-TLS, plus an **auth gate**. So `https://alpha.pipermorgan.ai/health` returns **401** unauthed — that's the gate, NOT a down app. |
| App image | `piper-morgan-stable-app`, **built on the droplet** from `/opt/piper` (`build: context: . dockerfile: Dockerfile`) |
| Code on droplet | `/opt/piper` — a **copy** of the repo, NOT a git checkout (no `.git`). Droplet-local files that are NOT pulled from the repo and MUST be preserved across deploys: `.env`, `Caddyfile`, `docker-compose.override.yml` |

## The five questions (answered)

1. **Where is it hosted?** DO droplet `146.190.151.63` (`root@piper-alpha`), serving `alpha.pipermorgan.ai`.
2. **How is deploy triggered?** **Manually.** SSH in and run `/opt/piper/deploy.sh`. No push-to-`production` auto-deploy; no CI deploy workflow.
3. **Where are the env vars?** `/opt/piper/.env` on the droplet (not in the repo). Preserve it across deploys.
4. **Migrations?** `deploy.sh` runs `docker compose exec -T app python -m alembic upgrade head` after a 30s wait. ⚠️ See the footgun.
5. **Health URL?** `https://alpha.pipermorgan.ai/health` (401 = the Caddy auth gate; the app's own `/health` answers on `app:8001` inside the docker network). ⚠️ **The gate is being removed — see below (#1320); once applied, `/health` returns 200.**

## Caddy auth-gate removal (#1320 — PM-decided 2026-07-01) — DROPLET ACTION

**Decision (PM, 2026-07-01):** remove the Caddy basic-auth gate. It is now **redundant friction** — the app has its own JWT auth (#358), the setup wizard is auth-exempt, and the exempt list is hardened + lint-guarded (#1308, `TestAuthExemptListIsASecurityBoundary`). The gate actively **breaks onboarding**: the pre-login, XHR-heavy setup flow triggers Caddy's `401 WWW-Authenticate: Basic` → the browser credential dialog loops (#1320 symptom, confirmed via chrome-devtools).

**Why it's safe to remove:** once the gate is gone, the exempt list *is* the entire attack surface (per #1308). It's read-only + justified-writes-only. The one #1320 repo change (auth-exempting the two read-only slack/calendar `app-credentials/status` GETs — booleans only, never secrets; write siblings stay auth-required) is already merged.

**Procedure (SSH to the droplet — NOT a repo change; `Caddyfile` is droplet-local at `/opt/piper/Caddyfile`):**
```bash
ssh root@piper-alpha                       # 146.190.151.63
cp /opt/piper/Caddyfile /opt/piper/Caddyfile.bak-1320   # back up first
# Edit /opt/piper/Caddyfile — delete the basic_auth block inside the
# `alpha.pipermorgan.ai { … }` site block, leaving just:
#   alpha.pipermorgan.ai {
#       reverse_proxy app:8001
#   }
docker exec piper-caddy caddy reload --config /etc/caddy/Caddyfile --adapter caddyfile \
  || docker compose -f /opt/piper/docker-compose.yml restart caddy
# Verify — was 401, now 200:
curl -s -o /dev/null -w "%{http_code}\n" https://alpha.pipermorgan.ai/health
```
Then confirm the onboarding flow (fresh incognito): the LLM-key validation no longer pops the basic-auth dialog. Update this runbook's "401 = gate" lines to "200" once applied.



## `deploy.sh` (the on-droplet script)

```bash
cd /opt/piper
rm -f BUILD_OK BUILD_FAIL
docker compose build app \
  && docker compose up -d postgres redis chromadb app \
  && sleep 30 \
  && docker compose ps \
  && docker compose exec -T app python -m alembic upgrade head \
  && touch BUILD_OK
[ -f BUILD_OK ] || touch BUILD_FAIL
# all output → /opt/piper/deploy.log
```

## ⚠️ Footgun: the migrate races app startup

The Jun-7 (0.8.7) deploy wrote `BUILD_FAIL` — but it was NOT a real failure: the `alembic upgrade` fired while `piper-app` was still `Restarting` (the 30s sleep wasn't long enough), the migrate errored with *"container is restarting"*, so the script marked FAIL. The app stabilized seconds later and ran healthy for 12 days. **Mitigation (the race only)**: if `BUILD_FAIL` is present after `deploy.sh`, confirm `docker compose ps` shows `app` healthy. **But do NOT just re-run `docker compose exec -T app python -m alembic upgrade head`** — that hits the deeper bug below and fails the same way.

## ⚠️⚠️ The deeper cause (#1299, found 2026-06-20): the migrate has NEVER actually run via deploy.sh

`alembic.ini:87` hardcodes `sqlalchemy.url = postgresql://piper:...@localhost:5433/piper_morgan` (a dev default), and `alembic/env.py:43` reads that static value verbatim. Inside the app container, postgres is at `postgres:5432`, NOT `localhost:5433` — so `docker compose exec app alembic upgrade head` connects to nothing and errors `connection refused`. **The migrate has silently failed on every deploy**; the DB only stayed usable because schema changes were rare. The 0.8.8 deploy exposed it — the droplet DB was **7 migrations behind** (the entire D1/RECONNECT schema: documents/#1238, owner_id/#1252, project_integrations/#1267, intents/workflows/tasks/stakeholders/#1273). The app was "healthy" (`/health` 200) but hollow.

**Correct mitigation — run the migrate with the app's REAL DB URL** (a temp script in the container that overrides alembic's url with the working engine URL).

> **⚠️ 2026-06-22 correction (verified on the 0.8.9 deploy).** The previous script (`from services.database.connection import engine`) is **stale**: connection.py exports a module-level `db = DatabaseConnection()` **singleton** (the engine is a class attribute, not a module export) → `ImportError`. The env-var fallback *also* fails on the droplet — `POSTGRES_PASSWORD` is **unset** (the app uses connection.py's default; the postgres password is compose-hardcoded `dev_changeme_in_production`), so an `os.environ`-built URL has an empty password → `fe_sendauth: no password supplied`. Use `db._build_database_url()` (the app's own URL logic + real creds), sync-ified for alembic's psycopg2:

```bash
cd /opt/piper
cat > _run_migrate.py <<'PY'
import os
os.chdir("/app")
from alembic.config import Config
from alembic import command
from services.database.connection import db      # module-level DatabaseConnection() singleton
raw = db._build_database_url()                    # postgresql+asyncpg://user:realpw@host:port/db[?ssl]
url = raw.replace("+asyncpg", "").split("?")[0]   # sync psycopg2 URL; drop async-only ssl query
cfg = Config("alembic.ini"); cfg.set_main_option("sqlalchemy.url", url)
command.upgrade(cfg, "head")
print("MIGRATE OK @", url.rsplit("@", 1)[-1])     # host:port/db only — never log creds
PY
docker compose cp _run_migrate.py app:/tmp/_run_migrate.py && docker compose exec -T app python /tmp/_run_migrate.py
rm -f _run_migrate.py
# verify the head + restart clean against the now-complete schema:
docker compose exec -T postgres psql -U piper -d piper_morgan -tAc "TABLE alembic_version"
docker compose restart app
```
The durable fix (make `alembic.ini` env-driven so deploy.sh's migrate just works) is tracked in **#1299 (a) + (b)**.

## ⚠️⚠️ Secrets/env vars must be NAMED in the app service (found 2026-06-22, the 0.8.9 deploy)

`/opt/piper/.env` is **not** auto-loaded into the app container. The `app` (and `orchestration`) compose services use an explicit `environment:` list, **not** `env_file:` — so only vars *named* in that list reach the container. A new secret placed in `.env` alone is invisible to the app. (And `docker compose restart` never re-reads env config — only `up -d` / recreate does.)

This bit the 0.8.9 deploy: `ENCRYPTION_MASTER_KEY` was correctly in `.env`, every structural check passed (version / migrate / schema / health / site), but `FieldEncryptionService.from_env()` returned `None` → encrypt-at-rest silently no-op'd. **The repo `docker-compose.yml` now names `ENCRYPTION_MASTER_KEY=${ENCRYPTION_MASTER_KEY:-}` in both `app` + `orchestration`** (commit on main 2026-06-22) — so a deploy from a `production` that carries that commit just works. **Until then**, the droplet is patched via `docker-compose.override.yml`:
```bash
# /opt/piper/docker-compose.override.yml — under `services:` add:
#   app:
#     environment:
#       - ENCRYPTION_MASTER_KEY=${ENCRYPTION_MASTER_KEY}
docker compose up -d app   # recreate (NOT restart) to pick up the new env
docker compose exec -T app printenv ENCRYPTION_MASTER_KEY >/dev/null && echo PRESENT || echo ABSENT  # verify w/o printing the value
```
**The rule**: any new secret the app needs must be *both* in `.env` *and* named in the app's `environment:` (repo compose, or the droplet override).

## The code-update step (the gap PA flagged)

`/opt/piper` is a copy, not a checkout, so "get new code in" is the one previously-undocumented step. The **`production` branch is the release surface and is public over plain https** (per `scripts/alpha-setup.sh`), so no droplet git credentials are needed.

**Primary method — `git archive` over ssh (code-only, leaves no `.git` on the droplet):**
```bash
# from a local clone, with origin/production fetched:
git fetch origin production
git archive origin/production | ssh root@alpha.pipermorgan.ai 'tar -x -C /opt/piper'
```
This overwrites tracked files with `production`'s versions and leaves untracked droplet-local files — but ALWAYS back up `.env` / `Caddyfile` / `docker-compose.override.yml` first (step 2 below) in case the repo tracks any of them.

**Alt method — convert to a git checkout** (future deploys become `git pull`): `git init` in `/opt/piper`, `git remote add origin https://github.com/mediajunkie/piper-morgan-product.git`, `git fetch origin production`, `git checkout -f production`. Heavier; only if we want in-place git on the droplet.

## Full safe deploy procedure

On the droplet — backup + rollback safety:
```bash
ssh root@alpha.pipermorgan.ai
B=/root/alpha-deploy-backup-$(date +%Y%m%d-%H%M); mkdir -p "$B"
cp /opt/piper/.env "$B/"; cp /opt/piper/Caddyfile "$B/" 2>/dev/null; cp /opt/piper/docker-compose.override.yml "$B/" 2>/dev/null
docker tag piper-morgan-stable-app piper-morgan-stable-app:rollback-$(date +%Y%m%d)   # keep the working image
tar czf "$B/opt-piper-code.tar.gz" -C /opt/piper --exclude='.env' .                   # snapshot current code
echo "backup at $B"
```
From a local clone — push the new code:
```bash
git fetch origin production
git archive origin/production | ssh root@alpha.pipermorgan.ai 'tar -x -C /opt/piper'
```
Back on the droplet — restore config, deploy, verify:
```bash
cp "$B/.env" /opt/piper/.env; [ -f "$B/Caddyfile" ] && cp "$B/Caddyfile" /opt/piper/Caddyfile; [ -f "$B/docker-compose.override.yml" ] && cp "$B/docker-compose.override.yml" /opt/piper/
cd /opt/piper && ./deploy.sh
cat BUILD_OK 2>/dev/null && echo "BUILD_OK" || tail -20 deploy.log
docker compose ps                                              # app healthy?
docker exec piper-app grep -m1 '^version' /app/pyproject.toml  # = target version?
curl -s -o /dev/null -w 'site → %{http_code}\n' https://alpha.pipermorgan.ai/   # 200/302/401 (gate), not 5xx
# feature smoke — encrypt-at-rest actually works (structural-green != feature-working; this caught the 0.8.9 key gap):
cat > _verify_enc.py <<'PY'
import os; os.chdir("/app")
from services.security.field_encryption import FieldEncryptionService
svc = FieldEncryptionService.from_env(); assert svc, "no ENCRYPTION_MASTER_KEY in app env"
assert svc.decrypt(svc.encrypt("x", "smoke"), "smoke") == "x", "round-trip mismatch"
print("ENCRYPTION ROUND-TRIP OK")
PY
docker compose cp _verify_enc.py app:/tmp/_verify_enc.py && docker compose exec -T app python /tmp/_verify_enc.py; rm -f _verify_enc.py
```
**If `BUILD_FAIL`:** apply the footgun mitigation (re-run the migrate once `app` is healthy).
**Rollback if broken:** `tar xzf "$B/opt-piper-code.tar.gz" -C /opt/piper` → retag the `rollback-*` image back to `piper-morgan-stable-app` → `docker compose up -d app`.

## Future / beta

This is the *alpha* — a single droplet, manual deploy. The *beta* hosted backend moves to **Fly.io** (`server.pipermorgan.ai`, #1278) with the `InboundAuth` per-request-token pattern from PR #154 — gated on the Caddy gate-removal decision (Arch/LD) + #1162 (cred-decoupling). Full context: `piper-morgan-skunkworks/byoc/notes/piper-morgan-hosted-distribution-guide-2026-06-19.md`.

`beta.pipermorgan.ai` is not yet set up; it will follow the Fly.io path, not this droplet pattern.

## See Also

- [Release Runbook](release-runbook.md) — full release process (version bump, git ops, GitHub release)
- [CI/CD Smoke Test Runbook](ci-cd-smoke-test-runbook.md) — quality gate before release
- [Release Notes v0.8.9](../../releases/RELEASE-NOTES-v0.8.9.md) — current production release
- `memo-pa-to-lead-cc-pm-alpha-deploy-runbook-gap-2026-06-19` — the gap report this runbook closes
