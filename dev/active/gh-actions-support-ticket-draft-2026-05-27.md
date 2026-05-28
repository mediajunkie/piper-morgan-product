# GitHub Support Ticket Draft — stuck workflow run + scheduler suppression

**For PM to paste into**: https://support.github.com/contact (under GitHub Actions category)

**Status**: Step A (Settings toggle) tried 2026-05-27 2:23 PM PDT — failed.
Step B (volume-reduced commit via Phase 1+2 paths-filter merge `f372ce793`,
2026-05-27 2:31 PM PDT) — failed; ~3 hrs later still queued + scheduled workflows
still last fired May 11/13.

---

## Subject

Workflow run #25923061467 stuck in queued status 12+ days; correlated scheduled-workflow drop across all 6 scheduled workflows starting 2026-05-13

## Body

Hi GitHub Support,

We have two related problems on our repository `mediajunkie/piper-morgan-product` that appear to share a root cause:

### Problem 1: Stuck workflow run

Workflow run [#25923061467](https://github.com/mediajunkie/piper-morgan-product/actions/runs/25923061467) (Tests workflow) has been in `status: queued` since 2026-05-15 14:23 UTC — **12+ days as of this report**. All three API endpoints for clearing it return errors:

- `POST /repos/.../actions/runs/25923061467/cancel` → HTTP 500
- `POST /repos/.../actions/runs/25923061467/force-cancel` → HTTP 500
- `DELETE /repos/.../actions/runs/25923061467` → HTTP 403 (with `workflow` scope on the token; the docs note only `completed` runs are deletable, which matches our observed behavior)

### Problem 2: Correlated scheduled-workflow drop

All 6 of our scheduled workflows stopped firing simultaneously on/around 2026-05-13:

- `weekly-docs-audit.yml` — last scheduled run 2026-05-11 17:49 UTC
- `e2e-aaxt.yml` (nightly cron) — last scheduled run 2026-05-13 08:28 UTC
- `dependency-health.yml`, `pattern-sweep.yml`, `role-health-check.yml`, `quarterly-maintenance.yml` — all simultaneous drop

All workflows show `state: active` in `GET /repos/.../actions/workflows`. No `.github/workflows/` YAML changes occurred in the May 10-16 window. Push-triggered workflows continued firing normally throughout this period.

### Self-serve remediation attempted (both failed)

Based on community findings:

1. **2026-05-27 2:23 PM PDT** — Toggled `Settings → Actions → General` off/on. No effect; stuck run still queued, scheduled workflows did not resume.
2. **2026-05-27 2:31 PM PDT** — Merged a commit reducing push-trigger volume via `paths:` filters (`f372ce793` on `main`). No effect ~3 hours later. The hypothesis was that throttling pressure from high push volume was suppressing scheduled events; volume reduction should have released that pressure. It did not.

### Suspected root cause (best guess; needs backend confirmation)

Our repo's per-day push-triggered workflow run count is high (300-500+ runs/day from agent cohort activity). GitHub's documented behavior is that scheduled events can be deprioritized or dropped under heavy load. We suspect a wedged repo-level scheduler state — possibly accumulated from the high push volume — that:

- Refuses to dispatch new scheduled events
- Holds queue slot #25923061467 in a non-terminal state that doesn't respond to cancel APIs

Self-serve workarounds (settings toggle, volume reduction) haven't resolved either symptom, which suggests backend intervention is needed.

### What we need

1. Force-clear queued run #25923061467 (or confirm it's irrecoverable so we can document).
2. Investigate whether the repo's scheduled-workflow scheduler state is wedged, and reset it if so.
3. If both are the same wedged state: a single fix resolves both.

Happy to provide additional diagnostic info — workflow YAML, run logs, anything that would help diagnose.

Thanks,
[PM name]

---

**Reference materials**:

- Stuck run forensic research: `dev/active/gh-actions-stuck-run-research-2026-05-27.md`
- Phase 1+2 merge: commit `f372ce793` 2026-05-27
- Initial Docs scope memo: `mailboxes/lead/read/memo-docs-to-lead-cc-pm-arch-cio-github-actions-operational-refactor-scope-2026-05-27.md`
