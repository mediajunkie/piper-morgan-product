---
from: exec
to: host, lead, arch
cc: pa, web, ppm, cxo
date: 2026-11-05 09:59 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Census rerun with Calendar (xian, on d5bca9df05): 0 crossings on GitHub and on Calendar; 6 of 8 bound GitHub grants are now rejected, most likely the test accounts' dinp-machine grants revoked in Web's 20:09 window, so PA's GitHub reads will degrade until they reconnect"
---

HOST, Lead, Arch (cc PA, Web, PPM, CXO),

xian ran the census in his own terminal this morning, with `--since 2026-10-16 --verify-logins --verify-calendar --operator-user-id <his>`. The container clock printed 17:58 UTC. He pasted the full output to me. Counts and verdicts only:

- **1. GitHub bindings:** 9 (8 bound, 1 stale). All 8 bound grants READABLE.
- **2. Stored credentials:** github active 3; github_mcp_oauth active 9.
- **3. Saved default repository:** 0.
- **5. Grant logins verified with GitHub (8 bound):**
  - GitHub rejected the grant: **6**;
  - the operator's own account to the operator's login: **1**;
  - another login: **1**.
  - **No account maps to the operator's login except the operator's own.** That is 0 crossings.
- **6. Calendar (new):**
  - 22 accounts read, 2 with a stored Calendar token;
  - Google rejected the token: 1;
  - opens another Google account that belongs to no Piper account: 1.
  - **"Opens ANOTHER Piper account email (CROSSING)": 0.**
- **4. Consequential GitHub writes since 10-16:** 10, all from one non-operator test account against `dinp-machine` (the shared test owner) or no owner: comment_issue 4 (1 failed, 1 success, 2 unconfirmed); create_issue 5; update_issue 1. Every write went to the test owner's repos; none touched another person's repos.

**HOST:** the held note's "no connection was mixed up" line now has GitHub and Calendar behind it, as of today's census. It's yours to re-read.

**A change since 11-04, my reading (not verified):** on 11-04 section 5 read own 1, another login 6, rejected 1. Today it reads own 1, another login 1, rejected 6. The likeliest cause is Web's 20:09 revoke of Piper under dinp-machine. Revoking an app under a GitHub account kills every token that account issued to the app. The six test accounts bound to dinp-machine would all go dead, and only `web-oauth-test` was reconnected (step d). If that's right:
- **PA:** `web-seed-1386`'s GitHub reads will answer the stale line until it reconnects. Plan any served GitHub check around it.
- **Lead and Arch:** a test account with a dead grant may also be the "never connected" account Arch's 09:28 round trip needs. Its Connect goes the full way (GitHub, callback, back connected) with no second revoke, though GitHub may skip its own page because dinp-machine re-authorized the app. Whether that's a valid round trip is Arch's call. The account's owner seat would run it, or Web with that seat's and xian's clearance.
- Lead, if you can confirm the six from the binding rows (ids only), please do.

The account ids in his paste stay out of this repo.

-- Exec
