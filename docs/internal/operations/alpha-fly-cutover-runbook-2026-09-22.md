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
app serves (`/app/uploads`); untar chromadb into the `piper-morgan-chroma` app's volume. At 13 MB,
carrying Chroma beats rebuilding embeddings. **Redis: nothing to migrate** — the token blacklist
is a DB-seeded write-through cache since #1808 (DB is the record; cold Redis self-seeds at
startup). Denominator caveat: that's the one Redis surface Lead verified; Pard should eyeball
`data/redis` keyspace for anything durable-only before discarding.

**7. App restart on Fly** (release/machines restart) so it reads the restored DB + secrets.

**8. Arch/Pard — `mcp_server_ref` repoint** (plan §4d's named landmine): ADR-070 Amendment A made
bindings logical-key-based, so this *should* be config-only — verify against the restored data,
don't assume.

**9. PM — the cut**: `fly certs add alpha.pipermorgan.ai -a piper-morgan` (TLS moves off the
droplet's Caddy — do this before DNS so the cert is ready), then point `alpha.pipermorgan.ai`
DNS (CNAME → `piper-morgan.fly.dev`), then add the Fly callback URL to the GitHub OAuth app.
DNS revert is the rollback lever throughout.

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
