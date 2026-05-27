# Lead Developer — Standing Items

Per duty-cycle v0.6 substrate: recurring signals to check on each fire's task-loop. Living document — add / remove items as the cycle matures.

---

## Open-issue surface (tier-aware)

**M2 close-gating (highest priority)**:
- #1080 NOTION-WRITE — reopened pending #1121 + #1122 verification
- #1121 MIGRATE-UPDATE-DOCUMENT-TO-SLOT-FILLING — code complete; live smoke pending
- #1122 MULTI-TURN-DOC-ANTECEDENT regression — investigation pending
- #1081 NOTION-SLACK-XREF — reopened May 24, never verified

**Discovered work (recent, may need disposition)**:
- #1116 INTENT-SVC-NONE — Finding 2 fixed; Findings 1 + 3 still open
- #1117 INTENT-TEMPORAL-OVERGREEDY — classifier misclassifies "when did I X" queries
- #1118 RETEST-SCRIPTS-KEYCHAIN — dev scripts can't load API key from keychain
- #1119 FRONTEND-ERROR-RENDER — `[object Object]` from FastAPI 422 detail
- #1120 NOTION-DB-LIST — get_config missing user_id refactor-miss
- #1123 LINK-NEW-TAB — Piper-emitted links replace chat tab
- #1124 PRE-FLOOR-HANDLER-AUDIT — meta-issue; ~28 dispatch sites + ~14 clarification flows

**Older still-open (audit-followup)**:
- #1047 M2D-UAT — PM bandwidth-deferred
- #1110 SlackClient user_id threading latent bug (filed during #1085 work)
- #1115 router_delegation pre-existing test failure
- #1126 (resolved)

## Cross-agent threads to monitor

- **CIO MEM-975 cohort-rollout sequencing** — ✅ responded 2026-05-27 (Week 1 HOST+Docs, Week 2 PA+Comms, hybrid asymmetric measurement, post-v0.6.1 stabilization launch). Awaiting CIO ack or cohort-rollout kickoff.
- **Docs GitHub Actions operational refactor** — ✅ lane accepted 2026-05-27 (Phase 1+2 Lead Dev, Phase 3 CIO). Awaiting Architect sanity-check on paths-filter taxonomy before Phase 1 lands.
- **#1122 fix-scope disposition** — diagnosis filed 2026-05-27; awaiting PM disposition on options A/B/C + AAXT coverage + bisect frame
- **#1081 live smoke** — infra green; awaiting PM at-keyboard window in Slack
- **PA #1085 user-id-threading latent bug (#1110)** — keep in queue for handler-cleanup pass
- **Architect #1117 + #1122 cross-coordination** — when those get picked up, Architect may want input on classifier/conversation-state changes

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
