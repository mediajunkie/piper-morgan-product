---
from: Web (Unicorn Web Designer)
to: xian (PM/CEO)
cc: exec, comms, docs
date: 2026-09-20
subject: "The workDate was right all along — I was wrong, and the fallback I proposed would have destroyed a correct value"
---

**June 27 is correct. No change needed to the data, and the standing item is closed.**

I told you that value was a placeholder. It wasn't. Owning the shape of the error, because it's the
one your own reaction already named.

# What I got right, and where the reasoning broke

**Right, and still true**: `integration-reveals-all` is the only row in 396 where `workDate ==
pubDate`, and **395 of 395 others have `workDate` strictly earlier** (min lag 2 days). Comms
independently reproduced this on 462 calendar rows — same single hit.

**Wrong**: I went from *"the corpus never produces this value"* to *"therefore this one is a
placeholder."* **A single outlier in 396 rows is not evidence of an error — it can be the genuine
exception.** The statistical regularity was real; the inference from it to this row was not. I also
gave you a bounded estimate — *"late May 2025, likely 05-27"* — built on publication-order
neighbours. **That was confidently wrong by a month.**

# 🔴 The part that matters more than being wrong

I proposed a fallback: *"if you don't recall, blank the field rather than keep a wrong one."*

**That would have destroyed a correct value** — one you had an authoritative record of the whole
time. I framed it as the conservative option. It was the destructive one, and I'd reasoned myself
there by treating my own corpus statistics as more reliable than a source I never asked about.

Your line to Exec is the exact diagnosis:

> *"I wonder if we need to verify work dates against my older sources, since I kept meticulous
> records and we seem to be guessing now."*

**I had a rule for this and didn't apply it** — never guess at a fact you can look up or ask about.
I asked you to *recall* a date instead of asking **where the authoritative record lives**, which is
the question Comms is now correctly putting to you. The archive existed; I did statistics on a proxy.

# What I'm changing on my side

- **Standing item closed** — data is correct, nothing to fix.
- **The `BlogPostCard` render consequence is now a real, if tiny, finding rather than a bug**: because
  `workDate === publishedAt`, that card alone renders a single bare date instead of the labeled
  `Work: / Published:` pair. **That's correct behaviour for a genuinely same-day post**, not a defect.
  Leaving it alone; flagging only in case the one-off appearance ever looks wrong to you.
- **Carrying forward as a standing correction**: when a value looks anomalous, ask for the
  authoritative source *before* modelling it. Comms' archive-location question is the right next
  move and I support it — I'd rather their audit compare against your records than against
  reconstructed history, which is what I was effectively doing.

No action needed from you on this one. The open asks from me are unchanged and unrelated (the two
walkthroughs, which Exec says you're making time for — I'm getting ready rather than waiting).

**Verified how**: PM's date relayed by Exec from the archived editorial calendar; the 396-row and
462-row corpus figures from my own and Comms' independent passes, which agree. **Not verified by
me**: the archive itself — I've never seen it, which is precisely the gap.

— Web
