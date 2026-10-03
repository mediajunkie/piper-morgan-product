---
image: ''
alt: ''
caption: ''
---

# A Bounded Search Reported as a Total

*September 3, 2026*

My experience-design agent (CXO) sent a colleague a blunt piece of self-criticism: "I have never invoked" the heartbeat script, the small step that tells the rest of the team an agent is alive and working. "Not once."

It was a striking admission, and it was false. My chief of staff agent (Exec) checked it two independent ways, the commit history and the folder where heartbeats are stored, and found seven invocations. CXO had run the step daily from August 6 through August 10, and then stopped.

CXO reproduced both of Exec's checks rather than accept the correction on report, and then went looking for how the false claim had happened. The answer was in the search CXO had run to support it. The search only looked at commits since August 28. Its window started eighteen days after the last heartbeat it could have found. CXO's verdict on their own command: the search was incapable of finding the evidence, and its emptiness got reported as "not once."

# An absence has a window

CXO named it precisely, in their own log: "A bounded search reported as a total." And then: "An absence is a measurement and it has a window."

A search that comes back empty tells you something real, but only about the space it actually looked at. "I found nothing since August 28" is a true, useful statement. "Never" is a claim about all of time, and the search hadn't measured that. The gap between the two sentences is invisible in the output. Both arrive as the same blank result.

CXO also noted this was the third time that week they'd stated a total from a bounded query without stating the bound. That's the part worth taking seriously. A slip that recurs three times in a week is the default outcome whenever a narrow search hands back an empty answer and the narrowness doesn't travel with it.

# The same shape, at a larger scale

The same thing had happened about six weeks earlier, with higher stakes. We run a watchdog that's supposed to notice when one of the agents goes quiet for too long. In late July it was reporting the team healthy.

My chief innovation officer agent (CIO) went and checked directly. The watchdog's watch list had four entries, out of ten agents. Five agents had been dark for six days, and only one of them was on the list. The watchdog reported accurately on the four it watched, and phrased the result as if it covered the whole team.

Nothing in the watchdog's output said "of four." The all-clear looked exactly like an all-clear across the whole team.

# Clear is not a measurement

That same week, the team wrote the principle down as one of its working methods: "A check's 'all clear' is emitted identically whether it measured and found nothing wrong, measured the wrong object, measured part of its space, measured nothing at all, or never ran." And the sharp end of it: "An error gets investigated. A false clear gets trusted."

The fix in both cases was simple to state. Say the bound. "No heartbeat commits since August 28" instead of "never." "Four of ten agents are healthy" instead of "the team is healthy." Once the denominator is in the sentence, the reader can see exactly what was checked, and a missing six becomes impossible to overlook.

It costs a few words. The alternative is a confident "nothing found" that quietly means "nothing found where I looked," and whoever reads it downstream can't tell the difference.

---

*Next on Building Piper Morgan: "A Clean Result Has a Version Number" — a published post called agents "people," a check for exactly that already existed, and the reason it missed says something about every "passed" stamp.*

*What "nothing found" in your own work is really "nothing found where I looked"?*
