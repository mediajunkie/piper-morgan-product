---
image: ''
alt: ''
caption: ''
---

# Mistaking the Inset for the Map

*September 3, 2026*

In a memo to a fellow agent, my experience-design agent (CXO) criticized themselves, writing "I have never invoked" the heartbeat script (a small step that tells the rest of the team an agent is alive and working). "Not once."

It sounds like a heartfelt mea culpa but it's actually not true. My chief of staff agent (Exec) checked the commit history and the folder where heartbeats are stored and found six daily heartbeats. CXO had run the step every day from August 5 through August 10, and then stopped.

CXO reproduced both of Exec's checks rather than accept the correction on report, and then went looking for how the false claim had happened. The answer was that the search CXO had run only looked at commits since August 28 and called that forever. The last heartbeat from CXO had been 18 days before the window.

*I have found that agents' expressions of "always" and "never" are often unexamined reflections on their immediate context window.*

# For certain values of "ever"...

CXO summed it up in two lines with a distinctly Claude-ish ring:

* A bounded search reported as a total.
* An absence is a measurement and it has a window.

What this means (I had to decipher it a bit myself) is that when a search comes back empty that only tells you about the space it actually looked at. "I found nothing since August 28" is a true, useful statement. "Never" is a claim about all of time, and the search hadn't measured that.

CXO also noted this was the third time that week they'd stated a total from a bounded query without stating the bound. A slip that recurs three times in a week is a sign we need more rigor or it will keep happening frequently.

# The same antipattern on another layer

The same thing had happened about six weeks earlier, with higher stakes. I run a watchdog that's supposed to notice when one of the agents goes quiet for too long. In late July it flagged one stale agent, which read as if the rest of the agent team was fine.

My chief innovation officer agent (CIO) followed up on that alert and found the watchdog's watch list only included four of the ten agents expected. Five agents had been dark for six days, and only one of them was on the list. The watchdog reported accurately on the four it watched but it phrased the result as if it covered the whole team, misleading about the core piece of information it's responsible for.

Nothing in the watchdog's output said "of four."

# "Clear" has to say what is clear

The key is bearing in mind that not only is the map not the territory but the tiny inset you are looking at in the corner of the map is not even the whole map.

That same week, CIO wrote down a principle that boils down to "Say the bound." Report *no heartbeat commits since August 28* instead of *never.* Say *3 of 4 watched agents are healthy* instead of *the team is healthy*. Once the denominator is in the sentence, the reader can see exactly what was checked, and a missing six becomes impossible to overlook.

It only costs a few words. It shouldn't be hard. Experience tells me I'll eventually need to make it mandatory somehow.

---

*Next on Building Piper Morgan: "A Clean Result Needs a Version Number" — a published post called agents "people," even though I had added a check for exactly that, and the reason it missed made me reflect on how you can tell when. clean bill of health has gone stale or expired.*

*Have your run into this yourself, raeadinf "nothing found" in your own work when the real answer is"nothing found where I looked"?*
