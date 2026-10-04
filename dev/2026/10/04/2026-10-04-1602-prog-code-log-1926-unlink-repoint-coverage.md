# 2026-10-04 1602 — Coding Agent (prog), model Sonnet, dispatched by Lead

Role: Coding Agent (prog), one-shot dispatch. Branch: `claude/lead-cycle`
(shared worktree — did NOT commit/push; Lead reviews and commits).

## Task

Lead dispatched two units from Arch's ruling (`mailboxes/lead/inbox/rule-arch-to-lead-cc-cxo-cio-exec-
unlink-repoint-claim-connect-corpus-coverage-health-gate-inert-2026-10-04.md`, §1 + §2):

- **Unit 1**: re-point `unlink_repo`'s surface-1 claim (move the 3 unlink literals out of
  `REPO_MANAGEMENT_PATTERNS` into a new `REPO_UNLINK_PATTERNS`, claimed as `unlink_repo` in both claim
  tables) so the turn reaches the already-built DESTRUCTIVE rail's #1190 confirm.
- **Unit 2**: make `TestExecuteVocabCoverage` corpus-driven (Arch §2) — expect `connect` to force itself
  into `_EXECUTE_RE`.

Full detail written to `docs/internal/architecture/current/intent-routing-stack.md` (new section,
"`unlink_repo`'s CLAIM re-pointed, corpus-driven `_EXECUTE_RE` coverage built") — not duplicated here.

## What shipped

**Unit 1** (`services/intent_service/pre_classifier.py`):
- New `REPO_UNLINK_PATTERNS` (3 literals: unlink / remove...from / disconnect...repo), moved verbatim out
  of `REPO_MANAGEMENT_PATTERNS`.
- Claimed as `(PORTFOLIO, unlink_repo)` in `pre_classify`'s if-chain, checked BEFORE
  `REPO_MANAGEMENT_PATTERNS`.
- Same ordering added to `detect_multiple_intents`'s `pattern_groups` tuple list.
- `TestExtractionPatternRatchet` "pre-classifier" ceiling: unchanged at 155 (verified — pure move, sum
  identical; `test_extraction_ratchet_stays_tight` green with zero ceiling edit).
- `tests/unit/services/intent_service/test_repo_management.py::test_unlink_patterns_detected`: updated
  expectation from `manage_repos` to `unlink_repo` (the one test directly exercising
  `PreClassifier.pre_classify` for these phrases — everything else in that file tests
  `CanonicalHandlers._handle_repo_management` directly via a hand-built intent, untouched, out of my
  scope — that's the other lane's `canonical_handlers.py` residual).
- `tests/fixtures/inversion_corpus_phase0.yaml` + `scripts/build_inversion_corpus_phase0.py` (`HAND_ROWS`):
  the 3 unlink rows' `expected:` changed from `action:manage_repos` to `action:unlink_repo`, with a
  `RE-POINTED 2026-10-04` note citing the ruling. Regenerated the yaml via the builder script — diff
  confined to exactly those 3 rows (verified with `git diff --stat` + full diff read).
- `tests/unit/services/intent_service/test_inversion_write_allowlist_unlink_repo_1926.py`: module
  docstring updated — it previously stated "the live router... currently emits manage_repos; this unit
  does not change that," which is now stale. Replaced with an accurate note and an explicit flag that the
  surface-2 residual (Arch's own named follow-up) is NOT closed here.
- Did NOT touch `canonical_handlers.py`, `check_autoclose_keywords.py`, or `.claude/hooks` (other lane's
  files, per dispatch instructions) — confirmed via `git status` before finishing: both still show as
  modified from before I started, unchanged by me.

**Unit 2** (`tests/test_architecture_enforcement.py`, `TestExecuteVocabCoverage`):
- Added `_repo_management_list_literals`, `_corpus_rows`, `_write_or_allowlisted_destructive_corpus_rows`
  helpers + 3 new test methods: `test_corpus_scope_denominator_is_known`,
  `test_every_corpus_write_phrase_classifies_execute`, `test_destructive_corpus_rows_are_named_exemptions`.
- Resolution: same alias map `inversion_phase3_deletion_gate.py`'s `expected_action_is_live` uses
  (`derive_routing_grammar().alias_to_canonical` + `get_action_workflows()`), with one named exception for
  `manage_repos` (not yet re-pointed for link/list) — resolved via `REPO_MANAGEMENT_PATTERNS`' own
  link-shaped-vs-list-shaped sub-grouping (last 3 literals = list → `list_repos`, READ, skip; everything
  else = link → `link_repo`, WRITE, in scope), read by identity against the production list with a
  vacuity assert (`len == 9`, list-literal fragment checks), never a second hand-matched regex copy.
- **Denominator: 28 of 498 corpus rows** resolve into scope.
- Ran the new test against the OLD `_EXECUTE_RE` (monkeypatched in a throwaway interpreter, not by
  inspection) to confirm it's NOT vacuous — it failed on exactly 4 phrases before the fix, confirming the
  test actually exercises the gap.
- **Verb/vocabulary added to `_EXECUTE_RE`** (`services/intent_service/collaboration_gate.py`):
  - `connect` (bare verb, added to the existing alternation) — forced by `"connect my repository to the
    project"` + `"connect octocat/hello-world to the project"` (both resolve to `link_repo`, WRITE). This
    is exactly Arch's named prediction, landing from real corpus evidence, not by hand.
  - Two anchor-phrase branches (NOT bare verbs — neither idiom is verb-initial): `don'?t\s+let\s+me\s+
    forget\b` and `(?:i\s+)?need\s+to\s+remember\b` — forced by `"don't let me forget to submit the
    report"` + `"I need to remember to submit my timesheet"` (both resolve to `create_reminder`, WRITE).
    **This second gap was NOT anticipated by Arch's memo** (which only named "connect") — discovered
    building the corpus-driven scan. Flagging it clearly: before this fix, a confidently pre-classified
    `create_reminder` turn phrased this way read AMBIGUOUS in `classify_framing`, which (per
    `consent_gate.decide_consent`'s PRIVATE/WRITE/ambiguous/default-mode cell) arms an unnecessary
    COLLABORATE "shall I create this?" pause for a request the pre-classifier was never unsure about. I
    judged this a genuine, verified production gap squarely inside the #1509 contract ("covers EVERY
    WRITE-effect rail action") and in scope for "add whatever the test demands," rather than something to
    leave failing or paper over with a `framing: question` marker (these are not questions). **Flagging
    for Lead/Arch review** since it's a judgment call beyond the literal "add connect" instruction — happy
    to revert to a narrower fix (e.g. a corpus `framing:` exemption instead) if that's preferred.
  - Did NOT add `unlink`/`remove`/`disconnect` (the DESTRUCTIVE-exempted verbs) — `unlink_repo` is already
    in `EXEMPT_ALLOWLISTED_DESTRUCTIVE`; `test_destructive_corpus_rows_are_named_exemptions` confirms both
    DESTRUCTIVE-resolved corpus actions (`delete_todo`, `unlink_repo`) are named there.
  - Did NOT add any verb the test didn't demand (checked: `list_repos`-resolved rows are READ, correctly
    out of scope and untouched).
- Regression-checked the regex change against every `collaboration_gate`/`consent_gate`/`drafted_issue`/
  reminder-adjacent test file in `tests/unit/services/intent_service/` (974 tests across two batched runs)
  — all green, no existing test pinned a different framing for a phrase this change touches.

## Verified how

- `pytest tests/unit/services/intent_service/test_repo_management.py
  tests/unit/services/intent_service/test_inversion_write_allowlist_unlink_repo_1926.py` — 53 passed.
- `pytest tests/test_architecture_enforcement.py -k "ExtractionPattern or PreFloorDispatch"` — 5 passed
  (ceiling unchanged, confirmed by the tightness test, not just my own arithmetic).
- `pytest tests/test_architecture_enforcement.py -k TestExecuteVocabCoverage` — 7 passed (4 pre-existing +
  3 new).
- `pytest tests/unit/services/intent_service/test_subsumption_portfolio_write_family_1884.py
  test_inversion_cross_family_release_1920.py test_inversion_write_allowlist_1677.py
  test_destructive_confirm_1190.py test_read_portfolio_rail_1595.py` — 89 passed.
- Two batched regression runs across 32 `collaboration_gate`/`consent_gate`/`drafted_issue`/reminder test
  files — 403 + 571 = 974 passed, no failures.
- `scripts/inversion_phase3_deletion_gate.py --list REPO_MANAGEMENT_PATTERNS --live manage_repos` (9/9
  claimed, link+list only) and `--list REPO_UNLINK_PATTERNS --live unlink_repo` (3/3 claimed) — confirms
  the move landed cleanly on both sides.
- `ruff check` + `ruff format --check` on all 6 touched files — clean.
- Full required suite, all three Lead-specified commands, zero `FAILED` lines:
  - `pytest tests/unit tests/test_architecture_enforcement.py` (ignoring archive/integration/mcp/dev
    paths): **12447 passed**, 228 skipped, 3 deselected, 1 xfailed.
  - `pytest tests/intent/`: **205 passed**, 2 skipped, 93 deselected.
  - Keychain-stripped `pytest tests/unit/services/intent_service/ tests/test_architecture_enforcement.py`:
    **5201 passed**, 3 deselected, 1 xfailed.
- Layer: pure unit-test + regex-classifier layer (m-43) — no LLM calls, no live server, no DB writes
  beyond the existing test fixtures' own mocking.

## Discovered work

- The `create_reminder` idiom gap above (not filed as a separate GH issue — flagged inline in this log
  and in the routing-stack doc instead, since it was fixed in the same unit; Lead/Arch can decide whether
  it warrants its own issue for the record).
- Residual named by Arch (§1, surface-2 `manage_repos` misclassification for an unlink phrase the 3
  literals miss) is explicitly NOT closed — flagged, not silently assumed resolved.

## Files changed

- `services/intent_service/pre_classifier.py`
- `services/intent_service/collaboration_gate.py`
- `tests/test_architecture_enforcement.py`
- `tests/unit/services/intent_service/test_repo_management.py`
- `tests/unit/services/intent_service/test_inversion_write_allowlist_unlink_repo_1926.py`
- `scripts/build_inversion_corpus_phase0.py`
- `tests/fixtures/inversion_corpus_phase0.yaml` (generated, regenerated via the builder)
- `docs/internal/architecture/current/intent-routing-stack.md`
- `dev/2026/10/04/2026-10-04-1602-prog-code-log-1926-unlink-repoint-coverage.md` (this log)

## Memory & briefing surfaces referenced this session

- **Referenced**: CLAUDE.md "Intent dispatch" (no new elif chains — not touched); the
  intent-routing-stack doc's existing `manage_repos`/`unlink_repo` sections (informed where to append and
  the established prose shape); Arch's ruling memo (authority for both units).
- **Loaded but not referenced**: MEMORY.md feedback/project index (dispatched as prog, not a duty-cycle
  role — did not need it).
- **Wanted but not found**: none.
