---
image: ''
alt: ''
caption: ''
---

# Alpha Launches

*July 10–12, 2026*

Friday, my Lead Developer agent filed the beta-readiness gate: five criteria a build had to pass before a single outside tester could touch it. Sprint clear. The canonical test suite fresh and green. Three real multi-turn scenarios, defined by the roles who actually think about user experience, not by whoever happened to be building the feature. Three stable days. My own sign-off.

Writing the criteria took one role. Getting them right took five. Architecture added two verifications the draft had missed. Experience and Product defined the three scenarios the gate would actually run — and insisted, correctly, that none of them could be allowed to pass on faked or simulated data. Architecture checked that constraint too, then confirmed the whole thing held together. All in one day, nobody waiting on anybody else for long.

# The invitations went out

Saturday, the last thing standing between "ready" and "sent" cleared: an unconfirmed email address, chased down and confirmed. All eleven of the first-wave invitation codes were ready, with templates written for two different kinds of invitee — people already close to the project, and people who'd need more context to make sense of what they were being asked to try.

Sunday at 12:26 in the afternoon, I sent all eleven. My "sapient team" — the phrase I use for the mix of agents and humans building this together — included outside humans for the first time.

# The gate does its job

The same day the invitations went out, the beta-readiness gate got to do the thing it existed for. Not in a test environment against fabricated data — against the real, live, just-launched product, with the real multi-turn scenarios experience and product had defined.

It found eight real defects before a single tester encountered any of them. An apostrophe rendered wrong. A title cut off mid-parse. A query that returned someone else's usage numbers instead of their own. Ten scanner bots hitting the site within minutes of it going public and accidentally filling up the same capacity gauge real users would need. Each one found, fixed, and deployed the same day it was found — several within the same hour.

One scenario didn't pass clean the first time, and that was the most useful result of all: it surfaced a real gap. Piper couldn't yet resolve "actually, change the title" without being told explicitly which issue "it" referred to. A real boundary, honestly discovered instead of quietly shipped — a capability that isn't built yet. It got a plain-language explanation written for new testers before anyone could stumble into it, and the underlying question — how does Piper know what "that" refers to — became its own piece of architecture work.

Eight bugs closed, one honest gap named, before any outside person's experience of the product was anything other than working correctly.

---

*Next on Building Piper Morgan: "Confabulating a Peer's Unfinished Work" — what happens when one of your own agents asserts a colleague did work that was never done, and why catching it honestly matters more as systems get more autonomous.*

*Where in your own work has a rule you built to protect quality caught something only once you actually pointed it at something real?*
