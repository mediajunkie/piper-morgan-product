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

## Chunk 4: REPO_MANAGEMENT_PATTERNS — PARTIAL (5 of 9 literals; ceiling 140 → 135)

Synced first: `git fetch -q origin main && git merge -q origin/main -m "merge origin/main"` —
already up to date (STAKEHOLDER_UPDATE landed and pushed by Lead in between chunks). Re-measured
ceiling (140, consistent) and re-gated fresh before touching anything.

BEFORE gate: GO (partial) — 4 load-bearing literals SURVIVE (the bare "repo(sitory)" link/add
forms + both list forms), deleting the other 5. Unlike STAKEHOLDER_UPDATE_PATTERNS, the gate's own
BEFORE read was already partial — caught at gate time, not via a later test failure. Of the 6 `[OK]`
rows: 3 via the mis-serve escape (owner/repo-form claims disagree with ruled `link_repo`, which has
no live token; surface-2 probe shows no WRITE/DESTRUCTIVE op), 1 via a live-group MISMATCH
("connect my repository to the project" → `get_contextual_guidance`, live via `read_canonical`), 1
via a plain live MATCH ("can you show project repositories for this account" → `list_repos`, live
via `read_portfolio`). Emptied the 5 non-survivor literals, kept the 4 survivors.

**7 test sites across 4 files converted, ALL Rule-10(A) — zero (B) restores this chunk** (every
decline confirmed empirically via `claim_for_phrase`/direct `pre_classify`, no reabsorption, no
production misroute found):
- `test_repo_management.py::TestRepoManagementPatterns` — split the two parametrized "still
  claims" tests down to their 2 surviving phrases each; added `test_owner_repo_form_now_unclaimed`
  (plain decline, 3 phrases), `test_connect_repo_form_routes_via_inversion` (decline +
  `assert_inversion_routes`, `read_canonical`/`get_contextual_guidance`),
  `test_show_project_repositories_routes_via_inversion` (same idiom, `read_portfolio`/
  `list_repos`); swapped `test_multi_intent_includes_manage_repos`'s phrase to a survivor.
- `test_integration_connect_preclassifier_1417.py::test_slug_link_still_reaches_repo_management` —
  converted to a plain decline (mis-serve escape).
- `test_subsumption_portfolio_write_family_1884.py::test_link_family_single_intent` — swapped probe
  phrase to a survivor, confirmed identical single-intent property.
- `test_spend_free_canonical_ratchet_1818.py` — **the noted landmine**: `("PORTFOLIO",
  "manage_repos")`'s probe ("link mediajunkie/test to project X") matched a deleted literal;
  swapped to "link my repository to the project" (survivor), re-confirmed SPEND_FREE unchanged.

Targeted suites all passed (37 + 49 + 10). Full `tests/unit -q -p no:cacheprovider --maxfail=1000`
(FOREGROUND, read to the summary line, two full runs — one before finding the last 2 landmines,
one after): **12744 passed, 227 skipped, 0 failed** (279.88s final run) — identical count to every
prior chunk this session.

Ledger: 23rd entry (`partial: true`, `surviving_literals` = the 4 kept literals mapped to their
claiming corpus phrases, `misserved_at_deletion` for the 3 mis-serve-escape rows,
`expected_op_by_phrase` for the 3-distinct-op shape). Ceiling: 140 → 135 (confirmed
`pattern_literal_counts.py` → `TOTAL: 135`). Ledger-count pin renamed `..._twenty_two_deletions` →
`..._twenty_three_deletions`; name-set gained `REPO_MANAGEMENT_PATTERNS`; new
`repo_management_entry` assertion block. Doc gains a "Twenty-third deletion" section.

**Known, EXPECTED, OUT-OF-SCOPE breakage, not fixed per explicit instruction**: `tests/
test_architecture_enforcement.py::TestExecuteVocabCoverage` (3 tests) fail —
`_repo_management_list_literals`'s own internal assertion hardcodes "9 literals" for
REPO_MANAGEMENT_PATTERNS, now 4. Lead's own chunk-4 instruction: "I will also edit ...
TestExecuteVocabCoverage AFTER you hand back... don't touch TestExecuteVocabCoverage." Confirmed
these are the ONLY 3 failures in that file (68 passed, 3 failed when run alone) and the ONLY
failures anywhere outside `tests/unit` this chunk touches.

**Verbatim (B)-restore phrasings this chunk: NONE.** (Chunk 3's #1256 phrase was the only one so
far; see that chunk's entry for the verbatim text, already reported to Lead in the chunk-3
handback.)

## Verified how

Every claim above is from a command actually run this session: gate script invocations (quoted
verbatim in-line), `pattern_literal_counts.py` totals, the targeted and full pytest runs (exact
counts in the handback message, not re-transcribed here), `git status --short`. Layer:
deterministic/unit — zero LLM calls anywhere in this chunk's own work (every router verdict
consulted is a frozen, already-scored report, or a monkeypatched stub in tests). Denominator:
the FULL `tests/unit` tree, not a targeted subset, per the dispatch's explicit instruction and
rule 10's own text.

## Chunk 5: PROVENANCE_PATTERNS — PARTIAL (3 of 8 literals; ceiling 135 → 132)

Synced first (no-op, already up to date — REPO_MANAGEMENT landed/pushed between chunks, and the
Lead's own `TestExecuteVocabCoverage` fix (9→4 split) is on `main`; confirmed green:
`tests/test_architecture_enforcement.py` alone, 71 passed). Re-measured ceiling (135, consistent)
and re-gated PROVENANCE_PATTERNS fresh.

BEFORE gate: GO (partial) — 5 load-bearing literals SURVIVE, deleting 3. Like REPO_MANAGEMENT, the
gate's own BEFORE read was already partial (caught at gate time). Of the 3 `[OK]` (deleted) rows: 1
pre-existing probe row (REVIEW-agrees, live via `read_floor_2`), 2 from the same-day rule-10
deposit (1 plain live MATCH, 1 live-group MISMATCH where the router's own route, `explain_trust`,
is live via the same group). Emptied the 3 non-survivor literals (the "why did you
mention/bring-up/suggest/..." verb list, "what made you mention/think/suggest/bring", and "how do
you know about/that"), kept the 5 survivors.

**Caught and fixed the noted landmine**: `test_spend_free_canonical_ratchet_1818.py`'s
`("PROVENANCE", "explain_suggestion")` probe ("why did you suggest that?") matched a deleted
literal. Swapped to "Where did you get that from?" (a survivor), re-confirmed SPEND_FREE
unchanged.

**The widest single-test fallout this chunk**: `test_pre_classifier.py::
test_provenance_routes_before_trust` ran a 21-phrase for-loop, 12 of which matched the 3 deleted
literals. Split: kept the original test with only its 9 surviving phrases; added
`test_provenance_deleted_verb_literals_now_unclaimed` asserting all 12 deleted-literal phrases
decline cleanly (confirmed empirically, no reabsorption — verified every one of the 12 individually
before writing the assertion). **Zero (B) restores this chunk** — every decline confirmed safe.

Checked (not touched) a stale comment in `test_inversion_multi_intent_unit4_1595.py` referencing a
now-deleted PROVENANCE literal — the actual constant it narrates was already swapped away from a
PROVENANCE phrase in an earlier (2026-10-04) wave; purely historical narrative, no live dependency.

Targeted suites (9 files, including the landmine fix): 199 passed. Full `tests/unit -q
-p no:cacheprovider --maxfail=1000` (FOREGROUND, read to the summary line): **12745 passed, 227
skipped, 0 failed** (269.67s) — the +1 over the prior chunk's 12744 is the one test split into
two, not a regression.

Ledger: 24th entry (`partial: true`, `surviving_literals` mapped to 1 claiming phrase each,
`expected_op_by_phrase` for the single-op shape). Ceiling: 135 → 132 (confirmed
`pattern_literal_counts.py` → `TOTAL: 132`). Ledger-count pin renamed `..._twenty_three_deletions`
→ `..._twenty_four_deletions`; name-set gained `PROVENANCE_PATTERNS`; new `provenance_entry`
assertion block. Doc gains a "Twenty-fourth deletion" section (one arithmetic slip caught and
corrected while drafting it: initially miscounted 4 OK/4 FAIL instead of the actual 3 OK/5 FAIL —
fixed before finalizing, not left in the doc).

**Re-verification, now fully green (no out-of-scope breakage this time)**:
`tests/unit/test_inversion_phase3_deletion_1595.py tests/test_architecture_enforcement.py` →
**132 passed, 0 failed** — the Lead's own `TestExecuteVocabCoverage` fix from the prior chunk
means this file is clean again, exactly as the dispatch anticipated.

**Verbatim (B)-restore phrasings this chunk: NONE.** (Only chunk 3's #1256 phrase remains the
sole (B) case this session so far: `"Write a short update for the OpenLaws CEO John Phamvan on
where we are with the Piper Morgan alpha testing."` —
`test_pre_classifier_stakeholder_update_1256.py::TestStakeholderUpdateRouting::
test_judge_experiment_query_routes_to_stakeholder_update`.)

## Verified how (chunk 5)

Every claim above is from a command actually run this session: gate script invocations (quoted
verbatim in-line), `pattern_literal_counts.py` totals, the targeted and full pytest runs (exact
counts quoted above), `git status --short`. Layer: deterministic/unit — zero LLM calls anywhere
in this chunk's own work. Denominator: the FULL `tests/unit` tree (12745 tests), not a targeted
subset.

## Chunk 6: TODO_COMPLETE_PATTERNS — PARTIAL (2 of 7 literals; ceiling 132 → 130)

Synced first (no-op, already up to date — PROVENANCE landed/pushed between chunks). Re-measured
ceiling (132, consistent) and re-gated TODO_COMPLETE_PATTERNS fresh.

BEFORE gate: GO (partial) — 5 load-bearing literals SURVIVE, deleting 2. Like REPO_MANAGEMENT and
PROVENANCE, the gate's own BEFORE read was already partial. 17 corpus rows claimed (5 OK, 12 FAIL
— 11 UNSCORED multi-item/clear-family phrasings, 1 MISMATCH/CLARIFY), all 12 FAIL rows and 3 of
the 5 OK rows claim the survivors. The 2 deleted literals ("finish todo\b", "complete todo\b" —
bare todo-immediately-after-verb forms) each claim exactly one row, both today's rule-10 deposit:
"finish todo about deployment" and "complete todo for the deploy checklist", both MATCH live via
the `complete_todo` operation directly (no flip_group needed — `complete_todo` is itself a live
token in the current flag).

Dispatch's watch-items checked explicitly: `todo-floor-binding` and the ask-site ratchets in
`tests/test_architecture_enforcement.py` have no dependency on TODO_COMPLETE_PATTERNS' literal
count (grep-confirmed — unlike REPO_MANAGEMENT_PATTERNS, no `_todo_complete_list_literals`-shaped
hardcoded-count helper exists for this list). Ran `tests/test_architecture_enforcement.py` alone
right after the pattern edit, before any test conversion: exactly 1 failure
(`TestExtractionPatternRatchet.test_extraction_ratchet_stays_tight`, the expected
ceiling-not-yet-updated failure), nothing else — confirming the watch-items are clean. The
#1943/#1914 completion suites (`test_todo_completion_clause_split_1914.py`,
`test_complete_todo_disambiguation_1930.py`) checked and found NOT dependent on
`pre_classify` for either deleted literal (one tests `_split_completion_clause` directly, the
other constructs `Intent` objects directly) — confirmed by grep + full targeted run, zero changes
needed to either file.

**One test converted, zero (B) restores**:
`test_todo_completion_lifecycle.py::test_finish_todo_pattern` ("finish todo about deployment")
converted to decline + `assert_inversion_routes` (`live_categories="complete_todo"`,
`expected_action="complete_todo"`) — this list's own corpus row.

Targeted suites (3 files): 38 passed. Full `tests/unit -q -p no:cacheprovider --maxfail=1000`
(FOREGROUND, read to the summary line): **12745 passed, 227 skipped, 0 failed** (262.73s) —
identical count to the prior chunk, confirming no regression.

Ledger: 25th entry (`partial: true`, `surviving_literals` mapped to all their claiming phrases).
Ceiling: 132 → 130 (confirmed `pattern_literal_counts.py` → `TOTAL: 130`). Ledger-count pin
renamed `..._twenty_four_deletions` → `..._twenty_five_deletions`; name-set gained
`TODO_COMPLETE_PATTERNS`; new `todo_complete_entry` assertion block.

Caught and fixed one more arithmetic slip while drafting the doc section (same category as
chunk 5's: miscounted the OK/FAIL row split as "4 OK" before recounting the actual gate output
line-by-line to 5 OK/12 FAIL) — corrected before finalizing, not left in the doc.

**Re-verification, fully green**: `tests/unit/test_inversion_phase3_deletion_1595.py
tests/test_architecture_enforcement.py` → **132 passed, 0 failed**.

**Verbatim (B)-restore phrasings this chunk: NONE.** (Chunk 3's #1256 phrase remains the sole (B)
case this session: `"Write a short update for the OpenLaws CEO John Phamvan on where we are with
the Piper Morgan alpha testing."` —
`test_pre_classifier_stakeholder_update_1256.py::TestStakeholderUpdateRouting::
test_judge_experiment_query_routes_to_stakeholder_update`.)

Doc gains a "Twenty-fifth deletion" section.

TODO_COMPLETE_PATTERNS did not run long, so per the dispatch continuing straight to
PORTFOLIO_PATTERNS now rather than handing back prematurely (the Lead's hand-back-early clause was
conditional on a long run).

## Verified how (chunk 6)

Every claim above is from a command actually run this session: gate script invocations (quoted
verbatim in-line), `pattern_literal_counts.py` totals, the targeted and full pytest runs (exact
counts quoted above), `git status --short`. Layer: deterministic/unit — zero LLM calls anywhere
in this chunk's own work. Denominator: the FULL `tests/unit` tree (12745 tests), not a targeted
subset.

## Chunk 7 (final): PORTFOLIO_PATTERNS — PARTIAL (1 of 16 literals; ceiling 130 → 129)

No re-sync needed (same turn as chunk 6, no intervening Lead commit). Re-gated PORTFOLIO_PATTERNS
fresh per the dispatch's instruction regardless.

BEFORE gate: GO (partial) — 15 load-bearing literals SURVIVE, deleting 1. Per the dispatch's
explicit guidance: delete/remove/get-rid-of are named survivors until #1935 regardless of the
gate's own verdict; hide/put-away/add/new-project are held or survivors per the gate's own read.
Confirmed `\bnew project\b` moved from HELD (pre-deposit) to a genuine FAIL/survivor (today's
rule-10 deposit gave it a claiming row, "I'd like to start a new project") — closing exactly the
gap the dispatch named. The ONLY deletable literal is "search projects for Y"; its own corpus row
("search projects for budget", today's rule-10 deposit) is a plain live MATCH (search_projects,
live via read_portfolio).

**Two tests converted, zero (B) restores**:
- `test_pre_classifier.py::test_portfolio_patterns` — split off "search projects for budget" into
  a new `test_portfolio_search_now_unclaimed` (plain decline); kept "find project deadline"
  (survivor) in the original loop, unchanged.
- `test_subsumption_portfolio_write_family_1884.py::
  test_search_projects_read_verb_single_intent_no_status_to_begin_with` — "search projects for X"
  now returns `is_multi_intent=False, actions=[]` (confirmed empirically); swapped the probe
  phrase to "find project X in my portfolio" (a survivor), confirmed identical property.

Checked (not touched, no dependency): `test_portfolio_search_projects_read_1595.py`,
`test_render_truncation_sweep_1762.py` (both construct `Intent` directly), `test_restore_by_name_1470.py`,
`test_portfolio_service.py` (both exercise `PortfolioService.search_projects()` at the service
layer).

Targeted suites (4 files): 86 passed. Full `tests/unit -q -p no:cacheprovider --maxfail=1000`
(FOREGROUND, read to the summary line): **12746 passed, 227 skipped, 0 failed** (261.56s) — the +1
over chunk 6's 12745 is the one test split into two, not a regression.

Ledger: 26th (and final, for this batch) entry (`partial: true`, `surviving_literals` mapped to
all 15 survivors' claiming phrases — the longest `surviving_literals` map of the whole batch).
Ceiling: 130 → 129 (confirmed `pattern_literal_counts.py` → `TOTAL: 129`). Ledger-count pin
renamed `..._twenty_five_deletions` → `..._twenty_six_deletions`; name-set gained
`PORTFOLIO_PATTERNS`; new `portfolio_entry` assertion block.

**Re-verification, fully green**: `tests/unit/test_inversion_phase3_deletion_1595.py
tests/test_architecture_enforcement.py` → **132 passed, 0 failed**.

Doc gains a "Twenty-sixth deletion" section, plus a closing summary of the whole 7-list batch
(IDENTITY/FEATURE_INFO/STAKEHOLDER_UPDATE/REPO_MANAGEMENT/PROVENANCE/TODO_COMPLETE/PORTFOLIO; 26
literals deleted total; ceiling 155 → 129).

**Verbatim (B)-restore phrasings, this chunk: NONE.** Session total across all 7 lists: exactly
ONE (B) restore, from chunk 3:
`"Write a short update for the OpenLaws CEO John Phamvan on where we are with the Piper Morgan alpha testing."`
— `test_pre_classifier_stakeholder_update_1256.py::TestStakeholderUpdateRouting::test_judge_experiment_query_routes_to_stakeholder_update`
(restored literal: `\bwrite\s+(?:me\s+)?(?:a|an)?\s*(?:\w+\s+){0,3}update\s+for\b` in
STAKEHOLDER_UPDATE_PATTERNS; the phrase reopened the original #1256 `update_document_query`
misroute when deleted).

## Final repo-wide verification (both lists, before hand-off)

Pending: full tests/unit (already run per-list above, both green), ledger+enforcement tests
(already green), repo-wide ruff — see handback for exact output.

## Verified how (chunk 7, final)

Every claim above is from a command actually run this session: gate script invocations (quoted
verbatim in-line), `pattern_literal_counts.py` totals, the targeted and full pytest runs (exact
counts quoted above), `git status --short`. Layer: deterministic/unit — zero LLM calls anywhere
in this chunk's own work. Denominator: the FULL `tests/unit` tree (12746 tests), not a targeted
subset.
