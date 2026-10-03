# 2026-10-03 — Coding Agent (prog), model: Sonnet 5 — #1595 Phase 3 ninth deletion (DISCOVERY_PATTERNS, PARTIAL)

Dispatched by Lead Developer. Worktree: `/Users/xian/Development/piper-morgan-worktrees/lead`,
branch `claude/lead-cycle`. Do NOT commit (Lead commits by pathspec after review). No LLM calls, no
`gh`, no env/flag/deploy/web touches.

## Task

Ninth deletion in the #1595 Phase 3 ratchet, the THIRD PARTIAL one: `DISCOVERY_PATTERNS` (20
literals) in `services/intent_service/pre_classifier.py` — 19 literals go, 1 SURVIVES
(`\bneed\s*help\b`).

## STEP 1 — BEFORE gate + literal audit

Ran:
```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list DISCOVERY_PATTERNS \
  --live create_reminder,create_todo,delete_todo,read_floor,read_referent,read_status,read_strategic,read_synthesis,read_temporal
```

Result:
```
corpus denominator: 447 rows total = 121 claimed + 326 unclaimed

## DISCOVERY_PATTERNS
literals: 20  |  rows claimed: 20/447
verdict: GO (partial) — 1 load-bearing literal(s) SURVIVE, deleting the other 19: ceiling 259 -> 240
  survives: r"\bneed\s*help\b"  <- 'I need help understanding something'
```
19/20 claimed rows `[OK]` (18 MATCH + 1 REVIEW-agrees, "what can you do?"), 1 `[FAIL]` (the
survivor: `MISMATCH (route=CLARIFY != expected action:get_capabilities); the pattern is the live
path for this phrase — router did not name an operation (route=CLARIFY); surface 2 names
get_capabilities only 0/10 probe samples`). Matches the dispatch's expectation exactly — no STOP.

Confirmed independently:
- `pattern_literal_counts.total_literal_count()` → 259 (pre-deletion baseline).
- `pattern_literal_counts.per_list_literal_counts()["DISCOVERY_PATTERNS"]` → 20.

**Unexercised-literal audit (STEP 2)**: computed via the gate's own `unexercised_literals
("DISCOVERY_PATTERNS", lv.rows)` — **0 unexercised**. All 20 literals (19 to-delete + the 1
survivor) are each exercised by exactly one claimed corpus row. No literal needed a reachability
check through the real if-chain (`pre_classify_with_pattern_list`) because none was unexercised in
the first place — the clean case, unlike STATUS's 4 unexercised-but-shadowed literals or GUIDANCE's
reachability audit. No `shadowed_literals`, no corpus deposits needed, no STOP.

| literal | status | evidence |
|---|---|---|
| all 19 to-be-deleted literals | exercised, 1:1 | each claims exactly one of the 19 `[OK]` rows via `_first_pattern_match` |
| `\bneed\s*help\b` (survivor) | exercised | claims "I need help understanding something" (the `[FAIL]` row) |

## STEP 3 — applied the partial deletion

`services/intent_service/pre_classifier.py`: `DISCOVERY_PATTERNS` now exactly
`[r"\bneed\s*help\b"]` (1 literal), with a dated comment block recording the deletion, the gate
quote, the unexercised-literal audit (0 found), and the ceiling arithmetic. Claim branch (`pre_
classify`'s DISCOVERY_PATTERNS if-block, ~line 1210, checked before IDENTITY) left untouched (still
live, non-empty list). Confirmed via `pattern_literal_counts.total_literal_count()` → 240,
`per_list_literal_counts()["DISCOVERY_PATTERNS"]` → 1.

## STEP 4 — reabsorption check + AFTER gate

For each of the 19 deleted-literal phrases, ran `claim_for_phrase` (both entry surfaces —
`pre_classify_with_pattern_list` AND `detect_multiple_intents`) against the live, post-deletion
`PreClassifier`: **all 19 UNCLAIMED, zero reabsorptions.** The survivor phrase ("I need help
understanding something") remains claimed by `DISCOVERY_PATTERNS` itself
(`ClaimResult(pattern_list='DISCOVERY_PATTERNS', action='get_capabilities', category='discovery',
entry_surface='pre_classify')`).

`--all` gate: `DISCOVERY_PATTERNS 1 1 NO-GO` (1 literal, 1 row, `[FAIL]` — expected for a partial
list's remainder). Corpus denominator: 447 = 102 claimed + 345 unclaimed (down from 121 claimed;
121 − 102 = 19, matching the deleted-row count exactly, no net reabsorption).

## STEP 5 — ceiling + ledger

`CEILINGS["pre-classifier"]` 259 → 240 in `tests/test_architecture_enforcement.py`, dated comment
block matching the established per-deletion style.

Appended the 10th `DELETED_PATTERN_LISTS` entry to `scripts/inversion_phase3_deleted_patterns.json`
via a one-off Python build script (never hand-typed): `"partial": true`, `"surviving_literals"`
(1-literal map), `"literals": 19` (deleted count), `rows_claimed_at_deletion` (19 phrases),
`verdict_report` (resolved empirically via `RouterReports.lookup`'s `source_table` for every
claimed phrase — `inversion-phase1-shadow-score-2026-09-25.md` for "what can you do?",
`inversion-phase3-discovery-rescore-02-2026-10-02.md`, the newest DISCOVERY-specific report in
`PHASE3_REPORTS`, for the other 19), `expected_op_by_phrase` (19 entries, all `get_capabilities`),
`shadowed_literals: {}`, `misserved_at_deletion: {}`, `surface2_verified_at_deletion: {}` (all three
empty — every deleted row passed via a live MATCH/REVIEW-agrees, not a surface-2 floor probe or a
mis-serve licence), `known_reabsorptions: {}` (zero found). **Reloaded with `json.load` immediately
after writing** — confirmed 10 entries, parses cleanly. Verified via
`check_deleted_entry_non_regression` against ALL 10 ledger entries (not just the new one) — all
pass.

## STEP 6 — test conversion, 4 files

Ran the specified suite set, found and converted 4 broken files:

1. **`tests/unit/services/intent_service/test_discovery_intent.py`** — the 16-phrase
   parametrized `test_discovery_patterns_match` asserted every listed capability-query phrasing
   still matched a `DISCOVERY_PATTERNS` literal and routed to DISCOVERY; all 16 matched now-deleted
   literals. Renamed to `test_discovery_patterns_now_unclaimed_by_surface_1` and flipped the
   assertion to `PreClassifier.pre_classify(message) is None` (unclaimed, not misrouted — no claim
   about surface-2/LLM-classifier behavior for these exact strings, since that would need a live
   call this suite doesn't make). Added `test_discovery_survivor_literal_still_matches` to keep the
   "DISCOVERY still claims get_capabilities" coverage this file's job requires.
   `test_discovery_before_identity_precedence`'s fixture ("what can you do for me", matched the
   same deleted literal) swapped to "I need help understanding something" — still proves DISCOVERY
   is checked before IDENTITY (confirmed live).

2. **`tests/unit/services/intent_service/test_setup_routing_814.py`** —
   `test_what_can_you_do_still_routes_to_discovery` asserted `"what can you do"` matches some
   `DISCOVERY_PATTERNS` literal via direct regex iteration; the literal is gone. Fixture swapped to
   "I need help understanding something" (matches the survivor) — test's actual job (DISCOVERY_
   PATTERNS still fires on a capability/help phrasing) unchanged.

3. **`tests/unit/services/intent_service/test_preclaim_shadow.py`** — the file's canonical
   DISCOVERY-claimed fixture, the literal string `"what can you do?"`, appears 12 times across all
   5 pins (default-off byte-identical, sampled-on, fail-open, pattern-list identity threading,
   the threading-sibling spot-check) — every one relies on surface 1 claiming it deterministically
   (several via `explosive_router`, which asserts the router is NEVER touched). Confirmed the
   actual failure mode first: with the literal gone, `clf.classify("what can you do?")` falls all
   the way through to a REAL (unmocked) LLM-classifier path and raises
   `ContainerNotInitializedError` inside `self.llm.complete(...)` — not the explosive router's
   `AssertionError` — because `classifier.py`'s `self.llm` property resolves via
   `ServiceContainer.get_service("llm")` before any router call. This is exactly the "no LLM calls"
   hazard the dispatch warned about, caused by production code attempting a live classifier path,
   not by me calling one. Fixed by swapping all 12 occurrences (plus the module docstring and one
   prose comment) to "I need help understanding something" (matches the survivor, confirmed mapping
   to the same `DISCOVERY_PATTERNS`/`get_capabilities` claim) — every pin's actual point is
   unaffected; only the literal exercised moved to the one that survived. (One self-correction:
   my added docstring note used un-escaped `\b`/`\s` in a non-raw triple-quoted string, which ruff
   caught as `DeprecationWarning: invalid escape sequence` on the next pytest run — fixed by
   doubling the backslashes, re-verified clean.)

4. **`tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py`** —
   `("DISCOVERY", "get_capabilities")`'s probe message "what can you do?" (matched the deleted
   literal) swapped to "I need help understanding something". Unlike the eighth deletion's
   GUIDANCE pair (which had to be REMOVED because its only surviving literals structurally forced a
   different, non-spending handler branch), this swap needed no removal: `get_capabilities`'s
   handler flow doesn't depend on which literal matched it, so the pair still crosses the spend
   chokepoint exactly as before — confirmed empirically (`crossings > 0`, same as the original
   fixture) — `DISCOVERY`/`get_capabilities` stays in `SPENDS`, unaffected.

5. **`services/intent_service/chat_pointers.py`** — checked, **NOT touched**. Grepped for
   `get_capabilities`/`DISCOVERY` — no `CHAT_POINTERS` entry resolves through `DISCOVERY_PATTERNS`.

Full suite run (`tests/unit/services/intent_service/` + `tests/test_architecture_enforcement.py`,
run in background due to runtime): **5072 passed, 1 xfailed, 0 failed, exit code 0**. Plus
`tests/unit/test_inversion_phase3_deletion_1595.py` + `tests/unit/test_inversion_phase3_surface2_
floor_1595.py` + `tests/unit/test_inversion_phase1_shadow_score_1595.py`: **77 passed**. The
"#1897 spend-free shape pin" referenced in the dispatch is covered inside the `tests/unit/services/
intent_service/` run above (`test_inversion_multi_intent_unit4_1595.py` etc., all under that
directory) — the genuinely-LLM-spending `tests/e2e/test_1897_two_part_turn_live.py` (marked
`pytest.mark.llm`, requires a live header key) was correctly identified as out of scope and not
run.

`ruff format`/`ruff check` run on exactly the touched `.py` files (confirmed via `git status
--short` before invoking ruff — the ledger JSON was never in the argument list): all clean (one
file, `test_preclaim_shadow.py`, needed `ruff format` for the new docstring block; re-verified
clean + tests re-passing after).

## STEP 7 — docs

Appended "### Ninth deletion (2026-10-03): `DISCOVERY_PATTERNS` (partial — 19 of 20)" to
`docs/internal/architecture/current/intent-routing-stack.md` (full BEFORE/AFTER gate quotes, the
partial rule, the unexercised-literal audit, why no `surface2_verified_at_deletion`/
`misserved_at_deletion` entries were needed this time — the clean "every row is a live MATCH"
case — all 4 converted test files + the chat_pointers.py check, ceiling arithmetic). Dated entry
appended to `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

**Files touched** (no commits — Lead commits by pathspec):
`services/intent_service/pre_classifier.py`, `scripts/inversion_phase3_deleted_patterns.json`,
`tests/test_architecture_enforcement.py`, `tests/unit/test_inversion_phase3_deletion_1595.py`,
`tests/unit/services/intent_service/test_discovery_intent.py`, `tests/unit/services/intent_service/
test_setup_routing_814.py`, `tests/unit/services/intent_service/test_preclaim_shadow.py`,
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
`claim_for_phrase`/`pre_classify_with_pattern_list` run empirically for the unexercised-literal
audit, the AFTER reabsorption scan (19/19), and the survivor-row check; the `verdict_report` file
names were resolved by calling `RouterReports.lookup` directly (never guessed) and cross-checked
against the actual report file contents via `grep`; the `ContainerNotInitializedError` root cause
in `test_preclaim_shadow.py` was confirmed by reading the actual traceback (not assumed) before
deciding on the fix; the ledger entry was built via a one-off Python script and reloaded with
`json.load` immediately (never trusted a clean write alone); `check_deleted_entry_non_regression`
was run against all 10 real ledger entries, not just the new one; the full test suite was run to
completion with explicit pass/fail counts quoted (not a subset); `ruff`'s file list was checked
against `git status --short` before invoking it to guarantee the JSON ledger was excluded.

**Layer**: deterministic/unit only — zero LLM calls anywhere in this unit's own work (every
surface-2 probe consulted is a frozen, already-scored report file read as data via the gate's own
`_surface2_probe_rows`/`report_served`/`parse_report` helpers; no live classifier or router call
was made; the one place production code attempted a live LLM path — `test_preclaim_shadow.py`'s
pre-fix state — was caught and fixed, not run to completion).

**Denominator**: all 20/20 claimed rows checked at BEFORE (19 to-delete + 1 survivor); all 19/19
deleted-literal phrases checked at the AFTER reabsorption scan (not a sample); the full suite runs
(5072 + 77 = 5149 tests across the two invocations) were the complete specified sets, not a
subset; all 10 ledger entries checked by the non-regression test, not just entry 10.

## Memory & briefing surfaces referenced this session

- **Referenced**: the seventh-deletion (STATUS_PATTERNS partial) and eighth-deletion (GUIDANCE_
  PATTERNS partial) session logs as the exact templates for ledger-entry shape, comment-block
  style, the "NEVER pass .json to ruff" lesson, and the "pins referencing deleted literals are
  CONVERTED, never deleted" convention; their corresponding git commits (`73a40f7cbe`/`ee498077f8`
  for seventh, `1a16222dbb` for eighth) read via `git show --stat` + full diffs per the dispatch's
  explicit instruction; CLAUDE.md's worktree/sign-off/subagent-dispatch rules (session conduct — no
  commits made, per dispatch); CLAUDE.md's "no LLM calls" hard rule (directly informed how the
  `test_preclaim_shadow.py` `ContainerNotInitializedError` was handled — fixed the fixture rather
  than letting the suite attempt a live call).
- **Loaded but not referenced**: most of the skill listing (duty-cycle, mail, blog-drafting skills
  — not applicable to this coding task); the `read_floor` rail-entry doc section was read for
  context (confirming `get_capabilities` is a live op) and IS referenced in the routing-stack doc
  addition, so not actually unused — no further unused surfaces to report beyond the skill
  listing.
- **Wanted but not found**: nothing — the dispatch prompt, the gate script's own docstrings/code,
  and the two prior PARTIAL-deletion lane logs were sufficient to resolve every step without
  further lookups.
