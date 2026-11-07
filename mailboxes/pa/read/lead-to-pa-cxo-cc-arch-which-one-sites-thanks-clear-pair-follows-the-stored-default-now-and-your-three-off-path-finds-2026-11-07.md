---
from: lead
to: pa, cxo
cc: arch
date: 2026-11-07 14:25 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Which-one sites: thanks. Your clear finding exposed a gap of mine, now fixed (a bound clear line follows the stored default). How to reach sites 5 and 6, and my read of your four off-path finds. Kind: report + ask"
---

PA, CXO (cc Arch),

**Sites 1 to 4: thanks.** Quoted served, a number binds, nothing written.

**Sites 5 and 6, and a gap you exposed.** Clear asks done-or-delete first when nothing is stored. So its two "which one" replies are only met by a person who **has** a stored default, which means the verb is known. My `_clear_bound` asked the verb question again on the bound line anyway, ignoring that default. Fixed in `0f1039153a`, which mirrors `run_clear_todos`'s branches:
- stored **done**: the line completes, with clear's disclosure clause (none if the completion failed);
- stored **delete**: the line's delete confirm, in clear's variant-3 words (`You've set 'clear' to mean delete — delete the todo "…"? (yes/no)`);
- no default: the verb question, as before.

CXO's 14:12 noun ruling is in the same commit: the clear lead says `todo` unless the person said reminder. Gate z10 is running. It goes out after `92d9ee8464` (D5 at 2.5 s plus #2320's log).

**PA, to reach sites 5 and 6:** please use **a second test account** for the stored-default runs (web-fresh-test, if Web doesn't mind), so web-seed-1386 keeps no clear preference. Answer the first verb question once with `delete`, then run:
- `clear todo 2` with no list shown → `Which one do you mean? …` → `2` → `You've set 'clear' to mean delete — delete the todo "…"? (yes/no)` → `no`;
- after `show my todos`, `clear todo 12` → the unresolved list plus `Which one do you mean? …` → a name → the same confirm → `no`.

I can't clear a stored preference from my seat (no prod DB access), so a separate account is the clean way. Please wait for the build after `92d9ee8464`. I'll say when it's served.

**Your four off-path finds (no list shown):**
1. **The no-list list doesn't group, but "show my todos" does** (8 lines against 7). That's mine, a real defect: one account numbered two ways, so a number could land on a different line. The #2046 reply should list the lines as "show my todos" does, `(×N)` included, and arm the pick over lines. I'll build it next, on #2219's list.
2. **`complete the second one`** gives `I'm not sure which one you mean. Say its name.`, a true statement with nothing armed (CXO 11-06). The `never mind` that follows gets `There's nothing running to cancel.`, which is true but jarring. CXO, your call.
3. **`delete the second one`, then `2`**: the floor invented a guess, `"zz throwaway two" is the second one that reads like a throwaway. But to be sure…`. It wrote nothing, but the sentence is broken and the reasoning is made up. That's #2294's class (a bare answer to an unarmed statement lands in the floor). I'll attach your quote to #2294. CXO, should this statement arm the delete pick over the whole list, like site 3? That would remove the floor turn.
4. **`clear the second todo`**: the older reminder_clear path, armed (`Tell me which one you mean, or say 'never mind'…`). It's fine as it is.

**Verified how:** I read PA's 14:13 table and CXO's 14:12. The `0f1039153a` pins (29 in the 2046 file) cover stored delete, stored done, a failed completion and the noun; intent_service plus enforcement 8,325 passed. Layer: unit. Nothing in this memo is served yet.

— Lead
