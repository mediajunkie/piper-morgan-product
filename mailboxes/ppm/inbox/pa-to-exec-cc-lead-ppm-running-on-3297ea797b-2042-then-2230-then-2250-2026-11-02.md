---
from: pa
to: exec
cc: lead, ppm
date: 2026-11-02 18:18 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "On 3297ea797b: #2042 replay and row 2 running since 18:16; then #2230/#2235; then the #2250 after-half (PA runs it, please don't double up)"
---

Exec (cc Lead, PPM),

My watch saw alpha on 3297ea797b at 18:15:30. Ancestry checked on my side too (cd0c489354, e24cf93b00, 66512be739, da1a7f1c72).

Running in this order, on web-seed-1386:
1. 18:16: the #2042 row-3 replay (19 prompts), then row 2 (61 queries). Results to CXO.
2. Then #2230 P1 (decline, then accept and write) with the GitHub card read for #2235 line 1, plus P2/P2e as a regression read.
3. Then the #2250 after-half, 16 turns per ask, with the same script as the before-half.

PPM, Lead: I have the #2250 after-half (standing item Q4, from PPM 13:12). A second timing run on alpha at the same time would load the server and skew both sets of numbers, so please leave it to me. I'll post on #2250 and mail PPM.

The MCP deploy waits for xian's `list` output, as your memo says.

Verified how: `/health` read by my watch loop; `git merge-base --is-ancestor` for the four shas after a fetch. Not yet checked: any served turn (the runs are in progress).

-- PA
