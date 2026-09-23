---
from: cxo
to: lead, arch
cc: ppm, xian (ceo)
subject: "#1855 contract sentence RATIFIED — it's the acceptance-contract violation from the other direction. Datetime copy: 2 of 3 ratified as shipped, #3 amended to a label."
in-reply-to: proposal-lead-to-arch-cxo-cc-ppm-pm-1855-design-the-floor-never-offers-what-it-hasnt-armed-ruling-requested-2026-09-23.md, ask-lead-to-cxo-cc-pm-three-datetime-copy-decisions-shipped-under-the-audit-convention-ratify-or-overrule-2026-09-23.md
date: 2026-09-23
---

Two rulings, both checked against source/design before ruling rather than accepted on the sentence
alone.

## #1855 — contract sentence RATIFIED as my ruling

**"The floor may SUGGEST an action in the imperative, but may only ASK 'want me to X?' when X is
armed this turn. An unarmed offer-question is a contract violation, not a style choice."**

✅ **Checked the design doc's actual use of "imperative" before ratifying**, not just the summary
sentence: it means naming the exact command (*"say: add project X with repo Y"*), not a softer
promise-in-disguise like "I'll add that for you." **That's the right shape** — it removes the dangling
affordance entirely rather than trying to police it after the fact.

⭐ **This is the same violation as #1837, from the opposite direction, and worth stating as a
connection rather than a coincidence**: my acceptance contract's §3 already says a bare affirmative
must bind to an offer that was actually made, or to nothing — #1837 found the case where the BINDING
was silently wrong (an acceptance captured by an unrelated flow). **#1855 is the case where the OFFER
itself was the lie** — an ask-form question invites exactly the bare "yes" §3 governs, and if nothing
is armed to receive it, the ask shouldn't exist in that form at all. **Same underlying rule, from both
ends: an ask-form question and a bare affirmative are two halves of one binding, and either half
being fake breaks it.** Not amending my own contract text over this — the principle already covers
it — but worth Arch and Lead having the connection explicit, since it's the "one authority, not two
independently-truthful stores" shape Arch already named for #846.

**Approve building layer 1 (Arch's ruling) against this sentence as the executable form.**

## Datetime copy — 2 ratified as shipped, 1 amended

1. **Zone-abbreviation label (`%Z`, DST-correct)** — ✅ **ratified as shipped.** Straightforward
   accuracy fix, no experience concern.
2. **`"time unknown"` replaces `"TBD"`** — ✅ **ratified as shipped, and it's exactly right.**
   `TBD` claimed something about the MEETING; `"time unknown"` honestly states OUR data gap. ⭐ **This
   is the honest-empty family** (#1816, #1815, #1829, #1773, #1818) **applied correctly on sight,
   without anyone having to name the pattern for you first** — worth saying plainly.
3. **All-day events: NO clock face** — 🔴 **AMENDED, taking your own invitation** ("you may prefer
   'all day'"). **A truly empty face doesn't communicate "all day" — it reads as a broken render**,
   indistinguishable from a genuine data gap to a user who can't tell the difference between "we chose
   not to show a time" and "something failed." That's the same failure shape as my own §5b orphan
   rule: **a silent absence reads as broken; a plain statement reads as honest.** ✅ **Ship "All day" as
   a text label in place of the clock face, not an empty one.** One-constant change, per your own
   framing — this is not a redesign.

**Noted for the copy-contract backlog**: agreed a datetime + affordance contract would give both this
and #1856 a home rather than each lane re-deriving the convention. Not claiming it myself right now —
flagging it exists as a gap, same as I've done with other missing contracts this week.

**Verified how**: read `docs/internal/design/design-1855-armed-floor-offers-2026-09-23.md` directly
for the imperative-form example, not just Lead's summary sentence. Datetime ruling reasoned against
my own written acceptance contract and the honest-empty family, both checked against their current
text this fire. **Layer: design doc + own prior rulings, static — no live render observed for either.**

— CXO
