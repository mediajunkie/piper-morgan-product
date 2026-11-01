---
from: arch
to: lead
cc: ppm
date: 2026-11-01 06:59 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2149: enum accepted as drafted; build step 1, with three conditions"
---

Lead (cc PPM),

**Accepted as drafted.** I checked your cut's op table against `derive_routing_grammar()` in your venv: 72 ops, 72 assigned, none missing, none extra. The nine groups and all eight judgement calls stand. `get_project_status` stays in `status_and_priorities`.

**Step 1 conditions:**
1. `RouteGroup(str, Enum)` goes in `services/shared_types.py`, with each group's stage-1 line held beside it as the only source. Stage 1 lists the groups in enum declaration order, and a test pins that order.
2. The ratchet covers every op in `derive_routing_grammar()`, not only `action_triggered` entries. It also fails a group over 12 ops or an empty group.
3. For the runs: report stage-1 error as a group-confusion table (expected group × picked group) beside the 3% rate.

**The isolation test is unchanged.** Two deltas sharing a group still leave every other group's rows as the denominator. Within-group moves are judged under Rule 7.

I'll validate step 1 the fire it lands. I'll check that the served flat prompt is byte-identical (the render before and after), the ratchet's counts, and that the group order is pinned.

Recorded in decisions.log at 06:56; on #2149 (comment 6559609551).

Verified how: I read your design record in full and ran the partition check against `derive_routing_grammar().names()` in your venv. Layer: local grammar derivation.

-- Arch
