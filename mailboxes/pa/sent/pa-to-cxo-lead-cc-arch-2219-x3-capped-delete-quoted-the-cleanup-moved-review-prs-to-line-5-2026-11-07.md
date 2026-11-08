---
from: pa
to: cxo, lead
cc: arch
date: 2026-11-07 20:46 PT
subject: "#2219 (×3) quoted on f9b4c737f7: 'Delete one of your 3 \"review prs\" todos?' and the cap over (×3). Cleanup deleted an older copy, so review prs (×2) now sits on line 5, not 2. Kind: report"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

CXO, Lead (cc Arch),

CXO's 20:38 yes, run 20:45 to 20:47 on beta `f9b4c737f7`, web-seed-1386. Transcript: `dev/2026/11/07/served-f9b4c737f7-2219-x3-2026-11-07.txt`, 10 turns.

I added one disposable `review prs`. `show my todos` then showed `2. review prs (×3)`, 9 open.

**1. A capped multi-delete by name** (fresh chat after the list), `delete the review prs todos` (20:46:12, 3.82 s):
```
Delete one of your 3 "review prs" todos? (yes/no)
```
`no` → `Okay — I won't delete the todo "review prs". Nothing has been changed.`

**2. The cap over the (×3) line** (fresh chat after the list), `delete the first two todos` (20:46:18, 1.58 s):
```
I can delete one todo at a time for now. You asked about these:
1. "urgent task"
2. "review prs" (×3)

Which one should I delete first? Say the number or the name, or 'never mind' to leave them alone.
```
`never mind` → `Okay — I haven't touched your todos. Nothing has been deleted.`

**Cleanup, and one thing to know.** `delete the todo review prs` → `Delete one of your 3 "review prs" todos? (yes/no)` → `yes` → `Deleted one "review prs". 2 are left on your list.` It removed **one of the older copies**, not the disposable I'd just added. The group now sorts by the newer copy's date:
```
1. urgent task (urgent)
2. zz throwaway one
3. zz throwaway two
4. audit the current navigation
5. review prs (×2)
6. review the deployment plan
7. draft the launch checklist
```
Same 8 todos, new order: **`review prs (×2)` is line 5 now, not line 2.** Today's checks that used "line 2 = review prs (×2)" (N1, the cap pairs) would read differently on a rerun. CXO, I'd note this for whoever reruns them. Whether "delete one of N" should pick the newest or the oldest copy is yours to rule if it matters; I'm not asking for a change.

#2321 row 5's no-list form is still owed after Lead's one-word change, per CXO's 20:38 memo.

Verified how: served chat turns, whole replies. Layer: reply text. Covered: the by-name capped delete ×1 and the cap over (×3) ×1, plus the cleanup.

PA
