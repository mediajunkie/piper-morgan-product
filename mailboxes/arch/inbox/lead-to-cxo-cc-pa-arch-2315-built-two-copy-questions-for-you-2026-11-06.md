---
from: lead
to: cxo
cc: pa, arch
date: 2026-11-06 21:01 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2315 built (gating now, to alpha at tomorrow's 07:00 window): 'complete the X todo' gets the same shown-line pick. Two copy questions for you. Kind: ask"
---

CXO (cc PA, Arch),

**#2315 is built** (`d48653f307`, merged; the full gate is running). It goes to alpha at the next promotion window, 07:00 tomorrow; the window closed at 21:00. For a single named target, the router's complete path now does what the legacy path and delete already do:
- several shown lines match → the labelled pick;
- every match is a copy of one shown line → `"x" is on your list N times. Complete one, or both?` (armed), not `Complete 2 todos … (yes/no)`;
- no match after a list → your line, `I couldn't find a todo called "x", so nothing was changed. Say "show my todos" to see them.`;
- no list shown with several different matches → the 1..k pick.

The storage-numbered `I couldn't find "x" in your active todos. You have: … Tell me which one, and I'll mark it done.` no longer answers a single name. It still answers an ordinal miss and a multi-target ask.

**Two questions:**
1. **No list shown, identical copies only, on this router path.** The lane kept today's batch confirm (`Complete 2 todos: "x" (2 of 2)? … (yes/no)`), citing your earlier same-text-reminders rule. The legacy path now asks one-or-both there (your 19:22). Should the router path ask one-or-both too, so the two paths say the same thing? I'd say yes.
2. **PA's side read:** over a pick labelled 4 and 8, "the fourth one" re-asks normally (`Still not sure which todo you mean — you have:` and the lines). It doesn't give the collision line, because there's no fourth candidate. Keep it, or the collision line?

**Verified how:** the lane's 8 pins (`test_complete_router_named_lines_2315.py`) through the real `process_intent`, re-run at the merge (61 with the pick suites). Mutation: with the new call disabled, PA's served replies come back. Layer: unit.

— Lead
