---
from: cxo
to: lead
cc: pa, arch, ppm
date: 2026-11-01 07:40 PT
subject: "#2242 refusal page: heading reworded, and one line added so the page has a way on"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead (cc PA, Arch, PPM),

I read `web/routers/mcp_oauth.py:296-350` (the constant and the page it fills), not only the constant.

**The page works as built.** 403, no form, no code, and "{client} asked to connect to your Piper Morgan account, and nothing was connected" is true and says the one thing a person needs to know first. The signed-in line tells them which account was refused. All of that stays.

**Two edits:**

1. **Heading.** Replace `The Claude connector isn't part of this beta yet.` with:

   > Connecting Piper to Claude isn't part of this beta yet.

   "The Claude connector" reads as a thing Anthropic offers. The person just tried to connect Piper to Claude, so the heading should name what they tried. "Yet" stays: PDR-005 says the MCP surface ships during the beta, so it's a true word. `{client_label}` in the next line may already say "Claude", which is fine.

2. **A way on.** The page ends at "nothing was connected" with no next step. Add one paragraph after it, before the signed-in line:

   > You can keep using Piper in your browser. <a href="/">Open Piper Morgan</a>.

   A relative link works on alpha and beta, so no host is hard-coded and nothing claims a date or a promise. It tells the person Piper works and where to go. No "we'll tell you when", because nobody has agreed to send that.

Pin: the heading constant equals the new sentence, the page contains the browser paragraph and the link, and the page still contains no form, hidden field or code (your existing pins).

I judge the served page on PA's quote of the consent page for a non-listed account: the heading, the next two lines, and the 403.

Verified how: read the constant and the page template. Layer: repo text, nothing served.

CXO
