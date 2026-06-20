---
to: comms
from: pa
cc: xian (ceo)
date: 2026-06-20
subject: BYOC narrative angle direction — "we built onboarding in the wrong mode"
---

Comms —

PM direction on the BYOC narrative angle. You're cleared to draft.

---

## The angle

**Insight piece. Working title: "We built onboarding in our own image"** (or variation — yours to refine).

The core: the BYOC cold-start interview used the same serial one-turn-at-a-time interaction model that works well for ongoing PM assistance. That turned out to be wrong for onboarding — it stretched the experience out, made it hard to follow, and left the user with no sense of where they were or how much was left.

The insight: **onboarding and use have different interaction contracts.** The mode that earns trust in ongoing work is the wrong mode for earning trust at first encounter. Building onboarding in your own image — importing the assumptions that work in steady state — is a natural mistake with a non-obvious fix.

PM is comfortable ending with an open question rather than a tidy resolution. We know the serial model was wrong; we don't yet have a single canonical right answer. That honesty is part of the piece.

---

## Factual substrate

- The BYOC cold-start interview was a Claude plugin (`--plugin-dir` install) that ran a calibration interview to build a PM profile before the user's first real session
- PM's personal working preference is serial, one-turn-at-a-time conversation — deliberate, maintains context, doesn't overwhelm. This preference was imported directly into the onboarding skill design
- The result in testing: stretched out, hard to follow, user can't calibrate how long it will take or see where they're going
- The lesson: onboarding is not a lighter version of use — it's a different activity with different needs (orientation, calibration, building confidence) that may call for a different interaction model (batched questions, wizard-style progressive disclosure, something else TBD)
- This is a real finding, not a tidy post-hoc lesson. The right onboarding model is still an open question

**What NOT to claim**: don't frame the intake as having successfully demonstrated the working relationship — PM's point is that it didn't land as intended. The interesting story is the gap between the design assumption and the actual experience.

---

## Tone and framing

- Honest about imperfection — PM explicitly wants "the real friction"
- Transferable to any PM building an AI product: what do you import from your product's ongoing interaction model when you design the first encounter?
- Can end open — "we know what didn't work; the right model is still being worked out"
- Not a success story. Not a cautionary tale either. A genuine observation about product design, told from inside the work

---

## Category and timing

- Category: **insight** (standalone, not tied to the building-narrative beat sequence)
- No urgency on timing — publish when it's ready; the story doesn't go stale
- PM voice-pass needed as usual before handoff to Docs

---

One source worth reading before drafting (in addition to the PA memo you already have):
`dev/2026/05/30/pa-skunkworks-byoc-poc-learnings-2026-05-30.md` — the PoC learnings doc has the original framing of the cold-start interview's purpose, which gives you the "what we intended" half of the contrast.

— PA
