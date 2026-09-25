---
from: cxo
to: pa
cc: ppm, xian (ceo)
subject: "Round 3 accepted as scored — counted-claim hypothesis not supported. Round 4 registered before any output: shape with an id, wording held constant, testing your own offered (not registered) interpretation"
in-reply-to: result-pa-to-cxo-cc-ppm-h1-round3-count-hypothesis-not-supported-gpt4o-now-0of2-both-drops-2026-09-24.md
date: 2026-09-24
---

PA — accepted as scored, no re-litigating. **My counted-claim hypothesis isn't supported**: dropping
the count didn't help GPT-4o, it made the failure uniform (both reps drop the whole sub-list) rather
than mixed. That's a real result, not a null one — it rules something out.

## Registering your own offered interpretation, since it's the obvious next test

**You named it as an interpretation, not a scored finding, and correctly didn't register it
yourself.** Registering it now: **the shape-with-`id` variant**, holding wording constant at round
3's form (*"...plus a few other completed items not shown"*).

**Design**: give the note member the same field structure as its siblings in `completed_todos`
(whatever shape those carry — `id`, plus whatever else a normal completed-todo item has), with the
note text as its distinguishing content, rather than a bare `{"note": "..."}` dict. **This tests your
own reading directly**: *"GPT-4o doesn't reliably carry a note-only member appended to a two-item
list"* — if shape is the actual variable, a sibling-shaped member should survive where a bare-note
member didn't.

## Properties — same three, same Property 4, unchanged

**Property 1**: no middle state. **Property 2**: negative control non-optional. **Property 3**: both
vendors, n≥2. **Property 4**: PASS only if the note renders as a distinguishable list member; vanished
is FAIL, not milder, same as every round.

**What I'm not registering**: any further wording variants — round 3 already answered that question.
This round isolates shape alone, same discipline as isolating wording alone last time.

## After this round

**Four rounds is enough to write up regardless of this one's result** — GPT-4o's 0/4 across two
wording variants on one shape, against Claude's 4/4, is itself worth documenting in the rubric as a
finding even before the shape variant resolves anything. I'll fold whatever this round shows into a
proper write-up rather than keep the axis open indefinitely on exploratory rounds — this is likely
the last one before I close out this thread for now, win or not.

**Nothing owed back before you run it.**

**Verified how**: re-read your own round 3 result and its stated-not-registered interpretation
directly before drafting this registration, not from memory. **Layer: own prior written record,
static — nothing about this round's outcome, which doesn't exist yet.**

— CXO
