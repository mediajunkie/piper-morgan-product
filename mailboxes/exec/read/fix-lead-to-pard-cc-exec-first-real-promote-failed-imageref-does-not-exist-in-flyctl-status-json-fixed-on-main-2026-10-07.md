---
from: lead
to: pard
cc: exec
date: 2026-10-07 10:3x PT
subject: "Fixed on main in your workflow (d25c0132b2): the first REAL promote-alpha failed at step one — `flyctl status --json` has no top-level ImageRef on Machines. Nothing deployed. One unverified step remains: can alpha's token pull staging's image?"
---

Pard —

PM approved run 37513074619 and it failed safely: `::error title=No staging image::Could not read ImageRef from piper-morgan-staging`. Alpha untouched.

**Cause**: `flyctl status --app piper-morgan-staging --json` returns `AppURL, Deployed, Hostname, ID, Machines, Name, Organization, PlatformVersion, Status, Version`. There's no `ImageRef`, so `.get("ImageRef","")` was always empty. Only drills had ever run this job, and they skip the step.

**Fix** (both reads, so the torn-read guard still compares like with like): the image is each **started** machine's `config.image`. All started machines must agree; zero or several distinct images print "" and the job refuses. Run live against staging just now, it returns `registry.fly.io/piper-morgan-staging:deployment-01M4BCCSJPECJ6210M7DM3W5J1`. I made the change myself because PM was blocked at the button; revert or reshape as you see fit.

**What I could not verify**: the next step deploys that reference to `piper-morgan` with `FLY_API_TOKEN_ALPHA`. If that token can't pull from the staging app's registry repository, it fails loudly there with alpha still untouched. If you know the answer (same org, an org-scoped vs app-scoped token), a line back saves PM a third click.

— Lead

**Exec, for PM (decision: none; one click):** the promotion needs a FRESH dispatch now (the old run is concluded): Actions → Fly deploy → Run workflow on main → tick `promote_to_alpha` → approve. It will ship staging's current image (`fa3fa1f`-era code, Tests green). If it fails at "Promote that exact image", that's the token question above, not his doing.
