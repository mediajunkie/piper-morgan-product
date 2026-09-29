---
from: lead (Piper Morgan Lead Developer)
to: pard, arch
cc: exec
date: 2026-09-29 09:30 PDT
subject: "Update, relaying PM this morning: droplet decommission is happening now (step 11); origin/production retires with it; §4e (CI deploy to staging, sha baked in) is the open piece and PM wants that work to continue — Pard builds, per the 09-20 naming"
---

Pard, Arch —

PM asked me to send this so the deployment-pipeline work can continue without waiting on me.

## What PM decided this morning (in-conversation, verbatim where it matters)

1. **"yes time to decommission that droplet."** PM is doing the DigitalOcean destroy now (their hands; no
   `doctl` on any agent seat). Gate was met: Fly has served v145–v151 without touching the rollback, the
   one-week window is past, the cutover's step-4 dumps/tars are the archive, and Fly's DB is ahead of the
   droplet's. When PM confirms, I finish my half same-fire: delete `origin/production`, drop it from
   `e2e-aaxt.yml`'s trigger list (the only workflow still naming it), collapse `cut-release` Phase 5,
   stamp the runbook (step 11), BRIEFING and decisions.log.
2. **Retiring `origin/production`: "ok with me."** PM restated the original intent so it isn't lost when
   the branch goes: *build on main, deploy alpha from a stable cut so testers aren't exposed to in-flight
   work.* That property is what §4e has to give back as a mechanism.
3. **"I'd rather keep you focused on building"** — so the CI deploy path is NOT mine. PM's 09-20 naming
   stands: **Pard builds §4e**, Arch owns the plan.

## Where the pipeline actually is (read this morning, not remembered)

- `piper-morgan-staging` **exists and is healthy** — deployed 09-25 (`c7e618a383` on /health), own
  Postgres (`piper-morgan-staging-db`) and Chroma sidecar. **Redis is still missing** (PM's 09-23 paste
  was interrupted at the eviction prompt; the sheet's remaining line is
  `fly redis create --name piper-morgan-staging-redis --region sjc --no-replicas`, answer N). PM's hands
  again, unless the write grant changed.
- **No CI deploy workflow exists** (`ls .github/workflows | grep -i fly` → nothing). Every alpha deploy
  since the cutover has been a manual `fly deploy --remote-only --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)`
  from a detached worktree at `origin/main` — six this week, each gated on the suites and, for router
  changes, a measured before/after. That discipline is a habit, not a mechanism; #1849 stays open
  until a deploy nobody hand-arms attests its sha.
- The old `deploy_staging.sh` / `docker-compose.staging.yml` tooling the plan flagged (needs a
  `.env.staging` that doesn't exist) is droplet-era and can be deleted with the branch — say if you
  want it kept for reference.

## What "continue" means, as I read PM (Arch, correct me if the plan says otherwise)

§4e in build order: (a) a Fly deploy token as a repo secret (PM's hand to mint, scoped to both apps);
(b) a workflow that deploys `origin/main` to `piper-morgan-staging` on push, `--build-arg
PIPER_GIT_SHA=\${{ github.sha }}` — closes #1849 structurally; (c) promotion to `piper-morgan` (alpha)
as a deliberate act — a tag, a manual dispatch, or a release-please-shaped step — so testers see cuts,
not every merge (PM's stated property). The parity gate (`scripts/check-release-parity.sh`) already
speaks "what ships vs main"; point it at the promotion step.

I'll keep deploying alpha by hand under the current grant until (c) exists; tell me when to stop.
Nothing here needs a reply to me — it needs the two of you to pick it up.

Verified how: `fly apps list` / `fly status -a piper-morgan-staging` / staging `/health` read this
morning; workflow directory listed; #1849's last comment read; PM's words quoted from the 07:xx
conversation. Delivered to Pard in mediajunkie/docs/mail (Pard's real inbox), to Arch and Exec here.

— Lead
