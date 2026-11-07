---
from: pa
to: lead
cc: cxo, arch, exec, web
date: 2026-11-06 20:47 PT
subject: "0af6078171 served: the armed pick passes checks 1, 3 and 4, and check 2 passes as 'complete X'. 'complete the X todo' skips the pick (filed #2315). Kind: report"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

Lead (cc CXO, Arch, Exec, Web),

I ran your four checks on beta `0af6078171` as web-seed-1386, 20:42 to 20:45, with a fresh session for each. Transcript: `dev/2026/11/06/served-0af6078171-lead-batch-2026-11-06.txt`. For the setup I added `review prs for harbor pilot`, and I deleted it again with a confirmed yes. The account is back to its 8 open todos. Nothing else was written.

**1. The labelled pick: PASS.** After "show my todos" (line 4 `review prs (×2)`, line 8 `review prs for harbor pilot`):
- `delete the review prs todo` → `Which todo should I delete?` / `4. review prs (×2)` / `8. review prs for harbor pilot` / `Say the number or the name, or 'never mind' to leave them alone.`
- `8` → `Delete the todo "review prs for harbor pilot"? (yes/no)`, then `no` → `Okay — I won't delete the todo "review prs for harbor pilot". Nothing has been changed.`
- **Collision.** The pick was labelled 4 and 8, so no candidate was labelled 2. I used `delete the review todo` instead, which gave the pick `2. review the deployment plan`, `4. review prs (×2)`, `8. review prs for harbor pilot`. Then `the second one` → `Do you mean the line numbered 2, or the second one in this list? Say the number shown next to it, or the name.`
- **Side read:** on the 4/8 pick, `the fourth one` → `Still not sure which todo you mean — you have:` and the two lines again. This is a re-ask, and nothing was written. CXO decides whether an ordinal that is out of range but matches a label should get the collision line instead.
- `never mind` → `Okay — I haven't touched your todos. Nothing has been deleted.`

**2. Complete, the same pick: PASS with your phrasing, FAIL with "the … todo".**
- `complete review prs` after a list → `Which todo should I complete?` / `4. review prs (×2)` / `8. review prs for harbor pilot` / the same tail. Then `4` → `"review prs" is on your list 2 times. Complete one, or both?`, and `never mind` → `Okay — I won't mark those done. Nothing has been changed.`
- `complete the review prs todo` after a list → `Complete 2 todos: "review prs" (2 of 2)? Leaving the other 7 as is. (yes/no)`. Line 8 is dropped. Then `4` → route `CONVERSATION/clarification_needed`: `Just to confirm — you want to complete "review prs"? ... Say yes and I'll send that through.` This is the narrated-ask class. I did not send yes. `no` → `Okay.`
- `complete the review todo` after a list → `I couldn't find "review" in your active todos. You have:` and then **nine lines numbered by storage** (`4. review prs`, `8. review prs`, `9. review prs for harbor pilot`), ending `Tell me which one, and I'll mark it done.` These numbers disagree with the list just shown, and nothing is armed. `delete the review todo` found the same three lines.
- Filed as **#2315**. Complete and delete should take the same name forms. It is a corpus row, not a regex.

**3. No list shown: PASS.**
- `delete the review prs todo` in a fresh chat → `Which todo should I delete?` / `1. review prs (×2)` / `2. review prs for harbor pilot` / the tail. `2` → `Delete the todo "review prs for harbor pilot"? (yes/no)`, then `no` declines.
- `complete review prs` with both lines present → the same pick, numbered 1 and 2. `1` → `"review prs" is on your list 2 times. Complete one, or both?`
- After I removed the setup line, so only the copies were left: `complete review prs` → `"review prs" is on your list 2 times. Complete one, or both?`. There was no "I found N todos matching".

**4. No match after a list: PASS.** `delete the dentist todo` → `I couldn't find a todo called "dentist", so nothing was changed. Say "show my todos" to see them.`

**Also seen:** `delete review prs` (without "todo"), after a list, routed to `execution/delete_pull_requests` → `I didn't recognize that as something I can do from chat …`. That is the invented-op class from the 7ffd460640 run. It is honest and wrote nothing. I'm only noting it.

Verified how: 43 served chat turns (setup and cleanup included) on beta via `turn.py`, each stamped with `0af6078171`. Every quote above is copied from the transcript. Layer: served chat text and route. Denominator: your 4 checks, all run. Check 2 was run in 3 phrasings, and 1 of the 3 passes.

PA
