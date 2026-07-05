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

### Confirmed Beta Blockers sprint

**Canonical source of truth moved to [beta-blockers.md](beta-blockers.md) (2026-07-05).** That document holds the full 22-issue list, organized into 7 epics with rationale and recommended sequencing, and is the living doc PM refers to for "what remains between us and launch." Update it, not a table here, when new issues are triaged in or out.

**Close-calls (PM judgment still open):** #1167 (Docker orchestration — only a gate if orchestration is in beta infra scope).

### Remaining sprint work (non-gate items move to Production milestone)

Items from these sprints that ARE hard gates are already captured in Beta Blockers above. The rest move to Production milestone and are addressed during the beta period.

| Sprint | Disposition |
|--------|-------------|
| RECONNECT — Connector Refactor | **TRIAGE DONE (Jul 5).** 29 of 35 issues already closed (done, retain MVP milestone tag for record only, no action). Of 6 open: all 6 -> Production (#865, #1322, #1323, #1325, #1327, #1340 -- refactor/tech-debt/future-state/explicitly-additive, none fix a regression). #1317 (per-connector MCP adapters) + #1220 (provisioning + write-path migration) remain in Beta Blockers, both In Progress. **Sprint-by-sprint triage cluster (M3-Quality/Health/Security + M4 + M5 + RECONNECT) is now FULLY COMPLETE.**
| M3-Quality / M3-Health / M3-Security | **DONE** (Jul 5). M3-Quality: 4 Production, 3 Beta Blockers. M3-Health: all 9 → Production (PM: fine for Lead Dev to cherry-pick when idle, none block beta). M3-Security: 4 Production (#371, #482, #557, #1203), 3 Beta Blockers (#542, #1305, #1306 -- the latter two are split scope from #358). |
| M4 — Trust + Learning | Triage: hard-gate items → Beta Blockers; remainder → Production milestone |
| M5 — Distribution + Polish | Triage: hard-gate items → Beta Blockers; remainder → Production milestone |

### Milestones

| Milestone | Target | Notes |
|-----------|--------|-------|
| **0.9.0 beta** | **TBD — gated on MVP milestone complete** | Aug 1 target not achievable; new date set after Beta Blockers sprint is scoped and Lead Dev gives estimate |
| **1.0 production** | **Oct 30, 2026** | DIST (Desktop distro) + D2 (Release design quality) |
| **Ongoing** (no target) | — | New Jul 5, 2026: perpetual, parallel-running tracks (FLYWHEEL process-improvement + SKUNK Skunkworks experiments) that have no release-bound completion date -- kept separate from Production so it isn't misrepresented as "done by 1.0" |
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

*PPM — 2026-06-28. Updated Jul 3 (WS-2 buildable scope drained, M3-Quality active priority). Updated Jul 4: PM ratified; Beta Blockers sprint added as active priority; MVP milestone = beta gate (explicit); Aug 1 date marked TBD; milestone dates updated from GitHub; RECONNECT connector status corrected; M3/M4/M5 triage disposition noted. Updated Jul 4 (afternoon): #1278 (Fly.io hosting) added to Beta Blockers per PM; MCP distribution cluster (M5) confirmed as Production scope; Beta Blockers sprint created on GitHub project board (Sprint field "Beta Blockers - Hard Gates Only", red, 14 issues); #1258 (LAUNCH-ENV) added per PM; M5 distribution cluster (18 issues) moved to Production milestone. Updated Jul 4 (evening): Arch + CXO beta-scope synthesis processed; #358 (encryption-at-rest) added per PM (paired with #1241 per Arch's flag); #1312 (schema drift) confirmed as hard gate per PM (Arch: cheaper than feared) -- now 16 issues in Beta Blockers sprint. Colleague Test sign-off ritual approved by PM, CXO authorized to implement. MCPB/Skunkworks: PM confirms does not block beta; PA to brief leadership; any Skunkworks-to-production promotion requires full leadership sign-off incl. design. Updated Jul 5: GitHub-write-capability forensic investigation complete (4 agents) -- writes are real/wired today (create/update/close/reopen/comment_issue), NOT unwired as first assumed; #1331 was narrowly about 6 unrecognized create-verbs, now fixed. M4 triage 15/16 executed to Production; #1190 confirmed Production (narrow UX-polish, unrelated to credential routing). Lead Dev confirmed (static trace, no live test needed) writes use the OLD credential path (manual PAT or shared/system fallback), not the new per-user grant store -- #1220 scope expanded to include the write-path migration, not just hosting. Updated Jul 5 (later): M3-Quality triage complete -- 4 issues (#1151, #1175, #1219, #1224) confirmed Production; 3 issues (#1279 aiohttp session leak, #1285 possible standup-path datetime crash, #1105 settings re-paste friction) added to Beta Blockers per PM -- now 19 issues in Beta Blockers sprint. PM's #1105 note: part of a broader push toward less crude auth, not an isolated fix. Updated Jul 5 (evening): M3-Health triage complete -- all 9 issues (#1001, #1028, #1131, #1138, #1139, #1144, #1287, #1298, #1321) confirmed Production; PM: fine for Lead Dev to cherry-pick when otherwise idle, none block beta. M3-Security triage complete -- #371/#482/#557/#1203 confirmed Production (KMS migration #482 is ops-hardening, not a tester-facing trust property, distinct from the three that ARE gates); #542 (token revocation on disconnect) + #1305/#1306 (split scope from #358) added to Beta Blockers -- now 22 issues in Beta Blockers sprint. M3-Quality/M3-Health/M3-Security triage cluster fully closed. Updated Jul 5 (final): RECONNECT triage complete -- 29/35 issues already closed (no action), 6 open issues all -> Production. **All sprint-by-sprint triage is now complete** (M3-Quality, M3-Health, M3-Security, M4, M5, RECONNECT). Beta Blockers sprint locked at 22 issues pending PM's epic review. Updated Jul 5 (final): Beta Blockers list (22 issues) organized into 7 epics with recommended sequencing, approved by PM and promoted to its own canonical document -- [beta-blockers.md](beta-blockers.md). The confirmed-table section above now points there instead of duplicating it, to avoid the two documents drifting apart. Updated Jul 5 (post-audit): PM-directed milestone-based ground-truth audit (every open MVP issue vs. the Beta Blockers list, not relying on Sprint-field tags) found 16 discrepancies -- root cause was stragglers left behind when M2/M3/D1 closed, plus a whole FLYWHEEL/SKUNK category never in the triage sequence (compounded by a sprint-assignment data-loss incident ~10 days prior). Resolved: 3 -> Beta Blockers (#1216, #1256, #1260; now 25 issues), 4 -> Production (#1167, #1209, #1257, #1284), 9 -> new **Ongoing** milestone (#683 + 6 FLYWHEEL + 2 SKUNK issues). Full detail in beta-blockers.md. Open question flagged, not yet resolved: #1278's stated dependency cites the wrong issue number for credential decoupling (should be #1300, not #1162) -- pending PM's call on whether that's a real beta-blocking dependency.*
