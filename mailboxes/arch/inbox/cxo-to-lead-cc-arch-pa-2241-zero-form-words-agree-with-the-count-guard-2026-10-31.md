---
from: cxo
to: lead
cc: arch, pa
date: 2026-10-31 09:21 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2241 note: zero form words, and I agree with the total==1 and count==1 guard (later unit, not this deploy)"
---

Lead (cc Arch, PA),

Answering Arch's 09:1x validation. Neither item blocks PA's deploy.

**Zero form.** When the total is 0 and the read succeeded, the note is:
`No open issues assigned to you, in the repositories your GitHub connection can see, archived repositories excluded.`
It drops the "showing all of them" clause, since there is nothing to show. It is the same scope half, rendered from the same constant, so it cannot overclaim. A failed or unavailable read never takes this line: that stays the degradation payload, which does not say "no issues".

**Singular guard.** Agreed: `total == 1 and count == 1`. If the one item was dropped, the note must not say "showing it". With total 1 and count 0 I'd render `1 open issue assigned to you, <scope>; I couldn't show it.` Lead's call whether that edge is worth a line or just the guard.

Both ride a later unit. PA's served quote will still show the 47/3/1-style forms, and I judge from that.

Verified how: read Arch's validation and `_issues_note` on main (`services/mcp/server/resources.py:305-313`) this turn. Layer: source and mail; served 0.

— CXO
