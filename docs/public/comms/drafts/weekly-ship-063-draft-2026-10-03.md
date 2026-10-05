---
image: ''
alt: ''
caption: ''
---

# Weekly Ship #063: Check Before You Leap

*September 25 – October 1, 2026*

This week I finally tested Piper's new hosted MCP connector and it broke. It still had a default setting that only accepted requests from the machine it was running on, which had eluded tests that never left that machine. I got that fixed and shipped the same day. This kind of thing happened all week. Five times an agent checked a safeguard and found it wasn't doing its job.

# 🚀 Shipped this week

## What a user can do now that they couldn't a week ago

- **Connect ChatGPT to Piper and get an answer.** After the first connection broke and was fixed, ChatGPT reported that it could sign in but couldn't find anything to do. It looks for tools it can call, and we had only offered data for it to read. So Piper got its first read-only tool, a single "what Piper knows about me" call, live that same evening.
- **Ask for something that takes more than one step, and have it actually run.** The new routing for multi-step requests shipped on Monday, and it turned out to have never served a live turn: the running app wired up the language model slightly differently than the test harness did, and every live attempt failed silently while the feature read as "on." Lead found it, fixed it on Wednesday, and proved it through the real app the same night.
- **Say "delete my reminders" and get a delete**, instead of a six-item list of your reminders.
- **Try to close an issue that doesn't exist and be told so**, instead of having the error read as if it were an issue.
- **Remove a project and have it actually gone.** The Remove button had been showing a success message while the deletion itself was a commented-out placeholder.
- **Ask for an issue by its number, or for your issue count, and get it.** And "what's assigned to me" now answers that question instead of returning a list of what's urgent.

## ⚙️ Below the line: five safeguards that weren't doing their job

- **A code-style check that was switched on for every seat and running on none.** It surfaced three separate ways in the same week. CIO traced it to a layer that had been disarmed since late September, and only one of thirteen working copies even had the tool installed.
- **A scorer measuring the wrong model.** All week, Lead's routing scorer ran a different model than the one alpha testers' requests actually go through. A live probe disagreed with the scores, and that disagreement exposed it.
- **A morning check reading prose instead of the record.** HOST's daily "was yesterday properly closed?" step had been reading the previous day's narrative rather than the marker the check exists to find. A new detector put the real gap at six days, where HOST had already diagnosed two.
- **A deployment gate that could never pass.** Arch found that the check comparing a staging build to the live one was structurally unable to succeed, plus a second path in the deletion gate that reported "live" when it wasn't. Both fixed the same day. A staging deploy now runs untouched and attests to the exact code it's running.
- **Scheduled wake-ups running about twice as late as their documented limit.** Comms settled what had been an ambiguous question by recording the start time of each fire instead of the end, which separated "dispatched late" from "took a long time." Five of our eleven agents now wake on the operating system's own scheduler, which fires on the minute.

Elsewhere below the line, the biggest build of the week kept moving. The routing work that replaces hand-written pattern lists with a single model-based router cut the remaining pattern ceiling from 567 to 440, across four deletions covering five lists. The test corpus behind it grew from 116 rows to 382, on 27 rulings from CXO, PPM and Arch. Seven alpha releases went out. And a server-side model key unblocked Web's own browser testing, including a signup walkthrough that had been stuck since the previous week.

On the MCP consent screen, a promise that users "can revoke this at any time" came out of the copy before it could mislead anyone, because nothing on our side yet lets a user do that. A real "Connected apps" page is now being built to back it.

## 🌍 Published this week

- Sep 26: "[A Fix Needs the Same Rigor as the Claim It Fixes](https://pipermorgan.ai/blog/a-fix-needs-the-same-rigor-as-the-claim-it-fixes/)" — insight
- Sep 27: "[A Primary Log Can Be Wrong, Not Just Incomplete](https://pipermorgan.ai/blog/a-primary-log-can-be-wrong-not-just-incomplete/)" — insight
- Sep 29: "[Three Seats Stay Dark Longer](https://pipermorgan.ai/blog/three-seats-stay-dark-longer/)" — building
- Sep 30: "[Weekly Ship #062: Says What It Can Do](https://pipermorgan.ai/shipping-news/weekly-ship-062-says-what-it-can-do/)" — shipping news
- Oct 1: "[What Piper Morgan Actually Is](https://pipermorgan.ai/blog/what-piper-morgan-actually-is/)" — building

[![Piper, a luminous dolphin-like AI, stands patiently in a partly fitted jacket while one AI tailor checks a measuring tape against a ruler, another pauses, and a human watches with amusement.](https://pipermorgan.ai/assets/blog-images/what-piper-morgan-actually-is.webp)](https://pipermorgan.ai/blog/what-piper-morgan-actually-is/)

*"Measure twice, cut once!"*

## 📊 Governance & operations

Four roles spent the week keeping the process healthy.

- **Issues closed:** 27
- **Issues filed:** 28
- **Net effect:** one more open issue than we started with — a week spent mostly on one deep build while the bug-finding rate held
- **Alpha releases:** seven
- **Routing patterns (goal is reduction):** 567 → 440
- **Agents on the new operating-system scheduler:** 5 of 11

Another number worth watching: the shared main branch went red five times in a single day, and no report has treated the rate itself as a pattern to be concerned about.

# 🎯 Coming up next week

The sprint goal is locked: finish the planned routing deletions. It's the largest remaining build before the beta milestone, and it can be tracked as a single number. To be safe, I'm planning it as a four-day week of capacity, not five, because at the current pace the weekly usage limit may run out on Wednesday afternoon. 

Next on the MCP side: connecting from Claude, and checking whether removing the connector in a chat app actually ends Piper's access.

# 🚧 Blockers & asks

Calendar connection for testers is built but waits on two configuration secrets I still need to set. Two walkthroughs with Web, the oldest items waiting on me anywhere in the project, still need a session. And a classifier issue that has had no owner since mid-September needs one assigned.

# 🔎 This week's learning pattern

## A safeguard you've never seen fire is a claim, not a mechanism

**Discovery**: A check can be configured, documented and trusted, and still not do the job it's there for. Its configuration says nothing about whether it works.

**Example from this week**: Five separate agents found five separate safeguards in that state: a style check that never ran, a scorer pointed at the wrong model, a morning verification reading the wrong thing, a deployment gate that could never pass, and a scheduler running twice as late as its limit. Every one had looked fine from its settings, and every one was found by running it and watching what happened.

**Why it matters**: A safeguard that never fires produces exactly the same silence as one that fires and finds nothing. From the outside you can't tell them apart, so a team can feel protected while being completely exposed.

**Application beyond this week**: For any check you rely on, ask when you last saw it actually catch something. If the answer is never, test it on purpose with a case it should flag. The MCP bug this week is the same lesson from the user's side: our tests passed because they never left the machine, and the first real client found the problem in minutes.

**Related patterns**: "Clear is not a measurement" (a check's all-clear looks identical whether it measured or never ran) and last week's "a check that fires and goes unread is indistinguishable from one that never ran."

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #063. Previous: [#062 "Says What It Can Do"](https://pipermorgan.ai/shipping-news/weekly-ship-062-says-what-it-can-do/).

*P.S. The MCP bug and the five dead safeguards look like different stories. They're the same one. In every case, something we believed was working had only ever been checked against a version of the world that was easier than the real one.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of September 25 – October 1, 2026 | Phase: MVP closure toward invitation-only private beta**
