# Lead Developer — Standing Items

Per duty-cycle substrate: recurring signals to check on each fire's task-loop. Living document — add / remove items as the cycle matures.

**Last refreshed**: 2026-07-07 ~07:00 PT (full reconciliation against live GitHub state, not memory — the prior 2026-06-21 surface was significantly stale: 3 issues it described as open/gated, #1232/#1185/#1286, had all since closed). **Live ephemeral state** (active threads, what's gated on whom, this session's queue) lives in `lead-carry-forward.md` — THIS doc is the durable recurring-signals checklist; the carry-forward is the per-session queue. When they disagree, the carry-forward is fresher.

---

## Sprint position

**Beta Blockers sprint, post-v0.8.10 alpha deploy (verified 2026-07-09 evening).** The v0.8.10 release deployed to the alpha droplet 7/8; 7/9 was a nine-point-release day (v0.8.10.1 → .9) that closed the tester-loop GitHub leg end-to-end: OAuth connect (#1382 hosted credential store), first verified connector write (#1220 CLOSED — test-piper-morgan#104, PM's OAuth identity, read-back verified), routing SSOT (#1283 CLOSED per ADR-077), user-tz time (#1381 CLOSED), Settings LLM-key page (#1380 CLOSED). **Invites are ALL-CLEAR** (HOST notified 7/9 evening; PM ready to send codes).

**RECONNECT connector-port residue**: 4/8 ported (GitHub, Calendar, Notion, Slack); remaining 4 (cicd/devenvironment/gitbook/linear) still blocked on the PM product-scope call (does a live MCP server exist for any?). #1317 tracks. #1220 no longer tracks this front — it closed on the write-path evidence; per-connector grant-migration (B-per-port) rides each future port per the Arch concur.

---

## Open-issue surface (current, verified against live GitHub state 2026-07-09 evening)

**RECONNECT connector ports** (#1317 tracking issue, OPEN):
- ✅ GitHub, Calendar, Notion, Slack — ported (4/8). Slack newest (2026-07-06).
- 🔒 cicd/devenvironment/gitbook/linear — blocked on PM product-scope call (does a live MCP server exist/is one planned for any of these). Not a build task until that's answered.
- ✅ #1220 (WS-8, auth-layer → MCP) — **CLOSED 2026-07-09** (first verified connector write; binding-aware gates across all chat surfaces; #1322 read-back guard live).

**Security / encrypt-at-rest**:
- ✅ **#1307 + #1308** security gap closed (admin_compose removed + exempt-list enforcement lint, m-41).
- ⏳ **#358** encrypt-at-rest (floor + Dimension B content cols) — still OPEN, code-complete, **deploy-held**: set `ENCRYPTION_MASTER_KEY` on the box + run `scripts/backfill_encrypt_content_358b.py` on the next alpha deploy.
- **#1305/#1306** (encrypt PII-JSON / uploaded-file-content, both deferred from #358-B) — still OPEN, M5/later.
- ✅ **Redis exposure FIXED** (#1311, 2026-06-21) — 6379 now `127.0.0.1`-only on the alpha Droplet.

**Beta Blockers sprint (as of 2026-07-09 evening — re-verify on pickup)**:
- **3 open, all gated on non-code**: #1278 (Fly.io hosting — PM coordinates; also Epic-D history in the issue), #1312 (phase 3 gated on PM's todo_lists excise confirm; then reviewed reconciliation migration of the 30 residual autogen ops + CI autogen-empty guard), #1332 (root-caused + fixed in v0.8.10.7 — `Intent.original_message` never set by any classifier construction; SOAKING, close after a few clean days).
- **Filed 7/9, sprint membership = PM's call**: #1383 (Notion/Calendar chat gates don't thread user_id — same class as the GitHub gate bug, priority-high), #1384 (timeout-modal buttons dead — no handlers wired).
- Epic A (#1304) residue: required-status-check flip still PM-gated (CIO recommends visible-only variant).
- Closed 7/8–7/9: #1220, #1283, #1380, #1381, #1382, #1379 (deploy runbook, milestone'd), plus the deploy itself.

**Filed 2026-06-25 (discovered work), both DONE**:
- ✅ **#1309** stale onboarding test — DONE (`854880c7d`).
- ✅ **#1310** mail-send.sh residue tooling fix — DONE (`c66bc7d6e`), tool self-reconciles after a successful push. **Caveat added 2026-07-06**: still hit a "reconcile edge case" once (tool warned rather than silently leaving bad state) — the pushed commit was correct but the local worktree needed a manual `git merge origin/main` + surgical single-file `git checkout HEAD -- <path>` to restore. Auto-reconcile is the common case, not a 100% guarantee — know the manual fallback.

**Still-open, NOT current sprint** (milestones GitHub-verified 2026-07-07 — "M5" is dead terminology, these are Production/Ongoing; the only live sprint in the MVP milestone is Beta Blockers):
- **#1144** TEST-DISCIPLINE-REFACTOR (Production).
- **#1131** CANONICAL-TODO-JUDGE-ARTIFACT (Production).
- **#1162** SKUNKWORKS-BYOC-HOSTED-DISTRO (Ongoing).
- **#1300** BYOC-CRED-DECOUPLE (Production).
- ~~#1105~~ LLM keychain UI — **CLOSED 2026-07-07** (was MVP milestone / Beta Blockers Epic E all along — the "M5/later" label here was stale; confirmed not-a-regression, dead-code bug fixed + live-verified).

**⚠️ The real task-loop queue when "my threads are drained" is the Beta Blockers sprint itself, not this doc's leftovers** — check `docs/internal/planning/beta-blockers.md` FIRST before declaring (0,0). (As of 7/9 evening the sprint is genuinely drained: 3 open, all PM/time-gated — but re-verify on pickup; PM may sprint #1383/#1384.)

**Closed since last refresh (2026-06-21 → 2026-07-07), for the record**: #1232, #1233, #1185, #1229, #1307, #1308, #1311, #1286, #1309, #1310, plus the M3 cluster already noted closed (#1124 #1142 #1143 #1133 #1134 #976 #953 #669 #995 #1130 #1060).

---

## Cross-agent threads (who owes whom)

- **PM ← Lead**: Epic A (#1304) required-status-check variant — implement once PM gives an explicit go-ahead (CIO's recommendation is in, visible-only variant, cc'd to PM directly 2026-07-06).
- **PM ← Lead**: whether/how to correct the Beta Blockers board's Status field for #1278 (still shows "Done" post-reopen — held on the standing PM-gate for project-board field changes, not touched unilaterally).
- *(The 2026-06-21 version of this section — Arch ratify #1232, CXO Slice-2 decision, PM #1286 phone-UAT — is now moot; all three resolved when #1232/#1286 closed.)*

---

## Recurring infrastructure-health checks

- **Cron**: current job armed under expression `17 6,9,12,15,18,21 * * *` (6x/day, 6am-9pm PT, offset :17). Session-only, auto-expires 7d → re-arm on the cycle. *(Update this line whenever the cadence itself changes, not just the job id — a stale cadence description here is a second, independent source of confusion on top of any session-log note.)*
- **Inbox**: drain `mailboxes/lead/inbox/` to 0; move read items to `read/` per discipline.
- **mail-send.sh residue**: usually AUTO-reconciled since #1310 (2026-06-25) — but see the caveat under #1310 above; know the manual fallback (`git merge origin/main` + surgical `git checkout HEAD -- <path>`) for the edge case.
- **Sync before commit**: `git fetch origin main && git merge origin/main` (the worktree branch is busy; FF races happen) — verify pushes land on `origin/main` by content (`git log --oneline origin/main..HEAD` empty), not exit code.
- **Briefing freshness**: if `BRIEFING-CURRENT-STATE.md` is > 7d stale, refresh via the `update-current-state` skill (any agent who notices — PM standing request).
- **This doc's own freshness**: last went ~16 days without a refresh (6/21 → 7/7) before this pass, during which 3 of its "open/gated" items silently closed. No enforced trigger catches this class of staleness — refresh proactively when picking up standing-items work, don't wait for a discrepancy to surface it.

---

## Pinned discipline reminders

- `feedback_close_issue_properly_skill_recurring_miss` — update description checkboxes BEFORE closing.
- `feedback_deferred_ac_self_justification_is_premature_closure` — use `[⏸]` for deferred verification.
- `feedback_ui_fix_requires_template_render_test_not_curl_200` — UI/runtime fixes need real-shape verification (template.render), not curl-200.
- `feedback_make_promises_durable_no_happy_talk` — install mechanisms (issue / hook / lint), not just promises (cf. #1310 filed over a vigilance-note).
- `feedback_commit_immediately_after_write_for_new_files` — untracked files at risk on shared trees.
- `feedback_careful_git_sync_on_shared_main` — commit own work BEFORE syncing; explicit paths only; verify by content.
- `feedback_sprint_field_changes_require_pm_confirmation` — GitHub Projects board field changes (Sprint/Status) are PM-gated, even when the "right" value seems obvious.
- **New 2026-07-06**: GitHub Projects v2 custom-field option-list edits are full-replace, not additive — never resubmit a complete option list against a live field without testing on a throwaway field first (this destroyed the Sprint field's assignments for all 1175 items once already).
- **New 2026-07-06**: commit messages referencing an issue number must avoid close/fix/resolve-family words immediately before `#N` unless closure is intended — GitHub's auto-close matcher has no negation concept (already caused one accidental close of #1278).
