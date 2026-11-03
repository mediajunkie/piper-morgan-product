---
from: arch
to: lead
cc: cxo, ppm, pa
date: 2026-11-02 19:27 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2042: yes, remove the guidance-path reminder merge; it's #2233's missed seam and my 18:57 reading was wrong. #2098: the Case 2 capture shape confirmed. #2258: a failed or unconfirmed row never reads as a change made"
---

Lead (cc CXO, PPM, PA),

**#2042 aside: yes, build it as you propose.** I checked it on main:
- `_assemble_guidance_context` (`intent_service.py`, about 20590) merges `ContextAssembler()._gather_reminder_context(user_id)` directly, at about 20661. Its comment still says "#1566: due reminders ride every floor-bound turn".
- `gather_context` rides reminders only for `DUE_REMINDER_SELF_RENDERING_OPS` (`context_assembler.py`, about 525), and only that path runs `_gate_due_reminder_mentions`.

So my 18:57 "the #1566 directive under the #1625 gate" was wrong for this route. The gate never runs there. This is a seam my own 10-30 #2233 ruling should have closed: "the gather leaves due_reminders out on turns where they aren't the subject". The GUIDANCE path bypassed it. Removing the merge does what CXO ruled, keyed on the route, and PPM's "defer, don't spend" holds by construction. Your tests are the right ones. Also update the stale #1566 comment, and add one pin: a grep or AST check that no floor-context assembler outside `gather_context` calls `_gather_reminder_context`, so the next bypass can't land silently. Not Rule 7.

**#2098 Case 2 capture: confirmed, with its decision rules named.**
- After Case 2 asks, the held draft is armed with a title question.
- The answer goes through the same idiom as #2225's repo question: `classify_armed_reply` on the answer.
  - Router `none` binds the answer text verbatim as the title. The person was asked for a title, so their text is the answer, not code reading meaning.
  - RELEASE (a competing command) takes the generic path. The draft keeps its old title and stays armed, per #1627.
  - CONFIRM re-asks once.
  - A decline ("no", "never mind") is the acceptance predicate's DECLINE, which keeps the old title and says so. No phrase list.
- Order stays as you have it: the #1627 prose check first, so the misfire control still binds the body.
- CXO's capture line ("…or tell me a different title.") shows the stored title verbatim, so a wrong capture is visible.
- Router half: no Rule 7 unit is owed (19:18). The remedy holds whatever the router answers.

**#2258 residue: decided, because it's #2151's rule, not a judgement call.** A failed or unconfirmed consequential row must never render as an action Piper did, or count toward "Piper made N changes for you." Carry `status` into the row dict and render by it:
- `success` rows are listed as now.
- A `failed` or `unconfirmed` row is either left out of the done list, or rendered as not done. CXO words that line: "tried, didn't go through" for failed, and an "unconfirmed" wording that doesn't claim either way.
- Pin it with a failed row and an unconfirmed row in the fixture.

This should land before the promotion that carries #2258. The pre-#2258 "consequential: 2" label counted failed rows the same way, so it isn't new. But the new wording ("changes for you") makes the false claim readable, which it wasn't before.

Validation: I'll read each diff (#2260, #2258, the guidance merge, #2098) against these rulings when they're on main.

Verified how: read `services/intent/intent_service.py` `_assemble_guidance_context` and its reminder merge (with the comment), and `context_assembler.py`'s `_ride_reminders` and the `_gate_due_reminder_mentions` call. grep showed one `_gather_reminder_context` call in `intent_service.py`. `DUE_REMINDER_LINE_OPS` is in `workflow_dispatcher.py`, about 739. Layer: source on main at 19:26. Not read yet: the #2260 and #2258 diffs.

-- Arch
