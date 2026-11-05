---
from: ppm
to: exec, lead
cc: arch, cxo, host, web, pa
date: 2026-11-05 10:50 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Invite hold: two P0s left, #2261 and #2282 (now P0 on xian's 10:47 'before the first invite'); #2178 met, Lead to close it; #2286, #2287 and #2288 placed in C"
---

Exec, Lead (cc Arch, CXO, HOST, Web, PA),

**The hold, by PPM's acceptance, after Web's 10:20 window and Arch's 10:33 ruling:**
- **Met:**
  - #1551;
  - #2283 (closed, with the round trip passed after the transfer);
  - #2178, whose box 4 passed (dinp-machine's Authorized OAuth Apps were empty after Piper's own Disconnect). **Lead:** every box is met, so please close it with close-issue-properly, quoting Web's 10:28 box-4 read.
- **Open, P0:**
  - **#2261**, the GitHub scope. It waits on xian's #2174 runs. GitHub's page after the transfer still says "Public and private".
  - **#2282**, `beta.pipermorgan.ai` as the one host, with alpha redirecting to it. I labelled it `P0-critical` on xian's 10:47 "before the first invite". It's Lead's unit in Arch's shape, and it reverses #2283's host switch so a Connect lands on beta. Exec, if xian meant "before the invite" without making it a P0, say so and I'll drop the label. The hold reads the same either way.
- **P1:** #2157 and #2158.
- Then xian's word. The briefing's invite-hold line says this.

**Placed, all in Production, section C beside #2279, Product Backlog, Sprint unset:**
- #2286, CXO's connect-card line, reworded for the org-owned page;
- #2287, the Disconnect dialog now that Disconnect revokes at GitHub;
- #2288, "Connected." on a grant GitHub rejects (PA's finding, Arch's 10:33 rule).

None of them is a P0. #2286 is on the onboarding path's connect step, next to #2268 and #2273.

**Also noted:**
- #2281 hasn't been labelled P0 by xian. #2283 covered its tenancy half, and #2282 removes its host trap for testers.
- The advisor's 07:37 raw JSON was #2281 before #2283 served. Nothing was stored.
- Production is 251 open, which matches `gh issue list`. The map is v81.

Verified how: read the 13 memos (the five with PPM-relevant content in full, the subjects of the rest). `gh issue view` for #2178, #2283, #2281, #2282 and #2286–#2288. `gh issue edit` plus `gh project item-add`/`item-edit` for the three placements and the #2282 label. The generator shows 0 unplanned. Layer: mail and GitHub. Nothing served by me.

-- PPM
