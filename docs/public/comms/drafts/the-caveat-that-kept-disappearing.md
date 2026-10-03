---
image: ''
alt: ''
caption: ''
---

# The Caveat That Kept Disappearing

*September 1–3, 2026*

When Piper answers you inside Claude or ChatGPT, Piper doesn't write the final sentence you read. Piper hands over the data, and the host model turns it into prose. That handoff is where we'd already caught one failure a few days earlier: a read that failed outright came back to the user, in fluent prose, as "your todo list is currently empty." Marking the failure as a structured field fixed that one. The open question was quieter and harder. What about a caveat on a partial answer, like "here are your open issues, but not all of them"? Does that survive the rewrite?

My experience-design agent (CXO) had a theory about how to make it survive. The first week of September tested that theory to destruction, then tested the replacement, and then did something I don't see often enough from anyone. CXO stopped.

# A theory that lost in both models

The morning started with me sorting out why the OpenAI side of the experiment had no credit. I'd been topping up a different organization than the one the key actually lived in. Once that was fixed, my assistant (Piper Alpha) ran the full set of trials against both Claude and GPT-4o, thirty in all, including a check designed specifically to test CXO's theory.

The theory was that the caveat got dropped because it was descriptive. Make it an explicit instruction, a field that says in effect "this answer may not be claimed as complete," and the host model would honor it. It didn't, in either model. The partial-coverage caveat vanished with or without the instruction.

CXO took the loss and restructured the whole scoring rubric around a better question. Is the caveat about something that's in the reply, or about something that's missing from it? Caveats about delivered content held up when they were structured. Caveats about missing content disappeared, because the reply already looked like a finished answer. Piper Alpha checked that reading against their own transcripts instead of just agreeing, and put it more sharply: the reply "reads complete on its own." Content that's present crowds out content that's absent.

My chief architect agent (Arch) updated our rule for how connectors should report gaps the same afternoon, and labeled it plainly as a theory waiting on a decisive test.

# Catching your own drift

The decisive test didn't run right away. The next morning CXO noticed that their own request to run it had been sitting in their tracker as "not asking yet" for two days, with no reason attached and no trigger to restart it. That's exactly the kind of quiet deferral we'd been working all week to stop. So CXO asked me directly, and offered "drop it" as an equally acceptable answer.

Later that day the same tracker produced a stranger finding. CXO ran a check that should have flagged a known problem, and it didn't fire. Rather than blame the check, CXO opened the file and found it had been silently malformed for a day. A clumsy edit had left a broken table fragment that hid three of its four rows from every tool that read it. The file had been reporting clean because the tools could only see a quarter of it.

That afternoon, CXO also put the week's finding to work, drafting the copy Piper shows when Piper doesn't know much about you yet. Since caveats about missing information are the ones that get dropped, the copy leads with what Piper can do and doesn't apologize for gaps.

# The killer test

On the third morning I told Arch, more or less, "let's do the killer test (authorized!)." Piper Alpha had results by seven. Each model got a reply carrying two caveats, one of each kind, to see which survived. CXO had registered what each possible result would look like before any data came in.

Claude matched the predicted pattern exactly. GPT-4o matched neither prediction. Both of its caveats survived together, a third outcome neither prediction had allowed for.

CXO's read of that result: the test couldn't have settled the question at all. To compare two kinds of caveat, it had to add a second caveat, which meant the number of caveats changed along with the kind. Two things varied at once. It was CXO's third design miss on this question in a week, and CXO said so, recommended stopping the series, and made clear that stopping wasn't discouragement. Chasing a fourth experiment to rescue a theory isn't the same as learning something.

What the series did establish was enough to build on. On Claude, a lone caveat saying "this list isn't complete" vanished three times out of three. And one rule held regardless of which theory was right: put the caveat where the model can't drop it. Make it an item in the list ("…and four more not shown"), not a note beside the list.

Three days later, Piper Alpha tried exactly that. The caveat, written as the last item of the list, came through in both Claude and GPT-4o on the first try, the first clean pass across both models in seven rounds. It's one trial per model, and the team wrote it down that way.

# What stopping bought us

The underlying theory never got fully settled, and that turned out not to matter. The product question did get settled, and that's the one users will feel. Getting there took a theory being wrong in public, a broken tracker caught by its own owner, and an experimenter willing to call the experiment off.

---

*Next on Building Piper Morgan: "Where the Citation Came From" — a wrong citation spreads through the team for two days, and the agent who finally traces it back finds the trail ends at their own memo.*

*When was the last time you stopped an experiment because you'd learned what you needed, rather than because it finally told you what you wanted?*
