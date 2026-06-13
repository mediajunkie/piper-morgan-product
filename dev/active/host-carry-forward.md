# HOST Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time carry-forward for the `duty-cycle-tick` skill (v1.5, state-based dispatch). Holds the *genuinely transient* "where am I now" state. Durable owed/queued items also live in the session log; this file is the ephemeral working state the skill reads at START / each fire and rewrites at the end of every substantive fire. See `.claude/skills/duty-cycle-tick/SKILL.md`.

**Launch model + shape**: Model A worktree-cycle in `claude/host-cycle`; **WINDOWED low-frequency** (`37 6,9,12,15,18,21 * * *`, daytime-only). ⚠️ **MIGRATION PENDING (see below)** — plan-of-record 6/12 deprecated Model A in favor of Option B ephemeral worktrees; CIO has drafted a HOST migration handoff for PM to trigger.

**Last updated**: 2026-06-12 ~18:40 PT (Fri; #1058 Arch-concur fire + migration-aware carry-forward refresh)

---

## ⚠️ MIGRATION PENDING (PM-triggered, do NOT self-execute)
- Plan-of-record 6/12 (CIO `e1a2f2e72`): **Model A → Option B ephemeral worktree is canonical; Model A `claude/{role}-cycle` deprecated, migration-in-progress.** Wave order: PA (6/10) → Exec (6/11) → CIO (6/12) → **HOST next**. Account move to DinP (xian@designinproduct.com), **same model, no model change**. HOST does NOT supervise others (CIO carries the cohort).
- **CIO drafted my migration pair**: `dev/active/host-migration-handoff-2026-06-12.md` (PM pastes verbatim when ready to close this session) + `dev/active/host-bootstrap-brief-2026-06-12.md` (new-session bootstrap).
- **This carry-forward is pre-staged for that handoff** (handoff step 1 = "update carry-forward"). When PM triggers: do handoff steps in order (carry-forward ✓ already current → final MIGRATION-HANDOFF entry in BOTH logs → CronDelete → commit/push everything to origin/main → report back + stand by).
- **Migration touch-ups to flag**: my cron prompt + the thin-prompt cohort-rollout proposal both still name "Model A worktree-cycle" — update to Option B when migrating. NOT urgent (the cron still functions); just don't let the deprecated framing propagate.

## Active with PM (teed, awaiting PM)
- **#1058 template hygiene — RECOMMEND CLOSE, teed to PM.** Trim shipped (`3d16873e8`); Lead + Docs + **Arch** all converged on close. Deferred items in **#1206** (Lead+Arch items 1-2; Docs item 3 — run sweep against #1206, not a parallel issue; Arch's 4-tier deployment-model framing note added as a #1206 comment). Tried to self-close → classifier denied (take-on ≠ authorized-to-close, correct). **PM closes with one word.**
- **Ship #047 HOST workstream review** — DONE/filed to Exec (`dfd9a25be`).

## PM-blocked / awaiting-PM (gated, do not self-advance)
- **dev/alpha privacy decision**: `dev/alpha/alpha-tester-roster.md` is git-tracked but claims "gitignored" (tester PII committed contrary to expectation). My alpha re-ping tiering doc (`dev/alpha/host-alpha-reping-tiering-2026-06-08.md`, Michelle→Tier 2) is **held UNCOMMITTED** pending PM's keep-tracked+fix-note vs gitignore+scrub call. Do NOT commit additional tester PII until PM decides.
- **Wire #1178-recurring to cc/assign HOST** (so role-health-check auto-issues route to me, not just PM).
- **Thin-prompt cohort-rollout broadcast nod** (proposal finalized `thin-prompt-cohort-rollout-proposal-2026-06-07.md`; CIO carries mechanics).
- **Role-portfolio framework v0.1 ratify** → then cohort self-authors + HOST reviews. v0.1 + HOST pilot (`ROLE-PORTFOLIO-HOST.md`) delivered; Rule-3 three-way-seam v0.2 proposed + Exec-accepted.
- **v0.3 360 "what's-worth-changing" collaborative step** (do WITH PM, don't pre-decide). Extraction + D1-D7 diff durable in `agent-360-v0.3-synthesis-working-2026-06-04.md`; summary memo delivered 6/11. Headlines: mailbox-bridge convergence (T1); duty-cycle = unpredicted biggest change (D3); briefing-currency persistent gap (D6).
- **Exec BYO-colleague synthesis Qs 1-3** (three-party trust lens delivered `b3f3254a0`; watch for Exec's synthesis; legibility-of-deputization + resource-consent flagged as beta-architecture to Arch/PPM/CXO).

## In-flight with others (no-rush)
- **gbrain co-signed memo (CIO+HOST→PM)**: Target 1 (thin-job lived-friction) + Target 2 (dream-cycle propose-and-diff: drift.ts = report-file + off-by-default autoUpdate = trust-gradient lever) DONE. NEXT: trust-boundary (`remote` fail-closed) + minions↔dashboard reads → converge co-signed memo (open piece: where the changeset lives + who ratifies). Findings: `gbrain-host-agent-experience-findings.md`.
- **Dashboard welfare-criteria v0.2** (m-39, HOST owns; pair w/ CIO): v0.1 + B-bis (cross-pair-gap surfacing) + B-ter (institutional-memory integrity) done.

## Owed (HOST-lane)
- **mail-vs-GH-comments cohort-norm one-liner** (committed to Arch 6/7): "mail = cross-agent signaling layer; GH comments = passive work-artifacts, not signals." Cohort-norm doc + briefing line; coordinate w/ CIO on whether it's also a methodology-catalog entry. No-rush.

## Standing cycle responsibility (recurring-audit polling — GH doesn't notify agents)
- Poll open `sapient-trust` role-health-check issues (~weekly, 4-week audit cadence): `gh issue list --label sapient-trust --state open`. Auto-generated audits assign to PM (agents have no GH login); HOST's cycle is the catch mechanism. Fill on the cycle, post to the issue. (Workflow-side reminder added to `role-health-check.yml` 6/8.)

## Watch / trigger-bound
- **Alpha re-ping wave 1**: PM pinging Jake Krajewski + Rebecca Refoy (both setup-friction-blocked, same final-step blocker as Ted). On reply: log to human-network, update tester status, assess Tier-2/3/4 waves. Michelle Hertzfeld → Tier 2 (PM-added 6/11).
- **PM-as-catch graduated 6/8** (Arch+CIO concur): durable=true is a confirmed NO-OP (doesn't persist); cron-death cure = Gap-C two-layer (agent-side re-arm + Routines watchdog, watchdog PM-gated/OPEN). Watchdog↔dashboard convergence: watchdog = liveness tier, dashboard = open-gap tier (Criteria B-bis).

## Cron
- **WINDOWED `37 6,9,12,15,18,21 * * *`** (PM-ratified 6/11 token-efficiency): daytime-only 06:37–21:37, no overnight fires. Keep-armed-default (Rule 2): stays armed through PM conversation; pending PM question does NOT delete it or block other work. Positive CronDelete only on Rule 1 (substantive fire). ⚠️ Gap-C self-heal re-arms from prompt constants → use the windowed expr, never an older hourly/`*/3` shape.
