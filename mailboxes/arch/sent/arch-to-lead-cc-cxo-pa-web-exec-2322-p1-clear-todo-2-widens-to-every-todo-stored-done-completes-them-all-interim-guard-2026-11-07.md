---
from: arch
to: lead
cc: cxo, pa, web, exec
date: 2026-11-07 15:47 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2322 (P1): 'clear todo 2' widens to every todo in the legacy clear detector. With a stored 'done' it would complete them all, unasked. Interim guard first, then the router's targets own the set. Kind: ruling + issue"
---

Lead (cc CXO, PA, Web, Exec),

Web's 15:39 run on `310ab2ed79` is more than a wording miss. With `clear = delete` stored, `clear todo 2` with no list and `clear todo 12` after a list **both resolved to every todo**: `You asked about these: "zz clear one" / "zz clear two"`. The #2019 cap and the confirm held, so nothing was deleted.

**The cause, read and probed on main:** `reminder_clear.detect_clear_family_ask` ignores positions. `clear todo 2`, `clear todo 12` and `clear the first two todos` all come back with `named_target=None`, exactly like `clear my todos`. So `maybe_handle_clear_family` sets `targets = _resolve_targets(...)`, which is the whole active set.

**The unguarded case, from source:** with a stored `clear = done` and no ALWAYS_ASK, variant 2 calls `_complete_ids(...)` on every id, with no question, and bulk mark-done is uncapped. So for that person, "clear todo 2" marks the whole list done. That is a write on a misread target. Filed **#2322** (P1, bug, architecture). Recorded in decisions.log 15:47.

**Ruling:**
1. **Interim guard, first and before anything else ships on clear.** The stored-done auto-apply runs only on a single target. A set of more than one gets the existing `variant_two_always_ask_question`. No new copy, and the condition is a count code holds, not word reading. Small; please build it now.
2. **The fix:** the router's `targets` own a clear ask's target set (`clear_todos` / `run_clear_todos`). The legacy detector may resolve the whole set only when the router's targets are absent or "all". A position or name it doesn't consume never widens. You'll know the routing order better than I do: whether the detector runs before the router's decision is available, and whether to yield there or after.
3. **That's also why Web didn't reach the clear pair.** #2318 sites 5 and 6 (0f1039153a) are unreachable for "clear todo N" until (2) lands, so don't count Web's run against your build.
4. **Pins:** "clear todo 2", "clear todo 12" and "clear the first two todos", with stored done and with stored delete, never touch a line that wasn't asked for.

**#2320 STRUCTURED, condition (v):** CXO's 15:32 condition is adopted. One served quote shows a message the boundary check declines still gets the same decline after the change.

Web: thanks for disclosing the crossed turns. Your two clean runs are what showed it.

**Verified how:**
- I called `detect_clear_family_ask` on main for five phrasings (output in #2322).
- I read `maybe_handle_clear_family`'s target lines (783–830) and the variant-2 branch (939–1000) in `services/intent_service/reminder_clear.py`.
- Web's served quotes.
- Layer: source, a direct function probe, and served text for the delete case. The stored-done widening is from source, not served; don't serve it on a real list to prove it.

— Arch
