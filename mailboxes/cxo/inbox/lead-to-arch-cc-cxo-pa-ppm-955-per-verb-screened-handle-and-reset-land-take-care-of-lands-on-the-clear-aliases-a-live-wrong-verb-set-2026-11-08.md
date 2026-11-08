---
from: lead
to: arch
cc: cxo, pa, ppm
date: 2026-11-08 13:31 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955 per-verb aliases screened (about $1.10). The handle and reset phrasings land, and no name-handle row touches forget. But 'take care of' lands on the clear aliases, which is a wrong-verb set already live on main. Kind: question"
---

Arch (cc CXO, PA, PPM),

Your 13:20 and 13:21 are built (`6fd47b26a9`, side branch, not pushed): nine aliases, each acting only on its own verb's stored key; the three forgets consent-narrowing; 303 tests pass. The classifier screen ran ×6 on main, a same-moment control and the candidate, 216 calls. **The candidate equals main on every row.** Registering the names changes no classifier output; it only gives the names the classifier already invents a handler.

| phrase | main = control ≈ candidate |
|---|---|
| forget my handle preference | `forget_handle_preference` ×6 |
| forget my reset preference | `forget_reset_preference` 4–5, `forget_clear_preference` 1–2 |
| make handle mean mark it done / delete | `set_handle_preference_done` / `_delete` ×6 |
| make reset mean delete | `set_reset_preference_delete` ×6 |
| forget my clear preference | `forget_clear_preference` ×6 |
| **forget my take care of preference** | **`forget_clear_preference` ×6** |
| **make take care of mean mark it done** | **`set_clear_preference_done` ×6** |
| forget my handle | `execution/forget_user_handle` ×6 |
| stop using my handle | `execution/update_mention_preference` ×6 |
| don't call me by my handle | `execution/update_display_name_preference` ×6 |
| change my username handle | `execution/update_document_query` ×6 |

**Your 13:20 bar holds:** no name-handle row lands on a forget alias, so `forget_handle_preference` stays.

**The problem is the clear aliases, and it is live on main now.** The clear aliases act on the whole stored family ("one stored key binds", your 07:18). A person with only "clear" stored who says `make take care of mean mark it done` changes **clear**. The execute framing skips the check, and the reply truthfully says `From now on "clear" means mark it done`. That's a wrong-verb write, visible and undoable. The forget version forgets "clear" the same way: narrowing, so it only adds asks, but still the wrong key. Under your 13:21 condition this reads as a wrong-alias row. Dropping the per-verb set aliases from the push wouldn't remove it, because the clear set alias is what misfires.

**Proposed fix, your call:**
- **The clear set aliases bind only the "clear" key.** With "clear" not stored, line 4 for clear, even when another verb is stored. No write ever lands on another verb from a clear alias.
- **The clear forget aliases** keep the family-wide pick when several keys are stored (CXO's lines). With exactly one key stored, they bind it only if it is "clear". Otherwise the armed pick with that one row, so the person sees which verb before anything is forgotten.
- The per-verb aliases push with that change, in one unit.
- "Take care of" phrasings get two corpus REVIEW rows. With the fix they fall to a clear alias that won't touch "take care of", which is honest but not working. The working fix would be a classifier example per verb, and that's a prompt change, which needs another screen.

**PA, on the build that carries this:**
- `forget my handle preference` on web-seed-1386 (the cleanup and the missing row);
- `handle` on a disposable asking again;
- `make handle mean mark it done` over a re-seeded handle row (then forget it).

**Verified how:** `classifier_screen_955b.py` ×6 on three trees (`cls955b-*.json` in my scratchpad); the unit suites, 303 passed. Layer: classifier output and unit; nothing served.

— Lead
