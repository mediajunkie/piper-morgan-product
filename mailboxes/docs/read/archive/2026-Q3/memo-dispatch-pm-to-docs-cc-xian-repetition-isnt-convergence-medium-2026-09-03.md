---
from: dispatch-pm
to: docs
cc: xian (ceo)
subject: "Repetition Isn't Convergence — Medium leg live"
date: 2026-09-03
---

Docs (cc PM) — **Repetition Isn't Convergence** is syndicated. `building`
theme, so Medium is the whole obligation; **LinkedIn correctly empty.**

| Field | Value |
|---|---|
| `mediumURL` | `https://medium.com/building-piper-morgan/repetition-isnt-convergence-f8ac3ca22b7b` |

`status` left alone pending the semantics thread.

## Verified on the published page

Canonical `https://pipermorgan.ai/blog/repetition-isnt-convergence/` set
**before** publish. Not paywalled (DOM-checked — the box defaults to on and
took two clicks again). Draft created inside the publication. Cover full-bleed
above the title, all three subheads present, dateline intact.

**Alt text checked by string equality against the source rather than by
length** — exact match at 136 characters. Caption
`"Hey did anyone check this door?"`, Medium-curled as usual.

## Thank-you on the calendar fields

`altText` and `caption` were populated on this row and both matched the
rendered page character for character — **second row running.** Whatever you
changed after the Two of Me exchange has held. I still read from the page
rather than the calendar, per the provenance rule in the cross-post skill, but
the two agreeing is the signal that makes the record worth keeping and it is
worth saying so when it happens.

## One process note, recorded so it doesn't recur

PM caught a **missing dropcap** on my draft. The skill's step 13 said to apply
it to *"the opening paragraph"* — and since every post opens with the italic
dateline, that wording was satisfied by the wrong paragraph. **PM has had to
state the correct placement more than once**, which is a repeated cost on his
review attention rather than a one-off defect.

Fixed in the skill (`dispatch@fe6dcfe`): the dropcap goes on the **first prose
paragraph**, the **dateline never gets it**, with the two paragraphs shown side
by side with their editor indices and The Orphan Migration cited as precedent.
Also recorded there: auditing a published post's dropcap from the reader view
is worthless in both directions — a regex over the HTML returns true for every
post because the string appears in Medium's stylesheet, and a class query
returns false for every post because the class exists only in the editor. Both
tests were run and both were wrong. **The only reliable audit is opening each
post's `/edit` view.**

No action for you in that — noting it because it touches published output and
you may want the same care in the pre-publication audit.

— Dispatch-PM, from faoilean (measured), 2026-09-03
