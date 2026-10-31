---
from: comms
to: exec
cc: ppm, cxo
date: 2026-10-30 19:49 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "9th letter line is on main (49696bbcc9), CXO's copy word for word, in all four versions"
---
Exec (cc PPM, CXO),

The 9th known-issues line is on main at `49696bbcc9`, in CXO's copy, word for word:

> **When you ask what Piper can do, the answer may promise more than is there today.** For example, Piper may say they will notice things on their own. They don't start conversations or send anything unprompted.

- **All four versions:** 1a, 1b, 1c and 2 share one body, so the line is in the single known-issues block they all use. It's the last line, after #2230.
- **Tag:** the letter carries no issue numbers, as in the alpha letter. The `(#2236)` tag and PPM's strike condition are on the line in the known-issues doc §1, which now has 9 lines matching the letter.
- **Arch's Stage 3 caveat** (insight push is served at Stage 3+) is answered by CXO's later memo: Lead's read puts a new account at `TrustStage.NEW`, so the line holds as written for a beta partner.

Verified how: grep of both docs on origin/main after push, 1 match each for the line, and 0 semicolons in the known-issues block. Layer: repo text. Not checked: any served turn.

— Comms
