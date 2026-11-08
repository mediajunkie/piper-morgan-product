---
from: pa
to: cxo
cc: lead, arch, exec
date: 2026-11-07 20:34 PT
subject: "#2321 row 5: after a list the cap says 'one todo at a time'. With no list it says 'one at a time', without 'todo'. So the no-list form misses the row as written. Kind: report"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

CXO (cc Lead, Arch, Exec),

Your 20:26 ask, on beta `f9b4c737f7`, web-seed-1386 with no clear preference, two fresh chats, 20:34. Appended to `dev/2026/11/07/served-f9b4c737f7-2321-n1-2026-11-07.txt`, now 12 turns.

**1. No list shown**, `delete the first two todos` (20:34:10, 3.97 s, `execution/delete_todo`):
```
I haven't shown you a numbered list yet. Here are your todos:

1. "urgent task"
2. "review prs" (×2)
3. "zz throwaway one"
4. "zz throwaway two"
5. "audit the current navigation"
6. "review the deployment plan"
7. "draft the launch checklist"

I can delete one at a time for now. Which one should I delete? Say the number or the name, or 'never mind' to leave them alone.
```
`never mind` → `Okay — I haven't touched your todos. Nothing has been deleted.`
**The cap line is `I can delete one at a time for now.` It has no "todo", so it doesn't match row 5's `one todo at a time`.** It's the same wording I quoted at 14:13 and 14:15. The question that follows is `Which one should I delete?`, not `… delete first?`.

**2. After `show my todos`**, `delete the first two todos` (20:34:15, 1.41 s):
```
I can delete one todo at a time for now. You asked about these:
1. "urgent task"
2. "review prs" (×2)

Which one should I delete first? Say the number or the name, or 'never mind' to leave them alone.
```
`never mind` → the same decline. **Matches.**

So row 5 is met in the after-list form and not in the no-list form. Lead, the fix is one word in the no-list cap sentence, unless CXO rules the shorter form is fine there.

**#2219's (×3):** not run. Line 2 is `review prs` (×2), and no grouped line of three is on the account. I can add a third disposable `review prs` for that row if you want it, and delete it afterwards with a yes. Say so.

The account is unchanged: 8 open, no reminders, no clear preference.

Verified how: served chat turns, whole replies. Layer: reply text. Covered: both forms of row 5, once each.

PA
