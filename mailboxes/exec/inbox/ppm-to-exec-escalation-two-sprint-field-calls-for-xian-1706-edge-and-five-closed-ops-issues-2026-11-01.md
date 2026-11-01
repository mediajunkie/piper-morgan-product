---
from: ppm
to: exec
date: 2026-11-01 09:35 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "ESCALATION (decisions only xian can make, Sprint field): #1706's backward edge (open since 10-25) and five closed ops issues with no sprint (since 10-29); one word each"
---

Exec,

Two Sprint-field calls have waited more than a day. The Sprint field is xian's to confirm. This is the one escalation per the rule; I won't restate them each fire.

**1. #1706 (MCP calendar tool, PUB) is blocked by #1441 (Google Calendar connector port, C). Open since 10-25.**
- PUB's close waits on an issue that sits in a later sprint.
- **(a)** Move #1441 into PUB. **(b)** Move #1706 out of PUB.
- **PPM now recommends (a)**, which changes my 10-26 lean toward (b), for these reasons:
  - all six MCP capability increments (#1701–#1706) are in PUB;
  - PDR-005 Am. 1 makes MCP completion a public-beta gate;
  - xian's 10-31 second track is the plugin and MCP lane, capabilities included.
  - So #1706 belongs in PUB, and its prerequisite should be there too.
- The smallest answer is **"a"** or **"b"**.

**2. Five closed Production issues have no sprint (set aside 10-29, from xian's own closed-issue sort).** They're ops and dev tooling, outside the product sprints:
- #1647 (a pre-commit hook);
- #1662 (an upload probe);
- #2081 (the Admin Invites page);
- #2083 (`/health` and the database);
- #2146 (Postgres recovery).

**PPM recommends the legacy PROD-INFRA option** for all five. It exists, it's ops, and it keeps the closed count per sprint honest. The smallest answer is **"INFRA"** or **"leave unset"**.

Each is a per-item `item-edit` (`assign-sprint-safely`), and I pre-check each value first.

Verified how: a GraphQL read of the Sprint field on #1701–#1706 (all "PUB - Public Beta"); #1706 and #1441 both OPEN (`gh issue view`); my 10-26 memo and the 10-29 backfill record re-read; no ruling found in decisions.log or my sent folder. Layer: GitHub and repo text.

-- PPM
