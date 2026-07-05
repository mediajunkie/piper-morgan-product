# Beta Blockers — Source of Truth for Path to Beta

**Owner**: PPM
**Status**: LIVING DOCUMENT — canonical source of truth for what remains between now and beta release (v0.9.0)
**Last updated**: 2026-07-05
**Cross-references**: [sprint-order.md](sprint-order.md) (sprint sequencing across the whole board), [roadmap.md](roadmap/roadmap.md) (strategic plan), GitHub project "Building Piper Morgan" → Sprint field "Beta Blockers - Hard Gates Only"

---

## What this document is

This is the single canonical list of issues that must close before Piper Morgan ships beta. The MVP milestone is the beta gate: **beta ships when every issue on this list is closed** — not on a calendar date. Everything else that was in the MVP milestone but did not meet the hard-gate bar has been moved to the Production milestone, to be addressed during the beta period.

**Maintenance discipline** (per PM, 2026-07-05): when a new issue is discovered between now and beta release, triage it against this document's bar — does it block an external tester from safely and honestly using the product? If yes, add it here (table + GitHub Sprint field). If no, it goes to Production. This document must not drift from the GitHub board; every addition or removal here is a same-session edit to both.

## How we got here

The full open backlog was swept sprint-by-sprint (M3-Quality, M3-Health, M3-Security, M4, M5, RECONNECT — 2026-07-04/05), following a deep forensic investigation into GitHub write-action capability that revealed the roadmap's earlier confidence in an August 1 target rested on assumptions that hadn't been verified bottom-up. That investigation is documented in the PPM session logs for 2026-07-04 and 2026-07-05.

## The 22 issues, organized by epic

### Epic A — Verification foundation (1 issue)
Do this first — it's the prerequisite for trusting every other "done" claim on this list.

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1304 | CI gap: DB-backed security test suite never runs in gating CI | Main is chronically red with no required status checks — no other gate's closure is independently verifiable without this |

### Epic B — Multi-tenancy & data protection (5 issues)
The highest-stakes cluster, per independent Architect and CXO review. Likely the single largest lift in this list.

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1241 | Content not anchored to user auth (multi-tenancy completeness) | Cross-user data leakage — cannot ship beta |
| #358 | Encryption at rest for sensitive data | PM: an important principle, long-deferred (low issue number) |
| #1305 | Encrypt PII-bearing JSON/JSONB structured columns | Sibling scope split from #358 |
| #1306 | Encrypt uploaded file content at rest | Sibling scope split from #358 |
| #542 | Implement actual token revocation on disconnect | A disconnected tester's token must actually stop working |

### Epic C — Connector/OAuth cutover (2 issues)
Already in progress — Lead Dev's current active thread. Continue, don't restart.

| # | Title | Status |
|---|-------|--------|
| #1317 | Per-connector MCP-consumer adapters onto the Connector contract | In Progress |
| #1220 | github-mcp-server provisioning + write-path credential migration | In Progress. Scope expanded 2026-07-05: writes (create/update/close/comment) currently use the old native-PAT/shared-token credential path, not the new per-user grant store the read side uses — a tester connecting via the new OAuth flow would have writes silently misattributed until this migrates too. |

### Epic D — Deploy/hosting portability (5 issues)

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1168 | Linux build portability — macOS-only pyobjc deps in requirements.txt | pip install fails on Linux; breaks every fresh deploy |
| #1176 | Hosted-deploy portability — hardcoded-local assumptions | Unreachable through Docker/hosted deploy |
| #1258 | Strip inherited empty Anthropic env vars at server startup | Any hosted environment inheriting Claude Code's empty key fails every LLM call |
| #1299 | Deploy hardening remainder — alembic env-driven URL + deploy.sh migrate hardening | Migrations fail on hosted deploys |
| #1278 | Host piper-morgan server on Fly.io for beta launch | No hosted server = no external beta testers |

### Epic E — External-tester auth/account lifecycle (3 issues)

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #441 | Registration, password reset, security polish | Beta sign-up may be broken independently of #1261 |
| #1261 | Password recovery + login-identifier clarity | Beta tester dead end without it |
| #1105 | Settings UI requires re-paste despite working server-side keychain reads | Setup friction for new external testers; part of PM's broader push toward less crude auth |

### Epic F — Correctness bugs found in testing (3 issues)
Isolated, well-scoped fixes — good candidates to pick off quickly.

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1279 | GitHubIntegrationRouter has no close() — per-request aiohttp session leak | Reliability risk under sustained beta traffic |
| #1285 | Naive/aware datetime subtraction in conversation_manager.transition_state | Possible crash in a core beta-facing feature (standup) |
| #1332 | User messages intermittently arrive empty to the classifier | Active reliability failure, reproducible in UAT |

### Epic G — Routing/config integrity (3 issues)

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1283 | Action↔handler routing integrity audit | Unregistered action → confident wrong answers, no user signal |
| #1312 | DB↔model schema drift (~111 Alembic diffs) | High migration risk; cheaper to fix than the diff count suggests |
| #1324 | Audit: hardcoded config values that should be env vars | Deploy-portability risk |

**Total: 22 issues across 7 epics.**

## Recommended sequencing

1. **Epic A first** — a verification prerequisite, not just another item. Nothing else's "closed" status means much without it.
2. **Epic C continues in parallel** — already Lead Dev's active thread; don't interrupt momentum.
3. **Epic B is the long pole** — the biggest architectural lift on this list; likely wants a dedicated multi-day block once A is clear.
4. **Epics D and F** are largely isolated, well-scoped fixes — strong candidates for batching, or handing to a coding subagent in parallel, so Lead Dev's own attention concentrates on B and C.
5. **Epics E and G** interleave around the above as bandwidth allows.

## Target date

No fixed date as of 2026-07-05. Sprint-order.md's standing position: a real date gets set once Lead Dev can give a bottom-up estimate against this stabilized 22-issue list — not before.

## Change log

- **2026-07-05**: Document created. 22 issues confirmed across 7 epics, following the 2026-07-04/05 sprint-by-sprint triage (M3-Quality, M3-Health, M3-Security, M4, M5, RECONNECT) and the GitHub-write-capability forensic investigation. Established as the canonical source of truth per PM.
