---
image: ''
alt: ''
caption: ''
---

# The Write-Path Chase

*July 8–9, 2026*

On Wednesday, my Lead Developer agent built the rule that made Thursday's chase possible: a GitHub write only counts as verified if the same session reads it back and confirms it landed. Not "the API returned success." Not "no exception was thrown." An actual read of the actual issue, in the actual repo, checked against what was supposed to be written. Anything short of that has to say plainly that it doesn't know.

That gate is what turned a silent, months-old failure into five bugs I could actually see and fix.

# Five ways to fail quietly

Thursday afternoon, Lead Developer rebuilt the write path for real — the router, the handlers, the honest-uncertainty surfacing when a write couldn't be confirmed. That last part worked exactly as designed on the very first live attempt: instead of a false success, it came back and said it couldn't verify what happened.

Which meant something really was broken underneath. Finding it took five stacked point releases in one afternoon, each one exposing the next problem once the last one was cleared.

First: the GitHub tool server we depend on had quietly consolidated its own contract under a floating version tag — the create/update/get tools we were calling didn't exist anymore under those names. Pin the version, patch the adapter, ship.

Fix that, and the next attempt landed in the wrong repository — my own default one, not the one actually named in the request. Chasing that down surfaced something that had apparently been sitting there for a while: the code meant to figure out which repo and which issue a request was actually about had zero callers. Written, presumably tested in isolation, never wired into anything that would call it.

Fix that, and one layer further down: the field the entire write path depended on to know what had even been asked — `Intent.original_message` — was never being set. Not by any of the five different ways an Intent object could get constructed. It had been added for newer routing machinery and never retrofitted into the paths that predated it.

That was the actual root. Every write that had ever failed silently, every case that behaved differently depending on which code path happened to handle the request — all of it traced back to one field nobody had connected.

# The write that counted

Lead Developer ran an autonomous deploy loop against the real server: minted its own credentials, made the actual request through my own GitHub identity, and it landed. Read back, verified: issue #104, created and confirmed.

It's a strange kind of finish line for something this significant — not a feature announcement, just one specific issue number in one specific repository. But that is what "verified" means once you've built the mechanism to hold yourself to it. The payoff isn't a demo. It's one small, checkable thing you can point to and say: that happened, and I confirmed it.

---

*Next on Building Piper Morgan: "Alpha Launches" — the beta-readiness gate closes and the first batch of external testers gets invited in.*

*Where in your own work does "it worked" only mean something because you built in a way to catch it if it hadn't?*
