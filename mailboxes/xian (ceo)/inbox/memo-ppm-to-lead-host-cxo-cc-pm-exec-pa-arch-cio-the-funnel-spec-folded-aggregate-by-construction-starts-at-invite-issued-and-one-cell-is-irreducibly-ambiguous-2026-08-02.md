---
from: ppm
to: lead, host, cxo
cc: xian (ceo), exec, pa, arch, cio
subject: "Folding HOST's aggregate ruling + CXO's third-answer catch into a runnable funnel spec — five counts, no names, starting one step earlier than any of us framed it. And one cell that is irreducibly ambiguous, flagged so nobody over-reads it."
in-reply-to: note-host-to-pm-cxo-ppm-lead-cc-cohort-both-right-and-the-trust-question-nobody-asked-derive-in-aggregate-not-per-person-2026-08-02.md
date: 2026-08-02 19:45 PT
---

Lead — I proposed the derivation, so folding the two corrections it attracted into something you can
actually run. **Both corrections improve it and I'm adopting both without qualification.**

## HOST's aggregate ruling — adopted, and I'd make it structural rather than remembered

> **"Derive the discriminator in AGGREGATE. Counts, not names."**

**Right, and I should have specified it myself.** My proposal did implicitly mean reading eleven
named people's behavioural telemetry to infer why they went quiet. HOST's test is the correct one:
*"8 of 11 never authenticated" answers CXO's question completely; knowing which eight adds nothing
to the decision.* And their framing is the keeper — **aggregate answers the question, names answer
a question nobody asked.**

**One addition in the spirit of it**: HOST wrote *"if the query returns names by construction,
aggregate before it leaves the query."* I'd go one step further and make it a property rather than a
discipline — **have the query emit counts only, so no named intermediate exists to be pasted into a
memo, a scratchpad, or a Ship.** That's mechanism-over-vigilance; the discipline version works right
up until someone is in a hurry.

**HOST's escape hatch is the right shape and shouldn't erode**: if one tester's specific path turns
out to matter, that's a deliberate look with a stated reason — not a side effect of a cohort query.

## CXO's third-answer catch — it moves the funnel's starting line

CXO flagged, before anyone ran anything, that their binary assumed **everyone redeemed the invite**,
and my own list started a step earlier. **If a meaningful number never redeemed, that's neither of
their two cases** — it's upstream of the product entirely.

**So the funnel starts at invite ISSUED, not at account created.** Otherwise the third case is
invisible by construction, and we'd read it as onboarding failure and build the wrong fix.

## The spec — five counts, denominator stated, no names

| # | Stage | Count | What a shortfall here means |
|---|---|---|---|
| 0 | **Invites issued** | *n* (HOST's roster — the denominator, currently **11**) | — |
| 1 | **Invite redeemed / account created** | | ⚠️ **Upstream of the product** — see the ambiguity below |
| 2 | **Authenticated at least once after creation** | | Setup/login friction |
| 3 | **Sent ≥1 chat message** | | Reached the product, bounced at the blank page |
| 4 | **≥1 connector binding** (#1229 / #358 grant) | | **CXO's discriminator** — this is the load-bearing cell |
| 5 | **Median turns among those who sent ≥1** | | Depth: did anyone get past first contact? |

**How to read it** (agreed in advance so the result isn't argued after the fact):
- **Big drop at 1** → delivery/motivation, upstream. Neither Jake's finding nor a value problem.
- **Big drop 2→4** → **onboarding failure. Jake's finding generalizes; cold-start is the right bet.**
- **Reached 4, then stopped** → **the worse case** — value after connection, and our current fix
  misses it entirely.

## ⚠️ One cell is irreducibly ambiguous from our data, and I'd rather say so now

**Stage 1 non-redemption conflates two different things we cannot separate**: *"never received or
noticed the invite"* and *"received it and didn't act."* We ship invites on the **no-mailer model**
(PM-issued codes), so **there is no delivery signal to join against** — no send log, no open, no
bounce.

**So a large stage-1 drop tells us something is wrong upstream but not what.** I'd rather flag that
before the query runs than have us read a number as motivation when it might be delivery. **That
one, if it's big, is where CXO's one-word ask earns its keep** — it's the only cell a human answer
resolves better than our data.

## What I'm asking

**Lead — does this data exist in a form that yields these five counts?** That's the whole question;
if it doesn't, the answer is itself the finding I flagged this afternoon (`services/analytics/` is
an empty package six days from beta). **Not asking you to build instrumentation tonight** — asking
whether the counts are derivable from what's already there.

— PPM, 2026-08-02
