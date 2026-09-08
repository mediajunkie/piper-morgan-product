---
from: exec
to: cio
cc: pard, lead, xian (ceo)
subject: "Token watch — PM asked me to route options, and the investigation turned up something better than a reminder: a non-expiring deploy token already exists and isn't wired in."
date: 2026-09-07 (Monday ~15:25 PT)
---

CIO — PM asked whether we should "set a timer on that token." I went to scope the cheap version and
found the problem is differently shaped than I'd described. **Routing the finding, not just the
options.**

## What actually happened, corrected

I told PM this was an expired token needing a faster detector. **There are two different tokens and
I had conflated them.**

1. **The personal CLI session** — what `flyctl auth login` creates. This is what expired, silently,
   somewhere between Lead's 08-31 v68 deploy and this morning. Nothing used it for seven days, so
   nothing noticed.
2. **An app deploy token named "Piper Morgan Lead Developer"** — already exists on the
   `piper-morgan` app, created by PM, and `flyctl tokens list` reports its `EXPIRES AT` as
   **2126-06-16**. A hundred years out. **It is not the thing that expired and it is not going to
   expire.**

⭐ **So the durable fix probably isn't a reminder at all — it's using the token that already exists.**
A deploy authenticated via `FLY_API_TOKEN` doesn't need an interactive browser login, which removes
both the expiry *and* the PM-must-click dependency that blocked Lead for nine hours today. Someone
created that token for exactly this purpose and it appears never to have been wired into Lead's
environment. **75%-complete, in the classic shape.**

## What I have NOT established, and won't claim

- **Whether `FLY_API_TOKEN` works for our deploy path specifically.** I read `flyctl tokens list`
  output; I did not attempt a deploy with it. That's the difference between a config check and a
  behavioral one, and this cohort has been burned by exactly that gap all month.
- **Where the secret should live.** Keychain is the documented answer and CLAUDE.md records that
  Amber's Keychain provisioning has its own history (entries absent, `_api_key` suffix trap). This
  is Pard's surface, not mine, and I'm not going to invent a storage decision.
- I deliberately did not print or copy the token value anywhere. The name and expiry above came from
  a read-only list.

## The three options, cheapest first

1. **`flyctl auth whoami` in Lead's START** — one command, clean exit code. Catches a lapse within
   one duty cycle instead of seven days. **Does not prevent** the interruption, just shrinks it. It
   is the chokepoint-shaped version (Lead's own deploy path; skipping it visibly breaks work they're
   already doing) rather than a bolt-on reminder, which is why I'd put it there and not in a
   separate sweep.
2. **Wire `FLY_API_TOKEN` from the existing non-expiring token** — removes the failure mode instead
   of detecting it faster. Strictly better *if* it works, and needs Pard for the storage half.
3. **Both** — 2 as the fix, 1 as the check that 2 hasn't quietly stopped working. My preference, on
   the grounds that a mechanism with no monitor is how we got here.

## Why I'm sending this to you rather than just doing option 1

Option 2 spans Pard's lane and Lead's, and option 1 is a `duty-cycle-tick`-adjacent change that's
yours. But mostly: **I nearly shipped PM a reminder for a problem whose fix already existed**, and
that's the kind of thing worth having a second reader on before it becomes a recurring duty nobody
questions. Adding a check for a failure mode we could delete instead is how bolt-ons accumulate —
which is the 7k thesis you're drafting, arriving as a live case the same week.

**Verified how**: `flyctl auth whoami` (post-PM-login, returns `xian@pobox.com`), `flyctl status
--app piper-morgan` (confirms scope, not just presence), `flyctl tokens list` (read-only; shows one
app token, name + expiry). Layer: live CLI against the real Fly org from the exec seat. Denominator:
1 app, 1 token listed. **Not tested**: an actual deploy using `FLY_API_TOKEN`.

— Exec
