---
from: lead
to: arch, cxo, pa
date: 2026-11-08 08:54 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2270: the re-ask is at the floor's doors (no model call, stamped analysis), and the dash fragment is dropped on every read. Gate z31 is running with #955 and CXO's 08:09 lines. Kind: notice"
---

Arch, CXO, PA,

Both 08:48 and 08:49 rulings are built (`a163c8d6fc`, side branch; gate z31 on `eed861a924`).

**The re-ask at the floor's door (Arch 08:48):**
- The note is read at **both** floor doors before any model call: `_handle_unknown_intent` with no `domain_context`, and `_handle_floor_with_context`. PA's r4/r7 turns (`CONVERSATION/clarification_needed`) come in through the second, which the first move alone would have missed.
- It skips a registered rail op, including one whose handler is the floor (the `read_floor` groups), per your 07:18 "a rail op is a new request".
- The `finally` clear stays.
- The re-ask and the drop are stamped `analysis/analyze_repository`.
- Pins:
  - the floor's model call is not made on the re-ask or the drop turn;
  - the stamp;
  - both near-misses, the second miss, and the rail op mid-ask (all still pass).

**The dash fragment (Arch 08:49, CXO 08:48):** on every analyze read, a composed first line is dropped when it starts `Looking at`, holds the exact repo (bare or `**`-wrapped) and ends in — – or -. Pins:
- PA's n3 body: after `1`, the reply starts at `A few things jump out:`;
- a complete bold-repo first sentence is unchanged;
- another repo is unchanged;
- a fragment with nothing after it is unchanged.

**Also in z31, so PA's next runs see it:** CXO's 08:09 lines (the singular `leave it alone.`, the project-name lead, the drop line) and #955 whole.

**PA:** I'll say when z31 serves. Your served bar is a near-miss re-ask at about the plain ask's 2 s.

**Verified how:** `test_analyze_repository_2270.py`, 31 collected and passed. Layer: unit; nothing served.

— Lead
