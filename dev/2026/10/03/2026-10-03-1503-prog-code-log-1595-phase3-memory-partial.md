# 2026-10-03 — Coding Agent (prog), model: Sonnet 5 — #1595 Phase 3 eleventh deletion (MEMORY_PATTERNS, PARTIAL)

Dispatched by Lead Developer. Worktree: `/Users/xian/Development/piper-morgan-worktrees/lead`,
branch `claude/lead-cycle`. Do NOT commit (Lead commits by pathspec after review). No LLM calls, no
`gh`, no env/flag/deploy/web touches.

## Task

Eleventh deletion in the #1595 Phase 3 ratchet, the FIFTH PARTIAL one: `MEMORY_PATTERNS` (15
literals) in `services/intent_service/pre_classifier.py` — 12 literals go, 3 SURVIVE
(`\b(my|our) (conversation )?history\b`, `\bsearch (my |our )?(conversation )?history\b`,
`\bwhat (i|we) (said|talked|discussed)\b`).

## STEP 1 — BEFORE gate + literal audit

Ran:
```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list MEMORY_PATTERNS \
  --live create_reminder,create_todo,delete_todo,read_floor,read_referent,read_status,read_strategic,read_synthesis,read_temporal
```

Result (log noise stripped):
```
corpus denominator: 447 rows total = 87 claimed + 360 unclaimed

## MEMORY_PATTERNS
literals: 15  |  rows claimed: 14/447
verdict: GO (partial) — 3 load-bearing literal(s) SURVIVE, deleting the other 12: ceiling 225 -> 213
  survives: r"\b(my|our) (conversation )?history\b"  <- 'our history together has been good'
  survives: r"\bsearch (my |our )?(conversation )?history\b"  <- 'search history for that conversation topic'
  survives: r"\bwhat (i|we) (said|talked|discussed)\b"  <- 'what we discussed yesterday was helpful'

rows claimed:
  [OK] "what do you remember about me?" -> claim=get_memory expected=REVIEW router=get_memory@1.0 verdict=REVIEW :: REVIEW-agrees (route=get_memory == claim=get_memory; live via group)
  [OK] "what can you remember about our last conversation" -> ... MATCH (expected action live via group)
  [OK] "do you remember my last project update" -> ... MATCH (expected action live via group)
  [OK] "remember when we shipped the last release?" -> claim=get_memory expected=action:check_completion_status router=check_completion_status@0.85 verdict=MATCH :: MATCH on a non-live op, and the pattern mis-serves this row — deleting cannot make the fallback worse; surface 2: surface 2 lands in STATUS only 0/10 probe samples
  [OK] "can you show my conversation history" -> ... MATCH (expected action live via group)
  [FAIL] "our history together has been good" -> claim=get_memory expected=action:get_memory router=NONE@0.95 verdict=MISMATCH :: the pattern is the live path for this phrase — router did not name an operation; surface 2 names get_memory only 0/10 probe samples
  [OK] "let's look at past conversations we've had" -> ... MATCH (expected action live via group)
  [OK] "pull up my previous messages please" -> ... MATCH (expected action live via group)
  [OK] "can I see the conversation log" -> ... MATCH (expected action live via group)
  [OK] "find when I mentioned this bug before" -> ... MATCH (expected action live via group)
  [FAIL] "search history for that conversation topic" -> claim=get_memory expected=action:get_memory router=CLARIFY@0.4 verdict=MISMATCH :: the pattern is the live path for this phrase; surface 2 names get_memory only 0/10 probe samples
  [OK] "what did we discuss in our last session" -> ... MATCH (expected action live via group)
  [FAIL] "what we discussed yesterday was helpful" -> claim=get_memory expected=action:get_memory router=NONE@0.95 verdict=MISMATCH :: the pattern is the live path for this phrase; surface 2 names get_memory only 0/10 probe samples
  [OK] "how long is your memory exactly" -> ... MATCH (expected action live via group)
```
Matches the dispatch's expectation exactly (GO (partial), 3 survivors, ceiling 225 -> 213) — no
STOP.

Confirmed independently:
- `pattern_literal_counts.total_literal_count()` → 225 (pre-deletion baseline).
- `pattern_literal_counts.per_list_literal_counts()["MEMORY_PATTERNS"]` → 15.

**Unexercised-literal audit (STEP 2) — NOT the clean case, as the dispatch prompt flagged in
advance** (14 rows claimed for 15 literals): computed via the gate's own `unexercised_literals
("MEMORY_PATTERNS", lv.rows)` → exactly 1 unexercised, `\bhow (much|far back) do you remember\b`.

Constructed the most natural phrasings that would hit it and ran them through the REAL if-chain,
`PreClassifier.pre_classify_with_pattern_list` (never `_first_pattern_match` alone):

| phrase | result |
|---|---|
| "how much do you remember" | `(MEMORY_PATTERNS, get_memory)` |
| "how much do you remember about me" | `(MEMORY_PATTERNS, get_memory)` |
| "how much do you remember about our conversation" | `(MEMORY_PATTERNS, get_memory)` |
| "how far back do you remember" | `(MEMORY_PATTERNS, get_memory)` |
| "how far back do you remember our conversations" | `(MEMORY_PATTERNS, get_memory)` |
| "how far back can you remember" | `(None, None)` — doesn't match this literal's exact text either |

All 5 phrasings that DO match the unexercised literal's shape are claimed by MEMORY_PATTERNS, but
NOT by this literal — confirmed by running `PreClassifier._first_pattern_match` against
`MEMORY_PATTERNS` alone for the same 5 phrases: every one returns `\bdo you remember\b` (list
index 2, checked BEFORE this literal's former index 13) as the first match, never the unexercised
literal. "do you remember" is a guaranteed substring of every phrase the unexercised literal's
regex requires (`how (much|far back) do you remember`), preceded by a word boundary, so the
earlier sibling provably claims first for every possible phrase this literal could ever match.

**PROVABLY SHADOWED within the same list** (not cross-list): `\bdo you remember\b` is itself one
of the 12 literals this same commit deletes (not a survivor), so this shadowing changes nothing
about the deletion's safety — neither literal ever independently determined any corpus row's
claim. No corpus deposit needed, no STOP.

| literal | status | evidence |
|---|---|---|
| 10 of 12 to-be-deleted literals | exercised, 1:1, live MATCH | each claims exactly one `[OK]` row, expected action live via group |
| 1 to-be-deleted literal (`\bremember (when\|that\|our\|my)\b`) | exercised, mis-serve | claims "remember when we shipped the last release?" as `get_memory`, disagreeing with ruled `check_completion_status`; router independently MATCHes `check_completion_status@0.85` on a non-live op; N=10 surface-2 probe does NOT land STATUS (0/10) — mis-serve rule applies regardless |
| 1 to-be-deleted literal (`\bhow (much\|far back) do you remember\b`) | UNEXERCISED, shadowed | every candidate phrasing claimed first by the earlier sibling `\bdo you remember\b` (also deleted); never independently reachable |
| 3 survivors | exercised | each claims its own `[FAIL]` row |

## STEP 3 — applied the partial deletion

`services/intent_service/pre_classifier.py`: `MEMORY_PATTERNS` now exactly the 3 survivor
literals, in their original relative order, each with a one-line comment naming the corpus row it
carries, preceded by a dated comment block recording the deletion, the gate quote, the
unexercised-literal shadowing finding, and the ceiling arithmetic. Orphaned category comments
("# Direct memory questions...", "# Memory meta questions...") that no longer had any literal
underneath were removed rather than left dangling. Claim branch (`pre_classify`'s MEMORY_PATTERNS
if-block, checked after INSIGHT_PULL_PATTERNS and guarded by `_is_destructive_ask`) left untouched
(still live, non-empty list). Confirmed via `pattern_literal_counts.total_literal_count()` → 213,
`per_list_literal_counts()["MEMORY_PATTERNS"]` → 3.

`ruff check`/`ruff format --check` on the edited file: clean, no changes needed.

## STEP 4 — reabsorption check + AFTER gate

For each of the 11 deleted-literal corpus-row phrases, plus the shadowed literal's 2 candidate
phrasings, ran `gate.claim_for_phrase(PreClassifier, phrase)` (both entry surfaces internally)
against the live, post-deletion `PreClassifier`:

```
=== deleted corpus rows (11) ===
'what do you remember about me?'                        -> UNCLAIMED
'what can you remember about our last conversation'     -> UNCLAIMED
'do you remember my last project update'                -> UNCLAIMED
'remember when we shipped the last release?'            -> UNCLAIMED
'can you show my conversation history'                  -> list=MEMORY_PATTERNS action=get_memory (REABSORBED)
"let's look at past conversations we've had"            -> UNCLAIMED
'pull up my previous messages please'                   -> UNCLAIMED
'can I see the conversation log'                        -> UNCLAIMED
'find when I mentioned this bug before'                 -> UNCLAIMED
'what did we discuss in our last session'               -> UNCLAIMED
'how long is your memory exactly'                       -> UNCLAIMED

=== unexercised-literal candidate phrasings ===
'how much do you remember'                              -> UNCLAIMED
'how far back do you remember'                          -> UNCLAIMED

=== survivor rows still claimed ===
'our history together has been good'                    -> list=MEMORY_PATTERNS action=get_memory
'search history for that conversation topic'            -> list=MEMORY_PATTERNS action=get_memory
'what we discussed yesterday was helpful'                -> list=MEMORY_PATTERNS action=get_memory
```

**1 AGREEING reabsorption**: "can you show my conversation history" (formerly claimed by the
deleted `\b(show|view|see) (my |our )?(conversation )?history\b` literal) is now reclaimed by the
surviving `\b(my|our) (conversation )?history\b` literal — "my conversation history" is a
substring of the phrase, same action (`get_memory`), same list, same category. The other 10
deleted-row phrases plus both unexercised-literal candidates are genuinely UNCLAIMED. All 3
survivor rows remain claimed by `MEMORY_PATTERNS` itself.

`--all` gate: `MEMORY_PATTERNS 3 4 NO-GO` (3 literals, 4 rows — the 3 survivors `[FAIL]` plus the
1 reabsorbed row `[OK]` — expected for a partial list's remainder). Corpus denominator: 447 = 77
claimed + 370 unclaimed (down from 87 claimed; 87 − 77 = 10, the net of 11 deleted-row claims
losing the 1 reabsorbed row). `pattern_literal_counts.total_literal_count()` → 213 confirmed again
post-edit.

## STEP 5 — ceiling + ledger

`CEILINGS["pre-classifier"]` 225 → 213 in `tests/test_architecture_enforcement.py`, dated comment
block matching the established per-deletion style.

Appended the 12th `DELETED_PATTERN_LISTS` entry to `scripts/inversion_phase3_deleted_patterns.json`
via a one-off Python build script (never hand-typed): `"partial": true`, `"surviving_literals"`
(3-literal map), `"literals": 12` (deleted count), `rows_claimed_at_deletion` (11 phrases),
`verdict_report` (`inversion-phase1-shadow-score-2026-09-25.md` for the REVIEW-agrees row,
`inversion-phase3-memory-rescore-2026-10-03.md` for the rest — the latest MEMORY-specific rescore
in `gate.PHASE3_REPORTS`' precedence order), `expected_op_by_phrase` (11 entries: 10 `get_memory`,
1 `check_completion_status` for the mis-serve row), `shadowed_literals` (1 entry — the unexercised
literal, with the full shadowing evidence), `misserved_at_deletion` (1 entry — "remember when we
shipped the last release?"), `surface2_verified_at_deletion: {}` (empty — the mis-serve row didn't
need the surface-2 escape), `known_reabsorptions` (1 entry — "can you show my conversation
history", agreeing). **Reloaded with `json.load` immediately after writing** — confirmed 12
entries, parses cleanly. The first `json.dump` pass reformatted 3 PRE-EXISTING notes elsewhere in
the file from `—` escapes to literal em-dash characters (an `ensure_ascii=False` side effect)
and introduced 2 raw-string escaping artifacts of my own (`r"...\"` at a string's end, which in a
raw string literal keeps the backslash) in this entry's own prose — both caught via `git diff
--stat` showing unexpected `-`/`+` pairs on unrelated lines, and via `json.load` + manual
inspection of the decoded strings; both fixed with targeted `Edit` calls (restored the 3
pre-existing `—` escapes byte-for-byte; fixed the 2 stray backslashes in the new entry's
prose) so the final diff is a pure 73-line insertion. Verified via `check_deleted_entry_non_
regression`-equivalent checks (the AFTER reabsorption scan above) and by re-running the full gate.

## STEP 6 — test conversion, 3 files + 2 confirmed-unaffected

Ran the specified suite set, found and converted 3 files:

1. **`tests/unit/services/test_pre_classifier.py`**:
   - `test_memory_patterns` (12-phrase list, asserted every one matched MEMORY and routed to
     `get_memory`) — 9 of the 12 matched now-deleted literals with no surviving literal covering
     them. Renamed to `test_memory_patterns_now_unclaimed_by_surface_1`, dropped the 3 still-claimed
     phrases, flipped the assertion to `PreClassifier.pre_classify(pattern) is None` for the
     remaining 9. Added `test_memory_survivor_literals_still_match` for the 3 remaining ("show my
     history" and "view my conversation history" — reabsorbed by the surviving
     `\b(my|our) (conversation )?history\b` literal — plus "search my history for budget",
     unaffected, already claimed by the surviving `\bsearch ... history\b` literal).
   - `test_memory_not_trust` — its first fixture ("what do you remember about our project", matched
     the deleted `\bwhat do you remember\b` literal) swapped to "our history together has been
     good" — still proves a MEMORY-claimed phrase doesn't collide with TRUST.
   - `test_portfolio_not_memory` — its second fixture ("what do you remember about me", same
     deleted literal) swapped the same way — still proves MEMORY doesn't collide with PORTFOLIO.
   - `test_memory_get_memory_still_works_after_pull_insights` (4-phrase INSIGHT_PULL-ordering
     regression guard) — 3 of the 4 matched now-deleted literals. Split into a `now_unclaimed` list
     (asserting `None` for "What do you remember about me?", "Do you remember when we discussed
     the API?", "What did we talk about yesterday?") plus the 1 survivor query ("Show my
     conversation history"), still asserted MEMORY/`get_memory`.
   - Full file run: 35 passed.

2. **`tests/unit/services/intent_service/test_read_lane_destructive_greed_1756.py`**:
   - `MEMORY_LANE_DESTRUCTIVE` (15 phrases) confirmed unaffected: the `_is_destructive_ask` guard
     declines these before any MEMORY_PATTERNS literal is even consulted (verified directly — all
     15 still `None`).
   - `MEMORY_READS` (11 phrases, in `KEEP_CLAIMING`): 8 of the 11 matched now-deleted literals with
     no surviving literal covering them ("what do you remember", "do you remember", "past
     conversations", "previous conversations", "conversation log", "what did we talk about", "how
     much do you remember", "remember when we discussed the api"). Moved those 8 to a new
     `MEMORY_READS_NOW_UNCLAIMED` tuple and added `TestMemoryReadsNowDeclineAtSurfaceOne` (mirrors
     `TestTemporalReadsNowDeclineAtSurfaceOne`, noting MEMORY_PATTERNS is partial not tombstoned
     but none of these 8 is covered by a surviving literal). `MEMORY_READS` keeps the 3 still-
     claimed phrases ("show my history", "my conversation history", "search my history").
   - `READS_MENTIONING_DESTRUCTIVE_VERBS`: 2 of its 5 phrases ("do you remember what i deleted",
     "what did we discuss about deleting projects") matched now-deleted literals and lost their
     claim. Swapped for 2 phrases confirmed claiming at confidence 1.0 AND confirmed NOT an ask
     position (`PreClassifier._is_destructive_ask` returns `False` for each) via MEMORY_PATTERNS'
     surviving history literals: "can you show my history before i delete these old notes" and
     "search my history before i cancel this project".
   - Full file run: 264 passed.

3. **`tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py`**:
   - `("MEMORY", "get_memory")`'s probe message "what do you remember?" matched the now-deleted
     `\bwhat do you remember\b` literal. Swapped to "our history together has been good" (matches
     the surviving `\b(my|our) (conversation )?history\b` literal, confirmed mapping to the same
     pair this session) — the pair itself is unaffected.
   - Full file run: 11 passed.

4. **`tests/e2e/test_read_floor_live.py`** — checked, NOT touched: `pytest.mark.llm`-gated
   (skipped without `PIPER_E2E_LIVE_HEADER_KEY`), tests end-to-end router/floor dispatch for
   `get_memory` (among others), not which literal matched at surface 1 — out of scope for a
   no-LLM-calls unit regardless.

5. **`services/intent_service/chat_pointers.py`** — checked, NOT touched. Grepped for
   `get_memory`/`MEMORY` — no `CHAT_POINTERS` entry resolves through `MEMORY_PATTERNS`.

Also ran `git grep -l -e MEMORY_PATTERNS -e get_memory -- tests/` per the dispatch's explicit
instruction and checked every hit: `tests/e2e/test_read_floor_live.py` and
`tests/fixtures/inversion_corpus_phase0.yaml` (ground-truth corpus data, never edited by the
deletion procedure — only `pre_classifier.py` loses literals) and `tests/performance/
test_standup_performance.py` / `tests/plugins/performance/test_memory_usage.py` /
`tests/unit/services/integrations/slack/test_spatial_system_integration.py` /
`tests/unit/services/memory/test_conversational_memory.py` / `tests/unit/services/memory/
test_greeting_context.py` — all use an unrelated `get_memory_window` method name or mock
`intent_action="get_memory"` literal unconnected to `PreClassifier.pre_classify`, confirmed by
inspection, not affected by this deletion.

Full suite run (`tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py`
+ `tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py` +
`tests/unit/test_inversion_phase3_surface2_floor_1595.py` +
`tests/unit/test_inversion_phase1_shadow_score_1595.py`, one combined invocation, run in
background due to runtime — 149.54s): **5186 passed, 1 xfailed, 0 failed, exit code 0**.

`tests/unit/services/test_multi_intent.py` (pre-existing out-of-scope failures per the dispatch,
run separately with `-o addopts="--import-mode=importlib --tb=line"`): **16 failed, 11 passed** —
identical count to the dispatch's stated baseline (16), confirming no new failures.

`ruff format`/`ruff check` run on exactly the 6 touched `.py` files (confirmed via `git status
--short` before invoking ruff — the ledger JSON was never in the argument list): all clean, no
formatting needed.

## STEP 7 — docs

Appended "### Eleventh deletion (2026-10-03): `MEMORY_PATTERNS` (partial — 12 of 15)" to
`docs/internal/architecture/current/intent-routing-stack.md` (full BEFORE/AFTER gate quotes, the
partial rule, the shadowed-literal audit in full, the one `misserved_at_deletion` row, the one
`known_reabsorptions` entry, all converted/confirmed-unaffected test files + the
e2e/chat_pointers.py checks, ceiling arithmetic). Dated entry appended to
`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

**Files touched** (no commits — Lead commits by pathspec):
`services/intent_service/pre_classifier.py`, `scripts/inversion_phase3_deleted_patterns.json`,
`tests/test_architecture_enforcement.py`, `tests/unit/test_inversion_phase3_deletion_1595.py`,
`tests/unit/services/test_pre_classifier.py`,
`tests/unit/services/intent_service/test_read_lane_destructive_greed_1756.py`,
`tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py`,
`docs/internal/architecture/current/intent-routing-stack.md`,
`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`, this session log.

No product code outside `pre_classifier.py`'s pattern-literal edit was changed. No `.json` file
was ever passed to ruff. No `gh`/issue tooling used (off-limits for this dispatch). No env/flag/
deploy/web touches.

## Verified how

**Method**: every gate run quoted above was executed this session against the live repo state
(not recalled); `pattern_literal_counts.total_literal_count()`/`per_list_literal_counts()` called
directly against the live, edited `PreClassifier` class before and after the edit;
`unexercised_literals`/`pre_classify_with_pattern_list`/`_first_pattern_match`/`claim_for_phrase`
run empirically for the unexercised-literal audit (5 candidate phrasings, both the full if-chain
and the MEMORY_PATTERNS-only matcher), the AFTER reabsorption scan (11 deleted-row phrases + 2
shadowed-literal candidates + 3 survivor rows, 16 total), and the test-fixture breakage survey (a
dedicated script run against every phrase in the 4 affected test files before editing any of
them, not inferred from the regex text); the ledger entry was built via a one-off Python script,
reloaded with `json.load` immediately, and a `git diff` byte-review caught 2 self-introduced
raw-string escaping bugs and 3 incidental em-dash re-encodings before they were fixed and
re-verified; the full specified test suite was run to completion with explicit pass/fail counts
quoted (one combined background invocation, not a subset, confirmed via its exit code and the
printed summary line); the `test_multi_intent.py` baseline-failure count was re-measured this
session (not assumed from the dispatch's stated number) and found identical; `ruff`'s file list
was checked against `git status --short` before invoking it to guarantee the JSON ledger was
excluded.

**Layer**: deterministic/unit only — zero LLM calls anywhere in this unit's own work (every
surface-2 probe consulted is a frozen, already-scored report file read as data via the gate's own
helpers; no live classifier or router call was made; `tests/e2e/test_read_floor_live.py`, the one
file in scope that WOULD make a live call, was confirmed `pytest.mark.llm`-gated and left
untouched/unrun).

**Denominator**: all 14/14 claimed rows checked at BEFORE (11 to-delete-covering + 3 survivors);
the 1 unexercised literal's audit covered all 5 phrasings that match its shape, not a sample; all
11 deleted-literal phrases plus both shadowed-literal candidates checked at the AFTER reabsorption
scan (13 total, not a sample); the full suite run (5186 tests) was the complete specified set in
one invocation; `git grep -l -e MEMORY_PATTERNS -e get_memory -- tests/` returned 14 files and
every one was inspected, not a sample.

## Memory & briefing surfaces referenced this session

- **Referenced**: the tenth-deletion (TRUST_PATTERNS partial) session log and git commits as the
  exact template for the gate/ledger/doc/log structure; the ninth (DISCOVERY_PATTERNS), seventh
  (STATUS_PATTERNS), and PRIORITY_PATTERNS ledger entries for the `shadowed_literals` field's
  exact prose shape (STATUS and PRIORITY both have cross-list and within-list shadowing examples
  to mirror; DISCOVERY and TRUST had none); CLAUDE.md's worktree/sign-off/subagent-dispatch rules
  (session conduct — no commits made, per dispatch); CLAUDE.md's "no LLM calls" hard rule and
  "never pass .json to ruff" rule.
- **Loaded but not referenced**: most of the skill listing (duty-cycle, mail, blog-drafting skills
  — not applicable to this coding task).
- **Wanted but not found**: nothing — the dispatch prompt, the gate script's own docstrings/code,
  and the prior PARTIAL-deletion lane logs/ledger entries were sufficient to resolve every step,
  including the unexercised-literal case the TRUST/DISCOVERY precedents hadn't needed to show.
