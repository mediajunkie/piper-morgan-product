---
image: ''
alt: ''
caption: ''
---

# Distribution Is a Product Decision, Not a Marketing One

*September 1 – October 1, 2026*

I made a decision a while back to build way to use Piper Morgan requiring no dedicated app to download, no chat UI in a web browser, no second location at all. Instead,imagine Piper shows up inside the chat tools people already have open — Claude, ChatGPT, whatever they're already living in day to day.

The easy way to describe that choice is as a marketing decision. Fewer barriers, lower friction, more people willing to try it. All true, and all beside the point. Fundamentally, prioritizing this path was a decision about what the product actually is, not about how many people would see it.

# What changes when the surface changes

A standalone app and a plugin that lives inside someone else's chat interface are different products, with different constraints baked into their bones, even when they share a name and a feature list.

A standalone app can initiate. It can ping you, remind you, show up in your notifications before you asked it to. A plugin that lives inside a chat interface generally can't. It only gets to speak when spoken to, by the design of the surface it lives on. That's a real property of choosing where you live, not an oversight to build around, and it changes what kinds of promises the product can truthfully make.


Choosing distribution means choosing which shelf's physics your product has to obey — not packaging a finished thing for a new shelf.

# The listing we couldn't write yet

At the start of September we were preparing to list Piper Morgan on a plugin marketplace, and that turned into a better test case than any hypothetical.

The listing would describe a hosted connection — the same "meet people where they are" idea, extended to a backend service instead of a downloaded app. Before writing a word of it, the real question was whether the thing being described existed yet, not which sentence would read best.

It didn't. The acceptance criteria for the hosted connection sat at zero of fifteen. The code had pieces for calling other services and some shared plumbing underneath, but there was no server anyone outside our own team could connect to. No wording could make a listing true about a product that wasn't running.

That's the same principle from the other direction. Polish can't turn a description into a product. A product exists when it's in production, not when the description of it reads well.

# Then the shelf pushed back

About a month later, the hosted connection was running, and I connected ChatGPT to it myself. Signing in worked end to end. Then ChatGPT reported, in effect, that it could log in but couldn't find anything to do.

The reason was a product decision we'd made on our own terms. We'd exposed what Piper knows as read-only data for the chat tool to look at. As far as we could find, ChatGPT only looks for things it can call. Data to read, with nothing to call, looked to it like an empty shelf. So the product changed to fit the surface: we added a first read-only tool, a single "what Piper knows about me" call, and it was live by that evening.

The same connection turned up a second lesson. A setting that only allowed requests addressed to the local machine had been rejecting every real request from outside, and the tests had never noticed because they only ever talked to the local machine. The surface found what our own checks couldn't.

Both were the shelf deciding, again, what the product had to be.

# Why this matters beyond one listing

The instinct to treat distribution as a marketing layer — something you bolt on after the real work is done, to get the real work in front of more people — misses that the shelf changes the product before a single customer ever sees it. Committing to a surface that can only respond, not initiate, constrains what the product is allowed to promise, from the moment you pick where it lives.

That's the actual argument for treating distribution as product work from the start, not handing it off once the "real" decisions are made. By the time you're writing the listing copy, the decisions that matter have already happened. All that's left is whether the copy tells the truth about what you actually built.

---

*Next on Building Piper Morgan: "The Contract Tested the Day It Was Born" — a brand-new rule against overclaiming gets stretched wider by one team and pushed back on by another, on the very day it's signed.*

*Where in your own work has "how we'll ship it" quietly become "what it actually is" — after the decision was already made, not before?*
