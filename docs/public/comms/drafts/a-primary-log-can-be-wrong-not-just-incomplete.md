---
image: ''
alt: ''
caption: ''
---

# A Primary Log Can Be Wrong, Not Just Incomplete

*July 16, 2026*

My team has a fact-checking discipline for this blog: before allowing a claim into a post, trace it back to the actual session log where the work happened. Do not rely on a summary or a secondhand mention. Usually, the primary log settles the question. It's the closest thing we have to a transcript of what really happened.

One thing I learned this summer was that "closest thing to a transcript" is distinct from "the truth" particularly when it comes to correctly attributing who did what.

# The claim that wasn't true

While fact-checking a post about our hosted alpha going live, my communications agent (Comms) found a session log from one of our agents referring to a person as our first external tester. The claim was found in a log, so it went into the draft.

Fortunately, my memory for which people have actually tested he alpha so far is pretty good, and this claim was incorrect. (Often an agent will say something has happened for the first time based on their available recollection, without rechecking the entire span of time they are claiming about).

I said so. This person had not actually gotten as far as testing. The underlying claim was simply wrong.

# What a log is

The session log accurately recorded what an agent believed and reported at the time. There was no intention to make a false claim but also no independent check on reality. This is similar to how a log entry saying "sent to so-and-so" documents that someone believed the package was sent to that person. It doesn't, on its own, confirm the delivery, not does it confirm what the recipient then did with it (and it doesn't even inherently prove that the attempt to send the package was completely successfully).

Most of what a fact-checking pass verifies doesn't have this problem. Things like a metric, a date, a commit hash, a test count are facts about the system that can be checked directly. A claim about what a specific human did is a different category entirely. The only source that can actually confirm it is that human, or someone who watched them do it. (A perhaps a painstaking forensic investigation that still might need information only I have to get to the facts.) A log recording "I sent it to her" is exactly as reliable as the belief of the person who wrote that line, no more.

# What got missed

There was a warning sign in the fact-check itself. Comms didn't just accept the claim outright. There were some mildly contradictory claims about who, what, and when that hinted at a possible misunderstanding. Comms considered raising a caveat, then decided that matter was "likely non-contradictory") and moved on. That as a tell, a yellow flag we could learn to notice or maybe get in the habit of erring on the side of discussing anything that doesn't sit right.

Here's the narrow fix we came up with:  **when a claim is about who did something to or with a specific person, treat the primary log as evidence of what was believed, not proof of what happened** and when checking that kind of claim produces a hedge instead of confidence, say so rather than resolve it silently in the draft's favor. Perhaps we'll broaden it to other scenarios over time if we notice them too.

# Where this generalizes

This is really a rule about a category of claim that shows up anywhere a system keeps records of itself, not just about blog fact-checking: a log, a status update, a report someone wrote in good faith at the time. All of it is a transcript of belief, and belief is not automatically synced with reality, especially about a specific person's specific actions. The parts of a record that are hardest to independently re-verify — because the only real check is asking the person involved — are exactly the parts worth treating with the most suspicion, not the least.

The claim didn't make it into the published post. What replaced it was a description without a name attached, which turned out to be correct for two reasons instead of one: better for the person's privacy, and actually true.

---

*Next on Building Piper Morgan: "Three Seats Stay Dark Longer" — the whole team hits its usage limit and goes offline together, but three roles don't come back for twenty-one hours after everyone else does, and nobody knows why until the next day.*

*Where in your own systems does "we have a record of it" quietly substitute for "we confirmed it happened"?*
