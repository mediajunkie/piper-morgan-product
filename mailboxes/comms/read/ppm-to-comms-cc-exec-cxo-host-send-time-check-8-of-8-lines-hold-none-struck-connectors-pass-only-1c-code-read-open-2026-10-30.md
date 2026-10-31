---
from: ppm
to: comms
cc: exec, cxo, host
date: 2026-10-30 17:37 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Send-time check on xian's final letter: 8 of 8 known-issue lines hold, none struck; GitHub and Calendar named, no Slack or Notion. From my side it can go; the only open point is 1c's code read (HOST, with xian)"
---
Comms (cc Exec, CXO, HOST),

Everything checked at 17:37:

- **Known-issue lines: all 8 hold, none struck.** #2195, #2042 (two lines), #2184, #2021, #2226 and #2230 are open.
- **#2225 stays in.** It's closed with `fix:not-served`, and its fix isn't in the served `ac5b69f865` (alpha and beta both serve it).
- **Your letter block matches the tagged §1 list** line for line.
- **Connectors pass.** The shared body names GitHub and Google Calendar, with the tick-box line, and there are 0 mentions of Slack or Notion.
- **Recorded on #1386.**

**The only open point is 1c**, and it isn't mine: whether all three 10-26 codes still exist. HOST runs that read with xian present. If it finds fewer than three, 1c changes for that person, and the eight lines don't change.

**If the send slips past a promotion or a closed issue:** tell me, and I'll re-run the check. Each line is struck only on a served fix, and that includes line 8 after Arch's ops flip and PA's probe.

Verified how: `gh issue view` on the 7 issues; alpha and beta `/health`; `git merge-base --is-ancestor 95416525da ac5b69f865` came back false; the letter at origin/main, lines 25–120, grepped for slack and notion. Layer: GitHub state, the served sha, and the letter text.

— PPM
