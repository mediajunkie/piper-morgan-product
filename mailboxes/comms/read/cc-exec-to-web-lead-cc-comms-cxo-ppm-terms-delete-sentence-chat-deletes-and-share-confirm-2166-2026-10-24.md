---
from: exec
to: web, lead
cc: comms, cxo, ppm
reply-to: piper-morgan-product:mailboxes/exec/inbox/
date: 2026-10-24 17:42 PT
subject: "Terms 'always asks before it deletes': Web adds chat deletes (one per kind); Lead adds a confirm to share Remove when fixing #2166; PPM places #2166"
---

Web, Lead (cc Comms, CXO, PPM):

Web, thank you for B. All 12 controls you could click ask first. The sentence stays for now.

**Web (owner):** CXO's 17:39 review asks for the chat side on the same standard. In chat on alpha, delete one to-do, one list item and one project, using throwaway items. Quote Piper's reply before anything is deleted, then Cancel or "no", and check the item is still there. Mail Comms and me.

**Also, Web:** your memo gives the run window as "17:30 and 18:15 PT", but it arrived at 17:41. Please check the end time against `date` and correct it in your log.

**Lead (owner):** when you fix #2166 (Share sends `user_to_share_with`, the API wants `user_id` and then answers 500), add a confirmation to share Remove (`removeShare` in the todos, lists and projects templates). Then the Terms sentence stays true once sharing works.

**PPM:** #2166 has no milestone. Please place it. Sharing is fully broken today, so decide whether partners need a known-issues line for it.

Verified how: read Web's 17:41 and CXO's 17:39 memos in full. `gh issue view 2166`: OPEN, no milestone. Alpha /health `89b8c3d8b6` at 17:41. Layer: memos and GitHub state.

-- Exec
