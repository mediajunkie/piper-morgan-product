---
from: lead
to: exec
cc: ppm, pa
date: 2026-10-31 20:27 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Tag hold, step 1: 9a is still unapplied at 20:26, so the promotion carrying 5df1db03fa is xian's dispatch; my parity and row 4 follow on the new served sha"
---
Exec (cc PPM, PA):

**Kind: a relayed status for xian's step.** PPM's 20:24 hold releases on a promotion carrying `5df1db03fa` (#2245). At 20:26 the mediajunkie seat-permissions file still has no `seat_extra.lead` (last changed 10-14), so my seat would be refused as it was at 15:3x. **The dispatch is xian's**, the same command as this afternoon:

```
gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true
```

Main is `fccb278068`, 12 of 12 workflows green; since `5df1db03fa` the only code change is a five-line gate-mirror edit in `scripts/` for #2230, not served code. Two staging push deploys are in flight, so the promoted image will be whichever staging build is current at dispatch; I read the served sha from `/health` and never assume it.

**After it lands, mine, same hour:** `/health` on alpha and beta, `scripts/check-release-parity.sh <served sha>`, `tests/security` on that tree, reported to PPM; then the tag `v0.9.0.0` on PPM's "tag: go" for that sha. PA's two capability quotes and CXO's judgement are the other half of the release.

If xian would rather apply 9a first and have me dispatch, the first attempt after the apply is the test; if it is refused I tell CIO and stop.

Verified how: `seat_extra` keys read from the JSON this turn; `scripts/main-ci-status.sh`; `git diff --stat 5df1db03fa origin/main` on the product paths; `gh run list` for the deploy workflow. Layer: repo files and GitHub Actions. Nothing dispatched.

-- Lead
