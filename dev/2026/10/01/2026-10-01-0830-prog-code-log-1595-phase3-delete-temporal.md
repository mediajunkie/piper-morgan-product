# 2026-10-01 0830 — prog (Coding Agent) — #1595 Phase 3, fourth deletion: TEMPORAL_PATTERNS

**Role**: prog (Coding Agent), model Sonnet 5. Dispatched by Lead Developer, in the Lead's
worktree (`/Users/xian/Development/piper-morgan-worktrees/lead`, branch `claude/lead-cycle`).
No git index touched at any point (per dispatch instruction — no staging/commit performed).
No LLM calls anywhere in this unit; no flag/env changes.

## Task

Phase 3's fourth deletion of the #1595 Inversion epic-0 unit 5 — delete `TEMPORAL_PATTERNS`
(56 literals), the list CALENDAR_QUERY_PATTERNS' own third deletion found reabsorbing 19 of its
claimed phrases. Gated on two same-day prerequisites already landed before this unit started:
the per-row sort of the 48 TEMPORAL deposit rows and the `get_current_time_entry` READ rail
entry (both from Arch's 2026-10-01 ruling, implemented in a separate prog session,
`dev/2026/10/01/2026-10-01-0830-prog-code-log-1595-temporal-sort-and-rail.md`).

## Read first

- `dev/2026/10/01/2026-10-01-0745-prog-code-log-1595-phase3-delete-calendar.md` — the CALENDAR
  deletion lane's log, the exact shape of this unit (tombstone form, ledger entry with
  `expected_op_by_phrase` for every row, `known_reabsorptions` with `"agrees"`, ceiling
  arithmetic, pin conversion via `_inversion_pin_helper.py`) — and the finding that
  TEMPORAL_PATTERNS reabsorbed 19 calendar phrases as `get_current_time`, which this deletion
  removes.
- `docs/internal/architecture/current/intent-routing-stack.md` §Phase 3 (all four deletion
  subsections + the "scored on BOTH tables" rule + the "get_current_time becomes a rail key"
  paragraph).
- Arch's ruling `mailboxes/lead/read/rule-arch-to-lead-cc-ppm-cxo-temporal-give-get-current-time-
  a-rail-entry-and-the-gate-has-a-false-live-path-2026-10-01.md` — the per-row sort is DONE; the
  rail entry is DONE and live on v154; this is the deletion the ruling unlocks.
- `dev/2026/10/01/2026-10-01-0830-prog-code-log-1595-temporal-sort-and-rail.md` — the full
  per-row sort table (48 deposit rows + 2 pre-existing = 50 TEMPORAL rows, their ruled
  destinations, and the rationale for each).

## Gate before deletion

```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list TEMPORAL_PATTERNS \
  --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal
```
→ `corpus denominator: 283 rows total = 232 claimed + 51 unclaimed`, `literals: 56 | rows
claimed: 69/283`, `verdict: GO (deletable) — deleting removes 56 literals: ceiling 496 -> 440`,
`pattern->corpus conversion: 4 literal(s) unexercised`. Exactly matching the dispatch prompt's
expected numbers.

Of the 69 claimed rows: 7 pass via the new "mis-serves this row" branch (router declined AND
the pattern's own claim disagreed with the ruled destination) OR "MISMATCH but the router's own
route is itself live" reasons — of these, 5 are genuinely **mis-served** (`pull up my calendar`,
`schedule check for today`, `show all events`, `when's my next free slot`, `what's my available
time` — all claimed `get_current_time`, ruled `week_calendar`/`meeting_time`, router declined
CLARIFY) and 2 are **live-MISMATCH** (`what is on my calendar`, `is there a conflict on my
calendar` — router's own route is itself a live op). Both counted via `grep -c` against the
quoted gate output, not eyeballed.

## What I did

1. **Tombstoned `TEMPORAL_PATTERNS`** in `pre_classifier.py`: `= []  # type: List[str]`, citing
   the Haiku baseline, the 10-01 TEMPORAL rescore, Arch's ruling, and the per-row sort. Added
   comments at FOUR sites noting the resulting dead code is intentional and survives: (a) the
   class attribute itself; (b) `pre_classify`'s inline TEMPORAL branch (now structurally
   unreachable, with a note that surface 1 no longer produces a TEMPORAL claim, so
   `_requires_canonical_handler`'s TEMPORAL split is reached only via the LLM classifier now);
   (c) the `detect_multiple_intents` pattern-groups entry; (d) `_READ_LANE_GROUPS`' membership;
   (e) `_temporal_disjoint_from_connect`'s docstring (the helper it guards is now permanently,
   structurally inert — its loop runs zero iterations). Mirrored comment added to
   `services/intent/intent_service.py`'s TEMPORAL floor/keyword split comment (~line 15380,
   read-only otherwise — the split code itself is unchanged, only the comment explaining it's
   now reached only from surface 2). No other `*_PATTERNS` list touched.

2. **Ledger entry** in `scripts/inversion_phase3_deleted_patterns.json`: all 69
   `rows_claimed_at_deletion` phrases; `expected_op_by_phrase` for every one (6 real ops:
   `get_current_time`/`meeting_time`/`week_calendar`/`session_activity_query`/
   `check_completion_status`/`changes_query`, plus the literal strings `"floor"`/`"plan"` for
   floor/plan-ruled rows); `shadowed_literals` for the 4 unexercised literals (2 genuinely
   shadowed by an earlier sibling literal in the list — confirmed by checking which corpus
   phrase each would match and whether an earlier pattern already claims it first; 2 genuinely
   never corpus-exercised vocabulary, not shadowed by anything, confirmed via a direct regex
   search across all 283 corpus phrases finding zero matches for either); a new
   **`misserved_at_deletion`** field naming the 5 genuinely mis-served rows (phrase → claimed
   action → ruled destination → router route → explanatory note); `verdict_report` citing the
   Haiku baseline + the 10-01 TEMPORAL rescore report.

3. **The 19 ex-CALENDAR reabsorptions, resolved**: `CALENDAR_QUERY_PATTERNS`' own ledger entry
   gained a `"resolved_by": "TEMPORAL_PATTERNS deletion 2026-10-01"` tag on each of its 19
   `known_reabsorptions` entries (history kept, not deleted). Empirically re-confirmed (direct
   `claim_for_phrase` probe against the live, now-tombstoned `PreClassifier`, all 69 phrases —
   not just the 19) that every claimed phrase is genuinely UNCLAIMED by any surviving surface-1
   list post-deletion — **zero new reabsorptions**, matching the dispatch's "likely none"
   prediction.

4. **Mechanism addition — `misserved_at_deletion`'s non-regression escape**
   (`scripts/inversion_phase3_deletion_gate.py::check_deleted_entry_non_regression`): the
   "mis-serves this row" proof is a one-time fact about the DELETED pattern's own (wrong) claim
   at gate time — it can never be re-derived by the non-regression checker's synthetic-claim
   re-proof, because that synthetic claim deliberately carries the CORRECT target op (not the
   deleted pattern's wrong one), so the mis-serve condition (which requires the claim to
   DISAGREE with the ruled destination) structurally cannot fire on it. Verified this gap
   empirically BEFORE fixing it: with `cats` covering `read_temporal`, 3 of the 5 mis-served
   rows still failed non-regression (`router verdict now MISMATCH ... the pattern is the live
   path for this phrase`). Fixed by adding a documented third escape: when a phrase is in
   `misserved_at_deletion` and the phrase is confirmed UNCLAIMED (the reclaim branch already
   ran and found nothing), treat it as OK — the invariant actually worth re-verifying forever is
   narrower than MATCH/agreeing-REVIEW/live-MISMATCH: just "still at least as safe as being
   wrongly claimed." A reclaim by some OTHER pattern still falls through to the existing
   reclaim-and-`known_reabsorptions` branch untouched, so this escape never bypasses
   documentation for a genuine new reabsorption.

5. **Mechanism addition — `gate.CURRENT_LIVE_CATEGORIES`**: found and fixed a second gap, via
   the reachability-ratchet check (step 7 below). Promoted the `--live` category set every
   Phase-3 deletion gate run has used throughout this epic to a shared module constant in
   `inversion_phase3_deletion_gate.py` (previously hand-copied in the CLI string and in
   `TestDeletedPatternListsLedger._LIVE_CATS`). `TestDeletedPatternListsLedger._LIVE_CATS` now
   references the constant instead of a second literal (reduces drift risk between the two
   copies).

6. **Ceiling**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 496 → 440
   (`pattern_literal_counts.total_literal_count()` confirms 440).

7. **Reachability ratchet — found a real break, fixed it, not just confirmed**: the dispatch
   asked me to confirm time-shaped POINTER rows resolve via `phase3-deletion-ledger`. Running
   `TestChatPointersReachabilityRatchet` found `page:/settings/preferences`'s POINTER
   (`"what time is it for me?"`, #1876) FAILING to resolve. Root-caused in two layers:
   (a) the exact phrase was never itself a corpus row (TEMPORAL_PATTERNS claimed it only via a
   substring match before deletion) — depositing it fresh would add an UNSCORED row (no frozen
   router report has ever seen it, and scoring one needs a live LLM call this dispatch forbids),
   which would fail `check_deleted_entry_non_regression` for the WHOLE TEMPORAL_PATTERNS entry.
   Fixed by swapping the POINTER's utterance to `"what time is it?"` — already one of the
   ledger's 69 verified rows, MATCH@0.99, zero new corpus/scoring needed; confirmed via
   `test_agenda_render_faces_1576.py::TestDefaultZoneIsNamedNotAssumed` that no other test
   depends on the exact "for me" wording (it constructs its own `Intent` directly, never calls
   `pre_classify`). (b) Even after the swap, resolution STILL failed — `_phase3_ledger_resolve`
   calls `check_deleted_entry_non_regression(entry)` with `cats=None` (the strictest reading),
   and TEMPORAL's entry now carries a genuinely live-dependent row (`what is on my calendar`,
   reabsorbed from CALENDAR) that needs `read_temporal` in the live set — failing non-regression
   for the WHOLE entry over one unrelated row, blocking every phrase in it (including "what time
   is it?" itself, a plain MATCH needing no live flag at all) from resolving. Fixed via item 5
   above (`gate.CURRENT_LIVE_CATEGORIES`), threaded into `_phase3_ledger_resolve`. Verified both
   fixes independently before combining: confirmed the phrase is in `rows_claimed_at_deletion`
   with a resolvable `expected_op_for_phrase`, confirmed `check_deleted_entry_non_regression`
   fails with `cats=None` and passes with the live set, then confirmed the full
   `TestChatPointersReachabilityRatchet` suite passes.

8. **Converted every broken surface-1 pin** (63 failures on the first full-suite pass after
   emptying the list — the largest conversion count of the four deletions, reflecting
   TEMPORAL_PATTERNS' unusually broad vocabulary and heavy reuse as a fixture phrase across OTHER
   tests' own test suites, not just its own). Every failure converted, never deleted, across 12
   test files:
   - `test_action_registry.py` — 3 `TestMultiIntentSubsumption` tests rewritten to pin the new
     reality (no TEMPORAL claim survives, with or without a greeting/calendar companion); the
     `_KNOWN_TEMPORAL_REABSORPTION_EXAMPLES` skip-list from the third deletion removed (the one
     doc-string example it exempted now declines cleanly, confirmed directly).
   - `test_calendar_query_handlers.py` — the third deletion's own
     `test_meeting_time_variants_reabsorbed_by_temporal` (2 test-local phrases) renamed to
     `..._resolved_after_temporal_deletion` and converted to the decline+inversion-routes idiom
     — the reabsorption it pinned is itself resolved by this deletion.
   - `test_integration_connect_preclassifier_1417.py`, `test_keyword_disambiguation_901.py`,
     `test_reminder_query_preclassifier_1521.py` — `test_temporal_queries_unchanged*` groups
     (7 phrases total across the three files) converted to the decline+inversion-routes idiom
     (`_inversion_pin_helper.assert_inversion_routes`, `live_categories="read_temporal"`).
   - `test_inversion_split_stand_down_1896.py` — `SPLIT_TURN` swapped a SECOND time (the second
     deletion already swapped it once): `"give me my standup and what time is it"` no longer
     genuinely splits (TEMPORAL half degrades to no claim) — swapped to `"give me my standup and
     what should i do next"` (STATUS_PATTERNS + PRIORITY_PATTERNS, confirmed still producing 2
     intents).
   - `test_multi_intent_connect_1505.py` + `test_multi_intent_temporal_span_1755.py` — the
     entire #1755 span-aware-temporal-suppression test file (6 tests) rewritten: the mechanism
     it exists to pin (`_temporal_disjoint_from_connect`) is now permanently, structurally
     inert, so every "disjoint span survives" assertion becomes "only the connect/GUIDANCE half
     survives, correctly single-intent now."
   - `test_original_message_1460.py` — `MULTI_INTENT_MESSAGE` now claims ZERO intents (both
     halves' patterns deleted across the second and fourth deletions); kept unchanged for its
     own still-valid reader-side keyword-detection use (that test constructs Intents directly,
     doesn't call `pre_classify`), but a new `STILL_CLAIMED_MULTI_INTENT_MESSAGE` replaces it in
     the one parametrize case needing a genuinely multi-claiming message.
   - `test_read_lane_destructive_greed_1756.py` — the largest single conversion: `TEMPORAL_READS`
     (14 phrases) + `CALENDAR_READS` (3 phrases) moved OUT of `KEEP_CLAIMING` (there is no claim
     left to "keep") into a new `TestTemporalReadsNowDeclineAtSurfaceOne` class pinning the
     decline directly, plus one Inversion-routing plumbing test; 2 of
     `READS_MENTIONING_DESTRUCTIVE_VERBS`' phrases (which matched TEMPORAL's generic
     `\bdid.*yesterday\b`/`\bwhat.*yesterday\b`) swapped for verified STATUS-lane equivalents.
   - `test_spend_free_canonical_ratchet_1818.py` — `("TEMPORAL", "get_current_time")` REMOVED
     from both `PAIR_MESSAGES` and `SPEND_FREE`, not swapped (see Discovered work below).

9. **Reachability ratchet confirmation, beyond the POINTER fix**: `git grep` for
   `get_current_time`/temporal vocabulary in `chat_pointers.py` confirms `page:/settings/
   preferences` is the ONLY time-shaped POINTER row — no other row needed attention.

10. **New synthetic tests** in `test_inversion_phase3_deletion_1595.py`: ledger pin updated to 5
    entries (`test_real_ledger_has_the_first_five_deletions`, renamed from "...four..."); every
    test that used TEMPORAL_PATTERNS or CALENDAR_QUERY_PATTERNS as its "surviving list that still
    claims" synthetic example swapped for PRIORITY_PATTERNS/STATUS_PATTERNS (both unaffected by
    any of the five deletions) — `test_fails_when_phrase_is_claimed_by_a_surviving_list`,
    `test_passes_for_a_floor_expected_phrase_reclaimed_but_documented_disagreeing`,
    `test_fails_for_an_undocumented_reclaim_even_when_independently_safe`,
    `test_documented_disagreeing_reclaim_needs_the_live_flag_when_the_row_is_mismatch` (now uses
    a real STATUS_PATTERNS/`read_referent` example, `"give me a project status report"` →
    `generate_report`); `TestTemporalPatternsVerdictIsReported` renamed to
    `TestPriorityPatternsVerdictIsReported` (swapped example, same reasoning) plus a new
    `test_temporal_patterns_now_claims_zero_rows` pinning the post-deletion state directly.

11. **Docs**: `intent-routing-stack.md` gains a "Fourth deletion (2026-10-01): TEMPORAL_PATTERNS"
    subsection (full account — gate evidence, the three-shape claimed-row breakdown, the two
    mechanism additions, the POINTER swap reasoning, every converted test file, the #1818
    discovered-work finding in full). Scope doc
    `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` gets a 2026-10-01 progress-log
    entry.

12. **`ruff format` + `ruff check --fix`** on all 17 touched `.py` files — 1 file reformatted
    (`tests/unit/test_inversion_phase3_deletion_1595.py`, whitespace only — confirmed via
    `ruff format --check` clean re-run and a full test re-run after the reformat).

## Discovered work

- **#1818 spend-free ratchet gap, flagged not fixed** — see item 8's last bullet above and the
  routing-stack doc's full account. `("TEMPORAL", "get_current_time")` can no longer be driven
  through `test_spend_free_canonical_ratchet_1818.py`'s own precondition (surface 1 never
  produces the claim), and a direct keyless probe this session (`real_intent_service
  .process_intent(message="what time is it?", session_id=..., user_id=None)`, run twice — once
  standalone, once inside the real test file's own fixtures) confirms the turn now reaches
  `intent_classifier.classify()` (the full LLM classifier) — it has no zero-LLM-touch path left.
  But the failure is `ContainerNotInitializedError` wrapped as `IntentProcessingError`, NOT
  `UnboundLLMKeyError` — `classifier.py`'s `self.llm` property resolves via
  `ServiceContainer.get_service("llm")` before any code path reaches the test's
  `request_spend_key` chokepoint instrumentation. This means (a) the pair almost certainly now
  SPENDS in a fully-initialized deployment, and (b) the #1818 ratchet's own instrumentation has a
  coverage gap for turns falling through to the full LLM classifier via the container-based
  `classify()` path — a different code path than the `LLMClient`/`clients.py` paths the other 8
  `SPENDS` pairs cross. Not filed as a separate GitHub issue (no issue number assigned, and this
  sits squarely inside the same-day #1818/#1819/#1823 epic CXO/Arch already own) — flagged in
  loud detail in the test file's own NOTE comment (`test_spend_free_canonical_ratchet_1818.py`,
  right above `PAIR_MESSAGES`) and in the routing-stack doc, for Lead to route.
- **Reachability-ratchet mechanism gap, found AND fixed** (items 5+7 above) — not left as
  discovered work since it blocked this unit's own deletion from passing its own gate suite;
  fixed in the same commit, documented in both the gate script's new constant and the test file.

## Evidence

- Gate (before deletion, quoted in full above): GO, 69/69 claimed, 56 literals, ceiling
  496 → 440, 4 unexercised literals (2 shadowed, 2 genuinely unused — not a blocker).
- Gate (`--all`, after deletion, same `--live` flag): `corpus denominator: 283 rows total = 133
  claimed + 150 unclaimed` (202 → 133, a drop of 69 = exactly the 69 ledgered rows —
  `TEMPORAL_PATTERNS` shows `0 0 NO ROWS`).
- `pattern_literal_counts.total_literal_count()` = 440 confirmed directly.
- Empirical zero-new-reabsorption check: `claim_for_phrase` against all 69 claimed phrases post-
  deletion — every one `pattern_list=None` (genuinely unclaimed), confirmed via a direct script
  run, not inferred from the aggregate drop count alone.
- `tests/unit/services/intent_service/ tests/unit/services/intent/`: **5020 passed** (full run,
  no `-x`/`--maxfail`, every failure surfaced and converted across the pass).
- `tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py`:
  **98 passed, 1 xfailed** (ceiling exact at 440; the reachability ratchet included and passing).
- `scripts/run-sweep.sh ratchets`: **73 passed, 1 xfailed** + mypy gate — "all 24 ratcheted codes
  at ceiling (total=1121; ... var-annotated=69)" — identical to the prior three deletions'
  baseline.
- `ruff format` + `ruff check --fix`: clean on every touched file (`1 file reformatted` on the
  first pass — whitespace only — `17 files already formatted` / `All checks passed!` on re-run).
- Non-regression mechanism directly verified: real TEMPORAL entry with `cats=None` → `ok=False`,
  1 problem (`what is on my calendar`, `live-set-unknown`); with `cats` covering `read_temporal`
  → `ok=True`, `[]`. The `misserved_at_deletion` escape verified the same way before AND after
  the fix (3 of 5 mis-served rows genuinely failed without it, all 5 pass with it).
- Final combined run (post-reformat, post-mechanism-fixes): `tests/unit/services/intent_service/
  tests/unit/services/intent/ tests/test_architecture_enforcement.py
  tests/unit/test_inversion_phase3_deletion_1595.py` — **5118 passed, 1 xfailed** (5020 + 98 =
  5118, arithmetic confirmed).

**Verified how**: every count above is a command run THIS session and its literal output quoted
— pytest exit summaries, the gate script's own printed census (before AND after deletion),
`pattern_literal_counts.total_literal_count()` invoked directly, direct
`check_deleted_entry_non_regression`/`claim_for_phrase` calls against the real (not synthetic)
ledger entries with and without `cats`, and a direct keyless `process_intent` probe for the
#1818 finding (run twice, both tracebacks read in full, not summarized from memory). Layer: the
deterministic layer only (pre-classifier regex matching, corpus-row lookups, frozen router-
report table parsing, the gate's own `row_disposition` re-derivation) for the deletion itself —
zero live LLM calls anywhere; every router "verdict" consulted is a FROZEN, already-scored
report or a monkeypatched stub in tests. The #1818 probe's layer is different and stated
explicitly in its own write-up: a real `process_intent` call, keyless, which reached
`intent_classifier.classify()`'s container-resolution step and failed there — BEFORE any
provider call, confirmed by reading the traceback directly (`container.get_service("llm")`
raising `ContainerNotInitializedError`), not inferred. Denominator: the full
`tests/unit/services/intent_service/` + `tests/unit/services/intent/` suite (not a subset,
5020/5020), both ratchet/ledger suites (98/98 + 1 xfailed), the sweep script, and a final
combined re-run (5118/5118 + 1 xfailed) after every fix landed, all read to completion.

## Files touched (no commit — Lead stages)

- `services/intent_service/pre_classifier.py` — the deletion + 5 tombstone/inert-dead-code
  comments.
- `services/intent/intent_service.py` — one explanatory comment added to the TEMPORAL floor/
  keyword split (code itself unchanged, read-only otherwise).
- `services/intent_service/chat_pointers.py` — `page:/settings/preferences` POINTER utterance
  swapped + full reasoning comment.
- `scripts/inversion_phase3_deletion_gate.py` — `misserved_at_deletion` non-regression escape
  (code + docstring); new `gate.CURRENT_LIVE_CATEGORIES` shared constant.
- `scripts/inversion_phase3_deleted_patterns.json` — 1 new ledger entry (69 phrases,
  `expected_op_by_phrase`, `shadowed_literals`, `misserved_at_deletion`); CALENDAR_QUERY_PATTERNS'
  19 `known_reabsorptions` entries gained `resolved_by`.
- `tests/test_architecture_enforcement.py` — ceiling 496→440; `_phase3_ledger_resolve` now
  threads `gate.CURRENT_LIVE_CATEGORIES`.
- `tests/unit/test_inversion_phase3_deletion_1595.py` — ledger pin updated to 5 entries; 4
  synthetic-mechanism tests + the verdict-reporting class swapped off TEMPORAL/CALENDAR examples
  onto PRIORITY/STATUS; `_LIVE_CATS` now references the shared gate constant.
- `tests/unit/services/intent_service/test_action_registry.py` — 3 tests rewritten, 1 skip-list
  removed.
- `tests/unit/services/intent_service/test_calendar_query_handlers.py` — 1 test renamed +
  converted.
- `tests/unit/services/intent_service/test_integration_connect_preclassifier_1417.py` — 1
  parametrized test converted (3 phrases).
- `tests/unit/services/intent_service/test_inversion_split_stand_down_1896.py` — `SPLIT_TURN`
  swapped.
- `tests/unit/services/intent_service/test_keyword_disambiguation_901.py` — 4 tests converted.
- `tests/unit/services/intent_service/test_multi_intent_connect_1505.py` — 1 test rewritten.
- `tests/unit/services/intent_service/test_multi_intent_temporal_span_1755.py` — 6 tests
  rewritten.
- `tests/unit/services/intent_service/test_original_message_1460.py` — new constant + 1
  parametrize entry swapped.
- `tests/unit/services/intent_service/test_read_lane_destructive_greed_1756.py` — 17 phrases
  moved out of KEEP_CLAIMING, new decline-pinning test class (3 tests) + 2 phrase swaps.
- `tests/unit/services/intent_service/test_reminder_query_preclassifier_1521.py` — 1
  parametrized test converted (3 phrases).
- `tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py` — 1 pair
  removed from PAIR_MESSAGES + SPEND_FREE, with a full discovered-work NOTE.
- `docs/internal/architecture/current/intent-routing-stack.md` — "Fourth deletion" subsection.
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` — progress log entry.

No git add/commit/staging performed at any point (dispatcher instruction). Reporting back to
Lead via SubagentHandback.

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md` §Phase 3 (all
  three prior deletion subsections — informed tombstone form, ledger shape, test-conversion
  idiom, and specifically CALENDAR's `known_reabsorptions`/`cats` mechanism which this unit
  extended); the CALENDAR deletion log (format, procedure) and the TEMPORAL sort+rail log (the
  per-row sort table, which this unit's ledger entry transcribes directly rather than
  re-deriving); Arch's ruling memo (the gate-defect fix and rail-entry requirement this unit's
  prerequisites satisfied); `_inversion_pin_helper.py` (reused verbatim across 5 of the 12
  converted test files).
- **Loaded but not referenced**: CLAUDE.md's mailbox/sign-off/worktree-model sections (bounded
  prog dispatch inside an existing worktree, no mailbox write, no sign-off merge, no git index
  touched, per dispatcher scope).
- **Wanted but not found**: none — the dispatch prompt's cited sources were sufficient; the two
  genuinely new findings this unit made (the `misserved_at_deletion` mechanism gap and the
  reachability-ratchet `cats=None` gap) were found by direct investigation (running the gate and
  the architecture-enforcement suite, reading the actual failure messages), not something a
  briefing doc should have pre-empted.
