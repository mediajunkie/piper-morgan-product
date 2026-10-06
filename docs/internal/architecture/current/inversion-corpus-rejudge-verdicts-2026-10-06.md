# Inversion corpus re-judge: verdicts on stale expectations (2026-10-06)

**Author**: PPM (destination verdicts; CXO owns experience wording, Arch owns the gate rule, Lead owns the single corpus commit)
**Asked by**: Lead, three memos on 10-06 (the #1951 re-judge, the week_calendar text-4 landing plus a 13th row, the four GUIDANCE advice rows)
**Source report**: `inversion-week-calendar-listing-only-score-2026-10-06-anthropic.md` (full corpus, 514 rows, the latest of the three 10-06 reports)
**Status**: proposal for Lead's commit(s). PPM does not edit the corpus yaml or `build_inversion_corpus_phase0.py`.
**Revision 3 (10-06 ~16:00 PDT)**: applies Lead's parked-re-judge memo (three premise corrections) and Arch's three ledger rules. Changes are marked REV3 in the rows below; the landing split is in the new section "Landing split (REV3)". The deletion ledger (`scripts/inversion_phase3_deleted_patterns.json`, 399 phrases) was cross-checked by script this turn, which is how the ledgered REVIEW rows below were found. My first two revisions did not check it, and that was the gap.

## What this is, in one paragraph

Lead asked about 12 or 13 rows whose expectation predates the 10-04 operation split and the 10-06 text changes. Reading the same report shows those rows are only the regression delta. The report holds about 68 asserted mismatches (76 lines before de-duplication), and most are the same disease: the expectation names an old destination (`manage_portfolio`, `meeting_time`, `generate_report`) or a destination for a referent-less phrase where the router's honest answer is CLARIFY. A mismatch that is really a stale expectation must not count against a deletion (Lead's words), so the whole set needs one pass, not the 13.

## Rule used for every verdict (one rule, applied the same way each time)

1. **Router right, expectation stale** → re-point the row to the router's operation (or to `floor` when CLARIFY/NONE is the honest answer).
2. **Phrase has no referent** ("this", "here", "that topic") and the right answer depends on a prior turn → `REVIEW` (unasserted), per the existing precedent that context-dependent rows are not asserted. The corpus is single-turn; scoring a multi-turn phrase single-turn scores the corpus, not the product.
3. **Router wrong, expectation right** → the row stays, it is a real miss, and it is evidence for Epic 0 (a corpus row, not an issue, per the Epic 0 clause).
4. **A write operation selected for a read ask** → always a real miss, never re-pointed.

## Batch A: the rows Lead asked about

| Row (phrase) | Now expects | Router said | Verdict | Why |
|---|---|---|---|---|
| `what projects do I have?` and `what are my projects?` | `manage_portfolio` | `list_projects` @0.95 | **Re-point to `list_projects`** | `manage_portfolio` is a CANONICAL umbrella the 10-04 split retired for reads; `list_projects` is the live QUERY entry. The Exhibit-A completeness guards sit on the handler, so the destination is the one that carries them |
| `what projects am I working on` | `manage_portfolio` | `list_projects` @0.95 | **Re-point to `list_projects`** | Same |
| `link mediajunkie/test-piper-morgan to the project`, `connect octocat/hello-world to the project` | `manage_repos` | `link_repo` @0.75 / @0.85 | **Re-point to `link_repo`** | A named owner/repo is exactly what `link_repo` takes |
| `add octocat/hello-world to the project` | `manage_repos` | CLARIFY @0.4 | **Re-point to `link_repo`; keep asserted; REAL MISS** | Same shape as the two rows above that route; "add" is the only difference. Not stale |
| `link my repository to the project`, `connect my repository to the project` | `manage_repos` | CLARIFY @0.4 | **Re-point to `floor`** | No repository named; asking which is correct and safe |
| `please unlink my repository from this project`, `please remove…`, `please disconnect…` | `unlink_repo` | CLARIFY @0.4 | **`REVIEW`** | "This project" and "my repository" are both referents; unlink is destructive, so CLARIFY is the right behavior. Keep the live-probe row for the confirm path (#1926), where the destructive consequence is gated |
| `I could use some guidance on this`, `do you have a recommendation`, `what's your advice here`, `advise me on this decision` | `get_contextual_guidance` | CLARIFY @0.3–0.6 | **`floor`** (REVISED 12:40 from `REVIEW`) | CXO ruled 10-06 10:25 that CLARIFY is an acceptable served answer for a subject-less advice ask, on two conditions: (A) the clarification is armed or declarative, copy unread so far (unverified); (B) the turn-2 probe below exists. `floor` matches CLARIFY/NONE, so it asserts the router does NOT pick `get_contextual_guidance` on a bare turn |
| `ok that's merged, what now?` | `get_contextual_guidance` | `get_top_priority` @0.85 | **REV3: re-point to `get_top_priority`** (was `REVIEW`; the row is ledgered under GUIDANCE_PATTERNS, so it may not be REVIEW) | "What now" after a merge is a next-step ask, and the top priority answers it. Router right, expectation stale (rule 1). Destination is floor-served (no rail entry), so this one parks (see landing split) |
| `just getting started here` | `greeting` | (greeting) | keep, already ruled by CXO 09-28 | n/a |
| `what's my available time` | `floor` | `week_calendar` @0.72 | **Re-point to `week_calendar`** | #1880 (free blocks, truncated lists) is closed, and the week_calendar text-4 landing is the listing that answers it. Same for `when's my next free slot`, see Batch B |
| `show today's tasks` | `list_todos_query` | `attention_query` @0.85 | **REV3: stays `list_todos_query`; REAL MISS** (was `REVIEW`; the row is ledgered under STATUS_PATTERNS) | Ruled 10-01 by CXO and PPM to `list_todos_query`; the router's answer is a different list ("what needs attention"), not a task list. An asserted expectation that was already in force: no change to the corpus, and the miss is Epic 0 evidence |
| `what are the key tasks for this sprint` | `floor` | `get_contextual_guidance` @0.85 | **Stays `floor`; REAL MISS** | There is no sprint task view; the 10-01 ruling is that the honest destination is the floor. Guidance is the wrong answer |
| `what am I working on?` | `floor` | `session_activity_query` @0.7 | **Stays `floor`; REAL MISS** | Ruled 10-01 by CXO (PPM conceded). Not reopened |
| `is my calendar showing any conflict`, `is there a conflict on my calendar`, `check my calendar for conflicts` | `floor` | (router differs) | **Stays `floor`** | CXO's 10-06 ruling (conflict detection is not a listing; the floor must say it cannot compute one). Not reopened |

## Batch B: the rest of the report's asserted mismatches

### B1. Op-split re-points (the router is right; the expectation names a retired destination)

| Phrase(s) | Re-point to |
|---|---|
| `archive CoVa`, `Archive my project "Test"`, `Archive my project called "Test" please`, `Archive my project Test.`, `Archive my Test project, please.`, `Archive the project called Test` (each appears in two blocks of the report) | `archive_project` |
| `restore CoVa` (two blocks) | `restore_project` |
| `list my archive projects` | `list_archived_projects` |
| `list my active projects for this quarter`, `what are my current projects` | `list_projects` (the "quarter" qualifier is dropped by the handler; that is a handler-honesty question already carried under #1645, not a routing one) |
| `please show my linked repos`, `can you show project repositories for this account` | `list_repos` |
| `what is on my calendar`, `what meetings are coming up` | `week_calendar` (the old `meeting_time` destination is minutes-in-meetings, the wrong question) |
| `when's my next free slot`, `what's my available time` | `week_calendar` |
| `I need a status report`, `give me a project status report` | `get_project_status` (`generate_report` has no registry entry). REV3: ledgered under STATUS_PATTERNS and floor-served, so this re-point re-ledgers against the 10-06 report and parks (see landing split) |
| ~~`analyze the file I uploaded`~~ | **REV3: re-point WITHDRAWN.** My condition failed: `analyze_document` is the Notion-document analyzer (`read_referent`), not the uploaded-file handler (Lead's check). The router choosing a Notion op for an upload is a real miss: the row keeps its expectation and gets counted in B4 (Arch asked for a row for it) |
| `prs needing review` | the router's PR-list op (registry key `list_prs_query`; use whichever spelling `p0.matches` accepts). Currently `floor`, which predates the op |
| `I need to remember to submit my timesheet` | `create_todo` (no time was given, so a reminder has nothing to fire on) |
| `show today's progress` | `session_activity_query` |

Archive is a write. Re-pointing the expectation does not weaken the gate: the router names the operation and permission code still decides, as the inversion architecture intends (LLM decides meaning, code decides permission).

### B2. Honest-CLARIFY rows (expectation should be `floor`; CLARIFY or NONE is the right answer)

| Phrase(s) | Why |
|---|---|
| `I need help understanding something` | "Understanding what?" is the question |
| `please close this issue` | A write with no referent; CLARIFY is the only safe answer |
| `our history together has been good`, `what we discussed yesterday was helpful` | Statements, not requests; NONE @0.95 is correct |
| `search history for that conversation topic` | "That topic" has no referent in a single turn |
| `remind me` (bare) | Nothing to remind about |
| ~~`any upcoming milestones for this project`~~ | **REV3: WITHDRAWN.** My premise was wrong: `list_milestones` is a live rail entry (`workflow_entries.py:1330`, Lead's check; my grep was scoped to `action_registry.py` and missed it). The row keeps `list_milestones`; the router's CLARIFY is about "this project" and is a real miss or a CLARIFY-honest question, not a stale expectation. Row unchanged |
| `quick check, working on now?` | Same family as `what am I working on?`, ruled floor 10-01 |

### B3. `REVIEW` (unasserted; two defensible answers, or a referent only a prior turn supplies)

| Phrase | Why |
|---|---|
| `can you run an impact analysis on this change` | "This change" has no referent, and impact analysis is not what `analyze_blockers` does either |
| ~~`mark this as priority one`~~ | **REV3: not REVIEW.** The row is ledgered (PRIORITY_PATTERNS). Asserted as `prioritize` (a write), the CXO ruling of 09-30 that Lead and Arch both cite. Keep it; I do not ask for a different call |
| ~~`not sure what to do about this`~~ | **REV3: not REVIEW.** The row is ledgered (PRIORITY_PATTERNS). Same family as the four GUIDANCE advice rows, so the same asserted call: `floor`, on CXO's conditions A and B. Parks with them |
| ~~`schedule check for today`~~ | **REV3: not REVIEW.** The row is ledgered (TEMPORAL_PATTERNS). Asserted as `week_calendar`: "check my schedule today" is a calendar listing, which the text-4 landing now serves (rail entry). Unverified against the live router's answer for this phrase: if it names something else, that is a real miss and Epic 0 evidence |
| `what's the project landscape` | `list_projects` (the router) and `get_project_status` (the expectation) are both defensible overviews; CXO's call if it ever matters |
| `which repo connected to this project should i check` | Advice about "this project"; CLARIFY is honest |
| `show me all project plans` | **REV3**: `search_documents` IS a live rail entry (`workflow_entries.py:3782`, Lead's check; my grep missed it). The row stays `REVIEW` (it is not ledgered, so REVIEW is allowed), but the reason is "plans" (which documents?), not "no op". Tracked under #1949 |

### B4. Real misses (expectation right; the router is wrong; evidence for Epic 0, rows stay)

| Phrase | Expected | Router said | Note |
|---|---|---|---|
| `show priorities for this sprint` | `floor` | `prioritize` @0.85 | **A write verb picked for a read ask (rule 4).** The one that matters most here. A guard clause in the `prioritize` rail description is the fix, and it needs the full-corpus run |
| `edit my project description` | `floor` | `update_document` @0.85 | A write operation selected for an ask it cannot serve (rule 4) |
| `what's my focus this week` | `get_top_priority` | `week_calendar` @0.72 | "Focus" is not a calendar |
| `what are my focus areas this sprint` | `get_top_priority` | `get_contextual_guidance` @0.72 | |
| `what are the key priorities this quarter` | `get_top_priority` | `strategic_planning` @0.85 | |
| `let's focus on today's priorities`, `what is my most important work today`, `what matters most this week` | `get_top_priority` | `attention_query` @0.85–0.92 | "Important" and "priorities" ask for ranked priorities, not "what needs attention". Judgment call without comparing the two handlers' live output; Lead can sample both before committing |
| `what's the most urgent thing`, `what's the most critical thing` | `get_top_priority` | `attention_query` @0.92–0.95 | **Re-point instead to `attention_query`** (urgent and critical are the attention family). Listed here only because the call is a split from the three rows above |
| `any update on the next milestone` | `get_project_status` | `analyze_blockers` @0.72 | "Update" is status, not blockers |
| `what's in the way of finishing this`, `what's the main obstacle here` | `analyze_blockers` | CLARIFY @0.4 | Blocker analysis runs at project level and does not need the referent. A description clause ("what's in the way", "obstacle") closes both, bundled with the other description edits for one rescore |
| `pull up my schedule` | `week_calendar` | `meeting_time` @0.72 | |
| `show the team schedule` | `floor` | `week_calendar` @0.72 | Honesty-adjacent: the router answers a team ask with the user's own calendar |
| `tell me what I'm working on`, `show my active work` | `floor` | `session_activity_query` @0.7 / `attention_query` @0.85 | Same family as `what am I working on?` |
| `when's my next free slot` | now re-pointed (B1) | `meeting_time` @0.92 | The re-point makes this a miss, correctly: `meeting_time` is minutes in meetings |

## Landing split (REV3, Arch's rules 1 and 2 applied)

**Ledger rule (Arch rule 1)**: a re-point on a ledgered row re-ledgers it. The entry records the new expectation and the 10-06 report it was verified against, alongside the original deletion-time evidence. No literal is restored. **No ledgered row is `REVIEW` (Arch rule 3)**: the five that were are resolved above (`ok that's merged, what now?`, `show today's tasks`, `mark this as priority one`, `not sure what to do about this`, `schedule check for today`), and the four GUIDANCE rows were already moved to `floor` in revision 2.

**Land now**: B1 re-points whose destination is a rail entry. By `grep` of `workflow_entries.py` for the quoted op name (a string-presence check, not proof of an `action_triggered` registration; Lead owns the classification): `list_projects`, `archive_project`, `restore_project`, `list_archived_projects`, `link_repo`, `list_repos`, `week_calendar`, `list_prs_query`, `create_todo`, `session_activity_query`. That covers the Archive rows, `restore CoVa`, `list my archive projects`, the project-list phrases, the repo-list and link rows, the calendar and free-slot rows, `prs needing review`, the timesheet reminder and `show today's progress`.

**Park on the named trigger "PM's API-cost ruling"** (Exec's Decision F; the gate wants surface-2 probes for these, which are live spend):
- floor-served destinations: `get_project_status` (two status-report rows), `get_top_priority` (`ok that's merged, what now?`);
- every `floor` expectation on a ledgered row: the four GUIDANCE advice rows and `not sure what to do about this` (these also wait on CXO's condition B, the turn-2 probe), `please close this issue`, `quick check, working on now?`;
- the `floor` re-points on rows that are not ledgered (the repo-less link/connect rows and the other B2 rows) ride with the parked batch, because Lead's memo groups them with the floor-served ones. Lead decides if any of those can land now.

**Not applicable any more**: the `any upcoming milestones for this project` floor re-point and the `analyze_document` re-point (both withdrawn above).

## Counts, denominator stated

- Mismatch lines read: **76 unique lines** from the report's row-detail and gate-listing sections (some phrases appear twice, once per block). Distinct phrases are fewer; the table cells above de-duplicate by phrase.
- Verdict classes: counted by hand from the tables above, not by script: B1 re-points 22 phrases; B2 `floor` 8; B3 `REVIEW` 7 (plus Batch A's `REVIEW` rows); B4 real misses 18 phrases (two of them, `show priorities for this sprint` and `edit my project description`, are write-verb mis-selections).
- Shared-subset gate effect: the PORTFOLIO and QUERY REGRESSION cells (named regressions: the Archive rows, `what projects do I have?`, `analyze the file I uploaded`) are all in B1. Nothing else in the 08-12 shared subset regressed. **After the re-points, the regression delta against the 08-12 baseline should be zero, with the caveat that I did not re-run the scorer; the claim rests on Lead's re-run.**

## What I am asking for

1. **Lead**: one commit that re-judges these (yaml and `build_inversion_corpus_phase0.py`, which holds the rows), wires the three 10-06 reports into the Phase-3 deletion gate, and updates the 5 pins. Re-run the full corpus after, in the same lane (Arch's 10-06 rule).
2. **Lead** (now CXO's condition B, not only PPM's ask): a live turn-2 probe for the GUIDANCE advice phrases (state something in turn 1, then ask the advice phrase). This is the only way to tell whether "CLARIFY on a single turn" is truly honest or hides a router that fails on a real second turn. Until that exists, GUIDANCE deletion stays NO-GO (Lead's own position, unchanged).
3. **Arch**: add the full-corpus rule step (any commit adding a rail entry or changing a registry/rail description runs the full corpus in the same lane) to the Phase 3 procedure doc, so the next lane does not rediscover it from a regression table.
4. **CXO**: the armed-CLARIFY copy (a one-line question that names what is missing, e.g. "Which repository?") is worth a read before the repo-less link/connect rows go to `floor`, because those rows will now silently depend on CLARIFY wording.
5. **Optional, Lead + Arch, one rescore**: a "sprint/backlog tasks" clause on the `get_contextual_guidance` description and an "in the way / obstacle" clause on `analyze_blockers`, bundled with the `prioritize` guard clause. One description commit, one full-corpus run.

## Verified how

- **Method**: read the full-corpus report's gate table, row-detail section, and named-regressions list this turn; read `router_matches` in `scripts/inversion_phase1_shadow_score.py` this turn; grepped `action_registry.py` and `services/intent_service/*.py` this turn for each named destination.
- **Layer**: scorer semantics and registry source. **Not** the handler layer (the Exhibit-A completeness tests `test_project_list_source_1530.py` and `test_projects_lane_honesty_1645.py` were not run: no pytest or venv on this seat), and **not** a live router run (I re-scored nothing).
- **Denominator**: 76 mismatch lines from one report out of 514 rows; the 55 `REVIEW` rows already in the corpus and the 391 matched rows were not re-read.
- **Unverified**: that `analyze_document`, `update_document`, `strategic_planning`, `search_documents` and `list_milestones` are what their names suggest in the live catalog (only the router naming them is evidence they exist); the handler-level difference between `attention_query` and `get_top_priority` for the "important/priorities" rows; the post-re-point regression delta.
