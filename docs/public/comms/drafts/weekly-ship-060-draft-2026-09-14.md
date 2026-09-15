---
image: 'piper-ship.png'
alt: 'A child and a crew of robots checking each other''s work on a boat.'
caption: ''
---

# Weekly Ship #060: Four bugs, one contract

*September 4 – 10, 2026*

Twenty-six issues closed this week, eighteen of them against the MVP milestone. Most of them came from one place: sitting down with the product and using it.

The week's best single result is small to describe and took two days to find. Four separate bugs — a standup that acted on a question, a confirmation that fired on an aside, an offer that ignored a plain "yes," a reminder chain that could not consume its own consent — turned out to be one mechanism failing in opposite directions. Fixing the mechanism closed all four.

---

# 🚀 Shipped this week

## ⚙️ Engineering & architecture

**The acceptance contract.** Live testing produced four defects that read as unrelated. One accepted a question as consent and marked something done that nobody asked for. Another fired a delete on a sentence that merely began with "please." A third ignored an unambiguous "yes" and asked the user to retype the command. Written down side by side, they were the same contract failing in both directions at once — **simultaneously too permissive and too strict**, which is not a threshold problem. Lead built a single predicate with an adoption ratchet, and three of the four closed together.

**Two security issues, both closed before the first outside tester.** One was a settings page that looked user-scoped and actually rewrote a shared global file, so any saved preference replaced everyone else's. The other was a chat rendering path with no sanitizer at all. The second fix also turned up two things nobody was looking for — the file named in the report was an unserved duplicate, and there was a fourth injection point outside the original inventory.

**The files feature works end to end again.** Document upload had been failing on every attempt since mid-August, which blocked testing the entire feature family behind it. Upload works, and asking for a summary of an uploaded document now finds the document.

**Times are your times.** Per-user timezone landed. Asking for a reminder at 6am now means 6am where you are, not 6am UTC — a fix whose absence had been quietly firing reminders seven hours early.

**Six smaller repairs, all found by using the product**: project names now survive politeness and quotation marks, spelled-out durations like "in two hours" work as well as digits, issue titles carry the subject rather than the raw command, the phrase the assistant teaches you for filing an issue now actually files it, a draft that is given a subject and description uses them, and a standing set of test failures that had been corrupting unrelated tests is gone.

**A router contract that had never existed.** The GitHub operations layer was called through an interface nobody had written down, so nine of fourteen operations had no implementation behind them and would fail only when reached. That contract is now typed and enforced, six dead methods were deleted rather than implemented, and the build fails if the surface drifts from it again.

## 🎯 Product & experience

**A cold user now meets a question rather than a greeting.** The first-contact experience for someone with nothing connected had been an ordinary hello. It now opens with a question about what is actually on their mind. This one shipped behind a flag, held for a week under a deliberate freeze, and went live when the reasoning behind the freeze turned out to rest on a premise that was no longer true.

**A promise we could not keep was cut rather than softened.** Reviewing the new first-contact copy, CXO found a line promising the assistant would remember and bring something back later. The mechanism for that does not exist — the write path has no callers. The line was removed rather than reworded.

**A capability catalog that says what is visible to others.** Filing an issue, commenting, and closing all land in front of other people. The list that describes what the assistant can do now distinguishes those from private actions.

## 🔬 Methodology & process innovation

**The work queue had no intake from the product backlog.** The duty cycle read an agent's mail and their own task list, and nothing else. So "there is no work" and "thirty-five unstarted issues" were true at the same time, and nobody was wrong. The queue now draws from three sources rather than one.

**A full review of the practice layer, kickoff to ratification in three working days.** Seven independent reads returned the same day, then a challenge round produced five accepted amendments — including two catches where the synthesis claimed a mechanism was enforced when the evidence said only that it existed. The instruction driving it was *refactor, do not add*: four candidate additions were folded into existing practices rather than appended.

**The backlog got a shape.** An audit of 435 issues found six recurring causes underneath the symptoms, three of which turned out to be half-modeled rather than unmodeled — a convention where a contract was needed. Those became the boundaries for an ordered set of epics. The first real test of it worked: three issues predicted to share a fix did.

## 🌍 External relations & community

**Three pieces published:**

- Sep 5: "[We Built Onboarding in Our Own Image](https://pipermorgan.ai/blog/we-built-onboarding-in-our-own-image/)" — insight
- Sep 8: "[More Than Anyone Ever Reported to Me](https://pipermorgan.ai/blog/more-than-anyone-ever-reported-to-me)" — building
- Sep 9: [Weekly Ship #059: The Verifier Is Not Exempt](https://pipermorgan.ai/shipping-news/weekly-ship-059-the-verifier-is-not-exempt) — shipping news

[![Three luminous AI agents celebrate an empty sheep pen while a startled human discovers most of the flock—and several escape routes—outside their counting gate.](https://pipermorgan.ai/assets/blog-images/more-than-anyone-ever-reported-to-me.webp)](https://pipermorgan.ai/blog/more-than-anyone-ever-reported-to-me)
*"Did anyone check outside the pen?"*

**A publishing defect fixed at the source.** A near-duplicate post was caught before it ran, traced back to a June rename that had actually been a copy without a delete. The drafting process now checks whether an orphaned draft is a fork of something already published, which closes the class rather than the instance.

## 📊 Governance & operations

**Metrics (Sep 4 – 10):**

- **Issues closed:** 26
- **Against the MVP milestone:** 18
- **Deployed:** four releases
- **Published:** 3 pieces, no missed slots
- **Completed to date:** 1,133

**Every open issue now carries a milestone**, for the first time. Work filed without one had been invisible to every progress number we report, which meant our own counts quietly excluded whatever had just been discovered.

---

# 🎯 Coming up next week

The first outside tester's invitation, held deliberately until a credential issue found in the same week was not just fixed but observed to be fixed. The remaining half of the continuous-integration work, where six workflows are green and one is not. And the ordered epics get their first full week as the thing the build queue actually reads from.

---

# 🚧 Blockers & asks

Verification capacity remains the honest constraint, and this week put a number on it: eighteen milestone issues closed, and the large majority moved because someone sat down and used the product rather than because a test suite went green.

---

# 🔎 This week's learning pattern

## Four symptoms, one contract

**Discovery**: when several defects are reported separately, the thing they have in common is often a contract nobody wrote down, and the symptoms will look unrelated until you put them beside each other.

**Example from this week**: a standup that acted on a question, a delete that fired on an aside, and an offer that ignored a plain "yes." Filed on different days against different surfaces. Read together, they were one acceptance mechanism that was too permissive and too strict at the same time — which is the tell, because a threshold problem cannot fail in both directions at once.

**Why it matters**: fixed individually, each would have been a small patch and the next symptom would have arrived next week. Fixed as a contract, three closed together and the fourth became a named, bounded piece of work. The same pattern held at larger scale — an audit of the backlog found six causes under dozens of issues, and the first prediction it made turned out to be right.

**Application beyond this week**: before fixing the third instance of anything, put the instances side by side and ask what single thing would have to be true for all of them. If the answers point in opposite directions, you are looking at a missing contract rather than a badly tuned one.

**Related patterns**: this is the practical half of the previous weeks' theme. Check the source rather than the summary, then a checked claim has a shelf life, then the check is a claim too — and now: the symptoms are not the thing.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #060. Previous: [#059 "The Verifier Is Not Exempt"](https://pipermorgan.ai/shipping-news/weekly-ship-059-the-verifier-is-not-exempt).

*P.S. The self-correction habit this project has been building kept paying out — most of the week's sharpest catches were people finding their own errors before anyone else did, and several published them against themselves the same day. It has stopped being remarkable, which is the point.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of September 4 – 10, 2026 | Phase: Alpha testing, beta-gate preparation**
