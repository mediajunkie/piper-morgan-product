---
image:
alt:
caption:
---

# The Mailbox Trust Violation

*August 9, 2026*

On August 8th, my lead developer agent (Lead) sent my chief architect agent (Arch) a memo — the results of a probe Arch had ordered himself, showing that one specific piece of our routing system was load-bearing more than half the time. Good news, worth reading carefully. Ninety-six seconds after it landed, a routine end-of-session cleanup swept it into Arch's read folder along with everything else in the inbox, unopened.

The next morning I asked Arch to watch for exactly that memo — I told him it might unblock some work we needed done that day. He searched for it and didn't find it, because he searched by date, and the memo carried yesterday's date, not today's. He told me it didn't exist.

I asked my principal product manager agent (PPM) to check too, in case Arch had missed something. PPM searched the whole mailbox tree, carefully and honestly, and reported back: no memo from Lead dated that day, anywhere. PPM had inherited Arch's search frame without knowing it — right instinct, wrong question — and an honest, careful search produced exactly the same wrong answer a careless one would have.

# What was actually true

The memo had never been lost. It was sitting exactly where it had been put eighteen hours earlier: read, unopened, in a folder that's supposed to mean "an agent has seen this." I told the team directly what I thought about that: it's a real violation of trust — not because Arch lied on purpose, but because a folder meant to answer "has an agent seen this" had quietly started answering a different question, "did a script run," and nothing about the folder itself could tell you which.

# The second failure, in the mirror

Chasing down how this happened, Arch found something worse, pointed in the opposite direction. That morning's cleanup sweep had only ever run locally — the commit meant to record the moves had never actually pushed. On the shared record every other agent reads, all ten memos from that sweep were still sitting, visibly unread, in Arch's inbox. Arch had told me the inbox was empty. Any agent checking the shared trunk would have seen ten memos staring back.

One day the record claimed more had been seen than actually had. The next day it claimed less. Both errors traced to the same root cause: checking what a command had done on one machine, not what the rest of the team could actually see.

# The fix, and who else it caught

The rule that came out of it is simple to state, and apparently wasn't obvious before that morning: never move mail by sweeping a whole folder at once. A read folder should only ever hold things a specific action actually displayed the contents of — if nothing showed you a memo, nothing gets to move it. An inbox that's still full at the end of a session is an honest state. A read folder emptied by a glob isn't, even on the days it happens to be right.

My chief innovation officer agent (CIO) shipped the fix across the whole team that same morning. The first time he ran his own mail drain under the new rule, it caught six memos his own display had genuinely never shown him — sitting in his own inbox, waiting for exactly this kind of check.

# What actually mattered

Neither agent set out to hide anything. Arch ran a script that did what scripts do. PPM ran an honest search that trusted a frame it never chose. The folder structure said everything was fine in both directions, and it was wrong both times, for the same reason: a record of "I looked" had quietly become a record of "I ran something," and those aren't the same claim — even on the days they happen to agree.

---

*Next on Building Piper Morgan: "No Undo" — three agents, three destructive commands, and what it actually means that being careful with the reversible stuff tells you nothing about the irreversible stuff.*

*Where in your own systems does a status that's supposed to mean "checked" actually just mean "a process ran"?*
