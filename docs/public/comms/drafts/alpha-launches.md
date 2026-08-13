---
image: ''
alt: ''
caption: ''
---

# Alpha Launches

*July 10–12, 2026*

A small band of intrepid folks have volunteered since last winter to test the janky alpha version of Piper Morgan by cloning the repo and braving the manual installation flow in a "works on my machine" environment. So in a sense the software has been "in alpha" since then, but a while ago I realized that we weren't going to get really useful feedback until I could host the app and send testers a logon code (aka, "hosted alpha") 

Now, on a Friday, my Lead Developer agent tested against five criteria a build had to pass before a single outside tester could touch it. 

1. Sprint clear. 
2. The canonical test suite fresh and green. 
3. Three real multi-turn scenarios, defined by the roles who actually think about user experience, not by whoever happened to be building the feature. 
4. Three stable days. 
5. My own sign-off.

Lead Dev drafted the initial criteria. The Chief Architect agent (Arch) added two verifications the draft had missed. The experience and product leads (CXO and PPM) defined the three scenarios the gate would require and insisted, correctly, that none of them could be allowed to pass on faked or simulated data. Arch double-checked the plan for constraint too, then confirmed the whole thing held together. All in one day, nobody waiting on anybody else for long.


# The gate does its job

The beta-readiness gate got to do the thing it existed for against the real, live, just-launched product, with the real multi-turn scenarios experience and product had defined.

It found eight real defects before a single tester encountered any of them. An apostrophe rendered wrong. A title cut off mid-parse. A query that returned someone else's usage numbers instead of their own. Ten scanner bots hitting the site within minutes of it going public and accidentally filling up the same capacity gauge real users would need. Each one found, fixed, and deployed the same day it was found — several within the same hour.

One scenario didn't pass clean the first time, and that was the most useful result of all: it surfaced a real gap. Piper couldn't yet resolve "actually, change the title" without being told explicitly which issue "it" referred to. Mechanisms built into the architecture long ago for anaphoric parsing (the fancy term for understanding what a dangling it, that, this, them, etc. means in context) were not working on this level.

I added it to the known issues message for new testers before anyone could stumble into it, and the underlying question re wiring, refactoring, or rebuilding that mechanism, became its own piece of architecture work.

Eight bugs closed, one known issue added, before making my generous volunteers waste time bumping into problems I clearly could have caught myself.

# The invitations go out

Saturday, all eleven of the first-wave invitation codes were ready, with templates written for two different kinds of invitee: people already close to the project and people who'd need more context to make sense of what they were being asked to try.

Sunday at 12:26 in the afternoon, I sent all eleven, my "sapient team" fully including outside humans for the first time. Up to now my Head of Sapient Trust (HOST) role has for them most part operated as an HR or PeopleOps equivalent for the agent fleet. It has already helped me track advisors, contributors, and testers for some time, but now things are really getting real. 

---

*Next on Building Piper Morgan: "Confabulating a Peer's Unfinished Work" — what happens when one of your own agents asserts a colleague did work that was never done, and why catching it matters more as systems get more autonomous.*

*Where in your own work has a rule you built to protect quality caught something only once you actually pointed it at something real?*
