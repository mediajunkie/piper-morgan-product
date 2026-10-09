# Session log — Coding Agent (prog), model Sonnet 5, dispatched by Lead

**Date**: 2026-10-09
**Task**: #1595 Epic 0 Phase 3 — DRAFTING task only. Draft corpus rows for the 47/48 pre-classifier
literals currently HELD under rule 10 (dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md)
across the 9 lists named in the 10-09 batch's dispatch (PROVENANCE_PATTERNS, PORTFOLIO_PATTERNS,
IDENTITY_PATTERNS, DOCUMENT_QUERY_PATTERNS, FEATURE_INFO_PATTERNS, STAKEHOLDER_UPDATE_PATTERNS,
TODO_COMPLETE_PATTERNS, SET_DEFAULT_REPO_PATTERNS, REPO_MANAGEMENT_PATTERNS). Worked in
`/Users/xian/Development/piper-morgan-worktrees/lead`, branch `claude/lead-cycle`. **No code, corpus,
or test changes; no commits** — per the dispatch's explicit constraint.

## Outcome

Drafted 47 corpus rows to
`dev/2026/10/09/phase3-held-literal-rows-draft-2026-10-09.py` (a standalone, non-production Python
list of dicts — not a diff to `scripts/build_inversion_corpus_phase0.py`). The file's own module
docstring carries the full method, totals, and two flagged findings (REPO_MANAGEMENT_PATTERNS'
different gap; the one REVIEW row); this log summarizes rather than repeats that.

## What I did

1. Read `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (rules 4 and 10) and the
   10-09 log (`dev/2026/10/09/2026-10-09-1023-prog-code-log-1595-phase3-deletions-19-plus.md`) in
   full.
2. Ran `scripts/inversion_phase3_deletion_gate.py --list <NAME>` for all 9 named lists, collecting
   every "HELD (rule 10...)" line. Total: **47 held literals**, not the dispatch's estimated 48 —
   REPO_MANAGEMENT_PATTERNS contributes zero (its 4 non-survivor literals already have >=1 claiming
   corpus row each; rule 10's zero-row criterion finds nothing there). Flagged in the draft file as
   a DIFFERENT gap (claimed rows that score FAIL still read "GO (partial)" — the gate's partial-
   deletion logic checks "row exists", not "row passes"), not something this drafting task's remit
   covers fixing.
3. For each held literal, searched the specific test files the 10-09 log named as broken by the
   (reverted) deletion for a phrase the literal's own regex claims, preferring the test's verbatim
   wording. Found test coverage for 38/47; synthesized natural phrasings for the remaining 9 (marked
   `"origin": "synthesized"`).
4. Verified every one of the 47 phrases two ways this session (throwaway scripts under `/tmp`, not
   committed): (a) `PreClassifier.pre_classify(phrase)` returns the list's own uniform claim
   action/category; (b) a manual scan confirms the FIRST literal in the list's own source order that
   matches `phrase.lower()` is the exact literal the row is drafted for (not a shadowing sibling).
   All 47 passed both checks — `claimed_ok: True` throughout, zero exceptions, zero shadowed literals
   in this batch.
5. Mapped each `expected` action to the corpus's own category-bucket convention (confirmed against
   `scripts/build_inversion_corpus_phase0.py`'s `_ACTION_CATEGORY` dict AND several existing corpus
   rows in `tests/fixtures/inversion_corpus_phase0.yaml` — not surface-1's raw `Intent.category`,
   which disagrees for `update_document_query` and `set_default_repo` (surface-1 says QUERY; the
   corpus convention is EXECUTION for both, and existing rows confirm it).

## Per-list counts

PORTFOLIO_PATTERNS 12, DOCUMENT_QUERY_PATTERNS 9, PROVENANCE_PATTERNS 7, IDENTITY_PATTERNS 5,
FEATURE_INFO_PATTERNS 5, STAKEHOLDER_UPDATE_PATTERNS 3, TODO_COMPLETE_PATTERNS 3,
SET_DEFAULT_REPO_PATTERNS 3, REPO_MANAGEMENT_PATTERNS 0 = **47 total**. 38 test-derived, 9
synthesized.

## Flagged for the Lead (not resolved in this drafting pass)

- **REPO_MANAGEMENT_PATTERNS is out of scope for "add a row"** — it has zero rule-10 HELD literals,
  but its non-survivor literals' EXISTING claiming rows score FAIL (MISMATCH/non-live
  REVIEW/UNSCORED) and the gate still reports "GO (partial)" anyway. That's the gap #1969's own
  proposal (3) asked to audit for ("an audit of the six already-landed partial deletions ... for the
  same blind spot"), now shown on a *seventh*, not-yet-landed list. Reported, not fixed — fixing the
  gate's GO logic is a different task than depositing rows.
- **One REVIEW row**: DOCUMENT_QUERY_PATTERNS' `r"\bchange\s+(?:the\s+)?[\w\s]+\s+to\b"` literal. A
  real pinned test (`test_explicit_issue_update_1411.py::TestOrderingAndWiring::
  test_surface1_still_claims_no_hash_form`) asserts this EXACT literal claims "change the title of
  issue 108 to test new regressions" -> `update_document_query` at the bare `pre_classify` entry —
  but the same file's docstring and its sibling test establish that's the #1411 BUG shape; the ruled,
  full-pipeline destination (via B3 Stage 0 in `classify_multiple`) is `update_issue`. I don't know
  which entry point the deletion gate's own "surface 1" reading models for this row with enough
  confidence to assert either destination — flagged with a `lead_question` on the row rather than
  guessing.
- **Two TODO_COMPLETE_PATTERNS findings**: the "obvious" test phrases for `mark done` and
  `complete todo` (e.g., `test_mark_done_pattern`'s own "mark done the review docs todo") are
  actually claimed by a different, SURVIVING literal in the same list (the lazy-quantifier
  `.+?...{todo|task}` literal wins the race when a todo/task token appears later in the sentence).
  Wrote phrases without a trailing todo/task/done-family token so the intended literal fires;
  flagged as findings in the rows' `notes`, not corrected elsewhere.

## Rule 4 (effect-aware) literals flagged in the draft

PORTFOLIO_PATTERNS' hide/delete/remove/get-rid-of literals are destructive-shaped; restore/
unarchive/bring-back/add-create/new-project are WRITE-but-not-destructive. TODO_COMPLETE_PATTERNS'
three literals and SET_DEFAULT_REPO_PATTERNS' three literals are WRITE (todo completion, config
mutation) — noted as the same effect-aware caution even though they're not literally
"delete/archive/remove/hide." Every destructive/WRITE row's `notes` field says so explicitly.

## Discovered work filed

None new — the REPO_MANAGEMENT_PATTERNS finding above extends #1969's own proposal (3) rather than
opening a new issue; reporting it to the Lead via this log and the draft file's docstring per the
dispatch's own "report, don't fix" framing for this pass.

## Verified how

- The 47-literal HELD count: `scripts/inversion_phase3_deletion_gate.py --list <NAME>` run fresh
  this session for all 9 lists, output grepped for "HELD (rule 10" and separately for the summary
  "## <LIST> / literals: N / verdict:" lines (both quoted/counted in the draft file's docstring).
- Every phrase's claim: a throwaway verification script (`/tmp/verify_literal.py`, not committed)
  ran this session, importing the real `services.intent_service.pre_classifier.PreClassifier` with
  zero LLM calls, checking `winner_idx == target_idx` (the first literal in the list's own source
  order to match beats every row drafted here) for all 47 rows — 47/47 OK, printed and read in full,
  not sampled.
- No working-tree changes beyond the draft file: `git status --short` before and after this task
  shows only the new draft file plus one pre-existing untracked file
  (`dev/active/canonical-retest-serving-llm.json`, confirmed not mine, not touched).
- Layer: deterministic/surface-1 only (`PreClassifier.pre_classify`), zero LLM calls anywhere in this
  session. Denominator: all 47 drafted rows individually verified, not a sample.

## Memory & briefing surfaces referenced this session

**Referenced**: `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` rules 4 and 10 —
directly shaped which literals needed rows and how to flag destructive/WRITE risk; the 10-09 log —
the map from pattern list to broken test file that made the test-derived searches tractable instead
of a blind grep; `scripts/build_inversion_corpus_phase0.py`'s existing HAND_ROWS (several read in
full) — row-shape convention, `source`/`notes` phrasing style, and the `_ACTION_CATEGORY` dict that
resolved the EXECUTION-vs-QUERY category ambiguity for `update_document_query`/`set_default_repo`.

**Loaded but not referenced**: MEMORY.md index — no entry was load-bearing for a scoped drafting
task on an already-fully-specified dispatch.

**Wanted but not found**: a documented convention for how the deletion gate's "surface 1" reading
resolves when a literal's claim at the bare `pre_classify` entry diverges from the ruled destination
at the full `classify_multiple`+B3 pipeline (the DOCUMENT_QUERY_PATTERNS REVIEW row's exact
question) — flagged as a gap for the Lead/Arch rather than guessed at.

## Files touched

- `dev/2026/10/09/phase3-held-literal-rows-draft-2026-10-09.py` (new — the draft, not production
  code)
- `dev/2026/10/09/2026-10-09-1307-prog-code-log-1595-phase3-held-rows-draft.md` (this log)

No other files in the working tree carry any diff.
