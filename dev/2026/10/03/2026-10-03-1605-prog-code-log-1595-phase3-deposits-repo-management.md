# 2026-10-03 1605 — prog (Coding Agent) — #1595 Phase 3 REPO_MANAGEMENT_PATTERNS deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for `REPO_MANAGEMENT_PATTERNS` (12 literals) in
`services/intent_service/pre_classifier.py` (read only — no literal edited/deleted). Touched only
the corpus builder, the fixture yaml, the pinned corpus-size test, the scope doc, and this session
log. NO LLM calls made anywhere. Did not touch git index (dispatcher instruction). Did not touch
`tests/intent/` (another lane was concurrently active there this session) or `services/`.

## Read first

- `dev/2026/10/02/2026-10-02-1559-prog-code-log-1595-phase3-deposits-discovery-analysis-trust-memory.md`
  — template lane: row-shape convention, two-step empirical verification
  (`pre_classify_with_pattern_list` for list identity + `_first_pattern_match` for literal
  identity), the mathematically-unreachable shadow argument.
- `services/intent_service/pre_classifier.py` — read `REPO_MANAGEMENT_PATTERNS` (1148-1164),
  `SET_DEFAULT_REPO_PATTERNS`/`GET_DEFAULT_REPO_PATTERNS` (1109-1145, checked BEFORE
  REPO_MANAGEMENT so "default repo" phrasings don't collide), the single-intent claim branch at
  1420-1427 (checked right after DOCUMENT_QUERY, before PORTFOLIO/GUIDANCE/INTEGRATION_CONNECT —
  no `_is_destructive_ask` guard, unlike MEMORY_PATTERNS just above it), `INTEGRATION_CONNECT_
  PATTERNS`/`INTEGRATION_CONNECT_BLOCKERS` (858-876, Arch-ratified #1417, the repo-word/owner-repo
  guard), and the multi-intent group table (2190-2266) where INTEGRATION_CONNECT (2225) and
  REPO_MANAGEMENT (2255) appear in the OPPOSITE order from the single-intent path — moot for a
  repo-bearing phrase since the single-intent path (what `pre_classify_with_pattern_list` calls,
  the gate's claim source) checks REPO_MANAGEMENT first regardless.
- `services/intent_service/canonical_handlers.py` — `_handle_repo_management` (5099-5510): reads
  the original message with its OWN regex set (link/unlink/list sub-operation detection,
  independent of the pre-classifier's claim), confirming all three verbs (link/connect/add) share
  one regex group and dispatch identically; confirmed the UNLINK branch (5340-5413) executes
  `repo_repo.unlink_from_project` directly with no `destructive_confirm` gate.
- `services/intent_service/action_registry.py` — `manage_repos` is `ActionDisposition.CANONICAL`
  (line 121), `Verb.MANAGE` (545), with a real description (396-398) — a live wired handler, not a
  FLOOR destination like the four prior lists in this epic.
- `tests/fixtures/inversion_corpus_phase0.yaml` — grepped for "repo": the 2 existing
  REPO_MANAGEMENT rows ("link mediajunkie/test-piper-morgan to the project" → MATCH @0.95, "add a
  repo to my portfolio" → REVIEW, probe-row-7, DISAGREE) and the GUIDANCE-side "connect my
  slack/github/notion"/"link my google calendar" REVIEW rows (disjoint — none of those contain
  "repo", so INTEGRATION_CONNECT_BLOCKERS never engages).
- `docs/internal/architecture/current/*.md` — grepped for "add a repo to my portfolio" across all
  historical shadow-score/counterfactual reports to find WHY probe-row-7 disagreed (see Findings).

## What I did

1. Quoted the BEFORE gate command exactly as dispatched; confirmed 12 literals, 2/447 rows claimed.
2. Computed the exact unexercised-literal set via the gate's own `unexercised_literals(
   "REPO_MANAGEMENT_PATTERNS", rows_for_list)` (imported `inversion_phase3_deletion_gate`
   directly, not hand-counted): **10 of 12 unexercised**.
3. Read `_handle_repo_management` end to end to understand sub-operation dispatch: link/connect/
   add share one regex group (treated identically); unlink/disconnect/remove share another;
   show/list/view/which repos is the read path. The pre-classifier itself has no per-literal
   branching — all 12 literals claim the single action `manage_repos` (category PORTFOLIO),
   matching the "single hardcoded action for the whole list" shape of prior deposit lanes.
4. Investigated the dispatcher's named ambiguity question directly in code (not guessed): is
   "connect my repo to X" ambiguous between `manage_repos` and an INTEGRATION_CONNECT/github-
   connect flow? Found it RESOLVED: `INTEGRATION_CONNECT_BLOCKERS` (pre_classifier.py:862-868)
   explicitly documents "an owner/name slug or the word repo(sitory) means the repo-link lane (#862
   handles it earlier in the pass) — never integration setup" (Arch-ratified #1417, 2026-07-16).
   On the single-intent path (what the gate's claim computation actually calls),
   `REPO_MANAGEMENT_PATTERNS` is checked at line 1420 — well before `INTEGRATION_CONNECT_PATTERNS`
   at line 1835 — so a repo-bearing phrase never even reaches the integration-connect branch.
5. Checked whether this resolves-not-ambiguous finding should extend to the existing REVIEW anchor
   ("add a repo to my portfolio", probe-row-7). Traced every historical probe of that exact phrase
   across `docs/internal/architecture/current/`: the ONE disagreement
   (`surface1-counterfactual-results-2026-08-08.md` row 7) shows the router proposing a
   non-canonical `execution/add_repo_to_portfolio` @0.9 — not GUIDANCE/get_contextual_guidance, a
   different kind of disagreement entirely (a plausible-sounding but unwired action name, not an
   integration-connect mix-up). Every LATER re-probe (2026-09-25, 09-28 ×2, 10-01 ×2, 10-02)
   consistently shows the router AGREEING at `manage_repos@0.9-0.95`. Concluded: generalizing that
   REVIEW to the 10 new literals (by verb-family or genericity analogy) would not be
   evidence-backed — the anchor's own recent evidence leans AGREE, and the specific ambiguity type
   named in the dispatch is code-resolved. **All 10 new rows get `expected: action:manage_repos`,
   no REVIEW rows.**
6. Checked the destructive-confirm question (#1756 read-lane destructive greed) for unlink/remove/
   disconnect: `git grep destructive_confirm` + `_is_destructive_ask` across `services/`. Found
   `manage_repos`/`REPO_MANAGEMENT_PATTERNS` has NEITHER — no `_is_destructive_ask` guard at the
   pre-classifier claim site (unlike `MEMORY_PATTERNS` immediately above it, which does have one),
   and `_handle_repo_management`'s UNLINK branch executes the removal directly with no
   `destructive_confirm` wiring. This is a real gap (a destructive write with no confirm gate) but
   out of this unit's scope — reported inline per the established deposit-lane convention (not
   filed as a separate GitHub issue, matching the prior four lanes' practice for measurement
   findings), flagged for the Lead's disposition.
7. Drafted one natural phrase per unexercised literal, designed from the regex structure to (a)
   contain the exact substring each literal requires and (b) avoid interrupting words that would
   break adjacency-sensitive literals (notably literal 10 and 12, whose optional groups require
   nothing between the verb and the following required token — "show me my linked repos" would
   NOT match literal 10 because "me" breaks the `\s+(?:(?:my|the)\s+)?` adjacency; used "show my
   linked repos" instead). For the "which repos are linked" literal (11), reasoned from the regex
   that it is shadowed by literal 10 for ANY plural "which repos ... linked/connected" phrasing
   (10 matches first, checked earlier, and doesn't require "linked"/"connected" to follow), and
   that literal 11's own `(?:are\s+)?` alternation has no "is" option — so "which repo is linked"
   does not match literal 11 either. Used the one reachable shape: singular "repo" with direct
   verb-adjacent "connected" ("which repo connected to this project should I check" — a reduced
   relative clause, natural English).
8. Verified all 10 candidates empirically in one combined script against the REAL production
   matcher: `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name + action assertion)
   and `PreClassifier._first_pattern_match(cleaned, PreClassifier.REPO_MANAGEMENT_PATTERNS)`
   (literal-identity assertion). **All 10 passed on the first attempt — zero rewords needed, zero
   duplicate phrases** (checked against the existing corpus via grep first).
9. Deposited a HAND_ROWS block (10 rows) in `scripts/build_inversion_corpus_phase0.py`, after the
   existing MEMORY_PATTERNS block, before the closing `]`. `source` cites `phase3-conversion/
   REPO_MANAGEMENT_PATTERNS literal r"<literal>"` per row, matching convention. `category:
   PORTFOLIO` (matching the actual `IntentCategory.PORTFOLIO` the pre-classifier assigns — the 2
   existing anchor rows disagree with each other on this field, QUERY vs PORTFOLIO; picked the
   value that matches production truth). Two rows carry `notes:` documenting the ambiguity
   investigation (connect-generic) and the destructive-confirm gap (unlink) and the shadow
   reasoning (which-repo-connected), per the established REVIEW/notes convention.
10. Regenerated the corpus: `venv/bin/python scripts/build_inversion_corpus_phase0.py` — 447 → 457
    rows (+10). `git diff --numstat` on the yaml + builder: 151 insertions, 0 deletions total
    (purely additive). PORTFOLIO category denominator: 17 → 27.
11. Updated the pinned corpus total in `tests/unit/test_inversion_phase3_deletion_1595.py`:
    `test_claimed_plus_unclaimed_equals_corpus_size` 447 → 457 (claimed 65 → 75, unclaimed
    unchanged at 382 — confirmed by direct `gate.build_census(cats=None)` call using the test's
    own exact computation). Searched for other pinned `\b447\b` constants: `git grep -n "\b447\b"
    -- tests scripts` — only the just-fixed hit plus unrelated matches (the ledger JSON's
    historical notes, an unrelated large-text fixture line).
12. Re-ran the gate for REPO_MANAGEMENT_PATTERNS: 12/12 claimed (0 unexercised), still "GO
    (partial)" with all 12 literals now load-bearing survivors (the partial-verdict logic reports
    every claimed literal as a survivor when its row isn't a full-GO MATCH on a live op), every new
    row correctly UNSCORED (no router call made, no LLM calls anywhere in this unit — same
    2026-10-01 gate tightening every prior lane since has found).
13. Ran both dry-run validations — no LLM calls (each script self-reports this):
    - `inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls" self-reported (same
      pre-existing, unrelated TEMPORAL regression note the template lane also saw — not touched by
      this unit, no TEMPORAL literal involved).
    - `inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made" self-reported.
14. `ruff format` + `ruff check` on the touched `.py` files: `ruff check` was already clean; `ruff
    format --check` flagged the builder for reformatting (a long multi-line comment block), ran
    `ruff format` to fix, re-ran `--check` clean. `git diff --numstat` reconfirmed purely additive
    (0 deletions) after the reformat; regenerated the corpus yaml once more to confirm it's
    unaffected (byte-identical diff).
15. Tests (run together this turn, output quoted below):
    - `tests/unit/test_inversion_phase3_deletion_1595.py` +
      `tests/unit/test_inversion_phase3_surface2_floor_1595.py` +
      `tests/unit/test_inversion_phase1_shadow_score_1595.py` +
      `tests/test_architecture_enforcement.py` — **143 passed, 1 xfailed**, 0 failed.
    - Extraction ceiling re-confirmed **201** (unchanged) via direct
      `pattern_literal_counts.total_literal_count()` call — no `pre_classifier.py` literal
      edited/deleted in this unit.
16. Added a dated progress-log entry to
    `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.
17. Verified scope compliance via `git status --short` at session end: only
    `scripts/build_inversion_corpus_phase0.py`, `tests/fixtures/inversion_corpus_phase0.yaml`, and
    `tests/unit/test_inversion_phase3_deletion_1595.py` show as modified BY ME. `tests/intent/
    contracts/test_accuracy_contracts.py`, `test_bypass_contracts.py`,
    `test_multiuser_contracts.py`, `test_performance_contracts.py`, and `tests/intent/
    test_constants.py` also show modified — confirmed via `git diff --stat -- tests/intent/` these
    are a DIFFERENT, concurrently-active lane's edits (the dispatch explicitly warned "another lane
    is working there"); none created or touched by me. Git index not touched (nothing staged, per
    dispatcher instruction).

## Table: literal → phrase → expected → verified-claiming-literal

| literal | phrase | expected | verification |
|---|---|---|---|
| `\blink\s+(?:(?:my\|the\|a)\s+)?(?:repo(?:sitory)?)\s+(?:to\s+)` | "link my repository to the project" | `action:manage_repos` | pattern_list=REPO_MANAGEMENT_PATTERNS, action=manage_repos, matched literal = exact |
| `\bconnect\s+(?:(?:my\|the\|a)\s+)?(?:repo(?:sitory)?)\s+(?:to\s+)` | "connect my repository to the project" | `action:manage_repos` | same, exact — ambiguity investigated and resolved (see Findings) |
| `\bconnect\s+[\w.-]+/[\w.-]+` | "connect octocat/hello-world to the project" | `action:manage_repos` | same, exact |
| `\badd\s+[\w.-]+/[\w.-]+\s+to\s+` | "add octocat/hello-world to the project" | `action:manage_repos` | same, exact |
| `\bunlink\s+(?:(?:my\|the\|a)\s+)?(?:repo(?:sitory)?)` | "please unlink my repository from this project" | `action:manage_repos` | same, exact — no destructive-confirm gate (see Findings) |
| `\bremove\s+(?:(?:my\|the\|a)\s+)?(?:repo(?:sitory)?)\s+from\s+` | "please remove my repository from this project" | `action:manage_repos` | same, exact |
| `\bdisconnect\s+(?:(?:my\|the\|a)\s+)?(?:repo(?:sitory)?)` | "please disconnect my repository from this project" | `action:manage_repos` | same, exact |
| `\b(?:show\|list\|view\|which)\s+(?:(?:my\|the)\s+)?(?:linked\s+)?repos\b` | "please show my linked repos" | `action:manage_repos` | same, exact |
| `\bwhich\s+repos?\s+(?:are\s+)?(?:linked\|connected)\b` | "which repo connected to this project should i check" | `action:manage_repos` | same, exact — singular-repo reachable shape only (see Findings) |
| `\bshow\s+(?:project\s+)?repositories\b` | "can you show project repositories for this account" | `action:manage_repos` | same, exact |

All 10/10 reachable, verified on the first attempt, zero rewords needed.

## Findings

**Dispatcher's named ambiguity ("connect my repo to X": manage_repos vs INTEGRATION_CONNECT) —
investigated and RESOLVED, not live.** `INTEGRATION_CONNECT_BLOCKERS`
(`pre_classifier.py:862-868`, Arch-ratified #1417) explicitly blocks any phrase containing an
owner/name slug or the word repo(sitory) from the integration-connect lane, with the comment
naming this exact collision: "the repo-link lane (#862 handles it earlier in the pass) — never
integration setup." Independently, on the single-intent path (what `pre_classify_with_pattern_list`
— the gate's claim source — actually calls), `REPO_MANAGEMENT_PATTERNS` is checked at line 1420,
before `INTEGRATION_CONNECT_PATTERNS` at line 1835, so a repo-bearing phrase never reaches the
integration-connect branch regardless of the blocker. (The multi-intent group table at 2190-2266
checks them in the OPPOSITE order — INTEGRATION_CONNECT at 2225, REPO_MANAGEMENT at 2255 — but the
blocker still applies there, and this is moot for the single-intent claim the gate reads anyway.)

**The existing REVIEW anchor's DISAGREE does not generalize to these 10 literals.** "add a repo to
my portfolio" (probe-row-7) is REVIEW because of a ONE-TIME historical disagreement
(`surface1-counterfactual-results-2026-08-08.md`): the router proposed a non-canonical
`execution/add_repo_to_portfolio` @0.9 — a different unwired action name, not GUIDANCE/
get_contextual_guidance (so not the integration-connect ambiguity type at all). Every later
re-probe of the identical phrase (2026-09-25, two on 09-28, two on 10-01, 10-02) shows the router
AGREEING at `manage_repos@0.9-0.95`. Given this, I did not generalize REVIEW to any of the 10 new
rows by verb-family or generic-phrasing analogy — doing so would not be evidence-backed, and the
dispatch explicitly warns against inventing a ruling.

**No destructive-confirm guard on unlink/remove/disconnect (manage_repos is CANONICAL, not
FLOOR).** `REPO_MANAGEMENT_PATTERNS`'s claim branch (`pre_classifier.py:1420-1427`) has no
`_is_destructive_ask` guard, unlike `MEMORY_PATTERNS` immediately above it which does. At the
handler level, `_handle_repo_management`'s UNLINK branch (`canonical_handlers.py` ~5340-5413) calls
`repo_repo.unlink_from_project` directly with no `destructive_confirm` wiring (confirmed via
`git grep destructive_confirm` / `_is_destructive_ask` across `services/` — zero hits for
`manage_repos`/`unlink_repo`). This means "unlink my repo from X" / "disconnect my repo" / "remove
my repo from X" execute the removal immediately with no confirmation step — a real gap in the
#1756 destructive-ask-guard pattern applied elsewhere, but out of this unit's scope. Reported
inline per the established deposit-lane convention; not filed as a separate GitHub issue.

**No shadowed literals this unit.** All 12 literals (2 pre-existing + 10 new) are now claimed;
`unexercised_literals` returns empty post-deposit.

## Gate output — BEFORE

```
corpus denominator: 447 rows total = 65 claimed + 382 unclaimed

## REPO_MANAGEMENT_PATTERNS
literals: 12  |  rows claimed: 2/447
verdict: GO (partial) — 2 load-bearing literal(s) SURVIVE, deleting the other 10: ceiling 201 -> 191
  survives: r"\blink\s+[\w.-]+/[\w.-]+"  <- 'link mediajunkie/test-piper-morgan to the project'
  survives: r"\badd\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+to\s+"  <- 'add a repo to my portfolio'

rows claimed:
  [FAIL] "link mediajunkie/test-piper-morgan to the project" -> claim=manage_repos expected=action:manage_repos router=manage_repos@0.95 verdict=MATCH :: MATCH on a NON-LIVE op (not-live (no WorkflowEntry — the live consult dispatches rail keys only)) — the consult stands down, so deletion hands this phrase to surface 2; no surface-2 probe for this phrase
  [FAIL] "add a repo to my portfolio" -> claim=manage_repos expected=REVIEW router=manage_repos@0.9 verdict=REVIEW :: REVIEW-agrees (route=manage_repos == claim=manage_repos) but on a NON-LIVE op (not-live (no WorkflowEntry — the live consult dispatches rail keys only)); no surface-2 probe for this phrase
```

(Command: `scripts/inversion_phase3_deletion_gate.py --list REPO_MANAGEMENT_PATTERNS --live
create_reminder,create_todo,delete_todo,read_floor,read_referent,read_status,read_strategic,
read_synthesis,read_temporal`)

## Gate output — AFTER

```
corpus denominator: 457 rows total = 75 claimed + 382 unclaimed

## REPO_MANAGEMENT_PATTERNS
literals: 12  |  rows claimed: 12/457
verdict: GO (partial) — 12 load-bearing literal(s) SURVIVE, deleting the other 0: ceiling 201 -> 201
  survives: r"\blink\s+[\w.-]+/[\w.-]+"  <- 'link mediajunkie/test-piper-morgan to the project'
  survives: r"\badd\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+to\s+"  <- 'add a repo to my portfolio'
  survives: r"\blink\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+(?:to\s+)"  <- 'link my repository to the project'
  survives: r"\bconnect\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+(?:to\s+)"  <- 'connect my repository to the project'
  survives: r"\bconnect\s+[\w.-]+/[\w.-]+"  <- 'connect octocat/hello-world to the project'
  survives: r"\badd\s+[\w.-]+/[\w.-]+\s+to\s+"  <- 'add octocat/hello-world to the project'
  survives: r"\bunlink\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)"  <- 'please unlink my repository from this project'
  survives: r"\bremove\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+from\s+"  <- 'please remove my repository from this project'
  survives: r"\bdisconnect\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)"  <- 'please disconnect my repository from this project'
  survives: r"\b(?:show|list|view|which)\s+(?:(?:my|the)\s+)?(?:linked\s+)?repos\b"  <- 'please show my linked repos'
  survives: r"\bwhich\s+repos?\s+(?:are\s+)?(?:linked|connected)\b"  <- 'which repo connected to this project should i check'
  survives: r"\bshow\s+(?:project\s+)?repositories\b"  <- 'can you show project repositories for this account'

rows claimed:
  [FAIL] "link mediajunkie/test-piper-morgan to the project" -> MATCH (non-live op, as before)
  [FAIL] "add a repo to my portfolio" -> REVIEW-agrees (non-live op, as before)
  [FAIL] "link my repository to the project" -> claim=manage_repos expected=action:manage_repos router=None@None verdict=UNSCORED
  [FAIL] "connect my repository to the project" -> UNSCORED (same shape)
  [FAIL] "connect octocat/hello-world to the project" -> UNSCORED (same shape)
  [FAIL] "add octocat/hello-world to the project" -> UNSCORED (same shape)
  [FAIL] "please unlink my repository from this project" -> UNSCORED (same shape)
  [FAIL] "please remove my repository from this project" -> UNSCORED (same shape)
  [FAIL] "please disconnect my repository from this project" -> UNSCORED (same shape)
  [FAIL] "please show my linked repos" -> UNSCORED (same shape)
  [FAIL] "which repo connected to this project should i check" -> UNSCORED (same shape)
  [FAIL] "can you show project repositories for this account" -> UNSCORED (same shape)
```

Still GO (partial), 0 deletable this unit — correct and expected: every new row reads UNSCORED (no
router call made, no LLM calls anywhere in this unit). The Lead's budgeted scoring run resolves
MATCH/REVIEW/MISMATCH per row.

## New corpus total

447 → **457** rows (+10). Per-category denominators after rebuild: QUERY 129, TEMPORAL 69, STATUS
54, PRIORITY 44, **PORTFOLIO 27** (was 17), GUIDANCE 26, EXECUTION 26, DISCOVERY 25, MEMORY 17,
ANALYSIS 15, TRUST 11, CONVERSATION 5, SYNTHESIS 4, IDENTITY 3, PROVENANCE 2.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 457 rows (54 REVIEW), exit 0.
- `git diff --numstat tests/fixtures/inversion_corpus_phase0.yaml scripts/build_inversion_corpus_phase0.py`
  → `43 0` and `108 0` respectively — purely additive, zero deletions.
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls"
  self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made"
  self-reported.
- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list REPO_MANAGEMENT_PATTERNS --live
  create_reminder,create_todo,delete_todo,read_floor,read_referent,read_status,read_strategic,
  read_synthesis,read_temporal` → exit 0, corpus denominator 457 rows = 75 claimed + 382 unclaimed;
  REPO_MANAGEMENT_PATTERNS 12/12 claimed, GO (partial), all UNSCORED.
- `venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py
  tests/unit/test_inversion_phase3_surface2_floor_1595.py
  tests/unit/test_inversion_phase1_shadow_score_1595.py tests/test_architecture_enforcement.py
  -q -p no:cacheprovider` → **143 passed, 1 xfailed**, exit 0.
- `venv/bin/python -c "import sys; sys.path.insert(0,'scripts'); import pattern_literal_counts as
  plc; print(plc.total_literal_count())"` → **201**, unchanged (ceiling untouched — no
  pre_classifier literal edited/deleted; task's "no deletion in this unit" condition met).
- `venv/bin/ruff format` on `scripts/build_inversion_corpus_phase0.py` → 1 file reformatted (the
  new HAND_ROWS comment block); `ruff format --check` + `ruff check` on both touched `.py` files →
  clean after the reformat; `git diff --numstat` reconfirmed 0 deletions after the reformat, and
  the regenerated corpus yaml is unaffected.

## Files touched

- `scripts/build_inversion_corpus_phase0.py` (HAND_ROWS: +10 rows in one comment-headed block,
  after the MEMORY_PATTERNS block, before the closing `]`)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, purely additive, 447→457 rows)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (one pinned constant corrected 447→457, with
  updated docstring)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (dated progress-log entry added)
- This session log (new)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read only),
`services/intent_service/canonical_handlers.py` (read only), `services/intent_service/
action_registry.py` (read only), `tests/intent/` (another lane's concurrent edits, confirmed not
mine), `web/` (not touched, not relevant to this unit), any flag/env var,
`scripts/inversion_phase3_deleted_patterns.json` (no deletion performed), the gate script, the
ledger, GitHub.

## Verified how

- **Method**: computed the exact unexercised-literal set by importing and calling the gate's own
  `unexercised_literals()` against `build_census()`'s claimed rows for this list (not
  hand-counted). Read `_handle_repo_management`, `INTEGRATION_CONNECT_PATTERNS`/`_BLOCKERS`, and
  the single- vs multi-intent check ordering directly (not inferred) before drafting any phrase or
  deciding `expected`. Traced the existing REVIEW anchor's actual probe history across every
  historical shadow-score/counterfactual report in `docs/internal/architecture/current/` rather
  than assuming its REVIEW status generalizes. Drafted 10 phrases designed from the regex
  structure, then verified all 10 in one combined script run against the REAL production
  functions — `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name AND
  `intent.action` read directly) and `PreClassifier._first_pattern_match(cleaned,
  PreClassifier.REPO_MANAGEMENT_PATTERNS)` (literal-identity assertion) — with 0 failures and 0
  duplicate phrases (checked via `grep` against the existing corpus first) on the first attempt.
  Gate re-runs, pytest, ruff, and ceiling invocations were all run this turn via Bash and their
  output is quoted/counted above, not recalled from memory. `git diff --numstat` run and quoted
  directly to confirm purely-additive changes, re-confirmed after the ruff reformat. `git status
  --short` + `git diff --stat -- tests/intent/` run at session end to confirm scope compliance and
  attribute the concurrent lane's edits correctly.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by design of this unit —
  the Phase-1 router/LLM layer is deliberately UNSCORED here (no LLM calls made anywhere in this
  session, confirmed by each script's own self-report and the absence of any LLM-client invocation
  in the commands run). The CANONICAL/live-handler disposition was verified by reading
  `action_registry.py` and `canonical_handlers.py` directly, not inferred from behavior. The
  destructive-confirm gap was verified by `git grep` across all of `services/` for both
  `destructive_confirm` and `_is_destructive_ask`, not assumed from the absence of a comment.
- **Denominator**: 1 target list (REPO_MANAGEMENT_PATTERNS) — 10 of 12 previously-unexercised
  literals now have a corpus row; 0 of 12 shadowed or unreachable (all 10 drafted phrases matched
  their exact cited literal on the first attempt). Test denominator: 143/143 passed (plus 1
  pre-existing xfail) across all four specified test files run together in one invocation, not
  separately. Ceiling denominator: 201/201 unchanged, confirmed by direct call. `git status` run
  at session end to confirm scope compliance (3 tracked files touched by me, matching the
  dispatch's allowed scope; 5 `tests/intent/` files confirmed as a different, concurrently-active
  lane's work, not mine).

## Memory & briefing surfaces referenced this session

- **Referenced**: `dev/2026/10/02/2026-10-02-1559-prog-code-log-1595-phase3-deposits-discovery-analysis-trust-memory.md`
  (row-shape convention, two-step empirical verification method — directly informed this unit's
  structure); `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (procedure + progress
  log, appended to).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections
  (bounded prog dispatch inside an existing worktree — no mailbox write, no sign-off merge, per
  dispatcher scope — git index not touched at all); the other three same-day Phase-3 deletion-lane
  logs (DISCOVERY/TRUST/MEMORY/ANALYSIS partials) — not read in full, since this unit is a
  DEPOSITS lane (pre-deletion), not a deletion lane, and the template deposits log already carried
  the shared methodology.
- **Wanted but not found**: none — the dispatch prompt's cited template log and the live code
  (pre_classifier.py, canonical_handlers.py, action_registry.py) plus the historical shadow-score
  reports were sufficient for every claim made in this unit.

## Discovered work

None filed as a separate GitHub issue (matching the established convention of prior deposit lanes
— reporting inline rather than filing, since these are measurement/evidence findings for the
Lead's own ruling, not independently actionable bugs on their own). One structural finding reported
inline above: `manage_repos`/`REPO_MANAGEMENT_PATTERNS` has no destructive-confirm guard at either
the pre-classifier level (`_is_destructive_ask`) or the handler level (`destructive_confirm`) for
its unlink/remove/disconnect sub-operations — a real #1756-shaped gap, flagged for the Lead's
disposition, not fixed in this unit.
