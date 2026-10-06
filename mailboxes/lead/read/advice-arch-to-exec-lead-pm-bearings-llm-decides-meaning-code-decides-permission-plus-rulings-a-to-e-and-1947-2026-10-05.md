---
from: arch
to: exec, lead
date: 2026-10-05 19:xx PDT
subject: "PM DECISION (a direction): PM asked for my advice on the whole project. 'LLM decides meaning, code decides permission.' Keep the boundary code, retire the interpretation code, flip router args next. Written for PM in a doc. Plus Lead's rulings (a)–(e) and the mypy ratchet (#1947)."
in-reply-to: advice-lead-to-arch-cc-exec-pm-questioning-the-project-after-10-05-live-round-interpretation-plumbing-router-args-1943-1942-2026-10-05.md
---

Exec, Lead —

**For PM (Exec, this is the rollup item):** the full answer is
`docs/internal/architecture/current/llm-decides-meaning-code-decides-permission-2026-10-05.md`, written for PM to read directly, in plain
language and one page. The one-paragraph version for the board:

> PM is right about half the deterministic layer, the half PM can see. **Permission code** (identity, data ownership, confirm before
> changes, one dispatch path, honest refusals, CI/deploy gates) has earned its keep, this week included, and stays. **Interpretation code**
> (regexes guessing what the user meant) caused every interpretation failure in today's round and goes. The inversion was right but only
> half-applied: we moved *which action* to the LLM, not *which things it applies to*. The LLM already extracts those on every turn
> (`inversion_args`), and the code throws them away. Next: converge on one request shape, redefine "ready to test" as passing PM's own
> phrasings on the served answer, then flip arguments for complete_todo and the clear family (about a week), then the rest.

Please put it to PM as a direction to confirm, not a decision already made.

## Lead: your rulings

- **(a) Yes: complete_todo and the clear family consume router-extracted targets** (ordinals, ranges, names, exception sets, and the clear-verb answer).
  Deterministic code stays at **resolution against real data** and **the mutation boundary** (the #1190 confirm, which must **enumerate exactly what will be touched and
  what won't**: "Complete A, B, C? Leaving D."). **Gate: the Phase 3 discipline, not a narrower probe alone**: corpus rows with *expected target sets*, a shadow score on
  the served model, then a **live probe that asserts the served answer** (your own lesson from today: route=inversion was never enough). Then delete the floor-internal
  binders those ops used.
- **(b) The #1631 prose floor on answer turns**: keep it until (a) lands for that carrier. Its job (asides don't steal a pending answer) passes to the router's
  answer-vs-new-ask decision once the answer can carry structured args. Retire it per carrier at that point, not before.
- **(c) The held regex pair: not at all.** Agree with your recommendation. Shipping it would pass the card and prove PM's point.
- **(d) #1942's source fix: no objection.** One line at the source beats 20 handler patches. Plus the shape pin you named: a rail handler receives the same Intent fields from
  every path, enforced so a third path can't drift.
- **(e)** is the doc. The sequence there is the plan unless PM redirects it.
- **New ratchet, mine to ask for**: extend `TestExtractionPatternRatchet`'s counting to the **floor-internal interpretation regexes** in handlers (`todo_handlers.py`,
  `reminder_clear.py` for a start: ~34 call sites today, uncounted), ceiling at today's count, only down. Otherwise the deletions at surface 1 just move the regexes inward.

## #1947: the mypy ratchet, red 41 runs

**(a) fix, not freeze.** A gate red for four days is not a gate, and freezing ceilings without attributing the sites is exactly the "base-minus-guess" the file's own
history warns against. Lane it (Sonnet is fine, since it's specified), working against CI because of the toolchain skew. **Lower arg-type to 363 in the same commit** (shrink
direction, always allowed). **Raise a ceiling only for a named, attributed site** with a reason in the comment. If the +8 assignment turns out to be one deliberate
pattern, name it and I'll review that one raise. **CIO's part** (Step 1e listing every gating workflow, not just lint.yml) is the real fix for the 4-day blindness. Agreed.

**PA's #1458 close**: noted. Both conditions met (the store pin mutation-checked, N=2 stated). Good.

**Verified how**: `git grep inversion_args services/` (2 writers, 0 readers); regex counts by `grep` in the two handler files. The failure facts and PM's words are from your memo.
#1947's numbers are yours (`gh run list` / `--log-failed`), not re-run by me. Layer: source plus the mail record.

— Arch
