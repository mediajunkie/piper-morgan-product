# Canonical Sprint Order — Piper Morgan

**Owner**: PPM  
**Last updated**: 2026-07-04 (PPM — PM ratified Jul 4; Beta Blockers sprint added; MVP milestone = beta gate; milestone dates updated from GitHub; RECONNECT status corrected)  
**Status**: PM-ratified 2026-07-04  
**Purpose**: Single source of truth for sprint sequence. Reference this when "what's the order?" comes up — not roadmap prose.

---

## Beta Release Gate

**Beta (0.9.0) ships when the MVP milestone is complete.** The MVP milestone is the gate — not a calendar date.

The **Beta Blockers sprint** contains the issues that must close before beta. All items in the Beta Blockers sprint stay in the MVP milestone. Everything else currently in the MVP milestone that is not a hard gate moves to the Production milestone and is addressed during the beta period (communicated to beta users as known issues).

---

## Sprint Sequence

### Completed (closed)

| Sprint | Closed | Notes |
|--------|--------|-------|
| M0 — Conversational Glue | Mar 4, 2026 (v0.8.6) | |
| M1 — MVP Foundation | Apr 11, 2026 | |
| M2 — Conscious Floor + Action Handlers | Jun 3, 2026 | |
| M3 — Artifact Persistence | Jun 2026 | |
| RECONNECT WS-1 | Jun 22, 2026 (v0.8.9) | StandupAssembler, connector-protocol, Design D2, security batch |
| D1 — Beta Design Quality | Jun 20, 2026 | #1297 sign-off; #1270 straggler carries to Production |

### Active priority

| Sprint | Status | Lane |
|--------|--------|------|
| **Beta Blockers** | 🎯 ACTIVE PRIORITY | All — no theme; hard gates only |

### Confirmed Beta Blockers sprint (as of Jul 4)

| # | Issue | Why it's a hard gate |
|---|-------|---------------------|
| #1241 | Multi-tenancy: content not anchored to user auth | Cross-user data leakage — cannot ship beta |
| #1304 | CI: security test suite never runs | Can't verify any security fix; main chronically red |
| #1324 | Hardcoded localhost OAuth redirect + alembic.ini dev DB | Slack OAuth breaks in prod; migrations silently fail on deploys |
| #1299 | Alembic in-container migration fails | Migrations connect to wrong host on every deploy |
| #1176 | Server binds 127.0.0.1, not configurable | Unreachable through Docker — beta can't be reached |
| #1261 | No password recovery; login-by-email absent | Beta tester dead end — labeled beta-blocking in issue |
| #1332 | User messages intermittently arrive empty | Active reliability failure, reproducible in UAT |
| #1283 | Action↔handler routing: unregistered action → fabrication | Confident wrong answers with no user signal |
| #1168 | macOS-only pyobjc deps in requirements.txt | pip install fails on Linux; breaks every fresh deploy |
| #1317 (incr. 2) | OAuth redirect-orchestrator + callback | External testers cannot connect their own accounts |
| #1220 | github-mcp-server provisioning decision + write-path credential migration | Provisioning is ops-only (architecture ruled 6/27). Jul 5 finding (Lead Dev, static-trace-confirmed): create_issue/update_issue/add_comment take no user_id and use a single session-baked token from the OLD credential path (manual keychain PAT or shared/system fallback) -- NOT the new per-user grant store the read side uses. A tester connecting via the new #1317inc.2 OAuth flow would have writes silently execute against the wrong (shared/system) credential. Scope now includes migrating the write path onto the grant store, not just the hosting decision. |
| #1279 | GitHubIntegrationRouter has no close() -- per-request aiohttp session leak | Reliability risk under sustained beta traffic (places.py + radar WorkItem source); PM agreed Jul 5 |
| #1285 | BUG: naive/aware datetime subtraction in conversation_manager.transition_state (standup COMPLETE path) | Possible crash in a core beta-facing feature; PM agreed Jul 5 |
| #1105 | LLM keychain integration regression -- settings UI requires re-paste despite working server-side keychain reads | Setup friction for external testers (same shape as #1258); PM: "trying to get to less crude auth" -- part of a broader auth-quality push, not just this one fix |
| #441 | Registration + password reset (Phase 2/3) | Beta sign-up may be broken independently of #1261 |
| #1278 | Host piper-morgan server on Fly.io for beta launch | No hosted server = no external beta testers; PM added Jul 4 |
| #1258 | LAUNCH-ENV: strip inherited Anthropic env vars at server startup | Beta deploy (and any hosted environment) fails if server inherits Claude Code's empty env vars; no auto-fix in place — PM added Jul 4 |
| #358 | SEC-ENCRYPT-ATREST: Implement Encryption at Rest for Sensitive Data | PM: important principle, always has been; low issue number shows how long it's been deferred -- pairs with #1241 multi-tenancy per Arch's flag |
| #1312 | DB<->model schema drift: alembic autogenerate unusable (~111 diffs) | Arch: scary part is a stale duplicate not real complexity -- cheaper than the diff count suggests; PM still wants it done pre-beta |

**Close-calls (PM judgment still open):** #1167 (Docker orchestration — only a gate if orchestration is in beta infra scope). #1312 RESOLVED Jul 4 — PM confirms it's a hard gate (Arch: cheaper than the diff count suggests); moved to confirmed table above.

### Remaining sprint work (non-gate items move to Production milestone)

Items from these sprints that ARE hard gates are already captured in Beta Blockers above. The rest move to Production milestone and are addressed during the beta period.

| Sprint | Disposition |
|--------|-------------|
| RECONNECT WS-2 (architectural migration) | Continues in parallel; connectors work now via PAT/keychain fallback (PM-verified). Full ADR-070 migration is Production-milestone work. #1317 incr. 2 + #1220 moved to Beta Blockers. |
| M3-Quality / M3-Health / M3-Security | Triage: hard-gate items → Beta Blockers; remainder → Production milestone |
| M4 — Trust + Learning | Triage: hard-gate items → Beta Blockers; remainder → Production milestone |
| M5 — Distribution + Polish | Triage: hard-gate items → Beta Blockers; remainder → Production milestone |

### Milestones

| Milestone | Target | Notes |
|-----------|--------|-------|
| **0.9.0 beta** | **TBD — gated on MVP milestone complete** | Aug 1 target not achievable; new date set after Beta Blockers sprint is scoped and Lead Dev gives estimate |
| **1.0 production** | **Oct 30, 2026** | DIST (Desktop distro) + D2 (Release design quality) |
| Fast-follow | **Nov 19, 2026** | From GitHub milestone |
| Dot-release | **Feb 2, 2027** | From GitHub milestone |
| Enterprise | **Jul 4, 2027** | From GitHub milestone |

---

## Notes

- **MVP milestone = beta gate**: Beta (0.9.0) ships when the MVP milestone is clear. The Beta Blockers sprint is the mechanism for making that happen — close the sprint, clear the milestone, ship beta.
- **Non-gate work belongs in Production**: issues that don't block beta move to the Production milestone and are addressed during the beta period. Beta users are informed of known issues.
- **RECONNECT connector status**: GitHub and Calendar connections work now via PAT/keychain fallback (PM-verified). RECONNECT is an architectural migration (shared PAT → per-user OAuth + real MCP server), not a fix for broken connectors. The two beta-blocking items from RECONNECT (#1317 incr. 2 + #1220) are in the Beta Blockers sprint; the full migration is Production work.
- **D1 historical slot**: D1 ran concurrently with RECONNECT and closed June 20. Complete, not a gate for anything.

---

*PPM — 2026-06-28. Updated Jul 3 (WS-2 buildable scope drained, M3-Quality active priority). Updated Jul 4: PM ratified; Beta Blockers sprint added as active priority; MVP milestone = beta gate (explicit); Aug 1 date marked TBD; milestone dates updated from GitHub; RECONNECT connector status corrected; M3/M4/M5 triage disposition noted. Updated Jul 4 (afternoon): #1278 (Fly.io hosting) added to Beta Blockers per PM; MCP distribution cluster (M5) confirmed as Production scope; Beta Blockers sprint created on GitHub project board (Sprint field "Beta Blockers - Hard Gates Only", red, 14 issues); #1258 (LAUNCH-ENV) added per PM; M5 distribution cluster (18 issues) moved to Production milestone. Updated Jul 4 (evening): Arch + CXO beta-scope synthesis processed; #358 (encryption-at-rest) added per PM (paired with #1241 per Arch's flag); #1312 (schema drift) confirmed as hard gate per PM (Arch: cheaper than feared) -- now 16 issues in Beta Blockers sprint. Colleague Test sign-off ritual approved by PM, CXO authorized to implement. MCPB/Skunkworks: PM confirms does not block beta; PA to brief leadership; any Skunkworks-to-production promotion requires full leadership sign-off incl. design. Updated Jul 5: GitHub-write-capability forensic investigation complete (4 agents) -- writes are real/wired today (create/update/close/reopen/comment_issue), NOT unwired as first assumed; #1331 was narrowly about 6 unrecognized create-verbs, now fixed. M4 triage 15/16 executed to Production; #1190 confirmed Production (narrow UX-polish, unrelated to credential routing). Lead Dev confirmed (static trace, no live test needed) writes use the OLD credential path (manual PAT or shared/system fallback), not the new per-user grant store -- #1220 scope expanded to include the write-path migration, not just hosting. Updated Jul 5 (later): M3-Quality triage complete -- 4 issues (#1151, #1175, #1219, #1224) confirmed Production; 3 issues (#1279 aiohttp session leak, #1285 possible standup-path datetime crash, #1105 settings re-paste friction) added to Beta Blockers per PM -- now 19 issues in Beta Blockers sprint. PM's #1105 note: part of a broader push toward less crude auth, not an isolated fix.*
