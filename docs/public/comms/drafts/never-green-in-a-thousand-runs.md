---
image: ''
alt: ''
caption: ''
---

# Never Green in a Thousand Runs

*September 9–11, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. PM writes
the prose. Everything below the line is notes for PM. Delete it as the prose replaces it.
Slot: Tue 2026-11-10 (building). Beat 2, next in strict order after Thu 11-05 "Don't Overpromise" (Sep 7–8). xian said
yes 11-04 and may change the title.
Footer teases Thu 11-12 "The Server Key Is Not a Real Concept" (working title). Ship #068 (Wed 11-11) sits between
them and is skipped by the tease rule.
Sources: Lead 09-09 log (l.25-27, 37-70), Exec 09-09 log (l.94-103, 127-137, 148-149), Lead 09-11 log (l.41, 78-106),
prog 09-11 log (l.21-37), omnibus 09-09 (l.258-261) and 09-11 (l.308-312, 524-525), ship-059 internal report 09-04
(l.137), decisions.log l.1865. Facts gathered by a Sonnet subagent. Comms re-opened the key quotes at source.
-->

---

## Title options (pick one, or your own)
- **Never Green in a Thousand Runs** (working). Exact for the end-to-end suite only. See the accuracy notes.
- **A Subset Phrased as a Total.** Lead's own words for the mistake, and the thread through both halves.
- **Locally Correct, the Sum Wrong.** Lead's words for the first half.
- **They Weren't. I Was.** Lead's answer to your question.

## The story in one sentence

You asked how you could be the one blocking work nobody had started, and Lead said you weren't, Lead was. Two days
later Lead found that "the belt is fully green" had been true only for the four checks Lead was counting, while one
of the others had not passed once in a thousand runs.

## Beats, in order (facts verified, source in brackets)

**1. The pile that didn't shrink.** Wed Sep 9: your live test pass closed six more issues around midday, and the
backlog still grew. Exec's rollup: Sprint Backlog went from 28 to 34, "grew by six while PM closed six", and
"Never-started hasn't moved down all week." [Lead 09-09 l.25-27, Exec 09-09 l.94-103]

**2. Your question, and Lead's answer.** About 1:15 PM you asked how you could be blocking never-started work. Lead's
log heading: "PM's how-am-I-blocking-never-started question answered HONESTLY: they weren't. I was." [Lead 09-09 l.37]
- The mechanism: for two weeks every duty fire drained incoming mail first, so the agent was never idle, and the
  backlog-intake step never ran. In Lead's words: "Each fire locally correct; the sum wrong." [l.39-41]
- To Exec: "nothing prevents starting a never-started item — PM has never been the blocker on them, I have." [Exec
  09-09 l.132-134]
- Your exact question isn't recorded anywhere. Write it from memory, or paraphrase.

**3. Your words for the reporting problem.** The same day, of the status reports: "the state of the forest and not
just the most recently noticed trees." [Exec 09-09 l.148-149] Exec retracted two of three throughput numbers given
to you that day.

**4. "Fully green."** Lead's week before had been reported as "the CI belt fully green for the first time on record".
[Ship #059 internal report, 09-04 l.137] On Fri Sep 11 that morning, Lead again: "Belt fully green as of this
morning's fix." [Lead 09-11 l.41]

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
