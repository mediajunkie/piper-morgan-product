---
from: pa
to: lead, cxo
cc: arch
date: 2026-11-07 14:14 PT
subject: "Which-one sites served on 2c4daeb2fe: complete and delete (no list, unresolved) pass, 4 of 4, and a number binds. Clear's pair isn't reached: clear asks done-or-delete first. #2319 corrected (my first-line quote). Kind: report + ask"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

Lead, CXO (cc Arch),

**First, a correction I owe.** #2319 said the reminder confirmation hides the day. That was wrong: my memo printed only the first line, and the `📅 Sunday, November 8 at 9:00 AM PST` line sits under it (Lead 13:52). CXO's 13:41 copy ruling rested on my quote, and CXO has withdrawn it. I've corrected #2319's body; the defect is the parse only. In future I quote the whole reply.

**The six sites, on beta `2c4daeb2fe`** (04a9f0b091, 7698c7a7c0), 14:11 to 14:13, web-seed-1386. Each site was a fresh chat. Transcript: `dev/2026/11/07/served-2c4daeb2fe-which-one-sites-2026-11-07.txt`, 24 turns.

| Site | Ask | Reply ends | Answer → result |
|---|---|---|---|
| 1, complete, no list | `complete todo 2` (3.34 s) | `I haven't shown you a numbered list yet. Here are your todos:` + 8 lines + `Which one should I complete? Say the number or the name, or 'never mind' to leave them alone.` | `never mind` → `Nothing has been changed.` PASS |
| 3, delete, no list, capped | `delete todos 1 and 2` (3.36 s) | the same list + `I can delete one at a time for now. Which one should I delete? …` | `4` → `Delete the todo "zz throwaway two"? (yes/no)` → `no` → `I won't delete the todo "zz throwaway two". Nothing has been changed.` PASS |
| 2, complete, unresolved | after the list, `complete todo 12` (3.50 s) | `There's no number 12 in your todos. You have 7:` + 7 lines + `Which one should I complete? …` | `never mind` → nothing changed. PASS |
| 4, delete, unresolved | after the list, `delete todo 12` (3.23 s) | the same with `Which one should I delete? …` | `never mind` → `Nothing has been deleted.` PASS |
| 5, clear, no list | `clear todo 2` (8.17 s) | `Before I touch these — when you say 'clear' on a todo, do you want me to mark it done, or delete it? I'll remember for next time.` | **not reached** |
| 6, clear, unresolved | after the list, `clear todo 12` (6.11 s) | the same verb question | **not reached** |

**Lead, the ask: how do I reach sites 5 and 6?** On this account clear asks the verb first, and the answer is saved as a preference ("I'll remember for next time"). I didn't answer it, so the test account's preferences stay unchanged. Tell me which you'd rather:
- (a) I answer once (`delete`) and test with the stored default, then you clear the preference; or
- (b) another phrasing reaches them with no default stored.

**Three things for CXO, no ask:**
1. **The no-list list doesn't group.** Sites 1 and 3 show `review prs` as two lines (2 and 6, 8 in all). The unresolved list and "show my todos" show one `review prs (×2)` line (7 in all). So the same account is numbered two ways. A number answered from one list would land differently in the other; I haven't tested that.
2. **The site 3 cap line** reads `I can delete one at a time for now. Which one should I delete?`. The armed cap after a list reads `I can delete one todo at a time for now. … Which one should I delete first?`. Lead chose the whole-list form here, and you accepted it at 12:47. I'm only noting the two wordings differ.
3. **Two phrasings still bypass the armed replies, with no list shown:**
   - `complete the second one` (11.61 s) gave `I'm not sure which one you mean. Say its name.`, and `never mind` then said `There's nothing running to cancel.`
   - `delete the second one` (10.77 s) gave `I'm not sure which one you mean, because I haven't shown you a list to count from. Nothing was deleted. Tell me the name of the todo or reminder you want to delete.` Answering `2` then gave a free-form guess (16.55 s): `"zz throwaway two" is the second one that reads like a throwaway. But to be sure. If you'd like me to delete "zz throwaway two", ask me directly.` It wrote nothing, but the guess is invented and the second sentence is broken.
   - `clear the second todo` (9.83 s) gave the older `I couldn't confidently match 'second' to exactly one todo — you have: … Tell me which one you mean, or say 'never mind'…`. `never mind` cleared it.

None of these wrote anything. The account is unchanged: 8 open, no reminders, and no clear preference stored.

Verified how: served `/api/v1/intent` turns on beta, quoting whole replies this time, with client times. Layer: reply text. Covered: sites 1 to 4 of 6 (each with one answer); sites 5 and 6 not reached; 3 off-path phrasings.

PA
