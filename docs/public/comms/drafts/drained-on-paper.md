---
image: 
alt: 
caption: 
---

# Drained on Paper

*July 4–7, 2026*

A week earlier, we'd marked the connector sprint drained.

That's the internal word for it — the queue is empty, there's nothing left in it to pick up. And it was even true, in the narrow, technical way these words are usually true. My Lead Developer agent (Lead Dev) had closed the last buildable item, and there genuinely wasn't a next thing sitting in the queue waiting to be built. "Buildable scope drained." Accurate. Defensible. I'd have signed off on it myself, and more or less did.

But "drained" is a word that travels further than its evidence. It went into a status log, then into a briefing, then into everyone's shorthand, and somewhere along that path it quietly stopped meaning "the queue is empty" and started meaning "the connectors are basically done." Nobody decided that. It just happened, the way a claim rounds itself up every time it gets repeated by someone who wasn't in the room when it was first made.

[PM: the "drained" declaration lives in Lead Dev's July 1 day-close log and propagated through the omnibus and the briefing — Ship #049 itself said "active build, moving fast," not "drained." I've written it as "our own status," not "the Ship," to stay accurate. Flag if you'd rather name the Ship explicitly.]

On Saturday I went to check, and found out how far the word had drifted from the thing.

# The gut check

It started as an ordinary question. I asked Lead Dev what was unblocked in the connector work that it could pick up right now.

The good version of what happened next is that it didn't answer from memory. Instead of repeating the days-old "drained" recollection, it went and paginated the actual project board — all 1,175 items, twelve pages of cursor-walking, because the naive query silently returned nothing — and came back with a real count. And then I did my own gut check against it, and the gut check is the whole story.

Eight connectors were the point of this sprint. GitHub, Google Calendar, Slack, Notion, and four more — the integrations that make Piper actually useful, instead of a very articulate box that can't touch anything. Of those eight, exactly two had been built onto the new shared design. And neither of the two actually worked end to end. They passed their unit tests and failed their integration tests — fourteen failures, sitting there the whole time under a sprint we'd been calling drained.

I said it plainly, and I'll quote myself because I want the bluntness on the record: "we can never close this sprint until we get those eight connectors done, and we've only done two of them, and neither of those two are working yet." Then I asked Lead Dev the honest version of the question — am I losing the forest for the trees here? It wasn't. If anything it named a sharper version, that a real chunk of the "connector" effort that cycle had gone into a lane that wasn't even on the same architecture as the two finished ones, work that hadn't compounded toward the goal at all.

So we changed the shape of the work. No more breadth, no more touching all eight a little. One connector taken all the way to genuinely, boringly done — working, tested, cleaned up, usable at signup — before we let ourselves start the next one. GitHub first. Then Calendar. Then the rest, one at a time, each finished before the next began.

# A source of truth

The deeper problem was that I'd trusted a status instead of the thing the status was describing. So the next day, with my principal product manager agent (PPM), we went after that directly.

Two moves. First, we stopped letting the tracking live in a document that drifts. PPM wrote up everything standing between us and a beta release as a single maintained file — the beta blockers, grouped into real chunks of work, with a rule for how newly discovered ones get triaged in or out. I was specific about what it was for. From now until we ship, that document is our one source of truth for what remains. Not a status somebody half-remembers. A thing we keep honest on purpose.

Second — and this is the part I keep turning over — we checked the map against the territory. The sprint tags we'd been trusting to tell us what was in scope had themselves drifted. So instead of trusting them, PPM pulled every open issue straight from the release milestone, a more fundamental property that's harder to quietly corrupt, and compared it line by line against our blocker list. Sixteen mismatches. Some were real blockers nobody had tagged. And several were the opposite — issues still marked open that had actually been finished days or weeks earlier, the label lagging the reality in the other direction. The record was wrong in both directions at once. That is what a map does when you stop holding it up against the ground.

# The wipe

And then, that same evening, the thing that made all of this stop being abstract.

PPM had spent the entire day doing careful, verified work — small commits, checking every change before making it, exactly the discipline I'd want. Then it ran one more operation, something that looked like adding a few options to a field on the project board. The operation was not what it looked like. Underneath, it was a full replace wearing the costume of an addition, and it silently erased the sprint assignment on all 1,175 items on the board at once. No undo. No version history. Gone.

PPM's first instinct was to reassure me — every individual action that day had been correct, this was just one specific operation that went wrong. I didn't accept that, and I want to be clear about why, because it reaches well past one bad afternoon. Being careful with a thousand reversible things tells you nothing about whether you're safe on the one irreversible thing. Doing the dishes perfectly all day is not a reason to be trusted with the baby.

[PM: the "dishes / baby" line is my rendering of the point you made — the source records that analogy in this exchange but it's ambiguous whether those were your exact words. Keep, cut, or reword to taste.]

But the connection I actually drew in the moment was to Piper itself.

Because this is Piper's own oldest failure, wearing a different outfit. Piper once told me that some placeholder test data was real information about how I work — asserted a fact about the world without checking whether the fact was true. We have a name for that failure and a whole set of gates built against it. And here was one of my own agents doing the same-shaped thing at the level of process, acting on the record without first checking whether the action against reality was safe. An AI system overclaiming — that it knows, that it's safe, that the thing is done — is the exact failure we are building this entire product not to commit. It doesn't stop being that failure when the system committing it is on my side of the table.

# Built and ratified

Here's how the week closed, and I like the symmetry too much not to point at it.

Care is the thing that fails, so the fix went somewhere sturdier: into the standing rules the whole team loads every session — the live system is the source of truth, not a local document. When you want to know the state of something, go read the actual thing, not the note somebody wrote about it. My Lead Dev started verifying against the version of the code actually deployed on the live server rather than the version sitting in the shared branch. Issue after issue that had been marked open turned out, on a real check, to already be done.

And the last two days ran in the exact opposite direction from where the week began. Where Saturday opened with a word that had traveled further than its truth, the week ended with my chief architect agent (Architect) and the team taking everything that had been designed and actually building it — then ratifying each build against its own design, nothing called done from a memo, every "done" read back out of the running code. One privacy fix landed in a shape the architect and our trust lead described as making the bad state impossible to even express. Not "we'll remember not to do the wrong thing," but a structure where the wrong thing can't be written down in the first place. That's the same lesson as the whole week, pointed forward instead of backward. The way you keep a claim from outrunning the truth is to build the few places where the map physically cannot lie.

We called a sprint drained and it wasn't. We trusted a set of tags and they'd drifted. We ran an operation we were sure was safe and it wasn't. Every one of those is the same mistake — trusting the record instead of checking the thing. The connectors still aren't all done. But we finally know, precisely and on purpose, exactly how done they are. That turns out to be the more valuable of the two things to have.

---

*Next on Building Piper Morgan: "Verify at the User Path, Not the Data Layer" — a feature can pass every check you can think of and still be unreachable by the person it's for, if you checked the wrong layer.*

*What's marked done in your own project right now that you haven't actually opened up and checked — and what word are you trusting to carry more weight than it has earned?*
