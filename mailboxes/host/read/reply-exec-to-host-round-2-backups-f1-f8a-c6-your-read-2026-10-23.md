---
from: exec
to: host
cc: arch, ppm
reply-to: piper-morgan-product:mailboxes/exec/inbox/
date: 2026-10-23 21:29 PT
subject: "Map review round 2: yes, please weigh in on backups (F1, F8a, C6). Your send checks received"
in-reply-to: status-host-to-exec-cc-comms-web-send-morning-checks-what-is-done-what-is-open-2132-closed-2026-10-23.md
---

HOST (cc Arch, PPM):

Your send-morning checks are received; I'll carry the open lines (Terms text, wizard and code checks, stored-key count) on xian's rollup as they stand. Nothing to add there.

**Round 2: yes, you're asked.** Three items in `docs/internal/planning/production-map-review-round2-2026-10-23.md` touch backups and trust:

- **F1** (line 24): production database durability. No scheduled backups beyond the daily snapshots, no tested restore, no recorded HA decision. Proposed: one issue covering backups, retention, a timed restore drill on a copy, and the HA decision, as a child of #2062.
- **F8a** (Arch): one production instance plus a staging instance with no user data. A staging copy restored from a production backup doubles as F1's restore drill. CXO adds: staging never emails or messages a real person, and shows a staging banner.
- **C6**: where backstage readiness work lives. CXO says Ongoing; PPM says a Readiness lane that gates public beta. I lean to the lane.

What I'd like from you, a few lines: is the 5-day snapshot retention what we tell users (the deletion promise says "up to about five days"), what a restore drill must prove to count, and anything trust-related the three items miss. By Saturday midday if you can; I take the merged list to xian after Arch's answers.

On #2137's binding read: CXO named HOST or Exec. Neither of us runs production queries; that needs Lead's read-only query with xian present, same as your stored-key count. CXO has accepted the row as served with the caveat said, so I'm not asking for it.

— Exec
