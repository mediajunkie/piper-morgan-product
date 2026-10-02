# 2026-10-02 — Coding Agent (prog), Sonnet — #1595 Phase 3 seventh deletion (STATUS_PATTERNS, PARTIAL)

Dispatched by Lead Developer. Repo: `/Users/xian/Development/piper-morgan-worktrees/lead`, branch `claude/lead-cycle`. Do NOT commit (Lead commits by pathspec after review). No LLM calls.

## Task

Seventh deletion in the #1595 Phase 3 deletion ratchet, and the FIRST PARTIAL one: `STATUS_PATTERNS`
(56 literals) — 52 go, 4 survive (`\bnext milestone\b`, `\bcurrent work\b`, `\bproject overview\b`,
`\bproject landscape\b`).

## STEP 1 — BEFORE gate + literal audit

Ran:
```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list STATUS_PATTERNS \
  --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo
```

Result: `GO (partial) — 4 load-bearing literal(s) SURVIVE, deleting the other 52: ceiling 329 -> 277`,
with the 4 survivors exactly matching the dispatch prompt's named set, each with a `[FAIL]` row in the
`rows claimed:` listing (56 rows total: 52 `[OK]`, 4 `[FAIL]` = the 4 survivors). Full verbatim output
captured (63 lines, `corpus denominator: 385 rows total = 125 claimed + 260 unclaimed` through the last
claimed row).

Confirmed independently:
- `pattern_literal_counts.total_literal_count()` → 329 (matches ceiling constant
  `tests/test_architecture_enforcement.py:2305` `"pre-classifier": 329`).
- `pattern_literal_counts.per_list_literal_counts()["STATUS_PATTERNS"]` → 56.
- `PreClassifier.STATUS_PATTERNS` → 56 literals (programmatic read, not scraped from source text —
  avoids counting the two "# Removed:" comment-literals at the old lines 270/293, which a naive regex
  scrape over the raw file text picks up as 58).

**Literal→corpus-row audit** (the gate only prints "needs a corpus row" on a full GO, not a partial
one — computed it myself per the dispatch prompt, calling `unexercised_literals("STATUS_PATTERNS",
lv.rows)` the same way the gate's own `render_list_report` does, then filtering out the 4 survivor
literals from the result):

4 of the 56 literals are **unexercised by any corpus row claimed by STATUS_PATTERNS**:
- `\bmy current work\b`
- `\bwhat'?s the (?:next|upcoming) milestone\b`
- `\bmilestone status\b`
- `\bmilestone progress\b`

All 4 are among the **52 literals scheduled for deletion** (none is a survivor).

Per-literal reachability check (ran `PreClassifier._first_pattern_match` against `STATUS_PATTERNS` in
list order — the same call `unexercised_literals`/`load_bearing_literals` make, no new matching logic):

1. **`\bmy current work\b`** — **PROVABLY SHADOWED**. `\bcurrent work\b` (a SURVIVOR, list index 3,
   earlier than `\bmy current work\b` at index 13) matches the substring "current work" inside "my
   current work" (word boundary before 'c': preceded by a space; word boundary after 'k': end of
   string). Verified directly: `PreClassifier._first_pattern_match("my current work",
   STATUS_PATTERNS)` returns `\bcurrent work\b`, never reaching index 13. Since `\bcurrent work\b`
   survives (stays in the list, in the same relative position ahead of where `\bmy current work\b`
   would have been), this literal is unreachable both now and after the partial deletion — safe to
   delete with zero behavior change. → `shadowed_literals`, not a blocker.

2. **`\bwhat'?s the (?:next|upcoming) milestone\b`** — reachable in principle (its "upcoming" branch
   is NOT shadowed by `\bnext milestone\b`, which only covers the "next" branch — verified:
   `_first_pattern_match("what's the upcoming milestone", STATUS_PATTERNS)` returns this literal
   itself, not `\bnext milestone\b`), but **no corpus row anywhere in the 385-row corpus** exercises
   either branch distinctly from `\bnext milestone\b` (grepped the full corpus for "milestone" — the
   only STATUS-claimed milestone rows are "any update on the next milestone" and "what's the next
   milestone?", both of which `\bnext milestone\b` claims first, and "any upcoming milestones for this
   project", which `\bupcoming milestones?\b` (also a to-be-deleted, but separately audited — see
   below) claims). → genuinely unexercised, NOT shadowed.

3. **`\bmilestone status\b`** — reachable (`_first_pattern_match("milestone status",
   STATUS_PATTERNS)` returns this literal itself), but no corpus row of any category contains
   "milestone status". → genuinely unexercised, NOT shadowed.

4. **`\bmilestone progress\b`** — reachable (`_first_pattern_match("milestone progress",
   STATUS_PATTERNS)` returns this literal itself), but no corpus row of any category contains
   "milestone progress". → genuinely unexercised, NOT shadowed.

(`\bupcoming milestones?\b`, also scheduled for deletion, IS exercised — corpus row "any upcoming
milestones for this project" — so it is not in this list.)

**Pre-existing documentation note found, flagged as possibly stale**: `tests/fixtures/
inversion_corpus_phase0.yaml` line 1591 (attached to the "any upcoming milestones for this project"
row, written during the fifth deletion/GITHUB_QUERY_PATTERNS work) says: "the one reachable survivor
of STATUS_PATTERNS' 5-literal milestone subfamily — the other 4 are structurally unreachable." That
claim does not hold under direct measurement: of the other 4 milestone-family literals, only
`\bnext milestone\b` and (per this audit) `\bmy current work\b`-style shadowing logic apply narrowly —
`\bnext milestone\b` is in fact reachable and is one of the 4 gate-identified survivors (it claims
"any update on the next milestone" per the BEFORE gate quote), and the "upcoming" branch of
`\bwhat'?s the (?:next|upcoming) milestone\b`, plus `\bmilestone status\b` and `\bmilestone progress\b`,
are reachable-but-untested, not unreachable. Worth a correction pass but out of scope for this STOP.

## STOP

Per the dispatch prompt's explicit STOP condition ("any to-be-deleted literal is unexercised"): 3 of
the 52 to-be-deleted literals are unexercised AND NOT provably unreachable (only 1 of the 4 flagged
literals, `\bmy current work\b`, qualifies for `shadowed_literals`). Stopping before making any edit,
per instruction, rather than proceeding and leaving the gap for the Lead to patch afterward (the
sixth-deletion precedent did the latter; THIS dispatch's STOP list names unexercised-literal as an
explicit stop condition, so I'm following that literally rather than the precedent).

No files modified. No commits. Full BEFORE gate quote and literal audit handed to Lead via
SubagentHandback for a decision: deposit 2-3 corpus rows (one per genuinely-unexercised literal; the
"upcoming" branch and `\bnext milestone\b`'s own branch could share one row each, or just two rows:
one for "what's the upcoming milestone", one each for "milestone status" / "milestone progress") and
re-dispatch, or instruct me to proceed treating them some other way.

## Session Resumed — coordinator unblocked, STEPS 2-7 executed

Coordinator (Lead) identified the STOP as a false alarm: `PreClassifier._first_pattern_match`
against `STATUS_PATTERNS` alone is the wrong reachability instrument for a CROSS-LIST shadow — it
only proves reachability WITHIN one list. Re-checked with `PreClassifier.pre_classify_with_pattern_
list` (the real production if-chain): all 3 "genuinely unexercised" literals are claimed by the
inline (non-class-attribute) `MILESTONE_STATUS_INLINE_PATTERNS` check (Issue #1068), checked BEFORE
`STATUS_PATTERNS`. Verified independently (not just trusted): ran `pre_classify_with_pattern_list`
on all 6 of the coordinator's example phrases — all 6 → `(get_project_status,
'MILESTONE_STATUS_INLINE_PATTERNS')`, confirming the claim before proceeding. All 4 unexercised
literals recorded in `shadowed_literals` — no corpus deposits needed.

**STEP 2 — applied the partial deletion** to `services/intent_service/pre_classifier.py`:
`STATUS_PATTERNS` now `[r"\bcurrent work\b", r"\bproject overview\b", r"\bproject landscape\b",
r"\bnext milestone\b"]` (4 literals), with a dated comment block recording the deletion, the gate
quote, the shadowed-literal account, and the ceiling arithmetic. Claim branch (~line 1741) left
untouched (still live, no tombstone — the list has real literals). Confirmed via
`pattern_literal_counts.total_literal_count()` → 277, `per_list_literal_counts()["STATUS_PATTERNS"]`
→ 4.

Also fixed the stale `scripts/build_inversion_corpus_phase0.py` block comment (seventh-deletion
correction: `\bnext milestone\b` is reachable post-fifth-deletion, not "structurally unreachable"
as the pre-existing note claimed) and the "any upcoming milestones for this project" row's own
`notes` field; regenerated `tests/fixtures/inversion_corpus_phase0.yaml` via `python scripts/
build_inversion_corpus_phase0.py` — 385 rows unchanged, confirmed via `git diff --stat` (1 line
changed, the `notes` text only).

**STEP 3 — AFTER checks**: for each of the 48 deleted-literal rows (NOT 52 — the BEFORE gate's
"rows claimed: 52/385" line is corpus ROWS, distinct from the "52 literals" being deleted; 48 OK +
4 FAIL = 52 rows total, matching the gate header), ran `claim_for_phrase` (both entry surfaces —
`pre_classify_with_pattern_list` AND `detect_multiple_intents`, matching the gate's own precedence)
against the live post-deletion `PreClassifier`. Zero reabsorptions. All 4 survivor phrases
("any update on the next milestone", "can you summarize my current work", "give me a project
overview", "what's the project landscape") still claimed by `STATUS_PATTERNS` itself.

**STEP 4 — `--all` gate**: `STATUS_PATTERNS 4 4 NO-GO` (4 literals, 4 rows, as expected for a
partial list). Corpus denominator unchanged: 385 = 77 claimed + 308 unclaimed (down from 125
claimed; 125 − 77 = 48). `--list GUIDANCE_PATTERNS` re-checked: still GO (partial), same 3
survivors (`\bsetup.*projects?\b`, `\bset up.*projects?\b`, `\bset up.*portfolio\b`, 18 OK + 3 FAIL
= 21 rows) — unaffected by this deletion (GUIDANCE is checked before STATUS in the if-chain, so its
FAIL rows were never reclaimable by STATUS's now-deleted `\bmy projects\b`/`\bmy portfolio\b`).

**STEP 5 — ceiling + ledger**: `CEILINGS["pre-classifier"]` 329 → 277 in
`tests/test_architecture_enforcement.py`. Appended the 8th `DELETED_PATTERN_LISTS` entry to
`scripts/inversion_phase3_deleted_patterns.json` (built programmatically via a Python script, never
hand-typed) with `"partial": true`, `"surviving_literals"` (4-literal map), `"literals": 52`
(deleted count), `expected_op_by_phrase` for all 48 rows, `misserved_at_deletion` (9 rows),
`surface2_verified_at_deletion` (17 rows, both probe-report legs + samples + served model),
`shadowed_literals` (4 entries). Verified via `check_deleted_entry_non_regression` against ALL 8
ledger entries — all pass.

**STEP 6 — test conversion, 16 files + 1 product file** (`services/intent_service/
chat_pointers.py`'s `page:/standup` CHAT_POINTERS entry — "give me my standup" no longer resolves
deterministically; swapped to "can you summarize my current work," same destination, flagged a
discovered-work gap: the replacement no longer reads as standup-themed to a user, since no
surviving STATUS_PATTERNS literal is). Full list: `test_ftux_interview_1688.py` (2 sites),
`test_task_clarify_1654.py`, `test_reminder_clear_pick_target_1906.py`,
`test_inversion_multi_intent_unit4_1595.py`, `test_inversion_split_stand_down_1896.py`,
`test_original_message_1460.py`, `test_read_lane_destructive_greed_1756.py` (16 phrases),
`test_subsumption_portfolio_write_family_1884.py` (+ production's `status_project_noun_overlap`
value-copy pruned 9→2 members in `pre_classifier.py`), `test_truncated_render_provenance_1738.py`,
`test_subsumption_1084.py`, `test_keyword_disambiguation_901.py`,
`test_spend_free_canonical_ratchet_1818.py`, `test_inversion_phase3_deletion_1595.py` (ledger-count
pin renamed to "eight," new `test_status_patterns_now_claims_four_rows` pin, module docstring
updated). Every swap verified live against the real `PreClassifier` before committing to it (never
guessed) — confidence 1.0 claims only, cross-checked category membership where the test required it
(e.g. `READ_LANE_CATEGORIES`).

Full suite: `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py` +
`tests/unit/test_inversion_phase3_deletion_1595.py` + `tests/unit/test_inversion_phase3_surface2_
floor_1595.py` + `tests/unit/test_inversion_phase1_shadow_score_1595.py` +
`tests/test_architecture_enforcement.py` + the #1897 spend-free shape pin — **5166 passed, 1
xfailed, 0 failed**, run twice (once mid-fix, once final), identical both times. `scripts/run-
sweep.sh ratchets` — 1 PRE-EXISTING unrelated failure (`test_todo_marker_ratchet`, 36 vs frozen
ceiling 35), confirmed unrelated (reported, not fixed, per the dispatch).

**Tooling incident, self-corrected**: ran `ruff format`/`ruff check --fix` with
`scripts/inversion_phase3_deleted_patterns.json` in the file list. ruff (a Python tool) silently
introduced TRAILING COMMAS into the JSON — invalid JSON, `json.load` failed immediately
(`Expecting value`). Caught by reloading the file right after the ruff run rather than assuming a
clean exit meant a clean result. Fixed: diffed first (`git diff HEAD`, confirmed only my own
uncommitted, not-yet-reviewed addition was at risk — no PM/other-agent work, own worktree), then
`git checkout HEAD -- scripts/inversion_phase3_deleted_patterns.json` to restore the valid 7-entry
file, then re-ran the Python build script to re-append the 8th entry cleanly via `json.dump`.
Re-verified non-regression on all 8 entries and re-ran the full suite after the fix — both clean.
Never ran ruff on a `.json` path again this session.

**STEP 7 — docs**: appended "### Seventh deletion (2026-10-02): `STATUS_PATTERNS` (partial — 52 of
56)" to `docs/internal/architecture/current/intent-routing-stack.md` (full BEFORE/AFTER gate
quotes, the partial rule, the STOP/unblock incident with the lesson about the wrong reachability
instrument, all 16 converted files with per-file rationale, the ruff/JSON incident, ceiling
arithmetic). Dated entry appended to `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

**Files touched** (no commits — Lead commits by pathspec):
`services/intent_service/pre_classifier.py`, `services/intent_service/chat_pointers.py`,
`scripts/build_inversion_corpus_phase0.py`, `scripts/inversion_phase3_deleted_patterns.json`,
`tests/fixtures/inversion_corpus_phase0.yaml`, `tests/test_architecture_enforcement.py`,
`tests/unit/test_inversion_phase3_deletion_1595.py`, and the 15 other test files named above,
`docs/internal/architecture/current/intent-routing-stack.md`,
`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`, this session log.

**Verified how**: every gate run and reabsorption check quoted above was executed this session
(not recalled from memory); the full pytest suite was run twice end-to-end after all edits (not a
subset) with explicit pass/fail counts quoted; `pattern_literal_counts.total_literal_count()` and
`per_list_literal_counts()` were called directly against the live, edited `PreClassifier` class,
not assumed from the diff; `check_deleted_entry_non_regression` was run against all 8 real ledger
entries, not just the new one; the JSON corruption was caught by actually reloading the file, not
by trusting ruff's exit code. Layer: deterministic/unit only — zero LLM calls anywhere in this
unit's own work (every router verdict consulted is a frozen, already-scored report or a
monkeypatched stub).

## Memory & briefing surfaces referenced this session

- **Referenced**: CLAUDE.md worktree/sign-off discipline (not applicable — no commits made this
  session); sixth-deletion commits (`d1e954f08b`, `02c73d6dc1`) as the template for ledger-entry shape,
  tombstone-comment style, and the shadowed_literals / genuinely-unexercised distinction language.
- **Loaded but not referenced**: docs/internal/architecture/current/intent-routing-stack.md (not
  needed — no routing-stack edit made).
- **Wanted but not found**: nothing — the dispatch prompt and the gate script's own docstrings/code
  were sufficient to resolve the audit without further lookups.
