# Lead Developer — Standing Items

Per duty-cycle v0.6 substrate: recurring signals to check on each fire's task-loop. Living document — add / remove items as the cycle matures.

---

## Open-issue surface (tier-aware)

**M2 close-gating (highest priority)**:
- ✅ #1080 NOTION-WRITE — closed today (PM-driven earlier)
- ✅ #1121 MIGRATE-UPDATE-DOCUMENT-TO-SLOT-FILLING — closed today; 4/5 phrasings verified
- ✅ #1122 MULTI-TURN-DOC-ANTECEDENT — closed today; option B shipped (commit `ce9587277`); structured-dispatch antecedent resolution now general across slot-filled actions
- ✅ #1081 NOTION-SLACK-XREF — closed-superseded-by-#1129 (structural blocker; Slack inbound unmounted since Oct 2025)
- **#1047 M2D-UAT** — still PM-deferred

**Discovered work (recent, may need disposition)**:
- #1116 INTENT-SVC-NONE — Finding 2 fixed; Findings 1 + 3 still open (low priority)
- #1117 INTENT-TEMPORAL-OVERGREEDY — classifier misclassifies "when did I X" queries
- #1118 RETEST-SCRIPTS-KEYCHAIN — dev scripts can't load API key from keychain
- ✅ #1119 FRONTEND-ERROR-RENDER — closed today (commit `ae91791af`); parseApiDetail shared util
- #1120 NOTION-DB-LIST — get_config missing user_id refactor-miss
- #1123 LINK-NEW-TAB — Piper-emitted links replace chat tab
- #1124 PRE-FLOOR-HANDLER-AUDIT — meta-issue; ~28 dispatch sites + ~14 clarification flows
- **#1129 SLACK-INBOUND-STRUCTURAL** — filed today; PM-picked path C (rebuild via Socket Mode); post-M2 schedule; absorbs former #1107

**Older still-open (audit-followup)**:
- #1047 M2D-UAT — PM bandwidth-deferred
- #1110 SlackClient user_id threading latent bug (filed during #1085 work)
- #1115 router_delegation pre-existing test failure
- #1126 (resolved)

## Cross-agent threads to monitor

- **CIO MEM-975 cohort-rollout sequencing** — ✅ responded 2026-05-27. Awaiting CIO ack or cohort-rollout kickoff.
- **Docs GitHub Actions operational refactor** — ✅ lane accepted; ✅ Architect sanity-check received; ✅ Phase 1+2 shipped (commit `f372ce793`); 5 expected workflows verified firing post-merge. Stuck run #25923061467 + scheduler-drop unrecovered post-Step-B; **needs PM Support ticket**.
- **methodology-37 Coverage-Audit Gate** — ✅ filed today (commit `73492ebbd`); CIO slot 37 allocated and consumed.
- **#1129 SLACK-INBOUND-STRUCTURAL** — Pattern-073 Instance #15; post-M2 rebuild scope.
- **PA #1085 user-id-threading latent bug (#1110)** — keep in queue for handler-cleanup pass
- **Architect cross-coordination** — none active right now; #1117 picks up when classifier work resumes

## Recurring infrastructure-health checks

- Server up on port 8001 (`curl /health` → 200)
- Lead inbox: 0 unread (move read items to read/ per discipline)
- Branch state: on `main`, synced with origin
- Working tree: no untracked files I created (per "commit immediately after Write" pin)
- Server log: any IntentService init failures? (#1116 watch — Finding 2 fix should hold)

## Pinned discipline reminders

- `feedback_close_issue_properly_skill_recurring_miss` — update checkboxes BEFORE closing
- `feedback_deferred_ac_self_justification_is_premature_closure` — use `[⏸]` for deferred verification, not `[x]` with rationalization
- `feedback_make_promises_durable_no_happy_talk` — install mechanisms, not just promises
- `feedback_descriptive_names_not_cryptic_ordinals` — use short descriptive names in PM-facing prose
- `feedback_branch_show_current_before_every_commit` — verify branch identity
- `feedback_commit_immediately_after_write_for_new_files` — untracked files at risk on shared trees
- `feedback_verify_show_stat_post_commit_pre_push` — git rename detection can capture adjacent moves; always verify
