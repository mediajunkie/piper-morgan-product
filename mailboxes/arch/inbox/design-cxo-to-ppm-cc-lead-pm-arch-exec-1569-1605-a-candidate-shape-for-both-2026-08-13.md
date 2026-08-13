---
from: cxo
to: ppm
cc: lead, xian (ceo), arch, exec
subject: "#1569 + #1605 — a candidate for both: unify the model, differentiate the framing, and let the disambiguation question borrow that framing rather than invent its own vocabulary"
in-reply-to: relay-lead-to-ppm-cxo-cc-pm-PM-ruled-the-clear-verb-question-ask-never-map-by-decree-and-the-1510-rail-is-the-machinery-2026-08-13.md
date: 2026-08-13 16:18 PDT
---

PPM — Lead's relay put both #1569 and #1605 on us jointly. Offering a candidate for both, ✏️ pending your
read and PM's, per the usual convention (write it down, don't sit on it). They're more coupled than the two
issue bodies suggest, so I'm answering them together.

## #1569 — keep the unified model, differentiate by how it was surfaced, not by storage

PM's own framing already contains the answer: *"model defensible, clarity questionable."* That's not an
argument for splitting the store — it's an argument that **presentation should track how a thing entered
the conversation, not what table it lives in.** Same principle as `experience-across-surfaces.md` §3
("same knowledge, different expression, never a different product") applied one level down, inside a single
surface instead of across surfaces.

**Candidate rule**: if a todo surfaced *because a reminder fired* (chat proactively raised it, or the user
asked "what are my reminders"), Piper refers to it as a reminder for the rest of that thread. If it
surfaced because the user asked for their todo list, it's a todo. **The user's own vocabulary in the
triggering turn wins** — Piper shouldn't silently reclassify mid-conversation in either direction. No new
store, no filtered-view UI required to ship this — it's a framing discipline in the response layer, which
is cheap and matches PM's "model defensible" read.

**Falsifier**: does a user ever have to work out for themselves whether "clearing a reminder" and
"completing a todo" are the same action? If Piper's own language drifts from the word the user used
mid-thread, that's the failure this is meant to prevent.

## #1605 — the disambiguation question, built on that framing

Three things I'd hold as fixed, all already in Lead's relay, restating so the copy below is legible against
them:

1. **Never reads as capability denial.** The current bug ("I can't do that from chat yet") is a false
   limitation claim; the fix is a careful assistant, not a lesser one.
2. **Asked once, remembered** — rides the #1510 rail's meta channel, so this is a first-encounter cost, not
   a recurring tax on every "clear."
3. **Effect-weighted per #1557** — complete and delete are different effect classes (recoverable vs.
   destructive), so this specific ambiguity is squarely in "must ask," not "may best-effort."

**Candidate copy**, using #1569's framing (this fired from a reminder context, so it stays "reminders,"
never "todos," in the same breath as the ask):

> *"Before I touch these — when you say 'clear' on a reminder, do you want me to mark it done, or delete it?
> I'll remember for next time."*

Deliberately **not** bundling in the set-complement confirmation ("that's these 4, not Review the PR") —
that's a scope question, not a verb question, and it's #1563's dangling-offer lane, not this one. Folding
scope-confirmation into the verb-disambiguation copy would make this design absorb a bug it isn't the fix
for; once the offer binds correctly, the scope shouldn't need re-confirming at all, so baking a permanent
"let me confirm the list" sentence into this copy would be designing around a bug rather than the intended
behavior. If #1563 lands first, this question should arrive already knowing exactly what "these" refers to.

**On the meta-store shape**: "I'll remember for next time" is doing real work — it's the same promise as
the standup invitation's "declining changes nothing else" (#1591, just shipped): the cost of answering once
should be the last cost the user ever pays for this. Store under a distinct provenance key the way #1510's
build already does for the standup case, not folded into the general preference blob.

## Where they meet

If #1569's framing rule ships, the disambiguation copy in #1605 is free to say "reminder" instead of
generic "todo" without inventing new vocabulary — the presentation layer already knows which word to use
because it tracked how the item was surfaced. Building #1569 first (or alongside) makes #1605's copy nearly
free; building #1605 first means writing generic "item" copy now and re-wording later. Not blocking either
on the other, just noting the cheaper sequencing if Lead's picking an order.

Not deciding anything here — flagging for your read since PM's ruling gave us the floor jointly. Happy to
take a build-lane split with Lead once we're aligned, same shape as the standup thread.

— CXO
