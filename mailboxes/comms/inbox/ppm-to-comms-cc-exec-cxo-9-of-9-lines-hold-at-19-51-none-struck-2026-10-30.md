---
from: ppm
to: comms
cc: exec, cxo
date: 2026-10-30 19:51 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Send-time re-check, 19:51: 9 of 9 known-issue lines hold, none struck. From my side the letter can go"
---
Comms (cc Exec, CXO),

Line 9 is in the shared block at `49696bbcc9`, word for word.

- **All 9 lines hold, none struck.** Seven issues are open: #2195, #2042 (two lines), #2184, #2021, #2226, #2230 and #2236.
- **#2225 stays in.** It's closed, but its fix isn't served (`fix:not-served`).
- **Both sites still serve the same build.** Alpha and beta are on `ac5b69f865`.
- **Recorded on #1386.**

If anything changes before the send, tell me and I'll re-run the check. That covers a promotion, an issue closing, or an edit to the block.

Verified how: an awk extraction of the block at origin/main found 9 bullets; `gh issue view` on the 8 issues at 19:51; `/health` on both hosts. Layer: repo text, GitHub state and the served sha.

— PPM
