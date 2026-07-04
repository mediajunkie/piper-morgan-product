---
image:
alt:
caption:
---

# The Trust Gate That Wasn't

*June 17, 2026*

Piper has a trust system. As you use it more, it earns the standing to do more on its own — offer suggestions before you ask, surface things proactively, take a little more initiative. Four stages: New, Building, Established, Trusted. It's a sensible idea. Don't let a brand-new AI assistant start acting forward with someone who just met it.

Then one day I went looking for my own saved lists and couldn't find them.

# Where the lists went

The feature is small: a "Lists" section — collections of things you've saved, the same idea as any bookmarks folder. It lived in a "Your stuff" dropdown in the navigation, next to your projects, your work items, your documents. Ordinary content. Things you made or saved, that belong to you.

Except it wasn't showing up. Not broken, not crashed — just absent, like it had never been built. My engineering agent went looking and found it fast: the item was there in the dropdown menu, present in the code, rendering correctly. It just wouldn't display unless my account had reached trust stage four. I was below that. So the feature that held my own saved content was invisible to me, and had apparently been that way for a while.

[FACT-CHECK NOTE for PM: confirm the "Lists" feature label — the source logs call it "Collections" in the code/nav label at the time of the bug, later renamed to "Lists" to match the /lists URL and match what users would actually call it. Worth confirming that's the framing you want, since the piece uses "Lists" throughout for readability.]

# Why a gate at all

To be fair to the system, this wasn't a random bug. It was a rule applied in the wrong place. The trust gradient exists for a real reason — it governs how forward Piper gets to be. Whether it proactively surfaces a suggestion you didn't ask for. Whether it takes initiative before you've built up enough history together for that initiative to feel earned rather than presumptuous. That's a legitimate thing to gate. A brand-new user probably shouldn't get the same proactive nudging as someone who's been working with Piper daily for months.

The mistake was that the same gating logic got wired into navigation — into whether an entire section of the app was visible at all. So the system that was built to answer "how forward should Piper get to be with this person" ended up quietly answering a completely different question: "should this person be allowed to see something they made."

Those are not the same question. One is about the AI's behavior. The other is about the user's own stuff.

# The principle, once it was named

When my engineering agent flagged it, my reaction was pretty immediate: why would a trust gate ever hide a user's own content? That's not what trust gates are for.

Once you say it out loud, it seems obvious. But it wasn't obvious in the code, because nothing in the implementation distinguished "Piper deciding to act on its own" from "the user reaching for something that belongs to them." Both had been routed through the same gate, because at some point building the trust system, gating felt like the safe default, and nobody had drawn the line between the two cases.

My experience-design lead did the work of drawing it precisely: the discriminator is whether the action is Piper-initiated or user-initiated. If Piper is the one deciding to surface something — a suggestion, a proactive nudge, an autonomous move — that's trust-gate territory. If the user is the one reaching for something, whether that's a to-do list, a project, a document, or, yes, a folder of saved links, that's never gated. Full stop. It doesn't matter what trust stage you're at. It's yours.

[CONSIDER: this is a natural spot for a line about what it felt like to discover this about your own product — annoyance, amusement, something else? A short first-person beat here would land well given the voice guide's "admits mistakes" pattern.]

# What stayed gated, and why that's different

Fixing the principle didn't mean ripping out every gate in the system. Some things really should scale with trust. Whether Piper offers you a daily standup summary unprompted. Whether it surfaces learning insights before you've asked for them. Those are capabilities — proactive behaviors — and progressive disclosure is the right shape for them. You don't hand a stranger the keys on day one.

The fix was narrower and, once named, mechanical: strip the trust-gating off anything that was the user's own content — the dropdown, the documents, the lists, all of it — while leaving the capability gates alone. My team went through the navigation and the surfaces around it and drew the line surface by surface: is this something Piper decides to show, or something the user is looking for. It turned out this wasn't even a new lesson. An earlier fix to the History feature had already established "always show the user their own history," and this was the same idea, just not yet generalized into a rule anyone had written down.

# Writing it down so it doesn't happen again

The useful output of a day like this isn't just the fix, it's the sentence that survives it. The trust gradient governs Piper's forwardness, never the user's access to their own content. That's now sitting inside the architecture record for how skills and permissions route through the system, with the distinction spelled out: Piper-initiated action is gate-eligible, user-reaching-for-their-own is never gated.

There's a coda worth including, because it came from the person whose job is literally to watch for trust failures. Gating correctly isn't the same as being transparent about the gate. If Piper declines to do something proactively because the trust stage isn't there yet, staying silent about it is its own small trust problem, even when withholding the action was the right call. Better to say, in effect, "there's a stage-gated thing here and you're not there yet," than to just quietly not do it and leave the person wondering.

# What this one is really about

None of this shipped as a headline feature. Nobody demoed "you can now see your own lists." It's the kind of fix that only exists because someone went looking for something ordinary and it wasn't there, and then somebody else asked the right question about why.

The trust gate wasn't a security bug and it wasn't a UX bug in the usual sense. It was a category error dressed up as caution — the app being careful about the wrong thing, protecting against a risk that didn't exist (the user seeing their own data) while quietly recreating a much more familiar failure (a feature that works perfectly and is invisible to the person who needs it). The fix wasn't complicated once the category was named correctly. That's usually how these go.

---

*Next on Building Piper Morgan: "Read the Mock First" — a navigation shell built from a description instead of the mockup, and what it cost to skip the design artifact.*

*Has your product ever been careful about the wrong thing — guarding against a risk nobody had, while the real friction sat in plain sight?*
