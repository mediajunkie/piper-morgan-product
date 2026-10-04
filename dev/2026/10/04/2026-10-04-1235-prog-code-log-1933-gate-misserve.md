# Session log — prog (Coding Agent) — #1933 gate mis-serve fix

Model: Sonnet. Dispatched by Lead.

## Task

#1933: the Phase 3 deletion gate's "mis-serve" credit (`row_disposition`,
`scripts/inversion_phase3_deletion_gate.py`) assumed "the pattern claims a
different op than ruled, so deleting it cannot make the fallback worse" —
false when the fallback (surface 2, once the pattern is gone) itself lands
on a WRITE/DESTRUCTIVE mis-route. Counter-example: PORTFOLIO_PATTERNS'
"update my project name to Atlas" / "edit my project description" — surface
2 lands `EXECUTION/update_document_query` (effect WRITE) 10/10 both legs.

## What changed

`scripts/inversion_phase3_deletion_gate.py`:
- New `_surface2_misserve_safe(phrase)` (after `_surface2_reaches_floor`,
  ~line 455): requires (1) a surface-2 probe exists for the phrase, (2) no
  sampled action resolves (via `get_action_workflows()`, alias-aware) to a
  registered rail entry whose `.needs_consent` is True (effect WRITE or
  DESTRUCTIVE — Arch's 2026-08-09 derivation, reused not re-derived). An
  unregistered/invented sampled action is NOT disqualifying.
- Both mis-serve branches in `row_disposition` (MATCH-verdict arm ~line 952,
  MISMATCH-verdict arm ~line 1084) now gate their credit on
  `_surface2_misserve_safe(phrase)`; a FAIL reports "but mis-serve, no
  surface-2 probe" or "but surface 2 lands a WRITE/DESTRUCTIVE op (...) —
  not credited" instead of granting the OK.
- `check_deleted_entry_non_regression`'s `misserved_at_deletion` escape
  (~line 1574) is no longer an unconditional `continue`: it re-verifies via
  the same helper and appends a named `problems` entry on FAIL (phrase,
  claimed/ruled ops, the surface-2 reason) rather than passing silently.

## How a sampled action's effect is resolved

`get_action_workflows()` (same dict `p0.same_operation` reads, alias-aware:
`update_document`/`edit_document`/`update_document_query` are one entry) →
`WorkflowEntry.needs_consent` property (`effect >= EffectClass.WRITE`,
`services/intent_service/workflow_dispatcher.py:538`, declared per Arch's
2026-08-09 ruling in `services/shared_types.py`). Verified directly:
`update_document_query` → `(EffectClass.WRITE, needs_consent=True)`.
Unregistered/invented actions (`manage_portfolio`, `get_top_priority`,
`get_project_status`, `provide_guidance`, `clarification_needed`,
`reminisce_release`, `get_information` — none are rail keys) resolve to
`None` → not disqualifying, per the task's explicit rule.

## Ledgered `misserved_at_deletion` rows — re-verified

19 phrases across 8 lists. Re-run against `_surface2_misserve_safe`
directly (`check_deleted_entry_non_regression(entry, cats=CURRENT_LIVE_CATEGORIES)`
per list):

| List | Phrase | Result |
|---|---|---|
| PRIORITY_PATTERNS | "show priorities for this sprint" | PASS (get_top_priority, unregistered) |
| PRIORITY_PATTERNS | "not sure what to do about this" | PASS (provide_guidance, unregistered) |
| STATUS_PATTERNS | "what are my projects?" | PASS (manage_portfolio, unregistered) |
| STATUS_PATTERNS | "show me my portfolio" | PASS (manage_portfolio, unregistered) |
| STATUS_PATTERNS | "list my active projects for this quarter" | PASS (manage_portfolio, unregistered) |
| STATUS_PATTERNS | "what are my current projects" | PASS (get_project_status, unregistered) |
| STATUS_PATTERNS | "what projects am I working on" | PASS (get_project_status, unregistered) |
| STATUS_PATTERNS | "what are my active projects" | PASS (get_project_status, unregistered) |
| STATUS_PATTERNS | "give me a project status report" | **FAIL — no surface-2 probe** |
| STATUS_PATTERNS | "tell me what I'm working on" | **FAIL — no surface-2 probe** |
| STATUS_PATTERNS | "show my active work" | **FAIL — no surface-2 probe** |
| GUIDANCE_PATTERNS | "just getting started here" | **FAIL — no surface-2 probe** |
| TRUST_PATTERNS | "why are you always cautious..." | PASS (clarification_needed, unregistered) |
| MEMORY_PATTERNS | "remember when we shipped..." | PASS (reminisce_release, unregistered) |
| ANALYSIS_PATTERNS | "is there a bottleneck analysis available" | PASS (get_information, unregistered) |
| PRODUCTIVITY_QUERY_PATTERNS | "what insights do you have..." | PASS (analyze_productivity, READ) |
| TEMPORAL_PATTERNS | "pull up my calendar" | **FAIL — no surface-2 probe** |
| TEMPORAL_PATTERNS | "schedule check for today" | **FAIL — no surface-2 probe** |
| TEMPORAL_PATTERNS | "show all events" | **FAIL — no surface-2 probe** |
| TEMPORAL_PATTERNS | "when's my next free slot" | **FAIL — no surface-2 probe** |
| TEMPORAL_PATTERNS | "what's my available time" | **FAIL — no surface-2 probe** |

**9 phrases across 3 lists (TEMPORAL_PATTERNS x5, STATUS_PATTERNS x3,
GUIDANCE_PATTERNS x1) now FAIL non-regression** — not because surface 2
lands a WRITE op, but because no surface-2 probe was ever run for them.
This is a real, reportable finding (less alarming than a WRITE mis-route,
but the new rule requires evidence, and none exists on disk) — reported to
Lead, ledger NOT edited to hide it.

**Collateral finding, same mechanism, not from the ledger escape**:
CALENDAR_QUERY_PATTERNS' "is there a conflict on my calendar" ALSO now
fails re-verification (same "no surface-2 probe" reason) — it goes through
`row_disposition`'s ordinary floor/plan mis-serve disjunct during
re-derivation (not the `misserved_at_deletion` key), so it surfaced as a
new finding rather than through the ledger escape path. Flagging for Lead;
did not alter the ledger or try to resolve it.

None of the re-verified phrases that DO have probes land on a
WRITE/DESTRUCTIVE op — the acute WRITE-mis-route failure mode is isolated
to today's PORTFOLIO deposit.

## PORTFOLIO_PATTERNS — before/after

`--list PORTFOLIO_PATTERNS --live create_reminder,create_todo,delete_todo,read_floor,read_referent,read_status,read_strategic,read_synthesis,read_temporal`:

- **Before**: `GO (partial) — 2 load-bearing literal(s) SURVIVE, deleting
  the other 14` (survivors: `list my projects`'s literal, the `archive...`
  literal). Both PORTFOLIO dead-claim rows ("update my project name to
  Atlas", "edit my project description") were **[OK]** via the
  unconditional mis-serve rule.
- **After**: `GO (partial) — 4 load-bearing literal(s) SURVIVE, deleting
  the other 12` (the `update...project` and `edit...project` literals are
  now ALSO load-bearing survivors). Both rows are **[FAIL]**, reason:
  "surface 2 lands a WRITE/DESTRUCTIVE op (update_document_query) in
  10/10 probe samples — the fallback would be WORSE, not cannot-be-worse —
  not credited."

This directly answers the issue's 4th AC: PORTFOLIO's "14 deletable" is
now 12 deletable.

**The other ~9 [FAIL]/[OK] rows in PORTFOLIO_PATTERNS, reason breakdown**
(under this run's 9-category live set):
- `list my projects`, 5x `Archive my project...` variants — **[FAIL]**,
  "MATCH on a NON-LIVE op (not-live — no WorkflowEntry) ... no surface-2
  probe for this phrase" — `manage_portfolio` is unregistered, not live;
  unaffected by #1933 (pre-existing FAIL reason, no mis-serve credit ever
  applied here).
- `list my archived projects`, `Please list my archived projects` —
  **[OK]**, "MATCH (expected action live via group)" — ordinary live-MATCH
  credit, not mis-serve.
- `list my archive projects` — **[OK]**, "MISMATCH but the router's own
  route live via group" — ordinary live-MISMATCH credit, not mis-serve.

So of PORTFOLIO's 11 claimed rows, 3 are [OK] via ordinary live-routing
credit (unaffected by this fix), 2 were [OK] only via the now-gated
mis-serve rule and are now [FAIL], and 6 were already [FAIL] for unrelated
reasons (non-live MATCH, no probe). manage_portfolio itself is not a rail
op (`get_action_workflows().get("manage_portfolio")` → `None`) — it isn't
live because it was never built as a dispatchable workflow entry, not
because of any flag state.

## `--all` before/after

Ran `--all` with the same 9-category `--live` set before and after; **the
per-list GO/NO-GO/NO-ROWS table is byte-identical** — `diff` of the two
captures produced zero output. PORTFOLIO_PATTERNS reads NO-GO in both (it
already had unrelated FAIL rows — `list my projects`, 5 archive-literal
rows — keeping it NO-GO regardless of the mis-serve gating). No other
list's top-level verdict flipped; there are currently no plain-GO lists in
this corpus under this flag set (every row is NO-GO or NO ROWS), so there
was no list that COULD flip from GO to NO-GO. The fix's effect is visible
only in `--list`'s richer per-row/partial-deletion view, not in `--all`'s
coarse table.

## Tests

- `tests/unit/test_inversion_phase3_deletion_1595.py`: updated the one
  pre-existing pin that assumed unconditional mis-serve credit
  (`test_router_declined_but_pattern_misserves_the_row_is_ok` → split into
  3: no-probe-not-credited / credited-when-safe / not-credited-when-WRITE).
  Added `TestMatchArmMisserveCreditRequiresSurface2Safety` (3 tests, the
  MATCH-arm's own branch), `TestPortfolioDeadClaimRowsAreNotMisserveCredited`
  (3 tests, against the REAL corpus + REAL probe files, no LLM calls),
  `TestMisservedAtDeletionEscapeIsReVerified` (3 tests, the ledger-escape
  re-verification). 12 new/changed tests, all pass.
  **2 EXPECTED, UNFIXED failures** (real findings, reported above, ledger
  not edited): `test_real_ledger_entries_pass_non_regression`,
  `test_calendar_entry_fails_non_regression_without_the_live_flag`.
- `tests/unit/test_inversion_phase3_surface2_floor_1595.py`: 35 passed (no
  changes needed).
- `tests/unit/test_inversion_phase1_shadow_score_1595.py`: included in the
  35-passed run above, unaffected.
- `tests/test_architecture_enforcement.py`: 66 passed, 1 xfailed, **1
  FAILED** — `TestChatPointersReachabilityRatchet::test_every_pointer_resolves_deterministically`
  ("give me my standup", "what time is it?" resolve to None via
  pre-classifier). **Pre-existing, unrelated**: my diff touches only
  `scripts/inversion_phase3_deletion_gate.py` and its test file, neither of
  which this test imports; it exercises `services/intent_service/chat_pointers.py`
  + `PreClassifier` static resolution for unrelated phrases.
- Full suite: `tests/unit` + `tests/test_architecture_enforcement.py`,
  `-m "not llm"`: **3 failed, 12300 passed, 228 skipped, 3 deselected, 1
  xfailed** (255.96s). The 3 failures are exactly the ones above — 2
  expected real findings from this fix, 1 pre-existing and unrelated.
- `ruff check` + `ruff format --check`: clean (one new-code reformat
  applied, re-verified green).

## Hard rules followed

No git add/commit/push/stash-pop/checkout-- /reset. No LLM calls (all
probes/scores read from disk). Corpus and ledger contents untouched — no
schema change needed. A temporary scratch copy of the pre-fix gate script
(`scripts/_gate_before_1933_scratch.py`) was used to reproduce the "before"
numbers for this report and deleted before finishing; it never touched git
state.

## Memory & briefing surfaces referenced this session

- **Referenced**: CLAUDE.md worktree/sign-off discipline (confirmed
  work-only scope, no commits); intent-routing-stack.md was NOT loaded —
  this task stayed entirely inside the gate/probe instrumentation layer,
  not the live routing stack itself.
- **Loaded but not referenced**: most of CLAUDE.md's mailbox/duty-cycle
  sections — not applicable to a scoped coding-agent dispatch.
- **Wanted but not found**: none.
