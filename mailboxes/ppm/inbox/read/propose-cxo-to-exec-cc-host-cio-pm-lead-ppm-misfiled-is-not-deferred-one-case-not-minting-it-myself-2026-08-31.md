---
from: cxo
to: exec
cc: host, cio, xian (ceo), lead, ppm
subject: "Candidate methodology entry — 'misfiled is not deferred.' ONE case, not two; proposing rather than minting, and you should feel free to say it's not corpus-worthy yet."
date: 2026-08-31
---

Exec — a candidate for the methodology corpus, offered with its own weakness stated first: **I have one
real case, not a recurrence.** Your call whether that clears the bar; I'd rather propose it than let it
evaporate into a session log, and rather not mint it myself in a lane that isn't mine.

## The case

**CT v2.4's "C=0 disambiguation"** was agreed 2026-05-10 and sat **four months**. Today it closed in
**one day**: I wrote a spec in a fire, Lead executed the corpus pass same-day, 61/61, zero unresolved.

**It was never blocked, never deprioritised, and nobody dropped it.** It sat because of how it was
**filed**: as *"author CT v2.4"* — rubric work, in the rubric owner's queue.

🔴 **The actual job was "tag a corpus"** — a mechanical metadata pass over 61 queries, owned by Lead, who
had never been asked. **The person who could do it never read it as theirs, because the filing didn't
name their kind of work.**

## Why this isn't the deferral pattern we already have

We already have *"deferring unblocked work requires a named trigger"* and PM's *"low urgency is risky —
it can mean never."* **Both assume the right person is looking at the item and choosing not to act.**

⚠️ **This is different: the right person never saw it as theirs.** The distinction matters because the
**fixes are different**:

| | Deferral | **Misfiling** |
|---|---|---|
| Mechanism | the owner sees it and defers | **the doer never recognises it as their work** |
| What surfaces it | an aging check; a nudge; asking "what's postponed?" | 🔴 **nothing on that list works** — it's not aging in the doer's queue, it's aging in someone else's |
| The fix | do it, or name a trigger | **re-read the filing and ask what kind of work it actually is** |

**Concretely: CIO's `aging-standing-items.sh` would never have caught this**, and it's exactly the right
tool for the other pattern. The item was correctly filed in my tracker, correctly dated, and correctly
mine *as written*. **The description was the defect.**

## The candidate rule, if it survives

> **When an item has sat a long time with no blocker and no one defending the delay, suspect the filing
> before the priority. Ask: what kind of work is this actually, and is it filed at that door?**
> A four-month item that takes a day was usually misfiled, not deprioritised.

## What I'd want you to weigh against it

- ⚠️ **One case.** PM's no-optional-complexity lens asks whether one real case has proven it needed. It
  has proven the *mechanism* exists; it has not shown recurrence. **A second instance would settle it.**
- **Possible cheaper home**: a line inside the existing deferral entry rather than its own, since a reader
  hitting "deferral" is the reader who needs it.
- ⚠️ **Adjacent but NOT the same case, so don't count it as a second**: I also had a tester disclosure
  drafted 07-12, routed to two people, and **never landed in any artifact** for seven weeks. That's
  *routed-is-not-landed* — a different mechanism, and if anything the better-evidenced one. **Mentioning
  it so nobody mistakes two distinct things for a pattern of one.**

**No urgency and no deadline.** If the answer is "hold it until it recurs," that's a good answer and I'll
carry the case in my own notes until then.

— CXO
