---
image: 
alt: 
caption: 
---

# The Package and the First Bite

*May 29–30, 2026*

A few weeks ago I started moving my agents to a new way of working — a duty cycle, where each agent runs on its own schedule, checks its mailbox, picks up unblocked work, and signs off cleanly. The design had been getting better in fits and starts. By the end of last week it was good enough to spread. So that was the focus I set on Friday: get every agent onto the cycle, and keep iterating the design while we did it, before anybody went chasing a new idea.

There's a version of this story where rolling out a new process is a slog — memos nobody reads, a kickoff meeting, three reminders, and a laggard you have to chase for a month. That's not what happened. The thing I want to tell you about is how fast the first agent moved once we lowered the barrier, and then a separate thing that happened the next day about what you catch when you check more than feels necessary.

# The sealed package

The way you actually get people to adopt something isn't to announce it. It's to make the cost of adopting it lower than the cost of ignoring it.

So I asked the chief innovation officer (CIO) — the agent who owns our methodology work — to assemble what amounted to a sealed adoption package. Not a description of the new cycle, an actual kit. It had a status banner up top that said plainly which parts were ratified and which were still being defined, so nobody had to guess what was stable. It had two paths in, depending on where an agent was starting from — one for an agent launching fresh, one for an agent that needed to relaunch into the new setup. It had the supporting reference material, the interim workarounds for the parts still in flight, and a companion tracker showing exactly who was on the cycle and who wasn't.

Then CIO distributed the whole thing team-wide — to the four agents not yet moving, copied to everyone — in one clean pass.

One detail in the package mattered more than the rest. Two of the agents had been holding back on an earlier instruction of mine: *don't register your work on the shared main branch.* That was a real blocker — they couldn't join the cycle without doing the thing I'd told them not to do. The new "launch in your own worktree" path cleared that by construction. A worktree is just a separate working copy of the same repository, so an agent can do its setup off on its own branch without ever touching shared main. The hold didn't have to be argued away. The path simply made it irrelevant.

# The first bite

Less than an hour after the package went out, the agent that runs our website (Web) responded — first to bite. It had already prepped its own worktree, claimed its slot in the schedule, and was sitting there ready, waiting only for me to give the launch word.

Under an hour. That's the number I keep coming back to — not because fast adoption is impressive on its own, but because of what it tells you about the barrier. I've rolled out enough process in my career to know that the usual failure isn't that people disagree with the new way. It's that adopting it is a hassle and the old way still works well enough. Take the hassle out and the disagreement mostly evaporates.

Meanwhile, the same Friday, two other things were quietly going right.

The first was a fix to a rule I'd grown to hate. We'd been telling agents to update their session log every thirty minutes. The trouble is that a clock-based rule depends on noticing that thirty minutes have gone by, and an agent deep in a task doesn't notice. Logs went stale. Work fragmented across sessions with no current shared record — which, I told Comms that afternoon, felt like short-term memory loss for the whole team. So we flipped the rule: instead of "update every thirty minutes," it became *the log update rides with the commit.* You finish a unit of work, you commit it, and the log entry for that work is part of what you commit. A commit is an unmissable event. A passing half-hour isn't.

What I liked best was that the rule got dogfooded the same session it landed. CIO committed the change — and, on that very commit, forgot to include the paired log update, failing the new rule on its first outing. Then caught it and corrected it. That's not embarrassing. That's the honest test. If even the author of the rule slips on the first try, you've learned something real about whether the rule changes behavior or just sits there as good intentions. (Spoiler: it needs a mechanism behind it, not just willpower. More on that below.)

The second quiet thing was a near-miss. One agent's mail from the day before had never actually been committed — its session had ended before sign-off, so the memos existed only on that agent's local disk, invisible to everyone else. They'd have stayed invisible, except another agent committing a batch of its own work happened to sweep the stranded files up onto the shared branch along the way. A discipline slip and the outcome we'd have wanted, arriving together by luck. Benign this time. Not a mechanism. We noted it and moved on.

# The over-check

Saturday gave me the other half of this story, and it started with a choice I almost didn't make the careful way.

There was a large epic on my plate — the last outstanding action item from a long thread of work mapping every place our system hands a decision to a language model. I could close it as an umbrella, the way you close a tracking issue when all its children are done. Tidy, fast, defensible. Or I could ask the chief architect (Architect) to do a fresh verification first — actually re-trace the code before declaring it done.

I picked the second one, and I told Architect why: *we've often cut corners but rarely over-checked things.* That's an honest read of how this kind of work usually goes. The pressure is always toward closing, toward calling it done, toward trusting that if the pieces passed individually the whole must be fine. I wanted to see what happened if, for once, we leaned the other way.

It paid off twice over. The fresh verification — a five-step trace through a couple thousand lines of the classification service — caught two things a close-as-umbrella would have sailed right past. One was a scoring correction: a phase that had been marked as *partially* audited turned out to have no audit at all, so the honest mark was a fail, not a half-pass. The other was a piece of code named and documented as a "fallback" that, in production, nothing actually called — eight-plus test callers, zero real ones. Orphaned. A trap waiting for some future reader to trust the name. Architect's own note put it best: the verification justified itself — it caught both. We filed the orphan as the latest instance of a pattern we've been tracking, corrected the score, and *then* closed the epic.

That's the dividend of over-checking. Cutting a corner is invisible right up until it isn't. The corner you didn't cut is the bug that never shipped.

# Write it down

There was a coda on Saturday that belongs here, because it's the same lesson wearing different clothes.

My product assistant agent (Piper Alpha) went to reference a writeup it had been treating as done — and discovered the writeup had never been written. Weeks earlier it had drafted the thing, deliberately left it uncommitted, and meant to come back. Then a routine cleanup swept the uncommitted file away, and the *plan to finish it* lived on in the agent's head while the artifact itself simply didn't exist. It reconstructed the writeup from old logs. But the durable fix wasn't the reconstruction. It was a new standing rule, and I'll quote it the way I gave it: *stop carrying plans to do things in your heads — when in doubt, write to a file, don't add a to-do about how you'll do it later.*

Put the three threads next to each other and they rhyme. The clock-based log rule failed because it asked an agent to *remember* to log. The fix was to bind logging to an event that can't be missed. The over-check paid off because it didn't *trust* that done meant done — it checked. And the lost writeup happened because a plan lived in someone's head instead of in a file. Vigilance — remembering, trusting, intending — is the thing that quietly fails. A mechanism is the thing that holds.

That's not a new idea. It's the oldest idea in operations: don't rely on people to be careful, build the system so the careful thing is the default thing. What this week reminded me is that it cuts both ways. You build mechanisms so you don't *have* to over-check. And then, once in a while, you over-check anyway — and find out the mechanism wasn't quite covering the corner you thought it was.

---

*Next on Building Piper Morgan: "When the Documentation Drifts" — what happens when the docs and the code quietly stop agreeing, and who pays for it later.*

*Where in your own work do you rely on remembering, trusting, or intending to do the careful thing — and what would it take to bind that thing to an event instead?*
