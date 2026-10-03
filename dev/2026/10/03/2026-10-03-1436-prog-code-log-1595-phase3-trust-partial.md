# 2026-10-03 — Coding Agent (prog), model: Sonnet 5 — #1595 Phase 3 tenth deletion (TRUST_PATTERNS, PARTIAL)

Dispatched by Lead Developer. Worktree: `/Users/xian/Development/piper-morgan-worktrees/lead`,
branch `claude/lead-cycle`. Do NOT commit (Lead commits by pathspec after review). No LLM calls, no
`gh`, no env/flag/deploy/web touches.

## Task

Tenth deletion in the #1595 Phase 3 ratchet, the FOURTH PARTIAL one: `TRUST_PATTERNS` (16
literals) in `services/intent_service/pre_classifier.py` — 15 literals go, 1 SURVIVES
(`\bwhy can'?t you\b`).

## STEP 1 — BEFORE gate + literal audit

Ran:
```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list TRUST_PATTERNS \
  --live create_reminder,create_todo,delete_todo,read_floor,read_referent,read_status,read_strategic,read_synthesis,read_temporal
```

Result (log noise stripped):
```
corpus denominator: 447 rows total = 102 claimed + 345 unclaimed

## TRUST_PATTERNS
literals: 16  |  rows claimed: 16/447
verdict: GO (partial) — 1 load-bearing literal(s) SURVIVE, deleting the other 15: ceiling 240 -> 225
  survives: r"\bwhy can'?t you\b"  <- "why can't you create issues?"

rows claimed:
  [FAIL] "why can't you create issues?" -> claim=explain_trust expected=REVIEW router=get_capabilities@0.9 verdict=REVIEW :: REVIEW-disagrees (route=get_capabilities != claim=explain_trust); expected-not-action-shaped
  [OK] "why won't you create issues for me" -> ... MATCH (expected action live via group)
  [OK] "why don't you just do it yourself" -> ... MATCH (expected action live via group)
  [OK] "why are you always cautious about this suggestion" -> claim=explain_trust expected=action:explain_suggestion router=explain_suggestion@0.95 verdict=MATCH :: MATCH on a non-live op, and the pattern mis-serves this row (claim=explain_trust != ruled action:explain_suggestion) — deleting cannot make the fallback worse; surface 2: surface 2 lands in PROVENANCE only 0/10 probe samples
  [OK] "what can't you do here" -> ... MATCH (expected action live via group)
  [OK] "what are your limits as an assistant" -> ... MATCH (expected action live via group)
  [OK] "what's the capability boundary here" -> ... MATCH (expected action live via group)
  [OK] "how well do you know me by now" -> ... MATCH (expected action live via group)
  [OK] "do you trust me with this decision" -> ... MATCH (expected action live via group)
  [OK] "how much do you trust my judgment" -> ... MATCH (expected action live via group)
  [OK] "what's our relationship like these days" -> ... MATCH (expected action live via group)
  [OK] "how do you see our relationship evolving" -> ... MATCH (expected action live via group)
  [OK] "how do we work together on this project" -> ... MATCH (expected action live via group)
  [OK] "why did you go ahead without asking" -> ... MATCH (expected action live via group)
  [OK] "why do you always ask me the same thing" -> ... MATCH (expected action live via group)
  [OK] "i didn't ask you to do that" -> ... MATCH (expected action live via group)
```
Matches the dispatch's expectation exactly (GO (partial), 1 survivor `\bwhy can'?t you\b`, ceiling
240 -> 225) — no STOP.

Confirmed independently:
- `pattern_literal_counts.total_literal_count()` → 240 (pre-deletion baseline).
- `pattern_literal_counts.per_list_literal_counts()["TRUST_PATTERNS"]` → 16.

**Unexercised-literal audit (STEP 2)**: computed via the gate's own `unexercised_literals
("TRUST_PATTERNS", lv.rows)` → **0 unexercised**. All 16 literals (15 to-delete + the 1 survivor)
are each exercised by exactly one claimed corpus row — the clean case, same shape as DISCOVERY's
ninth deletion. No `shadowed_literals`, no corpus deposits needed, no STOP.

| literal | status | evidence |
|---|---|---|
| 14 of 15 to-be-deleted literals | exercised, 1:1, live MATCH | each claims exactly one `[OK]` row, expected action live via group |
| 1 to-be-deleted literal (`\bwhy (are\|do) you (so\|being so\|always) (cautious\|careful\|conservative)\b`) | exercised, mis-serve | claims "why are you always cautious about this suggestion" as `explain_trust`, disagreeing with ruled `explain_suggestion`; router independently reaches `explain_suggestion@0.95` live; N=10 surface-2 probe does NOT land PROVENANCE (0/10) — mis-serve rule applies regardless |
| `\bwhy can'?t you\b` (survivor) | exercised | claims "why can't you create issues?" (the `[FAIL]` row) |

## STEP 3 — applied the partial deletion

`services/intent_service/pre_classifier.py`: `TRUST_PATTERNS` now exactly
`[r"\bwhy can'?t you\b"]` (1 literal), with a dated comment block recording the deletion, the gate
quote, the unexercised-literal audit (0 found), and the ceiling arithmetic. Claim branch
(`pre_classify`'s TRUST_PATTERNS if-block, checked after PROVENANCE_PATTERNS and before
INSIGHT_PULL_PATTERNS/MEMORY_PATTERNS) left untouched (still live, non-empty list). Confirmed via
`pattern_literal_counts.total_literal_count()` → 225, `per_list_literal_counts()["TRUST_PATTERNS"]`
→ 1.

## STEP 4 — reabsorption check + AFTER gate

For each of the 15 deleted-literal phrases, ran `gate.claim_for_phrase(PreClassifier, phrase)`
(both entry surfaces internally — `pre_classify_with_pattern_list` AND `detect_multiple_intents`)
against the live, post-deletion `PreClassifier`: **all 15 UNCLAIMED
(`ClaimResult(pattern_list=None, action=None, category=None, entry_surface=None)`), zero
reabsorptions.** The survivor phrase ("why can't you create issues?") remains claimed by
`TRUST_PATTERNS` itself (`ClaimResult(pattern_list='TRUST_PATTERNS', action='explain_trust',
category='trust', entry_surface='pre_classify')`).

`--all` gate: `TRUST_PATTERNS 1 1 NO-GO` (1 literal, 1 row, `[FAIL]` — expected for a partial
list's remainder). Corpus denominator: 447 = 87 claimed + 360 unclaimed (down from 102 claimed;
102 − 87 = 15, matching the deleted-row count exactly, no net reabsorption).

## STEP 5 — ceiling + ledger

`CEILINGS["pre-classifier"]` 240 → 225 in `tests/test_architecture_enforcement.py`, dated comment
block matching the established per-deletion style.

Appended the 11th `DELETED_PATTERN_LISTS` entry to `scripts/inversion_phase3_deleted_patterns.json`
via a one-off Python build script (never hand-typed): `"partial": true`, `"surviving_literals"`
(1-literal map), `"literals": 15` (deleted count), `rows_claimed_at_deletion` (15 phrases),
`verdict_report` (resolved empirically by walking `gate.PHASE3_REPORTS` in precedence order for
each claimed phrase's actual matching file, plus `gate.RouterReports.lookup`'s `source_table` to
confirm which table matched — `inversion-phase3-trust-rescore-03-2026-10-02.md` for 15 of the 16
claimed rows via `deposits-asserted`, `inversion-phase1-shadow-score-2026-09-25.md` for the
survivor via `full-review`), `expected_op_by_phrase` (15 entries: 14 `explain_trust`/
`get_capabilities`/`pull_insights`, 1 `explain_suggestion` for the mis-serve row),
`shadowed_literals: {}` (0 unexercised), `misserved_at_deletion` (1 entry — "why are you always
cautious about this suggestion": `claimed_action=explain_trust`, `ruled_destination=
explain_suggestion`, `router_route=explain_suggestion@0.95`, note following the established
STATUS/GUIDANCE/PRIORITY template), `surface2_verified_at_deletion: {}` (empty — the one row that
attempted that escape failed its N=10 probe, 0/10, and passed via the mis-serve rule instead),
`known_reabsorptions: {}` (zero found). **Reloaded with `json.load` immediately after writing** —
confirmed 11 entries, parses cleanly. Verified via `check_deleted_entry_non_regression` against
ALL 11 ledger entries (not just the new one) — all pass (`True` for every entry, confirmed by
iterating and printing each result).

## STEP 6 — test conversion, 1 file + 3 confirmed-unaffected

Ran the specified suite set, found and converted 1 file:

1. **`tests/unit/services/test_pre_classifier.py`**:
   - `test_trust_patterns` (14-phrase list, asserted every one matched TRUST and routed to
     `explain_trust`) — 13 of the 14 matched now-deleted literals (the 14th, "why can't you do
     that", matches the survivor). Renamed to `test_trust_patterns_now_unclaimed_by_surface_1`,
     dropped the survivor phrase from the list, and flipped the assertion to
     `PreClassifier.pre_classify(pattern) is None` for the remaining 13. Added
     `test_trust_survivor_literal_still_matches` to keep the "TRUST still claims explain_trust"
     coverage this file's job requires.
   - `test_memory_not_trust` — its second fixture ("how well do you know me", matched the deleted
     `\bhow (well )?do you know me\b` literal) swapped to the survivor phrase ("why can't you do
     that") — still proves a TRUST-claimed phrase doesn't collide with MEMORY_PATTERNS.
   - `test_trust_not_identity` — confirmed unaffected: its fixture ("why can't you delete my
     project") matches the survivor; test passed without modification.
   - `test_trust_still_routes_after_provenance` (7-phrase PROVENANCE-collision regression guard,
     asserted all 7 routed to TRUST) — 6 of the 7 matched now-deleted literals. Split into a
     `now_unclaimed` list (asserting `PreClassifier.pre_classify(query) is None` — confirming
     PROVENANCE's own verb list, mention/bring up/suggest/recommend/surface/raise/flag, does not
     steal these "do"/"just/go ahead"/"how well"/"what are your limits"/"always ask" phrasings —
     if any came back non-None as PROVENANCE, that would BE the regression this pin guards
     against) plus the 1 survivor query ("Why can't you help me?"), still asserted
     TRUST/`explain_trust`.

2. **`tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py`** — checked,
   NOT touched: `("TRUST", "explain_trust")`'s probe message "why can't you do that?" matches the
   surviving `\bwhy can'?t you\b` literal; confirmed unaffected by running the file directly (11
   passed).

3. **`tests/e2e/test_read_floor_live.py`** — checked, NOT touched: `pytest.mark.llm`-gated
   (skipped without `PIPER_E2E_LIVE_HEADER_KEY`), tests end-to-end router/floor dispatch for
   `explain_trust` (among others), not which literal matched at surface 1 — out of scope for a
   no-LLM-calls unit regardless.

4. **`services/intent_service/chat_pointers.py`** — checked, NOT touched. Grepped for
   `explain_trust`/`TRUST` — no `CHAT_POINTERS` entry resolves through `TRUST_PATTERNS`.

Also grepped broadly across `tests/` for TRUST-adjacent literal strings beyond the mechanical
`git grep -l TRUST_PATTERNS`, per the dispatch's explicit instruction (the DISCOVERY lane's own
precedent — `test_pre_classifier.py`'s pin was missed by a narrower search last time). Found
several hits in `tests/unit/services/trust/test_explanation_detector.py`,
`test_explanation_handler.py`, `test_outcome_classifier.py`, `test_signal_detector.py`, and
`tests/unit/services/intent_service/test_action_gate.py` — all of these exercise
`services.trust.ExplanationDetector`/`ExplanationHandler` directly (a *different*, independently
implemented matcher the `PreClassifier.TRUST_PATTERNS` comment explicitly calls out as "derived
from ExplanationDetector but simplified for pre-classification") — none reference
`PreClassifier.TRUST_PATTERNS` and none are affected by this deletion. Confirmed by running the
full suite (below) with zero new failures from any of these files.

Full suite run (`tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py`
+ `tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py` +
`tests/unit/test_inversion_phase3_surface2_floor_1595.py` +
`tests/unit/test_inversion_phase1_shadow_score_1595.py`, one combined invocation, run in
background due to runtime — 151s): **5184 passed, 1 xfailed, 0 failed, exit code 0**.

`tests/unit/services/test_multi_intent.py` (pre-existing out-of-scope failures per the dispatch,
run separately with `-o addopts="--import-mode=importlib --tb=line"`): **16 failed, 11 passed** —
identical count to the dispatch's stated baseline (16), confirming no new failures.

`ruff format`/`ruff check` run on exactly the touched `.py` files (confirmed via `git status
--short` before invoking ruff — the ledger JSON was never in the argument list): all clean, no
formatting needed this time.

## STEP 7 — docs

Appended "### Tenth deletion (2026-10-03): `TRUST_PATTERNS` (partial — 15 of 16)" to
`docs/internal/architecture/current/intent-routing-stack.md` (full BEFORE/AFTER gate quotes, the
partial rule, the one `misserved_at_deletion` row and why `surface2_verified_at_deletion` is empty
for this entry, all converted/confirmed-unaffected test files + the e2e/chat_pointers.py checks,
ceiling arithmetic). Dated entry appended to
`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

**Files touched** (no commits — Lead commits by pathspec):
`services/intent_service/pre_classifier.py`, `scripts/inversion_phase3_deleted_patterns.json`,
`tests/test_architecture_enforcement.py`, `tests/unit/test_inversion_phase3_deletion_1595.py`,
`tests/unit/services/test_pre_classifier.py`,
`docs/internal/architecture/current/intent-routing-stack.md`,
`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`, this session log.

No product code outside `pre_classifier.py`'s pattern-literal edit was changed. No `.json` file
was ever passed to ruff. No `gh`/issue tooling used (off-limits for this dispatch). No env/flag/
deploy/web touches.

## Verified how

**Method**: every gate run quoted above was executed this session against the live repo state
(not recalled); `pattern_literal_counts.total_literal_count()`/`per_list_literal_counts()` called
directly against the live, edited `PreClassifier` class before and after the edit;
`unexercised_literals`/`claim_for_phrase` run empirically for the unexercised-literal audit, the
AFTER reabsorption scan (15/15), and the survivor-row check (via
`gate.claim_for_phrase(PreClassifier, phrase)`, the real production if-chain, not a
regex-iteration shortcut); the `verdict_report` file names were resolved by walking
`gate.PHASE3_REPORTS` in its documented precedence order and matching each phrase's
`_norm_phrase()` against each file's actually-parsed rows (never guessed from a filename),
cross-checked against `RouterReports.lookup`'s `source_table` label; the ledger entry was built
via a one-off Python script and reloaded with `json.load` immediately (never trusted a clean write
alone); `check_deleted_entry_non_regression` was run against all 11 real ledger entries, not just
the new one, with each entry's boolean result printed individually; the full specified test suite
was run to completion with explicit pass/fail counts quoted (one combined background invocation,
not a subset); the `test_multi_intent.py` baseline-failure count was re-measured this session
(not assumed from the dispatch's stated number) and found identical; `ruff`'s file list was
checked against `git status --short` before invoking it to guarantee the JSON ledger was excluded.

**Layer**: deterministic/unit only — zero LLM calls anywhere in this unit's own work (every
surface-2 probe consulted is a frozen, already-scored report file read as data via the gate's own
helpers; no live classifier or router call was made; `tests/e2e/test_read_floor_live.py`, the one
file in scope that WOULD make a live call, was confirmed `pytest.mark.llm`-gated and left
untouched/unrun).

**Denominator**: all 16/16 claimed rows checked at BEFORE (15 to-delete + 1 survivor); all 15/15
deleted-literal phrases checked at the AFTER reabsorption scan (not a sample); the full suite run
(5184 tests) was the complete specified set in one invocation, not a subset; all 11 ledger entries
checked by the non-regression test, not just entry 11; the broader `tests/` grep for TRUST-adjacent
literal strings (beyond the mechanical `git grep -l TRUST_PATTERNS`) covered every hit returned,
not a sample.

## Memory & briefing surfaces referenced this session

- **Referenced**: the ninth-deletion (DISCOVERY_PATTERNS partial) session log and git commits as
  the exact template for ledger-entry shape, the unexercised-literal audit procedure, and the
  "NEVER pass .json to ruff" / "pins referencing deleted literals are CONVERTED, never deleted"
  conventions; the seventh (STATUS_PATTERNS) and eighth (GUIDANCE_PATTERNS) partial ledger entries
  for the `misserved_at_deletion`/`surface2_verified_at_deletion` field shapes, since DISCOVERY's
  entry had neither populated and TRUST needed one; CLAUDE.md's worktree/sign-off/subagent-dispatch
  rules (session conduct — no commits made, per dispatch); CLAUDE.md's "no LLM calls" hard rule.
- **Loaded but not referenced**: most of the skill listing (duty-cycle, mail, blog-drafting skills
  — not applicable to this coding task).
- **Wanted but not found**: nothing — the dispatch prompt, the gate script's own docstrings/code,
  and the prior PARTIAL-deletion lane logs/ledger entries were sufficient to resolve every step
  without further lookups.
