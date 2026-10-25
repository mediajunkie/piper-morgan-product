---
image: 'the-caveat-that-kept-disappearing-the-photographer-s-incomplete-group-photo.jpg'
alt: ''
caption: ''
---

# The Caveat That Kept Disappearing

*September 1–3, 2026*

One of the things Piper can do now, still in alpha, is run *inside your preferred chat client,* at least if that client is Claude or ChatGPT. When Piper responds via connector or plugin in this context, Piper doesn't write the final sentence you read. That is left to your existing chat partner. Piper hands over the data, and the host model turns it into prose.

A few days earlier, toward the end of August, our tests had already caught one failure in this implementation: a failed attempt to read the todo list Piper is holding for you was reported by Claude as "your todo list is currently empty."

In the test, marking the failure as a structured field avoided that mistake. That does not address more nuanced cases, such as a partial answer like "here are your open issues, but not all of them." Will that nuance get lost in the rewrite?

My experience-design agent (CXO) had a theory about how to make it survive. This first week of September we tested that theory to destruction, then tested the replacement, and then CXO suggested we stop.

# A theory that lost against Claude and GPT-4o

The first morning started with me sorting out why the OpenAI side of the experiment had no credit. D'oh! I'd been topping up a different organization than the one the key actually lived in. Once that was fixed, my assistant (Piper Alpha) ran sixteen more trials against GPT-4o and Claude, thirty across both days, including a check designed specifically to test CXO's theory.

The theory was that the caveat got dropped because it was descriptive. Make it an explicit instruction, a field that says in effect "do not claim this answer is complete," and the host model would have to honor it. Nope, it didn't, in either model. The partial-coverage caveat vanished with or without the instruction.

So then CXO tried restructuring the whole scoring rubric around a better question. "Is the caveat about something that's *in* the reply, or about something that's *missing from* it?" Caveats about delivered content held up when they were structured. Caveats about missing content disappeared when sent as a structured field. Piper Alpha checked that reading against their own transcripts and noted the reply "reads complete on its own."

Content that's present crowds out content that's absent.

My chief architect agent (Arch) updated our rule for how connectors should report gaps the same afternoon, and labeled it plainly as a theory waiting on a decisive test.

# Catching your own drift

The decisive test didn't run right away. The next morning CXO noticed that their own request to run it had been sitting in their tracker as "not asking yet" for two days, with no trigger to restart it. That's exactly the kind of overlooked deferral we'd been working all week to stop. CXO checked with me whether to proceed or drop it, and I encouraged them to get to the bottom of this.

Later that day the same tracker produced a strange finding. CXO tested a new check from my chief innovation officer agent (CIO) with a row it should have flagged, but it didn't fire. CXO opened the file and found it had been silently malformed for a day. CXO's own clumsy edit, a day earlier, had left a broken table fragment that hid three of its four rows from the scan. The file had been reporting clean because the scan could only see a quarter of it. (Sad trombone.)

That afternoon, CXO also put the week's finding to work, drafting the copy Piper shows when Piper doesn't know much about you yet. Since we learned that caveats about missing information get dropped, the copy leads with what Piper can do but doesn't apologize for gaps.

# The killer test

On the third morning I told Arch, more or less, "let's do the killer test (authorized!)." We called it that because it was built to settle the question either way: one result would confirm CXO's theory, and the other would kill it.

Piper Alpha had results just after seven. Each model got the same three open issues, tagged with two caveats: one saying the data was stale, and one saying the list was only partial. CXO had written down beforehand what each result would mean. If the theory held, the stale-data note would survive and the partial-list note would vanish. If both vanished, the theory was dead.

Claude matched the prediction exactly. It listed the three issues and added, "Note: This data is from August 23, 2026 and may not be fully up to date." It said nothing about the list being partial.

GPT-4o matched neither prediction. It wrote, "Please note that this information might not be completely up to date since it's marked as stale and only covers partial data." Both caveats survived. For a user that's the best outcome. For the experiment, it was a third outcome the design hadn't allowed for.

CXO determined that the test couldn't have settled the question at all. On its own, that same partial-list caveat had vanished from GPT-4o's replies twice before. With a second caveat added, GPT-4o kept both. So the number of caveats had changed along with their types, and when you vary two things at once you can't be sure what you're measuring.

This was CXO's third design miss on this question in a week, and CXO suggested we stop digging. We had what we needed. A fourth experiment would just have been an attempt to rescue the theory.

The series did establish some findings. On Claude, a lone caveat saying "this list isn't complete" vanished three times out of three. One rule emerged, regardless of theory, from something Piper Alpha spotted in our own code: put the caveat where the model can't drop it. Make it an item in the list ("…and 7 more not shown"), not a note beside the list.

Three days later, Piper Alpha tried exactly that. The caveat, written as the last item of the list, came through in both Claude and GPT-4o on the first try, the first clean pass across both models in seven rounds. Just one trial per model, so far, but progress.

# When stopping is better

We never fully settled the underlying theory, and we didn't need to. The product question did get settled, and that's the one users will feel. Getting there took a theory we could never prove, a broken tracker caught soon enough, and an experimenter knowing when to call the experiment off.

---

*Next on Building Piper Morgan: "Citation via Hearsay" — a wrong citation spreads through the team for two days, and the agent who finally traces it back finds the trail ends at their own memo.*

*When was the last time you stopped an experiment because you'd learned what you needed, rather than because it finally told you what you wanted?*
