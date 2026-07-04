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
| #1220 | github-mcp-server provisioning decision | Required for per-user connector flow to work |
| #441 | Registration + password reset (Phase 2/3) | Beta sign-up may be broken independently of #1261 |
| #1278 | Host piper-morgan server on Fly.io for beta launch | No hosted server = no external beta testers; PM added Jul 4 |
| #1258 | LAUNCH-ENV: strip inherited Anthropic env vars at server startup | Beta deploy (and any hosted environment) fails if server inherits Claude Code's empty env vars; no auto-fix in place — PM added Jul 4 |

**Close-calls (PM judgment still open):** #1312 (schema drift — 111 Alembic diffs, high migration risk), #1167 (Docker orchestration — only a gate if orchestration is in beta infra scope).

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

*PPM — 2026-06-28. Updated Jul 3 (WS-2 buildable scope drained, M3-Quality active priority). Updated Jul 4: PM ratified; Beta Blockers sprint added as active priority; MVP milestone = beta gate (explicit); Aug 1 date marked TBD; milestone dates updated from GitHub; RECONNECT connector status corrected; M3/M4/M5 triage disposition noted. Updated Jul 4 (afternoon): #1278 (Fly.io hosting) added to Beta Blockers per PM; MCP distribution cluster (M5) confirmed as Production scope; Beta Blockers sprint created on GitHub project board (Sprint field "Beta Blockers - Hard Gates Only", red, 14 issues); #1258 (LAUNCH-ENV) added per PM; M5 distribution cluster (18 issues) moved to Production milestone.*
