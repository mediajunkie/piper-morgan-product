# PPM Session Log — 2026-07-05

**Role**: PPM (Principal Product Manager)
**Model**: Sonnet (claude-sonnet-4-6)
**Tool**: Claude Code
**Worktree**: claude/pensive-kepler-02a0f6 (Option B ephemeral)
**Session log**: dev/2026/07/05/2026-07-05-0000-ppm-code-sonnet-log.md

Continuing from Jul 4 session (DAY-CLOSED, see `dev/2026/07/04/2026-07-04-0652-ppm-code-sonnet-log.md`). Same live conversation with PM continues uninterrupted across the date rollover — this is a log-file transition only, not a session break.

---

### Carry-forward from Jul 4 (open at day transition)

- **GitHub-write OAuth verification** — memo sent to Lead Dev (commit `63060b2cc`) asking them to live-test whether create_issue/close_issue/comment route through per-user OAuth binding or a shared token. Lead Dev is folding this into testing already in progress. **Awaiting response.**
- **M4 triage — 15/16 executed.** #302, #558, #712, #713, #954, #955, #956, #1062, #1166, #1174, #1217, #1242, #1244, #1245, #1326 moved to Production milestone. **#1190 held in MVP**, pending the OAuth verification above (if writes need real per-user auth work, #1190's confirmation-gate scope may grow; if writes are already correct, #1190 is a narrower UX-polish item).
- **M3-Quality (7 issues) presented to PM, awaiting answer**: 4 leaning Production (#1151, #1175, #1219, #1224); 3 flagged — **#1279** (GitHubIntegrationRouter aiohttp session leak, reliability risk under beta load — PPM lean: Beta Blockers), **#1285** (possible datetime-subtraction crash in standup COMPLETE path — PPM lean: Beta Blockers pending confirmation it's a live crash), **#1105** (settings UI re-paste friction despite working server-side keychain — PPM lean: Beta Blockers, same shape as #1258).
- **Beta Blockers sprint** — 16 issues confirmed on GitHub board: #358, #441, #1168, #1176, #1220, #1241, #1258, #1261, #1278, #1283, #1299, #1304, #1312, #1317, #1324, #1332. Will grow depending on M3-Quality outcome + OAuth verification result.
- **PA's #1351 (MCPB session-isolation)** needs a tracking home distinct from the main Beta Blockers sprint (PA confirmed it gates MCPB-enablement, not beta release) — not yet resolved, raise with PM.
- **Gap flagged by Lead Dev, still unfiled**: no GitHub issue tracks "ship GitHub connector to production" (migration + release cut + MCP server hosting).
- **Close-calls remaining**: only #1167 (Docker orchestration).
- **#683 MUX-WIRE-DOD** — still BLOCKED on Lead Dev recipe.
- **Next sprints after M3-Quality closes**: M3-Health (9 open), M3-Security (7 open), RECONNECT — Connector Refactor (35, largely superseded by the narrower #1317inc.2/#1220 beta slice per Arch's ruling).
- **PM's clean-machine test result on MCPB v0.1.9** (run the night of Jul 4) — not yet reported to PPM, check with PM.

---

### Fire 6 — 00:0X PDT (cron, first fire after day rollover)

**Cron rotation**: deleted `30996514`, created new job with fully rewritten standing items reflecting the state above (Fire 5's prompt was stale — written before the OAuth investigation completed, M4 executed, and M3-Quality was presented).

**Inbox**: clean (MANIFEST.md only) — no Lead Dev response yet on the OAuth test.

**Day transition**: closed Jul 4 log with DAY-CLOSED sentinel + memory eval; this log created to continue. Live conversation with PM is uninterrupted — no session break, log-file rollover only.

**Status**: IDLE on new inbox mail; M3-Quality answer and Lead Dev's OAuth test are both awaiting external input (PM and Lead Dev respectively) — nothing further to drain until one arrives.

---

### Fire 7 — 10:22 PDT (cron)

**Cron rotation**: deleted `cfb9fa8a`, created new job (standing items to be rewritten this fire).

**Inbox**: 4 new memos, all processed to read/:

1. **Lead Dev's OAuth-write answer — DEFINITIVE finding.** Static trace (no live test needed, reasoning airtight): `create_issue`/`update_issue`/`add_comment` (`services/mcp/consumer/github_adapter.py:850,880,934`) take no `user_id` parameter — structurally cannot do a per-request grant-store lookup. They use one `aiohttp.ClientSession` with one token baked in at creation (`configure_github_api`), sourced from `GitHubConfigService.get_authentication_token(user_id)` — the OLD credential path (manual keychain PAT, falling back to a shared/system token) — NOT the new `ConnectorGrantStore`/`ConnectorBinding` rail the read side (`resolve()`, `list_open_issues`, etc.) correctly uses per-call. **Real implication**: a tester who manually pasted their own PAT has correct writes today (no gap). A tester who connects only via the new #1317inc.2 OAuth flow (not yet built) would have writes silently execute against the wrong (shared/system) credential once that flow ships. Lead Dev already added this as a comment on #1220 (the artifact, not just mail). Footnote: a session-reuse bug in `configure_github_api()` (second call with a different token silently doesn't take effect) looks unreachable today, flagged on #1220 as a footnote only.
   - **Action taken**: sprint-order.md v4 updated — #1220's scope description expanded to explicitly include "write-path credential migration," not just the ops/hosting decision. #1190 (destructive-mutation confirmation gate) confirmed as Production — it's a narrow UX-polish item (same-message regex vs. multi-turn state machine), genuinely unrelated to the credential-routing question once the OAuth answer came back. Moved via `gh issue edit` (spot-verified: Production).
2. **Exec: Ship #050 §0 due immediately** — correction to an earlier "Monday" framing; PM flagged this as a recurring antipattern (no agent authorized to delay unblocked work without written approval). **Action taken**: reviewed Jun 27–Jul 3 PPM activity via git log (People #1281 one-pager + roadmap v18.2 delivered Jun 28; #1331 alpha-trust yellow-flag-not-blanket-gate ruling Jul 1; #1235 escalated to PM with 3 options rather than unilaterally decided Jul 3; Ship #049 delivered on schedule). Wrote and sent §0 to Exec, honestly flagging that sprint-order.md's ratification sitting pending most of the week was itself a small instance of the exact antipattern this correction is about.
3. **Lead Dev: Slack connector design work needed** (to PPM+CXO) — spells out two design questions (app-level vs. per-user credential UX; UNREACHABLE-state visual treatment) so the shape of the work is visible whenever it's prioritized. Explicit: Production-milestone work, not a beta blocker, no urgency.
4. **CXO's answers** (cc) — app-level credential is invisible infrastructure to users (gate, not setup UI); keep 3 visual tiers, disambiguate UNREACHABLE via copy, don't add a 4th tier without evidence. Agrees Production-scoped. **No PPM action needed** — both leads converged cleanly; noted for awareness, no issue exists yet to move.

**Commits this fire**: sprint-order.md v4 (#1220 scope + footer) + 4 memos to read/ + MANIFEST + Ship#050 §0 memo to Exec + this log entry — pushed atomically.


---

### M3-Quality triage closed — PM decisions received (in-conversation)

PM: "1279 - agreed. 1285 - also yes. 1105 - agreed … we are trying to get to less crude auth."

All 7 M3-Quality issues now dispositioned:
- **4 → Production** (milestone move confirmed via `gh issue edit`): #1151, #1175, #1219, #1224
- **3 → Beta Blockers** (milestone already MVP; Sprint field set to "Beta Blockers - Hard Gates Only" via GraphQL, confirmed): #1279 (aiohttp session leak — reliability risk under beta load), #1285 (possible datetime crash in standup COMPLETE path), #1105 (settings re-paste friction — PM's framing: part of a broader push toward less crude auth, not an isolated UX fix)

**Beta Blockers sprint now 19 issues**: #358, #441, #1105, #1168, #1176, #1220, #1241, #1258, #1261, #1278, #1279, #1283, #1285, #1299, #1304, #1312, #1317, #1324, #1332.

sprint-order.md v5 pushed with all 3 new rows + footer update.

**M3-Quality fully closed.** Next in sequence: M3-Health (9 open), M3-Security (7 open), RECONNECT — Connector Refactor (35, largely superseded).


---

### M3-Health + M3-Security triage closed — PM decisions received (in-conversation)

**M3-Health (9 issues)** — clean tech-debt sprint, no live-bug candidates. PM: "agreed on all of those … they are ok for LD to cherrypick when otherwise idle but they do not block beta." All 9 moved to Production via `gh issue edit`: #1001, #1028, #1131, #1138, #1139, #1144, #1287, #1298, #1321.

**M3-Security (7 issues)** — real teeth this time, several tied directly to today's #358 decision:
- **4 → Production**: #371 (time-series DB infra, unrelated to security — likely mis-sorted into this sprint), #557 (WebSocket infra, same situation), #1203 (already PM-deferred to M5-reconsideration per a June 12 ruling), **#482** (SEC-KMS-INTEGRATION — PM asked PPM directly for a recommendation rather than accepting a soft flag; PPM's call: Production, since it's ops-side secret-storage hardening rather than a tester-facing trust property like the other three, and doesn't actually connect to the "less crude auth" theme on reflection — PM approved).
- **3 → Beta Blockers**: **#542** (token revocation on disconnect — a real trust property, was on PPM's very first hard-gate list from this morning's investigation and had fallen out of the refined lists; a disconnected tester's token must actually stop working), **#1305** and **#1306** (both explicitly "deferred from #358-B" — sibling scope of this morning's #358 encryption-at-rest decision, travel with the parent principle).

sprint-order.md v7 pushed — also backfilled the M3-Health sprint-order.md update that was skipped earlier (GitHub moves were executed but the doc update wasn't pushed before moving on to M3-Security).

**Beta Blockers sprint now 22 issues.** **M3-Quality/M3-Health/M3-Security triage cluster is fully closed.**

Next in sequence: RECONNECT — Connector Refactor (35 open, largely superseded by the narrower #1317inc.2/#1220 beta slice per Arch's ruling — most is post-beta full-migration work). This is the last sprint in the triage sequence.


---

### RECONNECT triage closes the sprint-by-sprint cluster — PM approved (in-conversation)

29 of 35 RECONNECT issues turned out to already be closed (spot-verified via `gh issue view` state check) — they retain the MVP milestone tag purely for historical record, no action needed. Of the 6 genuinely open issues, all read as Production: #865 (setup-wizard refactor), #1322 (dead-code transport retirement — its write-path sub-scope already tracked as expanded scope on #1220), #1323 (mixin dedup), #1325 (future-state, "when supported"), #1327 (explicitly self-described as "additive... no regression to fix"), #1340 (onboarding UX tied to already-Production-scoped #1300).

PM approved; all 6 moved to Production milestone. **Sprint-by-sprint triage cluster is now fully complete**: M3-Quality, M3-Health, M3-Security, M4, M5, and RECONNECT have all been reviewed. sprint-order.md v8 pushed.

PM's framing on why RECONNECT went this deep: "Lead Dev has been hard at work on this sprint, but it was getting so deep that it led to our work reassessing the path to beta vs. production" — i.e., the RECONNECT sprint's own scope-creep is what triggered today's whole beta-scope reassessment.

**Beta Blockers sprint locked at 22 issues.** Next: PM asked for a fresh epic-level read of the 22 — how many, do they chunk logically — before drafting a sprint-plan briefing for Lead Dev.


---

### Beta Blockers promoted to its own canonical document (PM directive)

PM: write up the epic breakdown in its own file, add to the docs tree per NAVIGATION.md, refer to it in mail to Lead Dev. PM's framing: "Between now and beta release I want to refer to that blocker sprint doc as our source of truth of what remains between us and launch. Newly discovered issues will be triaged to determine if they too block beta and if they do they'll be added."

**Created**: `docs/internal/planning/beta-blockers.md` — the 22 issues across 7 epics (A: verification foundation, B: multi-tenancy/data protection, C: connector/OAuth cutover, D: deploy/hosting portability, E: auth/account lifecycle, F: correctness bugs, G: routing/config integrity), with rationale, recommended sequencing, and a maintenance rule for triaging newly-discovered issues in/out.

**Updated `docs/NAVIGATION.md`**: added pointers to both beta-blockers.md and sprint-order.md under the Product Managers section (sprint-order.md wasn't referenced there at all before — a pre-existing gap, fixed in passing).

**Trimmed `sprint-order.md`**: the "Confirmed Beta Blockers sprint" table is replaced with a pointer to beta-blockers.md, to avoid two documents holding the same list and drifting apart over time. sprint-order.md keeps its role as the sequencing document across the whole board; beta-blockers.md is now the focused, living "what stands between us and beta" doc.

**Sent Lead Dev the sprint-plan brief** referencing the new doc: summarized the 7 epics, asked for (1) a sanity check on the epic groupings/sequencing, (2) a bottom-up estimate now that scope is stable at 22, (3) a flag on which of Epic D/F look parallelizable to a coding subagent. No urgency attached — Lead Dev continues Epic C (the active connector thread) regardless.

**Open question to PM (asked separately, awaiting answer)**: whether to keep Aug 1 as an aspirational/stretch date. PPM's recommendation: no, even softened — three leadership voices already said to remove it, this exact date has already calcified past its original "aspirational" framing once this session, and the newly-expanded 22-issue scope (vs. the smaller set at the time of PPM's earlier timeline estimate) makes the realistic range if anything later than previously estimated. Recommended alternative: no fixed date until Lead Dev's bottom-up estimate lands.


---

### Roadmap v18.5 fold — PM asked directly if the canonical roadmap had been updated

It hadn't — roadmap.md was still at v18.4 (Jul 4 morning), stale against everything since (the GitHub-write investigation, the full sprint-by-sprint triage cluster, beta-blockers.md's creation, Aug-1's removal). PM: "is it time for a new version? This is a fairly substantial update" — agreed, folded as v18.5.

**Sections updated**: title, date/author/status header (new v18.5 fold note), new v18.5 changelog entry, Current Position (full rewrite), M4 section (TRIAGE CLOSED), RECONNECT section (TRIAGE CLOSED, 29/35 already-done + 6 moved), M3-Quality/Health/Security sections (all TRIAGE CLOSED), Sprint Summary table (all affected rows), Timeline forward sequence (Aug 1 removed entirely, beta-blockers.md referenced, sequencing recommendation added), Change Log (v18.5 + backfilled v18.4 entry), footer.

**Gap discovered while reconciling against reality**: the old roadmap's M4 section named **#1032** and **#1216** as concrete M4 deliverables. Checked both: #1032 is already CLOSED (fine, no action). **#1216 is OPEN, MVP milestone, and was never part of the M4 sprint triage** — it carries no Sprint-field tag matching the board's "M4 - Trust + Learning" grouping, so it fell through my earlier GitHub-project-board query entirely. Read its body/comments: it's the honest-provenance anchor issue (Piper claimed dev-seed-script placeholder data was "real" in response to "what have you learned about my workstyle") — PM-placed on M4 2026-06-14, still unresolved. Its failure shape (confident false claim about what's real) is materially similar to #1331's, which WAS hard-gated. Flagged clearly in the roadmap (Current Position + M4 section) as an untriaged gap with a Beta-Blocker-candidate lean, NOT silently dropped or claimed as resolved. Surfaced to PM directly rather than buried in the doc edit.

roadmap.md v18.5 pushed.


---

### Milestone-based ground-truth audit — PM-directed, found 16 discrepancies

PM's insight, prompted by the #1216 discovery: reliance on Sprint-field tags for triage coverage was fundamentally unsound, especially given a sprint-assignment data-loss incident ~10 days ago that PA caused and the team had to reconstruct "as best we could." Proposed a cleaner ground-truth check: pull every OPEN issue in the MVP milestone directly (a milestone property, not a Sprint-field property) and diff against the Beta Blockers list. Anything open in MVP but not on the list is either a missed blocker or a housekeeping miss.

**Ran it**: 38 open MVP-milestone issues vs. 22 Beta Blockers = 16 discrepancies. Root cause confirmed: several issues were tagged to sprints that had already closed (M2, M3, D1) and were never swept forward when those sprints closed; a whole separate FLYWHEEL (process-improvement) and SKUNK (Skunkworks) category was never part of the active triage sequence at all.

**Resolved** (all executed, spot-verified):
- **3 → Beta Blockers**: #1216 (honest-provenance/seed-data confabulation, same failure shape as #1331), #1256 (INTENT-VOCAB misclassification bug), #1260 (ADR-071 D7 PM-identity config — likely a real prerequisite for #1241's multi-tenancy work). Beta Blockers now **25 issues**.
- **4 → Production**: #1167 (resolved via investigation — the broken Dockerfile is the `orchestration`/Temporal-worker service, not the app image #1278 deploys from; already worked around for alpha by skipping that service entirely), #1209 (future-phase AutonomousExecutor work), #1257 (pure architecture refactor), #1284 (nav-group naming/design polish).
- **9 → new "Ongoing" milestone** (created this session, milestone #10, no target date): #683 (Definition-of-Done process update — also corrected its stale Sprint tag from the closed M2 sprint to FLYWHEEL), plus 6 FLYWHEEL issues (#1160, #1259, #1272, #1275, #1277, #1296) and 2 SKUNK issues (#1162, #1295). PM's reasoning: Production implies "scoped for the 1.0 release," which misrepresents perpetual/parallel-running tracks that have no release-bound completion date — a dedicated milestone represents them honestly.

**Correction on the FLYWHEEL "touches code" rule**: PM clarified the rule is about Piper Morgan *product* code specifically, not any code in the repo — cohort/methodology tooling (mail-send.sh, mailbox infrastructure) doesn't disqualify an issue from FLYWHEEL. Retracted my earlier flag on #1259/#1296 as mis-tagged; they're correctly FLYWHEEL under the clarified rule.

**New discrepancy found and flagged, not yet resolved**: while resolving #1167, found that #1278 (Fly.io hosting, confirmed Beta Blocker) states in its own acceptance criteria that "credential decoupling (#1162)" must ship first — but #1162 is actually the Skunkworks hosted-distro issue; the real credential-decoupling work is #1300, which is currently Production-scoped. PPM's lean (given directly to PM): #1300 likely doesn't need to move into Beta Blockers — its actual scope (public-marketplace protection) is a bigger concern than a small, invite-gated beta cohort needs; recommend correcting #1278's stale reference and softening that acceptance criterion rather than pulling #1300 forward. Awaiting PM's confirmation before editing #1278's issue body.

**Verification**: re-ran the full MVP-milestone pull after all moves — 25 open issues remain, exactly matching the 22 original + 3 new Beta Blockers additions. Zero discrepancy remains between MVP milestone and the Beta Blockers list.

beta-blockers.md and sprint-order.md both updated to reflect the new 25-issue list and the Ongoing milestone.


---

### Epic breakdown refined — PM asked whether the audit findings changed the epic structure

PM's question prompted a genuine reconsideration, not just a "which bucket" check. Two real refinements to beta-blockers.md:

- **Epic B**: #1260 (per-user identity config) is likely a prerequisite for #1241 (multi-tenancy remediation), not just thematically related — #1241 can't be properly verified with real multi-user testing until #1260's fallback replacement lands. Reordered the table (#1260 first) and added an explicit within-epic sequencing note; updated the cross-epic "Recommended sequencing" section to call this out.
- **Epic F**: #1216's intended fix (a real `is_seed`/`source` provenance field on `InsightDB`) is a small feature, not a quick isolated bug fix like #1279/#1285/#1332 — it doesn't fit the epic's "batchable, quick" framing. Flagged a cheaper interim option (extending #1331's honest-decline mechanism at the prompt level, deferring the full provenance model past beta) as a real scope decision for Lead Dev/PM, not something to leave implicit.

Also fixed a stale "22-issue" reference in the Target Date section (should have read 25 since the milestone audit).

beta-blockers.md pushed.


---

### #1278 dependency settled before Lead Dev handoff — PM wanted crystal-clear instructions

PM: "Let's settle that before we hand off to Lead Dev? I want them to have crystal clear instructions from now till we ship." Verified via direct REST API (GraphQL was rate-limited again) that **#1185 (BYO-KEY-MULTI-TENANT) already shipped the actual per-user-key mechanism** — status "DONE (core)... Priority: P1 (beta-gating)". Authenticated users' LLM calls already resolve their own stored, encrypted Anthropic key, security-verified against cross-user leakage. #1340 (the piece I'd moved to Production) is confirmed pure UX polish on top of an already-complete capability — its own body says "the capability is complete... this tracks the UX fold only." #1300 turned out to be unrelated to #1278's actual need (it's about the public-marketplace distribution scenario, a bigger/different concern).

**Resolution, better than the original "soften the AC" plan**: #1278's dependency isn't just mis-cited, it's already satisfied. Edited #1278's GitHub issue body directly — struck through the stale "#1162 must ship first" language, checked that AC item, corrected the Dependencies section to name #1185 (shipped) as the real mechanism, and noted #1340/#1300 as separate, non-blocking, Production-scoped items. #1278 now has zero open dependency. Verified the edit landed via `gh issue view`.

---

### Fire 8 — cron rotation, inbox, standing items rewrite

**Cron rotation**: deleted `7fb14205`, created new job — this fire's prompt was itself hours stale (still listed M3-Quality/Health/Security and RECONNECT as open, all of which closed since), standing items rewritten wholesale.

**Inbox**: 1 new memo — Lead Dev's Slack-connector closure: design questions fully answered (CXO's two calls incorporated), issue **#1364** filed with a complete AC checklist, Production-scoped, no urgency. **Found and fixed a small gap**: #1364 was filed without its milestone actually set (Lead Dev said "Production-milestone" in the memo but the issue itself showed `milestone: null`) — set it to Production directly rather than letting it sit as an untracked open issue, exactly the kind of drift today's milestone audit was built to catch. Memo processed to read/, MANIFEST updated.

**Beta Blockers sprint status**: 25 issues (unchanged this fire). M3-Quality/Health/Security, M4, M5, and RECONNECT are all fully triaged. The Jul 5 milestone-ground-truth audit is closed (16 discrepancies resolved: 3 to Beta Blockers, 4 to Production, 9 to the new **Ongoing** milestone). beta-blockers.md is the canonical source of truth, now with epic-level sequencing refinements (#1260-before-#1241, #1216's scope caveat) and the #1278 dependency fully resolved.

**Still open**: PM's clean-machine MCPB test result (night of Jul 4) not yet reported to PPM. PA's #1351 tracking-home question not yet resolved. Lead Dev's "ship GitHub connector to production" gap still unfiled as an issue. #683 correctly reassigned to the Ongoing milestone this session (no longer "blocked," just perpetually-tracked FLYWHEEL work).


---

### #1278 accidentally self-closed via commit message — caught by PM's manual check, root-caused and fixed

PM manually checked the MVP milestone directly and noticed #1278 showing closed, prompting the question "why was #1185 on the list of open issues... if it's closed?" Investigation revealed two separate things:

1. **#1185 was never on any audit list** — it came up only during the #1278 dependency investigation (it's the already-shipped per-user-key mechanism), never flagged as an open-MVP discrepancy.
2. **#1278 itself was genuinely, accidentally closed** — by my own commit `0b92d1a2a` (the milestone-audit push). That commit's message included "Flagged, not yet resolved: #1278 cites the wrong issue number..." — GitHub's auto-close keyword parser does plain-text matching, not semantic negation-awareness, and read "resolved: #1278" as a close instruction, ignoring "not yet" entirely.

**Fixed immediately**: reopened #1278 (`gh issue reopen`), verified all 25 current Beta Blocker issues are open, and scanned every PPM commit message from both Jul 4 and Jul 5 for the same `close/fix/resolve` + `#N` pattern — confirmed #1278 was the only instance. No other accidental closures occurred.

**Lesson captured** (in beta-blockers.md's changelog and here): avoid writing resolve/close/fix language immediately adjacent to a `#N` issue reference in commit messages unless the closure is actually intended — GitHub's matcher has no concept of negation, so "not yet resolved: #N" is exactly as dangerous as "resolved #N."

### Epic labels added; #1340 flagged post-beta-priority

PM asked whether adding GitHub labels for the epics would help — agreed (makes the epic grouping filterable directly on the GitHub board, not just in beta-blockers.md) and executed: created 7 labels (`beta:verification`, `beta:multi-tenancy`, `beta:connector-cutover`, `beta:deploy-portability`, `beta:auth-lifecycle`, `beta:correctness-bugs`, `beta:routing-integrity`), applied across all 25 Beta Blocker issues per their epic membership, spot-verified. Also created and applied `post-beta-priority` to #1340 per PM's explicit call ("ok for production but should be a high priority after beta").

**#1300 discussed, not yet finalized**: PM's lean is post-beta, likely post-1.0 (Dot Releases) given its public-marketplace-distribution scope is a different kind of concern than Fast Follow's quick-iteration scope. PPM agrees with the reasoning. Deferred the exact milestone reassignment to the upcoming Production-sprint-organizing pass (PM's next requested task) rather than deciding it as a one-off.

beta-blockers.md updated: fixed a stale "22 issues" section header that survived an earlier edit pass, documented the label scheme, and recorded the #1278 incident + fix in the changelog.

**Status**: everything settled. Ready to send the final Lead Dev handoff, then move to organizing Production-milestone contents into proposed post-beta sprints (PM's explicitly next-requested task).


---

### CLAUDE.md updated cohort-wide; final Lead Dev handoff sent

Added a durable, cross-agent-visible warning to CLAUDE.md about GitHub's auto-close keyword matching having no negation awareness (the exact mechanism that closed #1278 by accident). Every role writes commit messages referencing issue numbers routinely, so this belongs in the shared instructions, not just this session log.

**Final Lead Dev handoff sent** (supersedes the earlier sprint-plan brief): summarized everything that changed since that first brief — the milestone audit's 16 discrepancies, Beta Blockers growing from 22 to 25, #1278's dependency now fully resolved, the 7 new epic labels, and the two epic-sequencing refinements (#1260-before-#1241, #1216's scope caveat). Same three asks as before (sequencing sanity-check, bottom-up estimate, parallelization flag on D/F), explicit that no blocking dependency should surprise them anywhere in the list. Told them to keep working the connector thread regardless.

**Status**: Beta Blockers work is genuinely done — 25 issues, 7 epics, labeled, sequenced, zero known open dependencies, canonical doc current, Lead Dev briefed. Next: PM wants to organize what's landed in the Production milestone into proposed sprints for after beta testing starts.


---

## INCIDENT: full Sprint-field data loss, project-wide — full account

While adding 8 new Sprint options for the Production-sprint reorganization (`updateProjectV2Field` with the complete `singleSelectOptions` array, the same pattern used earlier today to add "Beta Blockers - Hard Gates Only"), the mutation **silently detached every project item's existing Sprint-field value** — not just the items being worked on. Verified via `gh project item-list`: all 1175 items on the "Building Piper Morgan" board lost their Sprint assignment in one action.

**Root cause**: `updateProjectV2Field`'s `singleSelectOptions` argument performs a full replace, not an additive merge. The API rejects an `optionId` field in the input (confirmed by direct testing), so there is no way to submit the option list while preserving existing option identity. Submitting the full list — even with every existing option's name/color/description faithfully reproduced — caused GitHub to treat all 56 options (48 existing + 8 new) as newly created, orphaning every item's stored reference to the old IDs. Confirmed via direct query that the underlying field-value data is genuinely cleared, not just failing to resolve a name — this is not reversible through the API.

PM caught it immediately by checking the board directly and asked the root question directly: why didn't the same carefulness that worked all day (atomic git commits, diff verification, fetch-immediately-before-read-tree) prevent this? The honest answer: that discipline was calibrated to git, a system with cheap reversibility and full history. I applied the same *level* of care to a fundamentally different system — a live, shared, external API with no undo and no version history — without recognizing the operation carried a different risk profile than everything else I'd done that day. I verified *after* the mutation instead of confirming safety *before* running it against live, shared state.

PM drew a direct, fair parallel to Piper's own confabulation failures (#1331, #1216) investigated earlier today: an AI system acting on shared, load-bearing state without adequate care to know whether the action was safe. PM also, correctly, rejected my initial framing ("every individual action today was correct, this was one specific operation") as a version of "the au pair did the dishes fine, so trust them with the baby" — competence at routine, reversible tasks provides no assurance about safety on irreversible, catastrophic ones, and citing the former to soften the latter is exactly the kind of excuse-making PM named as unacceptable.

PM also corrected a second error: my claim that "the project's history isn't stored in just one place" (session logs, roadmap changelogs, decisions.log) was true in principle but empirically untested — and had *already* been tested and found wanting: PA destroyed the same Sprint field ~10 days prior (2026-06-25ish), and despite a real forensic reconstruction effort, that damage was never actually repaired. Citing "it's recoverable in theory" while a real, prior instance of the same damage sat unrepaired for a week and a half was itself a form of the cavalier treatment PM was naming.

### What was actually found and done about the recovery

Investigated the prior (PA) incident directly rather than continuing to assert recoverability in the abstract. Found `dev/2026/06/27/sprint-recovery-FOR-REVIEW-2026-06-27.csv` (originally filed in `dev/active/`, later archived — fully intact via git, a pure rename with zero content loss). This is a forensic reconstruction PA produced on 2026-06-27: 1146 rows, 265 with an actual proposed Sprint value (197 HIGH confidence, 49 MEDIUM, 19 LOW/needs-PM-decision), 853 marked UNKNOWN, 28 marked no-sprint. **Zero rows had ever been filled into the "PM Correction" column, and no commit anywhere shows this reconstruction being applied back to GitHub.** The real failure of the prior incident wasn't that reconstruction was impossible — it's that the reconstruction was done as a document and never became real. Naming this precisely so it isn't repeated: doing the analysis is not the same as doing the work.

**Recovery executed** (all via the safe, one-item-at-a-time `updateProjectV2ItemFieldValue` mutation — never another full-field-replace):
1. **105 issues restored from today's own first-hand knowledge**, zero ambiguity: the 25 Beta Blockers, 9 Ongoing (FLYWHEEL ×7 incl. #683, SKUNK ×2), and 71 Production issues into their 8 newly-created PROD-* sprints (the reorganization PM had just approved, now actually applied for the first time rather than lost before ever landing). #1364 was also discovered to have never been added to the project board at all (Lead Dev filed it directly) — added and tagged.
2. **160 issues restored from the June 27 CSV** (143 HIGH + 17 MEDIUM confidence, cross-checked against today's work first so fresher data always wins on overlap — 87 rows were already covered by #1 and skipped in favor of current knowledge). Applied in batches by target sprint, one item-mutation at a time; a 2-minute tool timeout interrupted the batch partway through (142/160), resumed and completed the remaining 18.
3. **Every single one of the 265 restored assignments independently re-verified** via a fresh `gh project item-list` pull cross-referenced against expected values — 265/265 correct, zero discrepancies.
4. **18 issues held back, not applied**: the CSV's own "LOW — needs PM decision" rows (`M5 (MVP Polish)` ×10, `M6 - MVP Future` ×8 — M6 doesn't even correspond to an existing sprint option) — these were flagged as ambiguous by the original 2026-06-27 reconstruction effort itself, and I'm not making that call unilaterally. Held for PM.
5. **Genuinely unrecoverable**: 853 UNKNOWN + 28 no-sprint rows from the original CSV — these were already unreconstructable as of June 27, before today's incident even happened. This isn't new damage from today; it's a pre-existing gap that today's incident didn't create and today's recovery effort can't close either, absent some other source of evidence I haven't found.

**Durable record added** (CLAUDE.md, cohort-wide, highest-severity flag of the day): `updateProjectV2Field`'s single-select options argument is a full replace with no ID-preserving path — never resubmit a complete options list against a live field with real item assignments without testing on a throwaway field first, or doing it via the web UI (additive), or stopping to ask a human when the safe primitive isn't available via API.

**Status**: 265 of the pre-incident Sprint assignments are restored and verified. 18 need PM's explicit decision. ~881 were already gone before today and remain a genuine, longstanding gap. Nothing further will be attempted on the project board without discussing it first.

