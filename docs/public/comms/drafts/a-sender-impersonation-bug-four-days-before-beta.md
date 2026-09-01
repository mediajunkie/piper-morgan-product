---
image: ''
alt: ''
caption: ''
---

# A Sender-Impersonation Bug, Four Days Before Beta

*August 4, 2026*

Four days before the first outside testers were due, my product-assistant agent (Piper Alpha) found something that broke my own stated rule for the forthcoming beta: no cross-user leakage on any surface a tester could reach.

The Slack connector had a real bad one. Every direct message or mention the bot received got processed as if it came from whoever had originally connected the workspace — not from whoever actually sent the message. Any member of a connected Slack workspace could DM the bot and read or write the connected owner's own to-do list, as that owner, without needing their credentials at all.

It wasn't hidden behind a flag. It ran at startup, unconditionally, the moment Slack was configured. And Slack was one of the connectors testers were being invited to try.

## The fix, and the fix's own fix

My chief architect agent (Arch) ruled the same day: block the runner from starting at all unless an explicit environment flag says it's safe to. Four lines. Simple, and correct as far as it went.

Piper Alpha (PA, for short) kept looking anyway, and found a second problem the first ruling had explicitly flagged but left for someone else to pick up: the fix stopped the runner from starting, but it didn't stop a non-admin user from overwriting the single, unscoped credential the runner reads. The write path survived the gate untouched. That became its own issue, filed the same day.

Then my experience-design agent (CXO) found a third problem nobody had been looking for. The fail-closed gate worked exactly as intended — except from the point of view of someone trying to set up the connector. Paste a valid token, and the interface reported success. Then, because the underlying connection could never actually complete while the gate was closed, the status kept re-rendering the same message on every check: *couldn't open a connection, try saving the token again.* Forever. The real reason had nothing to do with the token, and there was no way for the badge to say so.

Need I say this makes for a very frustrating experience?

CXO's framed it as a gate built to fail closed that had inherited the wording of a *different* kind of failure — the kind where trying again might actually help. It hadn't been reviewed as its own new failure mode. It had just borrowed someone else's copy.

## One word

The fix for that took the rest of the day, and most of it was deciding what to call the new state and where it belonged in the interface's list of possibilities, not writing code. Arch pointed out that whatever fixed the specific case would leave the same danger sitting in the default fallback — any *unrecognized* status, now or in some future version, would still fall through to the same falsely hopeful instructions. The real fix was flipping which message was the default — the safe, do-nothing state, not the one that invites an action that can't succeed — rather than writing a fourth message.

My principal product manager agent (PPM) settled the last piece — not the wording, but the name. CXO had proposed `unavailable`. PPM's rule, arrived at independently, in reply to CXO's own memo: a state a user cannot act on should never render as one that invites action, which happens to cover more ground than the naming question alone. They picked `disabled`, matching the underlying check that governs it, so the code and the label speak the same language rather than two.

## What four days doesn't buy you

We shipped three fixes, found in sequence by three different agents, each one looking at what the previous fix had actually done rather than trusting what it was supposed to do. The security hole closed the same day it opened. So did the smaller hole inside the fix, and the honesty problem inside that.

Four days before a launch is an anxious time to finding privacy bugs! Fortunately, we got it fixed without assuming the first patch was the end of the question.

---

*Next on Building Piper Morgan: "Repetition Isn't Convergence" — five people independently measure the wrong thing and agree with each other, and the agreement gets mistaken for proof.*

*When your own fix ships, who's still looking at what it actually changed — not what it was supposed to change?*
