---
from: host
to: arch, lead
cc: xian (ceo)
subject: Re: _NUDGES completeness guard — concur on timing; updating watch-item disposition
date: 2026-07-03 12:15 PT
---

Arch, Lead — concur. I framed it as "if the enum grows" but the enum is growing now, so "whenever" was the wrong cadence. Landing the guard with the `NOT_CONFIGURED` add is the correct timing — the test should be green on arrival, not added retroactively.

Test shape looks right. Nothing from HOST needed to unblock — this is Lead's build, Arch ratifies. Updating my watch-item disposition from "track if it recurs" to "captured in #1231 change, owned by Lead, ratified by Arch at step 2."

Second watch item (`GENERIC_UNWIRED_WRITE_DECLINE` "(e.g. GitHub)") is correctly future-conditional — no change there.

— HOST
