# Alpha Deployment Runbook

**Status**: COMPLETE — mechanism reverse-engineered from the live droplet by Lead Dev, 2026-06-19 (was a STUB; PA flagged the gap in `memo-pa-to-lead-cc-pm-alpha-deploy-runbook-gap-2026-06-19`).
**Created**: June 19, 2026 (PA)
**Last Updated**: June 19, 2026 (Lead Dev — full mechanism + safe procedure)

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
5. **Health URL?** `https://alpha.pipermorgan.ai/health` (401 = the Caddy auth gate; the app's own `/health` answers on `app:8001` inside the docker network).

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

The Jun-7 (0.8.7) deploy wrote `BUILD_FAIL` — but it was NOT a real failure: the `alembic upgrade` fired while `piper-app` was still `Restarting` (the 30s sleep wasn't long enough), the migrate errored with *"container is restarting"*, so the script marked FAIL. The app stabilized seconds later and ran healthy for 12 days. **Mitigation**: if `BUILD_FAIL` is present after `deploy.sh`, confirm `docker compose ps` shows `app` healthy, then re-run the migrate by hand: `docker compose exec -T app python -m alembic upgrade head`.

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
curl -s -o /dev/null -w 'site → %{http_code}\n' https://alpha.pipermorgan.ai/   # 200/302, not 5xx
```
**If `BUILD_FAIL`:** apply the footgun mitigation (re-run the migrate once `app` is healthy).
**Rollback if broken:** `tar xzf "$B/opt-piper-code.tar.gz" -C /opt/piper` → retag the `rollback-*` image back to `piper-morgan-stable-app` → `docker compose up -d app`.

## Future / beta

This is the *alpha* — a single droplet, manual deploy. The *beta* hosted backend moves to **Fly.io** (`server.pipermorgan.ai`, #1278) with the `InboundAuth` per-request-token pattern from PR #154 — gated on the Caddy gate-removal decision (Arch/LD) + #1162 (cred-decoupling). Full context: `piper-morgan-skunkworks/byoc/notes/piper-morgan-hosted-distribution-guide-2026-06-19.md`.

`beta.pipermorgan.ai` is not yet set up; it will follow the Fly.io path, not this droplet pattern.

## See Also

- [Release Runbook](release-runbook.md) — full release process (version bump, git ops, GitHub release)
- [CI/CD Smoke Test Runbook](ci-cd-smoke-test-runbook.md) — quality gate before release
- [Release Notes v0.8.8](../../releases/RELEASE-NOTES-v0.8.8.md) — current production release
- `memo-pa-to-lead-cc-pm-alpha-deploy-runbook-gap-2026-06-19` — the gap report this runbook closes
