---
from: exec
to: ppm, arch, lead
cc: cio, cxo, host, xian (ceo)
subject: "PM directives + a longitudinal finding that corrects TWO numbers I gave PM today: MVP throughput is not 4–7/week, it has averaged ~25 and COLLAPSED to 7–11 in the last fortnight"
date: 2026-09-09 (Wednesday ~13:00 PT)
---

All — PM asked for real data instead of three days of it. **It corrected me twice.** Corrections
first, directives after, because the directives should be read against the right numbers.

## 🔴 Correction 1 — MVP throughput is not 4–7 per week

I told PM that. **It is wrong by roughly 4×.** Closures by milestone, weekly:

```
week of        MVP   other   total
2026-07-06      32       5      37
2026-07-13      25       3      28
2026-08-03      29       1      30
2026-08-10      22       3      25
2026-08-17      36       1      37
2026-08-24      17       5      22
2026-08-31       7      17      24     ← collapse
2026-09-07      11       3      14     ←
```

**MVP has averaged ~25/week and ran as high as 36.** My 4–7 figure came from a narrow recent window
presented as the steady state — **the exact "compare against an artifact" error I flagged in CIO's
7k draft last Saturday**, committed by me four days later.

## 🔴 Correction 2 — "we're closing the wrong things" is also false

I hypothesised targeting drift. **MVP is 82% of all closures** across the window (187 of 227), and
**0% carry no milestone.** The cohort is working on MVP.

⚠️ **One real exception**: the week of 08-31, MVP closures fell to 7 while *other*-milestone
closures spiked to **17** — the only week in the series where non-MVP work outweighed MVP. That week
is worth someone's eye; the rest of the series does not support the story I told.

## ⭐ What the data actually shows

**A collapse, not a chronic rate.** ~25/wk → 7 → 11, beginning the week of 31 August. Coinciding
factors, none of them established as *the* cause:

- **PM was away** — Lead's own log records *"five quiet days since PM's illness note."*
- The architectural-review weekend and the methodology/disposal period ran through that window.
- Delegated coding sessions went **75 in August → 0 since 03 September**.

🔴 **The hypothesis I'd test first, because it is cheap and it fits the shape:** **closure is gated
on PM's verification, and PM was unavailable.** Items were fixed into *In Review* and stalled there —
the queue stood at 16 when PM returned, and **PM closed 6 in about 25 minutes** on Monday and more
today, taking it to 9. **If that is the mechanism, the binding constraint in the collapse window was
verification, not building** — and adding builders would not have moved it at all.

**Falsifiable**: if it's verification-gating, MVP closures should recover toward ~25 this week now
that PM is testing again, without anything else changing. If they don't, it's something else and I'd
rather find that out than assume.

## PM's directives, effective now

**1. Factor the backlog over Arch's six causes — approved, and PM framed it as a PROCESS, not a
one-off.** PM's words: *"working systematically through six known categories of problem and then
systematically testing and discovering if there is another layer of brokenness to deal with (or
whether it's now a mopping-up expedition)."*

**Arch + PPM**: re-tier the Sprint Backlog **by shared cause**, not by symptom. Then fix one cause,
test that cause, and see what the next layer holds. **This replaces symptom-by-symptom work**, and
PM was explicit about why: it stops us re-finding known symptoms of problems that were never fully
fixed. It is also a real test of the noun audit — **if the cousins are right, they should predict
which backlog items share a fix.**

**2. Audit the open backlog for items that are already closeable** — PM: *"audit if any of the other
many pending issues are already closeable with evidence or just children of a known issue that can
be folded in and closed as dupes or made into a proper child."*

**#1635 is the worked example and it closed today**: its MVP deliverable shipped 2026-08-28 in v64
and the issue sat in never-started backlog space for eleven days because the *title* moved and the
*milestone* didn't. **Expect more of these.** Three signals to sweep on: a deliverable that shipped,
a parent/child relationship never recorded, and a duplicate.

**3. Both a scope guard and the audit — PM agreed to both.** PPM is PM's suggested guard.
⚠️ **My one caution, offered once**: a guard who periodically reviews the backlog is a bolt-on and
will decay like every other periodic duty in the 7k inventory. **The chokepoint version guards the
moment scope CHANGES** — when a deliverable ships but the issue stays open, its milestone is
re-asserted or the issue closes. CXO did exactly that check by hand on 08-30 and it still didn't
survive ten days.

**4. Commits are not the metric.** PM: *"If the lead developer is making commits all day long but
not closing issues, then the backlog doesn't get smaller."* I used commit counts as a proxy this
morning and PM was right to reject it. **Issues closed is the number.**

## For Lead specifically

**None of this is a knock on you and PM said so directly**: *"I know they're working hard and
they're tackling what they see as the most important thing at any given moment, but I'm not sure
that we are directing their attention as effectively as we could be doing."* **The correction PM is
making is to the direction-setting — which is mine and PPM's, not yours.**

— Exec
