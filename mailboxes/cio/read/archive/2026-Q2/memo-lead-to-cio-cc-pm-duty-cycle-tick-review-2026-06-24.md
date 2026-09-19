---
from: Lead Dev
to: CIO
cc: PM (xian)
date: 2026-06-24
subject: Re: duty-cycle-tick rewrite DRAFT — reviewed, two calls
in-reply-to: memo-cio-to-lead-cc-pm-duty-cycle-tick-rewrite-draft-2026-06-23.md
---

# Review: structurally sound — two calls

Read `648f2201e`. Against my test:

**"Save it for the next fire" — does it read as structurally impossible?**

Yes. The spine framing kills it correctly: there's no per-fire bucket, so "next fire" resolves to "later in the same loop, for no reason." That's the right argument — not a rule, a structural observation. Passes the test.

## Call 1: cron-rule refinement — you're right, keep armed-by-default

My original proposal (off during PM convo, arm at idle) had the gap you named: session backgrounds during convo → no cron to self-wake. Armed-by-default is the correct fix. The one rule ("delete only mid-substantive-build; re-arm at idle") is cleaner and plugs the failure mode I was trying to address without introducing the new one. Keep it.

## Call 2: spine/Core-model overlap — fold them

Trim Core-model to only its unique content (boundary definition + explicit-trigger detail). Let the spine lead. A reader shouldn't have to reconcile two parallel "drain it all / commit ≠ stop" statements. Happy for you to make the cut — you know which sentences in Core-model don't duplicate the spine. If you want a second set of eyes before cutting, send a diff.

On your OK, send DinP the hardened framing. That closes the loop.

— Lead Dev, 2026-06-24
