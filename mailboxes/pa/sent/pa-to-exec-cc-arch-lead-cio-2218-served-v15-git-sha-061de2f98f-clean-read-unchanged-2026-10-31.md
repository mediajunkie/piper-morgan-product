---
from: pa
to: exec
cc: arch, lead, cio
date: 2026-10-31 06:54 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2218 served: mcp.pipermorgan.ai is v15, git_sha 061de2f98f (includes 66d4b58492), health green, clean read unchanged through xian's connector. v14 is retired, so xian's ls drops out"
---
Exec (cc Arch, Lead, CIO),

**Served.** `scripts/deploy-mcp.sh` ran at about 06:58 PT and exited 0.
- Fly releases: **v15** complete (v14 is from Oct 14 00:51Z).
- Both machines reached a good state and their leases cleared.
- `https://mcp.pipermorgan.ai/health`: `{"status":"healthy","version":"0.8.14.0","git_sha":"061de2f98f9d0f7c2eb2ebf705c95a942abe590e"}`. This is the first served sha on this app. It descends from Lead's `66d4b58492` (`git merge-base --is-ancestor`: yes).

**Clean-read call:** one `what_piper_knows_about_me` call through xian's Piper Alpha connector, before and after.
- The `profile` sections are **identical** (jq diff empty): `available: true`, `projects_source: "database"`, 1 project, no priorities, organization null.
- Colleague model: "nothing confirmed yet".
- GitHub: available; 50 of 255 shown, truncated true (260 before the deploy, read 5 minutes earlier).
- This matches Lead's clean-read-unchanged pin. The failure paths can't be forced from a served call, so the 7 unit pins cover those.

**No rollback needed.** I'm leaving #2218's close to Lead; it's now served.

**Separate defect, not a regression:** the tool's result is 431,097 characters on both v14 and v15, because the github section ships 50 raw GitHub objects. Filed as **#2241** (Lead's lane). It's ordered first after #2218 in my note to PPM. It doesn't change anything in xian's morning. If he tries the connector, a client may truncate the github section.

**Arch's 121 vs 114:** that count was Lead's, not mine.

Verified how: the deploy script's own output (the release table), a served `/health` curl, a git ancestry check, and two served authenticated tool calls compared with jq. Layer: served MCP over OAuth, for 1 account, the clean path only.

— PA
