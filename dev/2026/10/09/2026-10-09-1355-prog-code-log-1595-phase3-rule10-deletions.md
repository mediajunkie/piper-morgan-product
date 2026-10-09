# Session log — Coding Agent (prog), model Sonnet 5, dispatched by Lead

**Date**: 2026-10-09
**Task**: #1595 Epic 0 Phase 3 — the deletion lane for literals the gate now licenses under
Arch's standing rule 10 (#1969): a deletion lands only on literals with their OWN claiming
corpus row, scored, and only after a green FULL `tests/unit` run. Lead measured 7 lists as
licensed after PPM's same-day rule-10 corpus deposit (+45 rows, commit `41da0296a2`): IDENTITY_PATTERNS
(full, 6), FEATURE_INFO_PATTERNS (full, 6), STAKEHOLDER_UPDATE_PATTERNS (full, 4),
REPO_MANAGEMENT_PATTERNS (partial, 5), PROVENANCE_PATTERNS (partial, 3), TODO_COMPLETE_PATTERNS
(partial, 2), PORTFOLIO_PATTERNS (partial, 1). Working in
`/Users/xian/Development/piper-morgan-worktrees/lead`, branch `claude/lead-cycle`. No commits made
(hard rule: Lead reviews and commits). Lead directed work in CHUNKS, handing back after each.

LIVE set (13 tokens, by name, per Arch's condition): `read_status,read_referent,read_synthesis,
create_todo,create_reminder,read_strategic,read_temporal,delete_todo,read_floor,read_floor_2,
read_canonical,read_portfolio,complete_todo`.

## Chunk 1 (this entry): IDENTITY_PATTERNS bookkeeping, then FEATURE_INFO_PATTERNS fully

Lead asked for smaller chunks after the first handback, so this chunk landed IDENTITY_PATTERNS'
bookkeeping and FEATURE_INFO_PATTERNS end-to-end, and stopped there (explicitly NOT starting
STAKEHOLDER_UPDATE_PATTERNS) to hand back with a green tree.

### IDENTITY_PATTERNS — FULL (6 literals; ceiling 155 → 149)

Code deletion landed in a prior turn this session (before this log file was created — see the
handback reports for the turn-by-turn narrative). This entry completes its bookkeeping:

- **Ledger**: 20th `DELETED_PATTERN_LISTS` entry appended to
  `scripts/inversion_phase3_deleted_patterns.json` (`rows_claimed_at_deletion` = the 6 phrases,
  `verdict_report` = `["inversion-phase1-shadow-score-2026-09-25.md",
  "inversion-phase3-rule10-rows-score-2026-10-09-anthropic.md"]` — 1 pre-existing probe row +
  5 same-day rule-10 deposit rows, `expected_ops=["get_identity"]`, `expected_op_by_phrase` per
  phrase, no misserved/surface2/shadowed/reabsorption entries needed).
- **Ceiling**: `tests/test_architecture_enforcement.py`'s `CEILINGS["pre-classifier"]` 155 → 149,
  dated comment appended to the trail, value set to the MEASURED
  `scripts/pattern_literal_counts.py` total (`TOTAL: 149`).
- **Ledger-count pin**: `tests/unit/test_inversion_phase3_deletion_1595.py`'s
  `test_real_ledger_has_the_first_nineteen_deletions` renamed to
  `test_real_ledger_has_the_first_twenty_deletions`; name-set assertion gained
  `"IDENTITY_PATTERNS"`; a new `identity_entry` assertion block added (partial is not True,
  literals == 6); module docstring and the test's own docstring updated (nineteen → twenty,
  IDENTITY_PATTERNS's deposit provenance named).
- **Doc**: `docs/internal/architecture/current/intent-routing-stack.md` gains a "Nineteenth
  deletion (2026-10-09): `IDENTITY_PATTERNS` — FULL, rule-10-licensed" section (full BEFORE/AFTER
  gate quotes, the 7 converted test files with per-file rationale, ceiling arithmetic, the full
  12744-passed suite result).
- Re-ran `tests/unit/test_inversion_phase3_deletion_1595.py tests/test_architecture_enforcement.py`:
  **132 passed**, confirming the ledger/ceiling bookkeeping is internally consistent.

Rule-10(A) test conversions for IDENTITY_PATTERNS (all landed in the prior turn, confirmed again
here): `test_discovery_intent.py::test_identity_patterns_still_work` (6 parametrized cases),
`test_keyword_disambiguation_901.py::TestKeywordDisambiguationQ27::{test_tell_me_about_yourself_still_identity,test_who_are_you_still_identity}`,
`test_pre_classifier.py::TestPreClassifier::test_trust_not_identity` (split; new
`test_who_are_you_still_identity_via_inversion`), `test_preclaim_shadow.py::TestPatternIdentityThreading`
(2 sites, swapped carrier to `"why can't you create issues?"/TRUST_PATTERNS`),
`test_spend_free_canonical_ratchet_1818.py` (`("IDENTITY","get_identity")` removed with a NOTE,
same shape as PRIORITY's removal), `test_inversion_phase3_deletion_1595.py::TestNonRegressionMechanism::test_documented_disagreeing_reclaim_needs_the_live_flag_when_the_row_is_mismatch`
(swapped carrier, same reason). Full `tests/unit` confirmed clean: **12744 passed, 227 skipped, 0
failed** (267.69s).

### FEATURE_INFO_PATTERNS — FULL (6 literals; ceiling 149 → 143)

BEFORE gate (`--list FEATURE_INFO_PATTERNS` with the 13-token LIVE set): GO (deletable), 6/6
corpus rows claimed, all `[OK]` (MATCH, expected action live via `read_floor_2` group — same
`get_feature_info` rail entry IDENTITY_PATTERNS' deletion also relies on). 0 unexercised literals.

Edited `services/intent_service/pre_classifier.py`: `FEATURE_INFO_PATTERNS = []`, dated tombstone
comment (same form as every prior FULL deletion). AFTER gate: `literals: 0 | rows claimed: 0/563 |
verdict: NO-GO` (NO ROWS).

Rule-10(A) conversions (every failing test cites its replacing corpus row, `read_floor_2`,
`get_feature_info`):
- `tests/unit/services/intent_service/test_keyword_disambiguation_901.py::TestKeywordDisambiguationQ27`
  — 4 tests (`test_github_integration_routes_to_query`, `test_slack_integration_routes_to_query`,
  `test_calendar_feature_routes_to_query`, `test_notion_integration_routes_to_query`) converted to
  decline + `assert_inversion_routes`.
- `tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_feature_info_routes_to_query`
  — same conversion.

Ledger: 21st entry appended. Ceiling: 149 → 143 (confirmed `pattern_literal_counts.py` →
`TOTAL: 143`). `test_real_ledger_has_the_first_twenty_deletions` renamed to
`..._twenty_one_deletions`; name-set gained `FEATURE_INFO_PATTERNS`; new assertion block added.
Doc gains a "Twentieth deletion" section.

Targeted suite (the 5 converted tests + the 2 Q27-identity tests): **7 passed**. Full `tests/unit
-q -p no:cacheprovider --maxfail=1000` (run in the FOREGROUND per Lead's instruction, read to the
summary line, no truncation): **12744 passed, 227 skipped, 0 failed** (261.77s) — confirmed
clean, no restores needed (every failing test was Rule-10(A), none Rule-10(B)).

Ledger: 21st entry. Ceiling: 149 → 143 (confirmed `pattern_literal_counts.py` → `TOTAL: 143`).
Ledger-count pin renamed `test_real_ledger_has_the_first_twenty_deletions` →
`..._twenty_one_deletions`; name-set gained `FEATURE_INFO_PATTERNS`; new `feature_info_entry`
assertion block added. Doc gains a "Twentieth deletion" section in `intent-routing-stack.md`.

Re-ran `tests/unit/test_inversion_phase3_deletion_1595.py tests/test_architecture_enforcement.py`
after the bookkeeping: see handback for exact count. Repo-wide `ruff format --check . && ruff
check .`: see handback.

**Per Lead's explicit chunk-2 instruction, STAKEHOLDER_UPDATE_PATTERNS was NOT started this
chunk** — the smaller-chunk request was specifically to land FEATURE_INFO_PATTERNS alone and hand
back with a green tree, rather than continuing to STAKEHOLDER_UPDATE_PATTERNS as originally
drafted in this log's first version. (An earlier draft of this log section incorrectly described
STAKEHOLDER_UPDATE_PATTERNS as done — corrected here; it was never actually edited.)

Ceiling so far across this session: **155 → 143** (IDENTITY −6, FEATURE_INFO −6).
STAKEHOLDER_UPDATE_PATTERNS, REPO_MANAGEMENT_PATTERNS, PROVENANCE_PATTERNS,
TODO_COMPLETE_PATTERNS, PORTFOLIO_PATTERNS remain fully pre-analyzed (BEFORE-gate output matches
the dispatch's counts exactly) but untouched.

## Discovered work filed
None new this chunk (the zero-corpus-row gap was already filed as #1969 this morning, before
this session).

## Memory & briefing surfaces referenced this session

**Referenced**: CLAUDE.md's Rule 10 standing rule (via
`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`) — directly governed every
deletion/retire/restore decision this chunk; the 2026-10-03 batch's session log and commit
(`85130832d2`) — template for ledger-entry shape, ceiling-comment style, doc-section style;
the 2026-10-09 morning FAILED-attempt log — the exact failure mode (zero-row literals deleted)
this chunk's rule-10-licensed literals are specifically NOT exposed to, since every literal
deleted this chunk has its own scored, claimed corpus row.

**Loaded but not referenced**: MEMORY.md index (no specific entry was load-bearing).

**Wanted but not found**: none.

## Chunk 3: STAKEHOLDER_UPDATE_PATTERNS — PARTIAL (3 of 4 literals; ceiling 143 → 140)

First synced per Lead's instruction: `git fetch -q origin main && git merge -q origin/main -m
"merge origin/main"` — already up to date (no divergent local commits; IDENTITY/FEATURE_INFO had
landed on main from chunks 1-2, plus Arch's framing ruling bringing the corpus to 565 rows).
Re-measured ceiling (143, matching chunk 2's end state) and re-gated STAKEHOLDER_UPDATE_PATTERNS
fresh against the post-merge corpus before touching anything, per Lead's instruction (counts may
have moved).

BEFORE gate: GO (deletable, full) — 4 literals, 5/565 corpus rows claimed, all [OK] (2 pre-existing
rows, 3 from the rule-10 deposit). Emptied `STAKEHOLDER_UPDATE_PATTERNS = []` and converted all 4
affected tests in `test_pre_classifier_stakeholder_update_1256.py`.

**Rule-10(B) found**: `test_judge_experiment_query_routes_to_stakeholder_update` — the file's own
namesake #1256 regression pin — FAILED on the full deletion. The phrase ("Write a short update for
the OpenLaws CEO John Phamvan on where we are with the Piper Morgan alpha testing.") is NOT one of
the 5 corpus rows; once the "write ... update for" literal was gone, it mis-routed to
`update_document_query` (DOCUMENT_QUERY_PATTERNS' loose "update ... with" regex re-claimed it) —
reopening the exact bug #1256 fixed. **Restored that one literal** (and only it), converting the
deletion from FULL to PARTIAL (3 of 4 deleted). Reverted that one test's conversion back to its
original, unchanged assertion (it was never actually broken once the literal came back — same
zero-LLM direct-claim behavior as before this epic touched this list). The other 3 tests (whose
phrases ARE exact rule-10-deposit corpus rows) stayed converted, Rule-10(A).

**Note**: the gate's own corpus-only re-read of the single surviving literal (run alone, post-fix)
reports it as itself further-deletable (GO, 2/2 rows [OK]) — NOT acted on. The real failing
non-corpus test is the stronger evidence; rule 10's own text ("a unit test that fails on a deletion
is a phrasing the corpus is missing") argues against re-deleting, not for it.

Targeted suite (`test_pre_classifier_stakeholder_update_1256.py`): 7 passed. Full `tests/unit -q
-p no:cacheprovider --maxfail=1000` (FOREGROUND, read to the summary line): **12744 passed, 227
skipped, 0 failed** (266.34s) — same count as chunks 1-2's own full runs, confirming no drift from
the merge or this chunk's work.

Ledger: 22nd entry (`partial: true`, `surviving_literals` = the 1 restored literal mapped to its 2
corpus phrases, `rows_claimed_at_deletion` = the 3 deleted literals' corpus rows). Ceiling: 143 →
140 (confirmed `pattern_literal_counts.py` → `TOTAL: 140`). Ledger-count pin renamed
`..._twenty_one_deletions` → `..._twenty_two_deletions`; name-set gained
`STAKEHOLDER_UPDATE_PATTERNS`; new `stakeholder_update_entry` assertion block (partial IS True,
literals==3, surviving_literals == the 1 restored pattern). Doc gains a "Twenty-second deletion"
section in `intent-routing-stack.md` (full BEFORE/AFTER gate quotes, the rule-10(B) finding, the
gate-vs-test-evidence note).

Re-ran `tests/unit/test_inversion_phase3_deletion_1595.py tests/test_architecture_enforcement.py`:
**132 passed in 23.18s**. Repo-wide ruff: see handback for exact output.

Running ceiling across this session: **155 → 140** (IDENTITY −6, FEATURE_INFO −6,
STAKEHOLDER_UPDATE −3). REPO_MANAGEMENT_PATTERNS, PROVENANCE_PATTERNS, TODO_COMPLETE_PATTERNS,
PORTFOLIO_PATTERNS remain fully pre-analyzed but untouched.

**Discovered work**: none filed — the Rule-10(B) restore is exactly the mechanism rule 10 and the
dispatch's own procedure exist to catch; it is documented in the ledger/doc/ceiling comment, not a
separate GH issue (consistent with how every other epic finding has been handled: a documented
finding in the ledger, not a new issue, unless it reveals a gap in the GATE/MECHANISM itself the
way #1969 did this morning — this one didn't; the mechanism caught it as designed).

## Verified how

Every claim above is from a command actually run this session: gate script invocations (quoted
verbatim in-line), `pattern_literal_counts.py` totals, the targeted and full pytest runs (exact
counts in the handback message, not re-transcribed here), `git status --short`. Layer:
deterministic/unit — zero LLM calls anywhere in this chunk's own work (every router verdict
consulted is a frozen, already-scored report, or a monkeypatched stub in tests). Denominator:
the FULL `tests/unit` tree, not a targeted subset, per the dispatch's explicit instruction and
rule 10's own text.
