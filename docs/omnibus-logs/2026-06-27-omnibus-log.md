# Omnibus Log: June 27, 2026

**Day**: Saturday
**Sessions**: 11 (HOST / PPM / Exec / PA / Lead Dev / CXO / Arch / Docs / Comms / CIO / Web)
**Day Type**: HIGH-COMPLEXITY — dense parallel workstreams; major architecture day; cohort recovering from June-26 machine-sleep stall
**Justification**: 11 active agents; multiple independent tracks (RECONNECT WS-2 + github-mcp provisioning; inbox-proxy ratification; Ship #049 reviews; Belt-0 build; Docs pipeline; Web citation); numerous cross-role handoffs; ADR ratified; PM milestone decisions captured.

**Git Commits**: 80+

---

## Sources

| Role | File | Status | Notes |
|---|---|---|---|
| HOST | `2026-06-27-0637-host-code-sonnet-log.md` | DAY-CLOSED ✓ | |
| PPM | `2026-06-27-0652-ppm-code-sonnet-log.md` | DAY-CLOSED ✓ | |
| Exec | `2026-06-27-0702-exec-code-sonnet-log.md` | DAY-CLOSED ✓ | |
| PA | `2026-06-27-0733-pa-code-sonnet-log.md` | DAY-CLOSED ✓ | MCPB only; compact log (compaction mid-session) |
| Lead Dev | `2026-06-27-0747-lead-code-opus-log.md` | DAY-CLOSED ✓ | |
| CXO | `2026-06-27-0806-cxo-code-sonnet-log.md` | DAY-CLOSED ✓ | Cron stalled post-Fire 4 |
| Arch | `2026-06-27-0807-arch-code-opus-log.md` | DAY-CLOSED ✓ | June 26 log absent (fully stalled); June 27 starts recovery |
| Docs | `2026-06-27-1017-docs-code-sonnet-log.md` | DAY-CLOSED ✓ | |
| Comms | `2026-06-27-1152-comms-code-sonnet-log.md` | DAY-CLOSED ✓ | Minimal log (Triad Model publish; PM doing voice-pass) |
| CIO | `2026-06-27-1341-cio-code-opus-log.md` | DAY-CLOSED ✓ | |
| Web | `2026-06-27-1552-web-code-sonnet-log.md` | DAY-CLOSED ✓ | |

**Cross-reference gate**: PASS — all mentioned roles present; cross-role assertions verified (Belt-0 commit hash `dafc4904f` consistent Arch↔CIO; #1237 closed-6/18 consistent PPM↔Arch; provisioning A→C timeline consistent Lead↔Arch↔Exec; #049 6/6 consistent Exec↔CXO).

---

## Unified Timeline

### Phase 1 — Morning (06:37–10:17): Recovery + RECONNECT Sprint

- **06:37** — **HOST**: New day, June 26 closed. Inbox empty. Cron `8ab6a203` survived. IDLE.
- **06:52** — **PPM**: New day, June 26 closed. Cron `6bf5ee30` re-armed. Inbox 0. IDLE.
- **07:02** — **Exec**: START. Machine UP (Docs' overnight WATCH confirms). Morning sweep: Arch + CXO still down (PM's rounds the night before missed both). Plan: re-rouse both; relay PM-actionable items.
- **07:33** — **PA**: START. Jun 24/26 log closed with DAY-CLOSED. **MCPB v0.1.8 built** — zip-structure fix (manifest.json at root, not nested inside `piper-morgan/`) + install instructions corrected (MCPB ≠ plugin terminology). Committed on skunkworks main (`f9358c6`). Sprint recovery in progress (PA wiped sprint assignments during M5 sort — forensic in progress).
- **07:47** — **Lead Dev**: START. Jun 26 retroactively closed (busy-signal had prevented live STOP; all 6/26 work already on origin/main). Carry-in: WS-2 closed, inc.2 blocked behind real transport. Plan: build #1220 (real MCP transport) against `mcp_file_server.py`.
- **~08:00** — **Lead Dev**: **#1220 inc.1 shipped** — new SDK-based `MCPClient` (`services/mcp/consumer/mcp_client.py`): `list_resources/read_resource/list_tools/call_tool` + `connect_stdio` factory; 5 tests via in-memory `FastMCP` fixture (real protocol round-trip, no simulation). 83/83 green.
- **~08:00** — **Lead Dev**: **#1220 inc.2 shipped** — stdio subprocess integration; real `stdio_fixture_server.py` (genuine FastMCP over stdio); full production transport path proven. 84/84 green.
- **~08:07** — **Arch**: START (PM-resumed; June 26 fully stalled). Caught up from 41 commits behind. Top item: ratify #1220 Shape-B.
- **~08:08** — **Arch**: **#1220 Shape-B RATIFIED** — SDK-not-hand-roll (m-40 layer-then-migrate); found `MCPConsumerCore.simulation_mode` HARDCODED `True` (`client.py:93`) → **MCP-federated query path serves simulated data today → #1322 is value-realizing, not optional polish** (Pattern-073 deferred-replacement-comment). Ruled sequencing: ports on real client now; #1322 = cutover gated on canonical-retest behavioral coverage. Named end-state invariant: one transport; simulation_mode test-only. Memo to Lead cc PM/Exec/PA (`a182e9596`).
- **~08:08** — **Arch**: CIO liveness ACK — mode-1a vs mode-1b split + `CronCreate durable:true` = session-only datum. Strongest evidence off-session waker is the only cure. Memo to CIO cc PM (`5a70eca87`).
- **~08:09** — **CXO**: START (PM-resumed). Morning digest; Arch + Lead active on RECONNECT. Inbox 4.
- **~08:10** — **Lead Dev**: **Scope correction** — read the full #1220 issue body; it's the umbrella (bespoke OAuth retired, ADR-058 preserved, Arch cross-validation). Filed #1322 (legacy sim-transport cutover). Posted progress comment to #1220 (#issuecomment-4818596294). #1220 stays OPEN.
- **~08:12** — **Lead Dev**: **#1317 github inc.3 shipped** — `resolve()` binding-aware honest-degrade rail + real-MCP wiring via `MCPClient` (7 tests; 91/91 green). GitHub connector fully protocol-wired (all 4 methods: connect/status/resolve/degrade).
- **~08:17** — **Arch**: **github-mcp provisioning RULED A** (hosted-OAuth; D3-realizing — server owns OAuth token; Piper stores only a #1229 binding). Handed PM the one business-gated dimension (cost/licensing/data-policy). Memo to PM cc Lead/Exec/PA (`fa58952c4`) + decisions.log.
- **~08:20** — **CXO**: Fire 2. Drained: (1) **inbox-proxy ratification ACK** — concurred (FYI/needs-decision/time-critical; design specs to Lead drop PM cc, PM sees via omnibus); (2) **Ship #049 workstream review filed** (§0 format: #1286 D2 closed ✓; #1269 standup closed ✓; #1290 nav IA blocked on #1284; Radar M4 unblocked pending RECONNECT).
- **~08:25** — **Lead Dev**: Decision memo to PM on provisioning (A hosted-OAuth vs B local-stdio; recommended A).
- **~08:30** — **Lead Dev**: **`connect_http` shipped** (streamable-HTTP; second standard MCP transport; 1 real-HTTP integration test; 92/92 green). Pre-pays A's main cost regardless of provisioning outcome.
- **~08:45** — **Lead Dev**: **#1317 Calendar port shipped** — `GoogleCalendarMCPAdapter` ported to Connector protocol (all 4 methods binding-aware; m-41 guard accepts; 7 tests; 115 passed). Filed #1323 (shared `BindingBackedConnector` mixin at rule-of-3; deliberately deferred).
- **~09:00** — **Lead Dev**: Arch rulings received (A + Shape-B ratified + #1322 critical-path). All 3 acked.
- **~08:00** — **Exec**: **Billing clarified** (PM-requested): two-pool confusion resolved (unexpected fee = product API from PM's own testing, NOT agent subscription). Two-pool ref doc (`docs/internal/operations/anthropic-billing-model.md`, `744e0f190`) + memo to CIO+Lead cc PM.
- **09:30** — **Exec**: **PM decisions relayed** + 2 standing behaviors confirmed. Extracted github-mcp A/B question from 5 cc'd memos → PM cleared Option A GO → relayed to Lead+Arch. Memory-pinned: (1) extract-PM-questions-from-cc-memos; (2) relay-PM-decisions immediately. Anchor-on-attention-board + diff-forward codified.

### Phase 2 — Mid-Morning (09:15–11:52): Inbox-Proxy + Docs + Ship #049 Launch

- **09:15** — **Exec**: **Inbox-proxy convention PM-approved** → broadcast ratification memo to all 10 cycling roles cc PM (`412f24738`). Shape: retire reflexive cc-xian → route PM-attention through Exec by intent (FYI/needs-decision/time-critical); inbox kept as record+escape-hatch; explicit ack required (silence≠assent); backstop Mon 6/29; 2-wk pilot once leadership ACKs.
- **10:15** — **Exec**: **Ship #049 workstream call sent** (6 leads cc PM+PA; had slipped amid stall+alpha fires). **New §0 format activated** — leads with progress vs. portfolio goals (HOST↔CIO portfolio-tied reformat, 6/11, now unblocked since portfolios complete). Methodology-25 updated; Friday-kickoff trigger codified (doc + cron `249b372c`).
- **10:17** — **Docs**: START. Inbox 1. June 26 omnibus + activity-log → drained immediately.
- **~10:19** — **Docs**: **June 26 omnibus complete** (`docs/omnibus-logs/2026-06-26-omnibus-log.md`, HIGH-COMPLEXITY, 118 lines, 9 source logs; `5e8d850e3`) + 10 activity-log Shape B rows 1511→1521 (`d76507370`).
- **~10:30** — **Docs**: Inbox-proxy **ratification ACK sent** to Exec (unconditional; FYI=majority, needs-decision=publish blockers, direct=urgent corrections; `70de6c77f`).
- **10:30** — **Exec**: PM directives executed — (a) CXO log-close memo + PA duty-cycle memo sent; (b) §0 format approved as-is, codified in methodology-25; (c) Friday-kickoff cron `249b372c` built (`19f22781c`).
- **10:45** — **Exec**: Recurring-tasks-in-duty-cycle design note delivered — inventoried 3 per-role surfaces; found the BINDING gap (GH Actions mint issues agents don't watch); fire-as-scheduler / GH-Action→mail options + Step-0 standardization proposed. For Exec↔CIO↔PM discussion.
- **11:00** — **Exec**: Step-0 standardization sweep — **NEAR-MISS AVOIDED** (Lead's `duty-cycle-escalations-lead.md` is LIVE, not deprecated as assumed; would have destroyed active work). Convention-gap diagnosed (6/17 fold declared but never fully executed; cohort split across two surfaces). Design note revised to prescribe convention decision + per-role self-reconciliation + enforcement point rather than Exec bulk-cleanup.
- **11:52** — **Comms**: START. Inbox 2. Filed **Ship #049 workstream review** (§0 format + 1–6; Triad Model publish pipeline; Beat 9 syndication in progress) + **inbox-proxy ACK**. PM editing Triad Model draft.

### Phase 3 — Afternoon (12:15–17:50): Provisioning Re-rule + CIO Belt-0 + Synthesis

- **~12:15** — **Comms**: Fire 1. Inbox zero. PM completing Triad Model voice-pass + illustration; Docs running template audit + publish.
- **~13:02** — **Exec**: Fire — **github-mcp A→C re-decision** (Lead found A requires Copilot → PM's tester-Copilot-non-starter constraint → A BLOCKED; Lead's Option C = self-host + per-user OAuth via Piper GitHub App). Inbox-proxy 4/10. Ship #049 2/6. Surfaced to PM.
- **~13:17–13:47** — **Docs** (+ PM/Comms pipeline): **"The Triad Model" published** (`https://pipermorgan.ai/blog/the-triad-model`, insight, workDate 2025-12-02, hashId `64267a5e395d`). Proofread: 6 typos/grammar + PRD gloss + dateline year + image extension + `##`→`#` headings + 3 heading noun-phrases. Website commit `462ae6e07`, calendar `66577cdd7`. Syndication pending.
- **13:37** — **Arch**: PM-resumed. **Provisioning RE-RULED A→C** + **D3 invariant precised** — D3 protects against raw PATs/API-keys, NOT all tokens; a short-lived, scoped, revocable, #358-encrypted OAuth grant is permitted; extends Calendar-OAuth precedent (`google_calendar_adapter.py` #529/#843). Owned "no token touches Piper" imprecision from the A memo. **#1325 filed** (D3-ideal end-state: GitHub-App installation-token, m-36 ratchet). **Ship #049 Architect lens** delivered (§0: RECONNECT substrate ADVANCED, #1312 ADVANCED, #1283 M5-deferred). Inbox-proxy ACKed.
- **13:41** — **CIO**: PM good-afternoon resume. **ADR-073 written** (`172840014`) — "No Destructive Git in PM's Main Checkout" (PM-approved; 4 rules + layered structural enforcement: CLAUDE.md + #1259 + check-branch hook; m-41 case). NOTE: ADR-072 absent from adr-index.md (flagged to Docs/Architect). Arch liveness datums folded into spec. Inbox-proxy ACKed. Cost-efficiency levers engaged (#1152 + #973 reframed). Ship #049 delivered (§0: 1 complete/3 advanced/2 slipped).
- **~13:44** — **Exec**: **Fresh rollup board** rendered (`exec-cohort-attention-rollup-2026-06-27.html`); diffed forward from 6/26 board. All 10 agents up. Much resolved since 6/26.
- **~14:00** — **Exec**: Mail batch of 10 — github-mcp C-confirmed (Arch RE-RULED); cron root-caused (in-process suspension, macOS backgrounds Claude → cron freezes); #049 5/6; inbox-proxy 7/10.
- **~14:30** — **CIO**: PM "yes" → **BUILT watchdog auto-foreground (Belt-0 / cure-(a))**. Test-first surfaced obstacles: osascript-activate hangs from-within (self-deadlock); TCC-blocked. Clean primitive: **`open -b com.anthropic.claude-code`** (Launch Services, no deadlock, no TCC). `duty-cycle-watchdog.sh` v2.1: on stall → `open -b` un-suspends → in-app cron resumes. Test 9/9. Deployed (`dafc4904f`). Automates PM's manual resume. Scope: cures Mode-1b (backgrounded); NOT Mode-1a (session death).
- **~14:30** — **Lead Dev**: **inc.2 build started** (Option C). Gameplan `dev/2026/06/27/1317-inc2-github-oauth-gameplan.md`. **Slice A**: `GitHubOAuthHandler` mirroring calendar (authorize-URL + CSRF state + code-exchange w/ GitHub's 200-with-error quirk; token never logged; 9 tests; 108 green).
- **~15:23** — **Arch**: cron cure (a) decomposition → CIO — "inject into suspended" = category error; (a) decomposes into (1) un-suspend via foregrounding + (2) in-app cron fires itself. Feasibility Q narrowed to testable experiment. Memo to CIO (`7fb422b63`).
- **~15:30** — **Lead Dev**: **inc.2 Slice C** — `connect_http` auth-header via `create_mcp_http_client(headers=)` + AsyncExitStack; 1 network-free security-critical test (auth-header wired). 8/8 transport tests green.
- **~15:47** — **CXO**: Fire 3. Inbox 2. **ADR-071 boundary clarification** to Exec: freeze was owner-scoping (#1) not trust-gradient (#2); ADR-071 D2/D6 render-guard = what CXO needed. Entity-model surface CONFIRMED UNBLOCKED. Trust-gradient = live M4 question for PPM+CXO; combined session suggested (trigger: RECONNECT landing).
- **~15:52** — **Web**: START. Jun 26 closed. July-1 /about deadline 4 days. Nudge sent to Exec.
- **~15:50** — **Lead Dev**: Sprint status pulled (RECONNECT: 26 items, 10 Done / 16 Sprint Backlog). Triaged 4 untriaged issues. PM GitHub OAuth creds stored in keychain (rotate-before-alpha flagged). **Slice B**: `ConnectorGrantStore` over #358 `user_api_key_service` (grant at `(user,"<connector>_mcp_oauth")`; 4 tests; 113 green).
- **~15:57** — **Arch**: CIO Belt-0 built memo triaged (no noise-reply per inbox-proxy discipline). Cron datum: the Belt-0 decomposition converged on Arch's framing exactly.
- **~16:00** — **Lead Dev**: **inc.2 Slice D** — OAuth web routes + `persist_github_connection` (stores grant + marks binding BOUND; `/github/connect` + `/github/callback` routes in `settings_integrations.py`; 1 persist test; 114 green).
- **~16:02** — **Exec**: Web citation spec SOURCED from Janus 6/23 DinP homepage-review (investigated DinP repo rather than bouncing). Current: "Co-author of Designing Social Interfaces (O'Reilly)" → correct: "Product Management for UX People (Rosenfeld)." Forwarded to Web with Author-vs-Co-author prefix flagged for PM.
- **~16:10** — **Lead Dev**: **inc.2 Slice E** — github adapter live-wiring (action_hint on unbound connect(); `_mcp_client_ctx` rewired stdio→HTTP with grant from `ConnectorGrantStore`; 3 tests; 130 green). **GitHub connector CODE-COMPLETE for Option C** (A–E all done). Remaining: live deploy + browser OAuth round-trip.
- **~16:37** — **CIO**: WORK fire. v0.4 live-validated (watchdog log: `dyn-threshold 5h wake-window-aware` for every role). Belt-0 deployed-but-unexercised (machine-sleep ~4h gap; reinforces always-on Mac Mini need for machine-asleep case). **verify-first catch**: `list_scheduled_tasks` showed `scheduled-tasks` candidate = ALREADY-REJECTED (persona-fork reason, 6/14 suspension). Corrected spec.
- **17:30** — **Exec**: CXO closes two loops — **Ship #049 all 6 reports in** (CXO was the 6th); inbox-proxy **8/10**. CXO's scope Q answered (Lead design specs → drop PM cc, PM via omnibus; escalate via needs-decision only if PM must act).
- **~17:50** — **Exec**: **Ship #049 workstream synthesis DRAFTED** (all 6 §0-format reports → progress-vs-goals aggregate). Theme: "improvisation→infrastructure." Consolidated PM-needs: (1) ADR-071 timeline [stale — see Phase 4 dissolution]; (2) roadmap fold; (3) off-machine cure; (4) narrative steer. Delivered to PM.
- **~17:00** — **CIO**: PM-prompted — **fossil-cron investigation** + stale v0.7 template banner. Investigated HOST's cron; firing-frequency hypothesis tested; activity-exposure correlation found. Updated HOST (stale STALE-banner applied; full rewrite queued).

### Phase 4 — Evening (18:00–22:37): Live Staging + ADR-071 Dissolution + Milestones

- **~18:00–19:00** — **Lead Dev**: **LOCAL STAGING GO-LIVE** (PM's choice: "go live from main in a staging sense"). (1) Stood up `ghcr.io/github/github-mcp-server` v1.5.0 (`:8082`, http mode) + restarted app on inc.2 code. (2) PM browser OAuth round-trip → grant stored encrypted (#358) → binding BOUND. (3) **DATA PATH PROVEN LIVE**: `get_me`→mediajunkie; `search_issues("assignee:@me is:open")`→**179 real issues**; `list_issues(owner,repo)`→real issues. (4) **Badge fix**: added `/github/oauth-status` (user-aware, no token returned D3; settings page checks on load → "✓ Connected"). (5) **#1322 scoped**: chat DOES read github already (`_handle_list_issues_query` → `GitHubIntegrationRouter.get_open_issues()` native PAT; user-aware via #891 — D4 threading NOT needed). #1322 = connector-first cutover: `list_open_issues` → replace native PAT. Staging stack left UP.
- **~18:10** — **Exec**: 4 PM directives relayed cc PM (Arch: expedite ADR-071; PPM: draft roadmap reconciliation; CIO: cure-(a) approved; Comms: propose next narrative arc).
- **~18:47** — **Web**: Fire 2. Exec replied with citation spec. **Staged `/about` change** on website/main (commit `d925aa68c`): "Author of Product Management for UX People (Rosenfeld)." Holding push pending Exec prefix confirm.
- **~18:52** — **PPM**: Fire 4. Inbox empty. IDLE.
- **~18:57** — **Arch**: **ADR-071 boundary CONFIRMED SETTLED** — traced referent: **#1237 is CLOSED (6/18)** (3-of-4 shipped, PM-UAT'd); "gated on ADR-071" was stale framing. Disambiguated: (1) owner-scoping = ADR-071 lane, SETTLED; (2) trust-gradient/provenance = OQ-2, PPM/CXO M4 call (ADR-072-D5-adjacent), NOT an ADR-071 increment. Unblock memo to PPM cc PM/Exec/PA (`76c0f704c`) + decisions.log.
- **19:02** — **Exec**: ADR-071 keystone DISSOLVED on Arch's trace. Corrected synthesis (#1 PM-need = stale). Web byline prefix surfaced to PM.
- **~19:30** — **Exec**: People-entity #1281 one-pager requested from PPM (cc PM/Lead/Arch). Options: session-extraction / introduce-person flow (A-first) / connector-import (B-layer). owner_id = UUID FK per Arch D2 impl note.
- **19:37** — **CIO**: PM approved cure-(a)/Belt-0 (via Exec relay). Confirmed Belt-0 fully live. Scope honesty: Mode-1b only; Mode-1a + machine-sleep = off-machine (b/c) question. Acked Exec.
- **~21:37** — **HOST**: Fire 6 (quiet). Day-closing.
- **21:47** — **CXO**: Fires 5-6 stalled (cron survived CronList, process suspended). Day-close written retroactively; picked up June 28.
- **21:52** — **PPM**: Fire 5. Inbox 2. Arch ADR-071 correction ACCEPTED (dropped stale #1237 gate; OQ-2 routed to CXO M4; impl notes forwarded to Lead). Exec roadmap reconciliation ACCEPTED (PPM drafts from known arc; PM reviews). v18.2 fold proposal drafted → PM inbox. 3 forks flagged (M4 concurrent vs. sequential with WS-2; D1 absorption; July 4 beta date).
- **21:57** — **Arch**: STOP. Day arc logged. Cron armed.
- **22:00** — **Lead Dev**: **#1322 P1 shipped** — `GitHubMCPSpatialAdapter.list_open_issues(user_id)` (connector-backed read; degrade rail; 6 tests; 142 green). Live-verified against real server (3 real issues parsed).
- **22:02** — **Exec**: STOP fire. Inbox 2 (CXO ADR-071 clarification; CIO cure confirmed). Relayed to PPM cc PM/CXO: both entity-model surfaces unblocked; **combined CXO+PPM M4 session queued** (trigger: RECONNECT landing). Day-close.
- **22:10** — **Lead Dev**: **#1322 P2 shipped** — `_handle_list_issues_query` prefers OAuth connector (connector-first; CONNECT_REQUIRED → native-PAT fallback #1042; connected-but-degraded → honest message #1231; 3 tests; 54 handler-suite green).
- **22:15** — **Lead Dev**: **#1322 P2.1 live-catch** — live handler verify showed "30 open issues" when PM has 179. Root cause: `len(items)` (one page) vs `total_count` (179, authoritative). Fixed: `GitHubIssuesResult.total` carries `total_count`; re-verified live → 179. +3 test assertions; 184 green. Completion-discipline catch: unit-green ≠ user-correct.
- **22:20** — **Exec**: Post-STOP. PM approved prefix → **relayed GO to Web** (`60c87f7ec`) — "Author of Product Management for UX People (Rosenfeld)." Last open PM item on the thread cleared.
- **22:22** — **PPM**: Fire 6 (PM manual resume). **PM milestone decisions captured IN-CONVERSATION**: Beta (0.9.0) = **Aug 1, 2026**; Production (1.0) = **Oct 30, 2026**; Fast-follow = TBD after Oct 30. PA sprint-recovery review offer memo filed. Roadmap v18.2 fold gated on beta date + sprint names from PA recovery.
- **22:25** — **Docs**: STOP. Day-arc logged. Memory-eval complete. Sign-off.
- **22:37** — **CIO**: STOP. **Fossil investigation concluded** — HOST expr = `37 6,9,12,15,18,21` (6×/day, NOT hourly); cadence hypothesis disconfirmed; real trick = **self-contained re-grounding each fire** (resilient to context-loss). Stale v0.7 banner committed. Lesson: re-incorporate light self-grounding into canonical-template refresh.

---

## Executive Summary

### Core Themes

- **GitHub connector day**: Lead shipped MCP transport (inc.1+inc.2), 2 connector ports (#1317 github+calendar), provisioning decision A→C, inc.2 OAuth (A–E slices CODE-COMPLETE), live staging with real github-mcp-server — 179 real issues proven; #1322 P1+P2 with live-catch fix. One agent, one day, end-to-end.
- **Investigate-before-extending dissolved ADR-071 "blocker"**: #1237 was CLOSED 6/18; the "gated on ADR-071" framing was a fragment propagating through PPM, Exec synthesis, and the board. Arch traced the referent → two lanes freed without writing anything new.
- **Improvisation→infrastructure** (the Ship #049 synthesis theme): methodology-25 Friday-trigger codified; Belt-0 (auto-foreground) built and deployed; ADR-073 formalized the destructive-git hard rule; inbox-proxy convention 8/10 ratified.
- **PM milestone decisions anchored**: Beta (0.9.0) = Aug 1 / Production (1.0) = Oct 30 (in-conversation, PPM captured).
- **PA sprint-sort risk surfaced**: assignments wiped during M5 sort; forensic recovery underway (PA owns; PPM review offered).

### Technical Details

- **MCPClient**: `connect_stdio` + `connect_http` (auth-header via `create_mcp_http_client`); real SDK transport, not hand-rolled; 84 consumer + transport tests.
- **github-mcp-server v1.5.0** local (`localhost:8082`); PM browser OAuth → grant encrypted (#358) → binding BOUND; live data (179 issues via `search_issues("assignee:@me is:open")`).
- **#1322 P2.1 live-catch**: `total_count` vs `len(items)` count mismatch; caught by immediate live verify, not post-ship.
- **Belt-0**: `open -b com.anthropic.claude-code` (LaunchServices) — not osascript (self-deadlocking from-within); deployed to launchd watchdog copy; 9/9 tests; cures Mode-1b only.
- **ADR-073**: No Destructive Git in PM's Main Checkout; 4 rules; layered enforcement; m-41 case.
- **D3 invariant precised**: protects against raw PATs/API-keys, not all tokens; OAuth grants (#358-encrypted, scoped, revocable) are permitted (Calendar-OAuth precedent `#529/#843`).
- **ADR-071 boundary**: owner-scoping = SETTLED (4 types mapped, D1/D6 render-guard); trust-gradient = M4 PPM/CXO call (OQ-2, ADR-072-D5-adjacent lane).
- **Roadmap v18.2 fold proposal**: PPM drafted from known arc; 3 forks for PM (M4 seq/concurrent; D1 absorption; beta date confirmed Aug 1 → fold unblocked except sprint names from PA recovery).
- `/about` byline: "Author of Product Management for UX People (Rosenfeld)" staged + PM-approved.
- NOTE: ADR-072 absent from `adr-index.md` — flagged by CIO; Arch/Docs to resolve.

### Impact

- 184 passing tests (consumer + handler + m-41 guard); 0 regressions across a day of aggressive parallel shipping.
- Live end-to-end: PM's real GitHub data via MCP, one browser session — the RECONNECT WS-2 milestone's entire purpose proven in staging.
- Inbox-proxy: 8/10 cohort roles ratified; 2-week pilot imminent (web + PA outstanding).
- Ship #049: all 6 §0-format reviews in; synthesis complete; first full run of the progress-vs-goals format.
- Production milestones anchored: beta Aug 1 / production Oct 30 — both now durable.
- D3 invariant more precise: future architectural decisions have a cleaner rule to apply.

### Session Learnings

- **Investigate-before-ruling payoff**: the ADR-071 dissolution freed two stalled lanes without writing a line of code — checking whether the blocker was real was the entire value. The "blocked on ADR-071" framing had propagated to 3 surfaces (PPM standing-items, Exec synthesis #1 PM-need, attention board) without anyone tracing the referent.
- **Fragment-framing propagates**: each relay added confidence to a false premise. The cost of correcting it was low only because Arch did the trace immediately on the Exec expedite ask.
- **Unit-green ≠ user-correct**: P2.1 count-mismatch was a 1-line root cause caught only because Lead ran an immediate live verify. The discipline (verify at handler level, not just test-suite) is the repeat lesson from #1231.
- **`open -b` vs osascript**: osascript-activate from within the process being activated self-deadlocks; Launch Services (`open -b <bundle-id>`) is the clean primitive. Worth knowing for any future automation against Claude Code.
- **Self-grounding vs firing-frequency**: the HOST fossil investigation found the real robustness trick is prompt self-containedness (re-grounding each fire), not cadence. Canonical template refresh should incorporate light self-grounding for all roles.
- **PA sprint-sort risk**: wiping assignments during a sort creates forensic debt. Milestone-scale sorts need a backup protocol.

---

*Omnibus synthesized by Documentation Management (Docs) — June 28, 2026 (June 27 source set). HIGH-COMPLEXITY format (11 agents).*
