# Alpha → Fly cutover runbook — window APPROVED for Tue 2026-09-22 AM (PM, 09-21 evening)

Executes Arch's droplet-completion-path plan v0.2 §4b with Lead's verified correction (the droplet
DB is the source of truth — 6 users, live invite token — not "probably near-empty"). Authority:
decisions.log 2026-07-10 + 2026-09-21 entries. **Whether is closed; this doc is the when/how.**

## Measured payload (Lead, live on droplet 09-21 ~19:25 PT — "Verified how" is each command below)

| What | Size | Command that measured it |
|---|---|---|
| Postgres dump (`piper_morgan`, user `piper`) | **222 KB** | `docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" \| wc -c'` → 227551 |
| `uploads/` bind mount | **912 KB** | `du -sh uploads` |
| `data/chromadb` | **13 MB** | `du -sh data/chromadb` |
| `data/redis` | **88 KB** | `du -sh data/redis` |
| `ENCRYPTION_MASTER_KEY` in droplet `.env` | present (grep -c = 1) | value never printed, never transits a mailbox |

Everything moves in **< 15 MB**. The write-freeze need only cover dump→restore→DNS — minutes, not
hours.

## Roles

- **Lead**: droplet-side (freeze, dump, tars), verification, docs/decommission steps. Lead's seat
  is **classifier-denied for Fly writes** — never the Fly executor.
- **Pard** (leads the sort): Fly-side — deploy, secrets, restore, volume copies. Relay to Themis.
  **⚠ GATING, found 09-21 21:2x (Pard, amending):** Pard's seat is classifier-gated for this
  role as written — `fly deploy -a piper-morgan --remote-only` refused "[Production Deploy]", a
  read-only `ssh root@146.190.151.63` probe refused "[Production Reads]". Read-only Fly reads pass.
  So steps 1, 2 (droplet read + `secrets set`), 4's scp pull, 5, 6, 7 need EITHER **(A)** Bash
  allow rules on Pard's seat for the specific commands (`fly deploy`, `fly secrets set`,
  `fly proxy`, `fly volumes snapshots create`, `fly ssh console`, `ssh root@146.190.151.63 …`)
  set by PM before the window — then this runbook runs as written, Pard driving — OR **(B)** PM
  keystrokes for those steps with Pard preparing each command verbatim and verifying from the
  read side. PM decides; notice sent to Lead cc Exec/HOST/Arch/PM 09-21 21:3x.
  **Read-side facts gathered 09-21 (Fly, read-only):** `ENCRYPTION_MASTER_KEY` already EXISTS as a
  Fly secret name — whether its value equals the droplet's is UNVERIFIED and decides step 2's
  shape (equal → step 2 is only the remaining-names diff; unequal → set before restore or the
  encrypted columns come back unreadable); volumes `piper_data` (app, 1 GB) and `chroma_data`
  (chroma app, 1 GB) exist; `piper-morgan-db`'s volume has daily snapshots (5-day retention,
  newest 3 days old) — step 3's floor before any manual snapshot.
- **PM**: DNS cut + GitHub OAuth callback addition (PM-owned per the 07-10 entry) + any Fly
  keystroke Pard prefers PM to make — **and, per the gating note above, either the allow rules
  or the Fly-side keystrokes themselves.**
- **HOST**: pre-step roster check (step 0).
- **Arch**: eyes on the `mcp_server_ref` repoint (step 8).

## Sequence

**0. HOST — roster-check Fly's 4 stale accounts** (frozen since 2026-07-13) before they're
overwritten. Identity layer is HOST's; default is replace-all, HOST says if any needs preserving.
*Status 09-22 06:5x (Lead → HOST, Pard recording): the identifier pull is classifier-denied on
Lead's seat too (`fly ssh console`, [Production Reads]). Proposed and unobjected as of 07:1x:
**step 0 is satisfied-by-snapshot** — step 3's manual snapshot preserves all four accounts
completely and post-hoc retrievably, so replace-all loses nothing irrecoverable; the unblocked
executor runs HOST's pull at window-open as a courtesy (blind, to a chmod-600 file HOST reads),
not as a gate. Step 0 does not block the window unless HOST or PM objects.*

**1. Pard — deploy current `origin/main` to the `piper-morgan` Fly app.** It runs a pre-0.8.13
build (deployed 09-19). Current main = v0.8.13.0 + five post-release closures (#1823/#1824,
#1808, #1778 family, #1794). Verify: `curl https://piper-morgan.fly.dev/health` shows the current
version + sha (deploy-identity shipped in v0.8.13.0).

**2. Executor — set the master key BEFORE any restore** (encrypted columns are unreadable without
it). **Amended by Lead 09-21 ~21:5x, superseding the equality question in the gating note: do NOT
try to verify whether Fly's existing `ENCRYPTION_MASTER_KEY` equals the droplet's — ALWAYS set it
from the droplet value.** Setting a secret to a value it already has is harmless (worst case a
redundant machine restart, which step 7 does anyway); the comparison needs a seat that can read
both, which tonight nobody cleanly has, and Fly's digest isn't a reproducible hash to compare
against. The executor (Pard-under-allow-rules per path A, else PM) reads the value from droplet
`/opt/piper/.env` and runs `fly secrets set ENCRYPTION_MASTER_KEY=… -a piper-morgan`. The value
never transits a mailbox, repo file, or chat. Also reconcile any other `.env` secrets the Fly app
lacks — diff `.env` var NAMES against `fly secrets list` output (names only, values direct).

**3. Pard — snapshot Fly's current DB first** (it contains the dead exposed token ZVHW…8B35 and
the 4 July accounts; a snapshot is not live, that's fine): Fly Postgres daily snapshots exist —
take a manual one or `pg_dump` via `fly proxy 15432:5432 -a piper-morgan-db`.

**4. Lead — freeze + dump on droplet**: announce, then
`cd /opt/piper && docker compose stop app` (alpha briefly down — the honest freeze), then
`docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > /root/piper_morgan-20260922.sql`
and `tar czf /root/uploads-20260922.tgz uploads` + `tar czf /root/chromadb-20260922.tgz data/chromadb`.
**Transfer (amended by Lead 09-21 — Pard's seat cannot scp from the droplet, mine can): Lead pulls
all three artifacts to Amber at `~/migration-staging-20260922/` (OUTSIDE any repo — the dump holds
user data; `chmod 700` the dir), and the restore in step 5 runs from Amber where the files sit.**

**5. Pard — restore into `piper-morgan-db`**: via `fly proxy`, drop/recreate the app schema (or
the database) and `psql < piper_morgan-20260922.sql`. **This restore also completes the #1845
Fly-side burn** — the dead token row does not survive it. Verify: user count = droplet's count at
freeze (6 + anyone who registered since; Janne rides the dump whenever he registers), and the live
invite token row (masked NCBN…65FH) present iff still unused.

**6. Pard — uploads + chroma onto Fly volumes**: untar `uploads` into the app volume path the Fly
app serves — **`/data/uploads`** (corrected 09-22 from `/app/uploads` by reading `fly.toml`:
volume `piper_data` mounts at `/data`, `UPLOAD_DIR = "/data/uploads"`); untar chromadb into the
`piper-morgan-chroma` app's volume at **`/chroma/chroma`** (`deploy/fly/chroma.fly.toml`). At 13 MB,
carrying Chroma beats rebuilding embeddings. **Redis: nothing to migrate** — the token blacklist
is a DB-seeded write-through cache since #1808 (DB is the record; cold Redis self-seeds at
startup). Denominator caveat: that's the one Redis surface Lead verified; Pard should eyeball
`data/redis` keyspace for anything durable-only before discarding.

**7. App restart on Fly** (release/machines restart) so it reads the restored DB + secrets.

**8. Arch/Pard — `mcp_server_ref` repoint** (plan §4d's named landmine): ADR-070 Amendment A made
bindings logical-key-based, so this *should* be config-only — verify against the restored data,
don't assume. *MEASURED 09-22 06:5x (Lead, on the droplet, pre-freeze): Arch's query for
calendar/notion/slack literal rows → **0 rows**; the whole `connector_bindings` table is **one
github row**. Step 8 is config-only with a measured yes behind it. Lead re-runs at freeze time if
the count grows. Post-restore check (executor): the same query against Fly's restored DB returns
0 rows and 1 github binding — same numbers, or stop.*

**9. PM — the cut**: `fly certs add alpha.pipermorgan.ai -a piper-morgan` (TLS moves off the
droplet's Caddy — do this before DNS so the cert is ready), then point `alpha.pipermorgan.ai`
DNS (CNAME → `piper-morgan.fly.dev`), then add the Fly callback URL to the GitHub OAuth app.
DNS revert is the rollback lever throughout.
**9b (added 09-22 09:4x, Lead — found via `fly secrets list`): the URL-bearing secrets must move
to the alpha.pipermorgan.ai values with the cut** — `PIPER_BASE_URL`,
`GITHUB_OAUTH_REDIRECT_URI`, `SLACK_SETTINGS_REDIRECT_URI`, `SLACK_REDIRECT_URI`,
`GOOGLE_SETTINGS_REDIRECT_URI` all exist as Fly secrets and currently carry whatever the
Fly-standalone era set (values unreadable, presumed fly.dev-based). Executor sets them from the
droplet `.env`'s alpha.pipermorgan.ai values at step 9 time (a secrets set triggers a restart —
fine, pairs with the cut). Skipping this leaves OAuth callbacks + generated links pointing at
fly.dev after the domain moves.

**10. Verify on the real domain** (Lead + PM): `/health` identity on `alpha.pipermorgan.ai`
shows the Fly deploy's sha; PM logs in as a real user; run the pm-test-card retests (#1617,
#1824) — they double as the §4b step-4 watched-real-user verification. Tester-facing docs need
**zero changes** — they already say alpha.pipermorgan.ai, which is the point of cutting DNS.

**11. Aftermath (Lead)**: droplet stays warm ~1 week as rollback (`docker compose start app` +
DNS revert = full rollback). Then: decommission the droplet (spend stops), retire the `production`
branch (§4b step 6 — cut-release skill Phase 5 updates with it), sweep docs that name the droplet
(`grep -ril "droplet\|146.190.151.63" docs/`), update BRIEFING-CURRENT-STATE + decisions.log with
the completion date.

## Rollback at any step before 9: nothing user-facing changed (droplet untouched except a brief
app stop). After step 9: revert DNS, restart droplet app; the restored Fly DB may then be ahead
by any registrations that landed on Fly — check before discarding either side.

## Appendix — Executor command sheet (Pard, 09-22 07:2x; paths read from fly.toml, not assumed)

Runs from `~/Development/piper-morgan-product` on Amber, checkout clean at `origin/main`. Same
sheet whether the hands are Pard's (path A) or PM's (path B). Every step ends with a READ that
proves it; never proceed on an exit code. Secret VALUES are typed by the executor, never pasted
into a repo, mailbox, or chat.

```sh
# 1. deploy current main  (verify: /health identity shows the new sha + version)
git pull --rebase -q origin main && git status -sb | head -1   # expect: ## main...origin/main (no ahead/behind) — fly deploy builds the LOCAL tree
fly deploy -a piper-morgan --remote-only --build-arg PIPER_GIT_SHA="$(git rev-parse HEAD)"   # the Dockerfile ARG that /health's git_sha reads; without it /health says "unknown" (learned 09-22 v117)
curl -s https://piper-morgan.fly.dev/health | head -c 400   # READ: version/sha of the deploy just made
fly releases -a piper-morgan | head -3                       # READ: new vN "complete"

# 2. master key + secret-name reconcile  (value read by whoever holds droplet access; typed here)
fly secrets list -a piper-morgan | awk 'NR>1{print $1}' | sort > /tmp/fly-secret-names.txt
#    droplet side (Lead): grep -oE '^[A-Z_]+=' /opt/piper/.env | tr -d = | sort   → compare names by eye
fly secrets set ENCRYPTION_MASTER_KEY='<value from droplet .env>' -a piper-morgan   # ALWAYS set (Lead's amendment)
fly secrets list -a piper-morgan | grep -c ENCRYPTION_MASTER_KEY                     # READ: 1, digest changed if value did

# 3. snapshot Fly's DB before restore  (volume-level; daily ones exist, take a manual one now)
fly volumes list -a piper-morgan-db                          # READ: the volume id
fly volumes snapshots create <vol-id> -a piper-morgan-db
fly volumes snapshots list <vol-id> -a piper-morgan-db | head -3   # READ: newest = just now

# 4. (Lead) freeze + dump on droplet → ~/migration-staging-20260922/ on Amber, chmod 700
ls -la ~/migration-staging-20260922/                         # READ: piper_morgan-20260922.sql, uploads-*.tgz, chromadb-*.tgz

# 5. restore into piper-morgan-db  (proxy in one shell, psql in another)
fly proxy 15432:5432 -a piper-morgan-db                      # leave running
#    DATABASE_URL: fly ssh console -a piper-morgan -C 'printenv DATABASE_URL'  → user/pw/dbname (executor's eyes only)
psql "postgres://<user>:<pw>@localhost:15432/<db>" -c '\dt' | head           # READ: current schema present
psql "postgres://<user>:<pw>@localhost:15432/<db>" -c 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;'
psql "postgres://<user>:<pw>@localhost:15432/<db>" < ~/migration-staging-20260922/piper_morgan-20260922.sql
psql "postgres://…" -c 'SELECT count(*) FROM users;'         # READ: = droplet count at freeze (6 + any since)
psql "postgres://…" -c "SELECT connector, count(*) FROM connector_bindings GROUP BY 1;"   # READ: github 1 (step 8 check)
psql "postgres://…" -c "SELECT count(*) FROM connector_bindings WHERE connector!='github' AND mcp_server_ref LIKE 'http%';"  # READ: 0

# 6. uploads + chroma onto the volumes  (paths from fly.toml: /data/uploads ; /chroma/chroma)
fly ssh sftp shell -a piper-morgan          # put ~/migration-staging-20260922/uploads-20260922.tgz /data/
fly ssh console -a piper-morgan -C 'sh -c "cd /data && tar xzf uploads-20260922.tgz && ls /data/uploads | wc -l && rm uploads-20260922.tgz"'   # READ: file count
fly ssh sftp shell -a piper-morgan-chroma   # put ~/migration-staging-20260922/chromadb-20260922.tgz /chroma/
fly ssh console -a piper-morgan-chroma -C 'sh -c "cd /chroma && tar xzf chromadb-20260922.tgz && du -sh /chroma/chroma && rm chromadb-20260922.tgz"'   # READ: ~13M
#    the chroma tar unpacks as data/chromadb/… — if so, move its contents into /chroma/chroma (check with ls first)

# 7. restart so the app reads restored DB + secrets  (verify: health + a real login by PM at step 10)
#    non-interactive restart REQUIRES the machine id (learned 09-22 rehearsal): read them with --json
fly machines list -a piper-morgan --json | python3 -c 'import sys,json; [print(m["id"], m["state"]) for m in json.load(sys.stdin)]'
fly machines restart 2869194b694018 -a piper-morgan-chroma      # chroma first (ids as of 09-22: chroma 2869194b694018, app 2869e7ec495248)
fly machines restart 2869e7ec495248 -a piper-morgan
curl -s https://piper-morgan.fly.dev/health | head -c 400   # READ: healthy, same sha as step 1, timestamp after the restart
curl -sL -o /dev/null -w "%{url_effective} %{http_code}\n" https://piper-morgan.fly.dev/   # READ: keyless render — / is a 302 to the login page; follow it, expect 200

# 9–10 are PM's (certs, DNS, OAuth callback) and Lead+PM's (real-domain verification).
```

Read-side verification after every step is Pard's regardless of path; under path B PM reads
each command from this sheet and Pard confirms the READ line before the next command.
