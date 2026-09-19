# Alpha droplet upgrade plan — bring the tester surface onto the current cut

**Author**: Lead. **Filed**: 2026-09-19 (PM ruling same day: resolve the underlying
droplet-parity/billing question NOW, before Janne's invite — not next week).
**Status**: READY TO EXECUTE, blocked on exactly one thing: SSH access to the droplet
(146.190.151.63) — either PM authorizes this seat's key (below) or PM runs the steps.

## Why (one paragraph)

alpha.pipermorgan.ai — the only surface real testers touch — almost certainly runs a
July-era cut: every deploy since the 07-12 cutover went to Fly (v113–v116 are Fly release
numbers), no droplet deploy appears in any Aug/Sep log, and the droplet refuses this seat's
SSH so the version can't be read from here. A July cut predates the entire server-key
abolition (#1807→#1822): testers onboard under billing semantics PM has since ruled dead.
The fix is not a caveat on the invite; it's bringing the droplet to the current cut.

## Step 0 — access (the one PM action this plan cannot substitute)

Authorize this seat's existing pubkey on the droplet (from any machine that can reach it,
or the DigitalOcean console):

```
# this seat's pubkey (~/.ssh/id_ed25519.pub on the Studio):
#   -> paste into /root/.ssh/authorized_keys on 146.190.151.63
```
(Deliberately not inlining the key text in a mailbox file; it's at `~/.ssh/id_ed25519.pub`
on the Studio, or I'll hand it over in-conversation on ask. Both existing Studio keys were
tried and refused — the droplet knows neither.)

**Or**: PM runs steps 1–6 directly; each is copy-pasteable.

## Step 1 — read before touching (facts, then decisions)

```bash
ssh root@146.190.151.63
cat /opt/piper/VERSION                                  # the July-cut hypothesis → fact
cd /opt/piper && docker compose ps                      # stack health
docker compose exec -T app cat /app/VERSION             # what's actually RUNNING
docker compose exec -T app python -m alembic current    # migration position vs head
```

## Step 2 — backup (pause-before-irreversible; non-negotiable before migrate)

```bash
docker compose exec -T postgres pg_dump -U piper piper_morgan | gzip \
  > /root/piper-backup-$(date +%F).sql.gz && ls -la /root/piper-backup-*.sql.gz
```

## Step 3 — the release question (PM call, one line, before the archive)

The release train (Phase 1) deploys alpha from `production` cuts. `origin/production` is
thousands of commits stale and is NOT what Fly runs (CLAUDE.md standing warning). Two
honest options:
- **(a) Proper train**: cut the next release onto `production` from current `main` (the
  `cut-release` skill; VERSION bump per the 090-reserved scheme), archive THAT to the
  droplet. Keeps the train's meaning; ~30 min more.
- **(b) Direct**: archive current `main` (the v116-equivalent tree Fly already runs — the
  same bits already serving, just on the other box). Faster; leaves the train's alpha leg
  formally skipped this once.
My recommendation: **(a)** — PM's "too much unfinished business" cuts against another
process exception, and the train exists precisely for this deploy.

## Step 4 — deploy (runbook mechanics, with the #1299 fix now real)

```bash
# from the MAIN checkout on the cut ref:
git archive <ref> | ssh root@146.190.151.63 'tar -x -C /opt/piper'
ssh root@146.190.151.63 'cd /opt/piper && ./deploy.sh'
```
- Droplet-local files (.env, Caddyfile, docker-compose.override.yml) are outside the
  archive — preserved by construction; do NOT touch them.
- `ENCRYPTION_MASTER_KEY` in /opt/piper/.env must remain unchanged (ciphertext dies with
  it — fly.toml's own warning).
- **#1299(a) is FIXED in code since the last droplet deploy** (`alembic/env.py:42,75,99`
  resolves the URL from env, ignoring the ini hardcode) — so `deploy.sh`'s migrate step
  should genuinely run for the first time ever. Expect a LONG migration set (July→now).
  If `BUILD_FAIL` appears, check `docker compose ps` first (the known 30s race) before
  re-running anything.

## Step 5 — verify at the layers that can fail (m-43)

```bash
curl -s https://alpha.pipermorgan.ai/health            # 200 healthy
ssh root@146.190.151.63 'cd /opt/piper && docker compose exec -T app cat /app/VERSION'
docker compose exec -T app python -m alembic current    # == head
```
Then the render/flow layer, not just curl: one full FTUX drive against the live box —
fresh account, store a throwaway key, one turn that spends it, confirm refusal-when-keyless
and serve-when-keyed both behave (the #1810/#1814 observed-flow bar, this time actually on
the box testers use). Existing testers' stored keys are per-user DB rows (#1185-era, which
the July cut already wrote), so #1814's reader serves them post-upgrade — verify with one
existing-account turn if PM can, else note as watch item.

## Step 6 — after green

- HOST lifts the hold per their own verification; invite goes out on a current, parity box.
- Update `alpha-deployment-runbook.md` (401-gate lines are already stale; add the #1299(a)
  resolution) and the release-train doc's Phase-1 row if (b) was chosen.
- The recurring cause dies with a standing rule: **any deploy ritual that ships Fly must
  either ship the droplet or explicitly log the skip** — one line in the deploy habit,
  proposed for the release-train doc.

**Verified how (for this plan's claims)**: runbook + release-train doc + fly.toml read this
session; #1299(a) fix confirmed by reading alembic/env.py at HEAD; both Studio SSH keys
tried against the droplet and refused (that's the Step-0 blocker, tested not assumed);
droplet-deploy absence grepped across all Aug/Sep session logs. NOT verified: anything on
the droplet itself — that's Step 1's whole point.
