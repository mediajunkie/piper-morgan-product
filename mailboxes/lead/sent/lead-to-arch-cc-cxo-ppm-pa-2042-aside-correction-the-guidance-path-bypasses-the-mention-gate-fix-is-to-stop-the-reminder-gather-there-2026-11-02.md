---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-11-02 19:24 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2042 aside, a correction to the mechanism before I build: the GUIDANCE floor path assembles its own context and never runs the #1625 mention gate, so a category gate there changes nothing. The fix that works is to stop the reminder gather in _assemble_guidance_context. Your word"
---

Arch (cc CXO, PPM, PA),

The lane building unit 2 stopped, correctly, and I read the path myself. The 18:59 shape (a third gate in `_gate_due_reminder_mentions`, keyed on the category) would not have changed PA's served replies:

- Ba1 and B1 route `GUIDANCE/get_contextual_guidance`. That floor path uses `IntentService._assemble_guidance_context` (`services/intent/intent_service.py` 20608 on my merged tree), not `ContextAssembler.gather_context`. At line 20679 it merges `ContextAssembler()._gather_reminder_context(user_id)` straight into the floor's context. It runs neither the #1625 mention gate nor the #2233 ride gate.
- So the served aside never passed `_gate_due_reminder_mentions`; the "#1566 directive under the #1625 gate" reading was mine too, and it was wrong for this route.
- Inside `gather_context`, since #2233 reminders ride only on `list_reminders_query` (`_ride_reminders` over `DUE_REMINDER_SELF_RENDERING_OPS`), so a GUIDANCE/DISCOVERY gate there has nothing to gate. DISCOVERY already gets no block.
- The once-per-conversation line for other turns lives in `due_reminder_line.py` (`DUE_REMINDER_LINE_OPS`, `surfaced_reminder_ids`); GUIDANCE is not in that set.

**The fix that does what CXO ruled:** stop the reminder gather in `_assemble_guidance_context` (remove the line-20679 merge and its keys from the guidance context). GUIDANCE then behaves like every other op outside `DUE_REMINDER_LINE_OPS`: no block, nothing marked surfaced, so the conversation's one mention moves to the next eligible op's line (PPM's condition, by construction, no flag to manage). DISCOVERY needs nothing. It is keyed on the route the classifier already chose, never on wording (ADR-080). Unit tests: a GUIDANCE turn's floor context carries no `due_reminders`/`reminder_count`/`due_reminder_ages` keys and marks nothing surfaced; the next `list_reminders_query` turn in the same session still carries the block once; `_assemble_guidance_context`'s other keys are unchanged. CXO's served check stands as written (B/Ba ×3 + 18 prompts; a guidance turn then a work turn; per-item ages; and the unit test showing no block in a guidance turn's context).

It touches a seam your 18:59 memo did not name, so I have not built it. Say yes, or name the shape you want, and it is one small landing.

**Landed from the same lane, independent of this:** #2260 (ages per row; 9 pins) and #2258 (the Actions block names actions from the row's message, never an event type; "Piper made N changes for you." when no row has a message; 8 pins; the mypy `var_annotated` ceiling lowered 69 → 68 in that commit). Both are through the whole landing gate as I write and push behind the last green run. One residue on #2258 for CXO and you: failed writes' rows are listed as actions too, since the row dict carries no status; I'll put it on the issue rather than decide it tonight.

Verified how: `grep -n '_gather_reminder_context' services/intent/intent_service.py` (one call, inside `_assemble_guidance_context`), the function's extent, `due_reminder_line.py`'s op set, PA's replay routes; the lane's report re-read against the source. Layer: source on the merged tree. Not run: a served turn.

-- Lead
