# Coverage-Audit Gate for Refactor Deltas

## Overview

**Coverage-Audit Gate for Refactor Deltas** is the prevention discipline that requires, for any refactor commit with substantial line-count delta in cross-cutting surface files (entry points, route mounts, startup, plugin registries), a same-PR or follow-up coverage audit verifying that downstream subsystems retain their pre-refactor wiring. The discipline:

1. **Trigger**: a commit with `>300 line-delta` in surface-shaped files — `main.py`, `web/app.py`, `services/*/startup.py`, `*/plugin.py`, `services/orchestration/workflow_factory.py`, or equivalent registry/dispatch surfaces.
2. **Gate**: before merge, produce an inventory of pre-refactor subsystems mounted/registered via the surface, and verify each one has explicit wiring (or an explicit deprecation marker) in the post-refactor state.
3. **Failure mode this prevents**: silent wiring removal during refactor. The wiring's absence doesn't fail loudly — downstream subsystems just fail-silent (no inbound traffic, no error logged, no test catching the regression because tests cover the LOGIC not the WIRING).
4. **Successful audit becomes the verification artifact** — the inventory + post-state mapping is what proves no wiring was lost.

The discipline is general — applies to any refactor that touches surfaces where downstream subsystems register/mount. Different mechanism layer from Pattern-073 (Documentation-Asserted-Behavior Drift) and from methodology-30 (Consumer-Trace Verification): see below.

## Why This Methodology

### The 2026-05-27 #1129 SLACK-INBOUND-STRUCTURAL discovery

The discipline was named explicitly after today's forensic discovery (#1129). PM attempted a live Slack-inbound smoke test (DM "hey piper..." + channel @mention) and Piper did not respond. Investigation revealed:

- **CORE-GREAT-2D commit `aad66d9d1` (2025-10-01)** deleted ~750 lines from `main.py` (1184 → 421). That delta removed the `SlackWebhookRouter` mount line (`app.include_router(slack_router.get_router())`).
- **GREAT-3B commit `e12d62303` (2025-10-03)** introduced a plugin-system replacement but `slack_plugin.py::get_router()` only exposed `/status`, not the `/webhooks/events` routes.
- No follow-up coverage audit caught the gap.
- **8 months of cohort-wide asserted-behavior drift followed**: README declared "Phase 3 Complete ✅", multiple memos referenced Slack inbound as working, a 2025-10-06 blog post ("Three Integrations Walk Into a Bar") described Slack as working **5 days after the structural disconnection**. The runtime contradicted the documentation for the entire window.

The cost: a discoverable feature was silently broken for ~240 days. The cause: the refactor's line-count delta was load-bearing, and no procedure required reviewing the consequences of that load-bearing-ness.

CIO disposed this as methodology-37 (own slot, not Pattern-073 absorption) on May 27. Lead Dev authors (this filing).

### Why this is distinct from Pattern-073

Pattern-073 (Documentation-Asserted-Behavior Drift) is a **recognition discipline**: when narrative artifact A asserts behavior B that code C no longer implements, that's drift; the catch-trigger is a reader's audit during use.

methodology-37 is a **prevention discipline**: gate the gap-creating event (the refactor commit) before the drift can compound.

| Pattern-073 | methodology-37 |
|---|---|
| Architectural pattern (catalog) | Methodology discipline (corpus) |
| Names a failure shape | Names a prevention procedure |
| Filed when ≥3 instances surface | Applied as a gate before refactor commits land |
| Resolution: clean up the misleading surface after the fact | Resolution: don't let the gap open in the first place |
| Catches drift after propagation (8 months in #1129) | Catches the gap-creation event same-PR or close-to-it |

The two compose: methodology-37 at refactor time prevents the gap from opening; Pattern-073 catches the residual instances where prevention failed.

### Why this is distinct from methodology-30 (Consumer-Trace Verification)

methodology-30 verifies **claims about consumption** (X uses Y) by navigating the call site. methodology-37 verifies **the inverse**: that load-bearing producer-side wiring (mount points, route registrations) hasn't been silently removed during refactor. Consumer-trace traces from claim → call site; coverage-audit-gate inventories from pre-refactor surface → post-refactor surface.

The two compose at different lifecycle moments: consumer-trace is filing-time discipline for new claims; coverage-audit-gate is refactor-time discipline for surface-shaped changes.

## The verification procedure

For any refactor commit with `>300 line-delta` in a surface-shaped file:

1. **Inventory the pre-refactor surface.** Before merge, list every subsystem registered/mounted via the file being refactored. For `main.py`: every `app.include_router(...)`. For `web/app.py`: every `RouterInitializer.mount_router(...)`. For `*/plugin.py`: every plugin's exported endpoints/routers/services.
2. **Inventory the post-refactor surface.** Same exercise on the post-state. List what mounts/registers in the refactored file.
3. **Diff the two inventories.** Each subsystem in the pre-list must appear in the post-list OR have an explicit deprecation marker (commit message, ADR, or removed-intentionally comment).
4. **Verify each retained subsystem still reaches downstream.** Not just present-in-list but connected to its handlers. For a route mount, verify the route file actually mounts the handlers it claims to mount.
5. **Document the diff as the verification artifact.** The inventory diff becomes the proof. Future archaeologists navigate the diff, not the prose.

A refactor that passes step 3 but skips step 4 produces a load-bearing comment without verifying behavior. That's the GREAT-3B-vs-GREAT-2D shape: a replacement existed, but its exposure surface didn't match the original.

## When to apply this framing

### Apply this framing when

- Authoring or reviewing a refactor PR with substantial line-count delta in entry-point / mount / startup / plugin-registry files.
- Conducting an `audit-cascade` or `code-review` skill pass on a refactor of cross-cutting infrastructure.
- Investigating Pattern-073 instances where the cause is suspected to be a silent wiring removal.
- Reviewing cleanup-shaped refactor commits, since cleanup-shaped refactors are high-risk for this failure mode. (No standalone "cleanup as pattern" methodology was ever filed — see the corrected cross-reference below.)

### This framing does not apply when

- The refactor is contained to a single subsystem's internals (no cross-cutting surface touched).
- Line-count delta is `<300` AND the surface is not entry-point/mount/startup/plugin-registry shaped.
- The refactor explicitly deletes a deprecated subsystem (deprecation marker present in commit message or ADR).
- Type-system or generated code guarantees mechanical preservation of wiring (rare in Python; common in Rust/TypeScript with monorepo build tools).

## What it predicts

If methodology-37 is applied correctly across the cohort, the following downstream signals should appear:

- **Silent wiring removal regressions drop** — refactor PRs ship with an explicit "what was registered before vs. after" inventory; gaps are caught at review time, not 8 months later.
- **Pattern-073 instance count drops for the wiring-removal subclass** — instances that would have surfaced via Pattern-073 recognition discipline are caught at refactor time instead.
- **Refactor PRs grow richer review artifacts** — the inventory diff becomes a standard PR section, navigable by reviewers and future archaeologists.
- **Cross-agent challenges to refactor PRs become specific** — *"show me the pre/post mount inventory"* becomes a routine review request when surface-shaped files change.
- **Cohort-discipline-as-moat compounds** — methodology-37 plus methodology-30 plus Pattern-073 together cover prevention + verification + recognition at three different lifecycle moments. Pattern-29 (Pattern Formation via Successful Imitation) predicts adoption if the discipline visibly catches regressions in PR review.

## Operational heuristics

### What counts as a "surface-shaped" file

Files whose primary role is to register/mount/dispatch subsystems for downstream consumption:

- **Entry points**: `main.py`, `web/app.py`, language-specific equivalents
- **Startup orchestration**: `services/*/startup.py`, `web/startup.py`, lifecycle hooks
- **Plugin registries**: `*/plugin.py`, plugin-loader modules, plugin-discovery files
- **Workflow registries**: `services/orchestration/workflow_factory.py`, action mappers, intent registries
- **Route mount aggregators**: `web/api/router_initializer.py`, route-mounting orchestrators
- **Configuration loaders** that conditionally enable subsystems based on flags

### What counts as a "substantial line-count delta"

The `>300` line-delta threshold is heuristic — calibrate per repo. Rationale: 300 lines is roughly the size at which manual review reliably misses individual mount points without an explicit inventory. Smaller refactors are usually inspectable in one pass; larger ones aren't.

PRs that delete more than `>500` lines from a surface-shaped file should default to requiring the inventory diff even without other refactor markers.

### What counts as a "deprecation marker"

Acceptable explicit-deprecation forms:
- Commit message naming the removed subsystem ("removes deprecated SlackWebhookRouter mount; replaced by plugin system")
- ADR documenting the removal and its replacement
- Inline comment at the removal point naming what was removed and why
- Issue link to the removal-tracking issue

Absent any of these, the subsystem must appear in the post-state inventory.

## Adoption shape

Initial adoption: PR-author responsibility — when authoring a refactor with `>300` line-delta in surface-shaped files, include the pre/post inventory in the PR description. Reviewers verify the inventory before approving.

Tooling layer (v0.7+ candidate): a CI check that flags refactor PRs matching the trigger criteria and prompts for the inventory section. Not load-bearing yet — discipline-side adoption first.

Cross-agent: any role conducting `code-review` or `audit-cascade` on a refactor PR can apply the gate. Architect's surface review and Lead Dev's implementation review are the natural review touchpoints.

## Cross-references

- **#1129 SLACK-INBOUND-STRUCTURAL** (the seed incident): https://github.com/mediajunkie/piper-morgan-product/issues/1129
- **Lead Dev proposal memo** (May 27): `mailboxes/cio/read/memo-lead-to-cio-cc-pm-methodology-candidate-load-bearing-line-count-deltas-2026-05-27.md`
- **CIO disposition memo** (May 27): `mailboxes/lead/read/memo-cio-to-lead-cc-pm-methodology-37-disposition-coverage-audit-gate-different-layer-than-pattern-073-2026-05-27.md`
- **methodology-30 Consumer-Trace Verification** (sibling discipline, different lifecycle moment): `docs/internal/development/methodology-core/methodology-30-CONSUMER-TRACE-VERIFICATION.md`
- ~~**methodology-19 Cleanup as Pattern**~~ — **broken reference, resolved 2026-08-12 (CIO, #1584 Part C).** `methodology-19-CLEANUP-AS-PATTERN.md` was never filed; slot 19 belongs to `methodology-19-INTEGRATION-POINTS.md` and has since 2026-05-27 predates this doc. No sibling methodology on refactor-as-cleanup exists today — the closest filed discipline is `methodology-35-ASYMMETRIC-DISCIPLINE-CREATION-WITHOUT-PAIRED-CLEANUP.md`, but it addresses paired-cleanup-at-creation-time, not cleanup-shaped-refactor-risk, so it is noted here rather than substituted as an equivalent.
- **Pattern-073 Documentation-Asserted-Behavior Drift** (recognition discipline; catches what prevention misses): `docs/internal/architecture/current/patterns/pattern-073-documentation-asserted-behavior-drift.md`
- **methodology-28 Pre-Filing Slot-Availability Check** (CIO discipline that allocated slot 37): `docs/internal/development/methodology-core/methodology-28-PRE-FILING-SLOT-AVAILABILITY-CHECK.md`
- **Forensic report on #1129** (the empirical case study this methodology is built on): `dev/active/slack-inbound-forensics-2026-05-27.md`

---

*Filed 2026-05-27 by Lead Developer. Seed instance: #1129 SLACK-INBOUND-STRUCTURAL — Slack inbound silently disconnected for ~8 months after CORE-GREAT-2D refactor.*
