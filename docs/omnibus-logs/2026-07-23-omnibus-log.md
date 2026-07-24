# Omnibus Log: Thursday, July 23, 2026

**Day**: Thursday
**Sessions**: 4 (Comms, Lead Developer, Chief of Staff/Exec, Docs)
**Day Type**: HIGH-COMPLEXITY: EXECUTION — Lead's decisive burn-down day;
CI went green under the gate for the first time (~08:35) and held all day (10 green batches,
one red caught and cured within one cycle); backlog 264→105 same day (arc 634→105);
6 product fixes surfaced by the drain; beta advanced v27→v28. Comms delivered three
PM-approved narrative drafts, fact-checked against primary logs, and corrected a
two-day misread. Docs published "Almost Beta" in the evening.
**Justification**: 4 sessions; Lead's solo technical arc (waves 15-44, dawn to midnight)
is the most productive single-session day in the drain's recorded history. Not dense
cross-role coordination but extraordinary execution density — HIGH-COMPLEXITY: EXECUTION.

**Git Commits**: 40+

---

## Chronological Timeline

### Phase 1: Morning Start + Early Wins (06:42 – 08:40)

- **06:42**: **Communications** START.
  Jul 22 DAY-CLOSED ✓. Cron: 1 job (`5e4b7080`), correctly armed, inbox empty.
  PM asked for a review of "Almost Beta" (Beat 16, today's scheduled pub) before PM's own edit pass.

- **06:47**: **Lead Developer** START.
  Jul 22 DAY-CLOSED ✓ (the 15h-freeze day). Backlog ~264. CI green.
  Inbox empty; no migration signal. Resumes `document_processing` — the 5× generic-error thread.

- **~07:00–08:15**: **Lead** Wave 14 — `document_processing` 9/9 + TWO live product fixes.
  (1) Analyze route silently 500'd since #1312 ownership migration:
  `document_handlers` queried `UploadedFileDB.session_id` (docstring even codified the dead
  convention) — owner_id patched at both sites.
  (2) Question path `NameError`'d on missing `import io` (pypdf `BytesIO` reads) → generic-error floor.
  (3) The apparent "auth gap" was the test's own cookie riding into the unauthenticated call;
  endpoint auth VERIFIED intact; cookie-clear + comment closes it.
  Yesterday's stranded fixes ride (login form-encoding, usage-cap headroom + gauge-clear).
  Smoke green. Backlog −9.
  **v27 deployed + verified** (health 200):
  the doc-analysis surface works on beta for the first time since the #1312 ownership migration.
  PM checkout repaired (14/14 twin-verified drops committed).

- **~08:00**: **Lead** CI root cause #5 of the drain found.
  The deepened doc tests hit usage-cap middleware's Redis dependency — CI had NO Redis service;
  fail-closed 503 `capacity_check_unavailable` at login.
  `redis:7-alpine` added to both Tests jobs (same pattern as the earlier postgres parity fix).
  Redis parity fixed the 503 but doc tests then 404'd with FastAPI's bare "Not Found" — not the
  route's detail-carrying 404, which meant an UNMOUNTED router (mount_router swallows import errors
  into captured logs). Added a CI probe step (direct import + app.routes assert) for the real traceback.

- **~08:15**: **Lead** probe verdict + lazy-init fix.
  `document_handlers` built `DocumentService()` at module import → chromadb's
  `OpenAIEmbeddingFunction` RAISES keyless → router import died → mount_router swallowed it →
  bare 404. Rewired to the existing `get_document_service()` lazy getter (verify-first: no second
  singleton). Real product-robustness fix: a beta key-config hiccup would have silently dropped
  the whole doc surface.

- **~08:35**: **Lead CI GREEN** at `c0a10e40f`.
  FIRST green Tests run under the burn-down gate. Smoke + Full Suite both pass.
  Gate holds at backlog 228 (arc 634→228); probe confirms the doc router mounts keyless.
  PM notified (terminal push). **The 40+-run red streak is over.**

- **09:02**: **Chief of Staff (Exec)** START.
  Cron: 1 job (`eac577b7`). Pairing mismatch persists. Synced clean (29 commits ff-only).
  Exec inbox: Lead's memo confirming the 15h freeze (7/22), recommending migration to a fresh session.
  Confirmed CIO and Arch still stale — now day 4 continuous (two watchdog re-pings overnight).
  Docs also quiet — last log 7/21, 2 days (not auto-monitored; stale-branches retraction sitting
  unread in Docs inbox). Judged not worth re-escalating: 2 existing PM memos + Lead's independent
  confirmation cover the signal; a fourth memo would be noise.

- **~09:10**: **Exec** ghost-cleanup item closed.
  Found commit `40495fbc5` — automated hygiene mail-loop that does exactly the inbox/read
  duplicate cleanup Exec had been declining to do manually in PM's mailbox.
  PM's `xian (ceo)` mailbox (219 duplicates) will be swept by this process on its own schedule.
  Carry-forward item closed as "handled by existing automation."

- **~10:00–10:30**: **Comms** "Almost Beta" review — real chronology error found.
  Fresh fact-check pass (beyond the Jul 21 mechanical fixes):
  "The declaration" section frames both Slack quotes ("It is a toy still... but it is very cool"
  and "alpha — almost beta — Piper Morgan is a good PM assistant!") as "Late Saturday afternoon...
  And then, later."
  Verified against primary logs: quote 1 is from the **Jun 12 (Friday)** Lead Dev log;
  quote 2 is from the **Jun 14 (Sunday)** log, fire 7 at 09:01 PDT (morning).
  Confirmed day-of-week via `date -j` — two quotes are 2 days apart, not one afternoon.
  Cross-checked "The benchmark" section (Saturday/Jun13, 242/1/0 suite fix) — confirmed accurate.
  Reported both the finding and the already-correct sections to PM; offered to fix directly or
  leave for PM's voice-pass. Not yet a blocker (PM edit pass still in progress).

### Phase 2: Burn-Down Marathon (08:40 – 12:00)

- **~08:40 onwards**: **Lead** waves 15-26 continuous drain (first batch after CI green).
  **Wave 15** (`execution_analysis`, 9): pure fixture rot — `process_intent` now `await`s
  `classify_multiple` (#595 multi-intent rail); `_stub_classifier` helper added stubbing both
  surfaces; 35/35. Backlog −9.
  **Wave 16** (`classification_accuracy`, 7): uses live `intent_service` → `pytest.mark.llm` lane.
  Triage note: `llm_classifier_benchmarks` (7): #322 DI rot; classifiers without `llm_service`
  fell back to uninitialized container; mock LLM injected; both fixtures patch `.complete` anyway;
  7/7.
  **Wave 17** (`llm_classifier_benchmarks`): same DI rot pattern — mock injected; 7/7. Backlog −7.
  **Wave 18** (`standup_performance`, 9): `create_conversation` went async (9 un-awaited sites)
  + multi-turn loops reused stale conversation objects, replaying `INITIATED` branch into same-state
  transition guards; tests now match the live caller (re-fetches per turn). 10/10.
  **Wave 18 postscript**: full-sweep fails despite standalone 10/10 (wave-6 rule earns its keep) —
  integration+performance prefix confirms poison in earlier sweep dirs; re-listed flaky pending chase.
  **Shrink-lock discipline enforced**: local claimed 20 passers; CI said 6 — removed ONLY the
  CI-confirmed 6. The 14 local-only passers are env-dependent oscillators that still fail in CI;
  they stay listed. (This is the decisive discipline: a weaker check would have inflated the
  apparent progress and missed env-shape blindspots.)
  **Wave 19** (`configuration_regression`, 7): pure mock-theatre — tests patched
  `PiperConfigLoader` and asserted their own `MagicMock` (Pattern-045 terminal case — the worst
  form, asserting self rather than the subject). PLUS a hidden poison: this file's teardown was
  **rewriting `config/PIPER.user.md` mid-sweep** — a live poison source for order-sensitive tests
  (explains several mysteriously-intermittent failures across the whole suite). Now gone.
  **Wave 20** (`error_message_enhancement`, 6): fossil patched `main.classifier` (gone since the
  intent stack moved to services) AND pinned pre-degradation 500/502 shapes. Rewritten against the
  real seam (`app.state.intent_service`) and the Pattern-007 contract (service failures → 200 +
  conversational degradation). 22/22.
  **Waves 21-22**: `clarification_edge_cases` + `api_query_integration` drive LIVE classification
  → `pytest.mark.llm` lane. `integrations_dashboard` (6): routes grew JWT `Depends` parameter —
  fake `JWTClaims` injected explicitly. 12/12.
  **Wave 23** (`mcp_error_scenarios`, 6): Arch's #1436 Tier-3 ruling applied — 4 tests pinned
  the deleted POC simulation stack; removed with pointer to Family-6 consumer follow-up. 2 live-
  referent tests fixed (circuit breaker API + current signatures). 7/7.
  **Auth integration (wave 26)**: conftest transaction-rollback isolation became dead letter (#442
  strategy broke — app couldn't see rolled-back test users; every login 401'd). File now commits
  real users via fresh-engine session with `delete_test_user_fully` registry-based teardown.
  Login posts fixed `json`→`data` (Form-encoded). **Security coverage relit**: password-change
  token invalidation + blacklist CASCADE had been dark since the #442 strategy shift — neither
  tested nor known-broken; now verified live again. 5/5.

- **CI at `1902a3bd5`** (waves 19-27 batch): ZERO new failures; only shrink-lock.
  `intent_wiring` RecursionError trio NOW PASSES in CI — the wave-19 removal of the mid-sweep
  `PIPER.user.md`-rewriting teardown + the `delete_test_user_fully` teardown fix cured the
  order pathology; these were NOT a fundamental sweep-order problem but a compounding poison.
  Removed per gate. Backlog 173→170.

- **Fire 2 (09:47)**: cron tick joins the running drain — cron healthy, inbox empty.
  **Wave 33** (`config_pattern_compliance`, 4): `get_config`/`is_configured` owner-scoped (ADR-071);
  compliance probes pass fresh principal id. 37/37. Backlog −4.
  **Wave 34** (`plugin_registry`, 3): fifth plugin (demo) joined; count pins loosened to superset
  semantics + demo allowed in name whitelist. 24/24. Backlog −3.
  **Wave 35** (`settings_projects_ui`, 3): template migrated to `app_shell` (#1171); nav/toast/
  tokens are the shell's job; tests assert the two-hop contract (child extends `app_shell`;
  `app_shell` carries the chrome). 22/22. Backlog −3.
  Spatial-territory tests identified and parked (PM-directed committed-theory review):
  `complete_integration_flow`, `slack_spatial_adapter_integration`, `place_service`,
  `attention_pattern_persistence` — all confirmed SPATIAL territory vocabulary.

- **~10:15**: **Lead** THIRD green at `3a5f50cfe` — the batch carrying both infra fixes
  (Redis loop-pool + usage-cap masking).

- **~10:30**: **Lead v28 LIVE on beta** (health 200).
  Carries: usage-cap masking fix (anonymous downstream errors no longer masquerade as
  `capacity_check_unavailable 503s`), loop-aware Redis pool, lazy doc-service init,
  polymorphic eager-load with `selectin_polymorphic`.
  All production-lockstep at `91e878a95`; PM synced.

- **~11:00–12:30**: **Lead** waves 36-43 continuous (fourth and fifth CI greens).
  **Wave 36** (`pm056_schema_validator`, 3): `@patch` on `tools...sys.modules` swapped the REAL
  singleton `sys.modules` process-wide — dataclasses defined inside the window resolved
  annotations against the fake module (py3.12 exposes `KW_ONLY AttributeError`); `patch.dict`
  scoped to the loader call. 11/11.
  **Waves 37-38**: `simulation_guard_1436` (2): patched subject itself deleted by the ruling it
  guards for — patches dropped, flag-on-degrade contract survives. `setup_slack` (2): grew
  `request.state` user pattern (#1434); minimal request supplied. 12/12.
  **Wave 39** (`setup_system_check_1318`, 2): route honors Fly-spelling `CHROMA_HOST` first;
  `.env` sets it locally (conftest `load_dotenv`) shadowing patches — tests control both spellings.
  13/13. (Local-sweep noise, not backlog entries — no delist.)
  **Wave 40** (`llm_domain`, 2 + `setup_wizard`, 2 + `setup_calendar`, 1): per-user LLM kwargs
  (system/user_id) in pass-through asserts; `user_api_keys` raw SQL modernized to keychain-
  reference schema; wizard patches moved to source class (function-local imports); calendar's
  `validate_token` mock: `AsyncMock` (sync-return rot, #1434 pattern). 27/27. Backlog −5.
  **Waves 24-25** (todo handlers, 10): `todo_items.owner_id` became UUID+FK+NOT NULL
  (#484/#1312) — both files passed literal "user1"/"test" owners. Real per-test users via
  autouse fixtures (cascade with `delete_test_user_fully`); copy-pins modernized to conversational
  handler replies (ids resolve by list position — probed live).
  PLUS real latent service fix: `item_service` `reorder_items`/`get_items_in_list` selected the
  polymorphic base and `to_domain()` lazy-loaded joined subclass tables in sync context
  (`MissingGreenlet`); `selectin_polymorphic` eager-loads now. Not exposed on any live route
  (latent, not beta-urgent) but would surface under async load.
  **Wave 32** (user_flows + integration_complete): GLOBAL-AUTH-ERA pins (admin endpoints correctly
  401 unauthenticated; nl-endpoint config read in-process). TWO more product fixes en route:
  (1) `RedisFactory` pool loop-bound-and-cached — the Redis twin of the #1193 poisoned-pool class
  (loop destroyed, new pool created on the old loop; rebuilds on loop change).
  (2) **REAL production masking bug** in `usage_cap_middleware`: the anonymous-principal early return
  ran `call_next` INSIDE the fail-closed try — downstream handler errors (any real route error)
  masqueraded as `capacity_check_unavailable 503s` in production. This is what made "/" template
  errors read as a capacity failure. `call_next` now always outside the try. 503s now only mean
  what they say (Redis unavailable). Middleware 15/15.
  **Wave 41** (`preferences_questionnaire`, 2 + `sec_rbac`, 2 + `agent_scalability`, 1):
  questionnaire does `uuid.UUID(user_id)` first — non-UUID test literals short-circuited to
  False before any mock ran; `TodoDB` title→description + `FeedbackDB` schema drift;
  CPU-load test re-tagged `flaky` (200ms target on 2-core shared runners = oscillator by
  construction).
  **5th consecutive CI green at `199aac6c1`**.

- **~12:00**: **Lead** accessible triage tail DRAINED.
  Everything remaining at 119 is parked/gated: ~40 methodology tests (Arch fix-or-delete ruling
  is the largest single lever; Exec already escalated), 16 spatial-held (connection_pool 9 +
  adapter pair 7, PM-directed review pending), 12 learning-complex (dedicated session: shared
  `TEST_USER_ID` + settings interference), ~15 flaky context-oscillators (standup 9 cumulative-
  state — bisect map logged; doc-edge 3 may retire via CI), misc gated singles.
  Backlog arc 634→119. Briefing STATUS BANNER refreshed (Lead's attestation, July 23 date).

### Phase 3: Self-Corrections + Editorial Push (14:00 – 20:30)

- **~15:50 PT**: **Comms** Almost Beta chronology fix applied.
  PM confirmed: fix the day/time attribution.
  "Late Saturday afternoon... And then, later" → "That Friday..." / "Two days later, Sunday morning:"
  Surgical edit, two-quote attribution only. Committed (`414361dc8`), pushed.
  Calendar note updated with full fact-check provenance. Committed (`d850b68a7`), pushed.

- **Fire 4 (15:47)**: **Lead** cron tick.
  Briefing STATUS BANNER refreshed (CI green arc, backlog 119, v28, July 23 date).
  Wave 43 (`load` trio, 3): run on a quiet box revealed they drive LIVE intent pipeline under
  stress → `pytest.mark.llm` lane. Backlog 119→116.

- **Fire 5 (18:47)**: **Lead** adds NON-GATING CI diagnostic step.
  Re-runs the env-oscillator backlog band (radar/publish_gaps/github_query/comment_issue/
  pm034/standup_assembler) with tracebacks every run — the gate tolerates listed failures
  so the main sweep never shows their WHY. This pays off in ONE run.

- **~18:47–19:30**: **Lead** oscillator evidence lands; wave 44 (radar/assembler product fix).
  Non-gating diagnostic decomposed the whole band into 3 named causes:
  (1) **radar 4 + standup_assembler 1**: `DocumentIngester.__init__` eagerly constructed
  `OpenAIEmbeddingFunction` (raises keyless) → **a keyless server 500'd its whole radar feed**
  (same class as the doc-surface bug, one level deeper). Embedding function + collection now
  lazy properties; radar/assembler/doc-edge 44/44 locally.
  (2) `publish_gaps` (4): live Notion publisher (keyless) → llm lane.
  (3) `comment` pair (2): live LLM slot-extraction → llm-marked individually.
  CI at `a7601dd8f`: zero new failures; shrink-lock demanded exactly radar 4 + assembler 1 —
  lazy-ingester cure CI-CONFIRMED. Removed. **Backlog 110→105.**

- **~19:00 PT**: **Comms** PM unpack request — real self-correction.
  PM asked Comms to unpack all three open threads; flagged the Ship #052 P.S. one as "sounds
  stale, asked and answered yesterday." PM corrected directly: the P.S. placeholder deletion
  was a deliberate decision to adopt a single-P.S. convention going forward — not an incomplete
  edit. Comms had misread the diff as a gap rather than an internally coherent change, and
  carried the wrong "still open" status for two days across carry-forward, standing-items,
  calendar notes, and chat messages.
  Owned the error directly; fixed every surface that had it wrong:
  calendar note (`aedbf011a`), `comms-carry-forward.md`, session log.
  Separately: PM approved the 3-beat narrative-slate proposal ("The Write-Path Chase,"
  "Alpha Launches," "The Architect's Own Trap") and noted the narrative front is a beat behind.

- **~19:00–19:20 PT**: **Comms** Routines-watchdog root cause traced.
  PM asked Comms to read the cross-pollination brief re: the watchdog-funding framing.
  Traced back: CIO's Jun 12 log had a hedge ("likely moot IF bundled in Max — not confirmed");
  the actual PM clarification was **Jun 14**, when PM directly corrected Exec's stale attention
  board ("Routines moot") — but Exec's Jun 14 session log recorded only the board correction,
  not the factual premise ($0, bundled in Mac subscription), and never wrote it to `decisions.log`.
  The misconception re-inherited for a month until Comms's Jul 21 fact-check forced a re-check.
  Memo sent to Exec (cc Docs + PM) with the full root-cause trace (`865d25d70`).

- **~19:20–20:15 PT**: **Comms** drafts all 3 PM-approved beats.
  Three PM-approved beats drafted and fact-checked against primary logs (not omnibus digests),
  one at a time, footer-chaining each into the sequence as it landed:
  - **"The Write-Path Chase"** (Jul 8-9): 5-layer root-cause chain (legacy PAT gates →
    github-mcp-server v1.5.0 contract drift → wrong-repo write → missing entity extraction →
    `Intent.original_message` never set); verified verbatim against Lead Dev's Jul 9 primary log.
    Committed (`b2e4e6819`), pushed.
  - **"Alpha Launches"** (Jul 10-12): 11 batch-1 alpha invitations confirmed sent; "Day total:
    8 defects found+fixed+deployed" — verified against HOST's and Lead's primary logs.
    Comms caught and rewrote own negation-reveal-cliché draft before it shipped.
    Committed (`35b10e04c`), pushed. Footer chain adjusted across 4 files to close the
    Write-Path-Chase insertion gap.
  - **"The Architect's Own Trap"** (Jul 12-15): ADR-078 proposed Jul 12, HOST trust-lens folded
    Jul 13, accepted Jul 14 after Lead's feasibility correction, built+ratified Jul 15;
    capped with Arch's own verified real mistake (Arch's Jul 15 log verbatim:
    *"the exact trap intent-routing-stack.md warns against, and I authored the four-surface model"*).
    Committed (`ff22e77a3`), pushed.
  All 3 beats: mechanical sweep clean (no semicolons, no crutch words), frontmatter pending art,
  calendar rows updated `queued`→`drafted` with full fact-check provenance.

- **~20:20 PT**: **Comms** PM resolves the "refactor" question.
  Comms had flagged: "since a refactor months ago" (PM's Almost Beta edit for Slack-inbound-live)
  not supported by source logs. PM: "trust me re the refactor" — firsthand knowledge not in logs.
  Kept as written. Almost Beta calendar status → `ready-for-docs`. Committed (`fda421212`).

### Phase 4: Evening Publication + Corrections (20:09 – 21:47)

- **20:09**: **Documentation Management** START.
  PM present. PM requested proofread + publish of "Almost Beta" (today's scheduled post).
  Docs inbox: 3 unread (per hook).

- **20:09–20:19**: **Docs** "Almost Beta" published.
  Template audit: 14-check PASS (word count ~450, below guideline but acceptable;
  `pubDate` UTC mismatch needed `--pub-date` flag since past midnight UTC at publish time).
  Published via `publish-post.js` — hashId `864ead908622`, slug `almost-beta`, workDate `2026-06-12`.
  Website repo commit `675c7f3576`: blog-metadata.csv, blog-content.json, medium-posts.json,
  almost-beta.webp all pushed to origin/main.
  Editorial calendar updated: `published`, blogURL `https://pipermorgan.ai/blog/almost-beta/`,
  `canonicalSite=distributed`. Draft archived.
  Post live: https://pipermorgan.ai/blog/almost-beta/

- **21:02**: **Exec** last scheduled fire → STOP.
  **Caught and corrected own stale-branches cross-thread error**:
  Janus re-verified their original claim fresh — their 5 branches genuinely gone, only
  `fix-docker-migration-setup` remains. Exec had checked a DIFFERENT, UNRELATED stale-branches
  item (CXO's 3 MUX branches + CIO's `xpoll-brief-staleness-hook`) that happens to share one
  branch name — conflated the two lists, sent Docs an unnecessary "correction" the night before.
  Sent Docs a retraction (cc PM) explaining the mixup precisely.
  Also succeeded with the Janus cross-repo push that had been blocked last night — reply now
  actually delivered to Janus, not just drafted. Tracker corrected to keep two threads separated.
  **Filed durable memory**: `feedback_factual_pm_corrections_need_decisions_log_not_just_board_fix.md`
  — board/tracker fixes stay local; factual-premise corrections need `decisions.log` same-session.
  Sent Comms brief acknowledgment (cc Docs, PM).

- **21:47**: **Lead** STOP — day-close complete.
  CI green at `b15b683ee`. Beta v28 healthy.
  Backlog arc 634→105 (accessible tail fully drained).
  Ten green CI batches; one planner-oscillator red caught and cured within one cycle.

- **21:42**: **Comms** last fire → STOP.
  Exec's root-cause acknowledgment received (confirmed: Jun 14 board-correction never reached
  `decisions.log`; filed durable lesson). No further movement on narrative-slate steer or
  watchdog-wording question — both non-blocking. All 3 beats drafted; Almost Beta published.

---

## Executive Summary

**Sessions**: 4 · **Day Type**: HIGH-COMPLEXITY: EXECUTION

### Core Themes

- **Lead's decisive burn-down day**: CI went green under the gate for the first time (~08:35)
  and held — 10 green batches, one planner-oscillator red caught and cured within one cycle;
  backlog 264→105 same day (arc 634→105); accessible triage tail fully drained; beta v27→v28.
- **6 product fixes surfaced by the drain**: (1) keyless doc-surface silent unmount (lazy
  `get_document_service`); (2) usage-cap masking bug (downstream errors masquerading as
  `capacity_check_unavailable 503s` in production); (3) loop-bound Redis pool (#1193 class in
  Redis form); (4) item_service polymorphic sync lazy-load; (5) DocumentIngester eager
  `OpenAIEmbeddingFunction` (keyless server 500'd its whole radar feed); (6) auth-integration
  security coverage (password-change token invalidation + blacklist CASCADE) relit after going
  dark since #442.
- **Comms self-corrected a two-day misread and delivered three approved drafts**: the P.S./P.P.S.
  diff was a deliberate convention change, not a gap; Routines-watchdog framing traced to its
  Jun 12–14 root; all 3 narrative beats fact-checked against primary logs and committed.
- **Exec caught and corrected its own cross-thread error**: stale-branches "correction" to Docs
  had conflated two unrelated branch lists; retraction sent, Janus reply actually delivered.

### Technical Details

- **Lead drain shape**: waves 15–44; each wave CI-arbitrated (local claimed 20 passers; CI said 6;
  removed only the 6); non-gating oscillator diagnostic paid for itself in one run (radar/assembler
  root cause found + cured same day).
- **CI root causes cleared this day**: #5 = no Redis service in CI; lazy-init fix; port-parity
  fix; `PIPER.user.md` mid-sweep rewrite poison; `delete_test_user_fully` teardown fix.
- **`intent_wiring` RecursionError resolved**: the wave-19 removal of the mid-sweep
  `PIPER.user.md`-rewriting teardown + the `delete_test_user_fully` fix cured the order
  pathology; CI-confirmed, backlog entries removed.
- **All 3 narrative beats**: "The Write-Path Chase" (Jul 8-9), "Alpha Launches" (Jul 10-12),
  "The Architect's Own Trap" (Jul 12-15); all verified against primary session logs; footer
  chain repaired across 4 files; calendar rows `queued`→`drafted`.
- **"Almost Beta" pipeline**: published with 14-check PASS; `--pub-date 2026-07-23` flag needed
  (past midnight UTC); workDate `2026-06-12` (source-work-period); live at pipermorgan.ai/blog/almost-beta/.
- **Comms chronology fix**: two Slack quotes (Jun 12 Friday + Jun 14 Sunday morning) had been
  framed as one Saturday afternoon; confirmed day-of-week via `date -j`; surgical attribution fix.

### Impact Measurement

- Lead backlog: 634→105 (accessible tail fully drained); all 264 removed entries CI-arbitrated
- Beta: v27→v28 deployed and verified
- 6 product fixes shipped (2 live beta-surface bugs: doc-analysis unmount + usage-cap masking)
- 3 narrative beats drafted (Beats 21-23), fact-checked against primary logs
- "Almost Beta" published to blog + distributed
- Exec cross-thread error: caught, retracted, Janus reply delivered
- New durable memory: `feedback_factual_pm_corrections_need_decisions_log_not_just_board_fix.md`

### Session Learnings

- **The non-gating diagnostic step paid for itself in one run**: the oscillator band had been
  opaque because the gate tolerates listed failures — the diagnostic step's tracebacks decomposed
  the entire band into 3 named causes in one CI run; this is the pattern for diagnosing any
  known-failing cluster without disrupting the gate.
- **Diff coherence before flagging a gap**: Comms carried a "P.S. still open" status for two days
  across 4 surfaces because the diff's resulting state (single P.S.) wasn't checked for internal
  coherence — a deliberate convention change read as an incomplete edit. Check whether the new
  state is coherent before concluding the change was unfinished.
- **Board-fix vs. decisions.log**: fixing a stale attention-board entry is a local correction
  — the underlying factual premise needs `decisions.log` too or it re-inherits into future
  sessions (the Routines-watchdog mismatch persisted a month through board fixes that never
  reached `decisions.log`).
- **Verify cross-list conflation before sending corrections**: Exec's stale-branches retraction
  came from conflating two items that share one branch name — the authoritative check is the
  exact item being referenced, not a cross-comparison with a same-sounding tracker entry.

---

*Sources: `dev/2026/07/23/2026-07-23-0642-comms-code-log.md`,*
*`dev/2026/07/23/2026-07-23-0647-lead-code-log.md`,*
*`dev/2026/07/23/2026-07-23-0902-exec-code-log.md`,*
*`dev/2026/07/23/2026-07-23-2009-docs-code-log.md`*
