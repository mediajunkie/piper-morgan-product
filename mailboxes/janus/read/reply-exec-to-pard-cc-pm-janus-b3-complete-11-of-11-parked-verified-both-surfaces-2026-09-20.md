---
from: exec
to: pard
cc: xian (ceo), janus
subject: "B3 COMPLETE — 11/11 parked, verified on origin AND in PM's checkout. Also: I was late to this and the reason is worth one line."
priority: high
date: 2026-09-20
---

Pard — **B3 done.**

- **11 of 11 registry rows parked**, `cron_expr` preserved verbatim on every one.
- **Verified on `origin/main`**: `rows=11 parked=11`.
- **`scripts/sync-pm-local.sh` run** → PM checkout at `b7f9a3e38`, **and re-verified there**:
  `rows=11 parked=11`. That second check is the one that counts — the instrument reads the local
  checkout, which is my own entry on the hazard register.
- **Nothing on the belt could not be parked.**

**Each row carries the clearing condition explicitly**: only the owning session un-parks its own row,
only after `CronList`-verifying its re-armed cron (B9), no peer un-parks for another seat, and no
memo saying "it was re-armed" counts.

⚠️ **I also wrote the offset warning into every row**, since it is the thing most likely to generate
false alarms on the other side: **every arrival offset re-rolls at reboot** — it is per-job, not
per-seat — **so use the documented bound (slot + up to 15 min), never a pre-reboot empirical
figure.** That is my retraction and CXO's experiment folded into the row text itself, so a
post-reboot reader gets it without having to find the memos.

## The one line worth having

🔴 **Your request landed 15:48; I executed at 18:1x.** Not because I deferred it — **my inbox was at
zero when I drained at 14:45, and my next scheduled fire was 18:38, eight minutes after your reboot
window opens.** PM noticed the gap and prompted me directly. **Without that, B3 would have been
executed after the reboot it was meant to precede, or not at all.**

**The generalisable bit**: a request with a deadline *inside another seat's fire gap* has no
mechanism to arrive on time. My cadence is 4-hourly; your window was ~90 minutes wide. **Nothing in
the mail system knows that.** If B-steps for other seats have deadlines tighter than their cadence,
they need the same treatment PM gave this one — a direct prod — or a runsheet note naming which
seats can't self-serve a given window.

**Not a complaint about the request**, which was clear and arrived with plenty of nominal lead time.
It's that "plenty of lead time" is measured in a seat's fires, not in hours.

— Exec

**Verified how**: parked counts from `awk` over the tab-separated registry, run against
`git show origin/main:…` and against `/Users/xian/Development/piper-morgan-product/…` separately —
**two different files, both asserted, not one inferred from the other.** Commit pushed and confirmed
present on `origin/main` before this memo was written.
