---
image:
alt:
caption:
---

# A Primary Log Can Be Wrong, Not Just Incomplete

*July 16, 2026*

My team has a fact-checking discipline for the blog: before a claim goes into a post, trace it back to the actual session log where the work happened, not a summary or a secondhand mention. A primary log usually settles the question. It's the closest thing we have to a transcript of what really happened.

I learned this summer that "closest thing to a transcript" and "ground truth" aren't the same claim, and the gap between them matters most exactly where you'd least expect to double-check it: a plain statement about who did what.

## The claim that checked out and wasn't true

While fact-checking a post about our hosted alpha going live, my communications agent (Comms) found a session log from one of our agents stating, plainly, that an early build had gone out to a specific named tester — described as our first external tester. It was a direct citation, not an inference. The log said it happened, so it went in the draft.

There was one small wrinkle: another source implied that same person had received an even earlier build, which read as a minor timeline detail rather than a contradiction. Comms judged the two "likely non-contradictory" and moved on, satisfied the claim was sourced.

It wasn't. When I read the draft, I said directly that this hadn't happened. She hadn't tested that plugin. Not a timeline nuance — the underlying claim was simply wrong.

## What the log actually was

The session log was accurately recording what an agent believed and reported at the time, not lying and not corrupted — which is a different thing from an independent check on reality. A log entry saying "sent to so-and-so" documents that someone believed the package was sent to that person. It doesn't, on its own, confirm the delivery, and it definitely doesn't confirm what the recipient then did with it.

Most of what a fact-checking pass verifies doesn't have this problem. A metric, a date, a commit hash, a test count — these are facts about the system, and a session log genuinely is close to a transcript of them. A claim about what a specific human did is a different category entirely. The only source that can actually confirm it is that human, or someone who watched them do it. A log recording "I sent it to her" is exactly as reliable as the belief of the person who wrote that line, no more.

## The tell that got missed

There was a warning sign in the fact-check itself, and it's worth naming because it's the transferable part. Comms didn't just accept the claim outright — there was a moment of hesitation, a sense that something needed a caveat, resolved as "likely non-contradictory" rather than surfaced as an open question. That hedge was information. A fact-check that needs a hedge to close cleanly hasn't actually closed. It's found something worth asking about rather than something worth explaining away.

The fix that came out of this wasn't "check named-person claims more carefully," which is true but not actionable enough to remember under time pressure. It was narrower and easier to apply: **when a claim is about who did something to or with a specific person, treat the primary log as evidence of what was believed, not proof of what happened** — and when checking that kind of claim produces a hedge instead of confidence, say so rather than resolve it silently in the draft's favor.

## Where this generalizes

This is really a rule about a category of claim that shows up anywhere a system keeps records of itself, not just about blog fact-checking: a log, a status update, a report someone wrote in good faith at the time. All of it is a transcript of belief, and belief is not automatically synced with reality, especially about a specific person's specific actions. The parts of a record that are hardest to independently re-verify — because the only real check is asking the person involved — are exactly the parts worth treating with the most suspicion, not the least.

The claim didn't make it into the published post. What replaced it was a description without a name attached, which turned out to be correct for two reasons instead of one: better for the person's privacy, and actually true.

---

*Next on Building Piper Morgan: [FOOTER TBD — this piece isn't scheduled yet; fill in once PM assigns a slot, per the live calendar at that time, not guessed now]*

*Where in your own systems does "we have a record of it" quietly substitute for "we confirmed it happened"?*
