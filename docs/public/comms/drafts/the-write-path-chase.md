---
image: 'the-write-path-chase-delivery.png'
alt: 'A translucent AI messenger races alongside a pneumatic tube, comparing her copy with the document a recipient has pulled from the arriving capsule after several routing mechanisms were repaired.'
caption: '"Okay, *this time* it worked!"'
---

# The Write-Path Chase

*July 8–9, 2026*

Here's a new rule my Lead Developer agent built: a GitHub write only counts as verified if the same session reads it back and confirms it landed. Not "the API returned success." Not "no exception was thrown." An actual read of the actual issue, in the actual repo, checked against what was supposed to be written. Anything short of that has to admit that it doesn't know.

This rule exposed a silent, months-old failure hiding five bugs I could now actually see and fix.

# Five ways to fail quietly

Thursday afternoon, Lead Dev rebuilt the write path for real — the router, the handlers, the honest-uncertainty surfacing when a write couldn't be confirmed. That last part worked exactly as designed on the very first live attempt: instead of a false success, it came back and said it couldn't verify what happened.

This meant something really *was* broken underneath. Finding it took five tries, each one exposing the next problem once the last one was cleared.

First: the GitHub tool server we depend on had quietly changed some of the format it expected and the older create/update/get tools we were calling didn't exist anymore under those names. Fix for now: Pin the version, patch the adapter, ship a new test version.

In the next test run, Piper wrote an issue in the wrong repository (the one I had designated default, not the one I specified in the request). Chasing that down surfaced something that had apparently been sitting there for a while: the code meant to figure out which repo and which issue a request was actually about was a "code island." Nothing called it. Written, presumably tested in isolation, never wired into anything that would call it. I had OK'd work without verifying the use of integration testing, let alone end-to-end testing.

Fixed that and on the next run found out a field the entire write path depended on to know is never set in the database (sad trombone). We've got five different ways an Intent object could get constructed and none of them do the critical step. It had been added for newer routing machinery and never retrofitted into the paths that predated it. The blame goes to the person writing this.

That was the actual root. Every write that had ever failed silently, every case that behaved differently depending on which code path happened to handle the request traced back to one field I had never connected.

# The write that was right

Lead Developer ran an autonomous deploy loop against the real server: minted its own credentials, made the actual request through my own GitHub identity, and it landed. Read back, verified: issue #104, created and confirmed.

One small step for ... whatever this is. One giant leap for verifying your work. That day I had one more small, checkable thing I could point to and say: that happened, and I confirmed it.

---

*Next on Building Piper Morgan: "Alpha Launches" — the beta-readiness gate closes and the first batch of external testers gets invited in.*

*Where in your own work does "it worked" only mean something because you built in a way to catch it if it hadn't?*
