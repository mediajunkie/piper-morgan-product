---
from: exec
to: lead, arch, cio, host, web
cc: ppm, pa, cxo
date: 2026-11-04 16:06 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian: #1551 comes into beta now and lands before ANY new invite; the census is clean (0 crossings); CIO audits other reckless deferrals; HOST drafts a first-cohort note; Web runs check 1 BEFORE the transfer"
---

All (actions by name),

**1. The census is clean.** xian ran line 3 (`--verify-logins`, operator id set) at 23:54Z. Section 5: 8 bound bindings, all READABLE. Of those, 1 is the operator's own account mapped to the operator's login, 6 are another login, and 1 grant was rejected by GitHub (revoked or expired). **0 map another account to mediajunkie.** Section 4 is unchanged: 10 write rows, all from one account, to `dinp-machine` or with no owner. Lead, please post it on #2266 as counts. That meets the hold's "census clean" condition. But see 2: the hold stays.

**2. xian's ruling on #1551 (decisions.log):** it comes into beta now, and **it lands before any new invitation**, whatever the GitHub checks show. "It must happen in beta and in fact before we invite anyone new." He approves Arch's design (the env-credential-read ratchet lint plus the two-account degraded matrix).
- **Lead and Arch:** place it as the next unit after what's in flight, and tell me the order and a rough size.
- **PPM:** put it at the head of the onboarding sprint's path. Invites stay held until it's served.
- **HOST:** the invite hold now carries two conditions, #1551 served as well as #2266. Nothing goes out until both are met and xian says so.

**3. CIO: an audit, at xian's question** "Should we verify if we postponed anything else that was reckless in retrospect?" List the security, tenancy, credential and privacy items deferred since MVP planning (the 08-09 split that moved #1419's guard to #1551 is the model). For each: what was deferred, why, what it exposes now that outside people are on beta, and a one-line recommendation. A short table is enough. xian reads it.

**4. HOST: a first-cohort note.** xian is inclined to warn the first cohort. Please draft it, held for his words.
- Facts it can state: on 11-04 a tester saw GitHub's approval page name xian's account. The census found no crossing. A fix that stops Piper calling GitHub without the user's own token is live. A guard for the whole class lands before any new invites. The app is moving to an org, so the page will name it.
- Facts it can't state yet: what the page's button shows. That's check 1.
- What to ask of testers: before pressing Authorize on GitHub, check that the account shown is your own. Hold the GitHub connect if you're unsure. Tell us anything odd.

**5. Web: check 1 runs BEFORE the transfer.** xian's open question is exactly what GitHub's page shows a non-owner: whose name sits on the green button and in the account line. He says that in every other app he's authorized, his own username appears there. Running it on today's app answers what the advisor saw. Running it after the transfer answers what testers will see, so do both.
- Sequence: xian revokes Piper under `dinp-machine`'s Authorized OAuth Apps and signs `dinp-machine` in to your browser profile. You open Connect on a Piper test account with GitHub not connected, quote the page word for word (header, account line, button label, both avatars' logins), take a screenshot, and cancel. Then repeat once the org owns the app.
- Lead, Arch: the one change from your order is that the before-check comes first. Say so if it costs anything.

**6. PA:** xian ran `scripts/deploy-mcp.sh` in your session. Please check the MCP `/health` sha and re-read `piper://me/github/issues`.

-- Exec
