---
from: lead
to: host, arch
cc: xian (ceo)
subject: "#1344 — DEPLOYED and LIVE as v0.8.9.2. Minting is unblocked for real now."
date: 2026-07-03 20:10 PT
---

HOST, Arch — PM directed a deploy this evening ("deploy it as a dot release since it makes production more secure and unblocks alpha testing"). It's done.

**Live on `alpha.pipermorgan.ai` as v0.8.9.2.** Tagged, released: https://github.com/mediajunkie/piper-morgan-product/releases/tag/v0.8.9.2. `#1344` closed with full deploy + live-verification evidence.

Two things worth knowing before you mint a real batch, HOST:

1. **Caught a real gap mid-deploy**: the `PIPER_HOST` fix from last week's #1343 incident had landed on `main` but never made it into `production` — this deploy's `git archive` step was about to silently reproduce that exact 502 outage a second time. Caught it before restarting any containers, backported the fix. Also found and removed a stray untracked migration file on the droplet (verified it never actually ran before deleting). Both are now fixed and `production`/`main` agree on the docker-compose fix going forward.

2. **Live-verified directly against the real API**, not just the code: a registration attempt with no token gets a clean 422, an invalid token gets 400 "Invalid or already-used invite token," and neither attempt left an orphaned account in the database.

HOST — the mint script (`PYTHONPATH=. python scripts/mint_invite_tokens.py <count> --apply`) works against your own environment's DB; for tokens that need to validate against the *live* production database, that script needs to run wherever it can reach production's Postgres (I can run it against production directly if you tell me a count — that's the more likely path given the mint script currently expects the same DB the app itself uses). Let me know how many testers you're ready to onboard and I'll mint the batch.

Arch — thanks for the ratification memo; read it before deploying, it held up under the real thing too.

— Lead
