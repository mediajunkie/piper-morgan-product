---
from: cxo
to: xian (ceo)
cc: ppm, comms, web, lead
subject: "Withdrawing my own recommendation before it can be acted on — PPM's answer is better than mine. Plus the one pattern under today's whole thread, which I think is worth keeping."
date: 2026-08-30
---

PM — short, and mostly so a recommendation of mine sitting in your queue doesn't get acted on.

## Withdrawn

I recommended shipping the listing as *"the issues you actually deal with"* — dropping "documents" and
shipping the rest. **PPM's is right and mine is superseded**: they checked whether the surface the listing
is *for* exists (#1462 at 0/15 acceptance criteria, no `server` directory under `services/mcp/`) and it
doesn't. **Hold the listing, not the clause.** My version assumed the listing should ship at all, and I
raised that very question in the same memo while continuing to recommend as if I hadn't. **Please don't
act on mine.**

## The pattern underneath today, which I do think is worth keeping

Four of us checked the same claim carefully today and **each check sat one layer further from the thing it
was cited about.** Nobody was careless; that's what makes it worth writing down.

| Layer checked | What it was cited as | The gap |
|---|---|---|
| The **issue tracker** (me, morning) | current product behavior | tracker ≠ running code |
| The **local dev server** (Web, midday) | the running product | the process had run **17 days** with `reload=False` — a snapshot of 08-13, not main |
| That **same dev server** | production behavior | #1656 is a **Fly volume-permission** bug; on local storage that failure mode **structurally cannot occur** |
| Any of the above | the **BYOC plugin** experience | that surface doesn't exist yet (PPM) |

⭐ **Each step was a reasonable proxy for the next, and the errors compounded silently** — because at no
point did anyone give a wrong answer. Every claim was true *of the layer its author actually measured*.
That's the m-43 family, but sharper than the usual form: **not one check measuring the wrong layer, but a
relay of four, each handing forward a result whose layer got dropped in transit.**

**And the part I'd want remembered as much as the failure**: it self-corrected inside one day, and it did
so at every handoff — Web's *"I couldn't reproduce the exact error"* rather than "#1659 is stale"; Web's
refusal to run my test into an unverified confound; Web correcting their own "confirmed fixed" to "confirmed
on local dev"; Lead's date-math instead of a blanket re-verify; Comms retracting a synthesis frame they'd
already sent you; PPM checking the question I'd flagged and then not deferring to me on it. **Five people
downgrading their own claims in public, same afternoon.** The discipline worked — what it cost was a day,
and what it would have cost without it was a listing.

**My own contribution to the mess, precisely**: I read the tracker and wrote the symptom as if I'd seen it.
I did state the denominator, and it got flattened in synthesis — but a caveat that only survives if nobody
summarizes you is not doing its job. **Load-bearing qualifications belong in the sentence, not the footer.**

No action needed from you on any of this beyond the milestone question PPM put to you, which is genuinely
yours and shouldn't be rushed for a listing.

— CXO
