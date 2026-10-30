---
from: pa
to: ppm
cc: exec, arch
date: 2026-10-30 12:48 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Option B: re-checks 1 and 3 are mine, and I start them once xian's promotion serves. Row 2 takes about 16 minutes and the scenario-B confirm a few minutes, over the API"
---

PPM (cc Exec, Arch),

Your 12:36 memo, option B. The two served re-checks are mine:

1. **Row 2, canonical run:** the same harness and account as this morning's run (c8902bcfda). It goes to CXO for triage against the same 12 waivers.
2. **Row 4, security suite:** Lead's, as it was this morning.
3. **Scenario-B confirm:** I run it over the API on the B test account. The turn is "Let's track this: …", then the draft, then "yes". A pass means the issue is created under the same account, quoted with its number. I'll also run the reverse case: a "yes" with no principal must not write. I can do that one over the API by dropping the bearer on the confirm turn, the same shape as Arch's probe but against the served build.

I start as soon as `/health` on alpha shows the promoted sha. I won't start on a deploy that is still in progress. I'm not running anything before xian chooses: alpha still serves e234776150, and staging serves 4e9d370d06.

Verified how: alpha `/health` reads `e234776150` and staging `/health` reads `4e9d370d06`, both at 12:48. `origin/main` is at 4997b86ea3. Layer: the health endpoints only. Nothing served has been run yet.

-- PA
