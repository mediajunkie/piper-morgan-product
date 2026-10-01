---
from: cxo
to: xian (ceo)
cc: ppm, lead, docs, comms
subject: "Your 'low urgency is risky' point, cashed within the hour: draining that audit found the tester onboarding doc pointing at a branch 7,614 commits stale and calling the live hosted app a future plan. Filed #1708, banner up, decision is yours."
date: 2026-08-31
---

PM — you said low-urgency labels can mean never, and that the rule is drain everything unblocked. I went
back through my standing-items file rather than just agreeing. **Four items; three had quietly resolved or
gone moot without me; the fourth turned up something live.**

## What draining actually found

`docs/ALPHA_QUICKSTART.md` — the **tester-facing onboarding doc**, which is a first-contact surface in
exactly the sense we've been using all week. Three load-bearing claims are false. Measured today, not
inferred:

1. 🔴 **It tells testers to clone `-b production`**, framing it as the safe branch and warning them off
   `main`. **`production` is 7,614 commits behind `main`, tip dated 2026-07-26**, and
   `.github/workflows/docker.yml` builds on `main` — **`production` is not a deploy source.** The advice
   is exactly backwards. (CLAUDE.md carries PA's 08-13 warning about this branch, when the gap was 4,195.
   It has roughly doubled since.)
2. 🔴 **It describes the hosted app as *"planned for 2026"* and says *"all paths require the developer
   setup."*** 📄 ESSENCE v1.0 — ratified law — names the live web-chat app with **~11 alpha testers** as
   the current surface. **The doc offers a 20–50 minute local build of five-week-old code as the only
   path.**
3. **Version header 0.8.11.0, last edited 2026-07-17.** Deployed is v63/v64.

## What I did, and the line I didn't cross

**Filed #1708** with the measurements, and **put an accuracy banner at the top of the doc** stating only
what I measured, so nobody follows the clone command meanwhile.

⚠️ **I did not change the instructions.** What it *should* say is a real decision — is local install still
a supported tester path, or is the hosted app the only one? Is `production` meant to be revived as a
release channel or retired? **That belongs with you, PPM and Lead alongside PPM's new
`release-model.md`**, not with me editing onboarding copy on my own read.

**Denominator, stated**: I checked those three claims. **The other ~450 lines are unaudited** and may hold
more drift. The banner says so.

## The honest part about how this sat

**The trail is not flattering and I'd rather you have it.** On 2026-07-12 I drafted a tester-facing
disclosure line for #1386's gate — *required before invites went out* if #1394 was still open — sent it to
Lead and PPM, and **it was never landed in any doc.** Nobody noticed for seven weeks. It stopped mattering
only because #1394 closed on 08-09. **That is luck, not process**, and it's the same file I've now found
three more falsehoods in.

⭐ **Your point is sharper than "things get forgotten."** Each of those items was individually reasonable
to defer. What made them invisible is that **"low urgency" reads as a decision, so nobody re-examines
it** — where "blocked on X" gets rechecked whenever X moves. **A label that terminates review is worse
than a backlog**, and I had one in my own file while telling other roles to name their triggers.

I've dropped the category from my standing items. Items are now either **unblocked (do now)** or
**blocked on a named thing (recheck when it moves)**.

— CXO
