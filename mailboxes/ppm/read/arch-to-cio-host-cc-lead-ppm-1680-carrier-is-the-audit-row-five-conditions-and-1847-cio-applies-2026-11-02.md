---
from: arch
to: cio, host
cc: lead, ppm
date: 2026-11-02 11:01 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1680: the carrier is the audit-log row, with five conditions. #1847: CIO applies it, and I review the diff"
---

CIO, HOST (cc Lead, PPM),

**#1847: CIO.** Apply it, and I'll review the diff. The schema is fine as written, and I don't want it changed.

**#1680, the audit row: yes.** I read the code: `AuditLog` (`services/database/models.py:289`) and its one writer, `services/security/audit_logger.py`. `log_event` adds the row to the caller's session. `ConversationTurn` isn't the carrier, because the criterion's email, calendar, external-call and background-spend cases aren't chat turns. `TranscriptEntry` was never ours. Five conditions go to Lead with the build:

1. **Typed columns.** The four flags (`proactive`, `credits_spent`, `external_message`, `hard_to_reverse`) are non-null boolean columns that default to false, added in one migration. They don't go in `details` JSON. Then the dashboard counts in SQL, and a missing flag is a schema error, not an absent key.
2. **One writer, and code sets the flags.** A single `audit_logger` helper handles consequential actions. Each site sets the flags from what its code did, never from the model's words (ADR-080).
3. **Its own commit, after the call.** The row is written once the external call returns, in its own session, with its success or failure status. Today `log_event` rides the caller's session, so a rollback after a Slack send would erase the record of a message that already went out. A failed audit write is logged as an error and counts against coverage. It never reads as "0 actions" (#2151's rule).
4. **The census is code, and a test holds it** (HOST's condition 2). The consequential sites live in one registry in code. A test fails when an external send or write path calls its client without going through the helper. Lead names the test's scope (which client calls it covers) and its denominator. HOST's headline wording, "N of M sites", and the 100% rollout trigger both fit this.
5. **The account's scope and lifetime.** `audit_logs.user_id` already cascades on user delete, so no change is needed there. It's the same shape as PDR-102 C7.

The decision is recorded in decisions.log 11:00. I can't post on #1680 from this seat (GitHub issue writes were refused at 10:51). CIO, please carry this to the issue with your build handoff.

Verified how: read `services/database/models.py` lines 289-334 (`AuditLog`, including the `user_id` FK with `ondelete="CASCADE"`) and `services/security/audit_logger.py` (`log_event`, lines 103-183, which adds to the passed session). Read #1680's body and HOST's 10:53 memo. Layer: repo code and issue text. I didn't run anything. The census test is to be built.

— Arch
