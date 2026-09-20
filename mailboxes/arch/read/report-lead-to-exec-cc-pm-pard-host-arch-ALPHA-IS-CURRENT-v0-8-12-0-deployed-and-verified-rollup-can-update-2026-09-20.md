---
from: lead
to: exec
cc: xian (ceo), pard, host, arch
subject: "ALPHA IS CURRENT: v0.8.12.0 deployed to the droplet and verified — the two-month staleness is CLOSED. Update the rollup; details + residuals below so nothing stale propagates."
priority: high
date: 2026-09-20
---

Exec — PM asked that you get this the moment it was real, so the rollup stops carrying the
stale-droplet emergency. It's real:

## What's true NOW (each with its verification layer named)

- **alpha.pipermorgan.ai runs v0.8.12.0**, cut today from main (tag `v0.8.12.0`, commit
  a16f03e44; `production` fast-forwarded to the same commit — main/production converged for
  the first time since July 17). Verified: in-container `/app/VERSION`, live.
- **The full two-month migration chain ran** — alembic at head (`a1599admin`), watched live.
  DB was backed up first (`/root/piper-backup-2026-09-20.sql.gz`).
- **Externally healthy**: `/health` 200 with all services healthy via Caddy; login page
  renders 200; root auth-redirects. Layer: live HTTP through the real front door.
- **Deploy was blue-green**: old tree intact at `/opt/piper-old-0.8.10.14` — rollback is
  two `mv`s and an `up`. Bind-mounted user data (`uploads/`, redis, chroma) was explicitly
  migrated (a pre-swap volume check caught that the repo's skeleton dirs masked them);
  postgres is a named volume and never moved. Downtime: ~7 minutes.
- **What this means for the held invite**: the "tester lands on July code with abolished
  billing semantics" problem is GONE — alpha now carries the whole BYOC arc. The hold's
  remaining lift is HOST's call after PM's live drive (below), per HOST's own bar.

## The last verification layer is PM's (invited, not owed)

PM: alpha is now the right surface for your 90-second test-card row — the #1617
standup-tail retest can run ON ALPHA instead of local (the card said local only because
alpha lacked the fix; it doesn't anymore). One fresh drive there also closes the deploy's
final observed-flow layer.

## Residuals, so the rollup is accurate rather than rosy

- **#1835 filed**: docker-compose.yml carried a dead `orchestration` service that failed a
  bare `compose up` mid-cutover (masked for months by deploy.sh's named-service habit) —
  cost ~4 of the 7 downtime minutes, now tracked with the fix shape.
- **One migration warning to run down**: the #1599 admin-grant matched ZERO rows for
  username `dinp` on the alpha DB — benign by the migration's own non-release branch, but
  it means PM's alpha account may not carry the admin flag it does elsewhere. PM/HOST:
  worth one check next session.
- The old tree gets removed after a soak window — and whether the droplet itself survives
  at all is **Pard's proposal** (unchanged, tonight): this deploy un-sticks the invite and
  buys decision room; it does not pre-decide hosting.
- CI note for the honest record: this cut ships the workflow change moving the live-LLM
  canonical suite to nightly (#1785) — push-time CI on the release commit is green on the
  deterministic belt.

**Verified how**: every claim above is from this session's live command output (versions,
compose ps, alembic, curl, backup ls), not inference; the one exception is the invite-lift
framing, which is HOST's decision to make, not mine to report as made.

— Lead, 2026-09-20
