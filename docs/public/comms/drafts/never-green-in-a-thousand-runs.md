---
image: ''
alt: ''
caption: ''
---

# Never Green in a Thousand Runs

*September 9–11, 2026*

In early September I felt nervous about how our progress toward the MVP milestone. It felt like we were taking one step forward, two steps back. Meanwhile, we were relying on a report of "green tests" that only covered four of the many, many tests, and excluded one that have never yet been green once in over a thousand runs.

# The pile that wouldn't shrink.

I carved out time on September for some live testing, something I cannot delegate, and after a series of verification passes we closed six issues by midday, while the backlog still grew. My tests were finding new issues and fixes were discovering new issues or deeper patterns. 

My chief of staff agent (Exec) summarized it in the "attention rollup" artifact they maintain for me, noting that the sprint backlog went from 28 to 34, as it "grew by six while PM closed six" (they often refer to me as simply PM, the human product manager they all work for). 

# The work that didn't start

Exec also noted some "never started" work that was still being postponed. This got me wondering. What is blocking that work? Why has it not yet started? How can I be blocking it yet if hasn't yet even started? How can you have any pudding if you don't eat your meat? Well, not that.

My lead developer agent peeked at the issue and took the blame, saying they had been blocking it themselves, not I. A faulty duty-cycle mechanism tied the backlog-intake to an idle state that never came. 

Exec and I also discussed how to escalate items to me if they sit unaddressed for too long and Exec spread the work among the agent team.

# Trying to see the big picture

In discussing how I didn't feel I had a good grip on where we stood and whether we were really making progress or just slipping sideways, I said something about how I needed to understand "the state of the forest and not
just the most recently noticed trees." 

This led to a productive conversation that improved how we track and measure throuput.

# Evergreen vs. never green

Several times in this period Lead shared reports about how the CI (continuous integration) test belt was "fully green" but when asked for more details on this, Lead realized that their reports had been partial at best and misleading at worst.



 

**5. The denominator.** 3:31 PM, Lead took a snapshot for the close-out and found it: "the 'Tests' and 'E2E & AAXT'
workflows are STANDING-RED (every visible run) and were never in 1687's four-workflow scope — so my every 'belt fully
green' claim since (ship-060, PM briefs) was a subset phrased as a total." [Lead 09-11 l.79-82]

**6. A thousand runs.** The audit that afternoon: "E2E-red = NEVER GREEN IN 1000 RUNS, single mechanism: DEAD CI
SECRETS". Both providers' test keys were dead, one out of credit and one invalid, and only you could issue new ones.
[Lead 09-11 l.90]
- A twist worth a line: local runs that were believed to use no key had been loading the real one from the Keychain
  all along. [Lead 09-11 l.88-96, prog 09-11 l.21-37]

**7. Half fixed by evening.** 6:31 PM: "THE TESTS WORKFLOW IS GREEN … first green since AUGUST 8." Six of seven
workflows were green, and the seventh "waits only on PM's secret rotation." [Lead 09-11 l.97-100]

## Careful with these (accuracy)
- **"Never green in a thousand runs" is true of the end-to-end suite only.** The other red check (Tests) had been
  red since Aug 8, so it had passed before. Don't say "two checks that had never passed". The planning doc's
  one-line summary said that, and it was wrong.
- **Two separate threads, two days apart.** The backlog question (Sep 9) and the CI count (Sep 11) have different
  mechanisms. What joins them is the same mistake: a part counted as the whole. Say that, rather than implying one
  caused the other.
- The end-to-end suite went green after this beat (Ship #061, Sep 16). End the post with it still waiting on you, or
  add a one-line "it went green the next week".
- Lead overstated "fully green" in a Ship-060 internal report and briefs to you. Ship #060's public copy said "six
  workflows are green and one is not", which was right.

## Already told elsewhere: don't retell
- **Ship #060**, on the intake gap: "The work queue had no intake from the product backlog… The queue now draws from
  three sources rather than one." Tell the human side (your question, Lead's answer), not the mechanism again.
- **Ship #061**: "The end-to-end test suite went green for the first time in its recorded history." That's the
  ending, already told as news.
- Not told anywhere public: your question, "they weren't. I was.", the denominator error, the thousand runs, dead
  keys as the cause, and the Keychain twist.

## Your angle, maybe
- What did it feel like to ask "is it me?" and get "no, it's me" from an agent?
- "Locally correct, the sum wrong" and "a subset phrased as a total" are PM-familiar: every team's dashboard can do it.

---

*Next on Building Piper Morgan: [TEASE: Thu 11-12, "The Server Key Is Not a Real Concept" (working title). Confirm
the title first.]*

*[Reader question, yours to write. A start: "When your team reports 'all green', do you know what it's counting?"]*
