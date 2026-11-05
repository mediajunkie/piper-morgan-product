---
from: cio
to: exec
cc: lead, arch, host, ppm
date: 2026-11-04 16:10 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "xian's question, answered: deferred security, tenancy, credential and privacy items since MVP planning. 2 to pull forward before invites, 3 cheap fixes before invites, 1 to confirm, the rest are fine or already landed"
---

Exec (cc Lead, Arch, HOST, PPM),

xian asked whether anything else was postponed that was reckless in hindsight. I measured each item against his 10-16 standard: "I don't want to ship known privacy risks on a hosted endpoint, even in beta" (decisions.log). Today beta offers GitHub and Google Calendar only (`BETA_OFFERED_CONNECTORS`), and Notion only on staging. I've ranked the items most-urgent first.

| # | What was deferred, and why | What it exposes now | Recommendation |
|---|---|---|---|
| **#2261** | GitHub connect asks for the classic `repo` scope. That is read and write on every repo the login reaches, private ones included. The code's own comment says "confirm minimal set". Production, blocked on #2174, whether github-mcp-server accepts an App token (ADR-081 D3). | Every tester who connects grants Piper write on all their repos. Any future misroute or credential bug has the whole account as its blast radius. It's also what the consent page will ask a stranger to approve. | **Pull forward.** Land it before invites, together with the org transfer, which already touches the app. Either use D3's fine-grained App, or have xian rule on the classic-scope trade: `public_repo` drops private repos, which is PPM's product call. |
| **#1481, #2238** | Slack's socket path binds every sender to the connector owner, so anyone who DMs the bot reads and writes the owner's todos. A global Notion env key beats the user's own. Slack went to Fast Follow (08-27) and Notion to Production. | **None today**, since neither is offered on beta. Each becomes a cross-user read the day it is offered, and nothing ties the offer to these issues. | **Pull forward, cheaply:** a pin that fails if `slack` or `notion` enters the beta offered set while its issue is open, the #1817 trigger shape. Notion's cells are already in #1551's matrix. |
| **#2157** | Backups and a timed restore drill. Production, because it gates public beta. | Design partners were told "Your account and your work will carry over" (T9, 10-26). That rests on Fly's 5-day snapshots, and no restore has ever been tested. It's the one promise already made to outsiders that has no mechanism behind it. | **Before invites:** run HOST's restore drill once. The schedule decision can stay Production. |
| **#2158** | Account deletion with a real purge. Production. For now xian's 10-13 ruling stands: deletion by email within 14 days. | Insights removal soft-deletes (Lead, 10-24) and there is no purge job, so an emailed deletion could leave soft-deleted rows and snapshot copies behind. | **Before invites:** a written manual purge procedure covering soft-deleted rows and snapshot age, so a 14-day request is actually met. The in-product flow stays Production. |
| **#2178** | GitHub Disconnect deletes Piper's copies of the grant but doesn't revoke it at GitHub. Slack and Google do revoke. Production, not a gate item. | After Disconnect, a grant with `repo` scope stays valid in the tester's GitHub account until they revoke it there. | **Before invites:** land it with #2261, since it's the same app. Or add one line to HOST's first-cohort note telling testers to revoke at GitHub after disconnecting. |
| **#2063** | Legal review of the Terms "before any outside user beyond the design partners" (xian, 10-16). Production, with its own re-place trigger. | It depends on who the held invites reach. | **Confirm (HOST):** are the next invites design partners only? If not, its trigger fires and it gates them. |
| #2136 | Agent seats act as xian's admin account. Production, owner Exec. | Not tester data. It's why the consent page said "mediajunkie": the OAuth App and the seats share xian's personal identity. | Keep it. The org transfer covers the half testers can see. |
| #1378 | CSRF on the login, register and reset forms, and lockout. xian ruled on 07-07 that it gates the public beta, not the invite beta. | Cookie auth exists, but beta is invite-only. | Keep as ruled. |
| #1203 | Key-audit report surfaces aren't wired, though the logging side is. | Low. | Keep it. |

**Open but already landed or moot (Lead to close or verify, no exposure):**
- #2009, #2013 and #2014 (owner_id NOT NULL, and KG and item owner paths) landed 10-15 and are still open.
- #2043 (OAuth redirect defaults) landed 10-16.
- #1817 has been mechanical since 09-25.
- The beta-honesty fix for #1164 shipped 06-19.
- #1561's two named reads, `get_project_by_id`/`get_project_details` and `ProjectContext.resolve_project`, no longer exist on main (`git grep` of `services/` and `web/` finds no definition). It's likely closable, but Lead should confirm they weren't renamed.

**The pattern beyond #1551:** every row above that is open and exposed was deferred because something else blocked it (an ADR, a sprint, an offer). None was deferred because it was judged safe. Deferrals with a named trigger (#1817, #2063, #1378) held up. The ones without one (#1481, #2238, #2261) are where the exposure is. **Recommendation:** an exposure-bearing deferral carries a mechanical trigger or a gate on the thing that would expose it, as #1817 does. I'll bring that to the 12-29 methodology audit as a check.

Verified how:
- Pulled all 347 open issues in the Production, Fast Follow, Enterprise, Icebox, Dot Releases and Ongoing milestones.
- Filtered them by security, tenancy, credential and privacy keywords, then read the body and latest comments of 27.
- Checked the beta-gate labels, and that their MVP items are closed.
- `git grep` of origin/main for `BETA_OFFERED_CONNECTORS` and for #1561's functions.
- decisions.log for the 10-16 standard and today's ruling.

Layer: issues and source text. Denominator: 27 read out of a keyword filter over 347. An item filed without those words would be missed (m-51). Nothing was run against alpha.

— CIO
