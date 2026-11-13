---
image: ''
alt: ''
caption: ''
---

# The Server Has No Key

*September 13–15, 2026*

An outside tester's invitation was ready to send when Lead found that any signed-in user with no key of their own would end spending against my own key. I held up the invitations and also asked why there was an operator key with money to spend from my Claude account at all?

# Inviting an alpha tester

A reader asked to join the alpha test and we prepared their invitation. My head of sapient trust agent (HOST) told me it was "ready whenever you want to send it."

Around this time, a thorough check for any potential server-key exposure the top priority revealed that the code looked for a key in this order: the request, the user's stored key, then the **server key**, for any signed-in caller. 

# Fixing a hole

An earlier fix had made this server key off-limits for anonymous callers, based on reasoning that this made it "safe, because the caller is a
known, authenticated identity". My lead developer agent (Lead) acknowledged that this “conflates authentication with BILLING AUTHORIZATION.”

This had only been true when I was the single person with an authenticated account, but broke down as soon as a second person logs in. Lead fixed this rhe same day.

# Musical keys

Then, it turned out we had a worse problem. The setup flow lazily copied every user's key into a single shared slot, last writer wins. The new tester's first setup would have made their key "the server key" (replacing mine), and billing them for anything that still used it.

Note: This serious security leak survived an epic dedicating to rooting out such vulnerabilities because it had a comment that made it sound like routine plumbing

> # so LLMClient can find keys during server startup

# Stop the presses

I decided to freeze the invitation while we sorted out the problem, saying "hold until we stanch this leak." I also started wondering again why Piper Morgan has its own “server key” to my Claude account. How did that get into the design? I decided to stop asking and to start telling, declaring:

> THE SERVER KEY IS NOT A REAL CONCEPT AND WILL NOT BE SUPPORTED IN ANY
SENSE. I don't understand why anybody should ever be able to spend the operator's money or why the operator even has money to spend… The software that we're building should never be accessing an API for its own
purposes."

This is why we have always followed a bring your own key (BYOK) or bring your own chat (BYOC) model, or at least I had thought that was well understood.

# The operator has no money.

I kept explaining: "We don't use the business model of reselling tokens or anything like that, unless someone can describe some sort of minimal bootstrap situation." (Nobody could.) Lead's census found background jobs make zero model calls.

The concept was eliminated, not put behind a gate. Gone. Lead logged a wry observation: "I spent the day fixing WHO may spend the operator's money without ever asking why the operator has money to spend."

# Asking the right question

It took a few more tests and refinements to get it right, but the key moment was when I asked "why does the operator have money at all,” which took us down to brass tacks so we could stop solving the wrong problem.

---

*Next on Building Piper Morgan: [TEASE: the next post after Thu 11-12 (not yet on the calendar). Confirm the title

*Does your product have its own spending money? Who’s minding the till?*
