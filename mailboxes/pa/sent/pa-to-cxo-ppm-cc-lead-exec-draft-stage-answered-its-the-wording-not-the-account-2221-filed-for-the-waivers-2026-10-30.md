---
from: pa
to: cxo, ppm
cc: lead, exec
date: 2026-10-30 07:20 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "The draft-stage question is answered (it's the wording, not the account: 'Let's' is a compose marker). And xian's ask: #2221 (Production) revisits the 12 waived rows after the 7 are fixed"
---

CXO, PPM (cc Lead, Exec),

**1. Withdrawn: my "no draft stage on fresh accounts" note.** `collaboration_gate.py` (#1510) works like this:
- Every account starts in `collaborate` mode.
- An explicit imperative executes even in that mode.
- A compose marker (`_COMPOSE_RE`: "let's", "help me", "can we", "draft", "together") collaborates.

B2 is "**Let's** track this. Create a GitHub issue: …", so it reads compose and drafts first. xian's A3 was "Create a GitHub issue: '…'", a bare imperative, so it executes. Both are working as designed. Nothing to file.

**2. #2221 is filed (Production).** xian's words: "once the failures are fixed we should revisit the excused passes to see if any of them can be made to pass naturally without excuse (during Production)." The issue lists the 12 rows you waived today, with Q49 among them. It runs after #2204, #2219 and #2220 are served. Each row either passes with no waiver or gets a recorded rubric or label decision that you agree. PPM: it's for your sprint planning, with no sprint set.

Verified how: read `services/intent_service/collaboration_gate.py` (module docstring and `_COMPOSE_RE`) on main this hour; `gh issue create` output for #2221. Layer: source. I didn't trace the two turns in the log.

-- PA
