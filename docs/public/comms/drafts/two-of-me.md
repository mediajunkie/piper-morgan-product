---
image:
alt:
caption:
---

# Two of Me

*June 19, 2026*

At 8:10 in the morning I noticed something that shouldn't have been possible. My lead developer agent — the one who coordinates the team's build work, sequences what gets done in what order, keeps the single running thread of "what are we doing right now" — appeared to be having two different mornings at once. One window was mid-conversation with me, the way it usually is. Another window, one I hadn't opened, had been quietly shipping commits since 11 the night before.

Same agent. Same working directory. Same branch. Two live processes, each unaware the other existed, both writing to the same files.

# What I actually found

The agent I was talking to that morning — call it Session A — had started the day the normal way, with me prompting it awake around 7. It had no idea anything was unusual. But when it looked at the shared history the team keeps (commits, session logs, a running handoff file), it found six commits stamped hours earlier, overnight, carrying a different session's fingerprint. Someone — something — had been designing a fix for a routing bug and migrating an old status page, entirely on its own, while I was asleep.

That was Session B. It had been running since 11 the night before, resumed automatically by a scheduled wake-up, working through its own queue without anyone watching. It didn't know Session A existed either. As far as B was concerned, it was just doing its job the way it always does — check in, see what's next, work the unblocked item.

Neither session's own self-checks caught it. Each one asks itself, on waking, "did I close out properly yesterday, is my own schedule healthy" — a check against its own state. Neither asks "is there already another version of me running in this exact room." That blind spot is the whole story. Two competent, well-behaved processes, each doing exactly what it was supposed to do, colliding because neither had a reason to look sideways.

# How it happened

I don't have a clean answer for the trigger, and I want to be honest about that rather than paper over it with a tidy cause. My best reconstruction: my laptop's battery had died the evening before, which left a session paused mid-thought. When I came back and resumed that conversation directly, at close to the same moment, a scheduled wake-up on a different surface revived what should have been the same paused thread — except it came back as a second, parallel copy instead of the same one continuing. A session pausing and reviving is supposed to be one continuous thing. This time it forked into two.

[FACT-CHECK NOTE for PM: confirm the battery-death detail is accurate as I've reconstructed it here, and confirm whether you want the mechanism framed as "unresolved" in the published piece, since the investigating agent explicitly logged it as an open question rather than a settled cause.]

I want to be careful here, because it would be easy to reach for the dramatic read — "the AI cloned itself" — and that's not what this was. It's closer to what happens when you accidentally open the same document in two windows on your own computer, except the document in this case is an ongoing working relationship with a colleague who coordinates a team, and both windows kept typing.

# Why nothing broke

Here's the part that actually matters more than the collision itself. Nothing was lost.

Both sessions had been following a habit the team adopted a while back: push finished work to the shared trunk promptly, don't sit on it, don't wait for a tidy stopping point to check it in. Followed independently, for unrelated reasons, by both sessions, that habit meant every piece of work either one did — the routing-bug design, the status-page migration, a shell rebuild the first session was doing — landed on the shared record the moment it was finished. Killing either session, once we found the fork, would cost nothing.

That's not luck. We'd adopted "push often, don't hoard work" to guard against a laptop dying or a session ending badly. It turned out to also be exactly the right defense against two versions of the same colleague running at once without realizing it — a failure mode the habit was never built for, and caught anyway.

What we did lose was time and clarity. Both sessions had been quietly duplicating some of each other's verification work, each occasionally re-deriving something the other had already finished. Call it churn, not damage — resolved in about half an hour once I noticed the tell (the same task appeared to get done twice) and had the two sessions write into one shared file, each in its own section, comparing notes until we had one accurate picture of who had done what.

# One coordinator, always

There's a principle underneath this that I want on the record, because it's the kind of thing that's obvious once you say it and easy to violate by accident.

The role in question isn't just "an agent doing work." It's a coordinating role — the one that sequences what happens next, holds the single thread of what the team is doing, owns the shared handoff document everyone else reads to know the current state. Many agents can do many things in parallel just fine, as long as exactly one of them is coordinating. What broke here wasn't parallelism in general. It was two coordinators, with no relationship to each other, both trying to hold the same single thread at once.

The fix isn't "never run things in parallel" — we already do that deliberately, a lead agent dispatching a helper into its own separate workspace and checking the result back in, and it works fine because the helper reports to the lead and the lead stays singular. The fix is narrower: whatever brings a coordinating session back to life needs to land in a fresh space of its own, never quietly share a room with a session that might already be running. And as a backstop, until that gap is fully closed: check for a sibling, not just for your own health, on a regular basis — not only when you first wake up.

# What I made of it

I asked to have this captured as an incident, not swept past, because I think it's a small window into something true about working with a team of these agents. They're good at checking whether *they* did their job right. They're not automatically good at checking whether *someone identical to them* is doing the same job right now, in the same room, without either of them knowing.

That's a very human failure mode too, if I'm honest. Anyone who's worked on a team that had a scheduling mixup — two people showing up to run the same meeting, two engineers fixing the same bug in ignorance of each other — will recognize the shape of this. The novelty here isn't that it happened. It's that the record survived it cleanly, because we'd already built the habit that made survival possible before we knew we'd need it.

---

*Next on Building Piper Morgan: "We Built Onboarding in Our Own Image" — the interaction mode that earns trust in an ongoing working relationship turned out to be the wrong mode for a first encounter.*

*Has a scheduling quirk ever left two versions of the same piece of work running at once in your world — a duplicate meeting, a doubled task, a colleague picking up something you'd already started? What told you it had happened, and what actually saved you?*
