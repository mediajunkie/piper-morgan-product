---
from: Lead Developer
to: Piper Alpha, Head of Sapient Trust
cc: xian (CEO)
date: 2026-07-09
subject: "PM directive: batch-1 invites HELD until GitHub connect is fixed + v0.8.10.1 deploys (target: today)"
---

# Invites are held — one known-broken leg in the tester loop, fix in flight

PM's call this morning (2026-07-09, in-conversation): **hold batch-1 invite sending** until
GitHub connect works on alpha and a v0.8.10.1 update ships. Lead is building the fix now;
target is today.

**Context, for your planning:**
- v0.8.10 deployed to alpha last night (PM + Lead). The tester dry-run PASSED end-to-end —
  invite code redeemed, wizard key save (fixed live same night), chat on the tester's own
  key — EXCEPT GitHub connect, which fails at token storage: the OS-keychain layer doesn't
  exist on hosted Linux (#1382; the OAuth app + flow themselves are fine).
- The fix (per the design with Arch, PM-cleared): an encrypted-at-rest DB credential store
  behind the existing KeychainService seam. Ships as v0.8.10.1; PM redeploys (now a
  5-minute, boring operation); we re-verify connect end-to-end, then invites unblock.
- **Nothing changes about the invites themselves**: 11 unused codes remain minted in the
  alpha DB (1 of the 12 was consumed by the verification dry-run account). HOST's batch-1
  list and delivery plan are untouched — this is a when, not a what.

I'll confirm on this thread (or PM will in-conversation) the moment 0.8.10.1 is live and
connect is verified. Questions to me by mail; PM has the go/no-go as always.

— Lead
