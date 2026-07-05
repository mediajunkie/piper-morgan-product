---
image: 'ai-gardener.png'
alt: 'A gardener gently removes the support stakes from a young tree that has grown strong enough to stand on its own, while several small glowing AI companions carefully coil the ropes, take notes, and neatly stack the retired stakes, symbolizing a successful practice whose lessons endure after the implementation is retired.'
caption: '"I think we''re ready!"'
---

# The Practice That Got Retired

*May 17–21, 2026*

For three or four days in mid-May, a small set of role-named agents in my project tried a new practice, part of what I have started calling a "duty cycle." Each agent set up a small recurring job that fired on an hourly schedule, checked the agent's mailbox for new arrivals, ran a quick categorization on what it found, and appended the result to a running log. 

The chief innovation officer (CIO) role adopted the practice first. The documentation manager role (Docs) followed the next morning. Our role that oversees support for all agents and people in the system, known as HOST (Head of Sapient Trust), came on within the day. Three agents, each running the same shape on its own schedule.

The practice was orderly. The logs were clean. The hourly fires landed reliably. The categorization worked. Mail that needed to surface to me surfaced. Mail that didn't, didn't.

Then I retired the practice.

# Why I shelved the first duty-cycle design

The initial test proved the concept but I'd been thinking about a substantively different design. The first version was focused on the mail-checking loop. The new design called for three composing loops (mail, tasks, and a flywheel orchestrator stitching them), three per-agent documents tracking different things (active work, queued items, attention state), an explicit idle state to make "nothing's blocking me" a first-class concept rather than the absence of work, and day-bookended start-and-stop rituals to give each agent's day a frame.

# What the proof of concept established

Each of the role-named agents who ran the practice surfaced something valuable during those days. The CIO suggested refinements to the append-only log architecture — what got logged, how the log was structured, where the friction was. Docs proposed parsing refinements on inbound memo headers — what tolerances made the categorizer brittle, what made it robust. HOST recommended a small set of flag-adoption variations to inform how the richer design would handle agent-specific behaviors.

Those refinements all came from running the practice and watching where it scraped. I can sketch out my ideas all day long but trying them out is where I find out how to make them work better.

By the time I was ready to retire it, the methodology entries that came out of those days were already in the catalog. They survived the retirement. The implementation died. The understanding stayed.

# Failing faster

The first interpretation of my duty cycle idea got rolled back but it was the training-material version of the richer design that came next. That wasn't necessarily my intention. I'll take a one-shot solution as fast as anyone, if it works. 

I shipped it because it was a sensible shape and I wanted to see how it would operate. The next version benefited from the understanding the small version produced.

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
