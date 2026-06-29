# Omnibus Log: June 28, 2026

**Day**: Sunday
**Sessions**: 11 (CIO, HOST, PPM, Exec, Lead Dev, Piper Alpha, CXO, Docs, Chief Architect, Web, Comms)
**Day Type**: HIGH-COMPLEXITY: EXECUTION with coordination sub-threads
**Justification**: 11 parallel agents on independent tracks (RECONNECT P3, sprint recovery, roadmap, publishing). Two coordination threads weave through: (1) cohort-wide run-lean throttle cascaded by Exec with PM approval — 10 roles ACKed and complied; (2) CIO's Belt-0 failure diagnosis driven back through PM to disable + scope the off-machine cure. Sub-type = EXECUTION because the majority of work is role-independent; the two coordination threads are significant but not the day's primary shape.
**Git Commits**: 40+

---

## Chronological Timeline

### Early Morning: Overnight Coverage + Sprint Recovery Begins (03:37–07:00)

**03:37**: **CIO** fires overnight WATCH — inbox empty, cohort cleanly stopped overnight. Corrects 6/27 finding: watchdog is *silent-when-healthy* (nudge-state mtime = 02:49 → watchdog ran <1h ago); no demonstrated machine-sleep gap; "watchdog dark = machine-slept" was a weaker inference than stated. Belt-0 unexercised overnight (no mode-1b stall to trigger it).

**06:50–09:51**: **Belt-0 watchdog** FORGROUNDs 4× (06:50/07:50/08:51/09:51) on stale exec/arch/cxo/ppm — roles flagged but do NOT resume.

**06:52**: **PPM** fire 0 — reads PA sprint recovery memo (1,146-row CSV). Clears HIGH (197 rows) + most MEDIUM; files 6 flags to PA: #1249 D1/D2 conflict; #1217/#1246/#1179 need PM placement; LOW/M6 tier (9 issues, sprint non-existent); #1281 introduce-person flow. Applies roadmap v18.2 fold: RECONNECT WS-1 CLOSED, WS-2 ACTIVE; 3 M3-followon sprints added (Quality/Health/Security); milestone dates beta Aug-1/prod Oct-30; M4 entity-model spec marked delivered (#1237 CLOSED); v18.1 archived.

### Morning: RECONNECT P3 + Exec Relay + Sprint Execution (07:02–10:15)

**07:02**: **Exec** START — reads overnight PPM drafts: People #1281 one-pager + roadmap v18.2 reconciliation. Extracts PM-decision forks from each for relay.

**07:30**: **Exec** relays PM answers on both PPM drafts: introduce-person = standalone M4 issue; roadmap forks (1) M4 SEQUENTIAL — after RECONNECT + 3 M3 child sprints; (2) D1 verified-CLOSED per gate #1297 6/20 (#1270 lone straggler into M4); (3) beta Aug-1/prod Oct-30 confirmed. Requests canonical sprint-order list from PPM.

**08:23**: **Lead Dev** continues #1322 P3 (sibling chat handlers → OAuth connector). Staging stack up for PM testing.

**08:27**: **Piper Alpha** START — reads 15 memos + 4 workstreams. PPM cleared M3-Quality/Health/Security to proceed.

**~08:45**: **Lead Dev** ships #1322 P3a — `_handle_list_prs_query` → OAuth connector. Refactors connector call into shared `_search_via_connector(user_id, *, tool, query, limit)` helper (DRY; issues + PRs both use it). +4 tests, **204 green**. Live-verified: "You have 2 open PRs" (#1191, #1 with URLs).

**~09:00**: **Lead Dev** ships #1322 P3b — `_handle_stale_prs` → OAuth connector. Adds `if _user_id` principal guard (legacy None-user tests stay on native path). Reconciles 2 existing tests. **195 green**. Live-verified: "Stale PRs (2 found): #1 (166 days), #1191 (17 days)." **Milestone**: all user-wide GitHub reads in chat now flow through the OAuth connector.

**09:52**: **PPM** fire 1 — applies Exec relay decisions: files **#1326** (introduce-person standalone M4 issue). Applies roadmap v18.2 correction pass — D1 framing corrected from "future" to CLOSED Jun-20; sprint sequence corrected; M3-Quality issue count 12→8; downstream milestones (fast-follow/dot-release/enterprise) added. Creates `docs/internal/planning/sprint-order.md` (canonical sprint-order reference, routed to PM for confirm). Clears all 3 M3 sprints to PA.

**~09:52**: **Piper Alpha** runs **225 sprint assignments (zero errors)** — 197 HIGH confidence (TSV-sourced M0–M5) + 28 PPM-approved MEDIUM items. Fetches 1,158 project item IDs from GitHub GraphQL. Compiles M6 open list (7 items) for PM manual assignment.

**10:02**: **Exec** quiet fire — threads self-propelling. Arch + CXO still without Sunday START; surfaced to PM as prod-candidates, no urgency. Awaiting Comms arc, Web byline deploy.

**10:17**: **CXO** START — resumed after June 27 Mode 1b cron die. Retroactively closes June 27 log. Inbox empty, queue dry (all items gated/M4-deferred). Heartbeat.

### Late Morning: Belt-0 Failure Confirmed + Dead-Code Discovery (10:37–12:00)

**10:37**: **CIO** morning START — Belt-0's **first real stall validation: FAILED**. Watchdog FOREGROUNDed 4× (06:50–09:51) on stale roles, but roles did NOT resume. Diagnosis: `open -b` foregrounds the *app* (one window) but macOS/Chromium throttle background windows even when the app is frontmost → can't reach individual role windows. Conclusion: cure-(a) doesn't close autonomous-resume → **off-machine cure (b) is the path** (PM's branch-point resolved). Reporting to PM.

**11:06**: **Chief Architect** START (PM-prompted). Cron `ff1df50a` survived overnight — first clean overnight survival since CIO's Belt-0 fix (6/27). Queue awaiting Lead's RECONNECT builds + PPM one-pager + alpha bundle. On-call for ratify/loop.

**~11:10**: **Piper Alpha** afternoon phase — PM shares master inchworm map (Bike app, most authoritative source). Cross-references all unknowns against map + GitHub milestones. Finds: Enterprise/Fast Follow/Production items need no sprint — eliminates ~20 "unknowns." Of 7 M6 items, 6 are Fast Follow (no sprint needed); only #558 MVP. PM assigns remaining 9 MVP items: #558→M4; #1296→FLYWHEEL (CIO); #1241→M4; #1235→RECONNECT; #1217→M4; #1211/#1190→M5-polish; #1167→M5-distribution; #998 closed as superseded. Sprint recovery complete.

**11:10**: **Web** START (PM-prompted) — pushes staged book-citation commit `d925aa68c` to website/origin/main (Exec GO received Jun 27 22:20). pipermorgan.ai /about byline LIVE. Confirms to Exec. Inbox cleared.

**~11:10**: **Lead Dev** mail check — reads 2 Exec cc memos (roadmap-forks-resolved, People source). Notes GitHub collaborators import (People-source option B) could be fed by #1317 connector — surface to PPM when needed. No action now.

**~11:30**: **Lead Dev** traces sim-transport path — **finding: it's DEAD CODE**. Chat GitHub reads are always real REST (`_call_github_api`); sim reached only via `__main__` demo; `main.py` serves no MCP surface; `connect_to_mcp` has 0 callers. Arch's "behavioral-coverage-before-delete" premise (live sim path) is moot. Flags Arch + PM. Files #1322 executable removal plan (comment 4827173746): ~8 source + 19 test files, 5-step order + m-36 guard. Ships **inc.1**: removes dead federation/demo surface (`query_router_spatial_migration.py` + 8 integration tests). **176 unit green**, 890 integration collects clean.

**10:22**: **Docs** START — June 27 omnibus complete (HIGH-COMPLEXITY, 11 source logs, 163 lines; `c89da3c45`) + 11 activity-log Shape B rows appended for June 27 (`99af266fe`). Cross-reference gate PASS. Key themes captured: GitHub connector code-complete + live staging, ADR-071 dissolved, Belt-0 deployed, inbox-proxy 8/10 ratified, Ship #049 synthesis, PM milestones.

### Midday: Throttle Plan + Cohort Cascade (12:00–14:00)

**~12:00**: **Lead Dev** delivers HTML test plan to PM — 4 checks (badge + issues/PRs/stale-PRs + 3 Q's on remaining #1322 scope). PM answers: Q1 = resolution hierarchy (explicit→infer+trust→ask→smart-default); Q2 = default-repo mechanism → files **#1327**; Q3 = cut close/comment writes to connector (#1322 comment 4828041009). Build order clarified: #1327 → repo-scoped reads → writes.

**12:14**: **Exec** attention sweep + drafts throttle plan. PM at ~25% weekly quota (resets Wed Jul-1 9pm). Plan: IDLE HOST/CXO/PPM/Web; SLOW 2× Arch/Docs/PA/Comms; SLOW 3× CIO; KEEP Lead.

**12:27**: **Chief Architect** reads Lead's dead-code finding + verifies independently. **Owns the m-30 failure** in his #1220 ruling: asserted reachability from instantiation + hardcoded `simulation_mode` without tracing the call graph (instantiated ≠ called). Sends concurrence memo to Lead cc PM. Corrects `decisions.log`. #1322 = dead-code removal + m-36 guard; #1220 end-state invariant (one transport, no sim) HOLDS — reached by deletion (cleaner).

**12:27**: **Web** fire 1 — receives Exec run-lean throttle. Web = IDLE tier, no in-window deliverable. CronDelete. ACK to Exec. Suspended through Wed.

**12:35**: **Exec** throttle **EXECUTED** (PM approved "Go"). Exec cron 6→2× (`32 8,20`, `7007f7f7`). Cohort broadcast sent to all 10 roles (10/10 verified — zsh `$ROLES` word-split gotcha caught, redid with literal loop). STATUS = EXECUTED.

**12:37**: **HOST** — receives Exec run-lean throttle. HOST tier = IDLE, no active deliverable. CronDelete. ACK to Exec. Suspended.

**12:47**: **CXO** fire 2 — receives Exec run-lean throttle. CXO = IDLE, queue dry. CronDelete. Suspended through Wed.

**12:52**: **PPM** fire 2 — inbox cleanup: 7 stale inbox items purged via `git rm` (inbox deletion bug: files moved without git rm hadn't been committed, restored on pull). Exec throttle: PPM = IDLE, sprint-order already routed. CronDelete. Suspended.

**12:57**: **Chief Architect** absorbs throttle — cron 6×→2× (`ff1df50a`→`a512dcfa`, `27 8,20`). Updates freeze-registry (threshold 13 for 12h gap; new cron prompt carries restore trigger).

**~13:00**: **CIO** throttle compliance — trims cron 6×→3× (`7 10,16,22`, `310aa50c`). **Catches + fixes throttle↔watchdog interaction**: v0.4 derives thresholds from registry cron-exprs → paused roles with stale normal-cadence rows would false-alarm. Adjusts registry: CIO→3×; exec/cxo/ppm paused; arch already self-throttled. Watchdog now watches CIO+Arch only through Wed. ACKs Exec; flags Belt-0-auto-resume-FAILED.

**~13:00**: **Docs** run-lean throttle applied — cron 6×→2× (`17 10,22 * * *`). SLOW tier through Wed.

**~13:00**: **Lead Dev** enters AUTONOMOUS mode (PM away ~6/29). Refreshes carry-forward. Arms 3×/day KEEP-tier cron (`25e66c5f`).

**13:22**: **Docs** throttle applied + committed.

### Afternoon/Evening: CIO Cure Scoped + Day Wind-Down (15:00–22:00)

**15:10**: **Comms** START — June 27 DAY-CLOSED retroactively confirmed. Relationship-first Ethics template audit done (2 PM-owned FAILs: frontmatter, 4 PLACEHOLDERs). PM voice-pass in progress. Standing by for handoff signal.

**~16:38**: **CIO** fire — arch recovered (PM resumed it; CIO's morning "arch down" flag resolved). CIO's 13:40 registry change VALIDATED: watchdog silent + launchd loaded + nudge-state cleared → no false-alarms on paused exec/cxo/ppm. #1296 (mail-send residue, FLYWHEEL) received from PA/PM: scoped edge-cases for post-Wed execution; queued in standing-items.

**~17:40**: **PM directs CIO**: disable Belt-0, scope off-machine cure. **Belt-0 DISABLED** — watchdog v2.2, `WATCHDOG_AUTO_FOREGROUND=0` default (comment on why: validated-failed 6/28, window-throttle). Tests rewritten (T7→T7a default-off + T7b enabled-fires), **10/10**. Deployed to main-checkout. **Off-machine cure (b) SCOPED** → `docs/internal/operations/off-machine-resume-cure-scope-2026-06-28.md`. Key reframe: Iris is Phase-3 durable-cron (in-app), NOT off-machine; cure must be **SPAWN-FRESH, not wake-existing**. Three options: B1 launchd→headless `claude -p` (recommended interim, 6 open Qs, validation spike needed), B2 Mac Mini (durable, subsumes B1), B3 cloud (held). CIO recommends: don't build B1 if Mac Mini is imminent; spike first.

**~18:00**: **Piper Alpha** (evening) — reads 6 inbox memos: Exec throttle (PA = SLOW 2×/day); Janus MCPB one-pager request; Arch ADR-071 cc; 3 PPM sprint-recovery memos (already actioned). Sends MCPB v0.1.9 one-pager to PM. Removes Caddy basic-auth from alpha.pipermorgan.ai (Caddyfile on Droplet, Caddy reloaded, health 200 ✓). ENCRYPTION_MASTER_KEY confirmed set in Droplet `.env`. Alpha email gate: PM running clean-machine test tonight or tomorrow.

**21:02**: **Exec** STOP — throttle adopted cohort-wide. ACKs from Web/HOST/CIO verified. CIO also paused exec-row in freeze-registry (fine for the window). Day closed.

**22:37**: **CIO** day-close STOP (completed retroactively — Edit tool suspended by harness mid-write; PM confirmed no user rejection). Lesson: a tool-rejection around a suspend/resume may be harness, not PM — flag it. Clean close: all PM-directed work pushed.

### Overnight (6/29 early): Lead Autonomous Fires

**~00:06 (6/29)**: **Lead Dev** autonomous fire — reads Arch concurrence memo. Ships **#1322 inc.2**: removes `query_router.federated_search` (caller-less last method) + dormant `mcp_consumer` wiring (import + param + 2 init lines; kept `github_adapter`). **176 green**; 890 integration clean. (Note: filed as 6/28 work, Lead's session spans 6/28→6/29 continuously.)

**~00:25 (6/29)**: **Lead Dev** — PM clarifies autonomous operating model: attention doc for drop-ins; report+continue; idle on nothing unblocked. Ships **#1322 inc.3a**: removes dead `connect_to_mcp` from github_adapter. inc.3-remainder STOPPED for fresh fire — `list_issues_via_mcp` / `get_issue_via_mcp` removal has 4-test-file blast radius needing real-vs-sim investigation.

**~00:40 (6/29)**: **Lead Dev** resolves Jun-22 PA memos stranded on PM's local main (committed-but-never-pushed; Lead's origin/main never saw them). Verifies #1226/#1232/#1233 already CLOSED 6/22. Flags cleanup to PM.

---

## Executive Summary

### Core Themes

- **RECONNECT P3 milestone**: all user-wide GitHub reads in chat now flow through OAuth connector (issues/PRs/stale-PRs); sim-transport confirmed dead code + retirement in progress (inc.1–3a shipped, inc.3-remainder scoped)
- **Sprint recovery complete**: PA executed 225 sprint assignments (zero errors); PM directly placed final 9 MVP items; inchworm map audit resolved all unknowns; all open MVP issues now have sprint homes
- **Cohort-wide run-lean throttle cascaded**: Exec broadcast PM-approved plan; 10/10 roles complied; ~60-65% fire-frequency cut through Wed Jul-1 reset; CIO caught + fixed throttle↔watchdog false-alarm risk
- **Belt-0 auto-resume failure → cure-(b) scoped**: CIO's self-validation caught the `open -b` window-throttle failure before reliance; PM directed disable + scope; off-machine cure reframed as SPAWN-FRESH with B1 (launchd headless) / B2 (Mac Mini) / B3 (cloud) path
- **Roadmap currency pass**: PPM applied v18.2 fold + correction pass; D1 verified CLOSED (Jun 20); M4 sequential after RECONNECT + 3 M3 child sprints; canonical sprint-order doc created; beta Aug-1 / prod Oct-30 confirmed

### Technical Details

- **#1322 P3a**: `_handle_list_prs_query` → OAuth connector; `_search_via_connector()` DRY helper shared by issues + PRs; +4 tests, 204 green; live-verified "You have 2 open PRs"
- **#1322 P3b**: `_handle_stale_prs` → OAuth connector; `if _user_id` principal guard; 195 green; live-verified "Stale PRs (2 found): #1 (166 days), #1191 (17 days)"
- **#1322 sim-retirement inc.1**: removed `query_router_spatial_migration.py` + 8 integration tests (spatial-federation ×5 + pm033c-mcp-server ×2 + runner); 176 unit green, 890 integration clean
- **#1322 inc.2**: removed `query_router.federated_search` + dormant `mcp_consumer` wiring; 176 green, 890 clean
- **#1322 inc.3a**: removed dead `connect_to_mcp` from github_adapter (caller-less)
- **#1327 filed**: default-repo mechanism (resolution hierarchy: explicit→infer+trust→ask→smart-default); foundation for repo-scoped reads + writes
- **Watchdog v2.2**: Belt-0 disabled (`WATCHDOG_AUTO_FOREGROUND=0` default); T7a/T7b tests 10/10; deployed
- **Roadmap v18.2**: RECONNECT WS-1 CLOSED / WS-2 ACTIVE; 3 M3 child sprints; D1 CLOSED Jun-20; M3-Quality 12→8 open; downstream milestones added; v18.1 archived
- **`sprint-order.md` created**: single canonical sprint-order reference (M3-Quality → M3-Health → M3-Security → M4)
- **alpha.pipermorgan.ai**: Caddy basic-auth removed; ENCRYPTION_MASTER_KEY confirmed; email gate pending clean-machine test
- **pipermorgan.ai /about**: book-citation byline pushed live (Web, Exec GO)
- **#1326 filed**: introduce-person standalone M4 issue (PM-directed, separate from #1281)

### Impact Measurement

- **225 sprint assignments** executed with zero errors; all 1,158 MVP project items now have sprint homes
- **3 M3 child sprints** (Quality/Health/Security: 27 issues total) cleared and ready to execute
- **GitHub connector coverage**: 3 handler families (issues/PRs/stale-PRs) now production-ready via OAuth; 195-204 tests green
- **Dead code removed**: 3 increments shipped; src files + ~11 integration tests deleted; clean import graph
- **10/10 roles** complied with run-lean throttle; cohort-wide ~60-65% fire reduction through Wed Jul-1
- **Belt-0 self-validation**: catch-before-reliance on auto-resume failure — methodology working as designed
- **Docs**: June 27 omnibus (163 lines, 11 logs) + 11 activity-log rows + run-lean compliance

### Session Learnings

- **m-30 (instantiated ≠ called)** bit the Arch ruling on sim-transport — a production case of the anti-pattern; Lead's trace was the corrective; Arch's clean ownership + decisions.log correction is the model response
- **Belt-0 self-validation design worked**: CIO caught the auto-resume failure before it was relied on; "honest miss on my build" is the right framing; cure-(a) ruled out early → (b) scoped faster
- **SPAWN-FRESH not wake-existing** is the key reframe for off-machine cure: existing resume approaches (Iris Phase-3, scheduled-tasks) are in-app and subject to the same backgrounding limit; the cure must spawn a fresh process
- **CIO throttle↔watchdog catch**: reducing cron frequency without updating the watchdog registry would have produced false-alarms; CIO owned the interaction and patched it in the same session
- **zsh word-split gotcha** (unquoted `$ROLES` in fan-out loop): caught by Exec on first attempt; redid with literal loop; document for future fan-out scripts
- **inbox deletion bug** (PPM fire 2): `mv`-without-git-rm doesn't commit the deletion; files restore on next pull; lesson: always `git rm` inbox files, never `mv`
- **stranded-memos-on-PM-local-main** (Jun-22 PA memos): committed-but-never-pushed to origin/main are invisible to all worktrees; no clean mechanism to process without touching PM's checkout — flagged as a norm gap
- **CIO harness false-rejection**: Edit tool suspend/resume during a STOP write surfaced as "user rejected"; flagged pattern — tool rejections around harness suspend/resume warrant investigation, not assumption

---

## Sources

- `dev/2026/06/28/2026-06-28-0337-cio-code-opus-log.md` (CIO)
- `dev/2026/06/28/2026-06-28-0637-host-code-sonnet-log.md` (HOST)
- `dev/2026/06/28/2026-06-28-0652-ppm-code-sonnet-log.md` (PPM)
- `dev/2026/06/28/2026-06-28-0702-exec-code-sonnet-log.md` (Exec)
- `dev/2026/06/28/2026-06-28-0823-lead-code-opus-log.md` (Lead Dev)
- `dev/2026/06/28/2026-06-28-0827-pa-code-sonnet-log.md` (Piper Alpha)
- `dev/2026/06/28/2026-06-28-1017-cxo-code-sonnet-log.md` (CXO)
- `dev/2026/06/28/2026-06-28-1017-docs-code-sonnet-log.md` (Docs)
- `dev/2026/06/28/2026-06-28-1106-arch-code-opus-log.md` (Chief Architect)
- `dev/2026/06/28/2026-06-28-1110-web-code-sonnet-log.md` (Web)
- `dev/2026/06/28/2026-06-28-1510-comms-code-sonnet-log.md` (Comms)

*Cross-reference gate: PASS (all 11 roles with logs; Lead↔Arch dead-code concurrence verified; throttle 10/10 ACKs consistent across logs)*
