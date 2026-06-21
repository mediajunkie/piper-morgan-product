# Lead Developer — Standing Items

Per duty-cycle substrate: recurring signals to check on each fire's task-loop. Living document — add / remove items as the cycle matures.

**Last refreshed**: 2026-06-21 ~08:45 PT (RECONNECT-era reconciliation — the prior M2/M3 surface was 11/13 closed; replaced). **Live ephemeral state** (active threads, what's gated on whom, this session's queue) lives in `lead-carry-forward.md` — THIS doc is the durable recurring-signals checklist; the carry-forward is the per-session queue. When they disagree, the carry-forward is fresher.

---

## Sprint position

**RECONNECT sprint, post-D1** (D1 gate cleared 2026-06-19: #1293 closed, canonical regression 252/252 clean). Connector-refactor (WS1-9) + the BYOC foundation. Scope: `docs/internal/architecture/connector-refactor-sprint-scope-2026-06-14.md`. Phasing (ADR-070): **Phase-0** (#1185 identity + #1229 WS-2 cred-model, native) → **Phase-1** (WS-9 identity → WS-1 config → WS-2 creds → the connector ports) → Phase-2 (WS-3/4) → Phase-3 (WS-5/6/7/8). Foundation-gated.

D2 design-system (#1286, CXO-led) runs alongside.

---

## Open-issue surface (current)

**RECONNECT — shipped / in-flight**:
- ✅ **#1232** WS-5 connector contract — protocol + 4 sum-type results + m-41 no-credential guard + github structural proof. **Arch ratify pending** (mail `44e505456`). Ports deferred (D8 — need the WS-9/WS-1/WS-2 foundation).
- ✅ **#1233** WS-9 identity — PM resolved (m1-test + xian = same human; sole human → single identity; multi-tenant deferrable). Build = Phase-1.
- ⏸ **#1185** identity core — PARKED (gate chain: shared-gate removal + /connect flow + integration test). The per-user-key floor (#358) shipped.
- ✅ **#1229** WS-2 cred-model — native (Phase-0 foundation).
- 🔒 **Phase-1** — **Arch-gated** on the #1232 ratify + ADR-070 phasing confirm. Then WS-9 → WS-1 → WS-2 → ports.

**Security / encrypt-at-rest**:
- ✅ **#1307 + #1308** security gap closed (admin_compose removed + exempt-list enforcement lint, m-41). #1162 gate-removal ready for M5.
- ⏳ **#358** encrypt-at-rest (floor + Dimension B content cols) — code-complete, **deploy-held**: set `ENCRYPTION_MASTER_KEY` on the box + run `scripts/backfill_encrypt_content_358b.py` on the next alpha deploy.
- 🔴 **Redis exposure** (PA memo `…redis-security-droplet-2026-06-21`, PM forwarded the scan) — port 6379 public on the alpha Droplet. **Pending PM go** for the localhost-bind fix (Option A: compose `127.0.0.1:6379:6379`). Gates the alpha plugin wave. On fix: file+close a tracked issue.

**D2 design-system (#1286, CXO-led)**:
- ✅ Slice 1 (token foundation) + Slice 3 (responsive shell + mobile drawer) shipped — render+lint-verified; **CXO conformance + PM phone-UAT pending**.
- 🔒 Slice 2 (radar tiling) — **CXO-gated** (spec's dense tiling vs the roomy production `.radar-card`; memo `e6decb14f`, 3 options). Can't close #1286 until Slice 2 + the UATs.

**Filed this session (discovered work)**:
- **#1309** stale onboarding test (GATHERING_REPOS vs COMPLETE) — for the onboarding owner.
- **#1310** mail-send.sh residue tooling fix (reconcile-after-send) — until it lands, manually reconcile residue after each send.

**Still-open M3-era (verify relevance on pickup)**:
- **#1144** TEST-DISCIPLINE-REFACTOR (real SurfaceableInsight/ExtractedLearning fixtures).
- **#1131** CANONICAL-TODO-JUDGE-ARTIFACT (stateless judge flag).

**M5 / later**: #1300 BYOC-CRED-DECOUPLE, #1278 Fly hosting, #1305/#1306 (#1286 deferrals), #1105 LLM keychain UI, #1162 SKUNK.
**Closed (M3 cluster done)**: #1124 #1142 #1143 #1133 #1134 #976 #953 #669 #995 #1130 #1060 — all CLOSED (verified 2026-06-21).

---

## Cross-agent threads (who owes whom)

- **Arch** ← Lead: ratify the #1232 sum-type shapes (`44e505456`); confirm ADR-070 phasing for Phase-1. Then the ports unblock.
- **CXO** ← Lead: the Slice-2 radar-tiling decision (`e6decb14f`, 3 options) + the #1286 conformance review (Slice 1+3).
- **PM** ← Lead: Redis prod-fix go; #1286 mobile-nav phone UAT.

---

## Recurring infrastructure-health checks

- **Cron** `cbe956dc` armed (`5 5,8,11,14,17,20` — 05:05 morning, 20:05 day-close). Session-only, auto-expires 7d → re-arm on the cycle.
- **Inbox**: drain `mailboxes/lead/inbox/` to 0; move read items to `read/` per discipline.
- **mail-send.sh residue**: until #1310 lands, reconcile after each send (drop-local copies + FF-merge) before the next commit/merge.
- **Sync before commit**: `git fetch origin main && git merge origin/main` (the worktree branch is busy; FF races happen) — verify pushes land on origin/main by content, not exit code.
- **Briefing freshness**: if `BRIEFING-CURRENT-STATE.md` is > 7d stale, refresh via the `update-current-state` skill (any agent who notices — PM standing request).

---

## Pinned discipline reminders

- `feedback_close_issue_properly_skill_recurring_miss` — update description checkboxes BEFORE closing.
- `feedback_deferred_ac_self_justification_is_premature_closure` — use `[⏸]` for deferred verification.
- `feedback_ui_fix_requires_template_render_test_not_curl_200` — UI/runtime fixes need real-shape verification (template.render), not curl-200.
- `feedback_make_promises_durable_no_happy_talk` — install mechanisms (issue / hook / lint), not just promises (cf. #1310 filed over a vigilance-note).
- `feedback_commit_immediately_after_write_for_new_files` — untracked files at risk on shared trees.
- `feedback_careful_git_sync_on_shared_main` — commit own work BEFORE syncing; explicit paths only; verify by content.
