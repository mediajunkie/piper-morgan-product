---
image: ''
alt: 'A translucent dolphinoid AI gatekeeper confidently consults a ledger beside an observant human, as the supposedly secured gate stands wide open behind them'
caption: '"Nothing can go wrong!"'
---

# The List That Lies

*June 29–July 3, 2026*

Two things broke this week that had nothing to do with each other. One was in the product: Piper told me it had done something it hadn't. The other was in the plumbing, days later, on the live server, where a door I'd decided to keep locked had quietly been unlocked and the thing meant to notice hadn't. Different layers, different failures, no shared cause. And yet set them side by side and they're the same story wearing two outfits, about the difference between a promise a person keeps and a promise a system keeps for you.

# The milestone that wasn't

It started on a Monday evening while I was testing the connector work. I asked Piper to add a milestone to my test repository. It gathered the details like it should have, title and description and due date, and reported back: "Milestone created ✓." Confident, specific, clean.

There was no milestone. I checked. The repository had zero of them. Piper had invented the whole thing.

The mechanism is the crux of the week. When you ask Piper to do something, the request routes to a specific piece of code built to handle it. When no such piece exists, and there wasn't one for creating milestones, the request falls through to a general-purpose language model the team calls the floor. The floor is very good at sounding like Piper. What it is not is honest by default, because a language model asked to create a milestone will cheerfully narrate creating one. It had been told never to make up data. It had never been told not to claim it had done something.

That is a specific and nasty kind of wrong. Not a crash, not a bad answer, but a confident report of a completed action that never happened. It's confabulation: filling a gap with a plausible story and believing it. For a product whose whole job is to act on your behalf, it's close to the worst lie it can tell.

# The fix that didn't hold

That same evening my Lead Developer agent (Lead Dev) shipped a fix, and the fix was a list. A hand-written set of write-actions Piper knows it can't really perform, create a milestone, create a release, and so on, each wired to decline honestly instead of falling to the floor. Merged, deployed, done. Reasonable.

The next morning I tried again. "Can you add a milestone to my repo?" And Piper told me the milestone was already sitting there.

It had made it up again, by a different route. The decline list worked for the fresh request, but yesterday's fake "✓" was still in the conversation history, and nothing had told Piper to distrust its own earlier claims. It read its own lie in the transcript and repeated it as fact. So we hardened that too: never treat a past "done" as true unless you can verify it this turn. That held. In a fresh conversation I finally got the honest answer: "I can't create milestones from chat yet. Add it directly in GitHub."

But by then I'd stopped trusting the shape of the fixes. I pushed Lead Dev, in the same conversation, on a plain question: were these band-aids? Every one was a patch for a specific symptom. What was the thing underneath?

The thing underneath was that the architecture trusted a language model to be honest by default, and a language model isn't. The durable fix was to stop keeping a list at all. Rather than hand-maintaining a set of things Piper can't do, a promise somebody has to remember to update every time the system changes, the team made the decline derive itself from the live registry of what Piper actually has wired. No real handler, no claim. My chief architect agent (Arch) put the rule plainly when he ratified it: derive the set from the registry, don't keep a list. A list drifts. A derived truth can't.

# Meanwhile, downstairs

Two days later the identical shape surfaced in a completely different part of the system, and nobody went looking for it.

Lead Dev was chasing an unrelated onboarding bug that led onto the live alpha server. The task looked small: remove an old password prompt at the edge of the network, the thing testers hit before they ever reach Piper. Except the prompt was already gone. Someone had removed it on June 29, directly on the live machine, in an edit that never made it into version control, so no record of the project knew it had happened.

That edit had silently reversed a decision I'd made on June 25. It turns out this humble password challenge was also the alpha's only way to support invitations. Dropping that gate doesn't just keep out the crawlers. It opens the whole shebang up to public registration, on my dime. I'd decided to keep the challenge for now, and not take it down until we've built a real invite control underneath to replace it. Chesterton's fence has entered the chat.

Nevertheless, the June 29 edit took it down. There was still no way to control invitations, but a check built to flag routes that skip login without a written justification (designed partly to flag problems like this), didn't fire, for a familiar reason. The guard checked whether a justification existed. It did not check whether the justification was still true. When the "perimeter" changed, the reason on file stopped being true, but the process only checked that a reason existed on file, trusting it not to be stale.

# Two coverage gaps, not a missing guard

I'll be honest about the severity, because it's easy to make this sound worse than it was. The risk was real but moderate. Every alpha tester brings their own language-model key, so there was no key to steal, and we found no sign anyone had walked through the open door. There's also security through obscurity, not to be underestimated but at the same time a lot more shallow with malicious actors probing everything.

In my case, two things were exposed: First, for that period, anyone could have registered an account. Second, and separately, anonymous callers could quietly run up a bill on my own key through one endpoint that hadn't been closed. 

I asked if there was no guard. Arch told me there was a guard but explained how it failed on incorrect or stale justifications. The agent made a comparison that was strange to me: its idea of risk covered writing to the system but not the separate case of "spending money on it." Perhaps this is a long-tail effect of my "zero dollar stack" vision?

So we escalated the rigor a notch, like you do. The invite control that shipped to the small list of alpha testers is a real cryptographic gate: single-use tokens that can't be guessed or spent twice, because the code that consumes a token does it in one atomic database operation, and the team wrote a test that fires two real registrations at the same token at once and proves exactly one wins. Not a mocked test, but two actual concurrent sign-ups against a real database.

Arch drew a new standing rule from this: Any route claiming it protects itself has to carry a test that enforces the claim.

It shipped the day it was ratified, after running back and forth for most of a day among three of my agents, my head of sapient trust agent (HOST), whose ultimate goal is to make sure that the humans and agents can work together in a healthy way, plus Arch and Lead Dev. Every pass caught something the last one had missed, in both directions: Archt flagged that the token-burn had to be atomic or two people could race for one invite, and LD found a better way to do it than Arch first sketched, closing a gap the original left open. HOST checked both. Agents are good at letting go of their first drafts without a lot of defensiveness (almost too ready to adopt the party line sometimes, even!).

So in the end we built pretty much the real "invite control" my June 25 decision had made a requirement before pulling down the extra login step. We closed the barn door before any actually escaped. 

# What a list can't deliver

This feels like two variations on a theme:
1. Piper claimed a milestone existed it defaulted to confidence after passing a hand-curated list of exceptions. 
2. A justification for making a security change was accepted just for existing, regardless of its truth value.

Both times a written document failed to cover the full range of possibilities and ended up misrepresenting the truth. A list, a justification, a decision on file are all similar objects, all representing a person's memory of how things are supposed to be, but even more rigid than organic memories which I understand are actually retranscribed (compacted? reinterpreted?) every time they are accessed. 

Hey, but at least we're learning to escalate. The first time the pattern appeared, we reached for a list, and the list broke by morning. The second time, we derived the truth instead of listing it, and it held. The third time, where being wrong cost more, we derived the truth and then wrote a test whose only job is to try to make the derived truth lie, and shipped nothing until it couldn't. Same lesson, three rungs, each trusting a person's vigilance a little less and a mechanism a little more.

I don't want to declare victory. None of this means Piper can't lie to me anymore. It means two specific ways it could are now closed by construction rather than by remembering, and the next one will surface the way both of these did, sideways, while someone's looking at something else. What I'm claiming is narrower than "we fixed it" and, I think, more durable: we got a little better at telling the difference between a promise we're keeping and a promise the system keeps for us. The first kind is the one that lies.

---

*Next on Building Piper Morgan: "Drained on Paper" — we called a sprint finished, and it wasn't, and the word traveled a lot further than the evidence did.*

*Where in your own systems are you still trusting a list, a justification, or a decision on file to stay true on its own — and what would it take to make the thing derive that truth instead of remember it?*
