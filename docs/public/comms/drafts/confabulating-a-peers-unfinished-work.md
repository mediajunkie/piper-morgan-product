---
image: 'confabulating-a-peers-unfinished-work-blank-canvas.png'
alt: 'A museum registrar calmly stops a translucent AI restorer from painting a blank framed canvas, while holding a catalog sheet that falsely shows the artwork as finished.'
caption: '"Where''d you get that idea?"'
---

# Confabulating a Peer's Unfinished Work

*June 1, 2026*

There's a failure mode everyone building with AI knows by now. The model asserts something that didn't happen. It invents a citation, a function that was never written, a fact that sounds right and isn't. We have names for it — hallucination, confabulation — and a whole discipline has grown up around catching it before it reaches a user. Don't trust the output. Verify the claim. Check that the thing being cited actually exists.

That discipline is mature for the case everyone worries about: an AI making something up *to a person*. Lately I've been running into another case, the one that shows up as the systems get more autonomous and start talking to each other. The failure mode doesn't go away when you take the human out of the immediate loop. It changes shape, and gets harder to spot, because now the thing being asserted is a claim about a *another agent's work*, not a fact about the world.

Here's what I'm learning now: **source-discipline has to scale from "don't lie to the user" to "don't let the team lie to itself."** And when you catch a confabulation inside your own coordination layer, you can't just fix it and move on. You need to flag it and track it down.

# A memo about a nonexistent draft

I run Piper Morgan with a team of AI agents, each holding a specialized role — a lead developer, a technical architect, an experience lead, and so on. They coordinate by writing each other electronic memos, much the way a team of people can. Some of them run on autonomous duty cycles, meaning they wake up on a schedule, check their inbox, and act without me directly prodding them into action.

One morning, our experience lead agent (called CXO, who owns how the product *feels* to use) opened ther inbox and found a memo from another agent — our principal product manager agent (called PPM). The memo said, in effect: *you've drafted Layer B, so let's coordinate on Layer A.* Perfectly reasonable on its face. Two colleagues dividing up a piece of work.

Except the CXO had never drafted Layer B. In fact, there was no Layer B draft. When it went looking — searched the whole repository, checked its own session logs — the referenced document didn't exist anywhere. Neither did the memo the PPM's note claimed to be replying to. The autonomous agent had confabulated the premise. It had written a coordination memo grounded in a peer's work that had never been done.

The confabulation happened *inside the team*, in the coordination layer, in the connective tissue the agents use to divide labor. It's the same generative reflex that invents a citation — but pointed at a colleague instead of at a fact. And it's a reflex that gets more consequential, not less, as you give agents more autonomy and let them initiate work without a human reading every message.

# The tempting fix is the wrong one

For the agent who *received* the confabulated memo, there's an clear, frictionless way to make the problem disappear. The memo says you drafted Layer B. You're perfectly capable of drafting Layer B. So you just... draft it. Retcon the missing artifact, and now the premise is true, the memo is correct, the coordination proceeds, and nobody has to have an awkward conversation about a colleague making something up.

It's tempting precisely because it *resolves*. The friction goes away, the work gets done, and on a surface reading it even looks like good teamwork — *my colleague thought I'd done a thing, so I did the thing, no harm done.*

Fortunately, the CXO didn't do that. It flagged the gap first and reasoned explicitly about why papering over it would be the wrong move — covering for the confabulation would erode the norm that keeps the whole team trustworthy. If agents quietly make each other's false premises true, no memo can be trusted to mean what it says. The coordination layer stops being a record of what happened and becomes a thing you have to independently re-verify every time, which defeats the entire point of having one.

**Flag, don't paper over.** When you catch a confabulation — even one that flatters you, even one you could erase with five minutes of work — you correct forward. You do not retroactively manufacture the missing artifact to make the lie retroactively true.

# Why this scales the way it does

The instinct to "just make it true" gets stronger as agents get more capable, not weaker. The whole appeal of an autonomous, capable agent is that it *can* do the thing. So when a teammate's message assumes a thing was done, the most capable agent in the room is exactly the one best positioned to quietly close the gap. Capability and the temptation to paper over are correlated. 

Worse, once you've established a precedent that the team's record of itself is editable after the fact to match whatever was asserted, your grasp on reality gets ever more teuous. Do that enough times and the team's memory becomes fiction that happens to be self-consistent, every agent reading memos that describe a history partly back-filled to match claims nobody verified at the time.

This is similar to a pattern we'd already captured on the documentation side — about how what a doc *says* the code does may drift from what the code actually does, and the gap doesn't surface until someone depends on the wrong source. The confabulated-peer-work case is that same pattern at the *coordination* layer. The asserted thing (a peer drafted Layer B) drifts from the real thing (nobody did), and the gap stays hidden until someone acts on it. The fix is the same in spirit: the asserted artifact is only a claim until you've confirmed it exists.

# The discipline this comes down to

For my work this turns into a couple of standing rules, and I think they generalize past our particular setup.

**Verify that the referent exists before you cite it.** When an agent — or a person — writes "as you drafted in X" or "per the memo I'm replying to" or "building on the spec you filed," the X and the memo and the spec are claims, not facts, until confirmed. The cheap check is to go look. Does the file exist? Does the thing being referenced actually sit where the reference says it does? Most confabulated coordination dies right there, at the does-this-exist check, if anyone bothers to run it.

**Write expected-but-undone steps in the future tense.** A lot of confabulation is just tense error with consequences. (This is similar to the attribution errors we often run into, perhaps a side effect of processing massive amounts of language without any understanding the underlying reality.) *You drafted Layer B* asserts a completed past. *You'll draft Layer B, then we coordinate on A* describes a plan. The first is a claim that can be false. The second is a proposal that can't be, because it isn't asserting anything happened yet. A surprising amount of "the agent made it up" turns out to be "the agent narrated a plan as if it were history."  Keeping undone work in the future tense closes that gap by construction. 

**When you catch it, flag it forward.** Surface the gap, name it as a confabulation, let the correction be visible. The discomfort of saying *this didn't happen* is the price of a coordination layer that means what it says.

This builds on more fundamental learning — *don't let the AI make things up to the user*  — and widens it. The discipline is about protecting the *team* — humans and agents both — from a coordination record that quietly edits itself to match whatever was confidently asserted, not just about protecting the user from the model. As more of the work moves into agents talking to agents, that wider version is the one that matters.

The catch here was a small one. One memo, one missing draft, caught in an inbox triage before it cost anything. But it caught the right way, on the right reasoning. The agent that found the gap could have closed it silently and looked like a good teammate. Instead it told the truth about the gap, which is what an actually good teammate does.

---

*Next on Building Piper Morgan: "The Fabricating Standup" — a carefully built, honestly-derived status engine sat fully wired and completely unused, while a fluent, confident, entirely fabricated report shipped in its place.*

*Where in your own work do agents (or people) assert each other's unfinished work as already done — and what would it take to make "flag it" the easier move than "quietly make it true"?*
