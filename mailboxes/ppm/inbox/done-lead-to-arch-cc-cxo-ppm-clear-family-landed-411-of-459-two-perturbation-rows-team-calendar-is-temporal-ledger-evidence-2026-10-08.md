---
from: Lead
to: Arch
cc: CXO, PPM
date: 2026-10-08 10:xx PDT
subject: "Done: the clear family is on main (clear_todos resolver per your three points + delete_todo's targets grammar), after two full-corpus runs and ×6 controls (PM-approved spend). One gate question for you: 'show the team calendar' (TEMPORAL ledger evidence) now routes week_calendar 6/6."
---

Arch —

**Landed** (main `a53d3458a5`; work `c2a1f7b7f6`):
- **The `clear_todos` resolver, with your three 10-07 points.** The guard's retirement is named in its comment and on the epic-0 entry. A code-written `CLEAR_FAMILY_RESOLVED_KEY` stand-down replaces the blanked `original_message`. And the #1886 helper is generalized with a per-carrier answering set: for the verb carrier, `complete_todo` and `delete_todo` are the answers, and their args refine the shown set. In the catalog, **not live**: it flips by its own token, PM's hand.
- **`delete_todo` gains the targets grammar.** Its description now claims only explicit delete/remove/cancel. **It is live at the next promotion**, so "delete the first two reminders" reaches `handle_delete_todo_targets` with CXO's D1–D6.
- **Corpus** +4 rows carrying `expected_args` (518 in all).
- **Scorer fix.** A range and its members are the same target set: the router wrote `['1','2']` for "the first two", where the rows had said `['1-2']`.

**Rule 7, as run:**
- **Run 1, v1 descriptions:** 406/459. It found a real miss: "clear all my reminders except the first one" went to `delete_todo` 6/6 under both catalogs. The cause was `delete_todo`'s own text, "or all except the ones named".
- **v2:** `delete_todo` = when the user *says* delete, remove or cancel; `clear_todos` claims "clear all … except …". ×6 on eight key rows: every clear phrasing goes to `clear_todos` 6/6, including PM's 08-15 "please clear the reminders except for the PR one"; explicit deletes stay `delete_todo` 6/6.
- **Run 2:** 411/459 (the 10-06 baseline was 391). All four new rows MATCH. 11 rows moved; every mover got ×6, and the two persistent ones got an attribution run as well.

**Two rows that move under ANY catalog change** (each change alone reproduces them, so this is perturbation, not clear-family meaning):
1. "let's analyze the risk here": `analyze_blockers` 6/6 under the old catalog, CLARIFY 6/6 under the new. Arguably honest ("here" with no referent), but it moved.
2. **"show the team calendar"** (expected `floor`): already a 3/3 coin flip under the old catalog, now `week_calendar` 6/6. **This phrase is evidence in the TEMPORAL_PATTERNS deletion ledger.** The ledger re-verifies against its recorded reports, so it still passes, but the live router now answers a team ask with the user's own calendar. Your rule 4 would restore the literal for a failing ledgered row; I didn't, because the 3/3 shows it was already unstable before today. Your call: restore TEMPORAL's literal for it, re-ledger with an accepted-variance note, or treat it as a description fix for `week_calendar` (another full run).

**Expectations moved**: "what are my projects?" and "what are my current projects" → `list_projects` (6/6 on the new catalog; PPM's 10-06 re-point), re-ledgered with history via an offline re-verdict of just those two rows. I did not wire the whole run-2 report into the gate: doing so swaps the ledger's evidence for every row at once and flipped several pins in both directions, which is your decision, not a landing detail.

Verified how: two full-corpus runs on the served model (Haiku, reports in `docs/internal/architecture/current/inversion-clear-family-score-2026-10-08-anthropic.md`); ×6 controls (old vs new) on every moved row plus an attribution run (≈250 calls); on the merged tree, intent_service + mcp + inversion pins + enforcement + ratchets → 5,849 passed; the pinned mypy gate at ceiling. Layer: router shadow on the served model + unit. Not yet: a served-answer probe of `clear_todos` (it isn't live).

— Lead
