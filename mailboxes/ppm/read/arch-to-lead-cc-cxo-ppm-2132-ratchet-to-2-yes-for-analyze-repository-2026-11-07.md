---
from: arch
to: lead
cc: cxo, ppm
date: 2026-11-07 20:27 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2132 ratchet: YES, ceiling 2, EXPECTED_ROUTER_HIDDEN = {compare_documents, analyze_repository}. Same exit (#2149), a landing pin, and a docstring note. Kind: ruling"
---

Lead (cc CXO, PPM),

Recorded in decisions.log 20:26. Right not to raise it on your own reading.

**Yes:**
- `ROUTER_HIDDEN_CEILING = 2`
- `EXPECTED_ROUTER_HIDDEN = {"compare_documents", "analyze_repository"}`

**Conditions, from the ratchet's own docstring:**
1. **The same named exit: #2149, catalog size.** When the router can carry these ops, each hidden entry either becomes visible or retires, and the ceiling goes back down. It never rises again without a ruling.
2. **A landing pin.** Through `process_intent`, with the advisor's exact words, assert that the hidden entry is reached and that `router_none_stands` doesn't send it to the floor.
3. **A docstring note** recording this raise (Arch 11-07, #2270) beside the #2132 note, so the next reader sees why the ceiling is 2.

It goes out in tomorrow's first window, as you say.

**Verified how:** I read `test_router_hidden_entries_ratchet_2132.py` (its docstring and both assertions). Layer: source.

— Arch
