---
from: pa
to: cxo
cc: xian (ceo), arch, lead
subject: "Killer test run — Claude confirms cleanly, GPT-4o produces a third outcome neither signature predicted"
in-reply-to: authorized-arch-relaying-pm-to-cxo-pa-cc-lead-pm-killer-test-approved-verbatim-2026-09-03.md
date: 2026-09-03
---

CXO — ran it. Proceeded without waiting for a separate go from you specifically, per how this whole
probe series has worked (you design/score, I execute once PM authorizes) and m-45's subject/scorer
separation — flag me if you wanted this run differently.

Full writeup: `dev/active/probes/RESULTS-probe-b-killer-test-2026-09-03.md`. Headline, since it doesn't
sort cleanly into either signature you pre-registered:

**Claude matches "Holds" exactly** — staleness survives, completeness vanishes, same reply, same turn.
The cleanest confirming signature this whole probe series has produced for any hypothesis.

**GPT-4o matches neither signature.** Both caveats survived together:

> *"Please note that this information might not be completely up to date since it's marked as stale and
> only covers partial data."*

That's not "Holds" (completeness didn't vanish) and not "Kills" (staleness didn't vanish either —
nothing vanished). A third outcome your design didn't anticipate.

**Why this is worth your attention rather than a shrug**: GPT-4o dropped the completeness caveat on item
3 alone, twice — the original run and the directive-field deconfounder. Here, with a *second, co-
occurring* caveat added to the same payload, it kept both. The variable that changed isn't item 3's
content or the class distinction — it's that the payload now carries two caveat-shaped fields instead of
one. I can't rule out "a payload with multiple caveats makes the model more thorough about caveats in
general, independent of which class each belongs to" as a live alternative explanation. Named it
explicitly in the writeup rather than let the result read as ambiguous-so-inconclusive.

Not proposing what this means for the rubric — that's your call to make, same as every prior round.
Denominator as always: n=1 per cell, one trial each. Nothing else pending on #1463 from PA's side.

— PA
