---
image: ''
alt: ''
caption: ''
---

# Measure the Start, Not the End

*September 29 – October 1, 2026*

My agents wake themselves up on a schedule. For most of this year that schedule ran on the scheduler built into the coding tool they live in: "fire at 6:12, 9:12, 12:12," and so on through the day. And for weeks, several of them had noticed the same oddity. Their fires seemed to land about half an hour late.

The question was what "late" meant. Every agent records a small heartbeat at the end of each fire, and those end-of-fire timestamps kept showing up around thirty minutes after the scheduled slot. That could mean the scheduler was dispatching thirty minutes late. It could also mean the scheduler was punctual and the agent spent thirty minutes working before they wrote the heartbeat. Both stories produce the identical number.

# Several seats, one kind of evidence

My assistant agent (Piper Alpha) and my documentation agent (Docs) each saw the same thirty-minute pattern in their own logs. My chief of staff agent (Exec) pulled the same pattern from a third agent's heartbeats. The agent who runs our infrastructure host (Pard) was assembling the case. Several agents, one pattern, which sounds like strong evidence.

Exec declined to treat it that way. Passing the raw numbers along, Exec explicitly refused to say what they meant: agreement across seats that share one unexamined assumption is the very failure mode the team had already named. Every one of those readings came from an end-of-fire marker, so every one carried the same ambiguity, and agreeing with each other made them louder without making them more informative. Pard had already built and thrown out a month of pooled heartbeat data for a different flaw, mixing readings from different schedules. More of the same kind of measurement wasn't going to settle anything.

# A different instrument

What settled it was a habit of my communications agent (Comms), one that hadn't been built for this question at all. Comms runs a clock check as the very first command of every fire, before reading mail or touching anything else, and writes that time into their log.

That's a start time, measured directly. Across eleven fires, Comms' first command ran at 39 to 42 minutes past the hour for slots scheduled at 12 past. And those fires were short. Most finished under a minute or two after that first reading. So the half hour was elapsing before the fire began. It couldn't be work, because nothing had started yet.

The scheduler's own documentation says recurring jobs can run late by up to a tenth of their period, capped at fifteen minutes. On a three-hour schedule, that's a fifteen-minute ceiling. These fires were consistently running at about twice that.

The same week, Comms moved onto a different scheduler, one that lives in the operating system instead of the coding tool. The first fire under it began at 12:19 for a 12:19 slot. The next ones began on the minute too.

# Why the end-marker couldn't answer

An end-of-fire heartbeat answers the question it was built for: did this agent finish a fire, and when? The trouble came from asking it a different question, about when the fire began, that it structurally couldn't answer. Lateness and duration both add to the same end time, and no number of readings can separate two things that always arrive summed together.

Pard's summary named what had changed: the evidence was "no longer the same kind in four copies." Comms supplied a different measurement, aimed at the actual question, where another reading of the end time would only have added a fifth copy.

Comms also stated the limit plainly instead of letting the clean number carry more than it should. Their fires are quick partly because most of them are quiet. A fire doing real editorial work can run ten or twenty minutes. But that time lands after the start reading, which was the only thing the question needed.

# The habit worth stealing

When several observers agree, it's worth asking what their readings have in common before counting them. Shared instruments produce shared blind spots, and more of the same reading only makes the agreement look stronger without making it more informative.

And when a number could mean two things, look for a measurement placed somewhere the two explanations come apart, rather than collecting more of the same number. Here that place was a single clock check at the top of each fire, written down before anything else happened.

---

*Next on Building Piper Morgan: "The Feature That Was Never Real" — a feature everyone believed was working turns out, on inspection, to have never functioned once in fifteen months.*

*Where in your own work are several people agreeing because they're all reading the same gauge?*
