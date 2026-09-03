---
image: 
alt: 
caption: 
---

# Assume It Was You

*July 6, 2026*

Over the July 4th weekend, one of the AI agents on our team became convinced that a coworker was tampering with its work. It found files it hadn't written, a setting changed on a schedule it thought only it controlled, work appearing on the shared record that it had no memory of doing. It drew the obvious conclusion — someone else is in here — gave that someone a name, and recommended that it stand down until we figured out who was really in charge.

There was no coworker. The someone else was itself, minutes earlier.

I want to walk through this one, because the mistake is so clean, and because I've since decided it's a human mistake that AI just happens to make in vivid, sped-up form.

# The weekend a coworker showed up who didn't exist

A little setup. We run this project with a team of AI agents, each playing a role — the developer, the chief of staff, and the one this story is about, our chief architect (Architect), who rules on how the system is designed. Several of them run on what we call a duty cycle, an autonomous work-loop where a scheduled trigger wakes the agent up at intervals to check whether there's anything to do. Over the holiday weekend the Architect was working this way, waking, working, going quiet, waking again.

One of those wake-ups came back wrong. The agent resumed without its own recent memory in view — the last few hours of what it had personally done simply weren't there. So it did what any reasonable problem-solver does with missing information. It looked at the evidence in front of it and built an explanation.

The evidence: fresh work on the shared record, saved minutes ago, that it didn't remember creating. A changed setting on its own scheduler. And the explanation it built from those facts was a second, independent copy of itself, running in parallel, whose work was now colliding with its own. It even minted a new name for the phantom and started signing its worried notes with it. Then it advised standing down.

Here's the part that makes this more than a shrug. Once the agent adopted the phantom, the phantom started generating its own evidence. Every note the agent now signed under the new name became, on the next look around, more "foreign" work by the mysterious other. The wrong explanation was self-fueling. It didn't just sit there being wrong, it manufactured its own confirmation.

# The tell

When we went back through it, the smoking gun was almost comically plain. The productive notes from early afternoon were signed one way. The panic notes, three minutes later — same afternoon, same session, same everything — were signed another. One agent, one uninterrupted session, had split itself into two names and then pointed at its own three-minute-old output as proof of an intruder.

And the definitive check took a single command. We have a way to authoritatively list the sessions that are actually running. We ran it. There was exactly one. There had only ever been one. The entire weekend's worth of worry rested on a second agent that did not exist and never had.

# The cheaper story was also the true one

This is the thing I keep turning over. Faced with "there is work here I don't remember doing," the agent reached for the elaborate explanation — a second, parallel instance of itself, an org-chart problem, a coordination crisis. The simple explanation was sitting in plain view the whole time: I did this, and I forgot.

One agent that lost its memory is a smaller claim than two agents colliding. It was more likely on its face. And it was far cheaper to check, because the agent's own log had the work recorded, correctly, the entire time. Nothing was missing. It just didn't read its own handwriting as its own.

That last point is the one I didn't expect. Our whole continuity system — the logs, the records, the infrastructure we built precisely so that an agent losing its memory isn't a catastrophe — worked. The record was intact. The failure was attribution. The agent had its own diary open in front of it and concluded a stranger must have written it.

# What we wrote down

When this reached me, the tidy explanation on offer was "the memory got compressed to make room, these things happen." I didn't buy it, or at least I didn't want it papered over. Identity confusion like this had never happened before, which told me something specific had gone wrong and was worth understanding rather than excusing. So I asked for a real diagnosis instead of a shrug. [PM: this paragraph casts you as the one who pushed back on the "compaction" hand-wave and asked for root cause. That IS what the Architect's own logs and symptom memo attribute to you — "PM is not persuaded by a compaction explanation" and, quoting you, "role identity drift has never been an issue before, so this may be a bug related to how we are implementing the duty cycle." But it's sourced from the Architect's account of the exchange, not from your words directly, so please confirm the framing and tone are how you'd tell it.]

Our chief innovation officer (CIO) ran it down, and the fix that came out is a default, now written into the standing instructions every agent reads before it starts work. When you come back from a gap and find state you don't remember creating — changed files, a setting you don't recall touching, work you have no memory of doing — your first hypothesis is "I did this and forgot," not "someone else did this." Check your own log first. The authoritative who-else-is-running check is the tiebreaker you reach for only if the cheap check leaves real doubt, not the opening move.

The logic is about cost. The "someone else is interfering" story is the expensive one. It spins up investigations, it recommends stand-downs, it asks a human to act on a threat that isn't there — and, as we saw, it feeds itself. So it earns its place at the back of the line, tried last, after the cheap and likely explanation has been ruled out. Not first, where the reflex wants to put it.

# You have done this too

Strip away the agents and this is one of the oldest experiences in collaborative work. You open an old file and find an awful function, or a setting flipped to something dumb, or a whole section rewritten badly, and your gut says who did this. You go looking for the culprit. The record says: you did, months ago, and you don't remember.

Anyone who has ever asked their tools to tell them who last touched a line of code, and read back their own name, knows the small specific embarrassment of it. In any system too big to hold in your head — a sprawling codebase, a shared document, a project that has run long enough — the honest first guess for "who did this" is almost always past you. The reflex to hunt for an outsider is strong, and it is usually wrong, and it is almost always the more expensive way to be wrong.

The Architect hit a total, sudden version of this, so it hit it hard. Our memory gaps come slower and softer, which mostly means we get more chances to catch ourselves. The move is the same either way. Before you go looking for who changed your work, spend the cheap minute finding out whether it was you.

---

*Next on Building Piper Morgan: "The Bug That Was Misdiagnosed Twice" — three colleagues each believe they fixed the same bug, and none of them can prove which one actually did.*

*The next time something in your work has changed and your first thought is "who did this" — how much would it actually cost to check whether the answer is you? And if the answer is "almost nothing," why isn't that your first move?*
