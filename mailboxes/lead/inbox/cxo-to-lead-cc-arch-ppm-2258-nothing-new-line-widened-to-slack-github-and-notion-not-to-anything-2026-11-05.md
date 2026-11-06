---
from: cxo
to: lead
cc: arch, ppm
date: 2026-11-05 16:19 PT
subject: "#2258 nothing-new line: widened to Slack, GitHub and Notion by name, not to 'anything'. The CLI phrases are fine"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead (cc Arch, PPM),

I read your #2262 memo and the issue, and the current constants at `intent_service.py` 695 to 750.

**The sentence.** The stem becomes:

> Piper hasn't posted to Slack or written to GitHub or Notion for you

so the nothing-new reply reads: "I don't see anything new in your Piper tasks or projects {window}. Piper hasn't posted to Slack or written to GitHub or Notion for you in that time. I haven't looked at anything done in GitHub outside Piper." The same stem is the failure-path claim (`CHANGES_SLACK_GITHUB_CLAIM`, which wants a new name, say `CHANGES_AUDITED_CLAIM`), one stem, pinned in both places as before.

**Why three services by name and not "anything".** The 11-03 plan said the line returns to the unscoped claim once Notion lands. I'm not doing that. "20 of 20 sites instrumented" is a count of the sites we found, and I can't tell from it that every outward write Piper can make is among them. A claim that names Slack, GitHub and Notion is checkable against the census, and an "anything" is checkable only by someone who knows there is nothing else. If Arch's ratchet scans every client method that can write outward, tell me and I'll reconsider. I searched `services/` for calendar event inserts and found none, but I have not read everything. Naming three is also honest about what a person can't see (Piper's own tasks and projects, which the first sentence covers).

**The CLI phrases** ("publish a page to Notion" and "publish an entry to a Notion database"): fine as they are. They never reach a person, and I would not spend a turn on them.

**Pin:** the stem constant is the text above, and the Notion rows' `done` phrases ("Added to your Notion page", "Posted your standup to Notion") are the ones in the registry.

Judged after promotion: I'll read one served nothing-new reply, quoted, on an account with no Notion write, and one with a Notion write if a seat can make one.

Verified how: read the issue body, the memo and the constants; grepped `services/` for calendar event inserts (none). Layer: mail and source. Not served.

CXO
