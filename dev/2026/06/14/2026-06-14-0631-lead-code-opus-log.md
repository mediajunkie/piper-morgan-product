# Lead Developer session log — 2026-06-14 (Sunday)

**Role**: Lead Developer · Claude Code · Opus 4.8 · ephemeral worktree `interesting-beaver-7ee19c` (branch `claude/interesting-beaver-7ee19c`)
**Continuity**: new day. Yesterday `dev/2026/06/13/2026-06-13-0739-lead-code-opus-log.md` (DAY-CLOSED ✓ — 13 issues closed, M3 cleanup + flywheel: #1208/#1222/#1180/#1137/#1204 + the triage closes). Carry-forward: `dev/active/lead-carry-forward.md`.

## START — 06:31 PDT (PM-initiated; "ready to START + review what's still needed for M3")
- Step 0: 6/13 DAY-CLOSED ✓ (no self-heal needed). Sync clean. Lead inbox empty. Cron `0c673f7e` armed (next 7:17).
- **M3 review assembled** (authoritative source = #1165, the M3 closing gate). State verified via `gh`:
  - UAT-queue chat items **#1133 / #1155 / #496 / #497 / #1143 — all CLOSED** (code/server-side done); the gate tracks them for a live authenticated-browser confirmation.
  - **#1216** OPEN — confabulation symptom fixed (Lead guard shipped); provenance field = PPM follow-on (handoff sent), likely M4 / not M3-blocking.
  - **#1090** OPEN — History→Radar redesign (forward improvement; CXO entities-surfacing mockup pending); the #1133 History gate-item re-scopes to it.
  - **#1199** OPEN — default-repo unify — confirmed **M4** (PM 6/13), not M3.
  - Canonical suite green (243/0/0 after #1212 Q16 fix). All Lead code/test work for M3 is done.
  - **Net: M3 close = (1) PM's authenticated browser UAT walk + (2) the History→Radar scope decision (does M3 close on the current History UI, or wait for the Radar swap?). Not Lead-blocked.**

## Fire 1 (07:00 PDT — WORK: M3-close prep + server restart on latest)
- **M3 review delivered to PM.** PM gave conditional GO to close M3 + chose to do the UAT walk now.
- **#1090** now captures the History→Radar consolidation work, targeted **M5 polish** (PM's explicit M3-close condition) — comment posted (decision + design-then-build steps + "not an M3 blocker").
- **#1216 → M4** (Trust and Learning) + **#1224 → M5** noted on the issues (PM triage). **#1165** flagged ready-to-close on a clean walk.
- **Server restarted on LATEST** (PM: "restart to be sure"): worktree was behind → synced to `3673d45d7` (incl. cohort morning pushes); killed the Fri/auto-restarted server (57846); started env-stripped (port 5433, main venv, worktree cwd) → **PID 95577, health 200, clean boot**. **LLM path verified** — standalone `LLMDomainService.complete()` under the env-strip returned `'PONG'` (providers 1/1). All Saturday user-facing fixes (#1214/#1216/#1215/#953) now live, not just the gate items.
- gh-comment gotcha caught: inline `-c` with backticks triggers shell command-substitution → #1216/#1165 silently no-op'd; re-posted via `-F` files (verified).
- Standing by to close #1165 → M3 on PM's walk-pass.

## Fire 2 (07:00–07:28 PDT — M3 gate walk w/ PM; connector-model debt surfaced)
PM ran the gate walk one item at a time. **Item 1 (#1155 "what should I work on?") FAILED live**: chat gave a generic calendar greeting + "what i'm seeing" showed GitHub *"no open issues"* (repo has many).
- **Diagnosed — NOT a code regression**: GitHub token PRESENT (40-char PAT, user `xian@pobox.com`); failure was `resolve_repo → UnresolvedRepoError`. PM had no default repo: no UI prefs, no `PIPER_DEFAULT_REPO`, and **0 `project_repository_links` DB-wide** → the #1192b default-project path is non-functional for *everyone*.
- **Band-aid**: wrote `data/github_preferences.json` (PM → `mediajunkie/piper-morgan-product`); `resolve_repo` now returns it (source=`user_default`; fresh-read per call, no restart). Item-1 re-test pending PM.
- **Connector-model debt → filed #1226** (refactor-sprint input): repo-resolution churned 3× in 5 wks (#1042 May 4 removed the hardcoded shim → #1192a Jun 11 prefs-bridge → #1192b Jun 12 default-project w/ 0 data); the prefs store is a **cwd-relative flat file** (fragile across launch dirs — likely why "worked then broke"); silent-fail (no honest "configure a repo"); stacks #1199 (two competing stores). **PM signaled a connector-refactor sprint — I backed it with scope in #1226.**
- **Also filed #1225** — home "what i'm seeing" modules have no minimize/dismiss (PM flag; M5 polish).
- **HELD for PM**: keep walking the gate now (items 2–5: #496/#497/#1133/#1143) vs. pause + scope the connector sprint. PM's call.

## Fire 3 (07:30–07:45 PDT — connector-refactor sprint SCOPED, per PM)
PM chose: scope the connector-refactor sprint first (decomposable markdown) → then return to the gate walk.
- **Grounded the current-state across ALL connectors** (not just GitHub): cred storage = 4 different conventions across github/calendar/slack/notion; config = **cwd-relative flat files for ALL FOUR** (`data/*_preferences.json`); resolution ad-hoc w/ dead paths (0 `project_repository_links` DB-wide); silent degradation; native-vs-MCP fork already filed as **#1220**.
- **Wrote `docs/internal/architecture/connector-refactor-sprint-scope-2026-06-14.md`** (DRAFT for PM+Arch): trigger (#1226) → current-state map → 8 systemic problems (P1–P8) → target principles → **8 workstreams (WS-1..8) decomposable into issues** → proposed phasing (**Phase 0 = the #1220 MCP fork, gates everything**) → open questions → related issues (#1199/#1226/#1109/#1110/#1220 absorbed).
- **Key fork for PM/Arch**: native-vs-MCP (#1220) — recommend deciding it before filing the issue tree (so we don't decompose against the wrong topology).
- Next: PM reviews → decompose into issues → return to the gate walk (item-1 re-test still pending).

## Fire 4 (07:36 PDT — DECISION: PM ratified MCP for connectors)
PM reviewed the scope doc ("excellent") + made the Phase-0 call: **connectors go MCP, not native** ("the direction everyone is moving in; native is dated and clunky"). Recorded:
- **Scope doc §0** = the DECISION (resolves OQ#1; Phase 0 → "design," not "decide"). Implications: WS-5 = the MCP-consumer contract; WS-8 = native→MCP migration; auth/config likely shift to the MCP layer (structurally kills the #1226 silent-config class); foundation = `services/mcp/consumer/` adapters.
- **#1220** = the migration umbrella (commented).
- **Arch handed the ADR + substrate design** (memo via bridge) — PM ratified the *direction*; Arch owns the *how* (auth model, per-connector path, MCP-server maturity per connector).
- **Decompose into the WS-1..8 issue tree AFTER Arch's topology/ADR lands** (don't decompose against the wrong shape). No M3 dependency (M4/M5).
- Next: return to the gate walk (item-1 re-test).

## Fire 5 (08:00 PDT — Slack-test attempt → multi-identity gap)
PM at the farmers market on mobile (can't reach localhost:8001) asked to test the floor via Slack. Found: **web login ≠ Slack bound user** — web `a25db09c` (xian@pobox.com) vs Slack bound `009afc8c` (`_resolve_bound_user` = first user holding a `slack_bot` keychain entry). Config (default repo) set on one identity doesn't apply to the other → "no open issues" recurs per-identity.
- **Band-aided 009afc8c's default repo too** (prefs file now keys both → mediajunkie/piper-morgan-product) so the Slack test is valid. Compounds the fragility — clean example of the connector/identity no-unified-home problem. **Noted on #1226** (refactor must treat "one human, multiple connector identities" first-class; check duplicate user records).
- PM can now test item 1 via Slack ("what should I work on?") — validates the floor + the Slack inbound path (#1129), via the Slack identity. Caveat surfaced to PM: it's a 2nd band-aid + a real finding.

## Fire 6 (08:18 PDT — gate item 1 PASSED (Slack); M3-close triage drafted)
- **Gate item 1 (#1155) PASSED** — PM tested via Slack → Piper returned real GitHub issues + a strong PM-level triage of the backlog (cited #1165/#1223/#1218/#1216). The floor is working well enough to triage its own work.
- **Slack formatting bug → filed #1227**: Piper's Slack reply rendered raw markdown (`**` / `#`) instead of Slack mrkdwn. Beta UX (Slack-outbound formatter fix).
- **M3-close triage drafted** → `docs/internal/planning/m3-close-triage-2026-06-14.md`. Headline: **M3-close is gated by #1165 ALONE** (days, not weeks); the ~76 MVP-open issues are M4/M5/Fast-Follow tagged to the July-4 umbrella, NOT M3-close blockers. Cuts: M3-blocker (just #1165) / beta-must-fix (#1223/#1218/#1217/#1216 + security #358) / connector→M4-M5 / M4 trust-learning / M5 polish-distro / Fast-Follow. Caveat: board Iteration field = source of truth (best-effort cut).
- **Next**: finish the #1165 walk (items 2–5) → close M3.

## Fire 7 (09:01 PDT — M3 gate walk COMPLETE; ready to close)
- **Items 1–3 ALL PASS via Slack (PM live-tested)**: #1155 ("what should I work on?"), #496 ("what's my top priority?"), #497 ("what should I focus on?") — each returned real, specific, synthesized priorities citing actual backlog issues (#1227/#1220/MVP-burn). The floor works end-to-end.
- **PM quote (for the log)**: *"alpha — almost beta — Piper Morgan is a good PM assistant!"* 🎉
- **Item 4 (#1133 History sidebar)** — browser-only + being **re-scoped to Radar** (M5, #1090); recommend NOT blocking M3-close on a live walk of a transitional surface (closed-on-evidence; Radar replaces it).
- **Item 5 (#1143 composting)** — Lead-verified server-side earlier (affordance + #1033 reflective framing + #1035 persistence); not cleanly Slack-walkable.
- **→ Gate effectively satisfied**: user-facing floor (1–3) PM-verified live; 4 re-scoped; 5 Lead-verified. **#1165 ready to close → M3 ready** (PM's #1090-captures-Radar condition is met). Recommending close to PM (or a desktop spot-check of 4/5 first).
- **Typing-indicator UX note → filed #1228** (signal "thinking" vs frozen; non-blocking, beta).

## Fire 8 (10:21 PDT — duty-cycle tick + M3 GATE CLOSED 🏁)
Tick fired mid-conversation (10:17); light hygiene (cron healthy `0c673f7e`, sync clean, inbox empty) — then **PM gave the close-go ("close it!")**.
- **#1165 M3 CLOSING GATE — CLOSED ✅.** All 6 queue checkboxes marked + evidence trail on the issue: #1155/#496/#497 (PM live, Slack), #1133 (PM live, browser), #1143 + #953 (Lead server-side). History→Radar re-scoped (#1090, M5); GitHub-config band-aid noted (real fix = connector refactor #1226/#1220, MCP).
- **M3's gate is cleared → M3 ready to close at the board level** (PM's call to move the iteration).
- **Next** (per `m3-close-triage-2026-06-14.md`): beta-must-fix (#1223/#1218/#1216 + security #358) + the connector refactor (MCP, awaiting Arch's ADR) + board re-tag of the ~76 MVP-umbrella issues.
- Cron kept armed throughout (Rule 2). **The M3-close thread is complete.**

## Fire 9 (11:38 PDT — project-board access LIVE; M4 pull + assignment check + sequencing)
PM increased the GitHub PAT scope (project info) + asked to pull the M4 sprint. **Board access via gh now works.**
- **Board "Sprint" field** (single-select) holds the iterations. **M4 = "M4 - Trust + Learning" = just 2 items** (#558 MUX-STANDUP-CONVERSE, #302 CONV-MCP-DOCS, both Product Backlog) — confirms M4 is light.
- **Milestones NOT wrong (PM #1)** — I conflated milestone (MVP, correct) with the Sprint field (the iteration). Withdrew the "re-tag" suggestion; no milestone fix needed.
- **Assignments (PM #2)** — most ARE sprint-assigned; only **5 OPEN issues lack a Sprint**: #57/#58/#65/#66/#87, all old `FEAT-*` vision items (transcript/dashboard/vision/predict/graph) → look Post-MVP/icebox. Surfaced to PM (assign Post-MVP or close won't-do; not auto-acting — product-scope + write-access TBD).
- **Sequencing (connector vs M4)** — my read: lean connector-foundation BEFORE/early-M4, because **M4's Trust+Learning depends on unified identity** (= the connector refactor's WS-9 — can't "learn about the user" coherently with fragmented web/Slack identities) + the connector debt is biting + M4 is light (little to delay). PM/Arch's call; Arch's ADR informs timing.
- Mail: lead inbox empty.

## Fire 10 (12:0x PDT — CORRECTION: Fire 9's gh-board numbers were wrong)
PM caught it ("M2 has more than two items… can't rely on your gh view"). **Two bugs** in the Fire-9 analysis:
1. **Truncation** — `gh project item-list --limit 400` returned exactly 400, but the project has **1057** items → missed 657; tail-end sprints (M4, recent) badly undercounted.
2. **`comm` sort bug** — cross-refs used numeric-sorted files with `comm` (lexical compare) → wrong intersections (the "5 unassigned" was bogus).
**Corrected (full 1057 pull + `grep -xF` set-ops, verified):**
- **M4 - Trust + Learning = 16 tagged / 15 OPEN** (NOT 2/light): #302/558/712/713/954/955/956/1062/1166/1190/1199/1209/1211/1216/1217. M4 already CONTAINS connector/identity work (#1199 store-unify + #954/955/956 trust-lite/pref-infer/learning-surface).
- **Open-unassigned = 49** (NOT 5): ~17 recent (need sprinting — #1108/1109/1110 Slack, #1169–1174 UI design-floor, #1203 KeyAudit, #1011/1045/1051/1152/1154/1179/1181) + ~32 old/legacy (icebox/close — #57–716). Total open = 141.
**Downstream corrections**: "M4 is light" premise was WRONG (15 open). Identity-dependency argument for connector-before-M4 STANDS (and #1199 is literally already in M4). Assignment gap is real (49, not 5).
**Lesson/guard**: when a pull's count == the limit, suspect truncation (pull full / paginate); use `grep -xF` (not `comm` on numeric-sorted) for issue-number set-ops. PM was right not to trust the first view.

## Fire 11 (12:1x PDT — triage scope clarified → real set = 7; Production milestone planned)
PM scope clarification: only issues needing triage NOW = **MVP-milestone-no-sprint OR no-milestone-no-sprint** (open). Post-MVP/Fast-Follow/Enterprise issues legitimately have no sprint yet. (My Fire-10 "49" was raw open-no-sprint across ALL milestones — over-scoped; plus a 3rd bug: `.milestone|test("MVP")` matched milestone *descriptions* too, leaking Fast-Follow/Post-MVP. Fixed: `.milestone.title=="MVP"` exact.)
- **Real triage set = 7** (verified, all MVP, no sprint): #1169–1173 (DESIGN-FLOOR epic + F1/F2/F3/C1 UI remediation), #1174 (proactive-presence), #1203 (KeyAudit "deferred M5"). No neither-milestone-nor-sprint cases (all open issues have a milestone).
- Suggested homes (PM's call): #1169–1173 → M5/Production (UI polish); #1174 → M4; #1203 → M5.
- **Roadmap (PM planning)**: new **Production milestone** between MVP & Fast Follow. **MVP = Beta 0.9; Production = 1.0; Fast Follow = 1.01/1.1.** → some MVP-tagged work (UI design-floor, #358 encryption-at-rest) may belong in Production (1.0), not 0.9-beta.
- **Errors owned this pass**: (1) 400-limit truncation (real total 1057), (2) `comm` on numeric-sorted files, (3) milestone-substring match. 3 bad intermediate numbers before the verified 7. Slowed down + verified each. Board access itself is fine; my queries were sloppy.

## Fire 12 (14:3x PDT — board-structure doc → canonical home; 4-sprint evaluation)
- **Moved PM's board-structure doc** → `docs/internal/planning/sprint-board-structure.md` (date dropped → living doc); images → `docs/assets/images/sprint-board-milestones-{completed,open}.png` (renamed, **force-added past .gitignore `*.png`** — android-chrome precedent); NAVIGATION.md pointer added (PM/planning section, "read before board ops"); old dev/active draft+assets removed. Commits `6282d6971` + images commit.
- **4-sprint evaluation** (verified, full 1061-item pull, Python set-ops):
  - **M4 - Trust + Learning**: 15 open — trust/learning (#954/955/956/1062/1166), identity/connector (#1199/#1216/#1217), autonomous-exec (#1209), doc-UI (#712/713), MUX (#302/558), sweep (#1211).
  - **RECONNECT - Connector Refactor**: 1 open (#1226) — needs populating.
  - **D1 - Beta design quality**: 9 open — design-floor (#1169–1173) + proactive-presence (#1174) + UX bugs (#1225/#1227/#1228).
  - **M5 - Distribution + Polish**: 45 open — the big final bucket (DIST-*, security #358/482/542/441, infra, test-debt, #1220 MCP-umbrella, #1223/#1218 beta-bugs, #1090).
- **RECONNECT-population proposal** (PM applies, per boundary): move #1220 (M5→) + #1199 (M4→) into RECONNECT w/ #1226; flag #1227 (D1, connector-adjacent) + #1109/#1110/#1201 (Slack, Post-MVP/no-sprint) for PM; full WS-1..9 decomposition awaits Arch's ADR.
- **"Which next" recommendation**: **D1 now** (fully unblocked, self-contained, beta-UX value) while **Arch designs the RECONNECT ADR** (gates the connector build + M4's identity-dependent items) → RECONNECT → M4 → M5 (last). Plus pull beta-must-fix correctness bugs (#1223/#1218/#1216) forward regardless of sprint.

## Fire 13 (15:0x PDT — RECONNECT decomposed + D1 build order; board verified 1061)
PM agreed sprint order (D1 → RECONNECT → M4 → M5), moved 6 issues into RECONNECT (#1220/#1199/#1227/#1109/#1110/#1201 + pre-existing #1226 = 7) and pulled #1223/#1218 into D1 (now 10). PM: "you can do these things [board ops] when I authorize." Two deliverables requested: decompose RECONNECT + plan D1 order.
- **Board re-verified**: full pull = **1061 items, not truncated**. RECONNECT=7, D1=10 — both exactly match PM's moves.
- **RECONNECT decomposition** → appended **§10** to `connector-refactor-sprint-scope-2026-06-14.md`: §10a existing 7 → workstreams (cover WS-1/6/7/8; WS-3/9 seeded); §10b NEW issues proposed for **WS-2 / WS-4 / WS-5 (=ADR output) / WS-9** — **filing ADR-gated** (MCP §0 reshapes WS-1/2/5; PM nudging Arch); §10c **#1227 = the one ADR-independent quick win**. No filing, no board mutations (proposals only).
- **D1 build order** (proposed, awaiting PM bless): Track A quick wins (#1223 backend-correctness / #1225 / #1228, parallelizable) · Track B design-floor sequential under #1169 (tokens #1172a → Dialog #1170 → shell #1171 → chat-page #1173 → CI-gate #1172b LAST; recommend splitting #1172) · Track C parked (#1218 BLOCKED on PA capture; #1174 reads M4-flavored).
- **Boundary updated** in carry-forward: board ops OK **when PM authorizes** (was read+propose-only).
- **PROCESS NOTE (path-trap)**: first attempt wrote all 3 edits to bare main-checkout paths → lost (the shared main tree also actively reverts files); re-applied to worktree paths. Added a WRITE-TO-WORKTREE-PATHS guard to carry-forward Constraints.
- Cron `0c673f7e` healthy (single, armed). Commit: scope-doc §10 + carry-forward + log.

## Fire 14 (15:3x PDT — RECONNECT issues FILED + prefixed; first board write)
PM authorized: "create the new WS issues — feel free to rename others… Arch is working… Quick wins start sounds great!" First real board-write op (per the board-ops-when-authorized boundary).
- **Created 5 new issues** (milestone MVP, assignee mediajunkie): **#1229 WS-2** (credential model), **#1230 WS-3** (resolution correctness), **#1231 WS-4** (honest-degradation contract), **#1232 WS-5** (MCP-consumer contract = Arch/ADR output), **#1233 WS-9** (identity unification). Bodies cross-ref the scope doc per workstream.
- **Board-placed all 5**: Sprint=RECONNECT (opt `a838c1e7`), Status=Product Backlog (opt `e7d1c990`), via `gh project item-add` + `item-edit` (project `PVT_kwHOADE-8s4A-JwA`; Sprint field `…zg2hWcg`, Status field `…zgxpGyU`).
- **Renamed the 7 existing** RECONNECT issues to `RECONNECT-WS{n}:` prefix (#1226/#1199 WS-1, #1201 WS-6, #1109/#1110 WS-7, #1220 WS-8, #1227 discrete quick-win).
- **Verified**: RECONNECT = **12 items**, all Product Backlog/MVP, all 9 workstreams covered, clean prefixes (full board pull, 1066 items, not truncated).
- §10 of scope doc updated PROPOSED→FILED; carry-forward updated.
- **Board-ops mechanics learned** (for future skillify): field IDs + option IDs captured in this entry; `item-add --format json` returns item id → `item-edit --id … --field-id … --single-select-option-id … --project-id …`.
- NEXT: start Track A quick wins, #1223 first (PM-approved).

## Fire 15 (15:4x PDT — #1223 FIXED (D1 quick win 1/3) + #1234 filed)
First D1 quick win. **#1223** — `get_recent_turns` DB fallback returned OLDEST-N not newest-N (cold-cache → "recent" context = conversation's oldest turns).
- **Fix** (caller-safe `most_recent` param, per the prior caller analysis — NOT a blind DESC flip): added `most_recent: bool=False` to `ConversationRepository.get_conversation_turns` (DESC+limit+reverse → newest-N chronological); default preserved so the web conversations API (conversations.py:97/182) is untouched. Switched the two recent-context callers to `most_recent=True`: `_get_from_database` (cm:301) + `reference_resolver._get_conversation_history` (rr:358).
- **Tests**: removed the `xfail(strict)` marker on `test_conversation_window_management` (it now passes — returns Messages 6–15); added `test_get_conversation_turns_most_recent` (newest-N + default-unchanged regression guard). Verified: 5 conversation_turns/window tests PASS, web conversations unit 7 PASS.
- **Discovered (filed #1234)**: 2 PRE-EXISTING failures in `test_reference_resolver.py` (`test_context_window_limitation` — `_find_candidates` ignores the 10-turn window, #1223-adjacent; `test_definite_reference_resolution` — 66.67% < 90% accuracy). Stash-verified pre-existing (fail on clean tree); NOT in #1224's clusters. Un-sprinted for PM triage.
- Files: repositories.py, conversation_manager.py, reference_resolver.py, 2 test files. NEXT: #1225 / #1228 (Track A remainder).

## Fire 16 (16:0x PDT — audit cascade on the 14 filed/touched issues; grounding verified + corrections + ADR gap + #1235)
PM: "run full audit cascades on these issues to ensure grounding in docs, actual code, and recent planning and insights." Ran **5 parallel general-purpose audit agents** (config/creds · resolution/degradation · MCP+Slack-conn-state · identity+#1223+#1234 · docs/planning/insights), each grounding every claim against real code / live DB / docs, try-to-refute stance.
- **VERDICT: well-grounded, nothing fabricated.** Empirical claims verified TRUE (several understated): `project_repository_links`=0 AND `repositories`=0 AND 0 default-projects (ALL 3 DB resolution paths dead); §2a cred table accurate connector-by-connector; 6 MCP adapters confirmed; no `Connector` protocol (WS-5 greenfield); both identity records real in live DB (a25db09c=xian/xian@pobox.com web; 009afc8c=m1-test/m1t@dinp.xyz Slack).
- **Corrections applied** (scope §2a/§2c + comments #1226/#1229/#1230): resolve_repo is **5 paths not 4**; DB-dead understated (repos table empty + 0 default projects); stale 3rd GitHub reader `get_api_key("github")` (intent_service.py:6254/6416); band-aid prefs file now exists.
- **Most important gap (→ Arch, on #1232 + scope §11): ADR grounding missing.** **ADR-058** (multi-tenancy) already decided the WS-2/7/9 cred/OAuth/user-scoping model → much of RECONNECT *finishes ADR-058*, not greenfield. **ADR-001** supports MCP-consumer; **ADR-052** (tool-based, no separate servers) needs reconciliation in the WS-5 ADR. Commented on #1232.
- **New latent bug filed #1235**: `/turns` display endpoint returns oldest-50 (no offset param) for >50-turn convos — #1223-shape, display path, lower severity.
- **§0 MCP decision recorded in decisions.log** (was scope-doc/memo/session-log-only — the flagged process gap; cross-poll Insight #4 is literally "decisions referenced as if written").
- **Honest caveat surfaced**: "same human" for the 2 identities is plausible but NOT proven (different usernames/emails; 009afc8c reads as a test acct) — #1233 already carries this as an open question. Good.
- Artifacts: scope §2a/§2c/§8/§11; #1235 filed; comments #1226/#1229/#1230/#1232; decisions.log entry. NEXT (unchanged): #1225 / #1228.

## Fire 17 (16:xx PDT — the REAL /audit-cascade skill: 12 RECONNECT issues → full feature.md conformance)
**PM correction**: Fire 16 was a claim-grounding pass, NOT the `/audit-cascade` skill. The skill (Pattern-049) is TEMPLATE-conformance auditing — the prospective FRONT bookend of the excellence flywheel (vs `close-issue-properly` = back bookend). Owned the miss, read + invoked the actual skill.
- **Issue-phase audit** (skill Step 2): all 12 RECONNECT issues vs `.github/ISSUE_TEMPLATE/feature.md` (the features/fixes/refactors template — correct for all 12; bug_report_alpha.md is for tester-submitted bugs). Matrix → all 0–3/16 sections (scoping-level). Doc: `dev/2026/06/14/RECONNECT-issue-phase-audit.md`.
- **Bar decision** (skill critical rule: ZERO authorization to mark requirements N/A without PM): ADR-gating made "full now" non-trivial → surfaced via AskUserQuestion. **PM chose Option B — full conformance now** for all 12.
- **Fix** (skill Step 3): 5-agent fan-out, each cluster rewriting to the full 16-section template, grounded in the audit's file:line facts + scope doc, ADR-dependent specifics flagged `(provisional — refines once ADR #1232 lands)`, titles untouched.
- **VERIFIED** (re-ran section-presence audit): all 12 now **16/16**; bodies ~14–22 KB (was 0.7–3 KB). Spot-checked #1232 = grounded/honest, not filler. #1227 fully concrete (0 provisional); #1233 keeps "same human" as a gating Phase-0 open question.
- Issue gate COMPLETE. Next cascade gates (Gameplan→Prompts→Execute) run per-WS post-ADR.
- **LESSON**: when PM names a skill, USE IT — don't improvise a same-named thing. Both passes had value (claim-grounding + template-conformance) but they are different gates. Added the distinction to memory.
- Note: a fix-subagent created its own session log (`2026-06-14-1600-code-opus-log.md`) + pushed to main — expected for substantive subagent work.

## Fire 18 (16:37 PDT — DUTY-CYCLE WORK fire: mail triage + ADR-066 D7↔RECONNECT grounding)
Cron fire (16:17 slot; next 19:17; last-of-day 22:17 → not STOP). Cron healthy (single job `0c673f7e`, armed). Sync clean (HEAD==origin/main). PM mid-conversation w/ pending choice (#1225/#1228 vs more wrapping) → held that thread; advanced OTHER unblocked work per the pending-question rule.
- **Mail**: 2 CC memos in lead inbox → triaged to lead/read/ via main bridge (regen MANIFEST, commit `587858ba7`). (1) Docs: sprint-structure reconciled into roadmap/briefing, PPM owns the version fold, flagged RECONNECT as my scoping lane (awareness). (2) Arch: **ADR-066 v0.2 D7 Configuration Ownership** drafted.
- **ADR-066 D7 ≠ the connector ADR** (it's packaging/hosting / BYOC). But **D7 governs RECONNECT WS-1/WS-2**: config/credential durability is **server-owned**; host does per-request ephemeral augmentation only; config never crosses host↔server as durable state. This *supports* the RECONNECT direction (DB-backed config store, kill cwd-relative flat files — a host-fs assumption D7 forbids). Grounded the link in scope **§8** + carry-forward.
- **Owed (future, not now)**: Lead Dev **D7 OQ-1** consult (handshake-materialization timing) when Skunkworks BYOC **Phase 2a** scopes. Queued in carry-forward.
- Left the shared main checkout's other untracked logs (Web/omnibus) untouched — not mine (explicit-paths discipline).
- HELD for PM: #1225/#1228 vs more flywheel-wrapping (the question I asked). Re-armed (Rule 2 keep-armed).

## Fire 19 (17:0x PDT — PM "quick wins ok, flywheel for everything else" → #1228 Slack shipped; #1225 + #1228-web → Web)
PM answered the held question: **"quick wins ok but flywheel for everything else."** Captured the rigor-calibration in carry-forward Constraints (quick wins proceed direct: implement + real-render test + Review; substantive = full flywheel — audit-cascade gates + close-properly).
- **Collision check before touching frontend**: Web agent ACTIVELY in exactly these files — `c3ee98ac8` home modules re-skinned, `ac0f3aa86` "What I'm seeing" panel wired (#1192d/#1195/#684), `a65aa5451` design-floor #1172 tokens. → #1225 (home modules) + #1228 web-chat half = Web's active lane.
- **Coordinated split** (lane-respecting, collision-avoiding): I shipped the **#1228 Slack half** (connector backend, mine); handed **#1225 + #1228 web-chat half** → Web (memo `f6a0ac5b6` / `c708a088d`).
- **#1228 Slack** (`socket_mode_runner.py`): `_…thinking…_` placeholder before `process_intent` → `chat.update` in place with the reply (or honest error — never stuck at thinking); fallback to fresh post if placeholder/update fails. 4 unit tests (happy / processing-error / update-fail / placeholder-fail); full slack unit suite green (157 passed, 2 skipped). Commit `d1cd99ca6`. #1228 → In Progress + evidence comment.
- **#1227** (Slack mrkdwn) deliberately NOT bundled — it's RECONNECT *flywheel* work (despite being ADR-independent), not a D1 quick win, per the calibration.
- NEXT: #1228 fully done when Web lands the web-chat half; D1 Track A is otherwise clear on my side (#1223 Review, #1228-Slack done). Awaiting PM / Web.

## Fire 20 (17:2x PDT — CORRECTION: misattributed product front-end to Web; withdrew the mis-routed handoff)
PM flagged: **Web works on the WEBSITE** (`piper-morgan-website`, a different repo), not the product; PM was worried Web had "gone off the rails" into product work — a worry triggered by MY Fire-19 report.
- **Verified**: Web's role = "Unicorn Web Designer (piper-morgan-website)"; latest web log (6/13) = website blog-type work, explicitly "Product main: nothing affecting web"; **no web log references any product issue**. The product front-end commits I'd flagged (#313 / #1192d / #1194 / #1172 design-language / #1215 / home-modules / "What I'm seeing") were **my own earlier sessions + CXO's** (lead + cxo logs claim them) — NOT Web's.
- **My error**: saw product front-end churn → ASSUMED "the Web agent's lane" → routed #1225/#1228-web to Web + alarmed PM, all on an **unverified lane assumption**. Web is in-lane; I manufactured the false alarm.
- **Corrected**: WITHDREW the mis-routed handoff (`git rm`) + sent Web a truthful lane-reconciliation memo (cc PM) — disregard the handoff (my error); drop PM a line on your focus to close the loop. **Adapted PM's "tell them you're finding conflicts" framing** → sent the honest "no conflict, my misread" version (surfaced the adaptation to PM, since the premise had flipped). Commits `6c5c1210e` / `2b5ce3254`.
- **#1225 + #1228 web-chat half: ownership now OPEN → PM to assign** (product front-end = Lead + CXO; #1225 design-quality likely CXO). Did NOT re-route (the very error I'd just made).
- **LESSON**: detect a cross-lane anomaly → VERIFY the lane (role/log) + FLAG to PM; don't rationalize into an action; don't unilaterally route cross-lane work (PM in the division-of-labor loop).
- Per PM: "flywheel next but need to sort this first" → #973 flywheel waits until PM closes the Web/lane question.

## Fire 21 (18:0x PDT — D1 batch: #1174→M4, #1218 closed, #1228 done; PM methodology+lane clarifications)
PM clarified: (a) **#973/MEM = Q-sprint, NOT D1 — dropped**; (b) **"flywheel" = full `/audit-cascade`** (issue✅→gameplan+audit→subagent-prompts+audit→execute) **+ DDD + TDD** for non-quick-wins; (c) I'm **cleared for all product dev**; (d) **#1228 mine**; (e) **design-floor #1169–1173 = Lead builds + CXO guidance-logged-first** ("your voice matters").
- **Board ops (PM-authorized)**: #1174 (proactive-presence) Sprint→**M4**; **#1218 CLOSED** (cannot-reproduce — PA exhausted direct + consult-piper; left as findable anchor if it recurs) + Status=Done.
- **#1228 DONE → Review**: the web-chat half **already existed** (chat.js:504 "Thinking..." + `.thinking`, shown on send / replaced on reply) but was **static**. Completed-in-place (NOT rebuilt — STOP cond #3 "complete don't duplicate"): opacity-pulse animation on `.bot-message.thinking` + `prefers-reduced-motion` fallback (`9ae3f03bd`). Both halves done (Slack `d1cd99ca6` + web). Evidence on issue; CXO can restyle under conformance.
- **"Clean backend pickup" = none (PM caught my contradiction)**: #1218 was non-reproable → a close, not a pickup. With #1223 done + #1218 closed + #1228 done, **remaining D1 is FRONTEND** (the #1169–1173 design-floor) — no separate backend pickup. (Fine — cleared for product/frontend dev.)
- **#1223 test**: re-verified green (5 passed). User-test = long convo (>10 turns) + cache miss (restart) + ask recent-context → uses newest not oldest. In PM's Review queue.
- **CXO design-floor guidance: doesn't exist yet.** Lead inbox empty (no CXO memo). CXO's mockup (`radar-entities-surfacing-mockup-2026-06-14.html`) = the **Radar/home redesign**, NOT the design-floor (#1169–1173 = Dialog/shell/tokens/chat-page). CXO log says "#1169 conformance when Lead ships" queued → CXO's model is **review-AFTER**; PM wants guidance-**BEFORE**. Mismatch surfaced to PM; awaiting PM's call on how to log CXO's guidance (I request vs PM coordinates).

## Fire 22 (18:1x PDT — #1223 CLOSED via /close-issue-properly (PM-approved); CXO design-floor memo incoming)
- **#1223 closed properly** (PM approved on the tests + review). Ran `/close-issue-properly`: Step 3 description update FIRST (✅ RESOLVED banner + caller-safe `most_recent` design + verification: 5 tests green, xfail removed, files) — no checkboxes in the body but the banner+evidence went in the DESCRIPTION, not just a comment (avoids the comment-only-close anti-pattern); then closing comment → `gh issue close` → board Status=Done. No `bd` CLI (skipped sync). Fix commit `07826c74a`.
- **D1 my-side: CLEAR.** #1223 closed, #1228 done→Review, #1218 closed, #1174→M4, #1225→CXO-redesign. Remaining D1 = **design-floor #1169–1173** (Lead builds + CXO guidance-first).
- **CXO design-floor memo INCOMING** (PM: "crisp and I love it"). **Holding the build for it** — NOT sending my own request (PM/CXO have it). When it lands → full flywheel per issue (gameplan+audit → subagent-prompts+audit → execute) + DDD + TDD, order tokens(#1172a)→Dialog(#1170)→shell(#1171)→chat-page(#1173)→CI-gate(#1172b).

## Fire 23 (18:2x PDT — CXO #1090 Radar build handoff received; Verify-First recon; flywheel plan; nod-ask on issue-carve)
PM "you have mail" → CXO memo = **#1090 Radar/entities-surfacing slot-swap HANDOFF**, mockup = the binding spec (`dev/active/radar-entities-surfacing-mockup-2026-06-14.html`), PM-ratified + loved; **#1090 now in D1** (was M5 in my notes — corrected). NOT the design-floor #1169–1173 (those specs still pending). Triaged to read/ (`a3f180a66`/`51388f7e3`).
- **Verify-First recon (flywheel start)**: spec = two states (default real-only / empty explainer+1 example), 4 entity types (WorkItem/Conversation/Person/Document), lifecycle badge, honest provenance (● observed / ○ example), attention-first, entity-search-subsumes-chat. **Slot** = `templates/components/history_sidebar.html` (739L). **Backends**: conversations = `web/api/routes/user_history.py` (#1021); **entity-catalog (#706) backend DOES NOT EXIST** (only MUX design catalogs `docs/internal/design/mux/`) = the PPM entity-model dependency. **Card** = `cards.css` + `insight_card.html`; home Radar modules = `place_window.html`/`insight_card.html`.
- **#1090 is a scoping TRACKER** ("the actual UI work will land as separate tickets") → flywheel issue-gate = **carve a focused implementation issue** (child of #1090), not build under the tracker. **Awaiting PM nod** (board op) before creating it.
- **Plan (full flywheel — substantive)**: carve issue → gameplan+audit (DDD) → prompts+audit (if fan-out the render work) → TDD build → close-properly w/ CXO's Layer-2 closure gate (cite PDR-002 + the mockup). Build the surface + wire conversations (#1021) + home Radar modules; slot WorkItem/Person/Document as PPM lands the entity model (PPM cc'd on CXO's memo).
- NEXT: on PM nod → create the implementation issue, then gameplan.

## Fire 24 (18:3x PDT — #1090 Radar build: issue gate + gameplan gate done)
PM nodded → ran the flywheel's first two gates:
- **Issue gate**: carved **#1236** (RADAR entities-surfacing slot-swap), feature.md-conformant, D1/MVP/In-Progress, child of #1090 (link comment on #1090). AC = mockup spec + 6 build points + **Layer-2 closure gate** (cite PDR-002 + mockup) + PPM dep.
- **Gameplan gate**: `dev/2026/06/14/1236-radar-gameplan.md` to template v9.4, **self-audited** (matrix at doc tail). DDD: `RadarEntity` / `EntitySource` (protocol) / `RadarFeed.assemble` (provenance-filter + attention-first + two-state); `ConversationEntitySource` wraps #1021; richer types (WorkItem/Person/Document) slot-in as PPM lands #706 — the abstraction is the slot-in seam. Phases: 1 domain+source (TDD) → 2 surface slot-swap (render + wiring tests, feature-flagged for rollback) → 3 search + richer types. 0.7/0.8 = template-sanctioned skips (non-conversational / read-only). Closure gate in STOP.
- **NEXT: Phase 1 (TDD)** — Phase-0.5 contract read first (#1021 response shape in `user_history.py` + `history_sidebar.html` render pattern), then `services/radar/` domain test-first.

## Fire 25 (18:5x PDT — #1236 Phase 1 DONE: services/radar/ domain, TDD 8/8 green)
- **Phase 0.5 contract read**: `history_sidebar.html` = **client-side JS-fetch** (innerHTML/addEventListener, `{% include %}`'d in `home.html`) → Radar render = JS fetching a **server endpoint**; the feed assembly lives **server-side** (DDD + honest-provenance #1214/#1216 MUST be server-enforced, not client-trusted). #1021 `ConversationSummaryResponse` = `conversation_id/title/last_activity/turn_count/topics/preview/is_private` — **no lifecycle_state / open-questions** → v1 derives conversation lifecycle from `last_activity` recency + honest meta (no fabricated counts); conversations are all `observed`.
- **Phase 1 (TDD, domain) DONE** — `services/radar/`: `models.py` (EntityType/Provenance/RadarEntity/RadarView — frozen value objects), `sources.py` (EntitySource protocol + ConversationEntitySource wrapping #1021), `feed.py` (RadarFeed.assemble = provenance-filter + attention-first + two-state). The `EntitySource` protocol = the **slot-in seam** for PPM's WorkItem/Person/Document. **8 tests green** (`tests/unit/services/radar/test_radar_domain.py`).
- **NEXT Phase 2**: `/api/v1/radar` endpoint (RadarService wiring ConversationEntitySource → RadarFeed) + JS render in `history_sidebar.html` (feature-flagged) + real template-render + wiring tests.
- No puzzlers (the #1021 lifecycle gap handled with a documented v1 derivation, surfaced to PM).

## Fire 26 (19:0x PDT — D1 scope +4 + design-floor UNBLOCKED; re-plan) [RECONSTRUCTED — original entry lost to a working-tree revert; substance in carry-forward + commit 3ce8912b7]
PM moved 4 formerly-M5 issues into D1 (#1048/#1202/#1164/#1184) + nudged CXO → **CXO design-floor specs DELIVERED** (`dev/active/design-floor-component-specs-2026-06-14.md`; memo → read/). **Design-floor #1170-1173 UNBLOCKED.** CXO order: **F3 #1172 (build FIRST, locks tokens) → F2 #1171 → F1 #1170 → C1 #1173** (F3/C1 build-ready; F1/F2 want a ~20-min primitives-sync). **⚠ KEY COHERENCE (CXO)**: F2 page-shell = #1090's home frame; #1236's Radar = the L2 aside in it → build #1236 as a **frame-agnostic component** F2 re-homes (my DDD split already supports). 4 new triaged: #1202 files-follow-on (Lead/flywheel), #1164 privacy-toggle (Lead/small, OVERLAPS #1236's file → fold), #1184 artifact-rename (Lead/small-med), #1048 stage-visual (DESIGN Q → CXO). Sequence: #1236 → F3 → F2 → F1 → C1 → #1202/#1184 → #1048. (CXO ack sent `214fbb8f2`.)

## Fire 27 (19:1x PDT — #1236 Phase 2 BACKEND done: /api/v1/radar, TDD 11 green)
- **Phase 2 backend**: `web/api/routes/radar.py` — `GET /api/v1/radar` wires `ConversationEntitySource(_ConversationHistoryProvider(UserHistoryService.get_history))` → `RadarFeed.assemble` → `RadarViewResponse`. Registered in `web/app.py` (mount_router). `_build_feed()` = the seam where WorkItem/Person/Document slot in as PPM lands #706. **11 tests green** (3 route + 8 domain); `test_radar.py` tests REAL wiring (mock only the service — #490 lesson).
- **NEXT Phase 2 frontend**: JS render in `history_sidebar.html` (frame-agnostic, feature-flagged) → fetch `/api/v1/radar` → Part-B cards + two states; preserve + wire the privacy toggle (folds #1164); real `template.render()` test.
