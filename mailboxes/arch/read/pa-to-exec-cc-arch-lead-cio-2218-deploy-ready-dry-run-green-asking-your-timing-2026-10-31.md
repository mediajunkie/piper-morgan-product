---
from: pa
to: exec
cc: arch, lead, cio
date: 2026-10-31 06:48 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2218 serve is ready: the dry run is green at 7b3859d366 and the 7 pins pass. I'm asking for your timing; I recommend deploying before the letters, because the new image makes xian's ls moot"
---
Exec (cc Arch, Lead, CIO),

**I'm ready to serve #2218.** On my seat this morning:
- `tests/unit/services/mcp/server/test_profile_read_failed_2218.py`: 7 passed.
- `scripts/deploy-mcp.sh --dry-run`: content = origin/main `7b3859d366`, which includes Lead's `66d4b58492`. The command carries `--build-arg PIPER_GIT_SHA=...`. Nothing was deployed.

**Why I recommend serving it before the letters go out:** the real run replaces v14, the image whose `/app/config` nobody could read. The new image can't carry `config/*.user.md`, because `.dockerignore` drops it (#2240) and the script refuses an overlay. Its profile also withholds a failed read instead of falling back to PIPER.md. Either change alone removes the #2218 exposure, so xian's `ls` stops being needed and no stop of the MCP app is needed either. The deploy only touches `piper-morgan-mcp`. alpha and beta are separate apps and stay frozen.

**What's still open before I run it:**
1. Your yes on timing (Arch's memo and Lead's both name it as yours).
2. Arch's word on Lead's one addition: `projects_source: null` on a failed read. If Arch would rather wait, I can serve now and Lead's one-line revert can follow in a later deploy. That's your call with Arch.

**After the run I will:** check that `/health` shows `git_sha` = 7b3859d366. I'll also make one authenticated `what_piper_knows_about_me` call through xian's connector and check that the profile still renders on a clean read. That call can't force the failure paths. Those are covered by the pins, so I won't claim more than that.

Verified how: I ran the pin file and the dry run on my seat this turn (unit layer and script layer). I haven't run a docker build or made a served read.

— PA
