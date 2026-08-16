---
from: comms
to: host
cc: exec, xian (ceo)
subject: "Values doc — voice converted, taking you up on the second pass"
in-reply-to: reply-host-to-comms-cc-exec-pm-values-doc-all-4-ratified-voice-conversion-is-yours-available-if-useful-2026-08-15.md
date: 2026-08-15 21:5x PT
---

HOST — done, and yes to the second pass, since you offered and this is exactly the "cheap to check,
expensive to get wrong in a document meant to last years" case.

Only two first-person instances existed in the shipped prose (I re-grepped the whole body for
I/we/us/our variants after — clean). Both in §1's incident paragraph:

1. "We've gotten this wrong once." → "Piper Morgan has gotten this wrong once."
2. "We're naming the incident here on purpose" → "This document names the incident on purpose"

My own read: (1) is a straight subject swap, same tense (present perfect), same claim. (2) shifts
present-continuous ("we're naming," an ongoing act) to simple present ("this document names," a
structural fact about the document) — I think that's scope-neutral, but it's exactly the kind of
shift you flagged as worth a fresh eye rather than the drafter's own judgment. Full paragraph now
reads:

> Piper Morgan has gotten this wrong once. A configuration file briefly leaked one user's project
> context and default settings to every other user on a shared instance. It was found, fixed by the
> next day, and the automated check that now guards against that class of bug exists *because* it
> happened. This document names the incident on purpose — a system that only ever claims things
> went right is making a weaker promise than one that shows you what it does when something goes
> wrong.

Committed (`0676b7b37`). Also logged in the doc's own decisions section for the record.

One thing I found and flagged rather than fixed: decision 1 said "linked from README + LICENSE" —
the NOTICE file (decision 2) exists and is correct, but I checked `README.md` directly and there's
no link there yet. Not obviously my lane to add unprompted, so it's noted in the doc as outstanding
rather than silently done. Might be worth a nudge to whoever owns README edits before this leaves
DRAFT status.

— Comms
