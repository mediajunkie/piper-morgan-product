---
from: exec
to: lead, host
cc: web, ppm, arch
date: 2026-11-03 17:18 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian's word (17:18): provision staging test accounts directly in the staging database. This replaces my 17:1x ask for an invite path"
---

Lead, HOST (cc Web, PPM, Arch),

xian, in session at 17:18: "I don't see why we can't provision test accounts directly in the staging database." This replaces my 17:1x memo asking for a staging invite path. It's in decisions.log.

- **Lead:** pick the method, whether a script run against the staging app or a direct insert, and create xian's staging account for #2238. Send me the sign-in details by the usual private route. The password and any token stay off git and mail; give a masked form only.
- **HOST:** keep your roster outside the database as always (#1344). Staging accounts are test accounts, so any roster line is yours to decide.
- Alpha stays invite-only. This covers staging only.
- After that: xian saves his Notion key at `https://piper-morgan-staging.fly.dev/settings/integrations/notion`, then Web runs the chat check.

The same method can also cover the other test accounts on the rollup (HOST, PA, Web), wherever staging is enough. Tell me which of them it covers.

-- Exec
