# Lead Developer — Duty-Cycle Escalations

Items raised during cycle fires that need cross-agent or PM attention. Living doc — append-only with disposition tracking.

**Format**: timestamp · target · status · brief · disposition (when closed)

**Maintenance mechanism (methodology-41, added 2026-06-10):** the `duty-cycle-tick` skill's STOP procedure now includes an **attention-doc reconciliation step** — at day-close, `gh issue view` each Open item that references a GitHub issue; any CLOSED/merged → move to Resolved with a disposition note. Plus per-fire appending during the Mail/Task loops. This replaces the vigilance-promise that let the doc go 14 days stale (Exec memo 2026-06-10). The mechanism lives in the skill (read at every fire), not institutional memory.

---

## Open

- **2026-06-18 · CXO (cc PM) · #1280 dark-rail design spec** — Lead is BLOCKED on a detailed #1280 left-rail design spec before rebuilding the 22-page shell. PM UAT (2 rounds) found the flip "doesn't resemble the mock, no global nav"; PM chose spec-first over revert/match-now. Requested via memo `393d4178a` (the 4 gaps: rail-content + full-nav placement · Radar persistent-vs-slide-out · non-home-page layouts · what "no global nav" means). Current flip is LIVE-but-flawed (revert to top nav available in minutes on PM's word). **Awaiting CXO spec.**

## Resolved

- **2026-06-10 → 2026-06-16 · PM · #1165 M3 UAT gate** — **RESOLVED (reconciled 2026-06-16 STOP)**: `gh issue view 1165` = CLOSED (M3 closed). The #1133→Radar re-scope dependency became **#1236 (Radar surface) + #1238 (DocumentEntitySource)** — both SHIPPED this session (behind `?radar=1`, PM-UAT-pending), tracked as their own issues.
- **2026-06-10 · PM · #1187 floor-wiring TANDEM** — **RESOLVED (reconciled 2026-06-12 STOP)**: #1187 CLOSED (summarize-issue full chain shipped + live-verified, the tandem fetch-augment landed). `gh issue view 1187` = CLOSED.
- **2026-06-10 · PM · #1129 Slack reconnection** — **RESOLVED (reconciled 2026-06-12 STOP)**: #1129 CLOSED (Slack inbound LIVE via Socket Mode; PM uses it for M3 review). `gh issue view 1129` = CLOSED.

- **2026-06-10 · PM · M3 next-step direction** — **RESOLVED**: PM chose (b) — build #313 File Browser. Slice 1 (search+filter) shipped 57c66aab7; remaining slices + (a)/(c) still queued.
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
