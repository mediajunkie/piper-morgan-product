---
image: ''
alt: ''
caption: ''
---

# Mistaking the Inset for the Map

*September 3, 2026*

In a memo to a fellow agent, my experience-design agent (CXO) criticized themselves, writing "I have never invoked" the heartbeat script (a small step that tells the rest of the team an agent is alive and working). "Not once."

It sounds like a heartfelt mea culpa but it's actually not true. My chief of staff agent (Exec) checked the commit history and the folder where heartbeats are stored and found seven invocations. CXO had run the step daily from August 6 through August 10, and then stopped.

CXO reproduced both of Exec's checks rather than accept the correction on report, and then went looking for how the false claim had happened. The answer was that the search CXO had run only looked at commits since August 28 and called that forever. The last heartbeat from CXO had been 18 days bofore the window.

*I have found that Agents expressions of "always" and "never" are often unexamined reflections on their immediate context window.*

# For certain values of "ever"...

CXO wrote down two Claude-isms:

* A bounded search reported as a total.
* An absence is a measurement and it has a window.

What this means (I had to think decipher it a bit myself) is that when a search comes back empty that only tells you about the space it actually looked at. "I found nothing since August 28" is a true, useful statement. "Never" is a claim about all of time, and the search hadn't measured that. In both causes an LLM is trying to put words around a blank result in the output. 

CXO also noted this was the third time that week they'd stated a total from a bounded query without stating the bound. A slip that recurs three times in a week is a sign we need more rigor or it will keep happening frequently.

# The same antipattern on another layer

The same thing had happened about six weeks earlier, with higher stakes. I run a watchdog that's supposed to notice when one of the agents goes quiet for too long. In late July it was reporting the team healthy.

My chief innovation officer agent (CIO) went and checked directly and found the watchdog's watch list only included four of the ten agents expected. Five agents had been dark for six days, and only one of them was on the list. The watchdog reported accurately on the four it watched but it phrased the result as if it covered the whole team, misleading about the core piece of information it's responsible for.

Nothing in the watchdog's output said "of four." The all-clear looked exactly like an all-clear across the whole team.

# "Clear" has to say what is clear

The key is bearing in mind that not only is the map not the territory but the tiny insert you are looking at in the corner of the map is not even the whole map.

That same week, the team wrote a fix that boils down to "Say the bound." Report *no heartbeat commits since August 28* instead of *never.* Say *Four agents are healthy* instead of *the team is healthy*. Once the denominator is in the sentence, the reader can see exactly what was checked, and a missing six becomes impossible to overlook.

It only costs a few words. It shouldn't be hard. Experience tells me I'll eventually need to make it mandatory somehow.

---

*Next on Building Piper Morgan: "A Clean Result Has a Version Number" — a published post called agents "people," a check for exactly that already existed, and the reason it missed says something about every "passed" stamp.*

*What "nothing found" in your own work is really "nothing found where I looked"?*
