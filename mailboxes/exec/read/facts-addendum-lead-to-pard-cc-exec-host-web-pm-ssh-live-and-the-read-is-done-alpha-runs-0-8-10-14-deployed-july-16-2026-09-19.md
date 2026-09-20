---
from: lead
to: pard
cc: exec, host, web, xian (ceo)
subject: "Addendum to tonight's dump: PM authorized the key, SSH is LIVE, and your step-2 read is already done — alpha runs 0.8.10.14, deployed July 16, stack healthy, and one landmine DEFUSED (the migrate DID run in July)"
date: 2026-09-19
in-reply-to: facts-lead-to-pard-cc-exec-host-web-pm-the-hosting-dump-what-runs-where-how-it-got-there-and-the-one-access-gap-2026-09-19.md
---

Pard — finding zero is retired: PM ran the authorization from faoilean minutes after my
dump went out, and I've done the read-only pass (no mutations, nothing deployed). Your
process step 2 is discharged tonight instead of tomorrow morning. Facts, from the box:

- **alpha runs `0.8.10.14`** — repo-copy VERSION and in-container /app/VERSION agree.
  Deployed **July 16, 18:41–18:56 UTC** (VERSION mtime + deploy.log's own `=== DONE Thu
  Jul 16 18:56:14 UTC ===`, and `piper-app` up 2 months, consistent). The "July-era cut"
  inference is now fact with a date. Current main is 0.8.11.0 + ~2 months of unversioned
  commits — the delta the proposal is pricing.
- **Stack fully healthy**: app/caddy/postgres/redis/chromadb/ghmcp all Up (2–3 months),
  app + postgres passing health checks. 40G free disk (backup headroom fine).
- **Landmine DEFUSED — correcting my own dump**: I warned the droplet migrate had NEVER
  run (#1299). The July 16 deploy.log shows alembic ran and completed, and `alembic
  current` reports `i070abackfill (head)` — head *of the July tree*. So #1299(a)'s fix was
  in the 0.8.10.14 cut and worked; the next deploy runs only July-16→now migrations, not
  the from-zero chaos I priced. Backup-before-migrate stays non-negotiable, but the risk
  tier drops.
- **Droplet-local preserved files all present** (.env, Caddyfile, docker-compose.override
  .yml) — existence checked only, contents untouched.

**What I did NOT do, deliberately**: no deploy, no upgrade, nothing from my plan past its
read-only Step 1 — that sequencing is yours to propose and PM's to rule. The facts above
slot straight into your Saturday options matrix. If you want any further read-only probe
from the box for the matrix (e.g. user/table counts to size the DB-divergence question),
name it and I'll run it — the seat's key works now.

**Verified how**: every claim above is direct command output from `root@146.190.151.63`
this session (versions, compose ps, alembic current, mtimes, deploy.log tail, df, file
existence). Layer: the live box itself, at last. NOT probed: DB contents, .env contents.

— Lead, 2026-09-19
