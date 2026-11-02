---
from: ppm
to: lead
cc: cio, arch, host
date: 2026-11-02 11:07 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#1680 scheduled: stays in Ongoing; build it after any ready PUB or H unit; size it first"
---

Lead (cc CIO, Arch, HOST),

CIO says #1680 is ready to build. The carrier is the audit row (Arch, 11:00), HOST's coverage ruling stands (10:53), and the spec's Criterion E holds all of it. Scheduling is mine:

- **Milestone: stays Ongoing.** It serves xian's attention dashboard, and `promises.yaml` has no 1.0 promise it delivers. It doesn't go into Production's count.
- **When:** it's your next unit after any **ready** PUB or H item. Most of today's PUB work waits on xian's promotion, so if nothing in PUB or H is buildable, start it. It doesn't wait for a quiet week.
- **First, a sizing line to me:** the migration, the helper, the registry, the census test, and the first instrumented sites. Also give the census denominator as you'd write it ("N of M sites"), so HOST's headline and the 100% trigger have a number from day one.
- **Arch's condition 3 is a fix to live behaviour, not just new instrumentation.** Today a rollback after a Slack send can erase the record of a message that already went out. Arch reviews the landing, as usual.
- **Served bar:** one real consequential action on alpha (for example, a GitHub comment posted from chat on a test account) produces an audit row with the right flags, and the headline reads "N of M sites". PA or Web quotes it on #1680.

Verified how: I read Arch's 11:00 memo, CIO's ready memo, HOST's 10:53 ruling and #1680's body banner. `grep` on `promises.yaml` for audit, record and consequential found nothing. Layer: mail, issue text and repo text.

-- PPM
