---
from: exec
to: ppm
cc: arch, cxo
date: 2026-10-23 18:10 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian's concern about reusing old PROD-* Sprint options: a sprint that spans several milestones makes the statistics read strangely. Before he adds the three new options, check whether the six reused ones carry issues (open or closed) from other milestones, and recommend reuse or fresh names."
---

PPM (cc Arch, CXO):

xian, 2026-10-23 18:10 PT, on mapping C, E, T, Doc, Dist and Q onto existing PROD-* options: "My only concern about recycling older sprint names is that it then takes a sprint and it splits it over several milestones, presuming that each of those sprints has some closed issues in them. Although maybe that's not so … It just may make some of the statistics read strangely at some point when we say, 'Hey, this sprint had 500 issues in it.'" He calls it a minor point ("It doesn't really matter too much").

**Ask (read-only):** for PROD-RECONNECT, PROD-DESIGN, PROD-TRUST, PROD-DOCS, PROD-DIST and PROD-TECHDEBT, count the items by milestone and state (open and closed), for example with `sprint-truth.py` or a board export. Then recommend one of:
- **(a)** reuse as is, if nearly everything is Production;
- **(b)** fresh names for these too (xian adds them, you move the issues, and the old options stay as history);
- **(c)** reuse, but report sprint statistics by milestone.

Put the answer in your map-review memo or a short note. xian waits for it before he adds any options.

-- Exec
