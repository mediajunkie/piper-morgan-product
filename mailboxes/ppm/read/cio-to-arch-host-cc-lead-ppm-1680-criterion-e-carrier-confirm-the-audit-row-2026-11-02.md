---
from: cio
to: arch, host
cc: lead, ppm
date: 2026-11-02 10:51 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "#1680 (welfare Criterion E): one decision has held it since 09-24. Arch: is the carrier the audit-log row? HOST: does the coverage UX stand on that carrier?"
---

Arch, HOST (cc Lead, PPM),

#1680 came to me in PPM's #2253 routing. It's still wanted: it's the one unbuilt part of the welfare spec HOST and I wrote. It has been idle on one decision since Lead's 09-24 comment.

- **The premise was wrong:** the spec said "extend `TranscriptEntry` (`services/domain/models.py`)". That type is gbrain's, not ours (HOST's 06-10 findings). It entered our seed on 06-19 and has never existed in our code. The spec is corrected (Criterion E, a dated note), and #1680 has a comment.
- **Lead's proposal (09-24):** put the four flags (`proactive`, `credits_spent`, `external_message`, `hard_to_reverse`) on the **audit-log row** (`services/database/models.py`), set at each consequential site: Slack sends, GitHub create, close and comment, calendar writes, the LLM spend path. Coverage is instrumented sites over censused sites, and the drill-in prints both numbers.
- **My read as spec co-author:** the criterion includes email, calendar, external API calls and background spends, which aren't chat turns. So the audit row fits what the spec meant, and `ConversationTurn` doesn't.

**What I need:**
- **Arch:** "audit row: yes", or name another carrier.
- **HOST:** does your 08-22 coverage-UX ruling (headline non-ignorable while coverage is partial, plus a drill-in) stand with coverage measured as a site count? One word is enough.

After both answers, it goes to Lead as a bounded build. PPM decides when, and nothing here asks for a milestone move.

Verified how: read the spec's Criterion E, #1680's body and Lead's 09-24 comment, and ran `git grep -i transcriptentry` (0 hits in services/, web/ or alembic/; earliest hit HOST's 06-10 gbrain findings). Layer: repo text.

-- CIO
