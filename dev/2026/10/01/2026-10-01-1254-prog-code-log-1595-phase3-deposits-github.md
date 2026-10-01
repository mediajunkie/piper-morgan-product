# 2026-10-01 1254 — prog (Coding Agent) — #1595 Phase 3 GITHUB_QUERY_PATTERNS deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for `GITHUB_QUERY_PATTERNS` only (64 literals).
Touched only the corpus builder, the fixture yaml, the ledger pin test's corpus-size constant,
and the scope doc. NO LLM calls made. No pattern deleted. No flag/env changed. Did not touch git
index (dispatcher instruction — no staging/commit performed). Did not touch
`services/intent_service/todo_handlers.py` or `web/` — confirmed at session end via `git status`
that `todo_handlers.py` (modified) and `tests/unit/services/intent_service/
test_todo_completion_clause_split_1914.py` (untracked) belong to a concurrent lane in this shared
worktree, neither touched by me.

## Read first (per dispatch prompt)

- `dev/2026/09/30/2026-09-30-2150-prog-code-log-1595-phase3-deposits-calendar.md` — method: call
  the REAL production matcher directly; row-shape convention; verify the ACTION empirically per
  row (the claiming literal and the action-selecting literal can differ — CALENDAR's "agenda...
  week" finding).
- `dev/2026/09/30/2026-09-30-2155-prog-code-log-1595-phase3-deposits-temporal.md` — the
  shadowed-by-another-LIST shape (not just an earlier sibling in the SAME list).
- `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 — deletion gate" and the
  "scored on BOTH tables" rule (2026-09-29) — not directly exercised by this unit (no router/
  prompt/catalog change made), read for context on how `RouterReports`/`PHASE3_REPORTS` work.
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` — the epic's own progress log;
  confirmed the 4th deletion (`TEMPORAL_PATTERNS`) landed the same morning and introduced a
  same-day tightening to the gate's UNSCORED-row rule (see Finding 2 below).
- `services/intent_service/pre_classifier.py` — `GITHUB_QUERY_PATTERNS` (64 literals, lines
  396-475), its claim branch in `pre_classify_with_pattern_list` (~line 1532, checked AFTER
  `LOCAL_GIT_STATUS_PATTERNS` and `MILESTONE_STATUS_INLINE_PATTERNS` — confirmed by reading the
  surrounding if-chain) and its action-determination if/elif (lines ~1534-1620), and the
  `_github_read_claim_blocked` decline-guard (#1794) — confirmed none of the 53 deposited phrases
  trip it (all resolved to `GITHUB_QUERY_PATTERNS` cleanly, no silent fall-through).
- `services/intent_service/workflow_entries.py` (READ ONLY — not edited) —
  `_READ_QUERY_FLIP_GROUPS` (line 1249): `shipped_query`/`stale_prs_query`/`list_issues_query`/
  `list_prs_query` → `read_status`; `review_issue_query` → `read_referent`; both live under the
  dispatch's `--live` set. `close_issue_query`/`reopen_issue_query`/`comment_issue_query` carry
  neither a `flip_group` nor a `flip_write_allowlist_key` (grep-confirmed) — not live under any
  `--live` token today, a pre-existing gap this unit did not create.

## What I did

1. Ran the gate exactly as specified and quoted it (below). Confirmed 64 literals, 13/283 rows
   claimed, verdict NO-GO (2 pre-existing `[FAIL]` rows: "show issue #123" and "show milestones",
   both REVIEW-disagreements between the pre-classifier's claim and the router's actual route —
   left untouched; correcting an existing row's `expected` is a ruling, not a deposit, per the
   dispatch's explicit instruction).

2. Computed the exact unexercised-literal set using the gate's own `unexercised_literals()`
   function (imported, not reimplemented) against `build_census()`'s claimed rows for
   `GITHUB_QUERY_PATTERNS`: **53 unexercised** (64 total − 11 unique literals already exercised by
   the 13 pre-existing claimed rows, including the 2 FAIL rows, which still exercise a literal).
   This differs from a naive `64 − 13 = 51`; the gate's own function is authoritative, used
   directly, not hand-counted.

3. Derived one natural PM-style phrase per unexercised literal and verified each empirically
   against the REAL production matcher in a Python script:
   - `PreClassifier.pre_classify_with_pattern_list(phrase)` → asserted returned list name ==
     `"GITHUB_QUERY_PATTERNS"`, and `intent.action` read directly (not hand-derived from the
     if/elif — see Finding 1 below for why that matters).
   - `PreClassifier._first_pattern_match(cleaned, PreClassifier.GITHUB_QUERY_PATTERNS)` →
     asserted `.re.pattern` equals the specific cited literal (proves the claim isn't stolen by an
     earlier sibling literal in the same list).

   First pass: 48/53 clean. 5 failed and were reworded (all fixed on the single retry — **0
   literals needed a second reword, and 0 were structurally unreachable**, a first for this
   deposit lane; every prior lane found 3-6 permanently-shadowed literals):
   - "show me what shipped" → claimed by the earlier, shorter sibling `\bwhat shipped\b` instead
     of `\bshow.*what.*shipped\b`. Reworded "can you show what has shipped" (breaks the "what
     shipped" adjacency the shorter literal requires).
   - "what shipped this week" → same shadow, same fix shape: "what has shipped this past week".
   - "what's the next milestone" → claimed by a **different, earlier-checked list**,
     `MILESTONE_STATUS_INLINE_PATTERNS` (STATUS category, action=`get_project_status`, per the
     #1068 ordering comment at line ~1496), not `GITHUB_QUERY_PATTERNS` at all. Reworded "any
     update on the next milestone" (no "what's the" prefix).
   - "what prs are assigned to me" / "which pull requests are assigned to me" → matched **no
     literal at all** — `\bprs assigned to me\b` / `\bpull requests assigned to me\b` require that
     exact word-adjacency; my first attempt inserted "are", breaking it. Reworded "any prs
     assigned to me" / "any pull requests assigned to me".

4. Deposited a `# — GITHUB_QUERY_PATTERNS` delimited block (extending the existing `#
   phase3-conversion` HAND_ROWS section, after the TEMPORAL block) in
   `scripts/build_inversion_corpus_phase0.py`: 53 rows. `category` follows the pre-existing
   convention observed directly in the yaml fixture (`close issue 42`/`close issue #123`/`reopen
   issue #123`/`comment on issue #123` all use `category: EXECUTION`, not `QUERY`) — so
   `close_issue_query` (2 rows), `reopen_issue_query` (3), `comment_issue_query` (3) = 8 rows
   category `EXECUTION`; the remaining 45 rows (shipped/stale/list_issues/list_prs/review_issue)
   are category `QUERY`. `expected: action:<name>` per row, each `source` citing
   `phase3-conversion/GITHUB_QUERY_PATTERNS literal r"<the literal>"`.

5. Regenerated the corpus: `venv/bin/python scripts/build_inversion_corpus_phase0.py` — 283 → 336
   rows (+53). `git diff --stat` on the yaml + builder: 212 + 394 insertions, 0 deletions (purely
   additive, confirmed).

6. Updated the pinned corpus total in `tests/unit/test_inversion_phase3_deletion_1595.py`:
   `test_claimed_plus_unclaimed_equals_corpus_size` 283 → 336 (claimed 133 → 186, unclaimed
   unchanged at 150 — confirmed by direct `gate.build_census(cats=None)` call, not inferred; note
   `unclaimed` is 150, not the 51 cited in the PRIORITY/CALENDAR/TEMPORAL-era docstrings — the
   same-day `CALENDAR_QUERY_PATTERNS`/`TEMPORAL_PATTERNS` deletions emptied those two lists to
   `[]`, so every row that used to claim via them now reads unclaimed; this is a real, expected
   consequence of the 3rd/4th deletions landing earlier the same day, not a defect in this unit).
   Searched for other pinned `\b283\b` constants: `git grep -n "\b283\b" -- tests scripts` — only
   the one just-fixed hit plus an unrelated report-filename comment in the gate script and
   unrelated binary/fixture/line-283 matches (irrelevant).

7. Re-ran the gate for GITHUB_QUERY_PATTERNS: 66/336 claimed (13 pre-existing + 53 new), **verdict
   stays NO-GO** (was already NO-GO before this deposit, from the 2 pre-existing FAIL rows).
   **Mechanism finding, not a defect of this deposit** (Finding 2 below): every new row reads
   `[FAIL] UNSCORED; UNSCORED — score it (one router call); no verdict, no GO` — the
   "UNSCORED-but-expected-action-live-via-group" shortcut that let CALENDAR's deposits read `[OK]`
   was **removed from `row_disposition()` the same day** (2026-10-01, same commit cluster as the
   4th deletion): the function's UNSCORED branch now hardcodes `live_ok = False` unconditionally,
   with the comment "an unscored row is a row we know nothing about... Never OK." This makes
   UNSCORED uniformly NO-GO-contributing across every Phase-3 list now, not something specific to
   GITHUB_QUERY_PATTERNS. NO-GO suppresses the "needs a corpus row" section (same precedent
   PRIORITY/TEMPORAL established) — confirmed no such section printed.

8. Ran both dry-run validations — no LLM calls (each script self-reports this):
   - `inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls" self-reported.
   - `inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made" self-reported; reports `phase0
     corpus: 336 rows (untouched)`.

9. `ruff format` + `ruff check --fix` on both touched `.py` files → clean, no changes needed;
   `ruff format --check` + `ruff check` both clean on re-run.

10. Tests (all run this turn, output quoted below):
    - `tests/unit/test_inversion_phase3_deletion_1595.py` — **35 passed** (grown from 19 since the
      4th deletion added synthetic pins for its new `row_disposition` branches).
    - `tests/unit/services/intent_service/test_preclaim_shadow.py` — **29 passed**.
    - `tests/test_architecture_enforcement.py` — **63 passed, 1 xfailed**, clean.
    - Extraction ceiling re-confirmed **440** (unchanged) via direct
      `pattern_literal_counts.total_literal_count()` call — no `pre_classifier.py` literal
      edited/deleted in this unit.

11. Added a progress-log entry to `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

## Rows added — GITHUB_QUERY_PATTERNS (53 rows, all 53/53 of the unexercised literals)

All actions verified directly via `intent.action` from the real production function.

| phrase | literal exercised | action | flip group | category | reworded? |
|---|---|---|---|---|---|
| "what shipped recently" | `\bwhat shipped\b` | shipped_query | read_status | QUERY | no |
| "can you show what has shipped" | `\bshow.*what.*shipped\b` | shipped_query | read_status | QUERY | yes (avoid `\bwhat shipped\b`) |
| "what has shipped this past week" | `\bwhat.*shipped.*week\b` | shipped_query | read_status | QUERY | yes (avoid `\bwhat shipped\b`) |
| "show our stale pull requests" | `\bstale pull requests\b` | stale_prs_query | read_status | QUERY | no |
| "any old prs lying around" | `\bold prs\b` | stale_prs_query | read_status | QUERY | no |
| "prs needing review" | `\bprs.*needing review\b` | stale_prs_query | read_status | QUERY | no |
| "close the completed issue" | `\bclose.*completed.*issue\b` | close_issue_query | (none — rail action) | EXECUTION | no |
| "please close this issue" | `\bclose.*issue\b` | close_issue_query | (none — rail action) | EXECUTION | no |
| "re-open issue 88" | `\bre-open\s+issue\s*#?\d+\b` | reopen_issue_query | (none — rail action) | EXECUTION | no |
| "reopen the old issue" | `\breopen\s+.*issue\b` | reopen_issue_query | (none — rail action) | EXECUTION | no |
| "re-open the old issue" | `\bre-open\s+.*issue\b` | reopen_issue_query | (none — rail action) | EXECUTION | no |
| "add comment to issue 99" | `\badd comment to issue\s*#?\d+\b` | comment_issue_query | (none — rail action) | EXECUTION | no |
| "reply to issue 99" | `\breply to issue\s*#?\d+\b` | comment_issue_query | (none — rail action) | EXECUTION | no |
| "comment on 99" | `\bcomment\s+on\s+#?\d+\b` | comment_issue_query | (none — rail action) | EXECUTION | no |
| "review issue 101" | `\breview issue\s*#?\d+\b` | review_issue_query | read_referent | QUERY | no |
| "issue 101 details" | `\bissue\s*#?\d+\s*details\b` | review_issue_query | read_referent | QUERY | no |
| "get issue 101" | `\bget issue\s*#?\d+\b` | review_issue_query | read_referent | QUERY | no |
| "what are my issues" | `\bmy issues\b` | list_issues_query | read_status | QUERY | no |
| "list the issues please" | `\blist.*issues\b` | list_issues_query | read_status | QUERY | no |
| "show the issues" | `\bshow.*issues\b` | list_issues_query | read_status | QUERY | no |
| "what's the issue count" | `\bissue count\b` | list_issues_query | read_status | QUERY | no |
| "which issues are assigned to engineering" | `\bissues.*assigned\b` | list_issues_query | read_status | QUERY | no |
| "show my pull requests" | `\bshow my pull requests\b` | list_prs_query | read_status | QUERY | no |
| "what are my prs looking like" | `\bmy prs\b` | list_prs_query | read_status | QUERY | no |
| "where are my pull requests" | `\bmy pull requests\b` | list_prs_query | read_status | QUERY | no |
| "list the prs" | `\blist.*prs\b` | list_prs_query | read_status | QUERY | no |
| "list all pull requests from this sprint" | `\blist.*pull requests\b` | list_prs_query | read_status | QUERY | no |
| "any open prs waiting on me" | `\bopen prs\b` | list_prs_query | read_status | QUERY | no |
| "any prs assigned to me" | `\bprs assigned to me\b` | list_prs_query | read_status | QUERY | yes (phrasing matched no literal) |
| "any pull requests assigned to me" | `\bpull requests assigned to me\b` | list_prs_query | read_status | QUERY | yes (phrasing matched no literal) |
| "list the milestones for this quarter" | `\blist.*milestones?\b` | review_issue_query | read_referent | QUERY | no |
| "any update on the next milestone" | `\bnext milestone\b` | review_issue_query | read_referent | QUERY | yes (avoid MILESTONE_STATUS_INLINE_PATTERNS) |
| "what milestones do we have" | `\bwhat milestones?\b` | review_issue_query | read_referent | QUERY | no |
| "milestones due this month" | `\bmilestones?\s+(?:status\|count\|list\|due)\b` | review_issue_query | read_referent | QUERY | no |
| "when's the milestone deadline" | `\bwhen.*milestone\b` | review_issue_query | read_referent | QUERY | no |
| "any recent releases" | `\brecent releases?\b` | review_issue_query | read_referent | QUERY | no |
| "show me the releases" | `\bshow.*releases?\b` | review_issue_query | read_referent | QUERY | no |
| "list our releases" | `\blist.*releases?\b` | review_issue_query | read_referent | QUERY | no |
| "what version are we on" | `\bwhat version (?:are we on\|is current)\b` | review_issue_query | read_referent | QUERY | no |
| "what's the current release" | `\bcurrent (?:release\|version)\b` | review_issue_query | read_referent | QUERY | no |
| "what's our latest release" | `\blatest release\b` | review_issue_query | read_referent | QUERY | no |
| "what labels do we use" | `\bwhat labels?\b` | review_issue_query | read_referent | QUERY | no |
| "show me the labels" | `\bshow.*labels?\b` | review_issue_query | read_referent | QUERY | no |
| "list the labels" | `\blist.*labels?\b` | review_issue_query | read_referent | QUERY | no |
| "what are the issue labels" | `\bissue labels?\b` | review_issue_query | read_referent | QUERY | no |
| "labels count please" | `\blabels?\s+(?:list\|count)\b` | review_issue_query | read_referent | QUERY | no |
| "all labels please" | `\b(?:available\|all)\s+labels?\b` | review_issue_query | read_referent | QUERY | no |
| "show me the active branches" | `\bactive branches?\b` | review_issue_query | read_referent | QUERY | no |
| "show which branches exist" | `\bshow.*branches?\b` | review_issue_query | read_referent | QUERY | no |
| "list the branches" | `\blist.*branches?\b` | review_issue_query | read_referent | QUERY | no |
| "what feature branches do we have" | `\bfeature branches?\b` | review_issue_query | read_referent | QUERY | no |
| "what are the current branches" | `\bcurrent branches?\b` | review_issue_query | read_referent | QUERY | no |
| "what branches do we have" | `\bwhat branches?\b` | review_issue_query | read_referent | QUERY | no |

53 rows total. 45 QUERY-category rows live-routable (flip group `read_status`/`read_referent`, both
in the `--live` set). 8 EXECUTION-category rows (close/reopen/comment) carry no flip group and are
NOT live under any `--live` token today (a pre-existing gap in the inversion's write-rail coverage,
not created by this deposit — these three actions have never had a `flip_write_allowlist_key`
assigned).

## Unreachable literals: NONE

Unlike every prior deposit lane (CALENDAR 3, TEMPORAL 6, PRIORITY 5), **0 of the 53 unexercised
GITHUB_QUERY_PATTERNS literals were structurally unreachable**. All 53 got a clean row; the 5 that
initially mismatched were fixed with a single reword each (no literal needed a second attempt, and
none were abandoned as permanently shadowed).

## Pre-existing [FAIL] rows — reported, not touched

Two rows already in the corpus before this deposit fail the gate's row-disposition check. Per the
dispatch's explicit instruction, their `expected` field was **not** changed (that is a ruling, not
a deposit):

1. `"show issue #123"` → `claim=review_issue_query`, `expected=REVIEW`, `router=list_issues@0.9`.
   `REVIEW-disagrees (route=list_issues != claim=review_issue_query)`. The router (grammar/LLM
   layer) resolves this phrase to `list_issues`, while the pre-classifier's surface-1 claim is
   `review_issue_query` — a genuine disagreement between the two layers for an ambiguous phrase
   ("show issue #123" could plausibly mean "show me THAT issue" or "show me issues, filtered to
   #123" — the router picked the latter).
2. `"show milestones"` → `claim=review_issue_query`, `expected=REVIEW`, `router=list_milestones@1.0`.
   `REVIEW-disagrees (route=list_milestones != claim=review_issue_query)`. This is the SAME
   disagreement shape Finding 1 below documents at scale: the pre-classifier's action-determination
   logic has no milestone-specific branch, so it falls through to `review_issue_query`, while the
   router correctly resolves "show milestones" to `list_milestones` (a destination that, per
   `workflow_entries.py`, is a fully-registered, flip-grouped action the pre-classifier's own
   if/elif chain simply never reaches).

## Findings — reported to the Lead, not fixed in this unit

### Finding 1 (significant): milestones/releases/labels/branches literals all claim action=review_issue_query, not their own registered actions

23 of the 53 deposited rows (every literal from `\blist.*milestones?\b` through `\bwhat
branches?\b` — the full milestone/release/label/branch subgroups) claim via
`GITHUB_QUERY_PATTERNS` correctly, but their **action** comes out `review_issue_query` — literally
the same action as "show me issue #42" — because `pre_classify_with_pattern_list`'s
action-determination if/elif (`services/intent_service/pre_classifier.py` ~1532-1620) only has
branches for `shipped_query`/`stale_prs_query`/`close_issue_query`/`reopen_issue_query`/
`comment_issue_query`/`list_issues_query`/`list_prs_query`; everything else — including every
milestone/release/label/branch literal — falls into the trailing `else: action =
review_issue_query`.

This is despite `list_milestones_query`, `list_releases_query`, `list_labels_query`, and
`list_branches_query` being **fully registered WORKFLOW actions** with their own handlers
(`_handle_list_milestones_query` etc.) and `read_status` flip groups in
`services/intent_service/workflow_entries.py` (lines ~1216-1219, ~1256-1261, confirmed by direct
read, not inferred). Those four handlers are structurally unreachable from this particular
pre-classifier branch — confirmed empirically for all 23 literals (every one of the 23 candidate
phrases returned `action=review_issue_query` directly from `pre_classify_with_pattern_list`, not
assumed from reading the code). The pre-existing "show milestones" FAIL row (above) already showed
this exact disagreement at one data point; this deposit demonstrates the disagreement's full
scope across all four sub-categories. Not corrected here — this is a ruling (whether the
pre-classifier's action-determination chain should gain four more branches, or whether these
literals/handlers should be reconciled some other way), not something a corpus deposit decides.
Flagged for the Lead / Arch.

### Finding 2: the gate's UNSCORED-row rule was tightened the same day, changing what "[OK]" means for every Phase-3 deposit

The CALENDAR_QUERY_PATTERNS deposit lane (2026-09-30) observed new UNSCORED rows marking `[OK]`
via a shortcut: "UNSCORED but expected action live via group." That shortcut is **gone** as of a
same-day (2026-10-01) change to `row_disposition()` in `scripts/inversion_phase3_deletion_gate.py`
— its UNSCORED branch now unconditionally sets `live_ok = False`, with the comment "an unscored
row is a row we know nothing about... Never OK." This means all 53 of this unit's new rows read
`[FAIL] UNSCORED; UNSCORED — score it (one router call); no verdict, no GO`, even though 45 of
them have a live flip group. This is NOT specific to GITHUB_QUERY_PATTERNS and is not a defect in
this deposit — it is a cohort-wide tightening that makes every future Phase-3 deposit lane's
freshly-deposited rows read `[FAIL]` until the Lead's budgeted shadow-score run actually scores
them, full stop, regardless of flip-group liveness. Worth the Lead/next deposit-lane agent knowing
this changed, since it changes what a "clean" post-deposit gate run looks like going forward
(permanently NO-GO-by-default until scored, not "GO for live-grouped rows").

## Gate output — before

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 283 rows total = 133 claimed + 150 unclaimed

## GITHUB_QUERY_PATTERNS
literals: 64  |  rows claimed: 13/283
verdict: NO-GO

rows claimed:
  [OK] "show my open issues" -> claim=list_issues_query expected=action:list_issues_query router=list_issues@0.95 verdict=MATCH :: MATCH
  [OK] "show my open pull requests" -> claim=list_prs_query expected=action:list_prs_query router=list_prs@0.95 verdict=MATCH :: MATCH
  [OK] "close issue 42" -> claim=close_issue_query expected=action:close_issue_query router=close_issue@0.95 verdict=MATCH :: MATCH
  [OK] "comment on issue 42: looks good" -> claim=comment_issue_query expected=action:comment_issue_query router=comment_issue@0.95 verdict=MATCH :: MATCH
  [OK] "what did we ship this week?" -> claim=shipped_query expected=REVIEW router=shipped_this_week@1.0 verdict=REVIEW :: REVIEW-agrees (route=shipped_this_week == claim=shipped_query)
  [OK] "show stale prs" -> claim=stale_prs_query expected=REVIEW router=stale_prs@1.0 verdict=REVIEW :: REVIEW-agrees (route=stale_prs == claim=stale_prs_query)
  [OK] "close issue #123" -> claim=close_issue_query expected=REVIEW router=close_issue@1.0 verdict=REVIEW :: REVIEW-agrees (route=close_issue == claim=close_issue_query)
  [OK] "reopen issue #123" -> claim=reopen_issue_query expected=REVIEW router=reopen_issue@1.0 verdict=REVIEW :: REVIEW-agrees (route=reopen_issue == claim=reopen_issue_query)
  [OK] "comment on issue #123" -> claim=comment_issue_query expected=REVIEW router=comment_issue@1.0 verdict=REVIEW :: REVIEW-agrees (route=comment_issue == claim=comment_issue_query)
  [OK] "how many open issues do we have?" -> claim=list_issues_query expected=REVIEW router=list_issues@0.9 verdict=REVIEW :: REVIEW-agrees (route=list_issues == claim=list_issues_query)
  [OK] "show my prs" -> claim=list_prs_query expected=REVIEW router=list_prs@0.9 verdict=REVIEW :: REVIEW-agrees (route=list_prs == claim=list_prs_query)
  [FAIL] "show issue #123" -> claim=review_issue_query expected=REVIEW router=list_issues@0.9 verdict=REVIEW :: REVIEW-disagrees (route=list_issues != claim=review_issue_query); expected-not-action-shaped
  [FAIL] "show milestones" -> claim=review_issue_query expected=REVIEW router=list_milestones@1.0 verdict=REVIEW :: REVIEW-disagrees (route=list_milestones != claim=review_issue_query); expected-not-action-shaped
```
(NO-GO suppresses the "needs a corpus row" section — same precedent prior lanes established; not
re-pasted since it was absent both before and after.)

## Gate output — after

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 336 rows total = 186 claimed + 150 unclaimed

## GITHUB_QUERY_PATTERNS
literals: 64  |  rows claimed: 66/336
verdict: NO-GO

rows claimed:
  [OK] "show my open issues" -> claim=list_issues_query expected=action:list_issues_query router=list_issues@0.95 verdict=MATCH :: MATCH
  [OK] "show my open pull requests" -> claim=list_prs_query expected=action:list_prs_query router=list_prs@0.95 verdict=MATCH :: MATCH
  [OK] "close issue 42" -> claim=close_issue_query expected=action:close_issue_query router=close_issue@0.95 verdict=MATCH :: MATCH
  [OK] "comment on issue 42: looks good" -> claim=comment_issue_query expected=action:comment_issue_query router=comment_issue@0.95 verdict=MATCH :: MATCH
  [OK] "what did we ship this week?" -> claim=shipped_query expected=REVIEW router=shipped_this_week@1.0 verdict=REVIEW :: REVIEW-agrees (route=shipped_this_week == claim=shipped_query)
  [OK] "show stale prs" -> claim=stale_prs_query expected=REVIEW router=stale_prs@1.0 verdict=REVIEW :: REVIEW-agrees (route=stale_prs == claim=stale_prs_query)
  [OK] "close issue #123" -> claim=close_issue_query expected=REVIEW router=close_issue@1.0 verdict=REVIEW :: REVIEW-agrees (route=close_issue == claim=close_issue_query)
  [OK] "reopen issue #123" -> claim=reopen_issue_query expected=REVIEW router=reopen_issue@1.0 verdict=REVIEW :: REVIEW-agrees (route=reopen_issue == claim=reopen_issue_query)
  [OK] "comment on issue #123" -> claim=comment_issue_query expected=REVIEW router=comment_issue@1.0 verdict=REVIEW :: REVIEW-agrees (route=comment_issue == claim=comment_issue_query)
  [OK] "how many open issues do we have?" -> claim=list_issues_query expected=REVIEW router=list_issues@0.9 verdict=REVIEW :: REVIEW-agrees (route=list_issues == claim=list_issues_query)
  [OK] "show my prs" -> claim=list_prs_query expected=REVIEW router=list_prs@0.9 verdict=REVIEW :: REVIEW-agrees (route=list_prs == claim=list_prs_query)
  [FAIL] "show issue #123" -> claim=review_issue_query expected=REVIEW router=list_issues@0.9 verdict=REVIEW :: REVIEW-disagrees (route=list_issues != claim=review_issue_query); expected-not-action-shaped
  [FAIL] "show milestones" -> claim=review_issue_query expected=REVIEW router=list_milestones@1.0 verdict=REVIEW :: REVIEW-disagrees (route=list_milestones != claim=review_issue_query); expected-not-action-shaped
  [FAIL] "what shipped recently" -> claim=shipped_query expected=action:shipped_query router=None@None verdict=UNSCORED :: UNSCORED; UNSCORED — score it (one router call); no verdict, no GO
  [... 52 more [FAIL]/UNSCORED lines, one per new deposit row — all correctly UNSCORED, "no
       verdict, no GO" (see Finding 2 — this is the new, tightened gate rule, not a gap in this
       unit's deposit coverage) ...]
```
(No "needs a corpus row" section printed either before or after — NO-GO suppresses it, consistent
with the PRIORITY/TEMPORAL precedent.)

## New corpus total

283 → **336** rows (+53). Per-category denominators after rebuild: **QUERY 130**, TEMPORAL 69,
PRIORITY 41, GUIDANCE 26, **EXECUTION 26** (was 18, +8 from this deposit's close/reopen/comment
rows), PORTFOLIO 16, STATUS 8, CONVERSATION 5, SYNTHESIS 4, IDENTITY 3, MEMORY 3, DISCOVERY 2,
PROVENANCE 1, TRUST 1, ANALYSIS 1.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 336 rows (59 REVIEW), exit 0.
- `git diff --stat tests/fixtures/inversion_corpus_phase0.yaml scripts/build_inversion_corpus_phase0.py`
  → `2 files changed, 606 insertions(+)`, zero deletions.
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls"
  self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made"
  self-reported; `phase0 corpus: 336 rows (untouched)`.
- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list GITHUB_QUERY_PATTERNS --live
  read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal`
  → exit 0, 66/336 claimed, verdict NO-GO (unchanged from before — 2 pre-existing FAIL rows plus
  53 new UNSCORED rows per Finding 2), 0 "needs a corpus row" lines (NO-GO suppresses the
  section).
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

- `scripts/build_inversion_corpus_phase0.py` (HAND_ROWS: +53 rows in a `# —
  GITHUB_QUERY_PATTERNS` delimited block, extending the existing `# phase3-conversion` section,
  after the TEMPORAL block)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, purely additive, 283→336 rows)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (one pinned constant corrected 283→336,
  with updated docstring)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (progress-log entry added)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read only),
`services/intent_service/workflow_entries.py` (read only, consulted for `_READ_QUERY_FLIP_GROUPS`
and the close/reopen/comment write-rail check, never edited),
`services/intent_service/todo_handlers.py` and
`tests/unit/services/intent_service/test_todo_completion_clause_split_1914.py` (the concurrent
lane's files — confirmed via `git status` at session end, neither touched), `web/` (not touched,
not relevant to this unit), any flag/env var, `scripts/inversion_phase3_deleted_patterns.json`
(no deletion performed).

## Verified how

- **Method**: computed the exact unexercised-literal set by importing and calling the gate's own
  `unexercised_literals()` against `build_census()`'s claimed rows (not hand-counted or
  re-derived). For each of the 53 literals, called the REAL production functions directly —
  `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name assertion AND `intent.action`
  read directly) and `PreClassifier._first_pattern_match(cleaned,
  PreClassifier.GITHUB_QUERY_PATTERNS)` (literal-identity assertion). For the 5 phrases that
  mismatched on the first attempt, debugged each one individually (quoting the actual claimed
  literal / list / action, not guessing) before rewording. Gate re-runs, pytest, and ruff
  invocations were all run this turn via Bash and their output is quoted/counted above, not
  recalled from memory. `git diff --stat` run and quoted directly to confirm purely-additive
  changes.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by design of this unit —
  the Phase-1 router/LLM layer is deliberately UNSCORED here (no LLM calls made anywhere in this
  session, confirmed by each script's own self-report and the absence of any LLM-client
  invocation in the commands run).
- **Denominator**: 1 target list (GITHUB_QUERY_PATTERNS) — all 53 of 53 previously-flagged
  unexercised literals now have a corpus row (0 structurally unreachable, a first for this
  deposit lane). Test denominator: 35/35 in the target Phase-3 test file pass, 29/29 in the
  pre-claim shadow test file pass, 63/63 (plus 1 pre-existing xfail) in the full
  architecture-enforcement suite (full file run, not a subset). Ceiling denominator: 440/440
  unchanged, confirmed by direct call. `git status` run at session end to confirm scope
  compliance (4 files touched by me, 2 files/1 untracked-file belong to the concurrent
  todo_handlers lane, neither touched).

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 —
  deletion gate" and §"scored on BOTH tables" (read for context, not directly exercised — no
  router/catalog change made this session); `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`
  (procedure + progress log, confirmed the 4th deletion and its same-day gate tightening);
  CALENDAR and TEMPORAL prior-session logs (verification methodology, row-block convention,
  category-matches-existing-rows precedent — discovered the EXECUTION-vs-QUERY category split by
  reading the existing yaml fixture directly rather than assuming QUERY throughout, per the
  CALENDAR log's own "investigate before extending" discipline); `workflow_entries.py`
  (`_READ_QUERY_FLIP_GROUPS`, `flip_write_allowlist_key` grep, read only).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections
  (bounded prog dispatch inside an existing worktree — no mailbox write, no sign-off merge, per
  dispatcher scope); the GUIDANCE/PRIORITY deposit-lane logs (read via the progress-log's own
  summary rather than their full session logs, since GITHUB_QUERY_PATTERNS turned out to have no
  structurally-unreachable literals, so their "unreachable literal" methodology wasn't needed
  beyond what CALENDAR/TEMPORAL already demonstrated).
- **Wanted but not found**: none — the dispatch prompt's cited sources were sufficient, though the
  `row_disposition()` UNSCORED-rule tightening (Finding 2) wasn't mentioned in the dispatch and
  had to be discovered by reading the gate script directly when the post-deposit gate output
  diverged from the CALENDAR lane's precedent.

## Discovered work

None filed as separate GitHub issues (matching the PRIORITY/CALENDAR/TEMPORAL/GUIDANCE lanes'
established convention of reporting inline rather than filing). Two findings reported inline
above:
1. **Finding 1** (significant): 23 milestone/release/label/branch literals all resolve to
   `action=review_issue_query` instead of their own registered `list_milestones_query`/
   `list_releases_query`/`list_labels_query`/`list_branches_query` actions — a real gap in the
   pre-classifier's action-determination if/elif chain, not a regex-ordering artifact like prior
   lanes' shadow findings. Flagged for the Lead/Arch to rule on.
2. **Finding 2**: the gate's UNSCORED-row rule was tightened the same day this deposit landed,
   removing the "live via group" shortcut CALENDAR's deposits relied on — worth the next
   deposit-lane agent knowing this changed what a clean post-deposit gate run looks like.
