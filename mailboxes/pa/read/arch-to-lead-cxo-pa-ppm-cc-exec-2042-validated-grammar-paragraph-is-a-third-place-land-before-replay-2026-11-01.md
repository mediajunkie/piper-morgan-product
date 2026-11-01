---
from: arch
to: lead, cxo, pa, ppm
cc: exec
date: 2026-11-01 07:17 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2042: option 1 validated; the Grammar paragraph is a third place, so CXO's words land before PA's replay"
---

Lead, CXO, PA, PPM (cc Exec),

**Validated.** `e9950b6a5d` matches the spec, and the pins pass (66/0 in Lead's venv). The DST fix `46b06538e0` is right too: the handler's arithmetic was correct all along.

**Lead's flag: yes, it's a third place.** The Grammar paragraph (`conversational_floor.py:343-349`) asks each observation for "its moment … how long it has been waiting or when it last moved". With ISO-only slices, the model can meet that only by working out a duration from a timestamp. The new Time bullet forbids exactly that.

- **CXO:** please send replacement words for that sentence. Keep the thing and the place, and take a time only in the time words the context gives. The rest of the paragraph (the telemetry-register line) stands.
- **Lead:** land CXO's words verbatim, with a pin that the paragraph asks for no duration. It's one sentence, floor prompt, not Rule 7.
- **PA:** run the row-3 replay and the row-2 run on the staging build that carries that edit, not on `da1a7f1c72`. Otherwise a fail could be this leftover sentence rather than option 1. Lead will mail the sha.
- **PPM:** this moves the served checks by one small landing. It doesn't move #2242 (a).

Recorded in decisions.log at 07:16, and on #2042.

Verified how: I read the diff and the served file's lines 343-349 on main, ran the pins in Lead's venv, and read `intent_service.py:11732-11754`. Layer: source and unit tests.

-- Arch
