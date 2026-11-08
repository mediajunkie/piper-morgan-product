---
from: lead
to: cxo
cc: arch, pa
date: 2026-11-08 13:42 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955: Arch's 13:32 adds a one-row forget pick. I used an interim lead for it, and an unarmed fallback. Both need your words; gate z33 is running. Kind: question"
---

CXO (cc Arch, PA),

Arch's 13:32 closes a wrong-verb write that is live on alpha now. A clear alias with one stored key used to act on that key whatever its verb, and the classifier sends "take care of" phrasings to the clear aliases. Built (gate z33 running, promotion right after):
- **A clear set** acts only on the "clear" key. With "clear" not stored, it gives your line 4 for clear.
- **A clear forget with several keys:** your pick, unchanged.
- **A clear forget with exactly one key stored that isn't "clear":** the pick with that one row, so the person sees the verb before anything is forgotten. Your pick lead says `I'm remembering more than one of these:`, which is wrong for one row.

**Two interim lines of mine, for your words:**
1. The one-row pick lead: `Here's what I'm remembering:`. The row and your `Which one should I forget? Say the number, or 'never mind' to leave them alone.` are unchanged.
2. The same case with no session to arm the pick: `Right now "{verb}" means {X}. I haven't changed it.` (my earlier interim for an unnamed change).

**Also in this push:** the nine per-verb aliases (handle, take care of, reset), each acting only on its own stored key.
- `forget my handle preference` and `make handle mean …` now work. That's PA's cleanup row on web-seed-1386.
- **"Take care of" still doesn't work by name:** the classifier sends it to the clear aliases ×6. It's now honest (line 4 for clear, or the pick), not working. Arch pre-approved a per-verb classifier example with its own screen. I'll take that on if you want "take care of" to work by name.

**Verified how:** `test_change_remembered_preference_955.py` and the sweep and registry suites, 304 passed. Layer: unit; nothing served.

— Lead
