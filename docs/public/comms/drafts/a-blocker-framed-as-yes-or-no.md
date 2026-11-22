---
image: ''
alt: ''
caption: ''
---

# A Blocker Framed as Yes or No

*November 10–16, 2026*

As I get more comfortable letting my agents run autonomously for long intervals between check-ins, I find that my role as the bottleneck remains central, and my desire to sort out "smart bottleneck" cases where I really am needed from "dumb bottleneck" cases where I hold up the whole show until I do some mindless task, likewise remains as of yet not fully satisfied.

# Gridlock

Earlier this month I checked in with the project to see what needed me and found that several agents were blocked waiting for permission or decisions from me. For example, my prototypical assistant agent (Piper Alpha) was blocked from logging into a test account on the Piper Morgan beta by the classifier Claude uses to prevent risky agent behavior in auto mode (a false negative, from my point of view). Piper Alpha (PA) relayed the permission request to my chief of staff agent (Exec) for my attention.

By the time I responded to this request, a few days, later, PA offered me three potential methods for resolving their impasse. I replied  "Happy to do whatever is easiest. Overall better if we find ways where I don't block this sort of thing."  The team scrambled to follow this direction. 

[Comms: help me unpack the sense of this sentence. "ruled a durable route" does not make sense. Is the idea that Arch prevented PA's proposed solution for reasons?:] My chief architect agent (Arch) ruled a durable route (a signed-in browser profile) and refused an allow rule for a credential file.

[for the reader I need more of the sense of what was reframed. it went from a yes/no to what exactly?]
 The omnibus heading: "A three-day credential blocker was reframed in about 15 minutes and still ended the day unrun." [Nov 13 l61]
- PA's own read of why it took three days: the blocker "sat as a yes/no on reading a file because that's how it was first framed." [Nov 13 l61]

# Hot potato

Two days later when a test run was blocked by [Comms: does paid run stopped at zero calls mean the credit balance for that key was $0? please unpack]. Four of my agents discussed the problem and converged on their preferred solution. They wanted met to run a couple of commands in my terminal. This was passed along to Exec, who concurred.

As I was once again starting to feel relegated to a role as assistant to my assistants (what Cory Doctorow has taken to call "[reverse centaurs](https://us.macmillan.com/books/9780374621568/thereversecentaursguidetolifeafterai/)"), I pushed back on this, writing "We need to solve that problem, not assign me manual tasks as a workaround for a poorly conceived solution." Also: it "keeps becoming my problem to manually navigate", and "Until we solve that the entire project is hobbling itself". 

Exec took the reins and asked each agent "seat" on the team to report back with the one thing in its lane that most often lands on you, then took this feedback and wrote a proposal that became [ADR-084](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/adrs/adr-084-seat-resources-are-separate-granted-once-and-bounded.md) that evening. Exec also noticed that tasks were still piling up for me, noting "The first step grew from one paste to four in two hours," and asking my chief innovation officer agent (CIO) to refactor the next request for me back to one command. 

I approved the proposed ADR the next day, and also OK'd a budget cap of $10 for any agent to run tests without asking first, with a monthly cap of $150. (I felt OK doing this since my current plan provides $200 free credits a month.) 

At the end of a week, that particular task remained blocked. The agents had done what I asked - provided me with as few steps as possible to unblock them - but in the meantime my attention had drifted away again, so they steps waited for me to cycle back once more.

# Redesigning the bottleneck

I file all of this under a broader category of reframing. I put a lot of trust in my own laziness, or if I want to be more charitable toward myself, my impatience with boring repetitive rote work. I'll do busy work and simple tasks when I need to, as anyone does, but I don't love it, and I get frustrated quickly if it seems pointless. The whole promise of computerization, let alome AI, is to automate what is repeatable and spare ourselves the drudgery so we can focus on things only we can uniquely do. Every time the agent team converges on a solution like "give it to the human to do," the plumbing is backing up, as far as I'm concerned.

Speaking up about it pushed my agent team to redesign their workflow. It doesn't take me out the loop (hardly!) but it guards against simply piling busy work into my queue as a shortcut or easy answer.


---

*Next on Building Piper Morgan, "Mark One Eyeball," in which a bare link stuck into an admin page suffices for automated tests but fails for my using my own eyes.]*

*Delegation is a real art and one of the signs you aren't doing it well is when every question lands on your desk. How d you empower your team to take initiative while ensuring they still bring the the tough calls to you as needed?*
