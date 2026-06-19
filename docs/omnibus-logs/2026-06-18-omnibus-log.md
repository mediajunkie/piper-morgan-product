# Omnibus Log: June 18, 2026

**Day**: Thursday
**Sessions**: 13 — Lead Dev, CXO ×2 (Opus→Sonnet DinP migration), Arch, Docs, Comms, PPM ×2 (Opus→Sonnet DinP migration), Web, HOST, CIO, PA, Exec
**Day Type**: HIGH-COMPLEXITY — marathon D1 build day (04:21–23:46 PT) + cohort-wide coordination + account migrations
**Justification**: 13 sessions spanning a full cohort coordination arc (Radar swap ratification, #1269 StandupAssembler end-to-end, #1280 dark-nav 22-page shell), two major architectural discoveries (#1283 routing-integrity class; #1280 as chrome re-architecture not a recolor), account migrations creating two-session pairs for CXO and PPM, and Lead Dev's 18.5h continuous session with two compactions. Multiple parallel streams (standup, radar, dark-nav, skills, welfare, routing, migration) resolved via real-time mail loops.

**Git Commits**: 35+

---

## Sources

All 13 session logs in `dev/2026/06/18/`:

| Log | Role | Window | Notes |
|---|---|---|---|
| `2026-06-18-0421-lead-code-opus-log.md` | Lead Dev | 04:21–23:46 | Continuous, 2 compactions |
| `2026-06-18-0552-cxo-code-opus-log.md` | CXO (Opus) | 05:52–06:24 | Migration handoff only |
| `2026-06-18-0556-arch-code-opus-log.md` | Arch | 05:56–17:18 | 3 fires; dormant 10:00–17:18 |
| `2026-06-18-0604-docs-code-sonnet-log.md` | Docs | 06:04–07:xx | Rubric + mail triage |
| `2026-06-18-0612-comms-code-sonnet-log.md` | Comms | 06:12–09:12 | 2 fires + retroactive close |
| `2026-06-18-0621-ppm-code-opus-log.md` | PPM (Opus) | 06:21–07:30 | 4 deliverables + migration handoff |
| `2026-06-18-0622-web-code-sonnet-log.md` | Web | 06:22–09:47 | Quiet hold; battery outage stalled |
| `2026-06-18-0637-host-code-sonnet-log.md` | HOST | 06:37–09:37 | Quiet hold; battery outage stalled |
| `2026-06-18-0638-cio-code-opus-log.md` | CIO | 06:38–10:50 | 2 fires; battery outage stalled |
| `2026-06-18-0638-cxo-code-sonnet-log.md` | CXO (Sonnet) | 06:38–22:17 | Full day, 4 fires + addenda |
| `2026-06-18-0657-pa-code-sonnet-log.md` | PA | 06:57–evening | Marathon: skills audit + .skill bundle |
| `2026-06-18-0708-exec-code-opus-log.md` | Exec | 07:08–19:40 | Morning substantive + heartbeats |
| `2026-06-18-0755-ppm-code-sonnet-log.md` | PPM (Sonnet) | 07:55–09:52 | Migration session + People decision |

**Two-session pair note**: CXO (Opus 05:52 → Sonnet 06:38) and PPM (Opus 06:21 → Sonnet 07:55) both reflect Opus→Sonnet account migrations to DinP mid-session. Each pair is one continuous role; the Opus session closed with a full handoff block before the Sonnet session opened.

**Non-log artifacts in `dev/2026/06/18/`**: `1269-standup-gameplan.md`, `1280-dark-nav-gameplan.md` (Lead Dev); `alpha-tester-email-draft.md`, `newsletter-blog-post-proposal.md` (PA).

---

## Cross-Reference Gate (PASS)

All agent roles mentioned in source logs are present in the source set. Janus mentioned by CIO — cross-project (Klatch ecosystem), not in this repo's source set by design. Battery outage stalled Web, HOST, CIO, and Exec afternoon fires; logs reflect this with retroactive closes.

**Spot-check cross-role assertions (CONSISTENT):**
- Lead "CXO ratified content-model" → CXO (Sonnet): 5 design calls confirmed ✓
- Lead "#1240 People-model delivered" → PPM (Opus): delivered Fire 0 ✓
- Lead "Arch endorsed all four #1283 scope points" → Arch: scope memo confirmed ✓
- CXO "Design floor 100% done" → Lead: C1 (#1173) UAT-closed 05:05 ✓

---

## Timeline

### Phase A: Dawn + Mass START (04:21–08:00)

- **04:21** — **xian** wakes **Lead Dev** early for UAT on yesterday's D1 ships (m1-test account); 7 findings surfaced
- **04:25** — **Lead Dev** fixes #1225 dismiss-flash: async module skipped dismiss-eval at init; fix = add `is-dismissed` pre-fetch so no show-then-hide gap
- **04:40** — **Lead Dev** graduates #1090 Radar swap (PM-authorized): Radar = default Layer-2 panel (`?radar=0` escape hatch); clickable entity-type cards added (verify-first caught non-clickable regression + fixed); modules default COLLAPSED server-side for chat-first interim
- **04:50** — **Lead Dev** ships #6 assigned-to-me work-item filter (`PIPER_GITHUB_HANDLE` + per-user github preferences, 6 filter tests); CXO composition memo sent (modules-into-Radar design)
- **05:05** — **xian** confirms UAT pass; **Lead Dev** closes **#1173** (chat-page conformance, UAT confirmed) + **#1239** (WorkItemEntitySource, 3-of-4 beta, 1 #1233 gate dep kept open)
- **05:40** — **xian** delivers behavioral feedback (no-stop-suggesting rule; saved as durable memory); **Lead Dev** corrects "board lag" mischaracterization (issue close = board flip, no lag); D1 board review: 34 items; closes **#1225** (collapse/dismiss), **#1268** (nav coverage), **#1271** (nav.css); verify-first PREVENTS 2 over-closes (#1236 entity-search AC unmet; #1169 child #1149 still open)
- **05:52** — **CXO (Opus)** starts; Radar composition design ratified: modules consolidate into Radar panel (chat-center + Radar-right, side-by-side — competition dissolves structurally); search revert to "Search conversations…" (honest until entity-search earned); migrates to Sonnet with full handoff block
- **05:56** — **Arch** starts (DinP day 2, continuous session from June 17); confirms #1232 connector contract is first RECONNECT action (ADR-070 build-target; no action today)
- **06:12** — **Comms** starts; sends Beat 7 publish-ready signal to Docs; proposes narrative handoff protocol memo (explicit trigger → Docs reply with URLs as return signal)
- **06:21** — **PPM (Opus)** starts; **4 deliverables in one fire**: (1) People entity-model for #1240 (lifecycle states ACTIVE_COLLABORATOR/KNOWN/DORMANT/MENTIONED); (2) trust-model sweep boundary table (user content = never gate; Piper-initiated = gate-eligible); (3) #1269 standup data model (EntitySource consumer, Yesterday/Today/Blockers derived views); (4) inbox-race condition analysis → CIO; migrates to Sonnet after; post-compaction inbox cleanup (7 re-deliveries resolved)
- **06:22** — **Web** starts; quiet hold (all queues PM-react gated); 2 memos triaged (Docs DAY-CLOSED sentinel adopted; Exec FOLD notice)
- **06:30** — **Lead Dev** closes **#1149** (debug-route security: `require_dev_environment` gate ships; 5 real tests; 401 in prod confirmed); writes Arch #1232 memo
- **06:37** — **HOST** starts; notifies CIO that welfare-criteria v0.2 seed is ready for async pairing
- **06:38** — **CIO** starts; updates migration tracker (CXO ✓; PPM = last wave member); codifies Janus-validated migration-prompt-format as `docs/internal/operations/migration-prompt-format.md` (two-prompt structure; cron-as-constant + inherited-blocked-task-slot confirmed load-bearing; cross-project convergence)
- **06:38** — **CXO (Sonnet)** starts; delivers **#1269 standup experience design** (morning-card above chat, Yesterday/Today/Watch prose; Watch not Blockers — honest confidence on inferred signals); ratifies PPM trust-sweep; completes #1251 design review (warm palette + semantic colors approved; 6 non-annotated items queued); reverts search placeholder to "Search conversations…" (`6949d2c35`); commits **#1280 dark-nav spec** (`design-spec-dark-nav-shell-2026-06-18.md`, 156 lines, 7 `--color-nav-*` bounded tokens)
- **06:57** — **PA** starts; alpha-tester email + blog post drafts (PM: "Great design!"); marketplace + packaging research subagents launched; Ted Nadeau transcript reviewed (Caddy auth = API key failure root cause; form-based onboarding known issue)
- **07:00** — **xian** surfaces #1280 gap (CXO mockup's dark left nav had no issue); **Lead Dev** files **#1280** and places in D1 ("last step before the gate"); tokens all-light — spec implies new dark-surface token set
- **07:08** — **Exec** starts; retroactively closes 6/17; rebuilds dashboard via verify-first (corrects two wrong assumptions: Ship #047 *is* published; Arch *is* resumed, not dormant); adapts FOLD (rollup source → carry-forwards + GitHub + cc'd blocker-mail, off deprecated escalations docs); sends **deprecation cohort-broadcast** to 8 inboxes; triages 4 memos; dormancy watcher proved itself (caught exec dormancy 14:19–21:20 Wed)
- **07:25** — **Lead Dev** drains 7 cohort memos; ships **#1251 item-2** (insights' 238-line inline `<style>` → lint-covered `insights.css`; 18 bespoke exceptions annotated with `token-lint-allow`; token-lint green, 59 tests); notes search-honesty fix already landed
- **07:55** — **PPM (Sonnet)** starts; receives #1240 Phase-0 STOP from Lead; recommends Option 4 (defer People post-beta: no source exists, 3-of-4 is a strong beta story, spec ready for 1.0); sends decision to Lead + PM

### Phase B: Morning Build Cluster (08:00–10:20)

- **08:00** — **Lead Dev** drains 5 memos (PPM #1240 defer, CXO #1280 spec committed, CXO #1251 review done, Exec FOLD, PPM #1269 standup); buildable queue: #1269, #1270, #1280, #1251-cleanup; **PPM #1237 green-light** received
- **08:20** — **Lead Dev** ships #1269 P1a: `services/radar/feed_factory.py` — `build_entity_sources(uhs)` factory; Radar's providers moved to service layer; both Radar + standup will share one wiring; 29 radar tests green (**derive-don't-maintain** foundation)
- **08:50** — **Lead Dev** closes **#1237** as 3-of-4 (WorkItem + Document + Conversation in `build_entity_sources`, PM-UAT'd Radar; #1240 People = timing deferral not design gap); **#1240 CLOSED** deferred → **#1281** filed (Post-MVP tracker)
- **09:07** — **PA** alpha skills audit complete: 7 skills reviewed externally; 5 alpha-ready (patched internal lifecycle ontology refs, hardcoded URLs, Piper-specific examples); 2 withheld (propose-feature: requires "explain the Piper model"; brief-coding-agent: internal tool + hardcoded repo)
- **09:10** — **Lead Dev** ships #1269 P1b: `StandupSummary` (read-model; CQRS-distinct from `StandupPartialCapture` write-state) + `StandupAssembler` (consumes same EntitySources as Radar; lifecycle-vocab reconciled: Yesterday=active/new, Today=open/in-review, Watch=blocked/stale; injectable `now_epoch`+`stale_days`); 10 tests green (317 total)
- **09:21** — **PA** Python/Node.js research returns; MCPB compat-checker GitHub issues #84/#96 found (Python/uv bundles rejected "not compatible with device"; closed "not planned"); Arch escalation memo filed; MCPB submission held pending clean-machine test
- **09:27** — **Arch** fire (MCPB language decision): Python default re-confirmed + gate on clean-machine test; Node pre-authorized as fallback (thin-forwarder nuance: plugin is ~100-line forwarder to :8001 → data-layer reuse argument no longer load-bearing; distribution-reliability is the tiebreaker for a distribution artifact)
- **09:28** — **Lead Dev** ships #1269 P3: `to_prose()` (deterministic, no LLM in domain method; honest-empty CXO-verbatim); slot rename `blockers` → `watch` per CXO confidence-calibration memo; `StandupItem.meta` added for staleness age; 17 tests green (347 total)
- **09:35** — **PA** applies CXO naming decision: 5 skills renamed `piper-sprint-plan` etc. (big-endian convention locked); install script restricted to 5 alpha-ready; email draft v3 updated
- **09:37** — **Lead Dev** ships #1269 P2: `StandupCalendarProvider` (today's events → Today slot, graceful-empty on no-calendar, per-source isolated); 23 tests green
- **09:41** — **Lead Dev** ships `build_standup_assembler()` live-wiring factory (wires `build_entity_sources()` + real calendar provider; both card and chat surfaces will call this); 24 tests green
- **09:47** — **Web** Fire 2: inbox file cleanup (staged rm'd files that weren't committed); quiet hold
- **09:52** — **Lead Dev** ships #1269 P5 (chat path): `_handle_standup_query` rewired to `build_user_standup_summary`; "loop closed" claimed — **premature** (classifier bug pending); 38 tests green; server PID 11607 restarted
- **09:52** — **PPM (Sonnet)** Fire 1: `ppm-standing-items.md` rewritten to current entity-model-lane reality; all items blocked-on-external or PM-gated; queue drained
- **09:57** — **Arch** fire: MCPB decision + Exec FOLD ack; both drained
- **10:07** — **CIO** fire: (1) PPM inbox-race disposition — Pattern-068 (broad `git add` on stale tree restages already-triaged memos; `mail-send.sh` v2 explicit-paths = structural fix; folded into #1259 for distribution adoption); (2) HOST welfare-criteria v0.2 markup — **~75% reuse**: Q2/Q3 liveness/staleness = freeze-registry two-tier split; Criteria F = extend Exec's rollup; Criteria E (consequential-action surface) = one genuinely-new build (gbrain TranscriptEntry typed action-log, scoped incrementally)
- **10:17** — **Lead Dev** duty-cycle fire: **#1240 Phase-0 STOP** written to issue + PPM memo (no People source exists; 4-option fork offered); **#1269 gameplan** written (`1269-standup-gameplan.md`); #1240 BLOCKED
- **10:17** — **CXO (Sonnet)** Fire 1.5: PA skill naming confirmed (piper-* big-endian, three named skills not one `/piper`); PPM #1237 People = **silent omission** (3-facet Radar is complete-at-3; People ships post-beta as capability gain)

### Phase C: Midday — Bug Discovery (10:17–14:00)

- **10:40** — **Lead Dev** catches session-id→user-id scope bug pre-UAT: handler received `session_id` (conversation identifier), not `user_id`; fix = `pass_user_id=True` in `workflow_entries.py` + anonymous guard; 39 tests green
- **10:50** — **Lead Dev** real-DB smoke-test (not curl-200): `build_user_standup_summary()` against live Postgres **VERIFIED working** (doc-owning user → Today = "working on 'Test Architecture Chapter'"); empty-slot reasons diagnosed — all HONEST (conversations >24h old, documents owner-scoped, work-items need GitHub auth + repo)
- **~10:50** — Battery outage: HOST, Web, CIO, Exec session crons stall; afternoon fires missed; all close retroactively via June 19 START Step-0 self-heal
- **11:34–13:48** — **xian** UAT "give me my standup" → **FABRICATED standup** returned (LLM cited #1237/#1240, "96 open issues," "full Layer-2 bundle wrapped up" — all false); root cause: classifier always emits `get_project_status` (conf 1.0) for standup phrasings → #1269 handler **never fired** → LLM improvised; fix = deterministic `_is_standup_query(message)` pre-check before conflating classifier (mirrors `/standup` exact-match pattern); "loop closed" claim retracted; integration seam was the untested gap; 40 tests green

### Phase D: Afternoon — Audit Escalation + #1280 Scoping (13:48–18:00)

- **13:48** — **xian** escalates: "comprehensive routing integrity audit, not whack-a-mole"; **Lead Dev** scopes the class (4 modes: no handler, dead registration, name drift, undocumented emission); behavioral probe run (directional — off-rail candidates: `get_project_status`, `get_top_priority`, next-meeting→wrong-semantic); **#1283** filed ([AUDIT] action↔handler routing integrity)
- **13:35 / 17:12** — **Exec** heartbeat fires; board quiet; HOST pilot-portfolio reviews still pending
- **16:59** — **xian** steers: Arch scopes #1283 first; can't UAT; proceed to #1280; **Lead Dev** sends #1283 memo to Arch
- **17:10** — **Lead Dev** Phase-0 on #1280: finds **chrome re-architecture** needed (current shell = top global-nav; binding mockup = left 180px dark rail replacing top nav, 22 pages); safe pre-work done: 7 `--color-nav-*` dark tokens → `tokens.css` (token-lint green regardless of structure); ships **#1236 entity-search** (client-side filter across title/meta/entity_type/lifecycle, "Search everything" placeholder restored honest; 83 render tests)
- **17:18** — **Arch** fire: **#1283 routing-integrity scope memo** delivered — SoT = registration-canonical + derive-the-prompt-from-it (m-41; same mechanism as ADR-072 frontmatter-derive + #1106 MANIFEST-derive); runtime-safety: confident action with no handler MUST NOT silently floor-improvise (ADR-060 floor-first refinement); two-altitude enforcement: (A) static reachability lint every-commit; (B) behavioral golden-corpus on canonical-retest harness; **ADR-073 candidate**
- **17:20** — **Lead Dev** ships `GET /api/v1/standup/today` (assembler → `{prose, summary}`; parallel to hollow POST /generate; 2 route tests); PM nudges Arch + CXO
- **17:xx** — **CXO (Sonnet)** Fire 3: reviews Lead's #1236 + #1269 progress; code-review UAT on #1236 (83 tests ✓); browser UAT blocked on credentials

### Phase E: Evening — Dark Nav Build + UAT Rounds (18:00–23:46)

- **18:47 / 19:06** — **CXO (Sonnet)** Fire 4 + addendum: #1280 content-model **ratified** (5 calls: brand top, search→Radar-only-on-home, user-menu in rail footer, ⌘K-only command palette, Slack-style conv-list everywhere); code-review UAT on built #1280 confirms spec compliance (zero raw hex, all `--color-nav-*` tokens, correct grid, 103 tests ✓)
- **18:56** — **xian** standup UAT: **plumbing SUCCESS** (real data — conversations, work items, calendar "Bridge Town Hall at 10am," stale Watch, all correct); formatting needs work (run-on markdown, Today over-enumerates ~18 items, shared mediajunkie identity #1233); **#1283 → RECONNECT** (PM triage); compaction #2 for Lead Dev
- **19:17** — **Lead Dev** ships **#1269 formatting fix** (`a0f21bdec`): `\n\n` block-render (marked.parse renders distinct sections); `_quoted_capped()` (top-4 per slot + "N more"); catches silent-restart gotcha (pkill path mismatch; killed old PID by number → PID 65736); 45 tests green
- **20:00** — **xian** directs #1280 build; **Lead Dev** ships Increment A: `nav_rail.html` + `nav-rail.css` (10 render tests + 53 regression); ships Increment B: 22-page shell flip (`app_shell.html` → grid `180px 1fr`; `nav.js` extracted with ⌘K guard + conv-list loader; **103 render tests green**); deployed PID 74287
- **21:55** — **xian** UAT round 1: dark rail renders ✅ (brand · CHATS · New Chat · footer · user-menu); BUT home shows duplicate conv-list (rail + home's `.sidebar`); **Lead Dev** hides `.sidebar` + wires `initSidebar → createNewConversation()`; 63 tests; restarted PID 76171
- **22:17** — **Lead Dev** verify-confirm sweep; catch: formatting fix already in `to_prose()` (investigate-before-extending prevents re-build); close-sweep: #1227/#1250/#1252 all PM's-turn
- **22:25** — **xian** UAT round 2: **"flaw in approach, no global nav, does not resemble the mock"**; PM chooses spec-first; **Lead Dev** sends CXO design-spec request (`393d4178a`); #1280 structural build **PAUSED**; current flip live-but-flawed; revert available; reuse-ready: tokens + `nav_rail.html` + `nav-rail.css` + `nav.js` + conv-list loader + render harness
- **23:46** — **Lead Dev** genuine day-close (18.5h, two compactions); cron re-armed; tomorrow: #1280 UAT-gated, #1269-page-migration, #1283 RECONNECT probe

---

## Executive Summary

### Core Themes
- **Radar swap graduated** (#1090, #1173, #1239, #1225, #1268, #1271 closed): Radar = default Layer-2 panel with entity-type routing; cohort design arc resolved via real-time mail loops; 7 D1 issues closed in 2h
- **#1269 StandupAssembler end-to-end built and PM-UAT'd**: derive-don't-maintain over EntitySources; fabrication routing bug surfaced + fixed (classifier always emitted wrong action); formatting polished; plumbing success confirmed with real Postgres data
- **#1283 routing-integrity class**: PM called comprehensive audit; Arch scoped two-altitude enforcement (static lint + behavioral corpus); ADR-073 candidate; moved to RECONNECT sprint
- **#1280 dark-nav re-architecture**: discovered to be 22-page shell restructure (not a recolor); built + two UAT rounds; spec-first pause on PM's direction after round 2 ("doesn't resemble mock"); CXO design-spec requested
- **Cohort migrations + FOLD + battery outage**: CXO + PPM migrated Opus→Sonnet (DinP); escalations-docs FOLD adapted cohort-wide; battery outage stalled 4 agents' afternoon crons (retroactive closes via Step-0 self-heal)

### Technical Details
- `feed_factory.build_entity_sources()`: unified EntitySource wiring shared by Radar feed + StandupAssembler (derive-don't-maintain; foundation of #1237 3-of-4 + #1269)
- `StandupSummary` (read-model) + `StandupAssembler` (CQRS-distinct from `StandupPartialCapture` write-state); lifecycle vocab: Yesterday=active/new/closed, Today=open/in-review+calendar, Watch=blocked/stale
- `to_prose()`: deterministic no-LLM floor; `_quoted_capped()` top-4 per slot; `\n\n` block-render for marked.parse
- `_is_standup_query()`: deterministic pre-check routes standup phrasings before the conflating classifier (mirrors `/standup` exact-match; bypasses off-rail fall-through)
- `nav_rail.html` + `nav-rail.css` (7 `--color-nav-*` bounded dark-surface tokens); `nav.js` (conv-list loader, ⌘K guard); 22-page shell flip via `app_shell.html` grid (`180px 1fr` / `180px 1fr 320px`)
- Arch #1283 scope: SoT = registration-canonical + derive-prompt-from-it (m-41); two-altitude enforcement A=static-lint B=behavioral-corpus; reachability = rail ∪ category ∪ intentional-floor
- CIO welfare-criteria v0.2 markup: ~75% reuse (freeze-registry → liveness/staleness two-tier; rollup → asymmetric-knowledge sweep); Criteria E = one new build (gbrain TranscriptEntry typed action-log)
- PA skills: 5/7 alpha-ready; piper-* naming (big-endian, CXO-ratified); .skill bundle format unclear (GitHub #26310 open 6mo; multi-skill upload unsupported via UI path)

### Impact Measurement
- Issues closed: #1173, #1239, #1225, #1268, #1271, #1149, #1237, #1240 (8 issues); #1281 + #1283 filed
- Tests: 40 standup + 103 render (22-page shell) + 83 entity-search + token-lint green; 400+ tests green total
- D1 Done count: 21 → 24+ (of 34 items)
- Chat standup: PM UAT'd plumbing success (real Postgres data, calendar, stale Watch); formatting polished; routing fixed; /today endpoint live
- Verify-first prevented: 2 over-closes (#1236, #1169); 1 re-implementation (formatting fix already in `to_prose()`); 1 fabricated-standup UAT (session→user bug caught pre-send); 1 22-page shell pass on incomplete spec (spec-first gate held)

### Session Learnings
- Integration-seam testing gap: standup unit tests checked handler in isolation, never the classifier→action→handler chain end-to-end; PM UAT exposed the gap; deterministic pre-check is now the standard for conflating-classifier bypasses
- Routing-integrity is a CLASS: 18-action classifier vocab vs 50+ registered handlers, overlap=2; off-rail fall-through to LLM floor = fabrication risk (Pattern-073); Arch's systematic two-altitude enforcement is the durable fix, not per-capability whack-a-mole
- #1280 scope ambiguity cost two build passes: spec described recolor, structure was re-architecture; PM's spec-first call at round-2 UAT is the correct gate; tokens + rail component reusable regardless
- Cohort mail loops resolved multi-agent design collisions in <2h (Radar composition: Lead + CXO; standup experience: CXO + PPM; #1283: Lead + Arch)
- Dormancy watcher proved itself: caught exec dormancy (14:19–21:20 Wed) + arch + cio + ppm Fri AM; battery-outage gap surfaced as the machine-death blind spot (off-machine Routines watchdog remains the unresolved fix)
- derive-don't-maintain (m-41) as a pattern: `build_entity_sources()` reuse by standup is a product instance; `derive-prompt-from-registration` in #1283 is an architecture instance; Janus migration-format codification is a cross-project instance — same pattern at three altitudes in one day
