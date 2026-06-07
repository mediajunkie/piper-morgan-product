# Runbook — Piper hosted alpha (#1162)

**Goal**: stand up a password-protected hosted Piper backend (from the `production` / v0.8.7 build) so an
outside alpha tester (Beatrice) runs only the thin plugin — no local Piper stack. Host-agnostic: works on
your Rackspace box, a Hetzner/DO droplet, or any Docker-capable Linux host (~8GB RAM, 2 vCPU, ~20GB disk).

**Verified against the repo 2026-06-06** (PA). Markers: ✅ verified · ⚠️ confirm-on-the-box · 🔒 security.
This is a working runbook; graduate to `docs/internal/operations/` once a first run proves it.

---

## Prerequisites

- A Docker + docker-compose host you can reach (Rackspace VM / Hetzner / DO). ~8GB RAM (torch +
  sentence-transformers + ChromaDB + Temporal are the heavy tenants). ✅ stack confirmed: app +
  orchestration(Temporal worker) + postgres:15 + redis:7 + chromadb + temporal + traefik.
- An **Anthropic API key** for the server (server-side only — 🔒 never in the plugin zip).
- A way to expose it with TLS + an access gate (Cloudflare Tunnel/Access, Tailscale, or a reverse proxy
  with basic-auth). Decide auth approach in Phase 2.
- The tester's OS for the uv bundle (Beatrice = Mac, confirm arm64 vs intel).

---

## Phase 1 — Deploy the backend

```bash
# 1. Get the stable build (NOT main — production is the regression-passing v0.8.7 cut)
git clone git@github.com:mediajunkie/piper-morgan-product.git piper
cd piper && git checkout production          # HEAD self-reports 0.8.7

# 2. Create .env from the example
cp .env.example .env
```

**Edit `.env`** — the load-bearing values (✅ confirmed against `services/config/llm_config_service.py`
and `.env.example`):

- `ANTHROPIC_API_KEY=sk-ant-...`  ⚠️ **not in `.env.example` but REQUIRED** — the LLM client reads it via
  `os.getenv("ANTHROPIC_API_KEY")` (env-first; macOS keychain is only a local fallback, so a Linux host
  works fine with this set). Add it. (Filed thought: add it to `.env.example`.)
- `POSTGRES_PASSWORD=` → a real secret (the default literally says `dev_changeme_in_production`). 🔒
- ⚠️ **Service hosts inside the compose network are SERVICE NAMES, not `localhost`** — the example uses
  `localhost` (for running `main.py` directly on the host). When the app runs *in* the compose `app`
  container, set:
  - `POSTGRES_HOST=postgres`, `REDIS_HOST=redis`, `CHROMA_HOST=chromadb`, `TEMPORAL_HOST=temporal`
  (ports stay 5432/6379/8000/7233 internally). Confirm on the box; this is the #1 deploy gotcha.
- `APP_DEBUG=false`, `LOG_LEVEL=INFO` (🔒 don't run a public instance with debug on).
- `AUTH_ENABLED` — see Phase 2. For a network-gated alpha, leaving the app's own auth `false` and relying
  on the gate is simplest. ⚠️ If you set the app to a *production* env with auth on, `JWT_SECRET_KEY` must
  be set or the app fails loud (by design — #1087). Pick one model, don't half-configure.

```bash
# 3. Bring up the stack
docker compose up -d

# 4. Run migrations (M1+M2 migrations: user-history #1021, audit durability #1018, privacy #1089, ...)
docker compose exec app python -m alembic upgrade head

# 5. Verify locally on the box (before exposing it)
curl -s localhost:8001/health                     # ops health (web/middleware/staging_health.py)
curl -s -X POST localhost:8001/api/v1/intent \
  -H 'content-type: application/json' \
  -d '{"message":"what should I focus on today?"}'   # should return JSON (intent + floor response)
```

**Gate**: don't proceed until `/api/v1/intent` returns a real JSON answer on the box. If it errors,
that's a deploy problem to fix here, not after exposing it.

---

## Phase 2 — Expose + secure  🔒

**TLS + reachability.** Front the app (port 8001) with HTTPS. The stack already includes **Traefik**; or
put Cloudflare/Caddy/nginx in front. Map a subdomain, e.g. `piper-alpha.<yourdomain>`.

**Access gate — pick one:**

- **Option A — network-layer gate (recommended for one tester, zero plugin code change).** Cloudflare
  Access (email-allowlist / one-time-PIN) or Tailscale (tester joins your tailnet). The plugin's MCP
  server just hits the URL; the gate handles auth out-of-band. 🔒 The Anthropic key never leaves the
  server and no secret rides in the plugin.
- **Option B — shared bearer token.** Simpler infra, but ⚠️ **needs a small plugin change**: `ask_piper`
  in `mcp/server.py` currently sends no auth header. Add `PIPER_API_TOKEN = os.environ.get(...)` and
  attach `Authorization: Bearer` to the httpx call; the hosted app validates it. ~15 min. The token then
  lives in the alpha build's `.mcp.json` env (acceptable for a trusted tester, but it *is* a secret in
  the zip — Option A avoids that).

**Rate-limit** 🔒 — cap requests so testers' usage can't run up our Anthropic spend (Traefik rate-limit
middleware, or Cloudflare). Set a sane per-minute/day ceiling for the alpha.

**Gate**: from a machine *outside* the box, confirm the URL requires the gate and, once past it, the
`/api/v1/intent` curl works over HTTPS.

---

## Phase 3 — Build the tester plugin

The plugin already supports a remote backend — ✅ `mcp/server.py` reads `PIPER_BASE_URL`
(default `http://localhost:8001`). So:

```bash
# In the skunkworks plugin source: byoc/poc/dinp/piper-morgan/
# 1. Point .mcp.json at the hosted backend (env var, no code change):
#    "mcpServers": { "piper-morgan": { "command": "uv",
#      "args": ["run", "${CLAUDE_PLUGIN_ROOT}/mcp/server.py"],
#      "env": { "PIPER_BASE_URL": "https://piper-alpha.<yourdomain>" } } }
#    (+ "PIPER_API_TOKEN": "<token>" if you chose Option B)

# 2. Bundle uv for the tester's platform (Mac arm64): drop the uv binary in mcp/bin/uv and
#    point .mcp.json command at "${CLAUDE_PLUGIN_ROOT}/mcp/bin/uv" so she needn't install uv.

# 3. Build + validate the zip (keep plugin.json description <~480 chars — Desktop cap)
cd byoc/poc/dinp && zip -rq ../../dist/piper-morgan-alpha-beatrice.zip piper-morgan \
  -x '*.DS_Store' -x '*__pycache__*'
claude plugin tag byoc/poc/dinp/piper-morgan        # source validates clean
```

**Gate**: install the zip in *your* Claude Desktop, run `/meet-piper` (writes local config) then
`/ask-piper` — confirm `ask` reaches the hosted backend (not localhost). That proves the whole loop
before Beatrice touches it.

---

## Phase 4 — Onboard Beatrice

Send her: the zip + the access credential (Cloudflare invite / Tailscale / token) + a 5-line quickstart:
install the zip in Claude Desktop → `/meet-piper` (one-time ~10-min calibration, stays on her machine) →
`/ask-piper` and `/consult-piper`. Note honestly: it's an alpha; `meet-piper` is fully local, `ask`/`consult`
talk to the hosted Piper. (Known M2 edges are in `RELEASE-NOTES-v0.8.7.md` "Known limitations".)

---

## End-to-end smoke checklist

- [ ] `/health` 200 on the box
- [ ] `/api/v1/intent` returns JSON on the box
- [ ] URL gated from outside; works once past the gate over HTTPS
- [ ] rate-limit active
- [ ] plugin `/meet-piper` completes (local config written)
- [ ] plugin `/ask-piper` answer comes from the hosted backend
- [ ] 🔒 no Anthropic key anywhere in the plugin zip; `.env` only on the server

---

## 🔒 Security guardrails (non-negotiable)

- Anthropic API key lives **only** server-side in `.env`. Never in the plugin zip. (OpenLaws precedent: a
  live key shipped to evaluators in a zip — do not repeat.)
- Real `POSTGRES_PASSWORD` / `JWT_SECRET_KEY`; never the `_changeme_` defaults on a public box.
- `APP_DEBUG=false`. Gate the endpoint. Rate-limit. Watch API spend during the alpha.

---

## Rollback / teardown

- Stop: `docker compose down` (keep volumes) / `docker compose down -v` (wipe data).
- Revoke tester access at the gate; rotate the token/key if Option B was used.
- The plugin needs no teardown — testers just stop using it (their local config persists harmlessly).

---

## Cost & monitoring

- ~$0 if Rackspace (already running); ~$20–40/mo for a Hetzner/DO VM of the right size. Plus Anthropic API
  usage = our spend during the our-key alpha (rate-limit bounds it). **BYO-key** (roadmap) removes that.
- Watch: Anthropic usage dashboard, the box's RAM (torch/Temporal are the tenants), rate-limit hits.

---

## Open decisions still needed from PM

1. **Host**: Rackspace (if ~8GB free + Docker) vs a Hetzner/DO droplet.
2. **Auth**: Option A network-gate (recommended, no plugin change) vs Option B bearer token.
3. **Beatrice's OS/arch** for the uv bundle.

## Feeds / related
- #1162 (hosted distribution) · scope: `dev/active/pa-byoc-hosted-distribution-exploration-2026-06-06.md`,
  `dev/active/pa-byoc-hosted-alpha-scope-2026-06-06.md`
- Build source: `production` branch (v0.8.7) · `docs/releases/RELEASE-NOTES-v0.8.7.md`
- Plugin: `RELEASE-NOTES`/architecture lessons in skunkworks `byoc/`
