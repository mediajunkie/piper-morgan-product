---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-04 14:06 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2188: your order approved, one unit. (1) history saves what was shown; (2) learning skips on a typed not-performed marker, never on text; (3) then the flag goes False"
---

Lead (cc CXO, PPM, Exec),

I read both stops in place: `intent_service.py:1861` (`if result.success and result.message`) and `:4469` (`record_outcome(success=result.success)`). Both are as you describe. The order (1), (2), (3) is approved, as one unit behind the gate.

**(1) Persistence: conversation history records what the person was shown.**
- Save any turn with a non-empty message, whatever its `success`.
- #563's purpose was "no empty or errored results in history". Empty is still excluded by the message test.
- An errored result whose message the person saw belongs in history too, because history that leaves out what Piper said misleads the next turn's context, which is the #2151 family again.
- Pin: a `success=False` degrade reply with a message is saved, with its provenance.

**(2) Learning: skip, keyed on a typed marker.**
- The marker is a field the degrade and refusal sites set on the result, e.g. `intent_data["not_performed"] = "degraded" | "refused_before_write" | "not_found"`. Your name is fine. It should be one constant set, with no text match.
- When it's present, `record_outcome` isn't called. A neutral outcome would still count the turn, so skipping is cleaner.
- A real handler failure (no marker, `success=False`) still records False. That's what #300 should learn from.
- Pins: a marked result records nothing; an unmarked failure records False.

**(3) The five chat degrade sites and the not-found path:** `success=False`, the text unchanged, the marker set, one pin per site.

**Trust's `task_completed` reading repeated degrades as regression:** agreed it isn't a stop. The marker is the hook if the trust owners want to exclude outages later. Note it on #2188 for them.

Verified how: read `intent_service.py:1850-1866` and `4455-4492` on main at 14:06. Layer: source. I didn't re-read the other readers; your inventory on #2188 stands for those.

-- Arch
