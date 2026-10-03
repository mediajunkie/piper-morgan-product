# Workstream L — Claims-vs-reality ledger (tests H3, preregistration M3.1)

**Snapshot**: piper-morgan-product a191856 (read via `git show a191856:<path>`); GitHub state via read-only REST (`gh api`) on 2026-10-03; Phase 1 outputs cited by finding id. No server, no tests, no DB.
**Layer**: static (docs vs code/files) + record (GitHub issue/milestone metadata) + one live-GitHub read. **Denominator**: 60 sampled claims, 44 checkable (see per-stratum table), out of roughly 3,000+ candidate factual lines across the five sources.

## 1. Sampling rule (fixed before looking at content)
Per stratum, take the source file(s) at a191856; **candidate line** = non-heading, non-table-separator line of ≥50 chars that contains a backticked token, a number of ≥2 digits, "port", `.md` or `.py`. Take **every k-th candidate** (k per stratum chosen only to yield ~12 rows: briefing k=32 of 389; README+PROJECT k=4 of 49; architecture [intent-routing-stack.md + web-routes-conventions.md] k=125 of 1518; roadmap+vision [roadmap.md + vision.md] k=17 of 206; CLAUDE.md k=14 of 173). The claim rated is the **first checkable factual assertion on the selected line**; if the line contains none it is rated *uncheckable* and kept in the table (no replacement, no skipping). Script: `pick.py` (scratchpad; ~25 lines; reproduces the selection from the rule). Rows are in file order, not chosen for outcome.

Rating conventions (stated up front): *holds* = the factual assertion is true at the snapshot; a dated "as of X" or event-log entry that was true when written and is verifiable as such counts as holds (a **dated** claim is not penalised for later change, but see supplementary probes); *partly* = true in part or stale-but-dated; *false* = contradicted; *uncheckable* = needs live/PM-machine/process access or no evidence in reach.

## 2. Ledger
Claim location = `file:line` at a191856. Evidence: file:line, command, or finding id.

### (a) BRIEFING-CURRENT-STATE.md
| id | claim location | claim | rating | evidence |
|---|---|---|---|---|
| a1 | BRIEFING:78 | Phase 3 first deletion 09-27: extraction ceiling 567→558 | holds | tests/test_architecture_enforcement.py:2289-2292 ("567 -> 558 (2026-09-27 ...)") |
| a2 | BRIEFING:125 | Epic #1462 filed 2026-07-31, "Hosted MCP endpoint + plugin distribution (PDR-006 implementation)" | holds | `gh api issues/1462` → that title, created 2026-07-31 |
| a3 | BRIEFING:175 | #1331/#1333/#1231 trust arc: HOST/Arch rulings as described | uncheckable | issues exist and are closed (2026-06/07) but the rulings are mail-internal; not verified |
| a4 | BRIEFING:226 | PDR-005 BYOC v1.0 ratified June 5 | holds | docs/internal/product/pdr/PDR-005-bring-your-own-chat.md:3 "APPROVED (v1.0 — PM-ratified 2026-06-05)" |
| a5 | BRIEFING:267 | May 27-28 close burst, 11 issues closed (#1115, #1116, #1118, #1119 …) | holds (low) | `gh api` #1115/1116/1118/1119 all closed 2026-05-28; 4 of 11 verified, rest unverified |
| a6 | BRIEFING:314 | #1110 SlackClient `_make_request` calls `get_config()` without user_id, filed during #1085 | holds (dated) | #1110 filed 2026-05-23 with that title; code has since been fixed (slack_client.py:145 passes `self.user_id`), issue closed |
| a7 | BRIEFING:358 | #1090 Lead build-cost lens recommends 13-18 working days | holds | "13-18 working days" in dev/2026/05/15 cxo/arch logs + PDR-005 v0.4 draft; #1090 exists |
| a8 | BRIEFING:411 | Apr 21 audit flagged "86 services/ files with mock_/fallback" | uncheckable | point-in-time count; no snapshot of that date |
| a9 | BRIEFING:467 | Mar 15 floor-inversion investigation; Comms chat retired | uncheckable | process narrative |
| a10 | BRIEFING:561 | #932-#936 Security + infrastructure items | holds | titles: SEC HIBP stub / SEC key validation / orphaned stub / BudgetManager no persistence / UserService in-memory |
| a11 | BRIEFING:636 | Run 4 (May 8): routing 93.4%, quality 65.6% PASS | holds | both figures in dev/2026/05/08/canonical-retest-m2f-baseline-report.md |
| a12 | BRIEFING:710 | Footer: "Last Updated: July 16, 2026 …" | false | footer chain is out of order (Sep 1, Aug 12, Jul 16, Aug 1), front-matter says 2026-09-28, banner says Sep 29; a reader of the footer is misled on currency |

### (b) README.md and PROJECT.md
| id | location | claim | rating | evidence |
|---|---|---|---|---|
| b1 | README:31 | CONTRIBUTING.md exists (Contributing Guide link) | holds | file at snapshot |
| b2 | README:38 | same link (distinct sentence, same fact) | holds | same |
| b3 | PROJECT:19 | 4 staff + 7 leadership roles = 11 per ROSTER.md | holds | ROSTER.md: "Tier 1 (7 roles)", "Tier 2 — Staff (4 roles)". (CLAUDE.md says "3 staff" — cross-doc inconsistency, see S7) |
| b4 | PROJECT:27 | canonical agent registry at designinproduct `docs/agents/registry.md` | uncheckable | other repo, not in scope |
| b5 | PROJECT:36 | local directory name `piper-morgan` | uncheckable | PM machine; the checkout here is `piper-morgan-product` |
| b6 | PROJECT:42 | `production` = released builds; "Alpha testers pull from this branch" | **false** | BRIEFING banner (Version line): `production` branch deleted 2026-09-29, "deploys come from origin/main"; no `production` ref in the snapshot repo; alpha is hosted (Fly), not pulled. Related drift: test.yml:10 and security-tests.yml:18 still list `production` |
| b7 | PROJECT:57 | current state is in BRIEFING-CURRENT-STATE.md | holds | file exists |
| b8 | PROJECT:82 | web/app.py is 319 lines (as of 2026-05-12) | partly | `git show a191856:web/app.py \| wc -l` = 455; dated claim, but "refactor trigger at 1000" context now 45% used |
| b9 | PROJECT:102 | `services/intent_service/` = "universal entry point for all requests" | partly | entry point is `services/intent/intent_service.py` (`process_intent`; rail at :15670/:15877); `services/intent_service/` holds registries/handlers (A: intent routing = 55k LOC across both dirs) |
| b10 | PROJECT:106 | `services/knowledge/` is a RAG system with embeddings | holds | 63 "embedding" references under services/knowledge (code present; ChromaDB not exercised, per C env note) |
| b11 | PROJECT:128 | `docs/internal/architecture/patterns/` is the pattern catalog | holds | directory exists |
| b12 | PROJECT:175 | footer: web/app.py "933 → 319 on 2026-05-12"; "otherwise stable since Mar 14" | uncheckable | historical edit note |

### (c) Architecture docs (intent-routing-stack.md, web-routes-conventions.md)
| id | location | claim | rating | evidence |
|---|---|---|---|---|
| c1 | routing-stack:236 | `_act_on_resolved_targets` extracted from `maybe_handle_clear_family`'s tail | holds | services/intent_service/reminder_clear.py:573 and :764 |
| c2 | routing-stack:493 | regression test `test_multi_intent_floor_sibling_1763.py` exists | holds | file at snapshot |
| c3 | routing-stack:739 | post-turn observer's LLM leg is unscoped and uncached (`use_cache=False`) | holds | services/intent_service/inversion_shadow.py:367 `classifier.classify(message, use_cache=False)` |
| c4 | routing-stack:968 | Arch ruling memo `rule-arch-to-lead-cc-ppm-1595-unit4b-…-2026-09-26.md` in mailboxes/lead/read | holds | file exists at that path |
| c5 | routing-stack:1249 | rail keys: 102 incl. aliases (2026-08-02) | partly | dated and likely true then; C (§1) counts 144 live registry keys at snapshot, and the adjacent line says ACTION_REGISTRY "~43 pairs" vs C's 56. No sign of a refresh |
| c6 | routing-stack:1504 | `DESTRUCTIVE_ASK_BLOCKERS` stays live | holds | 4 references in services/intent_service/pre_classifier.py (shared-lane use not traced) |
| c7 | routing-stack:1693 | tests/unit/test_inversion_phase3_deletion_1595.py exists | holds | file at snapshot |
| c8 | routing-stack:1902 | `inversion-phase3-ruled-rows-rescore-2026-10-01-{19,20,43,44,52}.md` | holds | all five exist in docs/internal/architecture/current |
| c9 | routing-stack:2104 | probe found no reabsorption across 42 phrases | uncheckable | needs running the probe; out of scope |
| c10 | routing-stack:2325 | pre-classifier ceiling 329 → 277 | holds | test_architecture_enforcement.py ceiling comments "329 - 52 = 277" (then 277→259) |
| c11 | routing-stack:2521 | "5175 passed, 1 xfailed, 0 failed" on named files | uncheckable | no test runs allowed; B did not run that subset |
| c12 | web-routes:204 | `ui.py` has 27 root-level page routes (27 of 28 non-/api) | partly | at snapshot ui.py has 29 non-`/api/` route decorators + 1 `/api/v1/orientation/dismiss`; C counts 29 GET page routes. Count moved after the 09-23 measurement or method differs |

### (d) Roadmap / vision (roadmap.md v18.x, vision.md)
| id | location | claim | rating | evidence |
|---|---|---|---|---|
| d1 | vision:123 | floor-first routing confirmed working via UAT April 2026 | uncheckable | UAT record not in reach |
| d2 | roadmap:4 | Author/review credits (PA, CIO … ABSORBED v18) | uncheckable | process attribution |
| d3 | roadmap:32 | RECONNECT WS-1 closed Jun 22 incl. StandupAssembler (#1199) | holds | services/standup/assembler.py:61 `class StandupAssembler` (closure date unverified) |
| d4 | roadmap:79 | Conscious Floor … Investment-pillar extension (#950 v0.1 May) | uncheckable | design assertion |
| d5 | roadmap:140 | Surface 1 + Surface 7 "Unblocked NOW", ~4-6 working days | uncheckable | present-tense status in a body the doc itself marks as current only through 2026-07-16 (v18.8 changelog) |
| d6 | roadmap:197 | Klatch mechanism set on hold while Klatch is paused | uncheckable | other project |
| d7 | roadmap:238 | methodology-37 = Coverage-Audit Gate for Refactor Deltas | holds | methodology-37-COVERAGE-AUDIT-GATE-FOR-REFACTOR-DELTAS.md |
| d8 | roadmap:279 | Launch-in-worktree Option B canonical as of June 12; Model A DEPRECATED | **false (as current guidance)** | CLAUDE.md "Worktree model" (revised 2026-07-25): Model A is current on Amber, "neither is deprecated"; BRIEFING Current Operating Model says the same. Roadmap v18.8 stale-flag does not retract this line |
| d9 | roadmap:331 | doc-sync-sweep skill exists | holds | .claude/skills/doc-sync-sweep/SKILL.md |
| d10 | roadmap:375 | HOST 360 item 1.3 closed May 24 | uncheckable | process record |
| d11 | roadmap:398 | Enterprise milestone: July 4, 2027 "(from GitHub milestone)" | **false** | `gh api milestones`: Enterprise due **2028-10-30** (Production 2027-02-02, MVP 2026-10-30) — a 16-month discrepancy on a customer-facing date |
| d12 | roadmap:434 | v15.0 (Apr 11, 2026) archived | holds | docs/internal/planning/historical/roadmap-v15.0-2026-04-11.md |

### (e) CLAUDE.md operational facts
| id | location | claim | rating | evidence |
|---|---|---|---|---|
| e1 | CLAUDE:25 | ETA dormant, last session March 2026 (BRIEFING-ESSENTIAL-ETA.md) | uncheckable | briefing file exists (created 2026-03-13); no ETA-slug logs found by filename after 2025-11 (`test-code`), but slug history varies — not conclusive |
| e2 | CLAUDE:103 | `check-branch.sh` decides via `git diff --cached --name-only` | holds | .claude/hooks/check-branch.sh:28 |
| e3 | CLAUDE:161 | credential resolution "Keychain first, then env — see llm_config_service.py:213" | partly | order holds (keychain at ~:327, env after) but a new Priority-0 per-request key (#1814) precedes it, and :213 is now inside the `get_configured_providers` docstring; real code is `get_api_key` at :265 |
| e4 | CLAUDE:204 | actions dispatch via rail in `process_intent`; ratchet `MAX_DISPATCH_SITES` | holds | intent_service.py:15670/15877 `get_action_workflows()`; tests/test_architecture_enforcement.py:526 `MAX_DISPATCH_SITES = 0` |
| e5 | CLAUDE:256 | 2026-08-27 incident: 33 commits had landed in the gap | uncheckable | incident narrative |
| e6 | CLAUDE:325 | methodology-43 = "Name the layer" | holds | methodology-43-NAME-THE-LAYER.md |
| e7 | CLAUDE:377 | docs/briefs/cross-pollination/current.md | holds | exists |
| e8 | CLAUDE:413 | audit-cascade SKILL.md has Step 1b (dispatch tier) | holds | SKILL.md:67 "### Step 1b: …audit the dispatch tier" |
| e9 | CLAUDE:523 | docs/internal/operations/memory-eval-pilot.md | holds | exists |
| e10 | CLAUDE:635 | docs/internal/operations/github-and-tooling-gotchas.md | holds | exists |
| e11 | CLAUDE:666 | docs/internal/architecture/decisions/claude-md-history.log | holds | exists |
| e12 | CLAUDE:715 | "This repo is PUBLIC" | holds | `gh api repos/mediajunkie/piper-morgan-product` → visibility public |

## 3. Statistics (share of CHECKABLE claims that hold fully)
| stratum | rows | uncheckable | checkable | holds | partly | false | holds / checkable | Wilson 95% |
|---|---|---|---|---|---|---|---|---|
| (a) BRIEFING-CURRENT-STATE | 12 | 3 | 9 | 8 | 0 | 1 | **89%** | 57–98% |
| (b) README + PROJECT | 12 | 3 | 9 | 6 | 2 | 1 | **67%** | 35–88% |
| (c) architecture docs | 12 | 2 | 10 | 8 | 2 | 0 | **80%** | 49–94% |
| (d) roadmap / vision | 12 | 6 | 6 | 4 | 0 | 2 | **67%** | 30–90% |
| (e) CLAUDE.md | 12 | 2 | 10 | 9 | 1 | 0 | **90%** | 60–98% |
| **overall** | **60** | **16** | **44** | **35** | **5** | **4** | **79.5%** | **65.5–88.8%** |

Uncheckable share: 16/60 = 27% (highest in roadmap/vision, 50%).

## 4. Verdict on H3 (rule applied literally)
Rule: **Supported if fewer than 80% of checkable claims hold fully; Refuted if ≥ 90% hold.** Observed 35/44 = **79.5% < 80% → H3 SUPPORTED by the letter of the rule. It is not refuted (needs ≥ 90%).**

Read with care: **the verdict is a coin-flip at the margin.** One claim moving either way flips it (34/44 = 77% / 36/44 = 82%), and the 95% interval (65–89%) straddles 80%. The rule's supported/refuted/in-between structure would honestly label this "supported, weakly." What the sample does show robustly is the **shape** of the drift (below), not a precise rate.

Sampling caveats that cut both ways. (1) Many sampled claims are existence checks (file/path exists), which pass trivially and inflate the rate; the claims that fail are the ones that make a *state assertion*. (2) The briefing is mostly a dated event log, which my "true as dated" convention rates as holding; its present-tense Status Banner lines were hit only by the supplementary probes. (3) CLAUDE.md is the best-maintained surface (90%) and the roadmap/PROJECT the worst, matching which documents have an owner refreshing them per the duty cycle.

## 5. Supplementary probes (NOT in the H3 statistics — targeted at present-tense state claims, chosen after the fact, so selection-biased toward finding drift)
| id | claim location | claim | rating | evidence |
|---|---|---|---|---|
| S1 | BRIEFING STATUS BANNER (Sprint Structure line) | "M2g-C+ ... ← ACTIVE — 6 closures May 15" | false | same banner says Alpha is Fly v151 in late Sept; the "ACTIVE" sprint line is 4.5 months old |
| S2 | BRIEFING Current Position (09-29) | "no CI deploy workflow exists yet (#1849 open until one does)" | partly (stale by snapshot) | `.github/workflows/fly-deploy.yml` added 2026-09-29 (commit a0f1722827); B5: 100 runs, 89 success, not gated on tests |
| S3 | BRIEFING Current Focus (09-29) | "next deposits PRIORITY 44 / CALENDAR 49 / TEMPORAL 54" | partly (stale) | PRIORITY and CALENDAR deleted 10-01/10-02 per ceiling comments (376→329, CALENDAR 52 literals); attested 09-29, snapshot 10-03 |
| S4 | BRIEFING Version line | v0.8.14.0 live | holds | C: running server reports 0.8.14.0 |
| S5 | CLAUDE.md Ports | 8001 / 5433 / 6379 / 8000 | holds | docker-compose.yml:38,63,101,116; main.py:37 default 8001 |
| S6 | CLAUDE.md Critical Paths | main.py, domain/models.py, shared_types.py, config/PIPER.md, PIPER.user.md.example, intent_enforcement.py | holds (8/8 exist) | `git cat-file -e` |
| S7 | CLAUDE.md role table vs ROSTER | "7 leadership + 3 staff + specialized" | partly | ROSTER.md Tier 2 = 4 staff; PROJECT.md says 4 |
| S8 | BRIEFING Migration State | "All 7 leadership roles on Code … Migration arc complete" | partly | Amber migration (07-25) is described elsewhere in the same file as ongoing; this line is Apr-era and unlabelled |

Supplementary: 3 hold, 3 partly (stale-by-days), 2 false/partly-stale in the briefing banner. Pattern: **state assertions at the top of the briefing age in days; durable pointers (paths, ports, file existence) are reliable.**

## 6. Notable falsehoods and their impact
1. **PROJECT.md:42 — `production` branch "alpha testers pull from this branch" (b6).** The branch was deleted 2026-09-29; deploys are from main to Fly. PROJECT.md is a first-load orientation doc, and its "Upgrade instructions should reference `production`" would send an agent or tester to a nonexistent ref. Also, CI workflows still trigger on `production` (test.yml:10, security-tests.yml:18) — dead config echoing the same stale model. Impact: medium (orientation error, cheap to fix).
2. **Roadmap:398 — Enterprise milestone "July 4, 2027 (from GitHub milestone)" (d11).** The cited source says 2028-10-30. A 16-month error on an externally relevant date, with the provenance claim itself wrong. Impact: medium-high if the roadmap is shown to anyone outside.
3. **Roadmap:279 — "Model A DEPRECATED" (d8).** Directly contradicts the current worktree rule in CLAUDE.md (Model A current on Amber). Agents reading the roadmap would pick the wrong worktree model; the roadmap's v18.8 stale-flag did not retract it. Impact: low-medium (CLAUDE.md wins in load order).
4. **BRIEFING footer "Last Updated July 16" (a12) and the banner's "M2g-C+ ACTIVE" (S1).** Metadata that mis-states currency in the document CLAUDE.md tells every agent to refresh on a staleness hook. The hook watches front-matter dates, which are fresh (Sep 28) even where banner sub-lines are not — a "fresh date, stale lines" mismatch, i.e. a **false clear** in the sense of m-44. Impact: medium.
5. **Count drift in architecture docs (c5, c12, b8)** — dated numbers that are never refreshed (rail keys 102 vs 144 live; ACTION_REGISTRY ~43 vs 56; web/app.py 319 vs 455). Each carries a date so is not strictly false, but the docs give no signal that the number moved. Impact: low individually; they cost trust in every other number.

## 7. Implication for the guiding question ("should we change anything?")
Yes, narrowly and cheaply: (i) fix the three false sentences above (PROJECT.md production branch, roadmap Enterprise date and Model-A line) — minutes of work; (ii) stop treating front-matter `last_updated`/`last_verified` as a freshness signal for the briefing banner — add a per-section "attested-through" check or have the staleness hook compare banner-line dates to the latest commit; (iii) do not spend effort on a general doc-accuracy campaign: path/port/mechanism claims in CLAUDE.md are ~90% sound; the drift is concentrated in *dated counts*, *present-tense status*, and *superseded rules left in secondary docs* (roadmap/PROJECT). Confidence: medium (n=44, wide interval, existence-heavy sample).

## 8. Unobservables found (appended per instruction; not added to unobservables.md)
- **UL-1** Whether the 16 uncheckable sampled claims (27%) hold: they are process narratives (rulings, UAT, incident counts) and other-repo facts. Why: evidence lives in mail/session logs written by the same cohort, or off-repo. How: a second, independent corroboration pass against GitHub issue timelines and dated omnibus logs, or a sample of 10 audited by a person who was present.
- **UL-2** True-as-dated rate of the briefing's event log vs. any later reversal: I rated entries on whether they were true when dated; reversals (e.g. #1110 fixed since) are not tracked by the doc. How: diff each cited issue's later state against the entry.
- **UL-3** Whether the briefing banner was refreshed on Oct 1-3: the snapshot's last banner attestation is 09-29, so S2/S3 staleness could be a normal 4-day lag, not neglect. How: look at BRIEFING-CURRENT-STATE.md commit cadence over several weeks (D0-style) to estimate typical banner lag.
- **UL-4** Claim-level truth of runtime-state banner lines (Fly v151, sprint counts "25 not done", Redis missing on staging): needs live Fly/GitHub-board access; the Projects v2 board is unreachable (GraphQL blocked in this sandbox).

## Top findings for synthesis
1. **L-1** H3 supported by the literal rule at 35/44 = 79.5% (95% CI 65–89%), refuted-threshold (90%) missed; verdict is marginal — ±1 claim flips it.
2. **L-2** Drift concentrates in dated counts, present-tense status lines and superseded rules in secondary docs (roadmap 67%, PROJECT/README 67%); CLAUDE.md (90%) and the briefing's dated event log (89%) are comparatively sound.
3. **L-3** Three actionable false statements: PROJECT.md `production` branch (deleted 09-29), roadmap Enterprise date (2027-07-04 vs GitHub 2028-10-30), roadmap "Model A deprecated".
4. **L-4** Front-matter freshness dates give a false clear on the briefing: `last_updated 2026-09-28` coexists with a July footer and a May "ACTIVE" sprint line.
5. **L-5** 27% of sampled claims are uncheckable from the repo; process narrative in the briefing is effectively unauditable without mail/log access.
