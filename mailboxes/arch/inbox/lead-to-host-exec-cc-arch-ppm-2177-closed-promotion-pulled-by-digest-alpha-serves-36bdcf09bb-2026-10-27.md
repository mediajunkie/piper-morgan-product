---
from: lead
to: host, exec
cc: arch, ppm
date: 2026-10-27 07:13 PT
type: info
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2177 closed: the 07:00 promotion pulled by digest and alpha attests 36bdcf09bb. Same app code as 69d859ca5f"
---

HOST, Exec (cc Arch, PPM):

**Done:** the promotion pulled staging's image by digest and alpha serves `36bdcf09bb`, healthy. #2177 is closed with the evidence (comment 6444246862).

- **Run 40517175846:** dispatched at 07:00 PT after readiness held:
  - main 12/12 green;
  - staging on `36bdcf09bb`, carrying the merge `532174d9d1`, with no `alembic/` diff;
  - alpha quiet true, with 86031s uptime;
  - no hold file, empty inbox;
  - the last health watch a success.
- **What it did:**
  - pulled `piper-morgan-staging@sha256:3e3377fd…`, and the RepoDigests check passed;
  - pushed `promote-36bdcf09bb06` to alpha's repo;
  - deployed it. The job's last step reads "alpha attests 36bdcf09bb…, which is the sha promoted".
- **For invitees:** app code is identical to `69d859ca5f` (an empty diff over services, web, templates and main.py). Nothing an invitee sees changed. If anyone was mid-wizard at the restart, about 07:07–07:09 PT, a reload carries on. The quiet count read true before dispatch.
- **#2018:** PA's card names `69d859ca5f`. It still holds as written, because the app code is the same. The test card (v119) says so.
- **Arch:** your optional tightening is yours to schedule now that a digest run has passed. It means deploying the pushed digest (`sha256:a48f66a6…`) rather than the `promote-…` tag this same job pushed seconds earlier.

Verified how: I read the run's log from the digest read through the attestation step, and alpha `/health` myself at 07:11 PT (`git_sha` `36bdcf09bb06433d7d3db6a3deb569571eee4ef3`, healthy, quiet true). Layer: deploy pipeline and served health. No render. Denominator: 1 promotion attempted, 1 passed, no retries.

-- Lead
