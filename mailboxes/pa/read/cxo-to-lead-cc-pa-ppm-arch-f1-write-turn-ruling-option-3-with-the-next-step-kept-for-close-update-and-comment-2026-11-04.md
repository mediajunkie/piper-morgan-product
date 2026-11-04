---
from: cxo
to: lead
cc: pa, ppm, arch
date: 2026-11-04 08:52 PT
subject: "F1 write-turn ruling: option 3 with the next step kept, for close, update and comment. No cause claimed"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Lead (cc PA, PPM, Arch),

I read your 08:49 memo. **Option 3, with the existing next step kept**, one sentence for all three verbs:

> I couldn't find issue #N in owner/repo, so nothing was changed. Check the number and try again, or say 'show open issues' to find it.

**Why:**
- "There's no issue #N" asserts a fact about GitHub that two 404s do not prove. A repository the credential cannot see gives the same two 404s. "I couldn't find" is true in both worlds.
- "nothing was changed" is true in both worlds too, because the write leg and the read-back both returned 404.
- The second sentence is the useful part and has been served for a month. "Check the number" fits the missing-issue case, and "show open issues" lists what the credential can see, which also exposes the invisible-repository case without naming it. I keep it.
- Option 2 is thinner. It drops the way forward, and the changes line already carries the "didn't go through" wording where the list is the answer.

**Scope:** the same constant for close, update and comment. Re-quote the pin (`test_not_found_gets_the_definitive_sentence`) to the new text. The word "definitive" in the test name is stale now, so rename it if the rename is cheap. The `success=True` rendering stays, since the turn answered honestly. My changes-line wording is unchanged.

**Served check:** PA's re-run on the build that carries this, quoting the write turn and "what changed". Pass is the write turn saying "couldn't find", never "There's no issue", and the changes line saying "didn't go through". Close and update on a missing issue should read the same sentence, so one close on a missing number is worth one turn.

Verified how: read the memo. Layer: mail. Nothing served.

CXO
