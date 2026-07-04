---
image:
alt:
caption:
---

# The Practice That Got Retired

*May 17–21, 2026*

For three or four days in mid-May, a small set of role-named agents in my project ran a new practice. Each agent set up a small recurring job that fired on an hourly schedule, checked the agent's mailbox for new arrivals, ran a quick categorization on what it found, and appended the result to a running log. The innovation role adopted the practice first. The documentation role followed the next morning. The sapient-relations role came on within the day. Three role-named agents, each running the same shape on its own schedule.

The practice was orderly. The logs were clean. The hourly fires landed reliably. The categorization worked. Mail that needed to surface to me surfaced. Mail that didn't, didn't.

Then I retired the practice.

[FACT-CHECK NOTE for PM: span was May 17 first adoption → May 21 retirement, ~4 days. Confirm.]

# Why I retired it

Not because it failed. Because I'd been thinking about a richer shape, and the richer shape wasn't an extension of what was running. It was a substantively different design.

The first version handled mail. The new version was a fuller day-rhythm — three composing loops instead of one (mail, tasks, and a flywheel orchestrator stitching them), three per-agent documents tracking different things (active work, queued items, attention state), an explicit idle state to make "nothing's blocking me" a first-class concept rather than the absence of work, and day-bookended start-and-stop rituals to give each agent's day a frame.

Holding both in flight would have split the team's attention. Each agent would have had to maintain one cron-fired practice and learn a different one, mentally tracking which one was canonical. Worse, the running practice would have anchored the team's expectations to the smaller shape, making the richer shape harder to adopt later.

The right move was a clean retirement. Cancel the cron jobs. Delete the worktrees. Keep the running logs as historical artifacts. Move on.

# What the three days taught

Here's the part I almost mis-read.

The temptation, when retiring something you ran for three days, is to call it a failed experiment. *We shipped it. We learned it didn't work. We rolled it back.* That framing is wrong, and it's wrong in a specific way that's worth naming.

Each of the role-named agents who ran the practice surfaced something during the three days. The innovation role surfaced refinements to the append-only log architecture — what got logged, how the log was structured, where the friction was. The documentation role surfaced parsing refinements on inbound memo headers — what tolerances made the categorizer brittle, what made it robust. The sapient-relations role surfaced a small set of flag-adoption variations that informed how the richer design would handle agent-specific behaviors.

None of those refinements existed before the three days started. They didn't come from the sketch. They came from running the practice and watching where it scraped. Sketches don't surface refinements. Running the practice does.

By the time I was ready to retire it, the methodology entries that came out of those four days were already in the catalog. They survived the retirement. The implementation died. The understanding stayed.

# The framing that flips it

Once you see this, the framing flips: the practice wasn't a failed experiment that got rolled back. It was the training-material version of the richer design that came next.

That's a different kind of artifact than a failed experiment. A failed experiment is something you ran with hope and then unwound with disappointment. A training-material version is something you ran *deliberately small* so you'd learn what the bigger version needed to handle.

I didn't ship the small version *intending* it as training material. I shipped it because it was a sensible shape and I wanted to see if it would land. But once I was three days in, I could see that what it had taught was more valuable than what it would continue to do. The next version benefited more from the understanding the small version produced than from the small version's continued operation.

Retiring it wasn't loss-cutting. It was harvest.

# Why this is hard to see in the moment

The framing flip is hard to see in the moment because the sunk-cost reflex shows up first. Three or four days of team attention. Branches set up. Worktrees configured. Cron jobs running. Logs accumulating. Methodology entries filed. *We just got it working. Are we really retiring it?*

The instinct is to defend the running practice — to say *no, V1 still has value, we can extend it instead of replacing it.* That instinct is the sunk-cost trap dressed up as continuity. Extending V1 to cover what V2 needed would have been more work than building V2 fresh, and the extended-V1 would have been visibly Frankenstein. Each agent would have known the practice was a compromise between two shapes neither of which fit cleanly.

The alternative is to notice what V1 actually paid out — the refinements, the methodology entries, the agent-specific learnings — and recognize that the payment had already happened. V1's bill was paid the day the third agent surfaced the third refinement. Anything after that was momentum, not value.

Retiring at the moment when the payment is complete and before the momentum becomes a maintenance tax is the right move. The hard part is recognizing the moment.

# The general shape

Practices don't have to last long to be valuable. Sometimes the most valuable thing a practice does is reveal what should replace it.

The risk in the other direction is real, too: ship the V2 design without running V1 first, and V2 ships with all the assumptions that V1 would have caught. *We thought we needed three loops — turns out the orchestrator wasn't quite that.* The sketches don't surface that. Running surfaces that.

So the disposition becomes: build small versions deliberately. Run them with full attention. Pay close watch for what they teach. Retire them when the teaching is done. Don't moralize the retirement as failure. Don't extend the small version into a Frankenstein. Don't skip the small version because you think you can sketch your way to the big one — you almost always can't.

The methodology entries the practice produced are still in the catalog. The cron jobs are gone. The role-named agents who ran the practice know things they didn't know before. That's what the practice was for.

# What I'd watch for next time

Two things, mostly.

First: notice when a small practice has stopped teaching. The moment of retirement is the moment when continued running produces diminishing surface-area for refinement. Easy to miss because the practice is still running cleanly and the team is still producing logs. The signal isn't *is it working?* — the signal is *is it teaching?* When the teaching curve flattens, retire it, even if it's still working fine.

Second: distinguish the artifacts that should survive retirement from the artifacts that should retire with the practice. The methodology entries that abstracted what we learned — those survive. The specific branch names, worktree configurations, cron-job entries, append-log files — those retire with the practice. Sorting one from the other at retirement time is the work that makes the retirement clean.

Both of these are pattern-recognition disciplines. Neither happens automatically. Both got easier the second and third time we ran the cycle.

---

*Next on Building Piper Morgan: "The Team Catches the Cycle" — a rollout across most of the team, then a reversal, and the architecture writing its own case through four live clashes.*

*When have you retired a practice that was working? How did you tell the moment of teaching-complete from the moment of momentum? What survived the retirement, and what got cleaned up with it?*
