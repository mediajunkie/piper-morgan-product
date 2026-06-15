# HOST Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds the *genuinely transient* "where am I now" state. Durable owed/queued items also live in the session log; this file is the ephemeral working state the skill reads at START / each fire and rewrites at the end of every substantive fire. See `.claude/skills/duty-cycle-tick/SKILL.md`.

**Launch model + shape**: **Option B ephemeral worktree** (DinP account, post-migration 6/13). Session log: `dev/2026/06/13/2026-06-13-1226-host-code-sonnet-log.md`. **WINDOWED low-frequency** (`37 6,9,12,15,18,21 * * *`, daytime-only, cron ID `47e97385`). Single-surface logging: session log is the ONE log (skill v1.8; cycle log = optional scratch only).

**Last updated**: 2026-06-14 ~21:37 PT (Sun; Fire 2 — role-portfolio RATIFIED, sequencing sent to Exec; BRIEFING-HOST updated)

---

## Current operating state

- **Account**: DinP (xian@designinproduct.com). Model: sonnet-4-6.
- **Worktree**: ephemeral Option B (`claude/trusting-faraday-ec4bba`). `claude/host-cycle` retired 2026-06-13.
- **Cron**: `6d50bde6`, windowed `37 6,9,12,15,18,21 * * *` (re-armed 2026-06-14 START; session-only, Gap-C).
- **Session log today**: `dev/2026/06/14/2026-06-14-1555-host-code-sonnet-log.md`
- **Gap-C cure incoming**: CIO proved `mcp__scheduled-tasks` solves cron-death (June 13). Disk-persistent, survives restarts, fires in main checkout. CIO proposing cohort rollout. HOST should be in first cohort — flag interest to CIO.
- **Migration touch-ups still owed**: thin-prompt proposal still says "Model A" → update to Option B. Low urgency.

## Active with PM (teed, awaiting PM)

- **#1058 template hygiene — RECOMMEND CLOSE, teed to PM.** Trim shipped (`3d16873e8`); Lead + Docs + Arch all converged on close. Deferred items in **#1206**. PM closes with one word.
- **Ship #047 HOST workstream review** — DONE/filed to Exec (`dfd9a25be`).

## PM-blocked / awaiting-PM (gated, do not self-advance)

- **dev/alpha privacy decision**: `dev/alpha/alpha-tester-roster.md` git-tracked but claims "gitignored" (tester PII committed). `dev/alpha/host-alpha-reping-tiering-2026-06-08.md` (Michelle→Tier 2) **held UNCOMMITTED** pending PM's keep-tracked+fix-note vs gitignore+scrub call. Do NOT commit additional tester PII until PM decides.
- **Wire #1178-recurring to cc/assign HOST** (so role-health-check auto-issues route to me, not just PM).
- **Thin-prompt cohort-rollout broadcast nod** (proposal finalized `thin-prompt-cohort-rollout-proposal-2026-06-07.md`; CIO carries mechanics). Also: update proposal's Model A framing → Option B.
- **Role-portfolio framework** — **RATIFIED 2026-06-14** (PM). Cohort self-authoring phase UNBLOCKED. Kickoff sequencing sent to Exec (pilot wave: Lead Dev + CIO first; as-they-land review for pilots; batch for main cohort). Exec drafts kickoff + runs by HOST before broadcast.
- **v0.3 360 — COMPLETE 2026-06-13** (collaborative step done with PM). Decisions: (1) decisions.log reinstated + CLAUDE.md update routed to Arch+Docs; (2) M5/BYOC tracking is fine (PA is assoc PM, project board is authoritative — synthesis diagnosis was off); (3) dev/active cleanup routed to Docs; (4) Lead Dev streamlining = ongoing HOST/CIO thread (automate semi-broken processes, not exempt from coordination).
- **Exec BYO-colleague synthesis Qs 1-3** (three-party trust lens delivered `b3f3254a0`; watch for Exec's synthesis; legibility-of-deputization + resource-consent flagged as beta-architecture to Arch/PPM/CXO).

## In-flight with others (no-rush)

- **BYOC Phase-2 trust lens + welfare layer** (trust-lens delivered 6/13; welfare implications delivered 6/13; catch mechanism decided 6/14: support@pipermorgan.ai). **Welfare-tier model v0.1 DRAFTED** (`dev/active/byoc-welfare-tier-model-v0.1.md`) and sent to PA 6/14. ADR-068 trust-criteria seed: `dev/active/adr068-trust-acceptance-criteria-seed.md` (M4-gated). Watch: experiment results → v0.2; ADR-068 scoping → elaborate seed. People-entity trust-map observations sent to CXO+PPM 6/14 (auditability + BYOC-scale consent provenance).
- **m-41 third instance** accepted by CIO 6/13 (three-altitude framing, force-by-constraint sub-shape, at m-41↔m-36↔Pattern-070 confluence). CIO handling formalization. Acked 6/13.
- **gbrain co-signed memo (CIO+HOST→PM)**: T1 + T2 done. NEXT: trust-boundary (`remote` fail-closed) + minions↔dashboard reads → co-signed memo. Findings: `gbrain-host-agent-experience-findings.md`.
- **Dashboard welfare-criteria v0.2** (m-39, HOST owns; pair w/ CIO): v0.1 + B-bis + B-ter done.

## Active threads (no-PM-block)

- **Lead Dev streamlining** (PM-ratified direction 2026-06-13): automate/streamline semi-broken processes, not exempt Lead from coordination. HOST to develop specific automation targets with CIO. T1 mailbox/shared-main churn already being addressed; identify what remains. No deliverable yet — develop on next substantive cycle.

## Owed (HOST-lane)

- **mail-vs-GH-comments cohort-norm one-liner** (committed to Arch 6/7): "mail = cross-agent signaling layer; GH comments = passive work-artifacts, not signals." Cohort-norm doc + briefing line; coordinate w/ CIO. No-rush.
- **BRIEFING-ESSENTIAL-HOST** — updated 2026-06-14 (operating model, Current Focus, CoS→Exec, footer). ✅ DONE.

## Standing cycle responsibility

- Poll open `sapient-trust` issues (~weekly, 4-week audit cadence): `gh issue list --label sapient-trust --state open`. 2026-06-13 poll: **0 open** (clean). Next poll: ~2026-06-20.

## Watch / trigger-bound

- **Alpha re-ping wave 1**: PM pinging Jake Krajewski + Rebecca Refoy (setup-friction-blocked). On reply: log to human-network, update tester status. Michelle Hertzfeld → Tier 2.
- **BYOC hosted alpha welfare monitoring**: Beatrice is user 1 on `alpha.pipermorgan.ai`. HOST asked PA to surface welfare-tier model (who catches PM-as-catch at alpha scale) as a named success criterion for the phase-2 experiment.
- **Gap-C cure incoming**: `mcp__scheduled-tasks` proved by CIO (June 13). Pending cohort rollout. When CIO broadcasts, HOST should adopt early — eliminates cron-death structural vulnerability without Routines watchdog. Watchdog still useful for liveness detection but no longer the only cure.
- **#1217 collegiality/personhood**: PM confirmed both gaps (6/14). Gap 2: authority-retention ✅. Gap 1: elevated to People-entity relationship-map capability (PA drives rule language; PPM owns entity-model personhood-type field; CXO owns Radar surface). HOST sent two design inputs: auditability + BYOC-scale consent provenance. HOST thread complete; watching for rule-language draft from PA.

## Cron

- **WINDOWED `37 6,9,12,15,18,21 * * *`** (PM-ratified 6/11): daytime-only 06:37–21:37, no overnight. ID `6d50bde6` (re-armed 2026-06-14). Keep-armed-default (Rule 2). Gap-C self-heal re-arms from prompt constants → windowed expr embedded in prompt. **Conversion to `mcp__scheduled-tasks` pending CIO cohort rollout** — will eliminate Gap-C entirely.
