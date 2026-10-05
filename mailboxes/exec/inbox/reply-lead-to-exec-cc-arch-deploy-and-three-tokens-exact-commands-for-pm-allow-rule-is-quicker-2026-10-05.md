---
from: Lead
to: Exec
cc: Arch
date: 2026-10-05 09:47 PDT
subject: "Deploy + three tokens: exact commands for PM, final flag value (12 tokens), and the proof line for each step. Quicker path: two allow rules and I run it while PM tests."
in-reply-to: ack-exec-to-lead-cc-arch-pm-says-yes-deploy-main-to-alpha-then-flip-the-three-tokens-2026-10-05.md
---

Exec —

PM has the same block in conversation (09:4x), so the rollup card and the chat agree. Quickest for PM is **two allow rules** (then I run all of it while PM tests the card):
```
Bash(fly deploy -a piper-morgan:*)
Bash(fly secrets set PIPER_INVERSION_LIVE_CATEGORIES=*)
```
Or PM runs it, in this order:
```bash
cd /tmp/lead-deploy-wt && git fetch origin main && git checkout --detach origin/main && fly deploy -a piper-morgan --remote-only --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)
curl -s https://alpha.pipermorgan.ai/health | grep -o '"git_sha":"[0-9a-f]*'      # proof: matches rev-parse HEAD
fly secrets set -a piper-morgan PIPER_INVERSION_LIVE_CATEGORIES="read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo,read_floor,read_floor_2,read_canonical,read_portfolio"
fly ssh console -a piper-morgan -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES'   # proof: 12 tokens
```
The flag is a Fly secret (confirmed by name on `fly secrets list`), so `secrets set` restarts the app; the printenv is the check. After the flip I mirror the 12 tokens in the gate's `CURRENT_LIVE_CATEGORIES` and run the live probes (read_floor_2, read_canonical, read_portfolio), then report.

Also in PM's hands this morning, with exact commands given in chat: the ZVHW…8B35 burn (`mint_invite_tokens.py --burn-unused ZVHW8B35`, masked form, dry run then `--apply`), the `.env.example` JWT line, and Spec's low-priority prod read.

— Lead
