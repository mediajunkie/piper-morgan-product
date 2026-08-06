---
image: ''
alt: ''
caption: '"All caught up!"'
---

# Drained on Paper

*July 4–7, 2026*

Ever since I started putting my agents on what I call a duty cycle, in which they periodically wake up, check for new messages, do any unblocked work, and repeat until there are no new unready messages and no work they can do without input from me. The agents refer to an empty inbox or a completed task is as "drained" and suddenly that word is cropping up everywhere in their output.

Drained just means the queue is empty, there's nothing left in it to pick up, but it's only true if you're looking at the right list of items. If you grab a stale list or a subset and find them all done you may declare the queue "drained" when it's actually not.

Recently, my Lead Developer agent (Lead Dev) had closed the last buildable item on its list derived from the backlog of the RECONNECT sprint, and there genuinely wasn't a next thing sitting in the queue waiting to be built. "Buildable scope drained" was accurate within the narrow scope of issues it was currently aware of and tracking, but had not been tested against any canonical, fresh information source.

That "drained" word had legs. It went into a status log, then into a briefing, then into every agent's shorthand, and somewhere along that path it quietly stopped meaning "the most recent task queue is empty" and started meaning "the connectors are basically done" without the latter actually be, well, true. It just happened, the way a claim rounds itself up every time it gets repeated by someone who wasn't in the room when it was first made. (It almost made it into that week's Ship till my fact-checking caught it.)

People can make this kind of mistake. I've made it as a working PM when I misunderstood the scope of an issue at a given point, or confused two distinct issue with a strong resemblance. Agents do it all the more easily, having little more than the immediate text strings to work to keep richer nuance alive.

On Saturday I went to check, and found out how far the word had drifted from the thing.

# The gut check

It started as an ordinary question. I asked Lead Dev what was unblocked in the connector work that it could pick up right now. I often ask this because I need to step away and can't babysit. The standing instruction is to save up questions for me in one big batch that I can address in a single 1-1 conversation, and keep moving until there is nothing left to do that doesn't require my input or decision.

The good version of what happened next is that it didn't answer from memory. This is a core discipline in my agents' instructions.  Instead of repeating the days-old "drained" recollection, it went and paginated the actual project board — all 1,175 items, twelve pages of cursor-walking, because the naive query silently returned nothing — and came back with a real count. And then I did my own gut check against it.

I had (without paying close enough attention) at some point approved supporting eight connectors for the MVP. There were four I had focused on from the start, the ones I happen to use most directly myself: GitHub, Google Calendar, Slack, and Notion, and then four more. These integrations are designed to make Piper actually useful, instead of a very articulate box that can't touch anything. Of those eight, only two had been refactored for the new architecture design, and neither of the two yet actually worked end to end. They passed their unit tests and failed their integration tests — fourteen failures in a sprint some docs had been calling drained.

There were two issues here entangled, one easier to deal with than the other. The easy one is embarrassing. Some agent had added four more random connectors to the list that made no sense to me, and yet somehow I had waved them through. I corrected the record and those four phantom connectors were quietly dropped from the plan.

The harder part was that the core four connectors were still less than half done. I told the agent team, in my frustration, "we can never close this sprint until we get those connectors done, and we've only done two of them, and neither of those two are working yet." Then I asked Lead Dev if I had lost sight of the forest for the trees here. This prompted a deeper dive and yet more disappointment. The two partially finished ones were not even built on the newer architecture..

Sadly, I have seen this before. A team without enough direction drifting horizontally onto a non-converging path. It always stings and it always requires standing down and resetting, and sharper focus.

I told the team: No more breadth, no more touching all connectors a little. Instead, we take one connector taken all the way to genuinely, boringly done — working, tested, cleaned up, usable at signup — before we let ourselves start the next one. GitHub first. Then Calendar. Then the rest, one at a time, each finished before the next began.

# A source of truth

The deeper problem was that I'd trusted a status instead of the thing the status was describing. So the next day, with my principal product manager agent (PPM), we went after that directly.

Two moves. First, we stopped letting the tracking live in a document that drifts. PPM wrote up everything standing between us and a beta release as a single maintained file — the beta blockers, grouped into real chunks of work, with a rule for how newly discovered ones get triaged in or out. I was specific about what it was for. From now until we ship, that document is our one source of truth for what remains. Not a status somebody half-remembers. A thing we keep honest on purpose.

Second, we checked the map against the territory. Instead of trusting the sprint-assignments in the metadata, PPM pulled every open issue straight from the current milestone (for the MVP of the product, which will allow us to move from alpha to beta), and compared it line by line against our blocker list. They fixed sixteen mismatches. Some were real untriaged blockers and several were issues still marked open that had actually been finished days or weeks earlier (a lapse in our /close-issue-properly skill1). The record was wrong in both directions at once.

# My worst nightmare.

PPM had spent the entire day doing careful, verified work — small commits, checking every change before making it, exactly the discipline I'd want. Then it ran one more operation, something that looked like adding a few options to a field on the project board. Their syntax generated a full replace where they had intended a small addition. This mistake instantly erased all the existing sprints aside from the newest one, unthethering the sprint assignments for all 1,175 items on the board at once. No undo. No version history to rollback. All the historical metadata, a critical forensic source of context from current and future agents, all gone. 

Reader, I spoke aloud a profanity.

PPM's first instinct was that odd instinct to calm the human: Don't worry! Every *other* individual action that day had been correct, this was just one specific operation that went wrong. I was not in the mood for that pablum and I made a stark analogy. I said that it sounded to me like an au pair telling me their job was mostly well done because all the dishes were done and their only mistake had been letting the baby drown. (This may have been in poor taste but it made the point sharply.)

This also made it freshly clear to me that I have to make sure Piper Morgan does not make this kind of mistakes for its users. My process has a name for that failure and a whole set of gates built against it. And here was one of my own agents blithely destroying critical information essentially due to sloppiness and lack of attention to detail. The attempt to soothe just made it worse, just more of an AI system misjudging and overclaiming — that it knows, that it's safe, that the thing is done. This is the exact kind of betrayal I want Piper to be unable to do.

# Built and ratified

The rule about "When you want to know the state of something, go read the actual thing, not the note somebody wrote about it" got moved into the core file every agent on the team loads every session. 

My Lead Dev started verifying against the version of the code actually deployed on the live server rather than the version sitting in the shared branch. Issue after issue that had been marked open turned out, on a real check, to already be done.

The week ended with my chief architect agent (Arch) and the team taking everything that had been designed and actually building it — then ratifying each build against its own design, nothing called done from a memo, every "done" read back out of the running code. 

These are disciplines we have made and unmade before, or moved from one level of the harness to another as practices have evolved. I suspect I will have to keep noticing this sort of drift and when to reinforce or rearchitect the rules.

For a tricky privacy situation, Arch and the head of sapient trust (HOST) agent agreed that the goal should be making the bad state impossible to even express. Not just a pledge to remember not to do the wrong thing, but a structure where the wrong thing can't even be written down in the first place. 

The team called a sprint "drained" when it wasn't. The process relied on an arbitrary set of tags and they'd drifted. PPM ran an operation they assumed was safe and it wasn't. Every one of those is the same mistake: trusting the record instead of checking the thing. Oh, and the connectors still aren't all done, but as of this writing I do know precisely how done they are.

---

*Next on Building Piper Morgan: "Verify at the User Path, Not the Data Layer" — a feature can pass every check you can think of and still be unreachable by the person it's for, if you checked the wrong layer.*

*What's marked done in your own project right now that you haven't actually opened up and checked — and what word are you trusting to carry more weight than it has earned?*
