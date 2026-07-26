# HOST Standing Items — Task List

**Purpose**: HOST's task queue per duty cycle v0.6 (reframed standing-items tracker per Architectural Decision 1).

**Convention**: tasks listed roughly by priority/cadence. Mark `[x]` when complete; `[⏸]` when blocked on external (per recurring-failure memory on deferred-AC). Move to "Closed" section at end-of-day or end-of-week.

**Last refreshed**: 2026-07-25 19:30 PDT (Amber migration, fire 1 — honest staleness pass, no status fabricated)

> ⚠️ **STALENESS BANNER — read before acting on anything below.** This file went **~8 weeks without a refresh** (2026-05-27 → 2026-07-25). Everything dated June is from before the **Jul 19 outage** and the **Jul 25 Amber migration**; several items carry June target dates that **silently lapsed** and were never re-triaged. Sections "Watch surfaces" and "Closed (this week)" are June-era and their *headings* are now lying — "this week" means the week of Jun 5.
>
> **This is the exact trap I wrote into migration-checklist Rule 3** (a stale artifact reads as current), found in my own file the same day. I have flagged status rather than invented it: no item below has been marked done, dead, or de-scoped without evidence. **Treat every unflagged claim as a June-era claim needing verification, not as current status.**
>
> **Owed**: a real re-triage with PM/CIO on which June commitments are still wanted post-migration. Several may simply be overtaken by events — but that is a decision to make explicitly, not by letting them rot.

---

## Active

- [x] **HOST launched on v0.7 worktree-cycle (Model A)** 2026-06-02 22:06 in `claude/host-cycle` — supersedes the "cron HELD / do not register on main" hold (the worktree IS the structural fix that hold was waiting for). Cron-shape decision (intermittent-lane candidate per CIO 6/2 authorization) surfaced to PM at launch.
- [x] **Ship #045 workstream review (HOST lens, May 22–28)** — filed to exec inbox 2026-06-02 (`61ec2050c`). Through-line: worktree-default reversal mid-rollout as structural-fix-not-discipline trust property.
- [x] **v0.3 Agent 360 questionnaire FIELDED** 2026-06-03 (PM greenlight 07:34). Canonical `dev/active/agent-360-questionnaire-v0_3.md`; cover memos delivered to 9-role cohort (Lead/Arch/CIO/Comms/CXO/Docs/Exec/PA/PPM) — commit `234cec6f6`. Web out of scope (no §8 section / no v0.2 baseline). **Responses requested ~Jun 10; synthesis ~Jun 12.**
- [x] ✅ **v0.3 SPEC SHIPPED 2026-07-26** (`2a8199f34`) → `dev/active/dashboard-welfare-criteria-host-v0.3-spec.md`. Normative; supersedes the v0.2 seed. Adds **Criteria G (mechanism liveness — the belt needs its own belt)**, the **⏸ PARKED** liveness state, six render rules, and **F4** (undelivered outbound obligations). Routed with one named ask each: **CIO** accept/redirect G + PARKED (registry `state` field is CIO's call — I did not edit the registry) · **Exec** scope call on F2 + F4 rollup extensions · **Pard** the scheduled `verify-hooks` drumbeat. **Mine, unblocked**: E's coverage-indicator definition + G's per-mechanism verification intervals.
- [ ] 🟡 **Dashboard trust/welfare criteria — HOST owns** (accepted by CIO 6/3, m-39). **Remaining after v0.3**: the two unblocked pieces above, then v0.4 once the three reviews land.
  **Real status, read from the artifact rather than this line**: `dev/active/dashboard-welfare-criteria-host-v0.2-seed.md` — **v0.2 seed complete** (adds Criteria D dashboard-honesty / E consequential-action-accountability / F asymmetric-knowledge; all three v0.1 open questions answered) **with CIO's design markup already integrated async** (CIO reviewed 6/18, HOST responded 6/19). Joint state recorded per criterion; D/Q2/Q3/F/E all have agreed shapes, several reusing `duty-cycle-registry.tsv` + `duty-cycle-freeze-check.sh`. Doc closes *"Ready for v0.3 spec."*
  **So the pairing happened; the v0.3 spec is what's idle.** CIO was to flag when Criteria E approaches implementation.
  ⚠️ **Correction, recorded deliberately**: I first flagged this 🔴 *"heads-up NEVER SENT (7 weeks)"* — reading **this tracker's stale claim** instead of opening the artifact. Wrong by five weeks of work. That is the **"verified something adjacent to the claim"** error I had proposed a methodology rule for *earlier in the same fire*, committed against my own file within the hour. Left visible rather than silently fixed, because the correction is the more useful artifact — and because a tracker that misreports its own item's status is precisely why Rule 3 says read the substrate, not the index.
- [x] **v0.3 responses — FULL SET 9/9 complete 2026-06-04 15:55** (Exec last, after PM restarted its cycle). All welfare-scanned clean. HOST self-response done. **Synthesis BEGUN**: analytical extraction of all 10 voices → `dev/active/agent-360-v0.3-synthesis-working-2026-06-04.md`. Headline: mailbox-bridge/shared-main churn is the dominant convergence (~all 10 roles).
- [ ] 🔴 **TARGET LAPSED (~Jun 12, 6 weeks past).** **v0.3 synthesis memo** (diff-against-baseline → PM + cohort; then PM+HOST decide what to change) — target ~Jun 12. TODO: read 7 v0.2 baselines for §7 diffs; draft memo; PM-collaborative recommendations step. Analytical core durable.
- [ ] 🟡 **STALLED after Target 1 (6/5); "no-rush" framing with no trigger.** **gbrain (garrytan/gbrain) agent-experience deep-dive** — PM-directed scouting; CIO (innovation) + HOST (agent-experience), lens-split confirmed 6/4 (`97fa3aae8`). No-rush, fold into cycles (PM busy w/ demo day). HOST targets: thin-job prompt pattern (lived data — my fat cron prompts), dream-cycle's welfare effect (criterion: legible+reversible vs mutate-in-place), minions↔attention-dashboard observability, trust boundary (remote fail-closed). Note: dream-cycle PoC converges with 360 corpus-staleness finding. Repo default branch is `master`. → produce HOST findings pass → converge w/ CIO into co-signed memo to PM. **Convergence set 6/4** (`df3f39bb4`): my **propose-and-diff criterion adopted as a HARD design constraint on the methodology-dream-cycle pilot** (never mutate corpus in place). Division of labor: thin-job (CIO innovation-mechanics / HOST lived-friction); minions (CIO reads, flags observability overlap to HOST); 360-convergence = demand signal led in joint memo. HOST deep-dive targets: read `src/core/cycle/` for propose-and-diff-vs-mutate, thin-job pattern, minions↔dashboard, trust boundary. **Findings doc**: `dev/active/gbrain-host-agent-experience-findings.md`. **Target 1 done 6/5** (cron-scheduler): thin-job+state-in-files = Cat-1 fix for fat-cron-prompt chore; quiet-hours→held-queue = Cat-2 (legible overnight model, maps to dashboard); idempotency-rule = Cat-1-ish. **Next**: dream-cycle propose-and-diff read (CIO waiting); then trust-boundary, minions.
- [x] **v0.6 duty cycle Day-1 adoption**: substrate up + cron live at `:37`; **Day-1 mutual-assessment memo to CIO FILED** (commit `569c65a7f`, Fire 4 11:55 PDT). Watch items addressed: (a) trust-property-touch — too early to judge / observing / (b) role-health-touch — too early to judge / observing / (c) drift stable ~4 min past :37 across Fires 1-3 / (d) cron-prompt v2 with CIO framing reminders queued for next session-start.
- [x] **Mutual-assessment memo to CIO DISTRIBUTED** 2026-06-03 (`94051d398`) — reframed to current reality (rollout near-complete); folded in Gap-A response (low-freq shape self-wakes, sidesteps re-arm). v0.3 responses arriving: **2/9 in** (CIO, PA) as of 10:07.
- [x] **Day-7 cohort-readiness memo to PM DELIVERED** 2026-06-04 (`23d575cf4`, cc CIO/PA) — off-hold per PM 6/4. Verdict: operationally ready; 2 seams (mailbox-bridge + overnight Gap-B); PM-welfare/dashboard forward item. Recommendation to PM: prioritize the hook-amendment.
- [ ] 🟡 **Gated on Docs — verify it's still live post-migration.** **HOST input on MEM #974 format** (post-data, ~early Jun) — Docs will surface aggregated patterns; HOST evaluates whether 3-bucket format wants trust-relevant enrichment
- [ ] 🔴 **TARGET LAPSED (~Jun 12).** **v0.3 re-benchmark synthesis** (~Jun 12) — diff-against-baseline + tier-3 cross-role convergence findings

- [x] **Ship #046 HOST workstream review (May 29 – Jun 4) DELIVERED** 2026-06-05 (`db99c6978`, exec inbox + CEO CC) — 4 days ahead of the Jun 9 deadline. Authored after reading the full omnibus set (5/29–6/4, all 7 daily logs). Through-line: chapter-2 of the structural-fix arc (migration complete + autonomous flow proven + item-4 overnight gap structurally closed + agent-experience seat load-bearing in design). Prep doc superseded.

## Blocked / waiting on external

> ⚠️ All three below are **June-era** and none has been re-checked since. A blocker that has gone unverified for 8 weeks is not reliably still a blocker — re-check before treating any of these as genuinely waiting.

- [⏸] **CIO review of v0.3 questionnaire draft** — waiting silently OK; fielding ~Jun 1 if no rewrite by then
- [⏸] **PP-004 (Structural-Fix-Instead-of-Discipline-Fix) formal filing** — CIO holding for ≥4 instances before filing (3 confirmed so far); watch for instance #4 from Comms Layers B/C/D or v0.6 cycle pilot
- [⏸] **methodology-35 (Asymmetric Discipline) cite** — confirmed in v0.3 §10.4 cycle-experience module; pending CIO review feedback

## Watch surfaces *(June-era — all three predate the Jul 19 outage; re-scope needed)*

- v0.6 cycle pilot Phase B observations (CIO-led, HOST now also adopter — co-observer)
- Outcomes investigation (PA leads, CIO co-authors; week-of-May-25 start)
- Cohort response to v0.3 fielding (~Jun 1+)

## Closed — week of Jun 5 *(heading said "this week"; it means the week of Jun 5)*

- [x] Migration Checklist v1.2 → PM-ratified May 20 → HOST 360 commitment #1 closed (May 20)
- [x] 360 item 1.3 BYOC vehicle confirmed as PDR-005 + Q6/Q7 ADRs (May 24)
- [x] V1 HOST cycle retired (log merged, branch + worktree gone; May 24)
- [x] CronCreate durability empirical confirmation memo filed (May 20)
- [x] 360 commitments tracker refresh filed (May 20)
- [x] Ship #044 HOST workstream review filed (May 24)
- [x] v0.3 questionnaire draft filed for CIO review (May 27)
