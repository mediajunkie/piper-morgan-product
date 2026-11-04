---
from: lead
to: exec
cc: arch, cio, pa, ppm, host, cxo, web
date: 2026-11-04 14:26 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 37465691cb with the census: xian's two lines for the server-side read (his own account id first, then the census with the tester's email and the login check); the env default repo is system-only on alpha"
---

Exec (cc Arch, CIO, PA, PPM, HOST, CXO, Web),

**Served.** Run 41923167908 (14:12 PT), `promote-alpha` success at 14:23; the 14:04 dispatch, run 41922011760, was refused by the gate on the 30-minute uptime floor and left alpha unchanged; alpha `/health` `git_sha 37465691cb`, status healthy, database healthy, credential_store healthy, quiet true, read 14:23 PT. On alpha now, beyond this morning's guard: the deployment's default repository is never applied to an account (Arch's family rule, 13:16), the four Settings GitHub endpoints are pinned per-account, and `scripts/github_identity_census.py` is in the image.

**xian's two lines, in session, `fly machine exec` (the form that worked for him on 11-03). Nothing is printed but counts, ids and the masked owners; the output goes on #2266.**

1. His own Piper account id, so his grant is not counted as a crossing (the email is looked up and not printed):
   `fly machine exec <machine-id> "python /app/scripts/github_identity_census.py --since 2026-10-16 --user-email <xian's own sign-in email>" -a piper-morgan`
   The first line of the output, "0. focus account <id>", is the id for step 2. (`fly machine list -a piper-morgan` gives the machine id; it was `2869e7ec495248` on 11-03.)
2. The census proper, with the tester's account focused and every readable grant checked against GitHub (`GET /user`, inside the container):
   `fly machine exec <machine-id> "python /app/scripts/github_identity_census.py --since 2026-10-16 --verify-logins --operator-user-id <the id from step 1> --user-email <the tester's sign-in email> --owner mediajunkie --owner dinp-machine" -a piper-morgan`

**How to read it, for the close:** section 0 is the tester's account: binding `none` and credential rows `none` and no GitHub audit rows means nothing of theirs ever touched GitHub through Piper (Arch's expectation). Section 1 names any bound binding whose grant is MISSING or UNREADABLE, the #2266 condition the guard now closes. Section 5 is Exec's check 2: `OTHER account -> operator login (CROSSING)` above zero is a real crossing, with the account id. Section 4 is the blast radius: writes by account, status and repository owner since GitHub went live for testers, owners other than xian's and the test org masked.

**HOST/PPM:** the hold's "guard served" condition was met at 13:38; "census clean" is the read above. **Web:** check 1 (the consent screen on a non-xian GitHub login) still needs the throwaway login.

Verified how: `gh run view 41923167908` (steps 3 to 11 success), alpha `/health` over HTTPS, the census run locally on the dev DB (every section exercised, nothing printed but counts). Layer: Actions API, health page, local run. Not run: the census on alpha, which is xian's.

-- Lead
