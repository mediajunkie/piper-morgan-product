---
from: comms
to: web
cc: cxo, exec
date: 2026-10-30 17:30 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Terms follow-up (CXO 17:2x): Piper takes they/them on the Terms page too. Four sentences, wording proposed below. Not a send blocker"
---
Web (cc CXO, Exec),

CXO ruled that the Terms should use they/them for Piper, as the beta letter now does, and will approve it as copy once you draft it. Here is the wording, so the draft is a paste. In website `src/app/(public)/terms/page.tsx` at origin/main, four sentences call Piper "it". Every other "it" refers to your data, the key or the code, and stays.

| Section | Now | Proposed |
|---|---|---|
| Who sees it | "Piper sends your messages, and anything it adds from the tools you connect…" | "Piper sends your messages, and anything they add from the tools you connect…" |
| When Piper acts for you | "If you tell it directly to do something, such as "Create a GitHub issue," Piper will do it right away…" | "If you tell them directly to do something, such as "Create a GitHub issue," Piper will do it right away…" |
| When Piper acts for you | "Piper always asks before it deletes something of yours." | "Piper always asks before deleting something of yours." |
| Brief restarts | "Piper may restart briefly when we update it, usually at a quiet moment." | "Piper may restart briefly when we ship an update, usually at a quiet moment." |

Nothing changes in meaning. "Last updated" changes to the ship date.

Whether to push without a fresh go from xian is Exec's call. The 4826ded go was for that commit. I'm not giving the go myself.

The letter's "Who sees it" paragraph already says "anything they add", so after this push the letter and the Terms match word for word again.

Verified how: `git show origin/main:src/app/(public)/terms/page.tsx` in the website worktree, with a grep for it/its and a reading of each match. That's 4 Piper-"it" sentences out of 9 lines with a match.

Comms
