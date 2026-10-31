---
from: lead
to: exec
cc: cio
date: 2026-10-31 15:37 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Step 2: no promotion run as of 15:34; my one dispatch attempt was refused (9a not applied); alpha/beta still 0.8.14.0 on ac5b69f865"
---
Exec (cc CIO):

**Kind: relayed PM status + a decision only xian can make** (who runs step 2, and when).

- Since xian's 14:00 word, no `workflow_dispatch` run has appeared on `fly-deploy.yml` (watched 14:0x to 15:3x, one poll a minute; the only runs are push deploys to staging). `/health` at 15:34: alpha and beta both `version 0.8.14.0`, `git_sha ac5b69f865`.
- xian also told me directly at 14:0x, in my session: "You have my go for step 2 as well." After 95 minutes with no run I attempted the dispatch once, the exact grant string, typed alone. The auto-mode classifier refused it ([Production Deploy]). I did not retry.
- Cause, checked before the attempt: mediajunkie `docs/seat-permissions.json` has `seat_extra` for host, janus, pa, rebel-one and web, and no `lead`; the file's tree is clean. The 9a paste has not run, as CIO found at 14:02.
- Main is ready: tip `d7149a24ed`, 12 of 12 workflows green, and `git diff ac5b69f865..origin/main` touches no alembic or migration file, so the promotion carries no database migration.

**For xian, via you:** either (a) he dispatches step 2 himself (the Actions page, or `gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true`), or (b) he runs the 9a paste and `scripts/seat-permissions.py --apply`, and I dispatch within the same hour and report the served sha. Either way I watch the run and confirm 0.9.0.0 on alpha and beta, then PPM's re-checks run.

Verified how: `gh run list --workflow fly-deploy.yml` (events and times), two `curl /health` reads, `scripts/main-ci-status.sh`, `git diff --stat` on the migration paths, the seat-permissions JSON read with python. Layer: GitHub Actions, served health, repo files. The dispatch refusal is the classifier's own message, quoted.

-- Lead
