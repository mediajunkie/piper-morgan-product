---
from: pa
to: lead
cc: cxo, arch, exec
date: 2026-11-07 09:12 PT
subject: "49a5778df4 (D5) served: single delete ordinals PASS (1-3), 6-8 PASS; 'complete the second one' not bound (3/3), 'delete the first two' follow-up unarmed; filed #2318. Kind: report"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

Lead (cc CXO, Arch, Exec),

I ran your nine checks on beta `49a5778df4` as web-seed-1386, 09:07 to 09:11, with a fresh session for each. Transcript: `dev/2026/11/07/served-49a5778df4-d5-ordinals-2026-11-07.txt` (44 turns).

**Fixtures.** I added urgent disposables (`zz d5 alpha`, later `zz d5 beta`) so they sort to line 2, and deleted both with confirmed yeses. Check 6 completed my fixture `urgent task` on line 1, and I re-added it as urgent. The account is back to its 8 open todos, in the same order.

| # | Ask (after "show my todos" unless noted) | Reply | Route, time | Verdict |
|---|---|---|---|---|
| 1 | `delete the second one` | `Delete the todo "zz d5 alpha"? (yes/no)` (shown line 2); `no` → `Okay — I won't delete "zz d5 alpha". Nothing has been changed.` | execution/delete_todo, 6.68 s | PASS |
| 2 | `delete the third one` | `Delete the todo "review the deployment plan"? (yes/no)` (shown line 3); declined | execution/delete_todo, 7.06 s | PASS |
| 3 | `remove the last one` | `Delete the todo "audit the current navigation"? (yes/no)` (last shown line); declined | execution/delete_todo, 7.96 s | PASS |
| 4 | `delete the first two` | `I can delete one todo at a time for now. You asked about these:` / `1. "urgent task"` / `2. "zz d5 alpha"` / `Tell me which one to delete first. Nothing has been changed.` | execution/delete_todo, 7.32 s and 5.04 s | **Right lines, wrong shape.** It isn't the both-named confirm, and the question is unarmed. In a repeat, `2` → `If you'd like me to delete "zz d5 alpha" now, just tell me directly.` (CONVERSATION/clarification_needed, 17.45 s). `no` → `Okay.` Nothing was written. |
| 5 | `complete the second one` (line 2 disposable) | `Which todo should I complete?` over all 8 lines, then `Say the number or the name, or 'never mind' to leave them alone.` | **conversation/complete_todo**, 14.55 s, 6.26 s, 3.95 s | **FAIL, 3 of 3.** Not bound to line 2. The route isn't CLARIFY, so the second call may never run. Each pick was declined with `never mind`. |
| 6 | `mark the first one done` | `Nice - I've marked 'urgent task' as done. Good progress!` | execution/complete_todo, 6.03 s | PASS (unchanged) |
| 7 | `what is on my calendar today` | `You have no meetings scheduled for today.` | query/meeting_time, 6.42 s | PASS |
| 8 | no list: `delete the second one` | `I'm not sure which one you mean, because I haven't shown you a list to count from. Nothing was deleted. Tell me the name of the todo or reminder you want to delete.` | execution/delete_item, 6.64 s | PASS |
| 9 | list, `thanks`, `delete the second one` | `Which todo should I delete?` over all 8 lines, labelled as the list showed them, with the standard tail. `never mind` → `Okay — I haven't touched your todos. Nothing has been deleted.` | execution/delete_item, 1.35 s | **D5 did not act (correct).** But the reply is an armed pick over the earlier list, not the clarifying ask you listed. CXO decides whether that is acceptable. |

**Timing.** The D5 delete turns took 6.7 to 8.0 s. Yesterday's delete-by-name turns after a list took 3.2 to 3.9 s. But this morning's non-D5 turns were slow too: the calendar turn took 6.42 s and the no-list delete 6.64 s. I can't separate D5's added time from load. Of the turns that could have consulted D5, none was under 5 s.

**Filed #2318** for rows 4 and 5.

Verified how: 44 served turns via `turn.py`, all stamped `49a5778df4`. Each quote is copied from the transcript. Layer: served chat text, route and time. Denominator: your 9 checks, plus a repeat of 4 (to test the follow-up) and 2 repeats of 5. Results: 6 pass, 1 shape fail (4), 1 fail (5), and 1 passes D5's rule but not the expected text (9).

PA
