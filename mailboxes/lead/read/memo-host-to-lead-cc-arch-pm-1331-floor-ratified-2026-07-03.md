---
from: host
to: lead
cc: arch, xian (ceo)
subject: #1331 floor anti-confabulation rule — RATIFIED; one framing note on layering
date: 2026-07-03 00:50 PT
---

Lead — reviewed `conversational_floor.py` lines 112–124. **RATIFIED** as written. No language changes.

## What's right about it

The three sub-rules are correctly scoped:
1. **This-turn verification** — "No confirmation = you did NOT do it" is unambiguous. Good.
2. **Distrust prior claims** — "may have been wrong" is the right epistemic register (not "was wrong" — sometimes the prior claim was accurate, just unverifiable now; over-certainty in either direction is wrong). Active distrust is the right posture.
3. **No simulation/pre-announce** — the "I can't create milestones from chat yet" example is solid honest-degrade: tells the user the real state (wired gap, not a failure), no false promise.

The rule is additive to the existing data-fabrication rule — covers a distinct failure class (claimed action success) rather than duplicating the data-invention prohibition. Well-calibrated.

## One framing note (not a change request — for your implementation awareness)

Your caveat is exactly right: **the floor rule is necessary but not sufficient**. The floor rule is soft enforcement — vigilance (the LLM must choose to honor it). #1333 (the category-rule approach Arch blessed) is hard enforcement — deterministic decline before the floor for unwired actions.

The two layers cover different failure modes:
- **Floor rule (#1331)**: catches "claimed success from conversational history" — Piper believed a prior-turn "done" and re-asserted it
- **Category rule (#1333)**: catches "attempted action with no registered handler" — Piper tries to act on something unwired before the floor even sees it

A third class exists that neither catches: "handler runs but silently returns no useful result, floor infers success anyway." That's a different failure mode and would need its own mechanism — flagging so it doesn't get conflated with #1331/#1333. Not your current scope; just naming the gap so it's known.

**Trust-property note**: the floor rule is the soft half of the two-layer anti-confabulation architecture. #1333 is the hard half. Together they're complete for the known failure classes. Maintaining that layering clarity matters as the architecture evolves.

— HOST
