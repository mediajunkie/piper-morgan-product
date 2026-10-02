# 2026-10-02 1559 — prog (Coding Agent) — #1595 Phase 3 DISCOVERY/ANALYSIS/TRUST/MEMORY deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for `DISCOVERY_PATTERNS` (20), `ANALYSIS_PATTERNS`
(16), `TRUST_PATTERNS` (16), `MEMORY_PATTERNS` (15) in `services/intent_service/pre_classifier.py`
(read only — no literal edited/deleted). Touched only the corpus builder, the fixture yaml, the
pinned corpus-size test, the scope doc, and this session log. NO LLM calls made anywhere. Did not
touch git index (dispatcher instruction).

## Read first

- `dev/2026/10/01/2026-10-01-1320-prog-code-log-1595-phase3-deposits-status.md` — the template lane
  (STATUS_PATTERNS): row-shape convention, the two-step empirical verification
  (`pre_classify_with_pattern_list` for list identity + `_first_pattern_match` for literal
  identity), the "mathematically unreachable" shadow argument (a shorter earlier sibling pattern
  that is a guaranteed substring of a longer later one).
- `services/intent_service/pre_classifier.py` — read `DISCOVERY_PATTERNS` (166-189), `ANALYSIS_
  PATTERNS` (683-700), `TRUST_PATTERNS` (865-885), `MEMORY_PATTERNS`/`INSIGHT_PULL_PATTERNS`
  (887-933), and all four claim branches in `pre_classify_with_pattern_list`: DISCOVERY at
  ~1210 (checked right after greeting/farewell/thanks, before PROVENANCE/TRUST/IDENTITY — earliest
  of the four), PROVENANCE at ~1222 (checked before TRUST, disjoint verb list by design comment),
  TRUST at ~1232, INSIGHT_PULL at ~1245 (checked before MEMORY), MEMORY at ~1259 (guarded by `not
  _is_destructive_ask`), GUIDANCE at ~1768 then ANALYSIS at ~1778 (checked after GUIDANCE, before
  STATUS).
- `services/intent_service/action_registry.py` — confirmed all five relevant actions
  (`get_capabilities`, `explain_trust`, `get_memory`, `pull_insights`, `analyze_blockers`) are
  `ActionDisposition.FLOOR` (lines 69/74/80/83/204).
- `services/intent_service/workflow_entries.py` (READ ONLY) — grep for the five action names: zero
  hits, confirming none is WorkflowEntry/flip_group-registered (consistent with FLOOR, not a new
  finding — unlike STATUS's undocumented-gap finding, this disposition is already on record in
  `action_registry.py`).

## What I did

1. Confirmed all four lists' current literal counts match the dispatch (20/16/16/15) and ran the
   exact BEFORE gate command (`--all --live read_status,read_referent,read_synthesis,create_todo,
   create_reminder,read_strategic,read_temporal,delete_todo`). Quoted below.

2. Discovered (not assumed) that `--all`'s NO-GO column collapses both true NO-GO and "GO
   (partial)" into NO-GO (`render_census_table`'s `lv.deletable` check is the full-GO path only;
   `--list` mode's `render_list_report` is what distinguishes partial). All four lists in fact read
   "GO (partial)" under `--list` — their one existing claimed row is a `[FAIL]`/REVIEW-shaped row,
   not a scored MATCH, but is still "load-bearing" under the partial-verdict logic. This doesn't
   change the deposit task; it's a note on reading the `--all` summary correctly.

3. Computed exact unexercised-literal sets by importing and calling the gate's own
   `unexercised_literals()` against `build_census()` (not hand-counted): DISCOVERY 19/20, ANALYSIS
   15/16, TRUST 15/16, MEMORY 14/15 unexercised.

4. Read each claim branch directly: all four lists are single-action, no per-literal branching
   (DISCOVERY → `get_capabilities`, ANALYSIS → `analyze_blockers`, TRUST → `explain_trust`, MEMORY
   → `get_memory`) — the "no case for this family" shape from STATUS's lane, applied to all four
   lists in their entirety.

5. Checked for shadowing systematically (same-list earlier-sibling substring relationships, and
   cross-list earlier-checked-list collisions) by reading each list's full literal set and the
   if-chain ordering, THEN drafted one phrase per unexercised literal designed to avoid every
   identified shadow, THEN verified empirically in one combined script (62 candidates) against the
   real production matcher: `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name +
   action assertion) and `PreClassifier._first_pattern_match(cleaned, PreClassifier.<LIST>)`
   (literal-identity assertion). **All 62 passed on the first attempt — zero rewords needed.**

6. Found and proved ONE structurally unreachable literal: MEMORY's `\bhow (much|far back) do you
   remember\b` (list position 13) is a strict superset of its own earlier sibling `\bdo you
   remember\b` (position 2) — both of its two alternatives ("how much do you remember" / "how far
   back do you remember") contain "do you remember" as a direct substring with intact word
   boundaries, so the shorter, earlier pattern always wins. Same structural shape as STATUS's "my
   current work" vs "current work" — not phrasing-dependent. Confirmed empirically with two
   independent phrasings ("how far back do you remember our chats", "how much do you remember
   about my preferences"), both claimed by `\bdo you remember\b`.

7. Checked each literal's wording against "does this plainly name a different registered
   destination" (the STATUS standup/portfolio correction precedent) — found no comparable anchor
   for any of the 62 literals across these four lists (no already-MATCH-scored sibling row, no
   in-code documented-collision comment naming a different destination). Left all 62 rows'
   `expected` as the list's single hardcoded action, uncorrected — correcting without an anchor
   would be guessing.

8. Deposited a single HAND_ROWS block (after the existing STATUS_PATTERNS block, before the
   closing `]`) in `scripts/build_inversion_corpus_phase0.py`: 19 DISCOVERY rows (category
   DISCOVERY, `expected: action:get_capabilities`), 15 ANALYSIS rows (category ANALYSIS, `expected:
   action:analyze_blockers`), 15 TRUST rows (category TRUST, `expected: action:explain_trust`), 13
   MEMORY rows (category MEMORY, `expected: action:get_memory`) — 62 rows total. `source` cites
   `phase3-conversion/<LIST> literal r"<literal>"` per row, matching the established convention.

9. Regenerated the corpus: `venv/bin/python scripts/build_inversion_corpus_phase0.py` — 385 → 447
   rows (+62). `git diff --stat` on the yaml + builder: 686 insertions, 0 deletions (purely
   additive). Per-category denominators after rebuild: DISCOVERY 21, ANALYSIS 16, TRUST 16, MEMORY
   16 (each matches literal-count-based arithmetic against the pre-existing REVIEW/claimed rows for
   that category).

10. Updated the pinned corpus total in `tests/unit/test_inversion_phase3_deletion_1595.py`:
    `test_claimed_plus_unclaimed_equals_corpus_size` 385 → 447 (claimed 59 → 121, unclaimed
    unchanged at 326 — confirmed by direct `gate.build_census(cats=None)` call using the test's own
    exact computation, `r.claim.pattern_list is not None`, not a different metric). Searched for
    other pinned `\b385\b` constants: `git grep -n "\b385\b" -- tests scripts` — only the
    just-fixed hit plus unrelated matches (a ledger JSON note, an unrelated validator script
    comment, a large-text fixture line, an unrelated issue-number reference, and my own new text).

11. Re-ran the gate for all four lists: DISCOVERY 20/20 claimed, ANALYSIS 16/16, TRUST 16/16,
    MEMORY 14/15 (the 1 unreachable literal correctly has no row) — all four still NO-GO, every new
    row UNSCORED (same 2026-10-01 gate tightening every prior lane since has found; no live router
    data exists for any of these 62 rows).

12. Ran both dry-run validations — no LLM calls (each script self-reports this):
    - `inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls" self-reported (one
      pre-existing, unrelated TEMPORAL regression note printed — not touched by this unit, no
      TEMPORAL literal involved).
    - `inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made" self-reported.

13. `ruff format` + `ruff check --fix` on both touched `.py` files → clean, no changes needed;
    re-run confirms both still clean.

14. Tests (all run together this turn, output quoted below):
    - `tests/unit/test_inversion_phase3_deletion_1595.py` +
      `tests/unit/test_inversion_phase3_surface2_floor_1595.py` +
      `tests/unit/services/intent_service/test_preclaim_shadow.py` +
      `tests/test_architecture_enforcement.py` — **144 passed, 1 xfailed**, 0 failed.
    - Extraction ceiling re-confirmed **259** (unchanged) via direct
      `pattern_literal_counts.total_literal_count()` call — no `pre_classifier.py` literal
      edited/deleted in this unit.

15. Added a dated progress-log entry to `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

16. Verified scope compliance via `git status --porcelain` at session end: only
    `scripts/build_inversion_corpus_phase0.py`, `tests/fixtures/inversion_corpus_phase0.yaml`, and
    `tests/unit/test_inversion_phase3_deletion_1595.py` show as modified; untracked files present
    (`dev/2026/09/27…`, `dev/2026/09/28…`, `dev/2026/09/29…`, the 1030 guidance-deletion log,
    `dev/active/canonical-retest-serving-llm.json`) pre-date this session (the Lead's own
    in-progress work per the git-status snapshot at dispatch time) — none created or touched by me.
    Git index not touched (nothing staged, per dispatcher instruction).

## Rows added (62 total, 62/62 reachable literals, 1 unreachable)

### DISCOVERY_PATTERNS (19 of 19 unexercised literals — 100% reachable)

| phrase | literal exercised |
|---|---|
| "what are your capabilities?" | `\bwhat are your capabilities\b` |
| "what services can you provide?" | `\bwhat services\b` |
| "what do you offer as an assistant?" | `\bwhat do you offer\b` |
| "what features does piper have?" | `\bwhat features\b` |
| "what can you help me do today?" | `\bwhat can you help\b` |
| "show me your capabilities" | `\bshow me your capabilities\b` |
| "give me a menu of services" | `\bmenu of services\b` |
| "can you list your capabilities" | `\blist.*capabilities\b` |
| "I want to understand your capabilities better" | `\byour capabilities\b` |
| "pull up the capability menu" | `\bcapability menu\b` |
| "open the capabilities menu" | `\bcapabilities menu\b` |
| "show me the menu" | `\bshow.*menu\b` |
| "what are you able to do for my project" | `\bwhat.*able to do\b` |
| "show me the features you offer" | `\bshow.*features\b` |
| "what's available in terms of features" | `\bavailable.*features\b` |
| "help" | `^help$` |
| "open the help menu" | `\bhelp\s*menu\b` |
| "can you show help topics" | `\bshow\s*help\b` |
| "I need help understanding something" | `\bneed\s*help\b` |

All `expected: action:get_capabilities`. No rewords needed.

### ANALYSIS_PATTERNS (15 of 15 unexercised literals — 100% reachable)

| phrase | literal exercised |
|---|---|
| "what is blocking this release" | `\bwhat is blocking\b` |
| "what tasks are blocking our sprint" | `\bwhat.*block(?:s\|ing\|ed)\s+(?:the\|my\|our)\b` |
| "blockers for the release" | `\bblockers?\s+(?:for\|on\|in)\b` |
| "what's the main obstacle here" | `\bwhat.*obstacle\b` |
| "what's in the way of finishing this" | `\bwhat'?s in the way\b` |
| "let's analyze the risk here" | `\banalyze.*(?:risk\|impact\|blocker\|bottleneck)\b` |
| "I'd like a risk assessment for this project" | `\brisk assessment\b` |
| "can you run an impact analysis on this change" | `\bimpact analysis\b` |
| "is there a bottleneck analysis available" | `\bbottleneck.*(?:analysis\|report)\b` |
| "what risks does this project have" | `\bwhat risks\b` |
| "what risk do we have in this plan" | `\bwhat.*risk(?:s)?\s+(?:should\|do\|are)\b` |
| "please identify the risks in this plan" | `\bidentify.*risks?\b` |
| "risks we should flag before launch" | `\brisk(?:s)?\s+(?:i\|we)\s+should\b` |
| "threats to our timeline this week" | `\bthreats?\s+(?:to\|should\|i)\b` |
| "what could threaten this deadline" | `\bwhat.*threaten\b` |

All `expected: action:analyze_blockers`. No rewords needed.

### TRUST_PATTERNS (15 of 15 unexercised literals — 100% reachable)

| phrase | literal exercised |
|---|---|
| "why won't you create issues for me" | `\bwhy won'?t you\b` |
| "why don't you just do it yourself" | `\bwhy don'?t you\b` |
| "why are you always cautious about this suggestion" | `\bwhy (are\|do) you (so\|being so\|always) (cautious\|careful\|conservative)\b` |
| "what can't you do here" | `\bwhat can'?t you do\b` |
| "what are your limits as an assistant" | `\bwhat are your limits\b` |
| "what's the capability boundary here" | `\bcapability (boundary\|boundaries\|limits)\b` |
| "how well do you know me by now" | `\bhow (well )?do you know me\b` |
| "do you trust me with this decision" | `\bdo you trust me\b` |
| "how much do you trust my judgment" | `\bhow much do you trust\b` |
| "what's our relationship like these days" | `\bwhat'?s our relationship\b` |
| "how do you see our relationship evolving" | `\bhow do you see our relationship\b` |
| "how do we work together on this project" | `\bhow do (we\|you and i) work together\b` |
| "why did you go ahead without asking" | `\bwhy did you (do\|just\|go ahead)\b` |
| "why do you always ask me the same thing" | `\bwhy do you (always\|keep)\b` |
| "i didn't ask you to do that" | `\bi didn'?t (ask\|tell) you to\b` |

All `expected: action:explain_trust`. No rewords needed. Checked specifically against PROVENANCE
(checked earlier in the if-chain, overlapping "why did you" vocabulary) — disjoint by design
(PROVENANCE's verb list is mention/bring up/suggest/recommend/surface/raise/flag; TRUST's is
do/just/go ahead) — no shadow.

### MEMORY_PATTERNS (13 of 14 unexercised literals reachable — 1 unreachable)

| phrase | literal exercised |
|---|---|
| "what can you remember about our last conversation" | `\bwhat can you remember\b` |
| "do you remember my last project update" | `\bdo you remember\b` |
| "remember when we shipped the last release?" | `\bremember (when\|that\|our\|my)\b` |
| "can you show my conversation history" | `\b(show\|view\|see) (my \|our )?(conversation )?history\b` |
| "our history together has been good" | `\b(my\|our) (conversation )?history\b` |
| "let's look at past conversations we've had" | `\bpast conversations?\b` |
| "pull up my previous messages please" | `\bprevious (conversations?\|chats?\|messages?)\b` |
| "can I see the conversation log" | `\bconversation log\b` |
| "find when I mentioned this bug before" | `\bfind (when\|where) (i\|we)\b` |
| "search history for that conversation topic" | `\bsearch (my \|our )?(conversation )?history\b` |
| "what did we discuss in our last session" | `\bwhat (did\|have) (i\|we) (talk\|discuss\|say)\b` |
| "what we discussed yesterday was helpful" | `\bwhat (i\|we) (said\|talked\|discussed)\b` |
| "how long is your memory exactly" | `\bhow long (is\|do) (your\|my) memory\b` |

All `expected: action:get_memory`. No rewords needed.

**Unreachable**: `\bhow (much|far back) do you remember\b` (list position 13) — mathematically
shadowed by its own earlier, shorter sibling `\bdo you remember\b` (position 2). Both alternatives
of the unreachable literal ("how much do you remember" / "how far back do you remember") contain
"do you remember" as a guaranteed direct substring with intact word boundaries, so the shorter
earlier pattern claims first for every possible phrase — a structural shadow, not
phrasing-dependent (same shape as STATUS_PATTERNS' "my current work" vs "current work"). Confirmed
empirically with two independent phrasings, both claimed by `\bdo you remember\b`. No row deposited
for this literal; recorded with proof in the HAND_ROWS comment block.

## Literals whose wording names a different destination

None found. Unlike STATUS_PATTERNS (standup/portfolio literals with a direct in-corpus
already-MATCH-scored anchor, plus in-code documented-collision comments), none of these 62 literals
across the four lists has a comparable anchor pointing to a different registered destination.
`expected` is left as the list's single hardcoded action for all 62 rows; the Lead's scoring pass
will surface any warranted corrections from real router data.

## Per-branch action shape

All four lists are single-action (no per-literal branching), same "no case for this family" shape
STATUS_PATTERNS showed in its own lane — unlike GITHUB_QUERY_PATTERNS' partial if/elif (7 distinct
actions):
- `DISCOVERY_PATTERNS` → `get_capabilities` (category DISCOVERY) for all 20 literals.
- `ANALYSIS_PATTERNS` → `analyze_blockers` (category ANALYSIS) for all 16 literals.
- `TRUST_PATTERNS` → `explain_trust` (category TRUST) for all 16 literals.
- `MEMORY_PATTERNS` → `get_memory` (category MEMORY) for all 15 literals (guarded by `not
  PreClassifier._is_destructive_ask`).

All five relevant actions (including `pull_insights`, INSIGHT_PULL_PATTERNS' action, checked just
before MEMORY) are `ActionDisposition.FLOOR` in `action_registry.py`, with zero
`workflow_entries.py` registrations (grep-confirmed) — this is the documented disposition already
on record for these four lists, not a new finding the way STATUS's undocumented gap was.

## Gate output — BEFORE

```
corpus denominator: 385 rows total = 59 claimed + 326 unclaimed

list                                     literals   rows      verdict
----------------------------------------------------------------------
ANALYSIS_PATTERNS                              16      1        NO-GO
DISCOVERY_PATTERNS                             20      1        NO-GO
MEMORY_PATTERNS                                15      1        NO-GO
TRUST_PATTERNS                                 16      1        NO-GO
```

## Gate output — AFTER

```
corpus denominator: 447 rows total = 121 claimed + 326 unclaimed

list                                     literals   rows      verdict
----------------------------------------------------------------------
ANALYSIS_PATTERNS                              16     16        NO-GO
DISCOVERY_PATTERNS                             20     20        NO-GO
MEMORY_PATTERNS                                15     14        NO-GO
TRUST_PATTERNS                                 16     16        NO-GO
```

All four NO-GO is correct and expected: every new row reads UNSCORED (no router call made, no LLM
calls anywhere in this unit) — the same 2026-10-01 gate tightening every prior deposit lane since
has found. The Lead's budgeted scoring run resolves MATCH/REVIEW/MISMATCH per row.

## New corpus total

385 → **447** rows (+62). Per-category denominators after rebuild: QUERY 129, TEMPORAL 69, STATUS
54, PRIORITY 44, GUIDANCE 26, EXECUTION 26, **DISCOVERY 21** (was 2), PORTFOLIO 17, **MEMORY 16**
(was 3), **TRUST 16** (was 1), **ANALYSIS 16** (was 1), CONVERSATION 5, SYNTHESIS 4, IDENTITY 3,
PROVENANCE 1.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 447 rows (54 REVIEW), exit 0.
- `git diff --stat tests/fixtures/inversion_corpus_phase0.yaml scripts/build_inversion_corpus_phase0.py`
  → `2 files changed, 686 insertions(+)`, zero deletions.
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls"
  self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made"
  self-reported.
- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --all --live read_status,read_referent,
  read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo` → exit 0,
  corpus denominator 447 rows = 121 claimed + 326 unclaimed; DISCOVERY 20/20, ANALYSIS 16/16, TRUST
  16/16, MEMORY 14/15, all NO-GO (UNSCORED).
- `venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py
  tests/unit/test_inversion_phase3_surface2_floor_1595.py
  tests/unit/services/intent_service/test_preclaim_shadow.py tests/test_architecture_enforcement.py
  -q -p no:cacheprovider` → **144 passed, 1 xfailed**, exit 0.
- `venv/bin/python -c "import sys; sys.path.insert(0,'scripts'); import pattern_literal_counts as
  plc; print(plc.total_literal_count())"` → **259**, unchanged (ceiling untouched — no
  pre_classifier literal edited/deleted; task's "ceiling exactly 259" condition met).
- `venv/bin/ruff format` + `ruff check --fix` on both touched `.py` files → clean, no changes
  needed; re-run confirms both still clean.

## Files touched

- `scripts/build_inversion_corpus_phase0.py` (HAND_ROWS: +62 rows in one comment-headed block
  covering all four lists, after the existing STATUS_PATTERNS block, before the closing `]`)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, purely additive, 385→447 rows)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (one pinned constant corrected 385→447, with
  updated docstring)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (dated progress-log entry added)
- This session log (new)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read only),
`services/intent_service/workflow_entries.py` (read only), `services/intent_service/
action_registry.py` (read only), `web/` (not touched, not relevant to this unit), any flag/env
var, `scripts/inversion_phase3_deleted_patterns.json` (no deletion performed), the gate script, the
ledger, GitHub.

## Verified how

- **Method**: computed the exact unexercised-literal set per list by importing and calling the
  gate's own `unexercised_literals()` against `build_census()`'s claimed rows (not hand-counted).
  Before drafting any phrase, read each list's full literal set and the `pre_classify_with_
  pattern_list` if-chain ordering directly (not inferred) to identify same-list earlier-sibling
  substring shadows and cross-list earlier-checked-list collisions by hand; drafted phrases
  designed to avoid every identified shadow; then verified all 62 in one combined script run
  against the REAL production functions — `PreClassifier.pre_classify_with_pattern_list(phrase)`
  (list-name assertion AND `intent.action` read directly) and `PreClassifier._first_pattern_match
  (cleaned, PreClassifier.<LIST>)` (literal-identity assertion) — with 0 failures and 0 duplicate
  phrases on the first attempt. For the 1 unreachable literal, verified the shadow by (a) reading
  both patterns directly and confirming the substring-containment argument holds for both of the
  unreachable literal's alternatives, and (b) empirically confirming with two independent
  phrasings. Gate re-runs, pytest, and ruff invocations were all run this turn via Bash and their
  output is quoted/counted above, not recalled from memory. `git diff --stat` run and quoted
  directly to confirm purely-additive changes. `git status --porcelain` run at session end to
  confirm scope compliance.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by design of this unit —
  the Phase-1 router/LLM layer is deliberately UNSCORED here (no LLM calls made anywhere in this
  session, confirmed by each script's own self-report and the absence of any LLM-client invocation
  in the commands run). The FLOOR/no-workflow-entry disposition was verified by reading
  `action_registry.py` and `workflow_entries.py` directly, not inferred from behavior.
- **Denominator**: 4 target lists (DISCOVERY/ANALYSIS/TRUST/MEMORY) — 62 of 63 previously-flagged
  unexercised literals (across all four lists combined) now have a corpus row; 1 of 63 confirmed
  structurally unreachable (proven via substring-containment argument, not just empirically
  probed). Test denominator: 144/144 passed (plus 1 pre-existing xfail) across all four specified
  test files run together in one invocation, not separately. Ceiling denominator: 259/259
  unchanged, confirmed by direct call. `git status` run at session end to confirm scope compliance
  (3 tracked files touched by me, matching the dispatch's allowed scope; pre-existing untracked
  files from the Lead's own session left alone).

## Memory & briefing surfaces referenced this session

- **Referenced**: `dev/2026/10/01/2026-10-01-1320-prog-code-log-1595-phase3-deposits-status.md`
  (row-shape convention, two-step empirical verification method, the mathematical-unreachability
  argument shape — directly informed the MEMORY finding); `dev/2026/09/25/
  inversion-epic0-remaining-scope-2026-09-25.md` (procedure + progress log, appended to).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections
  (bounded prog dispatch inside an existing worktree — no mailbox write, no sign-off merge, per
  dispatcher scope — git index not touched at all); the GITHUB/PRIORITY/GUIDANCE deposit-lane logs
  (not re-read in full — the STATUS log's own summary of the shared methodology was sufficient
  since all four of this unit's lists share STATUS's exact "single hardcoded action" shape, with no
  new per-literal-branching or cross-list shadow complexity to investigate beyond the one MEMORY
  self-shadow).
- **Wanted but not found**: none — the dispatch prompt's cited template log and the live code
  (pre_classifier.py, action_registry.py, workflow_entries.py) were sufficient for every claim made
  in this unit.

## Discovered work

None filed as separate GitHub issues (matching the established convention of prior deposit lanes —
reporting inline rather than filing, since these are measurement/evidence findings for the Lead's
own ruling, not independently actionable bugs). One structural finding reported inline above (the
MEMORY self-shadow, with proof) — no corrections or disposition questions this time, since all four
lists' FLOOR disposition and lack of workflow-entry registration is already documented in
`action_registry.py`/`workflow_entries.py`, unlike STATUS's undocumented-gap finding.
