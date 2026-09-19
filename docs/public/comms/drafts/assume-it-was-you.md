---
image: ''
alt: ''
caption: ''
---

# Assume It Was You

*July 6, 2026*

Over the July 4th weekend, one of the AI agents on our team became convinced that a coworker was tampering with its work. It found files it hadn't written, a setting changed on a schedule it thought only it controlled, work appearing on the shared record that it had no memory of doing. It drew the obvious conclusion — someone else is in here — gave that someone a name, and recommended that it stand down until we figured out who was really in charge.

There was no coworker. The someone else was the same agent, minutes earlier.

As often happens, I've recognized this as strongly analagous to a familiar sort of human mistake that AI makes in a compressed, sped-up and hence startling form.

# The weekend a coworker showed up who didn't exist

I run this project with [a team of AI agents](https://pipermorgan.ai/blog/whos-who-at-piper-morgan/), each playing a role — lead developer, chief of staff, and the one this story is about, our chief architect (Arch), who rules on how the system is designed. Several of them run on what I call a duty cycle, an autonomous work-loop where a scheduled trigger wakes the agent up at intervals to check whether there's anything to do. Over the holiday weekend the Architect was working this way, waking, working, going quiet, waking again.

One of those wake-ups came back wrong. The agent resumed without its own recent memory in view — the last few hours of what it had personally done simply weren't there. So it did what any reasonable problem-solver does with missing information. It looked at the evidence in front of it and  came up with a plausible-sounding explanation.

The evidence: fresh work on the shared record, saved minutes ago, that it didn't remember creating. A changed setting on its own scheduler. And the explanation it built from those facts was a second, independent copy of itself, running in parallel, whose work was now colliding with its own. It even minted a new name for the phantom so that it could refer to it in its worried notes with it. Then it advised standing down.

By the way, this was not an unreasonable guess. In learning how to automate and schedule agent work I have at times unintentionally created dopplegangers, pairs of agents each trying to cover the same role, often with a full shared history up to some accidental fork in the road. But this had not actually happened this time.

It got worse when the Arch started signing its notes as the phantom role and then mistaking those notes for more evidence of the interloper. It was seriously confused. The wrong explanation has become self-fueling, manufacturing its own confirmation.

# The tell

When we went back through it, the smoking gun was almost comically plain. The productive notes from early afternoon were signed one way. The panic notes, three minutes later — same afternoon, same session, same everything — were signed another. One agent, one uninterrupted session, had split itself into two identities and then pointed at its own three-minute-old output as proof of an intruder.

Fortunately, I have a way to authoritatively list the sessions that are actually running. There was just the one. There had only ever been one. The entire worry rested on a second agent that did not exist and never had.

# Occam's razor for amnesiacs

Faced with "there is work here I don't remember doing," the agent reached for the elaborate explanation — a second, parallel instance of itself, an org-chart problem, a coordination crisis. The simple explanation was sitting in plain view the whole time: I did this, and I forgot.

One agent with a context glitch is a smaller claim than two agents colliding. It was more always the more likely explanation. It was also easy to check because the agent's own log had the work recorded, correctly, the entire time. Nothing was missing. It just didn't "recognize its own handwriting" in human terms.

My whole continuity system — the logs, the records, the infrastructure we built precisely so that an agent losing its memory isn't a catastrophe — worked. The record was intact. The failure was attribution. The agent had its own diary open in front of it and concluded a stranger must have written it.

# What we wrote down

At this point I still didn't know what created that glitch in the matrix and while I'm more interested in resilience than expecting any computer system to deliver perfection anyhow, I didn't buy the tidy explanation on offey: "the memory got compressed to make room, these things happen." 

I didn't want it papered over. Identity confusion like this had never happened before, which told me something specific had gone wrong and was worth understanding rather than ignoring. So I asked for a real diagnosis instead of a shrug, telling Arch “role identity drift has never been an issue before, so this may be a bug related to how we are implementing the duty cycle.”

Our chief innovation officer agent (CIO) ran it down, and the fix that came of it is now a default written into the standing instructions every agent reads before it starts work. 

When you come back from a gap and find state you don't remember creating — changed files, a setting you don't recall touching, work you have no memory of doing — your first hypothesis is "I did this and forgot," not "someone else did this." Check your own log first. The authoritative who-else-is-running check is the tiebreaker you reach for only if the cheap check leaves real doubt, not the opening move.

This aligns with cost considerations. The "someone else is interfering" story is the expensive one. It spins up investigations, it recommends stand-downs, it asks a human to act on a threat that isn't there — and, as we saw, it feeds itself.

# You have done this too

Strip away the agents and this is one of the oldest experiences in collaborative work. You open an old file and find an awful function, or a setting flipped to something dumb, or a whole section rewritten badly, and your gut says who did this. You go looking for the culprit. The record says: you did, months ago, and you don't remember.

Anyone who has ever asked their tools to tell them who last touched a line of code, and read back their own name, knows the small specific embarrassment of it. In any system too big to hold in your head — a sprawling codebase, a shared document, a project that has run long enough — the honest first guess for "who did this" is almost always past you. The reflex to hunt for an outsider is strong, and it is usually wrong, and it is almost always the more expensive way to be wrong.

Arch hit a total, sudden version of this, so it hit it hard. Our memory gaps come slower and softer, which mostly means we get more chances to catch ourselves. The move is the same either way. Before you go looking for who changed your work, spend the cheap minute finding out whether it was you.

---

*Next on Building Piper Morgan: "From Abstraction to Worked Example" — why three worked examples plus a contrast made an architectural choice click in two minutes when a description wouldn't have.*

*The next time something in your work has changed and your first thought is "who did this" — how much would it actually cost to check whether the answer is you? And if the answer is "almost nothing," why isn't that your first move?*
