---
from: ppm
to: comms
cc: cxo, exec, pa, host
date: 2026-10-30 08:04 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Row 5 met; #1386 is down to row 6 and go/no-go. Known-issues pre-check: all six lines still hold. One retag: the 'misreads' line's #1595 becomes #2195. The #2101 stall line stays out"
---

Comms (cc CXO, Exec, PA, HOST),

**Row 5's final read is done**, at xian's word via PA. Since 10-27: 0 P0/P1. CI is 12 of 12 green, and alpha is healthy on `e234776150` (#1386 comment 6525943984). **Rows 1-5 are done.** What's left is row 6 (your letter, after xian's HOST conversation) and his go/no-go.

**Known-issues pre-check**, so the send-time check is quick. I took each line in `design-partner-known-issues-and-calendar-lines-2026-10-19.md` §1 against `gh issue view` at 08:0x:

| Line | Issue state | Verdict |
|---|---|---|
| Piper sometimes misreads what you ask | #1595 CLOSED 10-29 (by split); the remainder is **#2195, OPEN** | **Keep. Retag (#1595) to (#2195)**, so a strike-at-send on a closed issue doesn't drop a true line |
| An answer about your own data can be wrong (#2042) | OPEN | Keep |
| No undo for deleted to-dos (#2019, #2021) | #2019 CLOSED (the one-at-a-time cap is what it built); #2021 OPEN (no undo) | Keep, as written |
| Searching your documents from chat doesn't work yet (#2122) | CLOSED 10-21, with the truthful decline as its fix | Keep (CXO 18:48 wording) |
| Milestone's issues in two steps (#2184) | OPEN | Keep; strike only on a served close |
| A detail Piper did not look up (#2042 class) | #2042 OPEN, rung 3 not served | Keep |
| *Contingent #2101 stall line* | #2101 CLOSED 10-20 | **Stays out** |
| *#2166 Share line* | dropped 10-24 (Share hidden, CXO 3 of 3) | Stays out |

I re-run this check against the final letter when you send it, and that read is row 6's second box. The first box (GitHub and Google Calendar named in xian's wording, with the plain Calendar caveat) is yours and CXO's. I check that it's there.

Verified how: `gh issue view` on #1595, #2195, #2042, #2019, #2021, #2122, #2184, #2101 and #2166 at 08:0x, against §1 of the draft as committed (c390dc02df, 10-29 21:21). Layer: GitHub state and draft text. I didn't check the served behaviour behind each line this time. Denominator: 6 of 6 listed lines plus 2 out-of-list lines.

-- PPM
