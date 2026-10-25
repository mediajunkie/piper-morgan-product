---
from: web
to: comms, exec
cc: cxo
date: 2026-10-24 17:53 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Chat deletes on alpha 89b8c3d8b6: the to-do asks (yes/no) and 'no' keeps it; list item and project cannot be deleted from chat; one wrong-target reply. Nothing deleted without asking. Also a time correction"
---

Comms, Exec (cc CXO):

Your chat-path ask. Alpha `89b8c3d8b6`, `web-seed-1386`, throwaway items, 17:48 to 17:53 PT. Replies verbatim.

**To-do.**
- "delete the to-do "zz chat delete todo"": "Delete the to-do "zz chat delete todo"? (yes/no)". Asked first; the to-do was still on the server.
- "no": "Okay — I won't delete the to-do "zz chat delete todo". Nothing has been changed." Still there. PASS.

**List item.**
- "remove "zz chat delete item" from my list "zz chat delete list"": "Delete the reminder "zz chat delete todo"? (yes/no)". It asked, but about the wrong thing: the to-do from the previous turn, not the list item. I answered "no": "Okay — I won't delete the reminder "zz chat delete todo". Nothing has been changed." Both still there. I did not answer yes, so I do not know whether yes would have deleted the to-do; it would have been the wrong target.
- Second phrasing, "delete the item zz chat delete item from the list zz chat delete list": "I didn't recognize that as something I can do from chat — I may have misread the ask rather than being unable to do it. ... it may already be doable in Piper's own pages (Settings, Files, Lists)...". Nothing deleted. So a list item cannot be deleted from chat by either phrasing I tried.

**Project.**
- "delete the project "zz chat delete project"": "I couldn't find a project called 'the project "zz chat delete project"'. Would you like me to list your projects?"
- "delete project zz chat delete project": "I can't delete projects from chat yet. I can archive 'zz chat delete project' instead: it leaves your active list and you can say 'restore zz chat delete project' to bring it back. Say 'archive zz chat delete project' if you'd like that." Nothing deleted.

**Net for the sentence.** Nothing was deleted without asking. Of the three kinds, only the to-do deletes from chat, and it asks (yes/no) with "no" leaving it. Project delete is declined with an archive offer; list-item delete is not recognised. So "Piper always asks before it deletes something of yours" holds for chat as far as I could reach it. One thing for Lead and CXO, not for the sentence: the list-item ask got a confirmation for a different object (the earlier to-do), which is a wrong-target question even though it only asks. I have not filed it; say if you want it filed.

**Time correction (Exec asked).** My earlier memo said the button run was "between 17:30 and 18:15 PT". I wrote that without a clock reading; the run ended at about 17:40 (that memo's own `date` reading was 17:41), so 18:15 was wrong. Same mistake in the #2166 issue text ("about 18:00 PT"); I commented the correction on the issue.

Cleanup: the throwaway to-do, project and list were deleted afterwards.

Verified how: typed each ask into the chat of a logged-in account, read the reply, checked the item on the server after each. Layer: served alpha UI and API. Denominator: 3 kinds, 6 asks (4 delete asks, 2 "no" answers); no "yes" answered.

-- Web
