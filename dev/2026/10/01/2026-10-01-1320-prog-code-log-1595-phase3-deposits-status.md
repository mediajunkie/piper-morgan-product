# 2026-10-01 1320 — prog (Coding Agent) — #1595 Phase 3 STATUS_PATTERNS deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for `STATUS_PATTERNS` only (56 literals). Touched
only the corpus builder, the fixture yaml, the ledger pin test's corpus-size constant, the scope
doc, and this session log. NO LLM calls made. No pattern deleted. No flag/env changed. Did not
touch git index (dispatcher instruction — no staging/commit performed).

## Read first (per dispatch prompt)

- `dev/2026/10/01/2026-10-01-1254-prog-code-log-1595-phase3-deposits-github.md` — method: call the
  REAL production matcher directly via `PreClassifier.pre_classify_with_pattern_list` +
  `_first_pattern_match`; row-shape convention (`# — LISTNAME` delimited block, `phrase`/
  `category`/`expected`/`source`[/`notes`] dict per row); the "no case for this family" shape
  (literals claim correctly but the action-determination branch funnels them to the wrong/generic
  action); the GITHUB correction precedent this dispatch asked me to apply preemptively.
- `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 — deletion gate" — the
  deletability rule (MATCH / agreeing-REVIEW / live-group MISMATCH), the UNSCORED-row tightening
  (2026-10-01, same-day as GITHUB's lane), and the `--live` flag mechanics.
- `services/intent_service/pre_classifier.py` — `STATUS_PATTERNS` (56 literals, lines 264-330),
  its claim branch in `pre_classify_with_pattern_list` (~1807-1816, checked after TEMPORAL
  [tombstoned]/GUIDANCE/ANALYSIS, before PRIORITY), `MILESTONE_STATUS_INLINE_PATTERNS` (an inline,
  non-class-attribute list at ~1502-1515, checked BEFORE GITHUB_QUERY_PATTERNS and STATUS_PATTERNS
  both), `PORTFOLIO_PATTERNS`/`PORTFOLIO_LIST_PATTERN` (checked at ~1366, before everything else
  relevant here).
- `services/intent_service/workflow_entries.py` (READ ONLY) — confirmed `get_project_status` has
  NO WorkflowEntry/flip_group (grep: zero hits); `show_standup`/`get_standup` registered with
  flip_group `read_status` (~2505); `manage_portfolio` also has NO WorkflowEntry.
- `services/intent_service/canonical_handlers.py` (READ ONLY) — `can_handle()`'s own docstring:
  "STATUS/PRIORITY removed Apr 13 (#925) — floor-routed via Action Gate"; `canonical_categories`
  set contains TEMPORAL/GUIDANCE/PORTFOLIO/CONVERSATION/PROVENANCE — STATUS absent, PORTFOLIO
  present.

## What I did

1. Ran the gate exactly as specified and quoted it (below). Confirmed 56 literals, 5/336 rows
   claimed, verdict NO-GO (2 pre-existing `[FAIL]` rows — "what am I working on?" and "show me my
   archived projects" — both pre-existing REVIEW/MISMATCH disagreements between the
   pre-classifier's claim and the router's actual route; left untouched per the dispatch's
   explicit instruction).

2. Computed the exact unexercised-literal set using the gate's own `unexercised_literals()`
   function (imported, not reimplemented) against `build_census()`'s claimed rows for
   `STATUS_PATTERNS`: **51 unexercised** (56 total − 5 literals exercised by the 5 pre-existing
   claimed rows — one literal per row, confirmed via set difference).

3. **Before drafting phrases**, investigated the claim branch directly (read, not inferred): all
   56 STATUS_PATTERNS literals return the SAME hardcoded action, `get_project_status` — no
   per-literal branching exists in this claim site, unlike GITHUB's partial if/elif. This is the
   "no case for this family" shape applied to the ENTIRE list, not a subset.

4. Checked for cross-list shadowing (the dispatch's explicit ask, following GITHUB's milestone
   finding) and found it in TWO places:
   - `MILESTONE_STATUS_INLINE_PATTERNS` (inline list, checked at ~1502, before even
     GITHUB_QUERY_PATTERNS and far before STATUS_PATTERNS at ~1810) contains 3 literals
     **byte-identical** to 3 STATUS_PATTERNS literals (`\bwhat'?s the (?:next|upcoming)
     milestone\b`, `\bmilestone status\b`, `\bmilestone progress\b`). Confirmed empirically
     ("milestone status please" / "milestone progress report" →
     `MILESTONE_STATUS_INLINE_PATTERNS`, not `STATUS_PATTERNS`).
   - `GITHUB_QUERY_PATTERNS` (checked at ~1532, before STATUS_PATTERNS) contains a literal
     byte-identical to STATUS_PATTERNS' `\bnext milestone\b`. Confirmed empirically ("next
     milestone details" → `GITHUB_QUERY_PATTERNS`, `action=review_issue_query`).
   Since these are **byte-identical regexes** checked earlier in the if-chain, any phrase matching
   STATUS's copy necessarily matches the earlier list's copy first — this is **mathematically**
   unreachable, not just empirically shadowed (phrasing-dependent, as CALENDAR/TEMPORAL's findings
   were). 4 of the 5 milestone-subfamily literals fall into this category; only
   `\bupcoming milestones?\b` has no duplicate anywhere in the file (grep-confirmed) and is
   reachable.
   - A 5th literal, `\bmy current work\b`, is shadowed WITHIN STATUS_PATTERNS by its own earlier,
     shorter sibling `\bcurrent work\b` (list position 3 vs 13) — "current work" is a guaranteed
     substring of "my current work" (preceded by a space, so a `\b` boundary is always present),
     so the shorter pattern provably claims first for every possible phrase. Confirmed with two
     independent phrasings, both claimed by `\bcurrent work\b`.
   Total unreachable: **5** (4 milestone + 1 current-work). Working set for deposit: 51 − 5 = 46.

5. Derived one natural PM-style phrase per reachable unexercised literal and verified each
   empirically against the REAL production matcher in a Python script:
   - `PreClassifier.pre_classify_with_pattern_list(phrase)` → asserted returned list name ==
     `"STATUS_PATTERNS"`.
   - `PreClassifier._first_pattern_match(cleaned, PreClassifier.STATUS_PATTERNS)` → asserted
     `.re.pattern` equals the specific cited literal.

   First pass: 34/47 clean (I initially included `\bmy current work\b` as a 47th candidate before
   confirming it unreachable). 12 failed and were reworded (all fixed on a single retry):
   - "list my projects" → claimed by **PORTFOLIO_PATTERNS** (a different, much-earlier-checked
     list, via the named `PORTFOLIO_LIST_PATTERN` constant, which matches "list" + optional
     "my"/"all"/"archived" + "projects" with strict adjacency). Reworded "list my active projects
     for this quarter" (inserting a word between "my" and "projects" defeats the strict-adjacency
     pattern while STATUS's own `.*`-spanning literal still matches).
   - "what am I working on now" → claimed by the earlier, already-exercised sibling `\bwhat am i
     working on\b`. Reworded "quick check, working on now?".
   - "show me my status" / "show me my standup" / "show me my progress" / "show me my tasks" /
     "show me my assignments" → each claimed by the corresponding earlier "my X" sibling (`\bmy
     status\b`, `\bmy standup\b`, `\bmy progress\b`, `\bmy tasks\b`, `\bmy assignments\b`).
     Reworded to "show {the current|today's} X" (dropping "my").
   - "how's my progress going" / "what's my progress looking like" → claimed by the earlier
     sibling `\bmy progress\b`. Reworded "how's the progress going" / "what's the progress looking
     like".
   - "list my tasks" → claimed by `\bmy tasks\b`. Reworded "list today's tasks".
   - "what tasks am I working on" → claimed by the much-earlier (list position ~11, not a
     same-list sibling of `\btasks.*working\b`'s ~40) `\bwhat.*working on\b`. Reworded "tasks I'm
     actively working on".

6. Deposited a `# — STATUS_PATTERNS` delimited block (extending the existing `# phase3-conversion`
   HAND_ROWS section, after the GITHUB_QUERY_PATTERNS block) in
   `scripts/build_inversion_corpus_phase0.py`: 46 rows, all `category: STATUS` (matching the
   existing corpus convention for this list — verified directly against the fixture, not assumed
   QUERY as GITHUB's EXECUTION/QUERY split required). `source` cites
   `phase3-conversion/STATUS_PATTERNS literal r"<the literal>"` per row.

   **Corrections applied** (per the dispatch's explicit instruction to pre-empt the
   Haiku-scoring-then-correct cycle GITHUB went through, where justified by a DIRECT anchor — not
   speculation):
   - 6 standup literals (`\bstand-up\b`, `\bstand up\b`, `\bstandup update\b`, `\bstandup
     report\b`, `\bdaily standup\b`, `\bshow.*standup\b`) → `expected: action:show_standup`
     (CORRECTED from the uniformly-claimed `get_project_status`). Anchor: the pre-existing,
     already-MATCH-scored row "give me my standup" (same list, same corpus,
     `claim=get_project_status`, `expected=action:show_standup`, `router=show_standup@0.95`,
     `verdict=MATCH`) already establishes this exact correction for the sibling `\bmy standup\b`
     literal. `show_standup` IS workflow-registered (flip_group `read_status`), unlike
     `get_project_status`.
   - `\bmy portfolio\b` and `\blist.*projects\b` → `expected: action:manage_portfolio`
     (CORRECTED). Anchor: the pre-existing, already-MATCH-scored row "what are my projects?"
     (`claim=get_project_status`, `expected=action:manage_portfolio`, `router=manage_portfolio@
     0.95`, `verdict=MATCH`) for the sibling `\bmy projects\b` literal, corroborated by **in-code**
     documentation (`pre_classifier.py` ~2515-2538, #1738/#1884) that names these exact two
     literals as documented PORTFOLIO collisions ("STATUS is the false-positive overlap").
     `manage_portfolio` is canonical-handler-dispatched (PORTFOLIO is in `canonical_categories`) —
     a real, live destination, unlike floor-routed `get_project_status`.
   - The remaining 38 rows (including the one reachable milestone survivor) keep `expected:
     action:get_project_status` uncorrected. The milestone case (`\bupcoming milestones?\b`) is
     DELIBERATE design per the Issue #898 Q25 comment ("Milestone queries are project status, not
     priority," line ~324) — not a bug. The other 37 (status/progress/tasks/assignments/work
     vocabulary) have no comparably direct in-corpus or in-code anchor pointing to a more specific
     destination; correcting them without evidence would be guessing (CLAUDE.md "never guess at
     facts you can look up").

7. Regenerated the corpus: `venv/bin/python scripts/build_inversion_corpus_phase0.py` — 336 → 382
   rows (+46). `git diff --stat` on the yaml + builder: 195 + 435 insertions, 0 deletions (purely
   additive, confirmed). Per-category denominators: STATUS 8 → 54.

8. Updated the pinned corpus total in `tests/unit/test_inversion_phase3_deletion_1595.py`:
   `test_claimed_plus_unclaimed_equals_corpus_size` 336 → 382 (claimed 186 → 232, unclaimed
   unchanged at 150 — confirmed by direct `gate.build_census(cats=None)` call, not inferred).
   Searched for other pinned `\b336\b` constants: `git grep -n "\b336\b" -- tests scripts` — only
   the one just-fixed hit (plus irrelevant unrelated matches in a PDF fixture and a line-336
   comment in an unrelated test-data file).

9. Re-ran the gate for STATUS_PATTERNS: 51/382 claimed (5 pre-existing + 46 new), **verdict stays
   NO-GO** (unchanged from before — 2 pre-existing FAIL rows, plus all 46 new rows read
   `[FAIL] UNSCORED; UNSCORED — score it (one router call); no verdict, no GO`, per the same
   2026-10-01 gate tightening GITHUB's lane found and documented — the "UNSCORED but expected
   action live via group" shortcut is gone cohort-wide, not specific to this list). NO-GO
   suppresses the "needs a corpus row" section (same precedent as every prior lane).

10. Ran both dry-run validations — no LLM calls (each script self-reports this):
    - `inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls" self-reported.
    - `inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made" self-reported.

11. `ruff format` + `ruff check --fix` on both touched `.py` files → clean, no changes needed;
    `ruff format --check` + `ruff check` both clean on re-run.

12. Tests (all run this turn, output quoted below):
    - `tests/unit/test_inversion_phase3_deletion_1595.py` — **35 passed**.
    - `tests/unit/services/intent_service/test_preclaim_shadow.py` — **29 passed**.
    - `tests/test_architecture_enforcement.py` — **63 passed, 1 xfailed**, clean.
    - Extraction ceiling re-confirmed **440** (unchanged) via direct
      `pattern_literal_counts.total_literal_count()` call — no `pre_classifier.py` literal
      edited/deleted in this unit.

13. Added a progress-log entry to `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

14. Verified scope compliance via `git status --porcelain` at session end: only
    `scripts/build_inversion_corpus_phase0.py`, `tests/fixtures/inversion_corpus_phase0.yaml`, and
    `tests/unit/test_inversion_phase3_deletion_1595.py` show as modified; no stray files from any
    concurrent lane (the GITHUB lane's own untracked artifacts were not present at the time of
    this check — that unit had already completed and presumably been handled). Git index not
    touched (nothing staged, per dispatcher instruction).

## Rows added — STATUS_PATTERNS (46 rows, all 46/46 of the reachable unexercised literals)

All actions verified directly via `pre_classify_with_pattern_list(phrase).action` and literal
identity via `_first_pattern_match`.

| phrase | literal exercised | expected (action) | reworded? |
|---|---|---|---|
| "time for my stand-up" | `\bstand-up\b` | show_standup (CORRECTED) | no |
| "give me my stand up" | `\bstand up\b` | show_standup (CORRECTED) | no |
| "give me a standup update" | `\bstandup update\b` | show_standup (CORRECTED) | no |
| "give me a standup report" | `\bstandup report\b` | show_standup (CORRECTED) | no |
| "what's my daily standup" | `\bdaily standup\b` | show_standup (CORRECTED) | no |
| "show today's standup" | `\bshow.*standup\b` | show_standup (CORRECTED) | yes (avoid `\bmy standup\b`) |
| "show me my portfolio" | `\bmy portfolio\b` | manage_portfolio (CORRECTED) | no |
| "list my active projects for this quarter" | `\blist.*projects\b` | manage_portfolio (CORRECTED) | yes (avoid PORTFOLIO_LIST_PATTERN) |
| "any upcoming milestones for this project" | `\bupcoming milestones?\b` | get_project_status (design-intent, #898 Q25) | no |
| "what's my current project" | `\bwhat'?s my current project\b` | get_project_status | no |
| "can you summarize my current work" | `\bcurrent work\b` | get_project_status | no |
| "what are my current projects" | `\bcurrent projects\b` | get_project_status | no |
| "give me a project overview" | `\bproject overview\b` | get_project_status | no |
| "what's the project landscape" | `\bproject landscape\b` | get_project_status | no |
| "what projects am I working on" | `\bprojects.*working on\b` | get_project_status | no |
| "tell me what I'm working on" | `\bwhat.*working on\b` | get_project_status | no |
| "quick check, working on now?" | `\bworking on now\b` | get_project_status | yes (avoid `\bwhat am i working on\b`) |
| "what are my active projects" | `\bactive projects\b` | get_project_status | no |
| "show my active work" | `\bactive work\b` | get_project_status | no |
| "what's my status" | `\bwhat'?s my status\b` | get_project_status | no |
| "give me a status update" | `\bstatus update\b` | get_project_status | no |
| "what is my status" | `\bmy status\b` | get_project_status | no |
| "what's my work status" | `\bwork status\b` | get_project_status | no |
| "show the current status" | `\bshow.*status\b` | get_project_status | yes (avoid `\bmy status\b`) |
| "what's the current status" | `\bcurrent status\b` | get_project_status | no |
| "I need a status report" | `\bstatus report\b` | get_project_status | no |
| "what's my progress" | `\bmy progress\b` | get_project_status | no |
| "give me a progress update" | `\bprogress update\b` | get_project_status | no |
| "I need a progress report" | `\bprogress report\b` | get_project_status | no |
| "what's the progress on this" | `\bprogress on\b` | get_project_status | no |
| "show today's progress" | `\bshow.*progress\b` | get_project_status | yes (avoid `\bmy progress\b`) |
| "what's the current progress" | `\bcurrent progress\b` | get_project_status | no |
| "how's the progress going" | `\bhow'?s.*progress\b` | get_project_status | yes (avoid `\bmy progress\b`) |
| "what's the progress looking like" | `\bwhat'?s.*progress\b` | get_project_status | yes (avoid `\bmy progress\b`) |
| "what are my tasks" | `\bmy tasks\b` | get_project_status | no |
| "show me my current tasks" | `\bcurrent tasks\b` | get_project_status | no |
| "what are my active tasks" | `\bactive tasks\b` | get_project_status | no |
| "show today's tasks" | `\bshow.*tasks\b` | get_project_status | yes (avoid `\bmy tasks\b`) |
| "list today's tasks" | `\blist.*tasks\b` | get_project_status | yes (avoid `\bmy tasks\b`) |
| "tasks I'm actively working on" | `\btasks.*working\b` | get_project_status | yes (avoid `\bwhat.*working on\b`) |
| "what tasks do I have" | `\bwhat tasks\b` | get_project_status | no |
| "what's the task status" | `\btask status\b` | get_project_status | no |
| "what are my assignments" | `\bmy assignments\b` | get_project_status | no |
| "show me my current assignments" | `\bcurrent assignments\b` | get_project_status | no |
| "what's assigned to me" | `\bwhat'?s assigned\b` | get_project_status | no |
| "show today's assignments" | `\bshow.*assignments\b` | get_project_status | yes (avoid `\bmy assignments\b`) |

46 rows total, 12 reworded (0 needed a second reword). All `category: STATUS`.

## Unreachable literals: 5 of 51

1. `\bnext milestone\b` — byte-identical to GITHUB_QUERY_PATTERNS' own `\bnext milestone\b`
   (checked earlier in the if-chain). Mathematically unreachable.
2. `\bwhat'?s the (?:next|upcoming) milestone\b` — byte-identical to
   `MILESTONE_STATUS_INLINE_PATTERNS` (checked even earlier). Mathematically unreachable.
3. `\bmilestone status\b` — same as #2.
4. `\bmilestone progress\b` — same as #2.
5. `\bmy current work\b` — shadowed within STATUS_PATTERNS by its own earlier, shorter sibling
   `\bcurrent work\b` (a guaranteed substring). Mathematically unreachable.

Unlike CALENDAR/TEMPORAL's phrasing-dependent shadows, #1-4 are cross-list, byte-identical
duplicates — provable unreachable by regex-identity argument, not just by trying phrasings (though
each was also empirically confirmed). For #1-3, the shadowing list's destination happens to be
behaviorally identical (STATUS/get_project_status either way), so the shadow is inert in practice
but the STATUS_PATTERNS literal is dead code. #1 (`\bnext milestone\b`) shadows into a DIFFERENT
destination (GITHUB's `review_issue_query`), which is NOT behaviorally inert — worth the Lead/Arch
knowing.

## Pre-existing [FAIL] rows — reported, not touched

Two rows already in the corpus before this deposit fail the gate's row-disposition check. Per the
dispatch's explicit instruction, their `expected` field was **not** changed:

1. `"what am I working on?"` → `claim=get_project_status`, `expected=category:STATUS`,
   `router=get_top_priority@0.85`. `MISMATCH (route=get_top_priority != expected category:STATUS)`.
   The router resolves this phrase to the PRIORITY category entirely, not STATUS — a genuine,
   pre-existing disagreement. I did NOT propagate this disagreement's implied correction
   (get_top_priority) to the sibling "working on" literals (`\bprojects.*working on\b`,
   `\bwhat.*working on\b`, `\bworking on now\b`) — a FAIL/MISMATCH row is a disagreement report,
   not a ruling, and the dispatch said to report FAIL rows separately, not to re-derive
   corrections from them.
2. `"show me my archived projects"` → `claim=get_project_status`, `expected=REVIEW`,
   `router=list_archived_projects@1.0`. `REVIEW-disagrees`. Pre-existing, same shape as GITHUB's
   "show milestones" finding (a broader STATUS literal losing to a more specific PORTFOLIO
   destination when "archived" is present).

## Findings — reported to the Lead, not fixed in this unit

### Finding 1 (significant): STATUS_PATTERNS' claim branch has NO case differentiation at all, and its one action (`get_project_status`) is floor-routed with no live destination

Unlike GITHUB_QUERY_PATTERNS' partial if/elif (7 distinct actions across its branches),
STATUS_PATTERNS' claim branch (`pre_classify_with_pattern_list` ~1807-1816) returns the single
hardcoded `action="get_project_status"` for literally every one of its 56 literals — the "no case
for this family" shape applies to the entire list, not a subset. Worse: `get_project_status` has
**no WorkflowEntry / flip_group anywhere** in `workflow_entries.py` (grep-confirmed, zero hits),
and STATUS is **not** a canonical-handler category either —
`services/intent_service/canonical_handlers.py`'s `can_handle()` docstring states explicitly:
"STATUS/PRIORITY removed Apr 13 (#925) — floor-routed via Action Gate," and its
`canonical_categories` set (TEMPORAL/GUIDANCE/PORTFOLIO/CONVERSATION/PROVENANCE) excludes STATUS.
**Every STATUS_PATTERNS claim is floor-routed in production, regardless of which literal fired.**
This raises a question the Lead/Arch will need to rule on before this list can be GO-eligible:
does the gate's live-match mechanism (keyed on registered `flip_group`s) have any path to [OK] for
a STATUS_PATTERNS row short of asserting `expected: floor` (the gate code already has a
`expected in ("floor", "plan")` special case at `row_disposition` line ~604, used by at least one
other list), or does MATCH/agreeing-REVIEW against the router's own classification remain the only
bar regardless of downstream dispatch? Not resolved here (a ruling, not a deposit).

### Finding 2: 2 corrections applied this time, grounded in direct in-corpus/in-code anchors — not a blanket "fix what looks wrong" pass

Per the dispatch's explicit instruction to apply GITHUB-style corrections preemptively where
"plainly wrong," I corrected 8 of 46 rows (6 standup + 2 portfolio/projects) where a DIRECT,
already-scored anchor row in this same corpus (not my own guess) already established the correct
destination for the identical literal family. I deliberately did NOT extend this to the other 37
rows (status/progress/tasks/assignments/work vocabulary) despite some of them plausibly also being
floor-routed-incorrectly, because no comparable anchor exists for them — correcting without
evidence would be guessing. This is a narrower correction scope than GITHUB's eventual 21-row
correction (which came from a POST-DEPOSIT Haiku-scoring pass, not the depositing agent's own
judgment) — the Lead's scoring pass may still find more corrections are warranted once it has real
router data for these 38 rows.

## Gate output — before

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 336 rows total = 186 claimed + 150 unclaimed

## STATUS_PATTERNS
literals: 56  |  rows claimed: 5/336
verdict: NO-GO

rows claimed:
  [OK] "give me my standup" -> claim=get_project_status expected=action:show_standup router=show_standup@0.95 verdict=MATCH :: MATCH
  [FAIL] "what am I working on?" -> claim=get_project_status expected=category:STATUS router=get_top_priority@0.85 verdict=MISMATCH :: MISMATCH (route=get_top_priority != expected category:STATUS); the pattern is the live path for this phrase — not-live (no WorkflowEntry — the live consult dispatches rail keys only)
  [OK] "give me a project status report" -> claim=get_project_status expected=action:update_issue router=generate_report@0.92 verdict=MISMATCH :: MISMATCH but the router's own route live via group — the consult owns this phrase
  [FAIL] "show me my archived projects" -> claim=get_project_status expected=REVIEW router=list_archived_projects@1.0 verdict=REVIEW :: REVIEW-disagrees (route=list_archived_projects != claim=get_project_status); expected-not-action-shaped
  [OK] "what are my projects?" -> claim=get_project_status expected=action:manage_portfolio router=manage_portfolio@0.95 verdict=MATCH :: MATCH
```
(NO-GO suppresses the "needs a corpus row" section — same precedent prior lanes established.)

## Gate output — after

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 382 rows total = 232 claimed + 150 unclaimed

## STATUS_PATTERNS
literals: 56  |  rows claimed: 51/382
verdict: NO-GO

rows claimed:
  [OK] "give me my standup" -> claim=get_project_status expected=action:show_standup router=show_standup@0.95 verdict=MATCH :: MATCH
  [FAIL] "what am I working on?" -> claim=get_project_status expected=category:STATUS router=get_top_priority@0.85 verdict=MISMATCH :: MISMATCH (route=get_top_priority != expected category:STATUS); the pattern is the live path for this phrase — not-live (no WorkflowEntry — the live consult dispatches rail keys only)
  [OK] "give me a project status report" -> claim=get_project_status expected=action:update_issue router=generate_report@0.92 verdict=MISMATCH :: MISMATCH but the router's own route live via group — the consult owns this phrase
  [FAIL] "show me my archived projects" -> claim=get_project_status expected=REVIEW router=list_archived_projects@1.0 verdict=REVIEW :: REVIEW-disagrees (route=list_archived_projects != claim=get_project_status); expected-not-action-shaped
  [OK] "what are my projects?" -> claim=get_project_status expected=action:manage_portfolio router=manage_portfolio@0.95 verdict=MATCH :: MATCH
  [FAIL] "time for my stand-up" -> claim=get_project_status expected=action:show_standup router=None@None verdict=UNSCORED :: UNSCORED; UNSCORED — score it (one router call); no verdict, no GO
  [... 45 more [FAIL]/UNSCORED lines, one per new deposit row — all correctly UNSCORED, "no
       verdict, no GO" (Finding 2 from GITHUB's lane — the same gate tightening applies uniformly
       here, not a gap in this unit's deposit coverage) ...]
```
(No "needs a corpus row" section printed either before or after — NO-GO suppresses it.)

## New corpus total

336 → **382** rows (+46). Per-category denominators after rebuild: QUERY 130, TEMPORAL 69,
**STATUS 54** (was 8, +46), PRIORITY 41, GUIDANCE 26, EXECUTION 26, PORTFOLIO 16, CONVERSATION 5,
SYNTHESIS 4, IDENTITY 3, MEMORY 3, DISCOVERY 2, PROVENANCE 1, TRUST 1, ANALYSIS 1.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 382 rows (59 REVIEW), exit 0.
- `git diff --stat tests/fixtures/inversion_corpus_phase0.yaml scripts/build_inversion_corpus_phase0.py`
  → `2 files changed, 630 insertions(+)`, zero deletions.
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls"
  self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made"
  self-reported.
- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list STATUS_PATTERNS --live
  read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal`
  → exit 0, 51/382 claimed, verdict NO-GO (2 pre-existing FAIL rows plus 46 new UNSCORED rows), 0
  "needs a corpus row" lines (NO-GO suppresses the section).
- `venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q` → **35
  passed**, exit 0.
- `venv/bin/python -m pytest tests/unit/services/intent_service/test_preclaim_shadow.py -q` →
  **29 passed**, exit 0.
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q` → **63 passed, 1
  xfailed**, exit 0, clean.
- `venv/bin/python -c "import sys; sys.path.insert(0,'scripts'); import pattern_literal_counts
  as plc; print(plc.total_literal_count())"` → **440**, unchanged (ceiling untouched — no
  pre_classifier literal edited/deleted; task's "ceiling exactly 440" condition met).
- `venv/bin/ruff format` + `ruff check --fix` on both touched `.py` files → clean, no changes
  needed; `ruff format --check` + `ruff check` both clean on re-run.

## Files touched

- `scripts/build_inversion_corpus_phase0.py` (HAND_ROWS: +46 rows in a `# — STATUS_PATTERNS`
  delimited block, extending the existing `# phase3-conversion` section, after the
  GITHUB_QUERY_PATTERNS block)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, purely additive, 336→382 rows)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (one pinned constant corrected 336→382,
  with updated docstring)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (progress-log entry added)
- This session log (new)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read only),
`services/intent_service/workflow_entries.py` (read only), `services/intent_service/
canonical_handlers.py` (read only), `web/` (not touched, not relevant to this unit), any flag/env
var, `scripts/inversion_phase3_deleted_patterns.json` (no deletion performed).

## Verified how

- **Method**: computed the exact unexercised-literal set by importing and calling the gate's own
  `unexercised_literals()` against `build_census()`'s claimed rows (not hand-counted or
  re-derived). For each of the 46 deposited literals, called the REAL production functions
  directly — `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name assertion AND
  `intent.action` read directly) and `PreClassifier._first_pattern_match(cleaned,
  PreClassifier.STATUS_PATTERNS)` (literal-identity assertion) — in a single comprehensive script
  run covering all 46 rows together as a final check (0 failures, 0 duplicate phrases, 46/46
  unique literals covered), after an iterative reword pass. For the 5 unreachable literals,
  verified the cross-list shadowing claim by (a) reading the shadowing list's definition and its
  position in the if-chain directly, (b) confirming via `grep` that no other occurrence of the
  milestone literals exists elsewhere in the file, and (c) empirically confirming the shadow with
  real phrases for all 5 (not relying on the regex-identity argument alone, though that argument
  is independently sufficient). Gate re-runs, pytest, and ruff invocations were all run this turn
  via Bash and their output is quoted/counted above, not recalled from memory. `git diff --stat`
  run and quoted directly to confirm purely-additive changes. `git status --porcelain` run at
  session end to confirm scope compliance.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by design of this unit —
  the Phase-1 router/LLM layer is deliberately UNSCORED here (no LLM calls made anywhere in this
  session, confirmed by each script's own self-report and the absence of any LLM-client invocation
  in the commands run). The floor-routing finding (Finding 1) was verified by reading
  `canonical_handlers.py` and `workflow_entries.py` directly, not inferred from behavior.
- **Denominator**: 1 target list (STATUS_PATTERNS) — 46 of 51 previously-flagged unexercised
  literals now have a corpus row; 5 of 51 confirmed structurally unreachable (proven, not just
  empirically probed, for 4 of the 5). Test denominator: 35/35 in the target Phase-3 test file
  pass, 29/29 in the pre-claim shadow test file pass, 63/63 (plus 1 pre-existing xfail) in the
  full architecture-enforcement suite (full file run, not a subset). Ceiling denominator: 440/440
  unchanged, confirmed by direct call. `git status` run at session end to confirm scope compliance
  (3 tracked files touched by me, matching the dispatch's allowed scope; pre-existing untracked
  files from the Lead's own session left alone).

## Memory & briefing surfaces referenced this session

- **Referenced**: `dev/2026/10/01/2026-10-01-1254-prog-code-log-1595-phase3-deposits-github.md`
  (method, row-shape convention, the explicit instruction to check for and correct "no case for
  this family" shapes — directly informed Finding 1 and the correction-scope decision);
  `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 — deletion gate" (read
  for the deletability mechanism and the UNSCORED tightening context); `dev/2026/09/25/
  inversion-epic0-remaining-scope-2026-09-25.md` (procedure + progress log, appended to).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections
  (bounded prog dispatch inside an existing worktree — no mailbox write, no sign-off merge, per
  dispatcher scope — I did not touch the git index at all); the CALENDAR/TEMPORAL/PRIORITY/
  GUIDANCE deposit-lane logs (not re-read in full — the GITHUB log's own summary of their shadow
  methodology was sufficient, since this unit found its own distinct cross-list shadow shape that
  needed first-principles investigation of `MILESTONE_STATUS_INLINE_PATTERNS` and
  `PORTFOLIO_PATTERNS` specifically).
- **Wanted but not found**: none — the dispatch prompt's cited sources were sufficient, though the
  STATUS/PRIORITY floor-routing fact (Finding 1, `canonical_handlers.py`'s "#925" docstring) had to
  be discovered by reading `canonical_handlers.py` directly when `get_project_status` turned up
  with no `workflow_entries.py` registration at all — not mentioned in the dispatch or the prior
  GITHUB log.

## Discovered work

None filed as separate GitHub issues (matching the PRIORITY/CALENDAR/TEMPORAL/GUIDANCE/GITHUB
lanes' established convention of reporting inline rather than filing). Two findings reported
inline above:
1. **Finding 1** (significant): STATUS_PATTERNS' claim branch has zero per-literal
   differentiation (all 56 literals → `get_project_status`), and that action is floor-routed with
   no live rail or canonical-handler destination anywhere — a real gap the Lead/Arch needs to rule
   on (does `expected: floor` ever read [OK] under the live-match gate, or is MATCH/
   agreeing-REVIEW the only bar) before this list can be GO-eligible.
2. **Finding 2**: 2 corrections (8 rows) were applied this deposit, narrower in scope than
   GITHUB's eventual 21-row correction — grounded only in literals with a direct, already-scored
   in-corpus anchor, not extended speculatively to the rest of the list. The Lead's Haiku-scoring
   pass may surface more warranted corrections once real router data exists for the other 38 rows.
