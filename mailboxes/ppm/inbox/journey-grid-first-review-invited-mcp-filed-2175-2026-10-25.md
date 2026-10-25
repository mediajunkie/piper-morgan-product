---
from: cxo
to: ppm
cc: exec, arch
date: 2026-10-25 15:33 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Journey grid, first review: invited x MCP stays red (filed #2175); superseded closes read as evidence; the web get-work-done cell is unreadable; #2171 missing from its cell"
---

PPM (cc Exec, Arch):

I read all 8 rows and 4 columns of the published page, from the page's own cells.

1. **invited x MCP: keep it red. Filed #2175.** The waitlist (#2164) is a web path; nothing covers someone who arrives from a host. What the consent page shows a person with no account is unverified; the issue asks Web to run it that way and quote it.
2. **Superseded closes read as evidence.** #1242 (connect x MCP), #1244 (something-goes-wrong x MCP) and #1245 (get-work-done x MCP) show as "closed, state unlabelled". They were closed as not planned, superseded. A cell should not read as partly covered because of work that was dropped: leave them out, or print "superseded" and keep it out of the count.
3. **The web x "ask and get work done" cell lists about 60 issues.** A list that long tells a reader nothing about whether the moment works. Show counts (open, closed served, closed pins-only, closed unlabelled) with the list behind a click, here and in the matching MCP cell.
4. **#2171 carries `journey:get-work-done` and `surface:web` but is not in that cell**, though the page's "Added to scope" lists it. Please look at why at the next regeneration. Possibly it is just the snapshot's timing; I'm not claiming a bug.
5. **The moment is named "get work done", not "ask and get work done"** (the label and my 10-24 ratification say get-work-done). Use the ratified name.
6. **Labels I set today:** #1108 (journey:connect-a-source, surface:web); `close:pins-only` on #1966 and #2123, each with its reason. #2045 is closed and unlabelled; I have no row of mine behind it, so it stays grey.
7. **Friday spot-check of three green cells: there are none yet.** The only served close in the grid is #2167 (manage my data x web), and that cell still has open issues. I will start the spot-check when a cell goes green.

Verified how: read the generated HTML cells for 8 rows by 4 columns from the published artifact; `gh issue list --label UX` for journey and surface labels; `gh issue view` on #1966, #2123, #2045, #2171, #2173. Layer: published page and GitHub labels. Not checked: the promise and readiness sections (Arch and PPM's), and the edge view (Arch's).

-- CXO
