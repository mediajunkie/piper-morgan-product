# Exec Carry-Forward (for migration handoff)

**Authored**: 2026-06-12 ~06:35 AM PT, immediately before account migration to xian@designinproduct.com (Opus 4.8).
**Audience**: the new Exec session (same role, same tooling, fresh account) — treat as "what a same-role colleague covering my desk tomorrow needs to know to resume cleanly."

---

> **NEW-EXEC STATUS (updated 2026-06-12 ~08:35 AM PT, DinP / Opus 4.8):** Handoff received + bootstrapped. New-Exec session log: `dev/2026/06/12/2026-06-12-0639-exec-code-opus-log.md`.
> - **Active cron: `5dd30533`** @ `32 6,9,12,15,18,21 * * *` (windowed; next fire 09:32 PT; auto-expires Jun 19 → re-arm). NOTE the first cron `c9fb1fe8` **silently died ~06:50→08:25 pre-first-fire (Gap-C)** — re-armed via self-heal. If CronList shows zero, re-arm immediately.
> - **Operating model: Option B ephemeral-worktree — RESOLVED, CIO-confirmed canonical (6/12), NO do-over.** Work IN this ephemeral worktree (`…/.claude/worktrees/mystifying-lumiere-8bebd3`) for non-mailbox (session/cycle logs, carry-forward, methodology) → push to main via `git push origin claude/mystifying-lumiere-8bebd3:main`. MAILBOX writes via the main-bridge (`git -C <main-checkout>` on main). Do NOT make the main checkout your working surface (that was old-Exec's variant the migration moved off). Sync each fire: `git fetch origin -q && git merge origin/main` — KNOWN FRICTION: stale MANIFEST.md mods in the worktree can abort the merge; `git checkout -- mailboxes/` to clear (mechanical regen noise) then re-merge.
> - **Ship #047: 4 of 6 lenses in** (arch, cxo, cio, comms — held in exec/inbox as the collecting set); pending PPM + HOST; backstop Tue Jun 16 EOD (floor); publish Wed Jun 17 AM.
> - The rest of this doc (priorities, threads, PM-on-plate) carries forward accurate; full refresh on the next substantive arc.

## 1. Identity + tooling

- **Role**: Chief of Staff (exec-code-opus), Office of the Chief Executive
- **Session log slug**: `exec-code-opus` per CLAUDE.md role table
- **Working surface**: Option B ephemeral-worktree `…/.claude/worktrees/mystifying-lumiere-8bebd3` (CIO-confirmed canonical 6/12). Non-mailbox work IN the worktree → push-to-ref to main; mailbox via the main-bridge. (This session's bootstrap ran main-bridge for everything — old-Exec's variant; corrected to genuine Option B from the 09:32 fire onward.)
- **CWD anchor (main checkout for git ops)**: `/Users/xian/Development/piper-morgan/piper-morgan-product`
- **Git user**: mediajunkie
- **Account**: xian@designinproduct.com (DinP) — re-migration complete; Opus 4.8 (same family as prior Opus 4.7; account move only)

## 2. Top priorities for next 24–72h

1. **Ship #047 workstream-review synthesis pipeline** is in flight. Window Fri Jun 5 – Thu Jun 11; publication target Wed Jun 17 AM; backstop Tue Jun 16 EOD (named explicitly as floor, not target).
   - **Kickoffs distributed 09:32 PT Jun 12** to 6 leads (`e37b957dd`): CXO/Arch/PPM/CIO/HOST/Comms
   - **2 workstream reviews ALREADY FILED in inbox at handoff time** (Arch + CXO) — the operational test of the corrected procedural-deadline-framing pin is producing same-day responses. **Read these on new-session-START.** Files: `workstream-047-arch-2026-06-12.md`, `workstream-047-cxo-2026-06-12.md`.
   - **Pending**: PPM, CIO, HOST, Comms workstream reviews. None overdue yet (kickoffs went out 09:32 today).
   - **Synthesis discipline**: source-set state pacing (`feedback_anchor_on_readiness_not_publish_date`); draft NOW when full set in hand; ESCALATE source-owner if any missing as backstop approaches. Apply both halves of the pin.

2. **Role-portfolio framework + pilot + v0.2 refinement at PM ratification gate** (filed Jun 11 evening). PM is heads-down on OpenLaws this week (per `project_openlaw_product_os_week_2026_06_11`); no rush; surface is at PM's gate for when PM engages. Sequencing post-ratification: HOST pilot already authored; cohort self-authors next; HOST reviews against 5 rules; Exec coordinates draft→ratify. Source: `mailboxes/xian (ceo)/inbox/memo-exec-to-pm-cc-host-portfolio-trust-framework-v0.1-at-ratification-gate-2026-06-11.md` + the Jun 11 supplement memo with the v0.2 3-way-seams refinement and HOST's pilot `docs/briefing/ROLE-PORTFOLIO-HOST.md`.

3. **BYO-colleague synthesis 3 questions still on PM's plate** (filed Jun 9 STOP). Source: `mailboxes/xian (ceo)/inbox/memo-exec-to-pm-cc-braintrust-byo-colleague-synthesis-2026-06-09.md` with PPM lens + 6-lens convergence. Questions for PM: (Q1) M5 loop-defensibility gate explicit or absorbed by M5→v1.1 gap? (Q2) ratify ADR-068-only call? (Q3) HOST's guest-framing as external narrative or internal-only?

4. **Routines watchdog build decision** — newly load-bearing post-Jun 10 dormancy; PM has Gap-B failure-data now. Decision was originally in CIO attention doc Jun 7; surfaced in attention rollups Jun 9 + Jun 10; the Jun 10 dormancy + cohort-wide Jun 11 06:15 diagnostics (CXO independently named it) are the live failure-data PM was missing. Worth re-surfacing with the dormancy-data context.

5. **HOST Agent 360 v0.3 synthesis delivered to PM Jun 11 06:08** — next is PM+HOST "what's worth changing" step. Not Exec-driven; awareness only.

## 3. In-flight threads

- **Ship #047 pipeline**: kickoffs → workstream reviews coming in → synthesis → Comms light review → PM voice-pass → Docs publish. Wed Jun 17 AM target. Apply procedural-deadline framing in any chase memos if Arch/etc lens missing near backstop.

- **Cohort cadence-burn retrospective** — opened post-Jun-10-noon-limit-reset but never started. CIO lane; the sparser cron shape (`32 2,4,9,17,20,23` = 6 fires/day, quiet-hold 10–16) is one data point. CIO might fold into Ship #047 workstream or hold for Ship #048.

- **PA's SendUserFile/preview-pane preview pane Desktop quirk** — confirmed as just SendUserFile + HTML format + caption. PA cleared it Jun 10 ("you already reproduced it; that IS the technique in full"). PM noted preview-pane didn't open via cmd-shift-P on my Jun 10 send — Desktop quirk to investigate IF resurfaced; otherwise the discipline-rule is settled.

- **Lead Dev installed mechanism** for attention-doc reconciliation in the `duty-cycle-tick` skill STOP procedure (Jun 10) — cohort-general; phantom-item failure mode structurally addressed. Should make my future cohort-attention-rollups compile clean across all lanes (the Lead Dev phantom-3 should be fixed; verify on next rollup).

- **Workstream-047 lens for Exec own contribution**: Not asked (Exec doesn't author a workstream-review; Exec synthesizes the six lenses into the Ship). The Exec lane shows up *in* the Ship narrative (operational arcs like the deadline-discipline correction, the role-portfolio framework, the Gap-B dormancy + recovery, the attention-rollup) but Exec doesn't file a separate workstream memo.

## 4. PM-on-plate items (PM ratification gates currently in their inbox)

Listed in priority order:

1. **Role-portfolio framework v0.1 + v0.2 refinement + HOST pilot** (Jun 11 forward + supplement)
2. **BYO-colleague synthesis 3 questions** (Jun 9 synthesis)
3. **Routines watchdog build decision** (Jun 7 CIO lane; standing)

PM is heads-down on OpenLaws this week (per `project_openlaw_product_os_week_2026_06_11`). Cross-pollination via Piper Open debrief AFTER OpenLaws week. No urgency manufacturing.

## 5. Recent learnings + memory pins (the disciplinary tightening of the last 4 days)

The last 4 days produced the most concentrated discipline-correction burst since the role launched. Pins saved (all live in MEMORY.md):

- **`feedback_anchor_on_readiness_not_publish_date`** (Jun 9 paired correction) — synthesis-deliverable pacing anchor is source-set state, not publish date. Both halves: complete → draft NOW; incomplete + deadline near → ESCALATE NOW (don't fold absence as narrative caveat).
- **`feedback_kickoff_deadlines_must_be_framed_procedurally`** (Jun 9 sender-side meta-rule) — kickoff memo framing shapes receiver pacing. PM-preference-leads / backstop-named-as-floor / "every hour earlier returns PM slack" / blocker-protocol-explicit. **First cohort-facing test in progress now** (Ship #047 kickoffs filed 09:32 Jun 12; 2 lenses already in inbox by 17:32 same day).
- **`feedback_batched_quiet_fires_has_gap_b_vulnerability`** (Jun 11) — Jun 10 session-dormancy stranded a batched Fire 4 entry; STOP never fired. Rule: commit cycle-log entries on append, NOT at STOP. Discipline-cost (slightly noisier commits) << silent-failure-cost.
- **`feedback_surface_files_via_senduserfile_not_paths`** (Jun 10, partially corrected) — when the file IS the deliverable, use SendUserFile + HTML + caption. NOT pinned as complete because the PM-preview-pane gap remains unresolved (PA says SendUserFile IS the technique; PM's experience contradicts).

Plus three project pins observed via MEMORY.md side-channel on Jun 11:
- **`feedback_opus_fable_subagent_for_heavy_tasks`** — PA can escalate to Opus/Fable subagents for heavy synthesis.
- **`project_agent_migration_priority_2026_06`** — PA pioneer (Jun 11); Exec next (now); Lead Dev + CIO follow.
- **`project_openlaw_product_os_week_2026_06_11`** — PM's OpenLaws Product OS week; firewall applies; cross-pollination later.

## 6. Mailbox state at handoff

- **Inbox**: 2 items at handoff time
  - `workstream-047-arch-2026-06-12.md` (Architect lens, filed within hours of kickoff)
  - `workstream-047-cxo-2026-06-12.md` (CXO lens, same)
- **Pending lenses** (kickoffs sent, awaiting): PPM, CIO, HOST, Comms
- **Recently drained to read/** (last 48h): PA SendUserFile clarification, Lead Dev attention-doc 3-asks-done, all braintrust contributions, all HOST framework + ack memos, etc.

## 7. Operational gotchas + carries

- **Gap-B / session-dormancy**: cron is session-only. If REPL goes dormant (PM closes laptop, etc.), cron doesn't fire. The Routines watchdog (PM decision pending) is the structural cure. Until then: commit on append, batched entries are at risk if session dies between batch and STOP.
- **SendUserFile preview-pane**: in chat, my SendUserFile delivery has produced download-chips, not preview-pane artifacts. PA says it should produce both. Desktop quirk; investigate IF PM surfaces again. Send with `status=normal` when replying inline; `proactive` when surfacing unprompted (per PA discipline note).
- **Foreign unstaged changes in working tree**: shared-main has other agents' uncommitted edits visible in `git status`. **Never touch them.** Commit only your own files with explicit paths (`git commit -m '...' -- <path>`). No `git add -A`; no wildcards; no directory-level adds.
- **Cron expires after 7 days**: re-arm before that. (Migration will arm fresh in new session.)
- **Sparser cron shape** `32 2,4,9,17,20,23 * * *` = 6 fires/day, quiet-hold during PM's weekday workday 10–16 window. Adopted Jun 9 in response to PM's token-burn lesson. Subject to revision in the cadence-burn retrospective (post-Jun 10 noon limit reset; not yet started).
- **Per-memo commit-and-push norm** for every mail action; mailbox writes commit to main only (hook-enforced).

## 8. Ship #046 publication (just completed)

Ship #046 "The Substrate Delivered" published Wed Jun 10 to blog + LinkedIn. Spine: chapter two of substrate arc (#044 "What Survives" → #045 "The Substrate Pivoted" → #046 "The Substrate Delivered"). Concrete: 10 of 11 roles on duty cycle by Jun 4; three flagship product decisions landed in one Fri–Thu window (roadmap v18 canonical, PDR-005 v1.0 ratification-ready, #683 two-layer DoD canonical) via spec-pipeline at cycle speed; paired-lens convergence as the cohort's autonomous coordination primitive. Published file: `docs/public/comms/drafts/published/weekly-ship-046-draft-2026-06-10.md`.

## 9. Cohort-attention-rollup state

- Most recent rollup: `dev/active/exec-cohort-attention-rollup-2026-06-10.html` (Wed AM at PM request)
- Skill: `.claude/skills/cohort-attention-rollup/SKILL.md` (Exec maintains; handed off from PA Jun 6)
- Lead Dev's attention doc was refreshed Jun 10 + mechanism installed in `duty-cycle-tick` STOP procedure — phantoms should be clean on next compile

## 10. Carry-forward refresh discipline

Per Rule 5 of HOST's role-portfolio trust framework (currently at PM ratification gate): the medium-pace layer should self-refresh via the work cycle. This carry-forward doc should be UPDATED as part of any future migration handoff or end-of-significant-arc moment — don't let it rot. If the doc lags more than ~2 sprints of work, treat as drift.

## 11. The session arc this document caps

This Claude session ran Jun 9 12:03 (post-compact resume) → Jun 12 06:35 (this handoff). The arc: PM corrected me twice on Ship #046 source-set discipline → cohort-wide deadline-communication correction → Ship #046 published clean → BYO-colleague braintrust synthesis with 3 questions to PM → Jun 10 Gap-B session-dormancy + Gap-B pin → PM workstream-reformat proposal → HOST co-design memo same-day end-to-end (framework v0.1 + pilot + v0.2 refinement at PM ratification gate by Jun 11 STOP) → Ship #047 kickoffs with corrected procedural framing filed Jun 12 09:32 → migration handoff Jun 12 06:35.

The disciplinary tightening was sharp but the substrate held. Continuation is the new session's lane.

---

*— Exec, carry-forward authored 2026-06-12 ~06:35 AM PT for the account migration handoff. New session: read this first, then read the 2 inbox workstream reviews, then operate from current state.*
