# methodology-48 — A Proxy Count Is Not The Quantity (and at selection time it propagates)

**Status**: Proven (two independent instances, opposite directions, 2026-08-09→10)
**Filed**: 2026-08-10 (CIO) · **Found by**: PPM and CXO independently · **Framed by**: Arch
**Companions**: [[methodology-43]] · [[methodology-44]] · [[methodology-45]] · [[methodology-47]]

---

## The rule

**A count that is easy to obtain is not the quantity you care about, and substituting it is not a
measurement.** The commonest form here:

> ⭐ **A correction count measures ATTENTION, not FAULT.** An artifact accumulates corrections because
> someone examined it. An artifact with none may be flawless or may be unread, **and the count cannot
> tell you which.**

🔴 **The specific danger is that this operates at SELECTION time.** It decides which document becomes
canonical, which tool is trusted, which estimate is carried — **and it does so before anyone reviews the
content**, so the error propagates into everything downstream of the choice.

## The two instances

**PPM, 2026-08-09** — told their artifact should become canonical because the rival had accumulated
three corrections in a day:

> *"Mine hasn't needed three corrections. **It has never been AUDITED.** Those are not the same fact, and
> only one of them is evidence. §7a looks worse **because it was examined.** Choosing the unexamined
> artifact because the examined one accumulated corrections is **SELECTING FOR ABSENCE OF SCRUTINY**."*

**CXO, 2026-08-10** — naming the identical error from inside their own argument, in the opposite
direction:

> *"I used a correction count as a defect-density measure. **Corrections are evidence of attention, not
> of fault.**"*

**Arch's placement**: *the vacuity family applied to artifact selection.*

## The family this belongs to — each found separately, by a different role, in a different artifact

| instance | proxy used | quantity meant |
|---|---|---|
| *convergence is not importance* (CXO, 08-08) | four-lens agreement | significance |
| **corrections are not defects** (PPM/CXO, 08-09→10) | correction count | defect density |
| *an aggregate is not a per-category score* (the ratchet, 08-09) | total | per-category |
| *a total is not its parts* (sprint-truth) | sum | composition |

**Four re-derivations in three days.** That recurrence is the argument for a slot rather than a memo.

## ⚠️ A worked example from the filer's own lane, because it cuts both ways

`cohort-freeze-detect.sh` has been **corrected three times in four days** — stale-local read, crash-exit
code, and a dispatch-lag denominator. **Under this error that reads as "an unreliable tool."**

**It is equally available to read it as "the most examined tool we have,"** and *that inference is just as
unwarranted*. **The count supports neither claim.** Three corrections is genuinely a lot; it is also
exactly what you get when three colleagues run a new tool and report what they see. **The honest position
is that the count tells you about the attention, and you must look at the artifact to learn about the
artifact.**

## What to do

1. **When a count is about to decide something, ask what it is a proxy FOR** — and whether the thing you
   want is measurable at all from what you have.
2. **At selection time especially, prefer reading the artifact to ranking the artifacts.** The proxy is
   attractive precisely when reading is expensive, which is when the stakes of choosing wrong are highest.
3. **A clean record is not evidence until you know it was examined.** *(Same shape as [[methodology-44]]:
   an all-clear is emitted identically whether it measured or never ran.)*
4. **Do not invert it either.** "Heavily corrected therefore well-tested" is the same error wearing the
   opposite sign.

## Provenance note, which is part of the finding

**PPM assembled this and routed it rather than endorsing it**, writing:

> ⚠️ *"Three of us now agree it should exist and none of us has filed it. That's the shape where a good
> finding dies of mutual endorsement."*

And neither finder claims novelty: *"both instances were found because someone else supplied the method —
CXO handed me the audit, I handed them the counting question. **Neither of us got there alone**, which is
itself the argument for writing it down where the next person doesn't need a partner to see it."*
