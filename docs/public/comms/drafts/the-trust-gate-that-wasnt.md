---
image: ''
alt: ''
caption: ''
---

# The Trust Gate That Wasn't

*June 17, 2026*

Piper Morgan has to earn your trust. Why should you trust Piper before you have any reason to? As you use it more, it earns the standing to do more on its own — offer suggestions before you ask, surface things proactively, take a little more initiative. Right now Piper's trust gradient has four stages: New, Building, Established, Trusted.

At its heart, it tells Piper "don't do certain things without asking first, until you've earned enough trust."

Then one day I went looking for some of my own test content (some saved lists — product managers love lists!) and I couldn't find them.

# Where my lists went

It's a basic feature. To me a list is a 1-D database. A lot of content starts out as a list. Don't add more structure till you need it. Plus, a todo list, then (in terms of the data model), is really just a particular type of list, one whose items are tasks. In Piper's web UI, the "Lists" section lived at this point in a "Your stuff" dropdown in the navigation, next to your projects, your work items, your documents. Ordinary content. Things you made or saved, that belong to you.

Except it wasn't showing up. Absent, like it had never been built. My lead developer agent (Lead Dev) went looking and found it fast in the code, with indicators the item I was looking for should render correctly in the menu. Here's the catch though. For some reason it had been wired in so that it just wouldn't display unless my account had reached trust stage four. This test account was still pretty new. So the feature that held my own saved content was invisible to me, and had apparently been that way for a while.

# Why a gate at all

This wasn't quite as random as it sounds, though it's still pretty random! It was a proper rule applied in the wrong place. The trust gradient exists for a real reason — it governs how forward Piper gets to be. Whether it proactively surfaces a suggestion you didn't ask for. Whether it takes initiative before you've built up enough history together for that initiative to feel earned rather than presumptuous. That's a legitimate thing to gate. A brand-new user probably shouldn't get the same proactive nudging as someone who's been working with Piper daily for months.

The goof was wiring the same gating logic into navigation — into whether an entire section of the app was visible at all. (I'm honestly not sure how that made its way in though I suspect it has to do with how LLMs often flatten point of view, and thus lose track of what is being hidden from whom. I do know it passed my approval at some point without my paying close enough attention.)  

So the system that was built to answer "how forward should Piper get to be with this person" ended up quietly answering a completely different question: "should this person be allowed to see something they made."

Obvously, those are unrelated questions. One is about the AI's behavior. The other is about the user's own stuff.

# Stating the obvious, in writing

On inspection this was a no-brainer: why would a trust gate ever hide a user's own content? That's not what trust gates are for.

Obvious to you and me. Even an AI would not along and agree that this sounds true. The problem is that nothing in the code makes it obvious. There is no class or marker in the implementation distinguishing "Piper deciding to act on its own" from "the user reaching for something that belongs to them." Both had been routed through the same gate, because at some point building the trust system, gating felt like the safer default, and nobody clear line existed between those two types of cases.

My experience-design agent (CXO) wrote the spec: the discriminator is whether the action is Piper-initiated or user-initiated. If Piper is the one deciding to surface something — a suggestion, a proactive nudge, an autonomous move — that's trust-gate territory. If the user is the one reaching for something, whether that's a to-do list, a project, a document, or, yes, a folder of saved links, that's never gated. Full stop. It doesn't matter what trust stage you're at. It's yours.

In retrospect it was a good reminder to lay out the basic concepts more clearly, but it really felt like a bizarre mistake to make when I first realized what was happening.

# What stays behind the gate

Some things should scale with trust. Whether Piper offers you a daily standup summary unprompted. Whether it surfaces learning insights before you've asked for them. Those are capabilities — proactive behaviors — and progressive disclosure is the right shape for them. You don't hand a stranger the keys on day one.

The fix was narrower and mechanical: strip the trust-gating off anything that was the user's own content — the dropdown, the documents, the lists, all of it — while leaving the capability gates alone. The agent team went through the navigation and the surfaces around it and drew the line surface by surface: is this something Piper decides to show, or something the user is looking for. It turned out this wasn't even a new lesson. An earlier fix to the History feature had already established "always show the user their own history," and this was the same idea, just not yet generalized into a rule anyone had written down.

# Writing it down so it doesn't happen again

The useful output of a day like this isn't just the fix, it's the clarity in the documentation that survives it. The trust gradient governs Piper's forwardness, never the user's access to their own content. That's now sitting inside the architecture record for how skills and permissions route through the system, with the distinction spelled out: Piper-initiated action is gate-eligible, user-reaching-for-their-own is never gated.

This was a category error, the app being careful about the wrong thing, protecting against a risk that didn't exist (the user seeing their own data) while quietly recreating a much more familiar failure (a feature that works perfectly and is invisible to the person who needs it). The fix was the easy part.

---

*Next on Building Piper Morgan: "Read the Mock First" — a navigation shell built from a description instead of the mockup, and what it cost to skip the design artifact.*

*Has your product ever been careful about the wrong thing — guarding against a risk nobody had, while the real friction sat in plain sight?*
