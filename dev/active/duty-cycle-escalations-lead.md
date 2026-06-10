# Lead Developer — Duty-Cycle Escalations

Items raised during cycle fires that need cross-agent or PM attention. Living doc — append-only with disposition tracking.

**Format**: timestamp · target · status · brief · disposition (when closed)

**Maintenance mechanism (methodology-41, added 2026-06-10):** the `duty-cycle-tick` skill's STOP procedure now includes an **attention-doc reconciliation step** — at day-close, `gh issue view` each Open item that references a GitHub issue; any CLOSED/merged → move to Resolved with a disposition note. Plus per-fire appending during the Mail/Task loops. This replaces the vigilance-promise that let the doc go 14 days stale (Exec memo 2026-06-10). The mechanism lives in the skill (read at every fire), not institutional memory.

---

## Open

- **2026-06-10 ~09:52 AM PDT · PM · M3 next-step direction** — With #1124 closed, surfaced the M3-remaining assessment + asked which to start: (a) #1165 UAT walkthrough (PM session), (b) build #313 File Browser backend/UI ahead of UAT, or (c) set up #1129 Slack DinP re-registration so Socket Mode can be wired. Awaiting PM choice.
- **2026-06-10 ~09:52 AM PDT · PM · #1187 defer decision** — Recommended moving #1187 SUMMARIZE-FETCH-AUGMENTATION out of M3 (graceful floor degradation is acceptable for beta; enhancement, not a gap). Awaiting PM confirm to re-milestone post-MVP.

## Resolved

- **2026-05-27 · PM · #1122 disposition** (multi-turn antecedent fix scope) — **RESOLVED**: #1122 CLOSED in GitHub (option B shipped — extract_slots conversation_history). Disposition made; no longer awaiting PM.
- **2026-05-27 · PM · #1081 live smoke** (NOTION-SLACK-XREF UAT) — **RESOLVED**: #1081 CLOSED. Superseded by #1129 (Slack inbound structurally unmounted since 2025-10-01 → live smoke can't pass until the Socket Mode rebuild).
- **2026-05-27 · PM · #1081 disposition post-#1129** — **RESOLVED (moot)**: #1081 already CLOSED; drop-vs-keep superseded by #1129 absorbing the Slack-inbound rebuild.
- **2026-05-27 · PM · GH Actions stuck run** — **RESOLVED**: 2 weeks moot; Phase 1+2 paths-filter + concurrency landed (commit `f372ce793` + follow-ups); CI green since. The single stuck queued run is no longer load-bearing.
- **2026-05-27 · Arch · GH Actions paths-filter sanity-check** — **RESOLVED**: Phase 1+2 GH Actions work landed with the filter taxonomy in place; no Arch objection surfaced.

## Notes

- **Format discipline**: terse single-line entries, link to memo / issue / commit if disposition needs detail elsewhere.
- **Escalation tiers**:
  - **PM**: requires CEO decision (scope, priority, ratification)
  - **Cross-agent**: requires another lead's input (Arch on classifier work, CIO on methodology codification, etc.)
  - **Cohort-wide**: requires multi-role coordination (governance, discipline, infrastructure)
- **Closure**: move from Open → Resolved with disposition (link to memo or commit). Don't delete entries.
- **Reconciliation**: STOP-fire step gh-checks Open items vs GitHub state; closed issues → Resolved (the methodology-41 mechanism above).
