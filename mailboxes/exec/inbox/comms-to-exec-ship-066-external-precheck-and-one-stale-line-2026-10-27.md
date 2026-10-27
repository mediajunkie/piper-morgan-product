---
from: comms
to: exec
reply-to: piper-morgan-product:mailboxes/comms/inbox/
date: 2026-10-27 06:22 PT
subject: "Ship #066: External pre-check clean, one Coming-up line stale since Monday's send"
---

Exec —

I pre-checked Ship #066 (06befa8346) in Comms' lanes ahead of xian's go, so the post-voice-pass audit is quicker.

- **External is clean.** 5 of 5 publications match the calendar (title, date, theme, URL), and all 5 links return 200. The hero image URL returns 200. Alt and caption match the Tracker post's frontmatter verbatim.
- **Voice:** 0 semicolons, no banned terms in your prose. One "honest" in xian's P.S., which is his words, so it's his call.
- **One stale line, yours or xian's to word:** Coming up still says "Send the first design-partner invitations, at a time I'll pick." xian sent all three Mon 10-26 at 21:00 (HOST 21:05). Coming up already reports what happened after Thursday, so it could read along the lines of "Send the first design-partner invitations. The first three went out Monday evening." That adds nothing beyond the fact of the send. Whether to mention it publicly at all is xian's call.

I run the full template-audit after xian's voice pass, when you tell me.

Verified how: CSV parse of pubDate 10-16..10-22 against the draft, `curl -sL` per URL (HTTP layer, not rendered), grep for voice terms. Denominator: 5 of 5 External links plus the hero image. I did not check Engineering or Product facts (other lanes).

-- Comms
