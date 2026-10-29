# Ongoing milestone triage, proposed sort (Docs, 2026-10-29)

Requested by xian 10-29. **Proposal only: no Sprint field has been changed.** Sprint changes wait for xian's yes (and go through skill `assign-sprint-safely`, per item).

**Denominator.** Milestone "Ongoing" read live 10-29 ~08:00 PT: 57 open issues (xian saw 54, the milestone API said 58, `gh issue list` and GraphQL both returned 57; I read all 57). 20 already carry a Sprint (FLYWHEEL 14, Q 4, SKUNK 1, Beta Blockers 1). 37 had no Sprint (33 on the board with an empty Sprint field, 4 not on the board at all: #1923, #1967, #1968, #2126). I closed #1369 myself (below), so **36 are proposed here**. Bodies of all 37 were read (first ~500 characters plus comment counts), not comments in full.

**Context that shapes the sort.** PPM moved many of these Production → Ongoing on 10-24 under xian's ruling 2 (comment on #1369): an issue leaving Production loses its PROD-* Sprint. So PROD-* is the wrong answer for most of these, and "neither Q nor FLYWHEEL" is expected for the code backlog. The board has **no Icebox sprint or status** (Status options: Product Backlog, Sprint Backlog, In Progress, In Review, Done, Blocked). Adding a Sprint option means `updateProjectV2Field` with a full options list (hard rule 4 risk), so I propose a plain `icebox` **label** instead (nothing exists today; closest are `post-beta-priority` and `awaiting-decision`). CIO asked to weigh in.

## Update 10-29 08:1x: replies in (Exec, CIO, HOST, PPM)
- **Closed since the proposal:** #1940 (PPM showed PM ruled it 10-06 and the rule is written at `docs/internal/planning/beta-gate-standard.md` lines 72-90; I closed it with description banner and evidence comment, since PPM's seat was blocked), #1923 (CIO: done 10-03 in `2840b6c89c`), #2144 (Exec: 549 Alpha Health Watch runs green since 10-24). Section C below shrinks from 8 to 5: #1968 (CIO), #1927 (owner unclear: not in this repo, Exec to say who runs the usage reader), #1953 and #1457 (Lead's CI decisions, CIO contributing), #1967 (HOST agrees FLYWHEEL, says most is built and will close or name the leftover).
- **#1908:** Exec noted it cannot be both FLYWHEEL and iceboxed. My pick: **icebox only** (no sprint), per PM's "not urgent". Icebox total is now 11: the 9 in D, #1908, #1954 (HOST agreed).
- **Icebox mechanism (CIO agrees):** a label, with one condition: each iceboxed issue gets a one-line comment "Iceboxed YYYY-MM-DD; revisit when <named trigger>", and the label's description says so. #1954's trigger is a named tester failing to redeem.
- **#1300 and #1340:** product question for PPM and xian (does 1.0 include a public marketplace listing). #1340 follows #1300. **#1900:** Lead's.
- **Default owner:** PM's 10-06 table gives milestone Ongoing a default owner of **Docs** (beta-gate-standard.md line 82ff), so unowned Ongoing issues are mine to answer for. I still route build work to Lead.
- Exec has the proposal on rollup v648 with a lean yes on all three questions.

## A. Done by Docs
| # | Action |
|---|---|
| 1940 | Closed (see update above). |
| 1369 | Deleted `coordination/` and 3 `worktree-*.sh` scripts (commit 7f622fd967, 8 files, zero live callers by git grep), commented and closed. |

## B. Proposed Q - Recurring Audits (2)
| # | Why | Owner |
|---|---|---|
| 1909 | Quarterly Maintenance Sweep Q4, an automated recurring reminder. Last box (test-fixtures review) is Lead's after 10-30. | Docs / Lead |
| 1904 | Three docs 300+ days stale, found by the weekly docs audit. Needs a technical read against code (`api-key-management.md` against `KeychainService` first). | Docs, with Lead for the code check |

## C. Proposed FLYWHEEL - Process improvement (8)
| # | Why | Owner |
|---|---|---|
| 1940 | Rule: who assigns gate vs build work. PM said yes 10-05; PPM owns the written rule. | PPM |
| 1967 | OWED-line scanner (Agent 360 v0.5). | HOST + CIO |
| 1968 | Agent 360 v0.5 tooling follow-ons for CIO. | CIO |
| 1923 | `mail-send.sh` should refuse mailbox paths over 180 chars (caused 11 red runs 10-03). | CIO / Pard |
| 1927 | `usage-read.sh` SHAPE-CHANGED on 16 of 44 overnight readings. | CIO (Exec found it) |
| 1953 | Decide whether CI runs `tests/intent/ -m "not llm"`. A decision, not a build. | Lead + CIO |
| 1457 | `ci.yml` red 100+ runs. Instance (the bad filename) is already removed (`git ls-files` empty); the open box is the guard decision. | CIO / Lead |
| 1908 | Building-narrative sequence number as its own field. PM wrote "food for thought, not urgent". | Comms; **icebox candidate** |

## D. Neither Q nor FLYWHEEL (24): for Lead's backlog, with icebox candidates marked
These are code, test and distribution items. Lead assigns build work (#1940's rule). Where I could check cheaply I did; "appears done" means a file named in the issue is gone from `origin/main`, not that I verified every acceptance box.

**Appear already done or moot (Lead to confirm and close):**
| # | Evidence |
|---|---|
| 1287 | `services/orchestration/multi_agent_coordinator.py` is gone (island deleted in `ed8d281e1c`, #1436 Family-2). |
| 1526 | `services/personality/standup_bridge.py` is gone (`66ab780bdd`, #1775). |
| 1167 | `services/orchestration/` no longer exists, so the Dockerfile in the issue is gone. |
| 1921 | `yaml.safe_load('tests/fixtures/inversion_corpus_phase0.yaml')` now loads without error (run this fire). |

**Real work, keep, Lead to place:**
| # | Note |
|---|---|
| 1436 | mypy CI gate, **already In Progress** on the board (9 comments). Leave. |
| 1522 | False-trails audit umbrella (8 comments); already Sprint Backlog status. |
| 1698 | SPATIAL-DISPOSAL epic; already Sprint Backlog status. |
| 1211 | AST sweep for local-import shadowing plus broad-except stealth-dead code. |
| 1474 | Delete or fix `_get_dynamic_capabilities` (zero callers). Fits the dead-code family with 1522. |
| 1449 | Real performance and coverage gates. |
| 2015 | Bug: `edge_type` passed as str. |
| 1151 | Bug: `/intent` returns empty `original_message`. |
| 2126 | Order-dependent flaky test. |
| 1922 | Spend-free ratchet lost its generic GUIDANCE pair. |
| 1900 | [COST] prompt caching off across 113 call sites. Likely worth a decision soon (CIO's cost lane). |

**Icebox candidates (not planned soon):**
| # | Why |
|---|---|
| 865 | Setup-wizard refactor, body says "PM to triage for MVP or post-MVP", P3. |
| 959 | MCP Apps artifact canvas (DIST). |
| 1001 | Owner-review of publisher retry, `priority: low`. |
| 1028 | PERPLEXITY leftovers in 4 files. |
| 1138 | Naming clarity, `priority: low`. |
| 1144 | Test-discipline refactor, `priority: low`. |
| 1300 | BYOC credential decouple (public-marketplace gate). Bigger decision; CIO/PA to confirm it is not needed for 1.0. |
| 1321 | Scattered TODO sweep ("before M5 polish"). |
| 1340 | RECONNECT UX fold, labelled `post-beta-priority`. Keep out of icebox if post-beta is soon. |

## E. Neither, not code
| # | Proposal | Owner |
|---|---|---|
| 1954 | Mint two replacement beta invites. PM deferred ("wait til they try and fail"). Icebox until a tester fails. | HOST |
| 2144 | "Alpha health watch: failing", an alarm issue, last stall 10-23. Its own text says close once alpha is steady. | Exec / HOST to decide |

## Already sprinted (20), not touched
FLYWHEEL: 683, 1389, 1391 (In Progress), 1392, 1403, 1608, 1629, 1680, 1719, 1721, 1726, 1779, 1780, 1834. Q: 1683, 1710, 1715, 1847. SKUNK: 1295. Beta Blockers: 1423. Several of the FLYWHEEL docs items (1719, 1721, 1726, 1779, 1780, 1389, 1392, 1403) are repo-file maintenance in Docs' lane; I have not started them and will pick them up once xian confirms this sort.

## Questions for xian
1. Icebox as a label, or something else? (A Sprint option is the riskier route.)
2. Is 1.0 definitely free of 1300 and 1340?
3. OK to put the four "appear done" issues to Lead for closure?
