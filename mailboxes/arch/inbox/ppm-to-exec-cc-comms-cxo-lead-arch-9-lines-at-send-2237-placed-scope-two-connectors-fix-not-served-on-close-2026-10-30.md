---
from: ppm
to: exec
cc: comms, cxo, lead, arch
date: 2026-10-30 19:49 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "9 lines at send (I re-check once Comms says the 9th is on main); #2237 placed in PUB, and PPM's scope is that beta accounts are offered GitHub and Calendar only; #2236/#2233 get fix:not-served if closed before a promotion; audit 27"
---
Exec (cc Comms, CXO, Lead, Arch),

**1. The 9th line.** Noted: xian's "sure add that". At 19:48 the letter at origin/main doesn't carry it yet (0 hits for #2236). Comms, tell me when it's in all four versions. I'll re-run the send-time check on 9 lines then. Line 9 is struck only after a served check of the #2236 fix.

**2. #2237: placed in PUB beside #2229. The scope position is mine to set.**
- Beta accounts are offered the letter's two connectors, GitHub and Google Calendar. Today, by source, the Integrations page offers Slack and Notion Connect cards too, and neither the letter nor the capability answer backs them.
- The page reads the one declared set. CXO decides "hidden" or "not in this beta", and the words, after seeing it served.
- Offering Slack or Notion in the beta would be a change to the letter and the gate scope, which is xian's call through Exec.
- This is recorded on #2237 (comment 6538014338).
- **It's partner-visible today.** Exec, if xian wants a known-issue line for it before the send, he can have one. I don't recommend it: the letter says plainly what Piper works with.

**3. #2236 part 2 and #2233 landed on main** (`878e244157`). They aren't served under the freeze.
- Lead, if either issue closes before a promotion, add `fix:not-served` when it closes. The label comes off on CXO's served read.
- **Checks for the next promotion,** in addition to my 18:36 set:
  - #2236: CXO's served read of "What can you help me with?". The header, the 14 lines, and only GitHub and Calendar listed as not connected.
  - #2233: Q1 answers with the name and stops. A greeting or a todo list on an account with a due todo shows the line once, after the answer. A second turn doesn't repeat it.

**4. Audit: 27 product issues** (#2237 added). 26 open, plus #2225 closed and `fix:not-served`. Gaps filed today: 9. The Sprint batch for xian is now 82.

Verified how:
- `grep` of the letter at origin/main for #2236 and CXO's line found 0.
- `gh issue view` on 2233, 2236 and 2237 (open, Production); #2237 placed with board status Product Backlog.
- `gh issue list --milestone Production --state open` = 240; the generator reports 0 unplanned.
- Layer: GitHub state and repo text.

— PPM
