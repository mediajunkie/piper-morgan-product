---
image: 'more-than-anyone-ever-reported-to-me-sheep-gate.png'
alt: 'Three luminous AI agents celebrate an empty sheep pen while a startled human discovers most of the flock—and several escape routes—outside their counting gate.'
caption: ''
---

# More Than Anyone Ever Reported to Me

*August 8, 2026*

I spent a Friday morning one month ago testing the product myself, the way an actual user would, instead of reading reports about how ready it was. A reminder feature broke three separate ways in under an hour. Three distinct, unrelated failures, each one a real defect that had been sitting there the whole time. They'd never been tested end to end, for real.

Every report I'd been reading suggested the sprint was in good shape, and forty minutes of my own hands on the keyboard found three ways that wasn't true on just one feature alone.

# The denominator problem

Earlier that same morning, before I'd even opened the product, I'd flagged something to my chief of staff agent (Exec) that felt smaller at the time: we kept reporting the beta blockers as more complete than they actually were, and I thought I knew why. Somewhere in the chain, a true statement about *part* of the work was getting restated as a true statement about *all* of it. "The build queue is empty" is a real, verifiable fact. "The sprint is build-complete" is a different claim, and it isn't the same thing, even though it's tempting to hear the first one and say the second.

*It's not great that I was the only one with an accurate sense of what was actually in the sprint.* A chain of individually-true partial statements had quietly become one confidently false total, and nobody along that chain had checked the whole against its parts.

# The decision

By mid-morning, between the denominator problem and the three-way test failure, I had what I needed. Verbatim, from the decision record: *"I am going to move the beta date back a month. We clearly have a lot more work still to do than anyone ever reported to me."*

I admit a bit of pique probably entered into that statement, passive-aggressively.

It's a statement about *reporting* — about the distance between what was actually true and what everyone, myself included until that morning, believed was true. I wasn't savaging the team's competence or even saying the code was in worse shape than I'd hoped. I was just seeking a honest measurement all the way up the chain, not expecting the agents to work harder.

# What happened next

Within hours, without my asking anyone to, several of my own leads went back through their own recent reports and found the same pattern in their own work. Exec found that their own summary — "the sprint is build-complete" — was the exact restatement-of-a-part-as-a-whole I'd just called out. My principal product manager agent (PPM) went back through their own status updates and found two items they'd been reporting as "advanced" in every review for over a week that had, in fact, never been started at all — the tool they'd been using to check status couldn't actually distinguish "not started" from "waiting on my own review," and they'd been reading the ambiguous case optimistically without realizing it.

Nobody defended their prior report or even waited to be asked to double-check. The correction moved through the team faster than the mistake had, once the mistake (and its nature) was identified.

# The tool that caught itself

That same morning, in direct response to the denominator problem, Exec shipped a small script whose entire purpose is refusing to report a sprint total without also showing its parts — the thing that would have caught the "build-complete" restatement before it ever reached me.

Within the hour, an agent ran the new tool against the actual data and found it had its own version of the exact bug it was built to prevent (sad trombone): it had pulled a large batch of items from the project board but never checked whether that batch was the *whole* board or just the first page of it — the identical error, one layer down. So that got fixed, too. A few hours after that, a second agent found *another* blind spot in the same tool — items that existed but weren't wired into the board it was checking — and that got fixed too, the same day.

*We still make tons of mistakes but we seem to be getting better at catching ourselves making them.*

A tool built that morning specifically to stop a team from mistaking a part for a whole needed two separate corrections, same day, because it had literally made the same incorporated the same error into its design in multiple ways. I think that may the whole lesson in miniature: that a discipline may require ongoing "re-applying," including to the instruments you just built to enforce it and may not be simply a problem you solve once and move past.

Anyhow, another month to work on issues before we get to beta, but a much clearer sense of what is still left to do.

---

*Next on Building Piper Morgan: "The Mailbox Trust Violation" — an agent searches for a memo, can't find it, and tells me it doesn't exist, while a second agent's own search independently gets the same wrong answer.*

*Where in your own work has "the queue is empty" quietly become "we're done" — and how would you actually find out if it had?*
