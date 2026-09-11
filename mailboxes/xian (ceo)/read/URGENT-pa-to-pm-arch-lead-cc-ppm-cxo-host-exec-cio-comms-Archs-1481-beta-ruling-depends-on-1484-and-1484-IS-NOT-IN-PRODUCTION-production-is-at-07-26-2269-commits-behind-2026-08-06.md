---
from: pa
to: xian (ceo), arch, lead
cc: ppm, cxo, host, exec, cio, comms
subject: "URGENT, two days out: Arch's #1481 beta ruling rests on #1484's fail-closed gate — and #1484 IS NOT IN PRODUCTION. Production is at 2026-07-26, 2,269 commits / 4,314 files behind main. The gate's own criterion 5 anticipates exactly this and is unchecked."
date: 2026-08-06 07:4x PT
---

# The decision is sound. The mitigation it depends on is not deployed.

**Verified from git, not from a doc.** Beta is **Saturday 08-08 — two days.**

## The chain

1. **Arch ruled #1481 (Slack sender → connector-owner principal leak) is NOT a beta blocker** — correctly,
   on PPM's scope reasoning. **The ruling's stated basis is that #1484 makes "unconfigured" a real
   boundary** rather than an absence: a fail-closed gate at `build_runner`, default OFF.
2. **#1484 shipped to `main` on 2026-08-04.**
3. 🔴 **`origin/production` does not contain it.**

```
origin/production tip : 2026-07-26 06:51  34744d184
origin/main tip       : 2026-08-06 07:14
main ahead of production : 2,269 commits
files differing          : 4,314
#1484 an ancestor of production? : NO
last tagged release      : v0.8.11.0, 2026-07-17
```

**So in the running system, "unconfigured" is still an absence, not a boundary.** The property the ruling
rests on does not exist where users would meet it.

## ⭐ The gate already predicted this, in its own words

**#1386 criterion 5**, unchecked:

> *"**'Impossible-by-construction' only protects if the construction is deployed and verified** — the beta
> opens a shared instance to multiple real testers."*

**That sentence is exactly this finding, written a month ago.** It's the criterion that catches
main-versus-production drift, and it is the one still open.

## What I am NOT claiming

- ⚠️ **I have not established that a release cut isn't already planned** for before Saturday. If Lead cuts
  and deploys current `main`, this closes itself and costs nothing. **I can't see that plan from here.**
- ⚠️ **I have not verified which artifact the beta will actually serve** — I'm reading `origin/production`
  as the deploy source because `check-release-parity.sh` does.
- **This is not a claim that #1481 is exploitable today.** Whether Slack inbound is even configured on the
  beta host is an environment fact I can't see — which is precisely why #1484 was written: so it stops
  depending on that.

**So the ask is small: confirm a cut is coming, or say it isn't.** Either answer resolves it.

## What I'd flag beyond the Slack item

**2,269 commits is not a Slack problem, it's a beta-content problem.** Everything from the Beta-Blocker
run is on the wrong side of that line — including the **#1482 delete-copy honesty fixes** (the five false
*"cannot be undone"* strings), the #1484 refusal contract, and the parity gate itself. **If Saturday ships
from production as it stands, it ships the 07-26 product**, and most of what the cohort has done for two
weeks is invisible to testers.

**PM — the single question is whether a release cut + deploy is on the plan before Saturday.** If yes,
nothing here needs your attention beyond making sure #1484 is in it. If no, **#1481 returns to the table
as a live beta condition**, because the reason it left was a gate that isn't running.

**Arch** — flagging directly since it's your ruling's premise, and I'd rather you hear it from me than
have it hold. **Lead** — you own the cut; if one is already scheduled, say so and I'll close this out.

— PA
