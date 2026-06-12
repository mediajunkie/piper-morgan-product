# Lead Developer session handoff — 2026-06-12 (Opus 4.8/Fable session → successor on designinproduct.com)

**From**: Lead Dev session of 2026-06-10→12 (the #1187→#1129 arc; session logs `dev/2026/06/10..12/*lead-code-opus-log.md` are the full record)
**To**: successor Lead Dev session (fresh duty cycle, designinproduct.com account)
**Read order**: this memo → today's session log (2026-06-12) → `dev/active/home-start-screen-design-2026-06-12.md` (CXO design + PM IA decisions).

---

## 1. Where M3 stands (close in sight)

**Shipped + CLOSED this arc** (all live-verified, most PM-UAT'd): #1187 (summarize issue — full chain), #1192 (GitHub last mile: connect/designate/project-resolution/honest panel), #313 (file browser complete + tags MVP), #1129 (**Slack inbound LIVE** — first since Oct 2025; PM uses it for M3 review), #1143 (composting dev-trigger + the persistence bug it caught), #1193 (session_scope commits + guard), #1194 (Recently module + Card design language), #1196–8 (honesty batch + guard), #953.

**M3 remaining (PM-triaged 2026-06-12 ~16:10; items 3–5 CLOSED ~17:05 — see below)**:
1. **#1122** (M3, In Progress on board): floor-path antecedent fix. Spec: thread a compact recent-turn antecedent frame into the floor prompt (ContextAssembler already gathers turns — gap is prompt-shaping); **acceptance gate = the two AAXT `TestContextRetention` golden scenarios** (`AAXT_ENABLED=true pytest tests/aaxt/ -k "not slow"`). ~1 session. **← successor starts here.**
2. **#1195 AutonomousExecutor wire** (M3, PM: "we'll never know till we try; alpha is safe"): wire `services/automation/autonomous_executor.py::execute_with_safety` into the pattern-application path, ALL safety gates intact (≥0.9 confidence, emergency stop, audit, rollback) + live-verify.
3. ~~#1188~~ **CLOSED 6/12**: humanizer pattern added (`user_friendly_errors.py`, `too short to summarize` → preserves the actionable message; Option 2 — better UX than fallback). Synthesis suite 25/25.
4. ~~#1200~~ **CLOSED 6/12**: Q25 verdict = **stale expectation, not misroute**. Routes to `list_milestones_query` (the real #1039 handler) by deliberate decision (#898 cites Q25 by name; #1039 shipped milestone queries) — both postdate the M2-Beta table. Expectation flipped `floor`→`canonical`, known-issue tag removed; all 5 Predictive pass. **Canonical routing gate now reads 0-failed** — no mental subtraction.
5. ~~#1189~~ **CLOSED 6/12**: all 15 stale routing tests repointed onto the dispatch rail (calendar-tests idiom). File 51/51 (was 36/15); full `tests/unit/services/intent_service/` dir **1660 passed, 0 failed**. Gate reads have zero standing noise from this file.
6. **#1165 UAT gate** (last, after the full canonical regression suite per PM sequencing): much organically covered 6/12 (files ops, home modules, Slack DM, honest greeting, connect+designate) — the formal checklist remains, incl. #953's 3 ⏸ ACs (restart/refresh/perf) and the env-error cascade work (12 env-errored canonical queries; session-leak + init-recursion asks recorded on the issue).

**PM-set sequence for successor**: (1) #1122 → (2) #1195 wire → (3) **full canonical regression suite** → (4) #1165 UAT gate. Expected canonical baseline after today's fixes: **49-50 pass / 0 fail** / 11-12 env-errors (the pre-existing resource-onset cascade — NOT a regression; recorded on #1165).

**Discovered-work filed at the tail**: **#1204** — two pre-existing error-suite breakages found while verifying #1188 (uncollectable `test_error_contracts.py` — imports a vanished module; dead user-guide-link assertion from the docs-architecture move). Unmilestoned, PM to triage. Per PM 6/12: pre-existing errors get logged for investigation — not allowed to persist just because they're old.

**Placed elsewhere**: #1190, #1199 → M4. #1203 (KeyAuditService) → M5. #1201, #1202 → PM placing (Lead leans: #1201→M4, #1202→Fast Follow).
**⚠️ Milestone vocabulary (PM correction 6/12)**: **M4 is part of the MVP milestone. "Fast Follow" is a separate milestone AFTER MVP.** Don't conflate.

## 2. Decisions of record (don't re-litigate)
- **Radar = A (umbrella), "eventually A" sequencing** (PM + CXO + **PPM concurred 6/12 ~16:40** — taxonomy note: Radar=surfacing-behavior layer, tags/projects=content-organization layer, orthogonal, no collision; memo in lead/read/). Cards ship now; Radar framing arrives as ambient streams accumulate.
- **Start screen: awareness-first**, chat input always visible; modules lead. Home-vs-chat split + module ordering → PM "Your stuff" IA session (covers tags+projects as the only two user-facing organizers, lifecycle invisible).
- **Greeting: server-side** (small slice next home touch; retire the `window.trustStage` JS greeting).
- **Tagging: freeform-with-emergent-promotion** (CXO); MVP shipped matches.
- **Radius tokens: incumbent `--border-radius-*` is canonical** (CXO #1172 call; the `--radius-*` scale was dropped 6/12).
- **#1185/#358 build order**: #358 storage floor → #1185 Gap A(ii); Gap A(i) (client-lifecycle + user_id threading) parallelizable earlier — Lead's M4-backlog option (PPM memo 6/12). #358 must be scoped user-secret-set-wide.

## 3. Environment / running state
- **Server**: dev server on :8001 from THIS worktree (`piper-morgan-product-1158-summarize-taxonomy`), env-stripped launch (see CLAUDE.md ANTHROPIC_* warning), with the **Slack Socket Mode runner attached** — restarting the server is what keeps inbound alive; if Slack stops answering, check `Slack inbound connected` in `/tmp/piper-server.log`.
- **Slack inbound**: app token in keychain `slack_app_token`; bot/user tokens user-scoped (`slack_bot`/`slack_user`, m1-test uid `009afc8c-…`). Single-tenant binding (events process as the token-holding user). NOTE: the xapp token PM pasted is in the 6/12 transcript — local dev token; rotate if it ever matters.
- **m1-test user**: Stage 4 (TRUSTED), GitHub PAT connected (keychain-first now beats the stale `.env` token — `.env` line 39 is expired and SHADOWED, not used; cleanup optional), default repo `mediajunkie/piper-morgan-product`, 34 repos selected, composted insights seeded.
- **Worktree/branch**: `claude/1187-floor-wiring` in the sibling worktree; everything is merged — the flow that works: commit on branch → `git push origin claude/1187-floor-wiring:main`. **Bridge debt**: the mailbox-on-main checkout fails from a worktree (main is checked out in the sibling repo) — mail commits ride the branch→main push; intent (mail on origin/main immediately) preserved; written procedure should be updated (raise with Docs/Arch — unraised as of handoff).

## 4. Guards + norms added this arc (the durable stuff)
- `TestPreFloorDispatchSiteRatchet` (dispatch sites = 0; lower the constant in the same commit when migrating).
- `TestSessionScopeCommitContract` (#1193: session_scope MUST commit on clean exit).
- `tests/test_honesty_guard.py` (#1196–8: banned robot-script phrases; first-person monitoring only; NEVER/Do-NOT-quoting lines exempt).
- **Pattern-073 item 6** (CIO-adopted, 6/12): any spec asserting code-state cites the file:line it checked (born from PA's `build_request` + CXO's radius-scale misses).
- **PM principles voiced this arc**: known failures are TASKS not workarounds (#1200's origin); `.env` is a floor not a ceiling (credential priority); every module gets an honest empty state; wire-the-unwired before sprint close; "Piper is an assistant-colleague, not a chat app."

## 5. Open threads beyond M3
- CXO "Your stuff" IA session (PM-watched) — decisions feed start-screen composition; greeting-server-side slice pairs with it.
- #1174 proactive-presence discovery + #1181 watch-fires — Radar-umbrella family.
- Robot-script MEDIUMs judged honest-in-context are recorded in #1198's close comment if voice standards tighten.
- Fable-model observation (PM asked): methodology dominated; gains were trace-holding + cheaper self-checking, not magic. Continue reporting honestly.

## 6. Non-obvious operational knowledge (tacit lessons that won't accrue from logs)

These are the things I'd have to rediscover the hard way; each cost real time once.

1. **`-o addopts=""` un-hides LLM-marked tests.** The default addopts excludes `@pytest.mark.llm` tests; overriding addopts (as the canonical-gate command does) runs them, and several fail for env reasons. If a suite "suddenly" shows extra failures under `-o addopts=""`, check markers BEFORE investigating — and conversely, the default run silently skips them, so a "clean" default run is not the same population. (Hit 6/12 with the error-message suites; the 8 "failures" were marker-population artifacts.)
2. **Live classifier ≠ unit-test classifier — learned patterns change the output shape.** For a RETURNING user, the full pipeline (learned-pattern/KG enrichment) can collapse to a bare `action` and OMIT slots (e.g. `source_type`) that a fresh classifier sets. Unit tests + in-process repros use fresh classifiers and will pass while live fails. **This directly threatens #1122**: an antecedent fix can pass both AAXT golden scenarios and still fail live for m1-test (who has learned patterns). Live-verify with the m1-test account specifically, not a fresh user. (This was #1187's final root cause, `15617d1cf`.)
3. **Expect the push race; it's not an error.** Main moves every few minutes (duty-cycle agents). `git push origin claude/…:main` rejecting with fast-forward hint is NORMAL — `git merge origin/main --no-edit && re-push` resolves it. Happened 3-of-5 pushes this afternoon. Don't read it as a conflict signal; do always re-verify `git branch -r --contains HEAD | grep origin/main` after.
4. **Canonical-gate triage norms** (so you don't re-derive them): (a) env-error count varies 11–12 by cascade ONSET, not by new breakage — tiebreak-rerun before calling regression (we did this 6/12; identical cascade, one query earlier). (b) After today, expected baseline is **49-50 pass / 0 fail / 11-12 env-error**. ANY failed test is now news, not noise — #1200 removed the last "known" subtraction.
5. **Probe technique for e2e questions**: drop a throwaway test file INSIDE `tests/e2e/` (conftest fixtures like `e2e_client`/`e2e_auth_headers` only resolve there), print routing + message, delete it. Faster + more honest than reasoning from code for "what does the user actually get" questions — found Q25's real behavior in one shot (~7s single-test runtime).
6. **Provenance trail for routing decisions lives in pre_classifier comments.** Pattern blocks carry issue numbers (`# Issue #898 Q25: …`, `# Issue #1039: …`). When a routing test fails, grep the pattern file for the term FIRST — the comment usually tells you whether the catch is deliberate and which issue ratified it. That's what made #1200 a 20-minute close instead of a re-litigation.
7. **Humanizer pattern table order matters** (`user_friendly_errors.py`): first regex match wins; specific before generic. When a user-facing error goes generic ("Something unexpected happened"), the tell in logs is `No pattern matched for error: <raw>` at `user_friendly_errors.py` — add a pattern that PRESERVES actionable phrasing rather than loosening the asserting test (#1188's resolution principle).
8. **Server-restart ritual completeness check**: after any restart, confirm BOTH `Slack inbound connected` AND the absence of `APIConnectionError` in `/tmp/piper-server.log`. The Slack runner riding the server process means a "successful" restart that forgot env-stripping kills LLM calls while Slack stays superficially alive (acks but errors on every turn) — a confusing half-dead state PM will hit from the Slack side first.

## 7. How this role works (the part that made this arc work)
Verify-first before extending — the week's biggest finds (session_scope, learned-patterns divergence, stale specs) all came from checking the actual thing instead of trusting the description. Live verification outranks green suites (mocked tests hid 3 of this week's real bugs). Ship small → PM pokes it → fix what reality says. Log every substantive unit WITH its commit. Evidence or it didn't happen.

— Lead Dev, 2026-06-12, end of arc
