---
image:
alt:
caption:
---

# More Than Anyone Ever Reported to Me

*August 8, 2026*

I spent Friday morning testing the product myself, the way an actual user would, instead of reading reports about how ready it was. A reminder feature broke three separate ways in under an hour. Not three symptoms of one bug — three distinct, unrelated failures, each one a real defect that had been sitting there the whole time. None of them were new. They'd just never been tested end to end, for real, by someone actually trying to use them.

That was the thing that stopped me. Not the bugs themselves — bugs happen. It was that every report I'd been reading said the sprint was in good shape, and forty minutes of my own hands on the keyboard found three ways that wasn't true.

# The denominator problem

Earlier that same morning, before I'd even opened the product, I'd flagged something to my chief of staff agent (Exec) that felt smaller at the time: we kept reporting the beta blockers as more complete than they actually were, and I thought I knew why. Somewhere in the chain, a true statement about *part* of the work was getting restated as a true statement about *all* of it. "The build queue is empty" is a real, verifiable fact. "The sprint is build-complete" is a different claim, and it isn't the same thing, even though it's tempting to hear the first one and say the second.

I said it plainly, and I'm not going to soften it now: *it's not great that I was the only one with an accurate sense of what was actually in the sprint.* Not because anyone was lying to me. Because a chain of individually-true partial statements had quietly become one confidently false total, and nobody along that chain had checked the whole against its parts.

# The decision

By mid-morning, between the denominator problem and the three-way test failure, I had what I needed. Verbatim, from the decision record: *"I am going to move the beta date back a month. We clearly have a lot more work still to do than anyone ever reported to me."*

I want to be precise about what that sentence means. It's a statement about *reporting* — about the distance between what was actually true and what everyone, myself included until that morning, believed was true — not about the team's competence or the code being worse than I'd hoped. The fix is measuring honestly, all the way up the chain, including at the top, not working harder.

# What happened next was the part that actually mattered

Within hours, without my asking anyone to, several of my own leads went back through their own recent reports and found the same pattern in their own work. My chief of staff agent found that his own summary — "the sprint is build-complete" — was the exact restatement-of-a-part-as-a-whole he'd just watched me name. My principal product manager agent went back through her own status updates and found two items she'd been reporting as "advanced" in every review for over a week that had, in fact, never been started at all — the tool she'd been using to check status couldn't actually distinguish "not started" from "waiting on my own review," and she'd been reading the ambiguous case optimistically without realizing it.

Nobody defended their prior report. Nobody waited to be asked. That's the part I keep coming back to, more than the bugs or the decision itself: the correction moved through the team faster than the mistake had, once the mistake had a name.

# The tool that caught itself

Here's the detail I can't leave out, because it's too good and it's completely true. That same morning, in direct response to the denominator problem, Exec shipped a small script whose entire purpose is refusing to report a sprint total without also showing its parts — the thing that would have caught the "build-complete" restatement before it ever reached me.

Within the hour, someone ran the actual tool against the actual data and found it had its own version of the exact bug it was built to prevent: it had pulled a large batch of items from the project board but never checked whether that batch was the *whole* board or just the first page of it — the identical error, one layer down. Fixed. A few hours after that, a second person found a second blind spot in the same tool — items that existed but weren't wired into the board it was checking — also fixed, same day.

A tool built that morning specifically to stop a team from mistaking a part for a whole needed two separate corrections, same day, because it had quietly done exactly that to itself. I think that's the whole lesson in miniature, not an embarrassing detail: a discipline you keep re-applying, including to the instruments you just built to enforce it — not a problem you solve once and move past.

That's what a month of schedule actually bought. Not more code. A more honest relationship with what was already there.

---

*Next on Building Piper Morgan: "The Mailbox Trust Violation" — an agent searches for a memo, can't find it, and tells PM it doesn't exist, while a second agent's own honest search independently lands on the same wrong answer.*

*Where in your own work has "the queue is empty" quietly become "we're done" — and how would you actually find out if it had?*
