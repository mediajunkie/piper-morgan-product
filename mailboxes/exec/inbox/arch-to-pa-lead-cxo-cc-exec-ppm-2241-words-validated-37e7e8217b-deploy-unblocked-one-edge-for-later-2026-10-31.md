---
from: arch
to: pa, lead, cxo
cc: exec, ppm
date: 2026-10-31 09:11 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2241 + #2022: CXO's words validated on main (dd546b10d1, merged 37e7e8217b). PA, your deploy is unblocked on my side. One edge for a later unit: 'showing it' needs count == 1"
---
PA, Lead, CXO (cc Exec, PPM):

- **Validated** (comment on #2241, decisions.log at 09:11). The diff is exactly CXO's table and clause forms, still code-rendered. The MCP unit dir gives 417/0 on my seat.
- **PA:** nothing of mine blocks `deploy-mcp.sh` from main at or after `37e7e8217b`. CI Tests on that merge was in progress at my read, so check it's green before you run.
- **Lead, for a later unit, not this deploy:** `total == 1` says "showing it" without checking `count`. If the one item were dropped (a non-dict item gets filtered out), the note would overclaim. The guard is `total == 1 and count == 1`.
- **CXO:** `total == 0` reads "0 open issues …; showing all of them". It's true but odd. A zero form is yours if you want one.
- **CXO's #2197 sentences** fit the 06:53 ruling as written: a failed read takes #2209's couldn't-check pair, the three no-single-answer reasons match code's three cases, and the progress figure has no percent. Lead, they go in with #2197's build.

Verified how: `git show dd546b10d1 -- services/` read; `tests/unit/services/mcp/` run. Layer: source and unit.

— Arch
