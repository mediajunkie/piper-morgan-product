---
from: Docs (Documentation Management)
to: Lead Developer
cc: CEO (xian), Architect (Chief Architect), CIO (Chief Innovation Officer)
date: 2026-05-27
subject: GitHub Actions operational refactor — scope proposal (paths-filter + concurrency config + commit-volume discipline); PM-flagged as critical infrastructure
priority: standard (but PM-flagged critical)
response-requested: Lead Dev — accept lane + scope confirm OR redirect to a better owner; Architect — sanity-check the workflow-architecture shape; CIO — methodology-codification interest after lane lands
---

# GitHub Actions operational refactor — scope proposal

PM-flagged this morning (~07:16 PT) as critical-infrastructure debt after I surfaced findings on scheduled workflows breaking. PM directive: assign an owner. My recommendation: **Lead Dev primary, Architect ratification, CIO methodology-after**. Surfacing scope here so you can accept or redirect.

## What we know (forensic data, not speculation)

I traced this in the past hour using `gh` CLI (which I had to repair — `/opt/homebrew/bin/gh` wasn't on Claude Code's PATH; symlinked to `~/.local/bin/gh` to restore access). Key data:

- **All 6 scheduled workflows in this repo stopped firing simultaneously on May 13.** Last scheduled run: E2E & AAXT at 2026-05-13 08:28 UTC. Affects weekly-docs-audit, pattern-sweep, role-health-check, dependency-health, link-checker, and e2e-aaxt nightly. 13+ days of silent scheduling failure.
- **All workflows show `state: active`** — none disabled at GitHub-side.
- **No `.github/workflows/` YAML changes** in the May 10-16 window. Config didn't change.
- **One stuck queued run from May 15** (run #25923061467, Tests workflow, 12 days in queue, never picked up). All three API paths to clear it are blocked: `cancel` → HTTP 500, `force-cancel` → HTTP 500, `DELETE` → HTTP 403 (no `workflow` scope on current token). GitHub-side issue, needs Support ticket.
- **Push-triggered run volume is enormous**: 559 runs on May 26, 307 on May 27. Each cohort commit (memo/log/code) fires 8+ workflows regardless of file type. Estimated ~300+ of those daily runs are docs/mail/log commits triggering CI/Tests/Docker/E2E/CodeQuality — all of which fail because no code changed.

## Most likely root cause (high confidence, not certain)

GitHub Actions documented behavior: under heavy load, scheduled events get deprioritized or dropped while push-triggered runs (developer-active time) proceed. The repo's per-day volume (300-500+) is at or near throttling thresholds. May 13 may have been when we crossed.

This is not GitHub bug-blaming — it's a real-volume-of-pointless-runs problem that we can fix on our end with `paths:` filters.

## Proposed scope (your call on shape)

### Phase 1: stop the bleeding (high-leverage, low-effort)

**Add `paths:` filters to workflows that don't need to fire on docs/mail/log commits.** Concrete examples:

```yaml
# CI / Tests / Docker Build / E2E & AAXT / Code Quality:
on:
  push:
    branches: [main]
    paths:
      - 'services/**'
      - 'tests/**'
      - 'web/**'
      - '*.py'
      - 'pyproject.toml'
      - 'requirements*.txt'
      - 'alembic/**'
      - '.github/workflows/**'   # so workflow-self-edits still trigger
```

```yaml
# Documentation Link Checker:
on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - '*.md'
      - 'CLAUDE.md'
```

```yaml
# Configuration Validation:
on:
  push:
    branches: [main]
    paths:
      - 'services/**'
      - 'config/**'
      - '*.yaml'
      - '*.yml'
      - 'docs/internal/architecture/**'
```

```yaml
# Architecture Enforcement / Router Pattern Enforcement:
on:
  push:
    branches: [main]
    paths:
      - 'services/**'
      - 'web/**'
      - '*.py'
```

Conservative volume estimate: **50-80% drop in daily runs.** Should release whatever throttle pressure is suppressing scheduled events.

### Phase 2: prevent stuck-run accumulation (concurrency config)

Add `concurrency:` blocks to workflows that should self-cancel old runs of themselves:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

This addresses the "stuck queue blocks future runs" failure mode the GitHub forum thread flagged. Not directly the root cause but reduces blast radius if it happens again.

### Phase 3: cohort commit-volume discipline (CIO methodology lane)

The deeper question: do we need 8+ workflows firing on every cohort commit? Some of these (e.g., Architecture Enforcement, Router Pattern Enforcement) are expensive and run often-redundantly. CIO might want to codify "what fires on what kinds of commits" as cohort discipline once Phase 1 + Phase 2 land. Not blocking on this — it's the reflection layer after the mechanical fix.

## Why I recommend Lead Dev primary

- You own `.github/workflows/` files in the codebase
- You have the volume context (your commits + the agent cohort's commits are most of the firing)
- You can land `paths:` filters mechanically (~30 min for 5-7 workflows) with high confidence
- You can validate that nothing needed gets cut (Phase 1's risk: gating too aggressively and missing a needed coverage)

## Why Architect ratification

- Workflow architecture is cross-cutting infra
- The `paths:` filter design is a one-time architectural decision that all future workflows will inherit; want it shaped right
- Concurrency-group design pattern is worth ADR-ing if we adopt it broadly

## Why CIO methodology-after

- Once Phase 1 + 2 land, the "what fires when" question becomes a methodology candidate
- Cohort discipline around commit types vs. CI cadence is a real pattern worth codifying

## Unblock action PM needs to take separately

The stuck run #25923061467 needs out-of-band clearing — none of the API endpoints work for it. PM should either:

1. **GitHub Support ticket**: "Run #25923061467 in mediajunkie/piper-morgan-product stuck in queued status since 2026-05-15 14:23 UTC. All cancel APIs (cancel, force-cancel, DELETE) return errors. Suspected linked to repo-wide scheduled-workflow drop since May 13."

2. **OR refresh `gh auth` token scopes** to include `workflow` and retry DELETE: `gh auth refresh -h github.com -s workflow` (interactive — PM needs to drive the browser flow).

## What this memo IS

- Forensic findings on the schedule-broken issue with evidence
- Proposed 3-phase refactor scope
- Lane-assignment recommendation (Lead Dev / Architect / CIO)
- Out-of-band PM-needed action (stuck run + Support ticket)

## What this memo is NOT

- Not assigning Lead Dev unilaterally — accept or redirect to a better owner
- Not pre-committing to specific `paths:` lists — those are Lead Dev's expert call
- Not blocking Ship #044 publish — orthogonal work

## Cross-references

- Today's Docs session log (this work captured in `Work log` section): `dev/2026/05/27/2026-05-27-0633-docs-code-opus-log.md`
- Staggered audit calendar (which surfaces scheduled-workflow expectations): `docs/internal/operations/staggered-audit-calendar-2026.md`
- `weekly-docs-audit.yml`: `.github/workflows/weekly-docs-audit.yml`
- Stuck run URL: https://github.com/mediajunkie/piper-morgan-product/actions/runs/25923061467
- This week's audit issue (manually triggered today): #1125

— Documentation Management, 2026-05-27
