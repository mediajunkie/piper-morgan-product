# Deploy Environments & the Release Train

**STATUS: Phases 0–1 are CURRENT PRACTICE (operating today). Phases 2–4 are a PROPOSAL — written down per the write-it-down-even-unratified discipline; PM ratification pending.**

> ⚠️ **UPDATED 2026-09-22 (Lead) — THE DROPLET ERA ENDED TODAY.** alpha.pipermorgan.ai is now
> **served by Fly** (cutover complete, `docs/internal/operations/alpha-fly-cutover-runbook-2026-09-22.md`;
> authority decisions.log 2026-07-10 + 2026-09-21). The droplet is stopped-and-warm as rollback
> until ~2026-09-29, then decommissions; the `production` branch retires with it (runbook step 11).
> Deploys to alpha are currently **manual `fly deploy --remote-only --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)`
> from `origin/main` under a per-window grant**; the durable path is §4e of the deployment-pipeline
> plan (CI deploy, builder pending PM's naming). Tables and diagrams below marked (superseded) are
> retained for the record.
**Owner**: Lead Dev · **Created**: 2026-07-12 (PM-requested during the beta cutover) · Decisions feeding this doc: decisions.log 2026-07-10 (#1278 walkthrough), the 7/10 staging-branch conversation (PM + Lead).

---

## The one-screen answer to "where does code go?"

```
worktrees (claude/*)  →  main  →  ┌─ alpha.pipermorgan.ai  (Fly app piper-morgan — since 2026-09-22)
   development           staging  └─ beta.pipermorgan.ai   (same Fly app; PM-only, OAuth mismatched since the cut)
                                      (production branch: retiring with the droplet, runbook step 11)
```

1. **Development happens in ephemeral worktree branches** (`claude/*`, Model B). Every agent works there; finished units push to `origin/main` continuously.
2. **`main` IS the staging branch.** It's where the cohort's work integrates, where CI gates run (Security suite, Architecture Enforcement incl. the ADR-077 D4 lint), and where code soaks before a release. We do not have — and at current scale do not need — a separate `staging` branch: main's continuous-integration discipline plus the release-cut ritual below already provides the main→release quality boundary.
3. **`production` is the external-share branch.** Releases are *cut* onto it (temp-worktree cherry-pick of the release payload + VERSION/pyproject bump — see `cut-release` skill + the v0.8.10.x train), never developed on.

## Where each environment gets its bits (TODAY — Phase 1, parity)

| Environment | URL | Host | Deploys from | How |
|---|---|---|---|---|
| **Alpha** | alpha.pipermorgan.ai | **Fly.io app `piper-morgan` (since 2026-09-22)** | `origin/main` | `fly deploy --remote-only --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)` (manual, grant-gated; CI path = plan §4e); verify via `/health` version+sha |
| *(superseded 09-22)* Alpha-on-droplet | — | DigitalOcean droplet (PM's VPS), stopped-warm to ~09-29 | `production` | `git archive origin/production \| ssh … tar -x` then `./deploy.sh` |
| **Beta** | beta.pipermorgan.ai (+ piper-morgan.fly.dev) | Fly.io (`personal` org) | `production` — **same cut** | `flyctl deploy --remote-only` from the repo (fly.toml; release_command runs the migrate); sidecars `piper-morgan-chroma` / `piper-morgan-gh-mcp` deploy from `deploy/fly/*.fly.toml` |

**Why both get the SAME cut right now**: beta's current job is *proving it matches alpha* (internal testing, #1386 gate execution). Parity is the point. One release train, two targets; a release isn't "done" until both boxes verify.

**Environment-specific state that is NOT in git** (the checklist that made the cutover real):
- **Secrets** — `fly secrets` is the one hosted store since 09-22 (droplet `/opt/piper/.env` is historical; ENCRYPTION_MASTER_KEY was set from the droplet value at the cutover — same key, never regenerate). GitHub OAuth: the Fly app now runs the **"Piper Morgan Alpha"** OAuth app (client + callback moved at cutover step 9b); **beta.pipermorgan.ai's GitHub login is therefore mismatched** (PM-only host, accepted per PM's alpha-canonical ruling). Slack/Google redirect URIs still carry fly.dev values — #1852.
- **Databases diverge** — beta's Postgres was seeded from a 2026-07-10 alpha snapshot; from that moment the two histories fork. A fresh re-migration (pg_dump → machine-side restore, minutes) is a *decision*, taken at most once more: right before beta becomes the primary surface.
- **`connector_bindings.mcp_server_ref` currently stores literal per-environment URLs** (compose hostname on alpha, `.internal` on Fly). Until ADR-070 Amendment A's resolver lands (task queued), any DB copy between environments requires the repoint step.

## Phase 2 — when beta needs to run AHEAD of alpha (the canary split)

**Trigger**: the first time we want a build on beta that alpha shouldn't have (release candidates for internal testing while alpha stays stable for alpha invitees + the PM/PA MCP-rig work).

- Beta becomes the **canary**: deploys from `main` cuts (or a then-created `staging` branch if we want named RC tags — decide at trigger time; the mechanics are a one-flag difference).
- Alpha stays the **stable** surface on `production`.
- Declare the split in decisions.log + here; nothing needs pre-building.

## Phase 3 — public beta (PM's "does production now go to beta?" — answer: yes)

**Trigger**: beta invitations go out (gate #1386 passed, per PPM's recommendation executed against the Fly artifact).

- `production` cuts deploy to **beta.pipermorgan.ai as the primary public surface** (if Phase 2 happened, beta "graduates" back from canary to stable at this moment — and the canary role moves to a fly `staging` app if still wanted).
- **Alpha enters sunset**: parallel-run continues only for the alpha cohort's migration window (their re-invite to beta), then the droplet is decommissioned per #1278's checklist (final backup, nothing load-bearing).
- One decision to make then: whether alpha-era user data merges into beta's DB (a second snapshot-migration) or alpha users start fresh. **PM call at the time; both are cheap at current data sizes.**

## Phase 4 — 1.0 / post-beta (envisioning; deliberately loose)

The natural end-state is a boring, conventional three-tier:

```
worktrees → main (CI) → staging env (auto-deploy from main) → production env (cut + promote)
                         staging.pipermorgan.ai                app.pipermorgan.ai (or www)
```

- **beta.pipermorgan.ai likely *becomes* the staging environment** (rename or CNAME) once a real production hostname exists — the Fly infrastructure is already the right shape for both.
- The release ritual stays: cuts onto `production`, promoted only after staging verification; the #1386-style gate becomes a *release* gate template rather than a one-off.
- Open questions parked for then: production hostname choice; whether prod gets its own Fly org (billing/isolation — apps can move orgs); multi-region; whether the droplet has any residual role (none expected).

## The refactor worth doing regardless of phase (small, already queued)

1. **ADR-070-A resolver** (task #108) — kills the per-environment binding-repoint step.
2. **A `deploy-release` skill** codifying the two-target deploy + verification (droplet loop + fly deploy + both container-verifies) so releases stay one-command-per-target. *(Candidate; not yet written.)*
3. When Phase 2 triggers: CI deploy automation (push-to-production → both deploys) is the moment auto-deploy earns its complexity — not before.

---
*Update this doc when any phase-trigger fires; each phase transition is a decisions.log entry. A stale phase label here is worse than no doc — the noticer-updates-stale-state rule applies.*
