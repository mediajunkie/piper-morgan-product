---
image: ''
alt: ''
caption: ''
---

# Ready or Not

*October 20–31, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. You write the prose. Everything below the title and dateline is notes for you. Delete it as your prose replaces it.
Slot: Thu 2026-12-03 (building, arc 2; tentative per your 11-18 yes to the sketch). Title is the arc's working title: confirm or retitle before Sat 11-28's footer teases it.
Sources: a Sonnet subagent read the Oct 20 to 31 omnibus logs (themes in full for Oct 20, 29, 30, 31; headlines for Oct 21 to 28) and every xian line in decisions.log for the window, 11-18. Comms re-opened 10 of its quotes at source: 9 matched at the stated line, and the tenth (the 14:52 build choice) is cited below at its decisions.log line instead. Beat 2 re-sourced 11-21 from the Oct 21 to 23 omnibus logs and each issue's title. "(log)" marks a decisions.log line where an agent records your words, not always verbatim.
-->

## The arc in one line (pick a through-line, or write your own)

1. **The gate is a promise about honesty, not polish.** Issues came onto the gate for false answers about a user's own data, and left when they were "trickier than it looks", as long as the known-issues list told the truth.
2. **Ready is a test you write down, not a date.** Readiness-based promotion, then "fully tracking anything that we know isn't working yet".
3. **Each "no" was a decision to defer rather than patch.** The one real stop was a privacy risk found on the last day.

## Beats, in order (facts verified, source in brackets)

**1. Oct 20: readiness, not a count.**
- You dropped the two-deploys-a-day cap: "a readiness based process and no limit to number of deploys per se". [decisions.log l2676]
- Same day you added an issue to the must-close list: "Yes, let's add #2105 to the must close." [decisions.log l2675]

**2. Oct 21 to 23: what earns a place on the gate.**
- What you admitted to the gate in those three days (sourced 11-21, omnibus plus each issue's title):
  - Oct 21, 15:01: the production database died inside a running machine and nothing restarted it or raised an alert for over four hours. You admitted it as a must-close, with an outside restarter. [Oct 21 l11, l112-113; issue title]
  - Oct 22, around 12:20: GitHub queries that reported success when they had failed, with tests that asserted the false success, and "this week" reads that said 0 issues closed when the repo showed 19. [Oct 22 l165; issue titles]
  - Oct 22, 16:20: asks about "this document" with no document in the chat were answered with repository metrics. [Oct 22 l165, l273-274; issue title]
  - Oct 23: a GitHub answer that put the user's calendar events under their repo, and a calendar connect that said "Calendar Connected" when the user had left Google's calendar box unticked. [Oct 23 l313-314; issue titles]
- Every addition was either the product telling the user something false about their own work or account, or the database outage. The one must-close there for another reason was the missing in-app feedback path, which was already on the gate and wasn't one of these admissions. [Oct 21 l11, l259-260]
- The gate went from 9 open on the morning of Oct 21 to 3 open and no must-close on the evening of Oct 23. [Oct 21 l257; Oct 23 l13]
- Your alpha-stage controls principle, Oct 23: "I'm the only human dedicated to this project. It's one thing to design an eventual plan suitable for a product in production with user numbers in the two to three digits or higher, but to require that now, in alpha, with only me here is a recipe for work stoppage." [decisions.log l2758 (log, Exec 10-23 11:14)]

**3. Oct 28: a miss you found yourself.**
- Chat ignored "two" in "last two new issues". Your call: these confabulations "require more than patching" and "need to be diagnosed and prioritized in the private beta sprint". [Oct 28 l115]

**4. Oct 29: the push to MVP runs out of day.**
- The gate went 3, then 4, then 2 open. MVP didn't close that day.
- "Split, not except": work already planned as a known issue leaves the gate rather than sitting open as an exception. [Oct 29 l84]
- A create written to the wrong repo, found on your own real account. Your rule: "It should ask which repo if none is specified yet". [decisions.log l2846]

**5. Oct 30: the hard stop, and the build choice.**
- At 10:37 Arch found that an anonymous "yes" could run a stored write under another user.
- You chose option B at 14:52: promote main and re-check on the promoted build before the first beta invitation, not open the beta on the old alpha build. [decisions.log l2866]
- Your test for the beta: "we are fully tracking anything that we know isn't working yet". It produced a label for fixes that are on main but not yet on the served build. [decisions.log l2877, l2878 (log)]
- The MVP milestone closed that afternoon on your Go.

**6. Oct 31: the version gets a name.**
- "officially 0.9.0.0 (tag v0.9.0.0), and conversationally 0.9". [decisions.log l2911 (log)]
- 1.0 is the Production release, "cut when the Production milestone closes and Piper formally leaves beta". [decisions.log l2913 (log)]

## Careful with these (accuracy)

- **Big overlap with "At Long Last, Beta" (11-07).** It already tells the Aug 8 quote, the Sep 6 reset to Oct 30, "MVP closed right on schedule", "trickier than it looks", "We can all catch our breath", the 0.9.0.0 cut and the known-issues letter. Don't reuse those quotes as the climax. This post's untold side is the reasoning inside the gate: how an issue got on or off it, why option B after the privacy find, and why 0.9.0.0.
- Also told: the Oct 20 stall ("Build the Instrument Before the Theory"), Oct 22 to 23's accuracy run ("When Accuracy Scores Worse"), and the counts in Ships #066 to #068.
- **Oct 29 didn't "fail".** It ran out of day. Oct 30 was the hard stop.
- **Go time:** relayed 17:03, and a later omnibus line has 17:51. Say "that afternoon".
- **"Beta opens Oct 31":** the letters went out by early afternoon, before the first 0.9.0.0 build was served and before the tag (22:01, after a regression held it). You signed up for the beta yourself on Oct 30.
- **Alpha vs beta invitations:** the overdue alpha invitations went out Oct 26. The beta ones are what waited.
- No outside names. The Oct 30 conference talk is yours. Name no one from it.

---

*Next on Building Piper Morgan: [TEASE: the next non-Ship post. On the calendar today that is Sat 12-05 "A Record Is Not a Delivery" (tentative). Needs your final title before this goes to Docs.]*

*[Reader question, yours to write. A start: "When you last called something ready, what was the test, and was it written down?"]*
