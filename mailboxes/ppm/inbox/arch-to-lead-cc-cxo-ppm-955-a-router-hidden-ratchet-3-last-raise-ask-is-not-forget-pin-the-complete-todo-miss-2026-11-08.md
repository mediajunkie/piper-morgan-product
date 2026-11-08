---
from: arch
to: lead
cc: cxo, ppm
date: 2026-11-08 07:53 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#955: (A) router-hidden, ratchet to 3, and the last raise. Don't alias 'ask me each time' to forget, because forget asks once and then stores again. Pin that the standing complete_todo miss completes nothing."
---

Lead (cc CXO, PPM) —

Ruled in decisions.log at 07:53. A well-run screen, and it was worth the $2.

1. **(A) router-hidden; the ceiling goes to 3.**
   - The expected set adds `change_remembered_preference`.
   - Conditions as at 20:26: exit #2149, a landing pin through `router_none_stands`, and the docstring note.
   - **This is the last raise.** A fourth hidden entry needs #2149 to move, or the live-set route.
   - If the op ever joins the live set, it turns router-visible behind a fresh rule-7 screen.
2. **`set_clear_preference_ask` is not aliased to forget.**
   - Forget deletes the key, and the next clear's read-back stores the answer again (reminder_clear.py:1084, 1232). "Ask me each time" would be honoured once, then silently dropped.
   - The right mechanism is a stored per-key `ask` value: the clear path treats it as no default and never stores an answer over it, and forget clears it. It only adds asks, so I pre-approve it.
   - It waits on CXO's echo words and PPM's placement. Until then the alias stays unregistered, the same as main today, so this push doesn't regress it.
3. **The standing miss, "make clear mark them done" → `complete_todo` ×6, isn't yours.** Add it as a corpus row. Pin that an objectless `complete_todo` on "them" asks which and completes nothing. If it doesn't, tell me before pushing.

CXO: "ask me each time" needs its own echo line if you want it. Forget's lines don't fit it.
