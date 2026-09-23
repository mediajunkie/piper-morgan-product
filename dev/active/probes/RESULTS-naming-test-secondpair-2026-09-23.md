# BYOC tool-catalog naming test — second ambiguous pair, generalization check

**Author**: PA. **Run**: 2026-09-23, 11:2x PT. Continuing BYOC work per PM's instruction ("continue
working on byoc"), following `RESULTS-naming-test-followup-2026-09-23.md`'s "Still not settled"
section, which named this exact open question: does the situation-shaped disambiguation benefit
generalize to a different ambiguous pair, or is it specific to `list_projects`/`attention_query`?

## Method

Extended the control pass's 12-op catalog with a new pair verified against the real handler
(`services/intent_service/todo_handlers.py:536-544`, `handle_create_reminder` docstring, #903):
`create_reminder` is literally "a time-annotated todo" — the real distinction between it and
`create_todo` is presence/absence of a time cue, a **different kind of ambiguity** than
`list_projects`/`attention_query` (which was about orientation-vs-action-needed intent, not time).
Both new ops' descriptions were freshly authored in the same voice as the existing 12, not derived
from code docstrings, to avoid the same-author confound flagged in pass 1.

Three utterances: one clear-reminder (explicit time), one clear-todo (no time), one genuinely
ambiguous (a soft time cue — "sometime tomorrow" — inside a general-need phrasing rather than an
explicit reminder request).

## Result

**Object-shaped: 3/3. Situation-shaped: 3/3. No difference.**

Both naming schemes resolved all three utterances correctly, including the deliberately-ambiguous
one — under object naming, `create_reminder`'s own name/description apparently carries enough
signal ("time-anchored," "timing cue") that the model didn't need situation framing to disambiguate
from `create_todo`.

## What this changes about the earlier finding

This is a **null result for this pair**, and it sharpens rather than undermines the prior finding.
The prior claim (followup pass) was already narrow: *"situation-shaped framing provides a genuine,
replicated disambiguation benefit specifically for inherently ambiguous user phrasing."* This pass
shows that claim needs a further qualifier — **the benefit doesn't generalize to every kind of
ambiguity.** The `list_projects`/`attention_query` ambiguity was about **purpose** (orientation vs.
action-needed) — genuinely hard to signal in a short object-shaped name/description, because
"list_projects" doesn't hint at *when* someone would reach for it over `attention_query`. The
`create_reminder`/`create_todo` ambiguity is about **a concrete, nameable feature (time)** — and an
object-shaped name/description can just say "time-anchored" and close the gap without needing
situational framing at all.

**Working hypothesis, stated as a hypothesis, not a finding**: situation-shaped naming helps most
where the disambiguating signal is about *user purpose/context* that's hard to compress into an
object-shaped noun phrase, and helps less (or not at all) where the disambiguating signal is a
concrete feature an object-shaped description can just state directly. This pass alone can't
confirm that — it's one data point on a different axis, consistent with the hypothesis, not proof
of it.

## Honest scope, unchanged from prior passes

Still Claude only, still n=1/cell, still a hand-picked pair. This is now **three ambiguous
situations tested**: two phrasings of one purpose-ambiguous pair (situation won both) and one
time-ambiguous pair (no difference). Enough to say the effect isn't universal; not enough to
characterize exactly which ambiguity types it helps with — that would need several more pairs
across more categories, which is a real cost/value tradeoff to raise with PM before pursuing
further, not a self-evidently-worthwhile next step.

**Verified how**: 6 live API calls this fire (`claude-sonnet-5`), raw JSON saved
(`probe_naming_test_secondpair_results_2026-09-23.json`). `create_reminder`'s real behavior read
directly from `todo_handlers.py`, not assumed from its name.
