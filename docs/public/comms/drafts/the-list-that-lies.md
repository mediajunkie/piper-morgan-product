---
image:
alt:
caption:
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

That same evening my Lead Developer agent shipped a fix, and the fix was a list. A hand-written set of write-actions Piper knows it can't really perform, create a milestone, create a release, and so on, each wired to decline honestly instead of falling to the floor. Merged, deployed, done. Reasonable.

The next morning I tried again. "Can you add a milestone to my repo?" And Piper told me the milestone was already sitting there.

It had made it up again, by a different route. The decline list worked for the fresh request, but yesterday's fake "✓" was still in the conversation history, and nothing had told Piper to distrust its own earlier claims. It read its own lie in the transcript and repeated it as fact. So we hardened that too: never treat a past "done" as true unless you can verify it this turn. That held. In a fresh conversation I finally got the honest answer: "I can't create milestones from chat yet. Add it directly in GitHub."

But by then I'd stopped trusting the shape of the fixes. I pushed my Lead Developer agent twice, in the same conversation, on a plain question: were these band-aids? Every one was a patch for a specific symptom. What was the thing underneath?

The thing underneath was that the architecture trusted a language model to be honest by default, and a language model isn't. The durable fix was to stop keeping a list at all. Rather than hand-maintaining a set of things Piper can't do, a promise somebody has to remember to update every time the system changes, the team made the decline derive itself from the live registry of what Piper actually has wired. No real handler, no claim. My chief architect agent (Architect) put the rule plainly when he ratified it: derive the set from the registry, don't keep a list. A list drifts. A derived truth can't.

# The same shape, downstairs

Two days later the identical shape surfaced in a completely different part of the system, and nobody went looking for it.

My Lead Developer agent was chasing an unrelated onboarding bug that led onto the live alpha server. The task looked small: remove an old password prompt at the edge of the network, the thing testers hit before they ever reach Piper. Except the prompt was already gone. Someone had removed it on June 29, directly on the live machine, in an edit that never made it into version control, so no record of the project knew it had happened. [PM: the logs establish only that the June 29 gate removal was "undocumented, not the Lead's, not from the runbook" — they don't say who made the edit. If it was you, there may be a stronger, more honest first-person beat here about owning an untracked change to the live server. If not, it stays attributed to no one. Your call.]

That edit had quietly reversed a decision I'd made on June 25, and that decision is the hinge of the thing. We'd found that this humble password prompt was doing a job nobody had designed it to do: it was the alpha's only invite mechanism. The code that creates a new user account had no gate of its own, no invite code, no allowlist. Remove the prompt and you don't just drop a crawler-blocker, you open public registration. So I'd decided: keep the prompt for now, and don't take it down until we've built a real invite control underneath to replace it.

The June 29 edit took the prompt down. The invite control still did not exist. And the guard that should have caught this, a check built to flag routes that skip login without a written justification, didn't fire, for a reason that is exactly the milestone bug again. The guard checked whether a justification existed. It did not check whether the justification was still true. When the perimeter changed, the reason on file silently became false, and a check that asks "is there a reason?" says yes to a reason that has quietly become a lie.

# Two coverage gaps, not a missing guard

I'll be honest about the severity, because it's easy to make this sound worse than it was. The risk was real but moderate. Every alpha tester brings their own language-model key, so there was no key to steal, and we found no sign anyone had walked through the open door. Two things were exposed: anyone could now register an account, and separately, anonymous callers could quietly run up a bill on my own key through one endpoint that hadn't been closed. Two holes, open a couple of days, found because someone was looking at something else.

The easy read was "we have no guard." My chief architect agent pushed back, and the correction mattered. The guard was real, and it worked. What it had were two specific coverage gaps: it checked a justification's existence but not its truth, and its idea of risk covered writing to the system but not the separate case of spending money on it. His phrasing, and I'm quoting him because the framing is his and not mine, was two coverage gaps in a working guard, not a missing guard. You fix two named gaps. You flail at a missing one.

Then the fix escalated the rigor a notch past the milestone fix, which is the part of the week I keep turning over. The invite control that shipped is a real cryptographic gate: single-use tokens that can't be guessed and, this is the detail I love, can't be spent twice, because the code that consumes a token does it in one atomic database operation, and the team wrote a test that fires two real registrations at the same token at once and proves exactly one wins. Not a mocked test, but two actual concurrent sign-ups against a real database.

That's the escalation, and the Architect drew a new standing rule from it: any route claiming it protects itself has to carry a test that enforces the claim.

It shipped the day it was ratified, after running back and forth for most of a day among three of my agents, my head of sapient trust agent (HOST), whose job is to watch whether the system is honest, plus the Architect and the Lead Developer. Every pass caught something the last one had missed, in both directions: the Architect flagged that the token-burn had to be atomic or two people could race for one invite, and the Lead found a better way to do it than the Architect first sketched, closing a gap the original left open. HOST checked both held. Nobody defended their first draft.

The thing that finally replaced that unlocked June 29 door was, almost exactly, the real invite control my June 25 decision had said we'd need before the door could come down at all. We just built it in the right order the second time.

# What a list can't promise

Put the two failures next to each other and they rhyme. Piper claimed a milestone existed because a list of what it couldn't do was a promise a person had to maintain. The server let registration fall open because a justification on file was a promise a person had to keep true. Both times, something written down had quietly fallen out of step with what was so, and both times the report kept asserting the old thing with total confidence. A list, a justification, a decision on file: these are the same object. They're a human's memory of how things are supposed to be, and human memory is the thing that fails silently while still sounding sure.

What the week showed me is that we're learning to escalate. The first time the shape appeared, we reached for a list, and the list broke by morning. The second time, we derived the truth instead of listing it, and it held. The third time, where being wrong cost more, we derived the truth and then wrote a test whose only job is to try to make the derived truth lie, and shipped nothing until it couldn't. Same lesson, three rungs, each trusting a person's vigilance a little less and a mechanism a little more.

I don't want to declare victory. None of this means Piper can't lie to me anymore. It means two specific ways it could are now closed by construction rather than by remembering, and the next one will surface the way both of these did, sideways, while someone's looking at something else. What I'm claiming is narrower than "we fixed it" and, I think, more durable: we got a little better at telling the difference between a promise we're keeping and a promise the system keeps for us. The first kind is the one that lies.

---

*Next on Building Piper Morgan: "Drained on Paper" — we called a sprint finished, and it wasn't, and the word traveled a lot further than the evidence did.*

*Where in your own systems are you still trusting a list, a justification, or a decision on file to stay true on its own — and what would it take to make the thing derive that truth instead of remember it?*
