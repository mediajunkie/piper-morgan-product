# piper-morgan-staging on Fly — setup sheet (step 2 onward)

Second Fly app approved by PM 09-22. Purpose: the place beta-blocker fixes run before they reach
the alpha build on `piper-morgan` (environment = staging; alpha/beta are access *stages* of prod).
Executor: PM's hands (Pard's seat has no Fly write grant since path A was revoked 13:38). Pard
verifies each READ line from the read side.

## Done (PM, 09-22 ~15:00) — verified by Pard from `fly` reads

- `fly apps create piper-morgan-staging` → exists, hostname `piper-morgan-staging.fly.dev`, no image yet
- `fly postgres create` → `piper-morgan-staging-db` exists
- `fly postgres attach` → `DATABASE_URL` is a **Staged** secret on the app; DB user
  `piper_morgan_staging` owns database `piper_morgan_staging`

## As executed 09-23 ~12:5x (PM's hands; Pard verified by reads)

Paste 1 was interrupted with Ctrl+C at the Redis eviction prompt, which aborted `fly redis create`
only; the rest of the paste ran. State read at 13:0x: **no staging Redis**; `piper_data`
(vol_4qlkj0je6knxwq6r, 1 GB, sjc) created once; `piper-morgan-staging-chroma` created, `chroma_data`
(vol_vxm0y6yz73nd17j4) created once, `chromadb/chroma:latest` deployed, machine 781e027ae44368
started; no public IPs on the Chroma app (the "allocate dedicated ipv4/ipv6?" prompt defaulted to
N — correct, it's an internal sidecar like prod's). Nothing duplicated, nothing to repair.
Remaining from paste 1: only `fly redis create --name piper-morgan-staging-redis --region sjc
--no-replicas`, answering **N** at the eviction prompt (matches prod; the token blacklist is a
cache where eviction could drop a revoked token).

## Step 2 — Redis, volume, Chroma, secrets, first deploy

Run from `~/Development/piper-morgan-product` on `main`, clean and current
(`git pull --ff-only origin main`). Secret VALUES are typed by the executor and never pasted into a
repo, mailbox, or chat.

```sh
# 2a. Redis — staging gets its own (prod's is piper-morgan-redis; sharing would mix key spaces)
fly redis create --name piper-morgan-staging-redis --region sjc --no-replicas
#     pick the smallest pay-as-you-go plan at the prompt; when it finishes it prints
#     "Private URL: redis://…" — copy that whole line's URL for 2d.
fly redis status piper-morgan-staging-redis            # READ: shows the same Private URL again if you lost it

# 2b. Upload volume — fly.toml [mounts] expects a volume named piper_data at /data
fly volumes create piper_data -a piper-morgan-staging -r sjc -s 1 -y
fly volumes list -a piper-morgan-staging               # READ: one volume, piper_data, 1GB, sjc

# 2c. Chroma — its own app, from the same file prod's Chroma was deployed from
#     (deploy/fly/chroma.fly.toml; -a overrides the app name inside it)
fly apps create piper-morgan-staging-chroma
fly volumes create chroma_data -a piper-morgan-staging-chroma -r sjc -s 1 -y
fly deploy -a piper-morgan-staging-chroma -c deploy/fly/chroma.fly.toml --remote-only
fly status -a piper-morgan-staging-chroma              # READ: one machine, started

# 2d. Secrets — nothing is copied from prod; staging gets its own values
#     (an empty DB has nothing encrypted, so a fresh master key is correct here)
fly secrets set -a piper-morgan-staging --stage \
  JWT_SECRET_KEY="$(openssl rand -hex 32)" \
  ENCRYPTION_MASTER_KEY="$(openssl rand -hex 32)" \
  PIPER_BASE_URL="https://piper-morgan-staging.fly.dev" \
  GITHUB_OAUTH_REDIRECT_URI="https://piper-morgan-staging.fly.dev/api/v1/settings/integrations/github/callback" \
  REDIS_URL="<Private URL from 2a>"
#     ANTHROPIC_API_KEY: read it from wherever prod's was set from and type it at the prompt —
fly secrets set -a piper-morgan-staging --stage ANTHROPIC_API_KEY="<value>"
#     GitHub OAuth: reuse the "Piper Morgan Beta" app (client Ov23liAfOzFyktgzdgot — it is free since
#     alpha moved to the Alpha app at 9b). In that app's settings, ADD the staging callback above as
#     an additional Authorization callback URL (up to 10 allowed), then:
fly secrets set -a piper-morgan-staging --stage \
  GITHUB_OAUTH_CLIENT_ID="Ov23liAfOzFyktgzdgot" \
  GITHUB_OAUTH_CLIENT_SECRET="<the Beta app's client secret — Generate a new one if it isn't stored>"
fly secrets list -a piper-morgan-staging               # READ: names only — DATABASE_URL, JWT_SECRET_KEY,
#                                                        ENCRYPTION_MASTER_KEY, PIPER_BASE_URL, GITHUB_OAUTH_*,
#                                                        REDIS_URL, ANTHROPIC_API_KEY, all "Staged"

# 2e. First deploy — same fly.toml as prod (so PIPER_ENVIRONMENT stays "production": the JWT and
#     encryption gates ARM on that exact string, which is what we want on staging too). Two things
#     are overridden on the command line: the app, and CHROMA_HOST (fly.toml's value is prod's Chroma).
fly deploy -a piper-morgan-staging --remote-only \
  -e CHROMA_HOST=piper-morgan-staging-chroma.internal \
  --build-arg PIPER_GIT_SHA="$(git rev-parse HEAD)"
#     the release_command runs `alembic upgrade head` against the staging DB before the app starts
curl -s https://piper-morgan-staging.fly.dev/health | head -c 400   # READ: healthy, version + the sha you just built
curl -sL -o /dev/null -w "%{url_effective} %{http_code}\n" https://piper-morgan-staging.fly.dev/   # READ: login page, 200
```

## Not done in step 2 (Lead's calls)

- The three feature-flag secrets on prod (`PIPER_INVERSION_LIVE_CATEGORIES`, `PIPER_INVERSION_SHADOW`,
  `PIPER_FTUX_INTERVIEW`) and the Slack/Google redirect URIs: values are not readable from Fly;
  Lead knows what prod runs and sets staging to match (or leaves defaults) — `fly secrets set` as in 2d.
- `PIPER_SLACK_INBOUND_ENABLED`: leave unset on staging unless a Slack test needs it.
- A `fly.staging.toml` committed to the repo would remove the two `-e`/`-a` overrides above; that
  is a code change and Lead's, tracked with the CI-deploy work (§4e).
- Test users: staging's DB is empty. Register through the staging login, or have Lead seed an invite.

## Traps learned on the alpha cutover that apply here

- `fly deploy` without `--build-arg PIPER_GIT_SHA` makes `/health` report `git_sha: unknown`.
- Non-interactive restarts need the machine id: `fly machines list -a piper-morgan-staging --json`.
- A near-miss in `PIPER_ENVIRONMENT` (e.g. "staging") silently DISARMS the production gates — that
  is why the sheet keeps the prod fly.toml value.
