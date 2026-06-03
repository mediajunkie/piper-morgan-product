# Lead Developer — Standing Items

Per duty-cycle substrate: recurring signals to check on each fire's task-loop. Living document — add / remove items as the cycle matures.

**Last refreshed**: 2026-06-03 ~16:15 PT (post-M2-close; PA-flagged staleness correction).

---

## Sprint position

**M2 CLOSED 2026-06-03.** Final close-gate (#1047 M2D-UAT) closed with surface-by-surface verdict. R4 (suggestion-provenance) shipped + verified end-to-end via PM browser-smoke. Canonical retest Run 11 (June 3): Routing 93.4%, Expected-pass Quality 80.5% (above ≥75% north star). M2 quality gate HELD.

**M3 now active.** Backlog tracked in `dev/active/M3.tsv` (20 items: 2 Done, 18 Product Backlog).

---

## Open-issue surface (tier-aware)

**M2 close-gating — ALL CLOSED**:
- ✅ #1047 M2D-UAT — closed 2026-06-03 (3 surfaces PASS / 2 deferred-to-#1142 / 2 not-testable-in-setup → #1143)
- ✅ #1135 INSIGHT-PULL-NOT-WIRED — closed (R4 Steps 1+2; verified Surface 3 smoke)
- ✅ #1136 INSIGHT-PUSH-NOT-WIRED — closed (R4 Steps 3+4; verified Surface 5 gate)
- ✅ #1132 TRUST-STAGE-HARDCODED — closed 2026-06-03 (real TrustComputationService lookup)
- ✅ #1122 / #1081 / #1080 / #1121 / #1116-#1123 burst — all closed (M2-close burst May 27 → June 3)

**M3 (active sprint)**:
- **#1124 PRE-FLOOR-HANDLER-AUDIT** (HIGH, LARGE) — ~28 dispatch sites; the architectural cleanup R4 pulls against
- **#1129 SLACK-INBOUND-STRUCTURAL** (HIGH) — PM-picked path C (Socket Mode rebuild via #1107 DinP re-registration). **Needs PM-at-keyboard window for DinP re-registration** (can't be agent-driven).
- **#1142 UI-AUDIT-FUNCTIONAL** — catalog every UI route: claims vs wired vs stale (testability prerequisite; from M2 smoke findings)
- **#1143 COMPOSTING-DEV-TRIGGER** — admin affordance to verify #1033/#1035 (composted reflection + scheduler)
- **#1144 TEST-DISCIPLINE-REFACTOR** — real SurfaceableInsight + ExtractedLearning fixtures (R4 twin-bug lesson)
- **#1060 INFRA-CONVERSATION-REPO**, **#976 MEM-COMPOSTING**, **#953 CONTEXT-PERSIST**, **#669 COMPOSTING-HYBRID-TRIGGER** — memory/persistence cluster
- **#1133 HISTORY-SIDEBAR-UNWIRED** + **#1134 INSIGHT-JOURNAL-INTEGRATION-GAP** — PM tentatively M2-disc but design-decision-shaped; pending #1142 audit + CXO UX discussion
- (full list in M3.tsv)

**M5 (polish) — filed, deferred**:
- #1105 LLM keychain settings UI re-paste; #1130 SPRINT-MEMBERSHIP-TSV; #1131 CANONICAL-TODO-JUDGE-ARTIFACT; #1137 calendar test-drift; #1138 ActionDisposition naming; #1139 PremonitionService method audit
- **#995 fabrication-probe re-run** — Run 11 showed 6 Phantom (confident invention); should trigger #995 re-run

**post-MVP**:
- #1108 Slack OAuth failed-attempt recovery UX (folds into #1129 Slack rebuild)
- #1110 SlackClient user_id-threading latent bug

---

## Cross-agent threads

- **EC-2 capability-claim-consistency (PDR-005 v1.0)** — ✅ Lead Dev concurred on synthesized qualifier (2026-06-03); folding to v1.0. Closed from Lead side.
- **Agent-360 v0.3 fielding (HOST)** — response requested ~June 10 backstop. Questionnaire at `dev/active/agent-360-questionnaire-v0_3.md`. **OWED: Lead Dev response memo** (§8 role-specific + §7 from Code-era experience, no v0.2 baseline). Queued for a calmer cycle.
- **#1142 UI audit + CXO UX discussion** — CXO memo sent 2026-06-02; PM wants UX + web-UI working session. UI-vs-architecture mismatch is the M3 theme-setter.

---

## Recurring infrastructure-health checks

- Server up on port 8001 (`curl /health` → 200) — currently PID 99378 (restarted 2026-06-02 with R4 + #1132 fixes)
- Lead inbox: drain to 0, move read items to read/ per discipline
- Branch state: on `main`, synced with origin (working in worktree `mux-ui-lane-scoping`)
- Cron-prompt staleness: the duty-cycle fire prompt still references "awaiting PM call on Option A/B for #1047 UAT realignment" — **#1047 CLOSED 2026-06-03**; prompt text is stale (flag to CIO/PM for cron-prompt refresh)

---

## Pinned discipline reminders

- `feedback_close_issue_properly_skill_recurring_miss` — update checkboxes BEFORE closing
- `feedback_deferred_ac_self_justification_is_premature_closure` — use `[⏸]` for deferred verification
- `feedback_ui_fix_requires_template_render_test_not_curl_200` — UI/runtime fixes need real-shape verification, not mock-with-attributes (bit twice during R4: bucketing bug + add_turn gap)
- `feedback_make_promises_durable_no_happy_talk` — install mechanisms, not just promises
- `feedback_commit_immediately_after_write_for_new_files` — untracked files at risk on shared trees
- `feedback_verify_show_stat_post_commit_pre_push` — git rename detection can capture adjacent moves
