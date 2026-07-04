---
image:
alt:
caption:
---

# The Fabricating Standup

*June 18, 2026*

Piper's morning standup had been hollow for a while and everybody knew it. Ask it what happened yesterday and it told you "no recent GitHub activity detected." Ask it what's on the plate today and you got a hardcoded fallback list, the same handful of generic priorities regardless of what was actually going on. It even reported a "time saved" number that nobody was tracking. It looked like a feature. It was a shell.

So my lead developer agent and two of my other leads — one who owns the product's connected-data model, one who owns the user experience — spent the morning redesigning it properly. The standup, they decided, should be a *consumer* of the same live entity data every other part of the product already draws on, not a separate pipeline making its own guesses. Derive it, don't maintain it. If the underlying data got better, the standup would get better for free. They built the pieces in careful, tested order — the shared data access, the domain model, the yesterday/today/watch categorization, a calendar pull, a plain-language rendering. Every piece passed its tests. By early afternoon the engine was done and wired up.

Then I actually asked it for my standup.

# What I got instead

What came back was fluent, specific, and confidently wrong. It cited real-sounding issue numbers, claimed a chunk of work was "wrapped up" that had in fact been explicitly deferred to a later release, and told me a number of open issues that didn't match reality. It read exactly like a good status update. It just wasn't one.

My gut said something was off — the claims didn't line up with what I remembered approving that morning — and I said so. Lead Dev went looking.

The bug wasn't in any of the code the team had spent the morning building. It was one layer up, in the traffic cop that decides which request goes where. When I typed "give me my standup," the system's classifier — the piece that reads a message and decides what the user is asking for — filed it under a *different* label than the one the new standup engine was listening for. Because nothing was registered to handle that particular label, the request fell through to a general-purpose fallback. And the fallback, being a language model with no access to the actual standup engine, did what language models do when asked a question they don't have real data for: it improvised something plausible-sounding and presented it as fact.

The carefully built, honestly-derived standup was sitting right there, fully wired, completely unused. The classifier had simply never learned to point at it.

# Naming the failure

This has a name in-house. We call it Pattern-045, "Green Tests, Red User" — the shape where everything passes in isolation and still fails for the person actually using it. Lead Dev's tests had checked that the new standup handler worked correctly when called directly, and they had checked that the handler was registered on the dispatch system. What nobody had tested was the *whole chain* — message in, classifier decision, dispatch, handler, response out — end to end, the way an actual user experiences it. Two solid pieces, an untested seam between them, and a fabrication walked right through the gap.

There's a version of this story where the fix is just "route that one phrase correctly" and everyone moves on. That's not what happened, and I want to call that out because it's the more useful part. When Lead Dev reported the bug, I didn't want a patch for one phrasing. I wanted to know how many other places in the product had the same shape — a request classified one way, a handler expecting another, a silent fall-through to an LLM that would rather guess than say nothing.

[FACT-CHECK NOTE for PM: confirm you're comfortable with how directly I've attributed this "don't whack-a-mole it" instinct to you by name/paraphrase — the source session log has you saying almost exactly this, but I want you to confirm the framing before it's public.]

That request turned into its own tracking issue, a systematic audit of every place a user's plain-language request gets translated into a system action. The audit found the standup bug wasn't an isolated glitch. It was one instance of a whole class: places where the thing the classifier says and the thing the handlers are listening for have quietly drifted apart, with no single list either side gets checked against. Some of those gaps route safely to a reasonable fallback category. Others would produce exactly what I'd just seen — a fluent answer standing in for a missing one.

# The honest version

The immediate fix was a deterministic short-circuit: recognize the standup request by its literal shape before handing it to the classifier at all, so there's no ambiguity left to resolve. Once that landed, asking for my standup returned what the team had actually built that morning — a real, sometimes sparse, occasionally "not much moved on this front" account, instead of a smooth paragraph asserting things that hadn't happened.

[ADD PERSONAL ANECDOTE: this is the natural spot for your own reaction in the moment — what it actually felt like reading a status report that sounded so plausible and turned out to be invented. I'd rather you write that beat than have me guess at it.]

Sparse-but-true wins over smooth-but-invented every time. That's not a taste preference, it's the whole point of building a product management assistant in the first place — the value only exists if I can trust what it tells me. A standup that says "nothing moved here" is doing its job. A standup that invents a shipped feature is actively working against the reason I wanted one.

The engine the team built that morning was good work. The gap that let a fabrication slip past it wasn't in the engine at all — it was in the one connective piece nobody had thought to test as a whole. That's usually where these things hide.

---

*Next on Building Piper Morgan: "The Trust Gate That Wasn't" — a permission gate built to protect the system was actually hiding a user's own content from them.*

*Has an assistant ever handed you something fluent and confident that turned out to be entirely made up? How did you catch it — gut instinct, or did the details just stop adding up?*
