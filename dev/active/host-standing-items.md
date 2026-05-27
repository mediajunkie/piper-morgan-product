# HOST Standing Items — Task List

**Purpose**: HOST's task queue per duty cycle v0.6 (reframed standing-items tracker per Architectural Decision 1).

**Convention**: tasks listed roughly by priority/cadence. Mark `[x]` when complete; `[⏸]` when blocked on external (per recurring-failure memory on deferred-AC). Move to "Closed" section at end-of-day or end-of-week.

**Last refreshed**: 2026-05-27 07:30 PDT (Day-1 of HOST v0.6 cycle adoption)

---

## Active

- [ ] **v0.3 Agent 360 questionnaire fielding** (target ~Jun 1; silence-is-consent if CIO doesn't return rewrite by then). Draft at `dev/active/agent-360-questionnaire-v0_3-draft.md`. Sent for CIO review at commit `58bfab3f5`.
- [x] **v0.6 duty cycle Day-1 adoption**: substrate up + cron live at `:37`; **Day-1 mutual-assessment memo to CIO FILED** (commit `569c65a7f`, Fire 4 11:55 PDT). Watch items addressed: (a) trust-property-touch — too early to judge / observing / (b) role-health-touch — too early to judge / observing / (c) drift stable ~4 min past :37 across Fires 1-3 / (d) cron-prompt v2 with CIO framing reminders queued for next session-start.
- [ ] **Mutual-assessment Day-3/4 memo** (cross-role observations comparing CIO + HOST deployments) — target ~May 30
- [ ] **Mutual-assessment Day-7 memo** to PM (adopt-readiness assessment for next cohort wave) — target ~Jun 3
- [ ] **HOST input on MEM #974 format** (post-data, ~early Jun) — Docs will surface aggregated patterns; HOST evaluates whether 3-bucket format wants trust-relevant enrichment
- [ ] **v0.3 re-benchmark synthesis** (~Jun 12) — diff-against-baseline + tier-3 cross-role convergence findings

## Blocked / waiting on external

- [⏸] **CIO review of v0.3 questionnaire draft** — waiting silently OK; fielding ~Jun 1 if no rewrite by then
- [⏸] **PP-004 (Structural-Fix-Instead-of-Discipline-Fix) formal filing** — CIO holding for ≥4 instances before filing (3 confirmed so far); watch for instance #4 from Comms Layers B/C/D or v0.6 cycle pilot
- [⏸] **methodology-35 (Asymmetric Discipline) cite** — confirmed in v0.3 §10.4 cycle-experience module; pending CIO review feedback

## Watch surfaces

- v0.6 cycle pilot Phase B observations (CIO-led, HOST now also adopter — co-observer)
- Outcomes investigation (PA leads, CIO co-authors; week-of-May-25 start)
- Cohort response to v0.3 fielding (~Jun 1+)

## Closed (this week)

- [x] Migration Checklist v1.2 → PM-ratified May 20 → HOST 360 commitment #1 closed (May 20)
- [x] 360 item 1.3 BYOC vehicle confirmed as PDR-005 + Q6/Q7 ADRs (May 24)
- [x] V1 HOST cycle retired (log merged, branch + worktree gone; May 24)
- [x] CronCreate durability empirical confirmation memo filed (May 20)
- [x] 360 commitments tracker refresh filed (May 20)
- [x] Ship #044 HOST workstream review filed (May 24)
- [x] v0.3 questionnaire draft filed for CIO review (May 27)
