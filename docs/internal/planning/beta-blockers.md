# Beta Blockers — Source of Truth for Path to Beta

**Owner**: PPM
**Status**: LIVING DOCUMENT — canonical source of truth for what remains between now and beta release (v0.9.0)
**Last updated**: 2026-07-07 (Lead Dev correction pass — #1278 reopen reflected; see change log)
**Cross-references**: [sprint-order.md](sprint-order.md) (sprint sequencing across the whole board), [roadmap.md](roadmap/roadmap.md) (strategic plan), GitHub project "Building Piper Morgan" → Sprint field "Beta Blockers - Hard Gates Only"

---

## What this document is

This is the single canonical list of issues that must close before Piper Morgan ships beta. The MVP milestone is the beta gate: **beta ships when every issue on this list is closed** — not on a calendar date. Everything else that was in the MVP milestone but did not meet the hard-gate bar has been moved to the Production milestone, to be addressed during the beta period.

**Maintenance discipline** (per PM, 2026-07-05): when a new issue is discovered between now and beta release, triage it against this document's bar — does it block an external tester from safely and honestly using the product? If yes, add it here (table + GitHub Sprint field + `beta:<epic>` label). If no, it goes to Production. This document must not drift from the GitHub board; every addition or removal here is a same-session edit to all three.

**GitHub labels** (added 2026-07-05): each issue also carries a `beta:<epic-name>` label (`beta:verification`, `beta:multi-tenancy`, `beta:connector-cutover`, `beta:deploy-portability`, `beta:auth-lifecycle`, `beta:correctness-bugs`, `beta:routing-integrity`) so the epic grouping is filterable directly on the GitHub issue tracker/board, not only in this document.

## How we got here

The full open backlog was swept sprint-by-sprint (M3-Quality, M3-Health, M3-Security, M4, M5, RECONNECT — 2026-07-04/05), following a deep forensic investigation into GitHub write-action capability that revealed the roadmap's earlier confidence in an August 1 target rested on assumptions that hadn't been verified bottom-up. That investigation is documented in the PPM session logs for 2026-07-04 and 2026-07-05.

## The 20 open issues, organized by epic

### Epic A — Verification foundation (1 issue, 4/5 done)
Do this first — it's the prerequisite for trusting every other "done" claim on this list.

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1304 | CI gap: DB-backed security test suite never runs in gating CI | Main is chronically red with no required status checks — no other gate's closure is independently verifiable without this |

**#1304 status (corrected 2026-07-06, was mis-stated as closed below)**: 4/5 AC items done and verified — gating job built + proven live with teeth (3 real Actions runs incl. a deliberate canary that failed exactly as expected), 2 real bugs found+fixed along the way (`user_api_key_service.py` UUID/str bug, 5 un-awaited async test methods). **Deliberately left OPEN**: flipping GitHub's required-status-check setting is a repo-wide, hard-to-reverse-without-everyone-noticing change to every agent's push/merge behavior — Lead Dev asked for PM's explicit go/no-go rather than deciding unilaterally. **This is the one remaining item: a PM decision, not more engineering.**

### Epic B — Multi-tenancy & data protection (2 open issues + #358 nearly done; 3 closed total: 2 on 2026-07-05, 1 on 2026-07-06)

~~#1260~~ and ~~#1241~~ **closed 2026-07-05** (Lead Dev). #1260: done same-day (server-owned PM-identity config replaces a hardcoded username). #1241: turned out to be **already complete** — the audit (`dev/2026/06/15/1241-content-anchoring-audit.md`) and its design output (**ADR-071**, ratified 2026-06-15) already satisfied all 5 of the issue's own deliverables, and the downstream remediation had substantially shipped via #1238 (doc store), #1250 (learning toggle), and #1252 (the main D2-D6 consolidation refactor, closed 2026-06-19) — this issue was simply never closed after that work landed. The one genuinely remaining piece (#1257, the deeper 40+-site read-threading + `user_id`→`owner_id` column drop) is already its own separately-tracked issue, correctly milestone-scoped to **Production**, not a beta blocker. See #1241's closing comment for the full evidence trail.

~~#542~~ **closed 2026-07-06** (Lead Dev) — real Slack `auth.revoke` + Google token-revocation calls implemented (both were previously stubs/absent). Found and fixed a real sequencing bug along the way (Slack's revoke was reading tokens that had already been deleted from keychain, so it could never have actually revoked anything).

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #358 | Encryption at rest for sensitive data — **both dimensions code-complete + tested (2026-07-06); dimension B live-verified on alpha 6/25; only dimension A's live-alpha check remains, needs droplet access** | PM: an important principle, long-deferred (low issue number) |
| #1305 | Encrypt PII-bearing JSON/JSONB structured columns | Sibling scope split from #358 |
| #1306 | Encrypt uploaded file content at rest | Sibling scope split from #358 |

**New discovered-work item, not yet triaged into an epic**: **#1366** — `PIPER.user.md` is a single, unscoped, server-instance-level config file; every conversation on a shared instance (alpha.pipermorgan.ai included) gets the same personalization + GitHub default-repo regardless of which user is talking to Piper. Filed 2026-07-06 (Lead Dev), Architect ruled it decomposes into 3 components: **Component A (GitHub default-repo leak) — DONE 2026-07-06** (migration-completion, no ADR needed; `f04cbeea6`/`1784ae017` on main, enforcement lint shipped). **Component B (system-prompt personalization) — OPEN**, blocked on Architect's ADR-075 (not yet authored). **Component C** (#1260 PM-identity resolution) ruled out of scope — architecturally legitimate, not a leak. Issue stays open for B. Live on alpha today, not a future-only concern — PM/PPM's call on formal epic inclusion.

### Epic C — Connector/OAuth cutover (2 issues)
Already in progress — Lead Dev's current active thread. Continue, don't restart.

| # | Title | Status |
|---|-------|--------|
| #1317 | Per-connector MCP-consumer adapters onto the Connector contract | In Progress |
| #1220 | github-mcp-server provisioning + write-path credential migration | In Progress. Scope expanded 2026-07-05: writes (create/update/close/comment) currently use the old native-PAT/shared-token credential path, not the new per-user grant store the read side uses — a tester connecting via the new OAuth flow would have writes silently misattributed until this migrates too. |

### Epic D — Deploy/hosting portability (2 open issues; 3 closed)

~~#1168~~ and ~~#1176~~ **closed 2026-07-05** (Lead Dev, Beta Blockers estimate research) — both fixes were already shipped as part of #1299's 2026-06-20 alpha-deploy remediation, but the issues themselves were never separately closed. Verified directly against current `main` before closing (see issue comments for evidence). #1299's own scope also shrank: sub-item (a) verified done, only (b) remains open.

**#1278 — REOPENED 2026-07-06 evening (Lead Dev), genuinely OPEN, real remaining work.** This is Epic D's headline hard gate ("no hosted server = no external beta testers"). Full timeline (evidence comment on the issue): accidentally auto-closed 07-05 19:51 (the commit-keyword incident documented in CLAUDE.md and this doc's change log below) → reopened 21:55 (PPM) → closed again 23:18 via a direct API/CLI call, not another keyword accident, and left **unexplained** (zero comments/session-log/decisions.log entries anywhere) → **reopened again 2026-07-06 evening (PM-directed, Lead Dev executed)** once the unexplained second closure was flagged. The AC checklist still shows every substantive item unchecked (fly.toml, deploy, health check, domain cutover, TESTER-QUICKSTART update — only the dependency item is checked) — this reflects real, not-yet-done hosting work, not a bookkeeping gap. **The board's separate Status field still shows "Done" post-reopen** — held on the standing PM-gate for project-board field edits, not corrected unilaterally; flagged to PM.

| # | Title | Why it's a hard gate |
|---|-------|----------------------|
| #1258 | Strip inherited empty Anthropic env vars at server startup | Any hosted environment inheriting Claude Code's empty key fails every LLM call |
| #1299 | Deploy hardening remainder — **only (b) remains**: deploy.sh migrate hardening (real-deploy verification + BUILD_FAIL race disambiguation) | Migrations fail on hosted deploys |

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

**Total: 20 open issues across 7 epics** (25 minus #1168/#1176/#1260/#1241/#542, all genuinely closed — see Epic B, Epic D, and change log. #1278 is back to OPEN as of 2026-07-06 evening — see Epic D above — and is counted among the 20).

## Recommended sequencing

1. **Epic A first** — a verification prerequisite, not just another item. Nothing else's "closed" status means much without it. **DONE, closed 2026-07-05** (#1304).
2. **Epic C continues in parallel** — already Lead Dev's active thread; don't interrupt momentum.
3. **Epic B is the critical path, but smaller than first estimated** — #1260 and #1241 both closed 2026-07-05 (#1241 turned out to already be complete, see Epic B note — a stale-open issue, not real remaining work). Remaining: #358, #1305, #1306 (the last two need design decisions not yet made), #542.
4. **Epics D and F** are largely isolated, well-scoped fixes — strong candidates for batching, or handing to a coding subagent in parallel, so Lead Dev's own attention concentrates on B and C. **Exception: #1216** (Epic F) — scope decision made 2026-07-05 (interim fix for beta, full model deferred to Production).
5. **Epics E and G** interleave around the above as bandwidth allows. **#441+#1261 should be worked as one unit** (real shared code paths — password-reset token service, email flow); **#1312 should ride alongside Epic B** for Architect's attention (per-column judgment + a multi-Base architecture call), not batch with G's mechanical issues.

## Target date

No fixed date as of 2026-07-05. Lead Dev's bottom-up estimate (memo, 2026-07-05) is now **materially smaller than first given** following the #1241 correction: Epic A done, Epic B down from an estimated 9-16 days to roughly 5-9 days (only #358/#1305/#1306/#542 remain — #1260 and #1241 together were nearly half that original range and are both closed), Epic D down to ~1 day. Rough total wall-clock, accounting for parallelization once Epic B's remaining items start: **2.5-4 weeks**, revised down from the original 3-5 week estimate. A real ship date still isn't set — this is a rough range, and #1305/#1306's undecided design calls remain the biggest source of uncertainty in it.

## Change log

- **2026-07-05**: Document created. 22 issues confirmed across 7 epics, following the 2026-07-04/05 sprint-by-sprint triage (M3-Quality, M3-Health, M3-Security, M4, M5, RECONNECT) and the GitHub-write-capability forensic investigation. Established as the canonical source of truth per PM.
- **2026-07-05 (later)**: PM-directed audit found 16 open MVP-milestone issues untracked by the sprint-by-sprint sweep -- root cause: some issues carried Sprint-field tags from sprints that had already closed (M2, M3, D1) and were never swept forward, and a whole separate FLYWHEEL/SKUNK category was never in the triage sequence at all (compounded by a sprint-assignment data-loss incident ~10 days prior). Resolved by a milestone-level ground-truth check (every open MVP issue, not just tagged-sprint issues) rather than continued reliance on Sprint field alone. Result: 3 added to Beta Blockers (#1216, #1256, #1260 -- now 25 issues), 4 to Production (#1167, #1209, #1257, #1284), 9 to a newly-created **Ongoing** milestone (#683, #1160, #1162, #1259, #1272, #1275, #1277, #1295, #1296 -- FLYWHEEL/Skunkworks work with no release-bound completion target, kept separate from Production so it isn't misrepresented as "done by 1.0"). Also found and flagged (not yet resolved): #1278's stated dependency on "credential decoupling (#1162)" cites the wrong issue -- the real credential-decoupling work is #1300, currently Production-scoped -- open question on whether that's a real beta-blocking dependency or a stale/overscoped acceptance criterion.
- **2026-07-05 (final)**: #1278's dependency question settled -- verified the actual mechanism (#1185, per-user LLM keys) already shipped; corrected #1278's issue body directly (stale reference + unmet-dependency framing both fixed). **Incident, self-caught and fixed same-day**: the commit message resolving this ("...not yet resolved: #1278...") was parsed by GitHub's naive close-keyword matcher as "resolved #1278" and silently closed the issue -- caught when PM spot-checked the board directly, reopened immediately, and all 25 Beta Blocker issues + all commit messages from both days scanned to confirm no other accidental closures occurred. Lesson: avoid close/fix/resolve wording immediately adjacent to a "#N" reference in commit messages unless the closure is intended, even inside a negated clause -- GitHub's matcher has no concept of negation. Added `beta:<epic>` GitHub labels (7, one per epic) across all 25 issues, and a `post-beta-priority` label on #1340 (PM: high priority for the first Production sprint after beta, since it's the onboarding-polish counterpart to the already-shipped #1185 mechanism).
- **2026-07-05 (Lead Dev estimate research pass)**: #1168 and #1176 closed with evidence — both fixes shipped as part of #1299's 2026-06-20 alpha-deploy remediation but were never separately closed; verified directly against current `main` (independently re-verified by PPM via `gh issue view`, both confirmed CLOSED/COMPLETED). #1299's own scope reduced: sub-item (a) verified done, only (b) — real-deploy migrate verification + BUILD_FAIL race disambiguation — remains open. #1216's flagged scope decision resolved: ship the interim honest-decline fix for beta (reuses the #1331 mechanism, ~1hr), defer the full `is_seed`/`source` provenance field to Production (independently re-verified by PPM via issue comments). **Beta Blockers count: 25 → 23 open.** Lead Dev's full sequencing-refinement + bottom-up-estimate memo received same day; headline numbers noted above under Target date, full incorporation into the epic tables still pending a dedicated processing pass.
- **2026-07-05 (Epic B start, major correction)**: #1260 closed same-day (implemented + evidenced). **#1241 closed as already-complete** — starting the estimated 3-5 day audit, Lead Dev checked whether ADR-071 (touched minutes earlier for #1260) already covered #1241's deliverables before beginning fresh work. It did, completely: the audit (`dev/2026/06/15/1241-content-anchoring-audit.md`) and ADR-071 (ratified 2026-06-15) satisfied all 5 stated deliverables, and the downstream remediation had substantially shipped via #1238/#1250/#1252 (closed 2026-06-16 through 2026-06-19) — #1241 itself was simply never closed afterward. The one remaining piece (#1257, deeper read-threading + column drop) is already its own issue, correctly Production-milestone-scoped. **Beta Blockers count: 23 → 21 open.** This corrects the earlier estimate materially: Epic B's critical-path estimate revised down from 9-16 days to roughly 5-9 days; overall wall-clock revised from 3-5 weeks to 2.5-4 weeks. Lesson generalized: always check whether recent, adjacent work already answers an issue's deliverables before treating "still open" as "not started" — this is the same stale-tracking pattern as #1168/#1176 (Epic D) earlier the same day, now confirmed a third time.
- **2026-07-06 (Lead Dev, full re-verification pass against live GitHub)**: PM asked for a fresh Beta Blockers status after a multi-hour gap. Queried all 25 `beta:*`-labeled issues directly rather than trust the doc's snapshot; found 2 discrepancies the doc had wrong or missed. (1) **Epic A's "Recommended sequencing" line wrongly said #1304 was closed — it is genuinely OPEN.** 4/5 AC done (gating job live + proven with teeth via 3 real CI runs incl. a deliberate canary), the 1 remaining item is a deliberate hold pending PM's go/no-go on flipping the repo-wide required-status-check setting — corrected in the Epic A section. (2) **#1278 (Epic D's headline hard gate) shows CLOSED as of 2026-07-05T23:18:37Z, discovered only now** — this predates today's session (closed last night, missed in this morning's Epic-B-focused edit pass) but has **no comment, no session-log entry, and no decisions.log entry anywhere** explaining it, and the issue's own AC checklist shows the actual Fly.io hosting work still unchecked. Flagged in Epic D as unconfirmed-legitimate pending PM confirmation, rather than silently reporting Epic D as done. **Beta Blockers count: 20 → 19 open** (#1278 moves from open to closed-but-flagged; #542 already reflected closed from this morning). Also #542 closed this morning (Lead Dev) is now reflected in the open count for the first time in this changelog (was already noted in Epic B's prose).
- **2026-07-06 (later, Lead Dev) — #1278 REOPENED, per PM direction.** PM confirmed via chat that #1278's second closure needed reopening ("Fly mystery unclear but reopen as we discussed"). Reopened via `gh issue reopen 1278` with a full evidence-trail comment on the issue documenting the complete timeline (accidental keyword-close → PPM reopen → the unexplained second closure). The board's Sprint field confirmed directly from the live project board ("Beta Blockers - Hard Gates Only" — unchanged). The board's separate Status field still shows "Done" post-reopen — held on the standing PM-gate for project-board field edits, flagged to PM rather than corrected unilaterally. **Beta Blockers count: 19 → 20 open** (this document's own Epic D section + total-count line updated same-session on the correction pass below, since the reopen action itself happened in-conversation, not as an edit to this doc).
- **2026-07-07 (Lead Dev, correction pass)**: this document's Epic D section and total-count line still read from before the 2026-07-06 reopen (a doc-vs-GitHub drift, caught during a routine standing-items refresh, not a fresh investigation) — corrected to reflect #1278 as genuinely OPEN. No new facts here beyond the 2026-07-06 entry above; this is closing the gap between what happened and what this document said.
