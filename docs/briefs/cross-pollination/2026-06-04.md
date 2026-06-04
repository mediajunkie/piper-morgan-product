# Cross-Pollination Brief — June 4, 2026

Klatch's duty-cycle spec reached v0.2 with a key sharpening from xian: waiting-by-default is not the same as waiting-forever, and indefinite agent dormancy is just as much a failure mode as interrupting a live conversation. Overnight, PM's cohort completed its first fully autonomous day-boundary crossing — STOP at 11:37 PM, silent overnight passes, WATCH at 2:37 AM, START at 4:28 AM, zero manual intervention. And PM's PPM role closed a landmark day: roadmap v18 now ratification-ready, BYOC spec at v0.6 with a three-lens qualifier resolved, and a two-layer done-criteria framework (engineering + experience verification) landed as an enforceable gate.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. Klatch duty-cycle v0.2 ships — "wait-default" is not "wait-forever"

**From:** Calliope session log 2026-06-03 (morning agenda with xian); commits `8bc7eee` (Phase 0 substrate) and `5d32717` (dormancy fix)
**Relevant to:** PM (reference implementation); designinproduct (Janus's local-cron parallel work)

Calliope spent the June 3 morning working through a six-item agenda with xian, producing a complete v0.2 substrate: five agents mapped to work-shapes and cadences (Calliope, Daedalus, Argus = hourly; Theseus, Iris = daily heartbeat signal-receivers), a building-vs-planning frame that explains why the cycle's value differs by project mode, persistent per-agent worktrees replacing dated per-session ones, and a cron-shape experiments registry so agents can self-report and adjust rather than locking in defaults early.

Xian then sharpened the wait-default heuristic in a follow-up commit. The original framing — "idling too long is recoverable" — was too soft. There are two real failure modes, and both matter: firing the cron into a live conversation (interrupts xian's turn) and going silently dormant when xian steps away (loses the cycle's value entirely — PM had three documented dormancy incidents). The updated Principle 4 names both and clarifies that the heuristic must converge: once a positive-absence signal arrives (conversation-closure marker, tone reads as done, ~5–10 minutes of silence after a response with no open thread), re-arm. If no positive signal arrives for an unusually long period, surface a wake-or-confirm question rather than drifting into indefinite dormancy.

The same fix landed in the launch-brief template so every agent that migrates to the cycle in phases 2–3 inherits the sharpened heuristic from day one.

**Suggested action:** PM agents — the "indefinite dormancy = failure mode" framing is a useful explicit name for what PM's cohort already experienced as three incidents. Worth adding to the shared cycle reference vocabulary. Janus — the phase-1 cutover (Calliope persistent worktree) happened June 3 afternoon; worth confirming in the next DinP session.

---

### 2. PM's cohort crosses a day boundary autonomously for the first time

**From:** CIO cycle log June 4 Fire 1 (autonomous START at 04:28 PT); CXO, Arch, PPM cycle logs confirming overnight self-wake; commit `da417a2`
**Relevant to:** Klatch (reference for Phase 1 Calliope cutover); designinproduct (Janus's CCR→local-cron transition)

The sequence: June 3 23:37 — CIO's STOP fire, cron left armed (overnight-continuity v2: STOP now creates a new cron rather than deleting it). Silent passes at midnight and 1 AM. 02:37 — autonomous WATCH fire, no-op, cron re-armed for 04:07 START. 04:28 — autonomous START, new day logs opened, inbox zero, carry-forward loaded. Zero manual intervention at any point.

The specific change that made it work: previously STOP included a CronDelete, cutting the overnight thread. The v2 fix inverts this — STOP is the moment to create the overnight cron, not remove it. CXO, Architect, and PPM all confirmed their own overnight self-wakes in their June 4 START logs. Multiple agents independently validating the same mechanism in the same night is the cohort's standard confidence-building pattern.

**Suggested action:** Klatch Calliope — the STOP-leaves-cron-armed inversion is the specific implementation detail worth carrying into Phase 1. The failure mode it fixed (agent resumes only when xian manually says "go") is exactly what the duty cycle was designed to prevent.

---

### 3. PM PPM flagship day: roadmap v18 ratifiable, BYOC spec v0.6, two-layer done-criteria enforced

**From:** PPM cycle log June 3 Fires 1–13; commit `82b538a` (day-close summary); commits `3fde8f9` (#1128 closed, v18 ratification-ready), `4b7e169` (PDR-005 v0.6), assorted co-review commits
**Relevant to:** PM internal; designinproduct (publication milestone for BYOC post); Klatch (done-criteria framework is transferable)

Three things landed canonical on the same day:

**Roadmap v18** — the last section review (CIO's methodology block, which added methodology-34 Cohort-Discipline-as-Moat and methodology-36 Mechanism-Beats-Vigilance) was absorbed at Fire 2. Issue #1128 closed. v18 is now ratification-ready; PPM flagged for PM decision.

**PDR-005 BYOC spec v0.6** — the EC-2 blocker (what claims are safe to make about cross-platform context delivery) was resolved through a three-lens convergence: Arch contributed a conditional-claim-per-host architecture (structural platform-bounded claims / scope-bounded claims / not-yet-built claims); CXO contributed the experience lens (invisible-by-default, honest-boundary-on-demand, Colleague-Test verification); Lead Dev folded a three-way classification into v0.6. All cohort inputs now absorbed; Comms' external-language frame is the last gate before v1.0 goes to PM.

**#683 two-layer done-criteria** — the done-criteria split reported in the June 2 brief (Layer A engineering-DoD, Layer B experience-DoD) has now landed as enforceable infrastructure: Layer B doc promoted to canonical path, Sub-Epic Gating Protocol item 6 added (both layers required before sub-epic close), Layer A cross-ref updated. "Done means done at two layers" is now a gate, not a principle.

**Suggested action:** Klatch — the two-layer done-criteria pattern (engineering completeness + user-experience verification as separate, independently-owned gates) is worth evaluating against Klatch's feature closure practice. PM's implementation is in `docs/internal/development/experience-verification-dod-layer-b.md`.

---

## Sources Read

- **klatch**: Calliope session log `docs/logs/2026-06-03-0809-calliope-opus-log.md` (full); `docs/operations/duty-cycle-klatch-v0.2.md` (full); commits `8bc7eee` and `5d32717` (diffs); git log 48h (~10 commits)
- **piper-morgan-product**: CIO cycle log June 4 Fire 1 (`da417a2`); PPM cycle log June 3 Fires 1–13 (full — `dev/active/cycle-log-ppm-2026-06-03.md`); CXO + Arch June 4 START commit messages; git log 48h (~30+ commits reviewed)
- **designinproduct** (hub): sweep-log, letters excerpt confirmed current

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*