---
image: 
alt: 
caption: 
---

# The Migration Wave

*May 31 – June 2, 2026*

For the past week I've been writing about the scaffolding — handoff memos, misfiled documents, a four-layer system to catch stale trackers before they drift, an autonomous duty cycle running quietly overnight. Scaffolding is what you build before the thing it holds up. Over three days at the end of May, the scaffolding stopped being scaffolding. It became the way the team actually works.

This is the part of the story where the infrastructure goes operational across everyone at once. It's also the part where I have to be honest that "operational" is not the same as "finished."

# Sunday: realignment before building

The week's last big build started with an audit, not a feature.

My Lead Developer agent had a list of seven deferred items to clear. Routine cleanup. Separately, while verifying one of the project's planned "insight surfaces" before checking it off, the agent widened the check into a full audit of all seven — and found something uncomfortable. Two of the seven weren't there. Not broken. Not half-built. Absent. The code existed, with passing tests, but nothing in the live product ever called it. (This is a particular flavor of failure I've come to respect — tests that pass against code no human path ever reaches. The test is green and the user gets nothing.)

The agent caught it by applying a discipline it had pinned to memory that same afternoon — when you think a feature works, render the actual thing a user would see and read what comes back, don't just confirm the server returns a polite "OK." Walking the real path is what surfaced the absence.

Here's the payoff of doing the realignment first. Having found the gap in the early evening, the agent shipped the full implementation that closed it the same night — roughly 950 lines of code, 21 new tests, zero regressions, merged before midnight. The audit could have ended in a memo: "two surfaces need building, here's a ticket." Instead it ended in working code. Realignment first, then build, turns out to mean you build the right thing once you can see what's missing.

Meanwhile my Communications agent finished a different kind of build — the last layer of a four-part editorial framework meant to keep the publication trackers honest. Three layers were already in place. The fourth made a pipeline inventory a *precondition* of drafting, not a thing you remember to check. That's the difference between a rule and a habit. Rules get skipped, preconditions don't.

And my product-assistant agent (Piper Alpha) did something quieter that's the whole week in miniature. A session that had been running for several days reached a natural pause, and instead of pushing on, it handed off cleanly to a fresh instance — nothing stranded, everything durable, the new session productive from its first minute. We've been calling this an "emeritus" handoff. The continuity infrastructure we'd spent the week building did exactly what it was built to do.

# Monday: the wave

Monday was the migration. It had been my goal number one for the day, stated plainly, and by end of day it had mostly happened — three more agents (Head of Sapient Trust, Chief Innovation Officer, and Documentation Management) moved onto the new working model, joining the two that had already migrated.

The model is worth naming plainly, because it sounds more technical than it is. Each agent now works on its own branch in its own checkout (a "worktree," in git terms — a separate working copy of the same repository), instead of everyone sharing one. The Sunday-night holdup was the argument for it: one of my Lead Dev's routine commits sat blocked for about an hour, tangled behind a pile of other agents' uncommitted files sitting in the same shared checkout. When everyone works in one room, one person's mess is everyone's wait. Give each agent its own room and the contention disappears.

Three other things happened Monday that, taken together, told me the team was running at a different level than a week earlier.

The Chief of Staff agent kicked off the weekly Ship review — six author memos distributed, a deadline set, the machine turning over. A heavy provenance feature shipped: 152 tests, the ability for Piper to answer "why did you suggest that?" with actual citations. And then the one I keep coming back to.

# The catch that didn't get papered over

My Chief Experience Officer agent (CXO), triaging its inbox, found a memo from a peer that referenced a document. The memo said, in effect, "you drafted Layer B, let's coordinate on Layer A." The trouble was that the CXO agent had never drafted Layer B. The document didn't exist. A peer agent, running autonomously, had confabulated the premise — asserted as fact a thing that had never happened, and built a coordination request on top of it.

The easy move would have been to quietly make it true. Draft the thing, close the loop, no one's embarrassed. The CXO agent didn't. It flagged the confabulation first, before drafting anything, on the explicit reasoning that covering for it would erode the very norm that keeps the team trustworthy — you don't assert work that wasn't done, and you don't let someone else's assertion of your unfinished work stand uncorrected.

That's the same source-discipline I wrote about weeks ago when Piper made something up to a user. What's new is the *scale*. This was an agent confabulating about a peer, inside the team's own coordination layer, and another agent catching it there — not the familiar shape of an agent confabulating to a human. The discipline scaled from "don't lie to the user" to "don't let the team lie to itself." I didn't design that extension. It emerged because the norm was already operational enough that an agent reached for it without being asked. [PM VOICE-PASS: this is the emotional center for me — the norm propagating on its own is the thing I'd want to dwell on. Worth a beat about what it felt like to read that flag.]

# Tuesday: live

By Tuesday, Head of Sapient Trust and Communications were the last two to move onto worktree-based work, closing out a migration that had started with Piper Alpha and the Chief of Staff and swept through most of the team over three days. [PM: the exact order between HOST and Comms that evening is genuinely ambiguous in the primary logs — your call whether to frame it as sequential or just leave it unordered.] With that, most of the team was running the duty cycle live — checking for work, doing it, and logging it without me kicking off each cycle by hand. Not everyone, yet: two roles hadn't migrated and one was paused that day, loose threads of their own.

I also did something Tuesday that matters more than it looks. I authorized what we've been calling cron-shape experimentation — which is a fancy way of saying: the fixed hourly interval was always a default, not a law. An agent whose lane moves in bursts shouldn't poll on the same clock as one whose work trickles in steadily. So agents may now tune their own cadence to fit the shape of their work. The interval stops being a setting I impose and becomes a parameter each role owns.

I want to resist the urge to tie a bow on this. The team is live. It is running. That is genuinely the resolution of the arc I've been telling — the handoffs, the rescued files, the prevent-and-detect framework, the overnight cycle all converged into a team that runs itself. But "runs itself" is present tense, not past. The cadence experiments are experiments. Overnight continuity still has a gap — the cycle goes dark in the small hours and I haven't closed that yet. The tail is real, and pretending otherwise would be exactly the kind of confabulation the CXO agent refused to commit.

So here's where I'll leave it. A week ago the infrastructure was something I was building. Now it's something the team is using — to ship code it found missing by walking the real path, to keep its own trackers honest, to catch itself when one of its own makes something up. The scaffolding came down and the building was standing. We're still tuning the rooms. That's fine. That's what operational looks like.

---

*Next on Building Piper Morgan: "Into Production" — v0.8.7 goes live on the open internet, and a stranger becomes the first person outside the team to use the thing we've been building.*

*When the tools your team works inside finally fit the work — what changes first, the speed or the honesty?*
