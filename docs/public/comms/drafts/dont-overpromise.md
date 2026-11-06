---
image: ''
alt: ''
caption: ''
---

# Don't Overpromise

*September 7–8, 2026*

I keep going back and forth on how much structure to provide for new users working with Piper Morgan for the first time. Without cues, how is someone supposed to know what to ask for, what to expect? But wizards and onboarding questionnaires feel so rigid and overdetermined before we fully understand where the person is coming from.

Still, I keep trying and last month tried out a new-user interview. When I checked it the next day I found Piper overpromising, claiming to do things that may be in the roadmap but that are definitely not true now. In this case that Piper would "tune to your role." I got that line cut.

# A cold open

Befor this, a brand-new user with nothing connected yet would get a generic greeting. With this approach, Piper now opens with one useful question. My principal product agent (PPM) ruled it should not ship yet, citing a freeze on web chat changes but I used my boss prerogative to override that caution and allow it, approving the request in the terse way Claude agents often prefer: *flip ftux* ("meaning switch over to the new first-time user experience").

My lead developer agent (Lead) deployed it that evening and turned the interview on.

# First run

The next day my web design agent (Web) logged into a local copy of the app as a fresh account in a real browser and said "Hi." Piper replied with the interview question CXO had written for this routine, but also ad libbed these words:

> (Running with a default configuration for now — I'm fully useful as-is, and I'll tune to your role and priorities as I learn them.)

This wasn't supposed to be part of the interview. Web flagged it, suggesting it didn't seem right. It turned out to be older copy from a personalization feature, riding along on the same first reply. 

# The claim

Lead also traced the claim Piper was making and found that the code path that would store anything about your role at this time is never called in the code: "nothing can ever tune it" (at least until we wire that in, likely during the beta period). Worse, Lead pointed out the "two halves of a learning→tuning loop both exist and never touch." 

CXO ruled against hedging or adding weasel words. For now Piper makes a more modest promise, noting in this case that they are "(Running with a default configuration — nothing here needs setting up first.)

# Watch out for stale promises

I sincerely hope and expect that Piper will connect those two systems and start being able to learn and tune their behavior based on the experience of working with their human But this is not the case today, and the copy written at one point in anticipation of it being true by now almost slipped out as a false promise until we checked.

It's a little scary how easy it is overpromise to the people you are designing and building for, which is the easiest way to squander the trust you might have otherwise earned.

---

*Next on Building Piper Morgan, "At Long Last, Beta" about what finally reaching beta means to me, and taking a quick look back and forward, takin stock.*

*Are you carefully reading every promise your product makes in your name! Scary thought, right? Maybe it's time to take the Halloween decorations down.*
