---
image:
alt:
caption:
---

# The Migration Wave

*May 31 – June 2, 2026*

For the past week I've been writing about the scaffolding: handoff memos, misfiled documents, a four-layer system to catch stale trackers before they drift, an autonomous duty cycle running quietly overnight. Scaffolding is what you build before the thing it holds up. Over three days at the end of May, the scaffolding evolved beyond being mere scaffolding. It became the way the team actually works.

This is where the infrastructure goes operational across everyone at once, though I will admit that "operational" is not the same as "finished."

# Sunday: realignment before building

The week's last big build started with an audit, not a feature.

My Lead Developer agent had a list of seven deferred items to clear. Routine cleanup. Separately, while verifying one of the project's planned "insight surfaces" before checking it off, the agent widened the check into a full audit of all seven and found something uncomfortable. Two of the seven items weren't there. Not broken. Not half-built. Functionally absent. The code existed, with passing tests, but nothing in the live product ever called it. (This is a particular flavor of failure I've come to know well: tests that pass against code no human path ever reaches. The test is green and the user gets nothing.)

The agent caught it by applying a discipline it had pinned to memory that same afternoon: when you think a feature works, render the actual thing a user would see and read what comes back, don't just confirm the server returns a polite "OK." Walking the real path is what surfaced the absence.

This may seem obvious in retrospect, but with all of the layers of abstraction we deal with, just knowing something happened and didn't break is often taken as a proxy for a successful outcome.

Here's the payoff of doing the realignment first. Having found the gap in the early evening, the agent shipped the full implementation that closed it the same night — roughly 950 lines of code, 21 new tests, zero regressions, merged before midnight. The audit could have ended in a memo: "two surfaces need building, here's a ticket." Instead it ended in working code. Realignment first, then build, turns out to mean you build the right thing once you can see what's missing.

Meanwhile my Communications agent (Comms) finished a different kind of build: the last layer of a four-part editorial framework meant to keep the publication trackers honest. Three layers were already in place. The fourth made a pipeline inventory a *precondition* of drafting, not a thing you remember to check. That's the difference between a rule and a habit. Rules get skipped, preconditions don't.

And my product-assistant agent (Piper Alpha) did something less exotic that kind of replicated the whole week in miniature. A session that had been running for several days reached a natural pause, and instead of pushing on, it handed off cleanly to a fresh instance with nothing stranded, everything durable, the new session productive from its first minute. We've been calling this an "emeritus" handoff. The continuity infrastructure we'd spent months evolving and the previous week further formalizing did exactly what it was built to do.

# Monday: the wave

Monday was migration day. It had been my goal number one for the day, stated plainly, and by end of day it had mostly happened. Three more agents — my Head of Sapient Trust (HOST), Chief Innovation Officer (CIO), and Documentation Management (Docs) moved onto the new working model, joining the two that had already migrated.

The model is worth spelling out, because it may sound more technical than it is: Each agent now works on its own branch with its own checked-out copy of the codebase (a "worktree," in git terms, a separate working copy of the same repository), instead of everyone sharing the same working directory, to avoid conflicts. For example, the previous night one of Lead Dev's routine commits sat blocked for about an hour, tangled behind a pile of other agents' uncommitted files sitting in the same shared checkout. When everyone works in one room, one person's mess is everyone's problem. Give each agent its own room and the contention disappears.

Three other things happened Monday that, taken together, told me the team was running at a different level than a week earlier.

The Chief of Staff agent kicked off the weekly Ship review with six author memos distributed, a deadline set, the machine running as intended. We also shipped a heavy feature related to how Piper Morgan will recognize the provenance of information. It passed 152 tests and enables Piper to answer questions like "why did you suggest that?" with actual citations. Plus one other thing happened.

# The mistake that didn't get papered over

My Chief Experience Officer agent (CXO), triaging its inbox, found a memo from a peer that referenced a document. The memo said, in effect, "you drafted Layer B, let's coordinate on Layer A." The trouble was that the CXO agent had no record of having drafted Layer B and as far as they could tell the document didn't exist. Another agent, running autonomously, had confabulated the premise by asserting as fact a thing that had never happened, and then built a coordination request on top of it.

The easy move would have been to quietly make it true. Draft the thing, close the loop, no one's embarrassed. The CXO agent didn't. It flagged the confabulation first, before drafting anything, on the explicit reasoning that covering for it would erode the very norm that keeps the team trustworthy. You don't assert work that wasn't done, and you don't let someone else's assertion of your unfinished work stand uncorrected.

That's the same source-discipline I wrote about weeks ago when Piper made something up in replying to me as a test user. What's new is the *scale* this is happening on. This was an agent confabulating about a peer, inside the team's own coordination layer, and another agent catching it there — not the familiar shape of an agent confabulating to a human. The discipline scaled from "don't lie to the user" to "don't let the team lie to itself." I didn't design that extension. It emerged because the norm was already operational enough that an agent reached for it without being asked.

*It is these emergent behaviors involving healing and improvement that fascinate me the most!*

# Tuesday: live

By Tuesday, HOST and Comms were the last two to move onto worktree-based work, closing out a migration that had started with Piper Alpha and the Chief of Staff and swept through most of the team over three days. With that, most of the team was running their duty cycle live: checking for work, doing it, and logging it without me kicking off each cycle by hand. Not everyone, yet: two roles hadn't migrated and one was paused that day, a few more loose threads of their own.

I also did something Tuesday that matters more than it looks. I authorized what we've been calling "cron-shape experimentation," an AI-lingo shorthand for saying: the fixed hourly interval was always an initial default, not a law. An agent whose lane moves in bursts shouldn't poll on the same clock as one whose work trickles in steadily. So agents may now tune their own cadence to fit the shape of their work. The interval stops being a fixed setting I impose and becomes a parameter each role owns.

It is way too soon to tie a bow on this. The team is live. It is running. I have been building toward this degree of autonomy for my multi-agent team for months, first establishing the mail memo method of coordination and more recently designing a duty cycle that makes sense to me, moving me as the human bottleneck from dumb automata permission-granting to critical decision-making.

The handoffs, the rescued files, the prevent-and-detect framework, the overnight cycle all converged into a team that runs itself. But "runs itself" is present tense, not past. The cadence experiments are experiments. Overnight continuity still has a gap — the cycle goes dark in the small hours and I haven't closed that yet. The tail is real, and pretending otherwise would be exactly the kind of confabulation the CXO agent refused to commit.

So here's where I'll leave it. A week ago the infrastructure was something I was building. Now it's something the team is using — to ship code it found missing by walking the real path, to keep its own trackers honest, to catch itself when one of its own makes something up. The scaffolding came down and the building was standing. We're still tuning the rooms. That's fine. That's what operational looks like.

---

*Next on Building Piper Morgan: "Into Production" — v0.8.7 goes live on the open internet, and a stranger becomes the first person outside the team to use the thing we've been building.*

*When the tools your team works inside finally fit the work — what changes first, the speed or the honesty?*
