# 2026-10-02 — Coding Agent (prog), model: Sonnet 5 — #1595 Phase 3 eighth deletion (GUIDANCE_PATTERNS, PARTIAL)

Dispatched by Lead Developer. Worktree: `/Users/xian/Development/piper-morgan-worktrees/lead`,
branch `claude/lead-cycle`. Do NOT commit (Lead commits by pathspec after review). No LLM calls, no
`gh`, no env/flag/deploy/web touches.

## Task

Eighth deletion in the #1595 Phase 3 ratchet, the SECOND PARTIAL one: `GUIDANCE_PATTERNS` (21
literals) in `services/intent_service/pre_classifier.py` — 18 literals go, 3 SURVIVE
(`\bsetup.*projects?\b`, `\bset up.*projects?\b`, `\bset up.*portfolio\b`).

This resolves an earlier same-day STOP (`dev/2026/10/02/2026-10-02-1030-prog-code-log-1595-phase3-
deletion-guidance.md`, a prior lane's FULL-tombstone attempt): with GUIDANCE_PATTERNS fully gone, 4
phrases were reabsorbed by STATUS_PATTERNS' then-live `\bmy projects\b`/`\bmy portfolio\b` literals
into a disagreeing wrong answer. STATUS_PATTERNS' own seventh deletion (same day, earlier) has
since removed both literals; this dispatch's PARTIAL form additionally keeps the collision's
load-bearing literals alive regardless.

## STEP 1 — BEFORE gate + literal audit

Ran:
```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list GUIDANCE_PATTERNS \
  --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo
```

Result:
```
corpus denominator: 385 rows total = 77 claimed + 308 unclaimed

## GUIDANCE_PATTERNS
literals: 21  |  rows claimed: 21/385
verdict: GO (partial) — 3 load-bearing literal(s) SURVIVE, deleting the other 18: ceiling 277 -> 259
  survives: r"\bsetup.*projects?\b"  <- 'I need to setup my projects'
  survives: r"\bset up.*projects?\b"  <- 'I want to set up my projects'
  survives: r"\bset up.*portfolio\b"  <- "I'd like to set up my portfolio"
```
18/21 claimed rows `[OK]`, 3 `[FAIL]` (the 3 survivors — each "MATCH on a NON-LIVE op ... surface 2
lands in GUIDANCE only 0/10 probe samples"). Matches the dispatch's expectation exactly.

Confirmed independently:
- `pattern_literal_counts.total_literal_count()` → 277 (pre-deletion baseline, matches
  `tests/test_architecture_enforcement.py` ceiling constant before edit).
- `pattern_literal_counts.per_list_literal_counts()["GUIDANCE_PATTERNS"]` → 21.

**Reachability audit (the REACHABILITY RULE — real if-chain, not within-list)**: for each of the
21 claimed phrases, ran `PreClassifier._first_pattern_match(cleaned_phrase, GUIDANCE_PATTERNS)` —
all 21 literals matched exactly one claimed phrase each (1:1 mapping, no literal unexercised). Then
confirmed via the gate's own `claim_for_phrase` (which threads the REAL if-chain:
`pre_classify_with_pattern_list` then `detect_multiple_intents`) that all 21 rows in the gate's
"## GUIDANCE_PATTERNS" report section are grouped there because `claim.pattern_list ==
"GUIDANCE_PATTERNS"` for every one of them (`build_census`'s `by_list[claim.pattern_list].rows.
append(rec)` — the grouping IS the real if-chain attribution, not a within-list check). Result: **no
cross-list shadowing found for any of the 18 to-be-deleted literals; no corpus deposit needed.**

## STEP 2 — applied the partial deletion

`services/intent_service/pre_classifier.py`: `GUIDANCE_PATTERNS` now exactly the 3 survivors, each
with a one-line comment naming the corpus row it carries and the probe proving it EXECUTION not
GUIDANCE (`...-set4.md`, both legs, 10/10). A dated comment block above the list records the full
deletion rationale, the reachability audit, the prior-STOP resolution, and the "set up / configure
/ connect integrations" disposition (6 of the 18 deleted literals claimed CONNECTOR-flavored rows;
`INTEGRATION_CONNECT_PATTERNS` does not claim any of them — confirmed, no reassignment needed).
Claim branch and the `INTEGRATION_CONNECT_PATTERNS` skip-guard (`patterns is
PreClassifier.GUIDANCE_PATTERNS and connect_claimed`) left live (non-empty, still-real check).

Confirmed via `pattern_literal_counts.total_literal_count()` → 259,
`per_list_literal_counts()["GUIDANCE_PATTERNS"]` → 3.

**Gate re-run post-edit**: `GO (partial) — 3 load-bearing literal(s) SURVIVE, deleting the other 0:
ceiling 259 -> 259` — all 3 survivors still claimed, 0 further deletion possible (expected).

## STEP 3 — AFTER checks

For each of the 18 deleted-literal phrases, ran `claim_for_phrase` (both entry surfaces) against
the live, post-deletion `PreClassifier`: **all 18 UNCLAIMED, zero reabsorptions.**

All 3 survivor rows ("I need to setup my projects", "I want to set up my projects", "I'd like to
set up my portfolio") still claimed by `GUIDANCE_PATTERNS` itself.

**The four setup phrases, explicit check**:
- "I need to setup my projects" → `GUIDANCE_PATTERNS`, `get_contextual_guidance` (survivor row, as
  expected)
- "I want to set up my projects" → `GUIDANCE_PATTERNS`, `get_contextual_guidance` (survivor row)
- "I'd like to set up my portfolio" → `GUIDANCE_PATTERNS`, `get_contextual_guidance` (survivor row)
- "how do I configure my projects" → **`None`, `None`, `None` — UNCLAIMED.** Confirmed: not a
  survivor row (its literal `\bconfigure.*projects?\b` is one of the 18 deleted); `STATUS_PATTERNS`'
  `\bmy projects\b` is gone since the seventh deletion, so nothing reabsorbs it. Falls through to
  the LLM classifier (surface 2), which the frozen probe shows lands it in GUIDANCE 10/10 anyway.
  **Nothing claims it — exactly as the dispatch predicted.**

## STEP 4 — `--all` gate

`GUIDANCE_PATTERNS 3 3 NO-GO` (3 literals, 3 rows, all `[FAIL]` — expected for a partial list's
remainder). Corpus denominator: 385 = 59 claimed + 326 unclaimed (down from 77 claimed before this
deletion; 77 − 59 = 18, the full deleted-row count, no partial reabsorption to net out).
`STATUS_PATTERNS` unaffected: still `4 4 NO-GO`.

## STEP 5 — ceiling + ledger

`CEILINGS["pre-classifier"]` 277 → 259 in `tests/test_architecture_enforcement.py`, with a dated
arithmetic comment block matching the established per-deletion style.

Appended the 9th `DELETED_PATTERN_LISTS` entry to `scripts/inversion_phase3_deleted_patterns.json`
via a one-off Python build script (`/private/tmp/.../scratchpad/build_guidance_ledger_entry.py`,
never hand-typed): `"partial": true`, `"surviving_literals"` (3-literal map), `"literals": 18`
(deleted count), `rows_claimed_at_deletion` (18 phrases), `expected_op_by_phrase` (18 entries, 3
distinct ops: `get_contextual_guidance` ×16, `get_top_priority` ×1, `greeting` ×1),
`shadowed_literals: {}` (none found), `misserved_at_deletion` (1 entry: "just getting started
here"), `surface2_verified_at_deletion` (17 entries, probe reports/samples/served pulled
programmatically from the gate's own `SURFACE2_FLOOR_PROBES` list — never hand-typed),
`known_reabsorptions: {}` (zero found). **Reloaded with `json.load` immediately after writing** —
confirmed 9 entries, parses cleanly. Never passed the `.json` file to ruff (verified via `git status
--porcelain | grep '\.py$'` before invoking ruff — the ledger file was not in the list).

Verified via `check_deleted_entry_non_regression` against the entry (and all 9 ledger entries via
the real test): all pass.

## STEP 6 — test conversion + full suite

Ran the specified suite set — one unexpected break beyond the pinned ledger/count tests, found and
converted (not pre-announced in the dispatch, since it required running the suite to surface):

1. **`tests/unit/services/intent_service/test_setup_routing_814.py`** —
   `test_help_me_get_started_matches_guidance_patterns` asserted `"help me get started"` (matches
   the now-deleted `\bget started\b`) still matches `GUIDANCE_PATTERNS`. Renamed to
   `test_help_me_set_up_my_portfolio_matches_guidance_patterns`, fixture swapped to "help me set up
   my portfolio" (matches the surviving `\bset up.*portfolio\b` literal, confirmed live this
   session) — the test's actual job (GUIDANCE_PATTERNS still fires on an onboarding-setup phrasing)
   is unchanged; only the specific literal exercised moved to one that survived.

2. **`tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py`** — the harder
   one. `("GUIDANCE", "get_contextual_guidance")`'s probe message "any guidance?" (matched the
   deleted `\bguidance\b`) could NOT simply be swapped to a surviving literal: tried "help me set up
   my projects" first (matches `\bset up.*projects?\b`, confirmed via `pre_classify_with_pattern_
   list`), but step 3 of the ratchet failed — `crossings == 0` where the pair's registered `SPENDS`
   membership requires `crossings > 0`. Root cause, confirmed by reading
   `CanonicalHandlers._handle_guidance_query` / `_detect_setup_request`: ALL 3 surviving
   GUIDANCE_PATTERNS literals require BOTH a setup verb ("set up"/"setup") AND a
   "project(s)"/"portfolio" noun — **exactly** the shape `_detect_setup_request`'s "projects" topic
   checks for (same verb list: `["set up", "setup", "configure"]`, same noun list: `["project",
   "projects", "portfolio"]`). So every message reachable via step-1 pre_classify for this pair is
   now STRUCTURALLY guaranteed to route to `_handle_project_setup_request` (the non-spending
   onboarding branch), never the generic/spending guidance-formatting branch "any guidance?" used to
   exercise. This is not a guess — it's a direct read of the handler's dispatch logic plus an
   empirical confirmation (0 chokepoint crossings). Resolution: removed the pair from
   `PAIR_MESSAGES` with a dated NOTE block, following the file's own established idiom for the
   TEMPORAL_PATTERNS (2026-10-01) and PRIORITY_PATTERNS (2026-10-02) removals — explicitly flagged
   as discovered work for Lead/Arch/CXO, NOT resolved here: the generic/spending branch still exists
   and still spends for LLM-classifier-routed messages without a setup phrase; only this harness's
   deterministic step-1 drive can no longer pose the pair's spending behavior. This is NOT a
   product-code change — same idiom already used twice in this file for exactly this situation.

3. **`services/intent_service/chat_pointers.py`** — checked, **NOT touched**. Grepped every
   GUIDANCE-destination `CHAT_POINTERS` entry; all use "connect my X" phrasings. Confirmed via
   `pre_classify_with_pattern_list("connect my github")` → `(GUIDANCE, get_contextual_guidance,
   'INTEGRATION_CONNECT_PATTERNS')` — none resolve through `GUIDANCE_PATTERNS` directly, so none of
   this deletion's 18 literals back any pointer's verified utterance. Reported per the dispatch's
   instruction, no product change needed.

**Full suite run** (`tests/unit/services/intent_service/` + `tests/unit/services/
test_pre_classifier.py` + `tests/unit/test_inversion_phase3_deletion_1595.py` +
`tests/unit/test_inversion_phase3_surface2_floor_1595.py` + `tests/unit/
test_inversion_phase1_shadow_score_1595.py` + `tests/test_architecture_enforcement.py` + the #1897
spend-free shape pin): **5175 passed, 1 xfailed, 0 failed** — run twice (once before `ruff`, once
after), identical both times.

`tests/unit/test_inversion_phase3_deletion_1595.py` alone: 41 passed (ledger-count pin renamed
`test_real_ledger_has_the_first_nine_deletions`, now asserts both STATUS and GUIDANCE partial
entries; new `test_guidance_patterns_now_claims_three_rows` pin added; module docstring updated
with a GUIDANCE paragraph mirroring the existing STATUS one).

`ruff format` + `ruff check --fix` on exactly the touched `.py` files (confirmed via `git status
--porcelain | grep '\.py$'` BEFORE invoking ruff — the ledger JSON was never in the argument list):
"5 files left unchanged" / "All checks passed!". Reloaded the ledger JSON with `json.load`
immediately after (9 entries, parses cleanly) — no repeat of the prior lane's ruff/JSON corruption.

`scripts/run-sweep.sh ratchets`: **1 PRE-EXISTING unrelated failure**
(`test_todo_marker_ratchet`, count 36 vs frozen ceiling 35) — same failure the fifth/sixth/seventh
deletions found and left; confirmed unrelated (no file this unit touched is in its scan scope).
Reported, not fixed, per the dispatch.

## STEP 7 — docs

Appended "### Eighth deletion (2026-10-02): `GUIDANCE_PATTERNS` (partial — 18 of 21)" to
`docs/internal/architecture/current/intent-routing-stack.md` (full BEFORE/AFTER gate quotes, the
partial rule, the prior-STOP resolution with full mechanism, the "setup/configure/connect
integrations" disposition, both converted test files + the chat_pointers.py check, ceiling
arithmetic). Dated entry appended to
`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

## Files touched (no commits — Lead commits by pathspec)

- `services/intent_service/pre_classifier.py` (GUIDANCE_PATTERNS partial deletion)
- `scripts/inversion_phase3_deleted_patterns.json` (9th ledger entry)
- `tests/test_architecture_enforcement.py` (ceiling 277 → 259)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (ledger-count pin rename + GUIDANCE
  assertions; new `test_guidance_patterns_now_claims_three_rows`; module docstring)
- `tests/unit/services/intent_service/test_setup_routing_814.py` (fixture rename + swap)
- `tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py` (pair removed +
  NOTE)
- `docs/internal/architecture/current/intent-routing-stack.md` ("Eighth deletion" subsection)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (dated entry)
- this session log

No product code outside `pre_classifier.py`'s pattern-literal edit was changed. No `.json` file was
ever passed to ruff.

## Verified how

**Method**: every gate run quoted above was executed this session against the live repo state (not
recalled); `pattern_literal_counts.total_literal_count()`/`per_list_literal_counts()` called
directly against the live, edited `PreClassifier` class before and after the edit;
`claim_for_phrase`/`pre_classify_with_pattern_list` run empirically for the reachability audit, all
21 claimed-phrase checks, the AFTER reabsorption scan (18/18), and the four-setup-phrase check; the
`test_spend_free_canonical_ratchet_1818.py` root cause was confirmed by both reading
`_detect_setup_request`'s source and empirically measuring 0 chokepoint crossings for a candidate
replacement message before deciding not to use it; the ledger entry was built via a one-off Python
script and reloaded with `json.load` immediately (never trusted a clean write alone); the full test
suite was run twice end-to-end (before/after ruff) with explicit pass/fail counts quoted both times,
not a subset; `ruff`'s file list was checked against `git status --porcelain` before invoking it to
guarantee the JSON ledger was excluded.

**Layer**: deterministic/unit only — zero LLM calls anywhere in this unit's own work (every
surface-2 probe consulted is a frozen, already-scored report file read as data via the gate's own
`_surface2_probe_rows`/`report_served`/`parse_report` helpers; no live classifier or router call was
made).

**Denominator**: all 21/21 claimed rows checked at BEFORE (18 to-delete + 3 survivors); all 18/18
deleted-literal phrases checked at the AFTER reabsorption scan (not a sample); the full suite run
(5175 tests) was the complete specified set, not a subset; the ratchet sweep (`scripts/run-sweep.sh
ratchets`) covers its own full fixed scan scope, 1 of 73 failing (pre-existing, unrelated).

## Memory & briefing surfaces referenced this session

- **Referenced**: the prior GUIDANCE lane's session log (`...-1030-prog-code-log-1595-phase3-
  deletion-guidance.md`) as the exact source of the earlier STOP this dispatch resolves; the
  seventh-deletion (STATUS_PATTERNS partial) session log and its ledger/doc entries as the template
  for ledger-entry shape, comment-block style, and the "NEVER pass .json to ruff" lesson; CLAUDE.md's
  worktree/sign-off/subagent-dispatch rules (session conduct — no commits made, per dispatch);
  CLAUDE.md's Discovered Work Discipline (informed how the test_spend_free_canonical_ratchet_1818.py
  finding was framed — flagged for Lead/Arch/CXO rather than silently resolved, though filing a
  `bd create` tracking issue was out of scope since `gh`/issue tooling was off-limits for this
  dispatch; reported in this log and the doc entries instead).
- **Loaded but not referenced**: most of the skill listing (duty-cycle, mail, blog-drafting skills —
  not applicable to this coding task); the STATUS_PATTERNS seventh-deletion lane's full "Session
  Resumed" STOP/unblock narrative (read for template purposes only, not re-applied — this lane's own
  reachability audit found zero cross-list shadowing, so no equivalent STOP/unblock sequence was
  needed here).
- **Wanted but not found**: nothing — the dispatch prompt, the gate script's own docstrings/code, and
  the prior GUIDANCE-lane log were sufficient to resolve every step without further lookups.
