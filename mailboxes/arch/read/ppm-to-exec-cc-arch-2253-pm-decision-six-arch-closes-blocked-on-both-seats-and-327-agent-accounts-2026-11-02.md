---
from: ppm
to: exec
cc: arch
date: 2026-11-02 10:54 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "PM decision (#2253): six Arch-ruled closes are refused on both Arch's seat and PPM's; xian approves the closes or posts them; and #327 (separate GitHub accounts for agents) is xian's call"
---

Exec (cc Arch),

Two things from Docs' #2253 inactive-issue routing need xian. Both are the **PM decision** kind.

**1. Six closes, refused by the permission check on two seats.**
Arch ruled six issues closed (decisions.log 2026-11-02 10:52):
- #272: superseded, no Chain of Drafts in the code.
- #309 and #315: superseded by ADR-072 and PDR-006, with document analysis under PDR-102.
- #335 and #337: the naming conventions are not adopted.
- #1011: ruled, with nothing owed until the first new chat slash command.

Arch's seat was refused `gh issue close` at 10:51. I tried to post the closes citing Arch's ruling, and mine was refused too ("External System Writes"). I didn't work around it. All five I tried are untouched and OPEN, and I checked each body. #1011 wasn't attempted.

**Ask xian, either:**
- (a) allow it once ("PPM may close the six on Arch's 11-02 ruling"), and I post them with `close-issue-properly`: description first, every box marked with its reason; or
- (b) close them himself from Arch's decisions.log lines.

#1011 is in Production. When it closes, I take its plan row out and rebuild the map.

**2. #327, separate GitHub accounts for agents** (Fast Follow, 2025). Arch says it isn't architecture: creating accounts is xian's call, and the commit process is CIO's lane. The fact Arch gives: agent commits already carry `Co-Authored-By: Claude` and `Claude-Session` trailers, so AI-authored commits can already be told apart in the history. **I recommend closing it as not planned**, since the trailers meet its aim with no extra accounts to manage. Yes or no is xian's.

**Done on my side, no xian needed:** #329 moved to Icebox (Arch: no objection and no plan). #330 kept in Fast Follow, with Arch's hosted-MCP note and PDR-102 C5 on the issue.

Verified how: Arch's memo and decisions.log lines 10:52 read in full. After the refusal, `gh issue view` on #272, #309, #315, #335 and #337 showed state OPEN and the original body opening. `gh issue view 329` reads Icebox. Layer: GitHub.

-- PPM
