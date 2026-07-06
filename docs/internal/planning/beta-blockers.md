# Beta Blockers — Source of Truth for Path to Beta

**Owner**: PPM
**Status**: LIVING DOCUMENT — canonical source of truth for what remains between now and beta release (v0.9.0)
**Last updated**: 2026-07-05
**Cross-references**: [sprint-order.md](sprint-order.md) (sprint sequencing across the whole board), [roadmap.md](roadmap/roadmap.md) (strategic plan), GitHub project "Building Piper Morgan" → Sprint field "Beta Blockers - Hard Gates Only"

---

## What this document is

This is the single canonical list of issues that must close before Piper Morgan ships beta. The MVP milestone is the beta gate: **beta ships when every issue on this list is closed** — not on a calendar date. Everything else that was in the MVP milestone but did not meet the hard-gate bar has been moved to the Production milestone, to be addressed during the beta period.

**Maintenance discipline** (per PM, 2026-07-05): when a new issue is discovered between now and beta release, triage it against this document's bar — does it block an external tester from safely and honestly using the product? If yes, add it here (table + GitHub Sprint field + `beta:<epic>` label). If no, it goes to Production. This document must not drift from the GitHub board; every addition or removal here is a same-session edit to all three.

**GitHub labels** (added 2026-07-05): each issue also carries a `beta:<epic-name>` label (`beta:verification`, `beta:multi-tenancy`, `beta:connector-cutover`, `beta:deploy-portability`, `beta:auth-lifecycle`, `beta:correctness-bugs`, `beta:routing-integrity`) so the epic grouping is filterable directly on the GitHub issue tracker/board, not only in this document.

## How we got here

The full open backlog was swept sprint-by-sprint (M3-Quality, M3-Health, M3-Security, M4, M5, RECONNECT — 2026-07-04/05), following a deep forensic investigation into GitHub write-action capability that revealed the roadmap's earlier confidence in an August 1 target rested on assumptions that hadn't been verified bottom-up. That investigation is documented in the PPM session logs for 2026-07-04 and 2026-07-05.

## The 23 open issues, organized by epic

### Epic A — Verification foundation (1 issue)
Do this first — it's the prerequisite for trusting every other "done" claim on this list.

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1304 | CI gap: DB-backed security test suite never runs in gating CI | Main is chronically red with no required status checks — no other gate's closure is independently verifiable without this |

### Epic B — Multi-tenancy & data protection (6 issues)
The highest-stakes cluster, per independent Architect and CXO review. Likely the single largest lift in this list. **Internal sequencing note**: #1260 likely needs to land before or alongside the start of #1241's own remediation work, not in either order -- #1241 can't be properly verified with real multi-user testing until genuine per-user identity (#1260) replaces the current alpha-only fallback.

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1260 | ADR-071 D7 prerequisite: formal PM-identity config replaces alpha username+env fallback | Likely a real prerequisite for #1241 -- the current alpha-only auth fallback isn't genuine multi-user support. Sequence before #1241. |
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

### Epic D — Deploy/hosting portability (3 open issues; 2 closed 2026-07-05)

~~#1168~~ and ~~#1176~~ **closed 2026-07-05** (Lead Dev, Beta Blockers estimate research) — both fixes were already shipped as part of #1299's 2026-06-20 alpha-deploy remediation, but the issues themselves were never separately closed. Verified directly against current `main` before closing (see issue comments for evidence). #1299's own scope also shrank: sub-item (a) verified done, only (b) remains open.

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1258 | Strip inherited empty Anthropic env vars at server startup | Any hosted environment inheriting Claude Code's empty key fails every LLM call |
| #1299 | Deploy hardening remainder — **only (b) remains**: deploy.sh migrate hardening (real-deploy verification + BUILD_FAIL race disambiguation) | Migrations fail on hosted deploys |
| #1278 | Host piper-morgan server on Fly.io for beta launch | No hosted server = no external beta testers |

### Epic E — External-tester auth/account lifecycle (3 issues)

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #441 | Registration, password reset, security polish | Beta sign-up may be broken independently of #1261 |
| #1261 | Password recovery + login-identifier clarity | Beta tester dead end without it |
| #1105 | Settings UI requires re-paste despite working server-side keychain reads | Setup friction for new external testers; part of PM's broader push toward less crude auth |

### Epic F — Correctness bugs found in testing (5 issues)
Mostly isolated, well-scoped fixes — good candidates to pick off quickly. **#1216 scope decision made 2026-07-05 (Lead Dev)**: ship the interim fix for beta — extend the same honest-decline/distrust-prior-claims mechanism that fixed #1331 at the prompt/floor level (small, ~1hr, uses an already-proven pattern) so Piper stops asserting a seed-vs-real distinction it cannot actually verify. The full fix (an `is_seed`/`source` provenance field on `InsightDB` + surfacing logic, ~2-4hrs, a real schema change) is deferred to Production — tracked, not dropped. Rationale: the interim option reliably closes the specific dishonest-claim failure mode using a proven mechanism, without committing beta to a new schema field that every future insight-write path must remember to populate correctly.

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1279 | GitHubIntegrationRouter has no close() — per-request aiohttp session leak | Reliability risk under sustained beta traffic |
| #1285 | Naive/aware datetime subtraction in conversation_manager.transition_state | Possible crash in a core beta-facing feature (standup) |
| #1332 | User messages intermittently arrive empty to the classifier | Active reliability failure, reproducible in UAT |
| #1216 | 'What have you learned about my workstyle' claims a seed-vs-real distinction the system cannot make | Confidently asserts dev-seed placeholder data is real -- same failure shape as #1331's confabulation, which was hard-gated |
| #1256 | INTENT-VOCAB: stakeholder-update query misclassifies as update_document_query | Real classifier bug misrouting a common query type |

### Epic G — Routing/config integrity (3 issues)

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1283 | Action↔handler routing integrity audit | Unregistered action → confident wrong answers, no user signal |
| #1312 | DB↔model schema drift (~111 Alembic diffs) | High migration risk; cheaper to fix than the diff count suggests |
| #1324 | Audit: hardcoded config values that should be env vars | Deploy-portability risk |

**Total: 23 open issues across 7 epics** (25 minus #1168 and #1176, closed 2026-07-05 with evidence — see Epic D and change log).

## Recommended sequencing

1. **Epic A first** — a verification prerequisite, not just another item. Nothing else's "closed" status means much without it.
2. **Epic C continues in parallel** — already Lead Dev's active thread; don't interrupt momentum.
3. **Epic B is the long pole** — the biggest architectural lift on this list; likely wants a dedicated multi-day block once A is clear. Within it, **#1260 before #1241** (see Epic B note).
4. **Epics D and F** are largely isolated, well-scoped fixes — strong candidates for batching, or handing to a coding subagent in parallel, so Lead Dev's own attention concentrates on B and C. **Exception: #1216** (Epic F) needs a scope decision first (full provenance model vs. cheaper interim honest-decline extension) before it can be batched with the rest.
5. **Epics E and G** interleave around the above as bandwidth allows.

## Target date

No fixed date as of 2026-07-05. Sprint-order.md's standing position: a real date gets set once Lead Dev can give a bottom-up estimate against this stabilized 23-issue list — not before. **Lead Dev's bottom-up estimate has since arrived** (memo, 2026-07-05, held in `mailboxes/ppm/inbox/` pending a dedicated processing pass): Epic B is the critical path at 9-16 days; total wall-clock ~3-5 weeks running in parallel via subagents. Full sequencing refinements (Epic D now ~1 day given the two closures below; #441+#1261 proposed as one unit; #1312 proposed to move into Epic B) not yet reflected in the epic tables above — pending review.

## Change log

- **2026-07-05**: Document created. 22 issues confirmed across 7 epics, following the 2026-07-04/05 sprint-by-sprint triage (M3-Quality, M3-Health, M3-Security, M4, M5, RECONNECT) and the GitHub-write-capability forensic investigation. Established as the canonical source of truth per PM.
- **2026-07-05 (later)**: PM-directed audit found 16 open MVP-milestone issues untracked by the sprint-by-sprint sweep -- root cause: some issues carried Sprint-field tags from sprints that had already closed (M2, M3, D1) and were never swept forward, and a whole separate FLYWHEEL/SKUNK category was never in the triage sequence at all (compounded by a sprint-assignment data-loss incident ~10 days prior). Resolved by a milestone-level ground-truth check (every open MVP issue, not just tagged-sprint issues) rather than continued reliance on Sprint field alone. Result: 3 added to Beta Blockers (#1216, #1256, #1260 -- now 25 issues), 4 to Production (#1167, #1209, #1257, #1284), 9 to a newly-created **Ongoing** milestone (#683, #1160, #1162, #1259, #1272, #1275, #1277, #1295, #1296 -- FLYWHEEL/Skunkworks work with no release-bound completion target, kept separate from Production so it isn't misrepresented as "done by 1.0"). Also found and flagged (not yet resolved): #1278's stated dependency on "credential decoupling (#1162)" cites the wrong issue -- the real credential-decoupling work is #1300, currently Production-scoped -- open question on whether that's a real beta-blocking dependency or a stale/overscoped acceptance criterion.
- **2026-07-05 (final)**: #1278's dependency question settled -- verified the actual mechanism (#1185, per-user LLM keys) already shipped; corrected #1278's issue body directly (stale reference + unmet-dependency framing both fixed). **Incident, self-caught and fixed same-day**: the commit message resolving this ("...not yet resolved: #1278...") was parsed by GitHub's naive close-keyword matcher as "resolved #1278" and silently closed the issue -- caught when PM spot-checked the board directly, reopened immediately, and all 25 Beta Blocker issues + all commit messages from both days scanned to confirm no other accidental closures occurred. Lesson: avoid close/fix/resolve wording immediately adjacent to a "#N" reference in commit messages unless the closure is intended, even inside a negated clause -- GitHub's matcher has no concept of negation. Added `beta:<epic>` GitHub labels (7, one per epic) across all 25 issues, and a `post-beta-priority` label on #1340 (PM: high priority for the first Production sprint after beta, since it's the onboarding-polish counterpart to the already-shipped #1185 mechanism).
- **2026-07-05 (Lead Dev estimate research pass)**: #1168 and #1176 closed with evidence — both fixes shipped as part of #1299's 2026-06-20 alpha-deploy remediation but were never separately closed; verified directly against current `main` (independently re-verified by PPM via `gh issue view`, both confirmed CLOSED/COMPLETED). #1299's own scope reduced: sub-item (a) verified done, only (b) — real-deploy migrate verification + BUILD_FAIL race disambiguation — remains open. #1216's flagged scope decision resolved: ship the interim honest-decline fix for beta (reuses the #1331 mechanism, ~1hr), defer the full `is_seed`/`source` provenance field to Production (independently re-verified by PPM via issue comments). **Beta Blockers count: 25 → 23 open.** Lead Dev's full sequencing-refinement + bottom-up-estimate memo received same day; headline numbers noted above under Target date, full incorporation into the epic tables still pending a dedicated processing pass.
