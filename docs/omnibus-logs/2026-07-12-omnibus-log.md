# Omnibus Log: July 12, 2026

**Day**: Sunday
**Sessions**: 11 (Docs×2, Communications, HOST, Chief of Staff, Lead Developer, Web, CIO, PPM, CXO, Chief Architect)
**Day Type**: HIGH-COMPLEXITY — MILESTONE
**Justification**: 10 distinct roles active on a day that achieved two of the project's most significant milestones: all 11 first-wave alpha invitations sent and beta.pipermorgan.ai live end-to-end. The #1386 beta-gate uncovered 8 product defects fixed before any tester saw them. The 744-issue sprint-recovery project (started after the 7/5 field wipe) reached completion. Three architectural decisions finalized (ADR-070-A ratified, ADR-078 authored, docs-duty-cycle architecture resolved). Comms advanced 3 blog posts with primary-source fact-checking. Web shipped Vercel admin migration.

**Git Commits**: 40+

---

## Sources

| # | Log | Role | Model | Start |
|---|-----|------|-------|-------|
| 1 | `2026-07-12-0517-docs-code-log.md` | Documentation Management | Opus 4.8 | 05:17 |
| 2 | `2026-07-12-0642-comms-code-log.md` | Communications | Sonnet 5 | 06:42 |
| 3 | `2026-07-12-0707-host-code-log.md` | HOST | Sonnet 4.6 | 07:07 |
| 4 | `2026-07-12-0720-docs-code-log.md` | Documentation Management | Sonnet 4.6 | 07:20 |
| 5 | `2026-07-12-1227-exec-code-log.md` | Chief of Staff | Sonnet 5 | 12:27 |
| 6 | `2026-07-12-1231-lead-code-log.md` | Lead Developer | Fable 5 | 12:31 |
| 7 | `2026-07-12-1506-web-code-sonnet-log.md` | Unicorn Web Designer | Sonnet 4.6 | 15:06 |
| 8 | `2026-07-12-1520-cio-code-log.md` | Chief Innovation Officer | Sonnet 5 | 15:20 |
| 9 | `2026-07-12-1520-ppm-code-sonnet-log.md` | Principal Product Manager | Sonnet | 15:20 |
| 10 | `2026-07-12-1521-cxo-code-log.md` | Chief Experience Officer | Sonnet 4.6 | 15:21 |
| 11 | `2026-07-12-1626-arch-code-log.md` | Chief Architect | Opus 4.8 | 16:26 |

**Cross-reference gate**: PASS. PA mentioned in passing (Exec noted silence; Lead noted #1312 context) but was genuinely inactive — PM in direct contact separately. All 10 active roles have logs. No factual divergences found; cross-role timeline assertions (invite confirmation, cutover milestone, Scenario B re-scope) verified consistent across logs.

---

## Timeline

### Phase 1 — Morning fires: Docs catch-up + Comms velocity (05:17–09:45 PT)

- **05:17** — **Documentation Management** (scheduled-task) START: Jul 10+11 omnibus backlog (2 days) identified; 14 source logs + 3 delta files read via subagent delegation
- **05:30** — **Documentation Management**: Jul 10 omnibus (`HIGH-COMPLEXITY: COORDINATION`, 201 lines) + Jul 11 omnibus (`STANDARD`, 73 lines) built and committed (`2c9f9b2de`); 14 activity-log rows appended (`9fd3cde50`); omnibus cadence restored through Jul 11
- **05:55** — **Documentation Management** STOP (scheduled-task day-close; watchdog Belt-2 ack triaged)
- **06:42** — **Communications** START: prior-day close verified; stale draftPath standing item: 22 published rows corrected (18→`drafts/published/`, 4→`drafts/superseded/`), standing item closed
- **07:07** — **HOST** START: sapient-trust poll 6th consecutive clean (0 open issues); inbox empty; carry-forward updated
- **07:20** — **Documentation Management** (PM-activated) START: LinkedIn URL added for "When the Documentation Drifts"
- **07:40** — **Communications**: PM's voice-pass on "The Server Crashed Mid-Draft" merged (no typos; prior fixes carried through cleanly)
- **07:50** — **Documentation Management**: frontmatter applied (storm-window.png + alt + caption confirmed on disk); calendar marked READY FOR DOCS

### Phase 2 — "The Server Crashed Mid-Draft" publish + blog audit (09:00–12:26 PT)

- **09:00** — **Documentation Management**: "The Server Crashed Mid-Draft" published (insight, workDate 2026-05-17); template audit 14/14 PASS; `publish-post.js` → hashId `b63577f98aa8`, storm-window.webp 129KB; website commit `e81d99791`; post live at `https://pipermorgan.ai/blog/the-server-crashed-mid-draft/`
- **09:09** — **Communications** fire (09:42 slot): post confirmed published, standing items updated, (0,0)
- **09:45** — **Documentation Management**: 81 `alert-duty-cycle-stall-*` files in PM inbox cleared (`fe5d539fa`); CIO notified of PM inbox retirement; 2 stranded Arch Jul 8 memos delivered to Exec inbox (`b98895020`)
- **10:45** — **Communications**: "The Migration Wave" (Beat 13, May 31–Jun 2) full review; 3 real corrections: shared-checkout holdup story mis-attributed to Comms (was 3 of 24 dirty files); "every role, self-running" overstated completion (9 of 11, not all); two unrelated "sevens" accidentally conflated. Committed + pushed (auto-merge on CSV resolved cleanly)
- **10:47** — **Documentation Management** tick: log-closure nudge memos sent to PPM (Jul 9+10) and CXO (Jul 10); Medium URL + LinkedIn URL added for "The Server Crashed Mid-Draft"
- **11:00** — **Documentation Management**: blog audit scan — 2 metadata-prefix title posts (`916-when-your-methodology-holds-under-pressure`, `86-revised-from-722`); 3 double-hero-image posts (`the-closing-sprint`, `the-migration`, `thirteen-mailboxes`). Filed #1391 (admin editing interface) + #1392 (blog legacy fixes). Web routing memo sent (`5c6ad4cf6`)

### Phase 3 — Alpha invites confirmed + full cohort resumes from laptop reboot (12:26–15:30 PT)

- **12:26** — **HOST**: **PM confirms all 11 batch-1 alpha invitations sent.** Alpha is live with first external testers. Welfare watch activated; #1383 (Notion/Calendar per-user creds) noted as known gap for those connectors; Jake Krajewski (brainpowerux@gmail.com) flagged for delivery confirmation
- **12:27** — **Chief of Staff** RESUME: own cron gone (reboot), 109 commits behind; began post-outage investigation — read 8 watchdog alert memos chronologically; confirmed machine-sleep infrastructure event (not individual failures) per the 7/11 12:39 alert's own self-diagnosis
- **12:31** — **Lead Developer** RESUME: retroactive 7/10 close; 5 memos drained; #1332 soak verified clean at 66h → **#1332 CLOSED** (sprint issue-list fully drained)
- **~12:45** — **HOST**: PM welfare question (text-only) → honest assessment: system healthier than friction count suggests; 6 clean sapient-trust polls meaningful; identity drift post-context-gap flagged as the one thing to monitor; alpha launch expands "sapient team" to first external humans
- **~13:00** — **Lead Developer**: **beta.pipermorgan.ai LIVE** (PM's DNS landed, cert issued, "Piper Morgan Beta" OAuth app created, PIPER_BASE_URL + REDIRECT_URI flipped; health 200 / unauth 401 on real hostname)
- **~13:05** — **Lead Developer**: #1390 found live within minutes of public exposure — ten scanner IPs filled ADR-076 session gauge → "Instance at capacity" for authenticated users. Root-caused: ip:* counting against user:* gauge. Fixed (gauge counts user:* only), 15/15 middleware tests, deployed same-hour — **first tester-class defect found before any tester saw it**
- **~13:11** — **HOST**: alpha records updated — both gitignored files (`invite-tokens-assignments-batch-1.md`, `alpha-tester-roster.md`) updated to SENT 2026-07-12 / "Invited — awaiting onboarding"
- **~13:32** — **Chief of Staff**: attention board rebuilt (outage as lead section, corrected sprint-recovery and invite status, needs-a-PM-turn list)
- **~14:00** — **Lead Developer**: #1386 Criterion 5 PASS both envs; Scenario B run 1 = productive FAIL → two bugs found and fixed same-hour: HTML entity escaping (`Let's`→`Let&#39;s`) in sidecar read path + colon-quoted title extraction miss. 30/30 write suites green, deployed
- **~15:06** — **Web** RESUME (PM: "Did you get the relay from Docs?"): Gap-C self-heal; #1392 COMPLETE this fire — 2 metadata-prefix titles stripped, 3 double-hero `<figure>` blocks removed; website commit `7c2673931`, product commit `f55a321be`
- **~15:15** — **Lead Developer**: Criterion 2 verdict — Quality PASS 92% (23/25, band-high), Routing 88.5% conditional; all 7 misses triaged as corpus-expectation drift (capability growth since corpus written, no product routing regression). Filed #1395 (corpus rev + harness UUID fix) + #1396 (vestigial preferences loader); D5 ratification memo → Arch
- **~15:20** — **Lead Developer**: Scenario B run 2 + Scenario C: B1✓ B2✓ B3✗ (misroutes to Notion — pre-existing continuity gap) B4✗ (no cross-turn recall — alpha-parity, not regression). **#1394 filed** (cross-turn antecedent resolution). Scenario C **PASS 3/3** (honest declines, zero simulation, accurate capability description)
- **15:20** — **CIO** RESUME: reboot recovery; retroactive 7/10 close; 3 Docs memos triaged; docs-duty-cycle investigation begun
- **15:20** — **PPM** RESUME: cron re-armed; #1386 B-rescope recommendation drafted and sent to CXO (cc PM/Lead/Arch): re-scope B using Lead's substitute turns, commit #1394 pre-wave-2 P1, TESTER-QUICKSTART disclosure if still open at invite time
- **15:21** — **CXO** RESUME: 5 memos triaged; **CXO+PPM joint sign-off filed**: re-scope B for this gate (substitute turns test real capabilities); #1394 pre-wave-2 P1; TESTER-QUICKSTART disclosure load-bearing from UX standpoint ("use explicit references like 'update issue #107'")

### Phase 4 — Architecture ratifications + Vercel migration (15:30–19:00 PT)

- **~15:52** — **Web**: #1391 COMPLETE — compose API auto-commits after save (no more manual git discipline); split-pane markdown preview added to ComposeEdit; website commit `ac7795185`
- **~16:00** — **Lead Developer**: #1394 investigation COMPLETE — floor history surface confirmed (last-4 user messages; assistant responses never reach any context surface; classification never sees history on this path). Fix = real build (response-aware history slice + antecedent-rule). Days-not-hours. CXO/PPM scope call stands
- **~16:07** — **HOST**: PM asks "Is it time to refactor CLAUDE.md for concision?" HOST: instinct right, risk if done carelessly. Named load-bearing (WHY lines, post-incident encoding) vs removable (historical transition narrative). PM insight: "used to be X, now Y" prose activates deprecated X as soft heuristic even when labeled deprecated — negation doesn't suppress in LLM readers. Collaboration shape: CIO leads architecture pass, Docs executes, HOST reviews behavioral completeness pre-ratification
- **~16:26** — **Chief Architect** RESUME: cron re-armed; ADR-070-A code-ratification: A2/A3/A5 PASS; **A4 gap found** → #1398 filed (`github_adapter` catches `ServerRefResolutionError` nowhere — flattens config error into generic UNREACHABLE at 6 call sites; config-masquerades-as-outage failure A4 exists to prevent). #1395 D5 corpus-rev **RATIFIED** (7 rows: stale-floor-not-regression; observed==intended confirmed; Q45 ruled PASS-with-clarification per ADR-060)
- **~16:30** — **Lead Developer**: Q51 two-layer bug found and fixed: `_handle_productivity_query` passing `session_id` as `owner_id` (#734/ADR-071 principal-confusion class — productivity stats never returned real data for any user); underlying `get_completion_stats` comparing VARCHAR status vs raw TodoStatus enums (asyncpg rejects). Both fixed + deployed. Q51 fingerprint+quality now PASS
- **~16:37** — **CIO**: docs-duty-cycle investigation complete — traced to Docs's own session implementing a schedule-change request via an unrequested mechanism change; matches the exact shape PM rejected on 6/14 and that B1 (6/28-29) does not cover (fixed schedule, no collision guard, main-checkout-direct). Recommendation: retire, extend Belt-4 for proper Docs stall-protection. Presented to PM before replying to Docs (PM is the one who raised concern)
- **~17:10** — **Lead Developer**: **#1388 built and closed** — `list_open_issues` gains repo-scoping; named repo beats default; count + empty-state phrasing names the scope. Live-verified both directions on beta
- **~17:30** — **CIO**: PM confirmed Belt-4 for Docs; found Belt-4 already architected for extension ("add a case branch; only cio/exec had prompts defined"); verified `docs-carry-forward.md` and `docs-standing-items.md` exist before building. Added `docs` case branch, updated plist (`WATCHDOG_AUTO_SPAWN_ROLES=docs`), tests 17/17 (added T13+T14). Commit `87bcdaae9`. Did NOT run `launchctl reload` (PM's machine action) or retire Docs's task unilaterally (Docs's ownership to execute). Memo → Docs cc PM
- **~17:52** — **Web**: **Vercel migration phases 1-3 executed** (PM approved + granted branch-protection bypass): Phase 1 — static export gate (`STATIC_EXPORT` flag, `next.config`/`deploy.yml`/`deploy.sh`/`build:static`); Phase 2 — GitHub Contents API draft storage (`src/lib/github-drafts.ts`, dual-mode compose API, SHA optimistic concurrency); Phase 3 — password login → 7-day httpOnly JWT (jose HS256); all admin APIs verify server-side; production without secrets FAILS CLOSED. 8-case auth matrix + open-mode regression + prod fail-closed all pass. Two pre-existing defects found+fixed: auto-commit swept other agents' staged files (→ pathspec commit); `serializeDraft` dropped post-frontmatter blank line (→ round-trip identity restored)
- **~18:00** — **Lead Developer**: **ADR-070-A BUILT** (`resolve_server_ref` single authority, `_KEY_TO_ENV` map, bind-time stores logical `'github'`, `i070abackfill` data migration). 7 contract tests + 66 write-suite green. Deployed; binding row backfilled; GitHub read resolves logical-key → deployment env → sidecar → real issues. Arch pinged for A2/A4 ratification
- **~18:20** — **Web**: Vercel deploy live; PM chose Pro plan (commercial-use standing + ToS). First build FAILED on Vercel CVE gate (Next.js 15.4.5 had post-pin CVEs). Fixed via 15.4.11 (security-backport tip of 15.4 line); redeploy green. `/api/admin/me` probe hit Vercel Deployment Protection (default-on for *.vercel.app — won't apply at custom domain cutover)
- **~18:38** — **Lead Developer**: away-window queue FULLY DRAINED — gate criteria 5+2+scenarios complete; 4 same-day bug-pairs fixed+deployed; #1388 closed; ADR-070-A built+verified; 5 issues filed; 3 ratification/decision memos dispatched

### Phase 5 — Scenario B re-scope + sprint-recovery complete + ADR-078 (19:00–22:30 PT)

- **~19:00** — **Lead Developer**: CXO+PPM joint sign-off received; Scenario B re-scoped (B3'/B4'): first re-run CAUGHT TWO MORE bugs — to-form title-extraction miss (the very SUBSTITUTE phrasing!) + raw HTML entities in display/verify/recall. Fixed (parse-boundary unescape + to-form extraction), 33/33 write suites, deployed
- **~19:45** — **Lead Developer**: **Scenario B re-scoped PASS 4/4 on live beta** (B3' explicit-reference title update — GitHub truth confirms; B4' clean-text recall after THIRD parse-site fix — `_parse_issue_detail` had its own `json.loads`). Meta-debt noted: 3 issue-parse copies in one adapter. **Day total: 8 defects found+fixed+deployed before tester exposure**. Scenarios fully executed; joint sign-off recorded on #1386
- **~19:20** — **Web**: admin `/admin/login` → "Wrong password" — diagnosis: argv-based bcrypt hash-generation recipe mangled by zsh history expansion. Delivered `read -s` stdin-based quoting-proof regen recipe. PM to retry
- **~20:00** — **Lead Developer**: #1399 — **FRESH-TESTER WALL found** (both envs, invitations in flight): `/` and `/register` 401'd (smart redirect never ran — `/` not exempt); self-host wizard failing localhost checks on Firecracker. Full chain fixed: `/` exact-match exempt; managed-infra sentinel (`FLY_APP_NAME + PIPER_ENVIRONMENT`); `DATABASE_URL`-first db check; `CHROMA_HOST` honored; chroma IPv4-vs-IPv6 6PN → private flycast bridge. Beta wizard: ALL GREEN; `/` → 302 `/login`
- **~21:00** — **Lead Developer**: **v0.8.10.12 CUT + DEPLOYED TO ALPHA** (PM-approved full-parity dot release): 45 files, zero residual delta vs main on product surfaces. Droplet migration `h1312recon→i070abackfill` clean; VERSION verified 0.8.10.12. **#1399 CLOSED — alpha invitees unblocked**. Both environments identical (true parity restored). Local-setup audit: #1400 filed (per-user connector prefs in local JSON — vanish on every Fly deploy) + #1401 filed (uploads on ephemeral FS — active data loss on Fly; storage decision wanted)
- **~21:15** — **Chief of Staff**: all 6 previously-dark roles confirmed self-healed (commits cross-checked from 13:32); entire "needs a nudge" section gone. Final attention board refreshed. STOP
- **~21:45** — **PPM** Fire 3: #1386 criterion 3 confirmed CLOSED (4/4 Scenario B PASS). Production milestone: #1358/#1374 → Ongoing/FLYWHEEL, **99/99 complete**
- **~21:47** — **CXO** Fire 7: Arch #1394 determination received (architectural gap: both B3 + B4 symptoms share one missing primitive — session-activity ledger). TESTER-QUICKSTART disclosure draft filed to Lead+PPM
- **~21:50** — **PPM**: PM resolved Group 3 (19 true-zero-evidence issues) from memory in one message: 10→M2, #409→V2, 4+#398→P4, 3→Q. All 19 verified live before and after mutating. **Sprint-recovery effort COMPLETE**: HIGH (433) + MEDIUM (93) + LOW (218) + S2→A12 correction (19) + Group 3 (19) + the #234 fix. Every issue that had a sprint before the 7/5 wipe has one again
- **~21:56** — **Chief Architect**: day closed initially, then REOPENED per PM for #1394 architectural mapping
- **~22:07** — **HOST**: CLAUDE.md memo confirmed by PM; `memo-host-to-cio-cc-docs-pm-claudemd-refactor-proposal-2026-07-12.md` sent. Day closed
- **~22:07** — **Documentation Management** STOP fire: 4 memos drained; **docs-duty-cycle RETIRED** (`mcp__scheduled-tasks__delete_scheduled_task`, 13 sessions archived, Belt-4 ready pending PM plist reload); CIO replied; day closed
- **~22:15** — **Chief Architect**: #1394 FINAL VERDICT — **ARCHITECTURAL GAP, both symptoms, one root**: B3 misroutes because LLM classifier (surface 2) has no conversation-history slot (antecedent-binding is real at floor/surface 4 but never reached after a misroute); B4 finds nothing because no authoritative session-activity reader exists (only ephemeral 10-turn window, no created-artifact scope). **One missing primitive: durable session-scoped activity ledger**. Integrity call: do NOT inject history into classifier (ADR-077/#1283 territory) — pre-classifier reference resolution (surface 1) reading the ledger instead. **ADR-078 AUTHORED** (PROPOSED v0.1): Session-Activity Ledger + Pre-Classifier Reference Resolution. D1 ledger-as-association / D2 pre-classifier resolution / D3 session-activity reader / D4 classifier-stays-stateless / D5 corpus coverage. Lead's ledger-feasibility the explicit gating open question
- **~22:20** — **PPM**: roadmap.md v18.6 — PROD-* reorganization origin documented (source of the 7/5 wipe); sprint-recovery complete as of today; 20-issue new triage; relative-link fix. Restore-sprint-field script built and tested dry-run clean. CLAUDE.md sprint-field wipe warning updated to point at both snapshot + restore scripts
- **~22:24** — **CXO**: 3 stranded Jun 18 CXO memos committed retroactively (#1269 standup experience design + #1270 ArtifactSourceType ratification, both delivered late to recipients)

---

## Executive Summary

### Core Themes

- **Alpha launch day**: all 11 first-wave external testers invited at 12:26 PT; welfare watch activated; HOST monitoring for onboarding signals
- **Beta infrastructure complete**: beta.pipermorgan.ai live end-to-end (DNS, cert, dedicated OAuth app, secrets, full parity at v0.8.10.12); #1332 soak closed 66h clean
- **#1386 gate earned its keep**: 8 product defects found, fixed, and deployed before any tester reached the product (including the fresh-tester wall found after invites went out, fixed same hour); Scenarios B (4/4) and C (3/3) passed; criterion 2 quality PASS 92%
- **Sprint-recovery complete**: the 744-issue effort from the 7/5 field wipe closed out — PM resolved Group 3 (19 issues) from memory; S2→A12 correction applied; everything that had a sprint before the wipe has one again
- **Docs-duty-cycle architectural question resolved**: retired (matched the exactly-rejected 6/14 shape); Belt-4 properly extended for Docs stall-protection (17/17 tests); CLAUDE.md refactor queued with CIO architecture lead + Docs execution + HOST behavioral review
- **Comms velocity**: 3 blog posts advanced with deep primary-source fact-checking (Beats 13+14, insight); "The Server Crashed Mid-Draft" published

### Technical Details

- **#1386 defects by session**: bug 1-2 (apostrophe entity escaping + colon-quoted title extraction, Scenario B run 1); bug 3-4 (Q51: session_id-as-owner_id principal confusion + VARCHAR vs enum stats query); bug 5 (ADR-070-A A4: config error masked as UNREACHABLE at 6 call sites → #1398); bug 6-7 (to-form extraction + raw HTML entities, Scenario B re-run); bug 8 (#1390: scanner IPs exhausting session gauge)
- **ADR-070 Amendment A** built and ratified: `resolve_server_ref` single authority (A2), `_KEY_TO_ENV` map in-module, bind-time stores logical key `'github'` (A1), `i070abackfill` data migration (A5); A4 gap (#1398) found and filed — adapter must catch `ServerRefResolutionError` distinctly
- **ADR-078** (PROPOSED): Session-Activity Ledger + Pre-Classifier Reference Resolution; substrate = existing `conversation_turns` + #952 ArtifactDB linked by session/turn→artifact association; D4 classifier-stays-stateless is the integrity constraint
- **v0.8.10.12 cut**: 45 files, including 7/9-morning items (Base unify, routing SSOT) that had never made any production cut; alpha/beta parity restored
- **Vercel admin migration** (Web): static export gate, GitHub Contents API dual-mode draft storage (SHA optimistic concurrency), 7-day httpOnly JWT admin auth; Next.js 15.4.11 CVE fix; Pro plan; Deployment Protection noted for custom-domain cutover
- **Blog published**: "The Server Crashed Mid-Draft" (insight, workDate 2026-05-17) — 14/14 template audit, storm-window.webp 129KB; Medium + LinkedIn syndicated
- **Watchdog Belt-2 routing fixed**: stall alerts re-routed from retired PM inbox to CIO inbox; tested with real isolated sandbox run (non-DRYRUN mode); 14 existing tests unaffected

### Impact

- 8 product defects found and fixed before first tester exposure
- v0.8.10.12 deployed to both alpha and beta environments with full parity
- 744-issue sprint-recovery complete; Production milestone 99/99
- All 11 alpha testers invited; welfare watch active
- blog: 22 stale draftPaths corrected (Comms); 2 metadata-prefix posts + 3 double-hero posts fixed (Web via #1392)
- CLAUDE.md -81 lines (658→577) from Jul 14 pass enabled by this day's CIO scoping + HOST endorsement
- Belt-4 operational for Docs; docs-duty-cycle scheduled-task retired (13 archived sessions)
- ADR-078 authored (session-activity ledger, pre-classifier antecedent resolution — architectural roadmap item)

### Session Learnings

- **Gate design validation**: the #1386 beta-gate found 8 defects + 1 architectural gap before tester exposure — the gate "earned its keep" in a single execution; re-scope-when-scope-is-uncertain is the right call when the original scenario can be reconstructed post-fix
- **Three parse-site copies**: `_parse_issue_detail` existed in 3 near-duplicate versions in one adapter — the HTML-entity bug required 3 sequential fixes (one per copy); consolidation candidate (#1397 discipline: meta-debt is worth tracking)
- **Comms fact-checking pattern confirmed**: same "adjacent-story number contamination" shape hit a third time (Beat 14: March 4 tag position vs June 3 actual landing — both real facts from the same log, attached to the wrong sentence); memory file (`feedback_adjacent_story_number_contamination.md`) updated with third confirming instance
- **Verify negatives via live API**: PPM guessed two planning files were missing based on a local `git ls-tree` against an assumed path; PM's "check GitHub before asserting a negative" caught it; both files present one directory up (`gh api repos/.../contents/` is the correct tool)
- **CIO cron-listing discipline**: post-reboot `CronList` showed a pre-reboot job with zero fire evidence — treated the listing as unreliable rather than trusting it, then delete-then-create-then-verify; the discipline shipped 7/10 was immediately applied
- **Docs duty-cycle provenance tracing**: CIO traced `docs-duty-cycle` to the exact transcript session that created it (via `search_session_transcripts`) rather than answering from impression; found the mechanism change was never itself surfaced for PM ratification — the "investigate before extending" discipline applied to an architecture question, not just code
- **Sprint-recovery backup now has a restore**: `scripts/restore-sprint-field-from-snapshot.py` closes the gap where a dated TSV backup existed but nothing could use it to recover; dry-run tested against same-session snapshot before declaring done

---

*Sources archived in `dev/2026/07/12/` (11 files).*
