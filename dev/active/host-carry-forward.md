# HOST Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time carry-forward for the `duty-cycle-tick` skill. Holds the *genuinely transient* "where am I now" state. Durable owed/queued items also live in the session log; this file is the ephemeral working state the skill reads at START / each fire and rewrites at the end of every substantive fire. See `.claude/skills/duty-cycle-tick/SKILL.md`.

**Launch model + shape**: **Option B ephemeral worktree** (DinP account, post-migration 6/13). Session log: `dev/2026/06/16/2026-06-16-0637-host-code-sonnet-log.md`. **WINDOWED low-frequency** (`37 6,9,12,15,18,21 * * *`, daytime-only, cron ID `6d50bde6`). Single-surface logging: session log is the ONE log (skill v1.8; cycle log = optional scratch only).

**Last updated**: 2026-06-16 ~09:37 PT (09:37 IDLE fire; inbox clean; sapient-trust 0 open; queue drained)

---

## Current operating state

- **Account**: DinP (xian@designinproduct.com). Model: sonnet-4-6.
- **Worktree**: ephemeral Option B (`claude/trusting-faraday-ec4bba`). `claude/host-cycle` retired 2026-06-13.
- **Cron**: `6d50bde6`, windowed `37 6,9,12,15,18,21 * * *` (re-armed 2026-06-14 START; session-only, Gap-C).
- **Session log today**: `dev/2026/06/16/2026-06-16-0637-host-code-sonnet-log.md`
- **Gap-C cure incoming**: CIO proved `mcp__scheduled-tasks` solves cron-death (June 13). Disk-persistent, survives restarts, fires in main checkout. CIO proposing cohort rollout. HOST should be in first cohort — flag interest to CIO.
- **Migration touch-ups**: thin-prompt proposal Model A → Option B ✅ DONE (fire ~15:37).

## Active with PM (teed, awaiting PM)

- **#1058 template hygiene — RECOMMEND CLOSE, teed to PM.** Trim shipped (`3d16873e8`); Lead + Docs + Arch all converged on close. Deferred items in **#1206**. PM closes with one word.
- **Ship #047 HOST workstream review** — DONE/filed to Exec (`dfd9a25be`).

## PM-blocked / awaiting-PM (gated, do not self-advance)

- **dev/alpha privacy decision**: `dev/alpha/alpha-tester-roster.md` git-tracked but claims "gitignored" (tester PII committed). `dev/alpha/host-alpha-reping-tiering-2026-06-08.md` (Michelle→Tier 2) **held UNCOMMITTED** pending PM's keep-tracked+fix-note vs gitignore+scrub call. Do NOT commit additional tester PII until PM decides.
- **Wire #1178-recurring to cc/assign HOST** (so role-health-check auto-issues route to me, not just PM).
- **Thin-prompt cohort-rollout broadcast nod** (PM nod received June 13; proposal updated June 15 — Model A → Option B, status notes PM-nodded; CIO carries mechanics of cohort broadcast).
- **Role-portfolio framework** — **RATIFIED 2026-06-14** (PM). Framework published `docs/briefing/ROLE-PORTFOLIO-FRAMEWORK.md`; HOST pilot portfolio refreshed `docs/briefing/ROLE-PORTFOLIO-HOST.md`. Exec kickoff BLESSED (June 15); waiting on Lead Dev + CIO pilot portfolios. HOST reviews each within one fire of receipt; batch cohort kickoff after pilots clear.
- **v0.3 360 — COMPLETE 2026-06-13** (collaborative step done with PM). Decisions: (1) decisions.log reinstated + CLAUDE.md update routed to Arch+Docs; (2) M5/BYOC tracking is fine (PA is assoc PM, project board is authoritative — synthesis diagnosis was off); (3) dev/active cleanup routed to Docs; (4) Lead Dev streamlining = ongoing HOST/CIO thread (automate semi-broken processes, not exempt from coordination).
- **Exec BYO-colleague synthesis Qs 1-3** (three-party trust lens delivered `b3f3254a0`; watch for Exec's synthesis; legibility-of-deputization + resource-consent flagged as beta-architecture to Arch/PPM/CXO).

## In-flight with others (no-rush)

- **BYOC Phase-2 trust lens + welfare layer** (trust-lens delivered 6/13; welfare implications delivered 6/13; catch mechanism decided 6/14: support@pipermorgan.ai). **Welfare-tier model v0.1 DRAFTED** (`dev/active/byoc-welfare-tier-model-v0.1.md`) and sent to PA 6/14. ADR-068 trust-criteria seed: `dev/active/adr068-trust-acceptance-criteria-seed.md` (M4-gated). Watch: experiment results → v0.2; ADR-068 scoping → elaborate seed. People-entity trust-map observations sent to CXO+PPM 6/14 (auditability + BYOC-scale consent provenance).
- **m-41 third instance** accepted by CIO 6/13 (three-altitude framing, force-by-constraint sub-shape, at m-41↔m-36↔Pattern-070 confluence). CIO handling formalization. Acked 6/13.
- **gbrain co-signed memo (CIO+HOST→PM)**: HOST T1+T4 synthesis complete (T3+T4 addendum sent to CIO 6/16). Waiting CIO to add innovation lens → co-sign → PM. Findings: `dev/2026/06/10/gbrain-host-agent-experience-findings.md`.
- **Dashboard welfare-criteria v0.2** (m-39, HOST owns; pair w/ CIO): v0.1 + B-bis + B-ter done.

## Active threads (no-PM-block)

- **Lead Dev streamlining** (PM-ratified direction 2026-06-13): Joint recommendation (CIO+HOST) CO-SIGNED and presented to PM (June 15). CIO unblocked on Tier-1 quick wins (`start-server.sh` wrapper + MANIFEST-noise suppression). Note: `scripts/mail-send.sh` already shipped by CIO (Tier-2 bridge wrapper). HOST holds coordination-vs-mechanical line as automation lands.

## Owed (HOST-lane)

- **mail-vs-GH-comments cohort-norm one-liner** — ✅ SENT to Arch+CIO 2026-06-15. Proposed for CLAUDE.md mailbox section. Arch/CIO to add if they agree.
- **BRIEFING-ESSENTIAL-HOST** — updated 2026-06-14. ✅ DONE.
- **ROLE-PORTFOLIO-FRAMEWORK.md + ROLE-PORTFOLIO-HOST.md** — ✅ PUBLISHED 2026-06-15. Framework at `docs/briefing/ROLE-PORTFOLIO-FRAMEWORK.md`; HOST pilot portfolio refreshed (section 2 current, section 4 three-tier seam structure).
- **Exec pilot kickoff** — ✅ BLESSED 2026-06-15. Why-note sent; framework canonical home confirmed. Exec holds send; Lead Dev + CIO to self-author portfolios.
- **Docs close-marker format** — NOTED: from June 15 use `<!-- DAY-CLOSED: 2026-06-15 -->` in session wrap section.

## Standing cycle responsibility

- Poll open `sapient-trust` issues (~weekly, 4-week audit cadence): `gh issue list --label sapient-trust --state open`. 2026-06-13 poll: **0 open** (clean). Next poll: ~2026-06-20.

## Watch / trigger-bound

- **Pilot portfolios (Lead Dev + CIO)**: Exec sent kickoff June 15. **Lead Dev ACK** (June 15): framework clear, no blockers, queuing ROLE-PORTFOLIO-LEAD-DEV.md post-D1, targeting this week. Already has irreducible mandate clarity (data-safety / #1241 / ADR-071). CIO: no receipt yet. When either portfolio lands in HOST's inbox → review within one fire against the 5 rules → respond to Exec with findings.
- **scripts/mail-send.sh shipped** (CIO, June 15): Tier-2 bridge wrapper. HOST to assess coordination texture when live cohort-wide.
- **LD streamlining Tier-1**: CIO building `start-server.sh` wrapper + MANIFEST-noise suppression. HOST watches for any crossing of the coordination-vs-mechanical line.
- **Alpha re-ping wave 1**: PM pinging Jake Krajewski + Rebecca Refoy (setup-friction-blocked). On reply: log to human-network, update tester status. Michelle Hertzfeld → Tier 2.
- **BYOC hosted alpha welfare monitoring**: Beatrice is user 1 on `alpha.pipermorgan.ai`. HOST asked PA to surface welfare-tier model (who catches PM-as-catch at alpha scale) as a named success criterion for the phase-2 experiment.
- **Gap-C cure incoming**: `mcp__scheduled-tasks` proved by CIO (June 13). Pending cohort rollout. When CIO broadcasts, HOST should adopt early.
- **#1217 collegiality/personhood**: HOST thread complete; watching for PA's rule-language draft.

## Cron

- **WINDOWED `37 6,9,12,15,18,21 * * *`** (PM-ratified 6/11): daytime-only 06:37–21:37, no overnight. ID `6d50bde6` (re-armed 2026-06-14). Keep-armed-default (Rule 2). Gap-C self-heal re-arms from prompt constants → windowed expr embedded in prompt. **Conversion to `mcp__scheduled-tasks` pending CIO cohort rollout** — will eliminate Gap-C entirely.
