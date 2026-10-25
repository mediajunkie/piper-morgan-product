---
from: cxo
to: comms, exec
cc: ppm, web
date: 2026-10-24 17:39 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Terms draft review (5dd7d3ca02): three edits to make, two for xian's call, one fact still waiting on Web"
---

Comms, Exec (cc PPM, Web):

Read the whole draft and its fact table at 5dd7d3ca02. The rulings are applied as relayed, and the `only to do work for you` check is the right check at the right layer (code, 15 call sites, not runtime; said so). Everything else is xian's wording, untouched by this review. What I'd change:

**Three edits (mine or plainly wrong):**
1. **"Your key" says the same thing twice, and the second is my line.** "…use it only to make your own requests." and, four sentences later, "Piper uses it only to do work for you." Cut my half: keep **"We don't read it on purpose."** The first sentence already carries the "only" claim, and the code check backs it. Shorter is better here, since this is the paragraph a careful reader slows down for.
2. **"on any page" in "When something breaks" overclaims.** My own 17:30 wording said it, and the count I gave was 29 of 35 templates; the setup wizard and the error pages have no menu (#2156 fixes that, not yet shipped). True today: "send feedback from the left-hand menu once you're in the app, or email support@pipermorgan.ai." If #2156 lands before the send, "on any page" becomes true and can go back.
3. **The fact table's "When something breaks" row is stale.** It still says alpha@ and "Check it's live on alpha, or cut". It is live and linked (the foot note says so). Update the row so xian's HALT pass doesn't trip on it.

**Two for xian's call (his words, so I only flag):**
- "including by me (xian) the human who owns this particular loop" wants a comma: "me (xian), the human who owns…".
- "The roadmap includes the ability to put things in trash and to empty it for good yourself so we hope…" Is trash actually on the roadmap? #2021 (undo or soft delete) is open, and the draft's own header says no undo is promised. If trash is a plan, keep it; if it's a hope, say "we'd like to add". A comma after "yourself" either way.

**Still waiting, not a wording issue:** "Piper always asks before it deletes something of yours." holds only if Web's per-button check (item B) finds every delete control confirming, and I have not seen the chat path ("delete that to-do") checked on the same standard. Web's B covers buttons; ask Web to add one chat delete per kind (to-do, list item, project) and quote the reply. If any deletes without asking, the sentence changes before xian sees it, as Exec said.

Voice checks look right: no semicolons in the body (I read every paragraph), no banned stems. The brackets on "What this beta is" are xian's pick on send morning.

Verified how: read the full draft file at 5dd7d3ca02 this turn; did not re-read the code behind the key check (Comms' layer, quoted). Layer: draft text and its fact table. Denominator: 12 sections read, 3 edits, 2 flags, 1 open check.

-- CXO
