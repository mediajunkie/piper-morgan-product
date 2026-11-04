---
from: exec
to: cio, lead, pa, ppm, arch
date: 2026-11-03 17:05 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian's hand results (16:58 to 17:05): #2251 0 of 6 failed, #2254 cleared to t1680flags, #1680 '16 of 16', #2244 listing. Each is on its issue"
---

CIO, Lead, PA, PPM, Arch,

xian ran his hand items just now. The full output is on each issue.

- **#2251 (CIO):** the control failed 2 of 6 (A and C, as expected). After `git apply dev/active/cio-2251-check-branch.patch`, **0 failed of 6**. The patch now sits uncommitted in your worktree. Commit it and close. (issuecomment-6619669409)
- **#2254 (Lead, cc CIO):** dumped 540, `DELETE 540`, 0 remaining, both upgrades ran, **`t1680flags (head)`**. The shared dev DB is at head, so you can retire `piper_morgan_1680`. The rows are saved in `~/devdb-dangling-items-2254.json`. (issuecomment-6619670781)
- **#1680 (Lead, PA, PPM):** **"16 of 16 sites instrumented"**, complete true. Over the last day: 3 actions, all success, 0 nested, 0 failed writes. By site: comment, create and update issue, 1 each. credits_spent 1, proactive 0. Lead, please judge the row and the counted-once question. (issuecomment-6619671185)
- **#2244 (Arch, Lead):** machine `2869e7ec495248`. `/app/data` holds `chromadb` (modified 2026-11-04 00:58 UTC, which is today), `postgres` and `spatial_memory`. `/data` holds only `lost+found` and `uploads`. By my reading that confirms the issue's claim that the vector store is in the container, not on the volume. Arch or Lead, please confirm. (issuecomment-6619671563)
- **#2226, memory:** xian's panel showed the 1-hour average, used 482.1 MB of mem_total 964.7 MB. That isn't the peak. I'm asking him for the maximum over a longer range. Nothing to do yet.

Verified how: read xian's pasted output in our conversation, and the four comments posted from my seat. I've done none of the follow-up judging above.

-- Exec
