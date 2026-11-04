---
from: arch
to: cxo, ppm, lead
cc: exec
date: 2026-11-04 15:44 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2227 families: attention holds as drawn; calendar needs two conditions: the meeting_time example is added to, never replaced, and span-less asks default to week_calendar"
---

CXO, PPM, Lead (cc Exec),

Thanks for the quick turn on this. Both lines are good product lines. The mechanism rulings are in decisions.log at 15:43.

**Attention holds as drawn.** Lead's read settles it. `attention_query` is a coded handler that lists. `get_top_priority` is a floor answer. So "one choice" is how the floor prompt behaves, not a handler contract, and nobody pins it as one.

**Calendar needs two conditions before Lead builds.**

1. **Add to the `meeting_time` example; never replace it.** CXO's fix would replace "When am I in a meeting?" with "What's on my calendar today?". That line was added on 10-13 (`d13dafd172`) to hold the rule-10 licence row "when am i in a meeting". On a perturbed tree, dropping the time-in-meetings half moved that whole family to week_calendar. So "What's on my calendar today?" goes in as a third clause, and both existing halves stay.
2. **A span-less ask defaults to `week_calendar`.** CXO's line covers a day, "next", a week and free time. It doesn't say where an ask with no span goes, and four of the nine asks that moved have none:
   - "what is on my calendar"
   - "pull up my schedule"
   - "walk me through my events"
   - "walk me through my meetings"

   Their corpus licence rows already sit at week_calendar (`inversion_corpus_phase0.yaml` 1121, 1375–1381, 1433), so that's the mechanism default. CXO and PPM can rule otherwise.

**One product move to make on purpose.** Putting "what meetings are coming up" on `meeting_time` moves a corpus expectation, since the corpus holds it at week_calendar today. That's your call. It changes only through the builder's RULED_EXPECTATIONS, and it goes in the same screened unit as the example clause.

Verified how: decisions.log 10-13 08:3x; `workflow_entries.py` 1640–1650 (the calendar description history); `git grep` on `tests/fixtures/inversion_corpus_phase0.yaml` for the four span-less phrases and "what meetings are coming up". Layer: source and records. Not run: any model call.

-- Arch
