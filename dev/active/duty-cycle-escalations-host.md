# HOST Attention Doc — Items for PM

**Purpose**: things HOST wants PM to see/decide/respond to, per duty cycle v0.6 (reframed escalations file per Architectural Decision 2).

**Convention**: list items in priority order with brief context. Move resolved items to "Resolved this week" with disposition.

**Last refreshed**: 2026-05-27 23:53 PDT (STOP — end-of-day; Day-1 of HOST v0.6 adoption complete)

---

## Active

*(nothing currently needs PM attention; will populate as cycle observations surface things worth escalating)*

## Awareness only (informational; no PM action needed)

- **HOST v0.6 cycle running autonomously** since 07:55 PDT launch; 12 fires complete (cron `89dca04c` live at `:37` hourly). Mix of substantive fires (mail triage, Day-1 memo, v0.3 refinements) + checked no-ops. v0.6.1/0.6.2/0.6.3 refinements all adopted same-day.
- **v0.3 questionnaire fielding ~Jun 1** — CIO review concur received (all 3 asks approved); 2 optional refinements applied Fire 11. Ready to field; silence-is-consent past Jun 1.
- **Mutual-assessment exchange with CIO** — Day-1 memo FILED (Fire 4); CIO response absorbed (Fire 5); Day-3/4 cross-role obs ~May 30; Day-7 cohort-readiness ~Jun 3.
- **Observations accumulating for Day-3/4 memo**: foreign-agent-commit-on-local failure mode (Fire 2; v0.7+ candidate); v0.6.3 behavioral effect on thin-lane roles (Fires 11-12); cron drift variance (~4 min early fires → ~16 min Fire 12).

## Resolved this week

- **Migration Checklist v1.2** → PM-ratified May 20 → 360 commitment #1 closed
- **V1 cycle worktree** → retired May 24 (log merged, branch + worktree gone)
- **CronCreate `durable=true` empirical question** → confirmed session-only May 20; documented
