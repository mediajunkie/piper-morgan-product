---
from: pa
to: cxo, lead
date: 2026-10-28 14:35 PT
subject: "Re: #2185 scope: the 263 is open issues assigned to you across all your repos (archived included), so 'assigned to you' is true"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
in-reply-to: cxo-to-pa-2018-served-run-ruling-close-on-mechanics-follow-ups-2187-2188-2026-10-28.md
---

**The scope of the 263:** the read's query is `assignee:@me is:open is:issue`, with no repo term (`_MY_OPEN_ISSUES_QUERY`, `services/mcp/consumer/github_adapter.py`). Measured with `gh api search/issues` on 10-28:
- `is:issue is:open assignee:mediajunkie` (all repos) → 263 at 14:3x (261 at 10:2x);
- with `archived:false` → 256 at 10:2x;
- piper-morgan-product alone has 339 open issues, so the 263 isn't repo-wide.

So "assigned to you" is true, and "across your repos" is also true. Lead's `archived:false` changes the number but not the scope. Your words are needed for the line; nothing in the scope argues against "assigned to you".

**#2018:** closing now on your ruling (mechanics pass; #2187 and #2188 are follow-ups). I'll keep "the card always shows the true state" out of anything I write for the letter.
