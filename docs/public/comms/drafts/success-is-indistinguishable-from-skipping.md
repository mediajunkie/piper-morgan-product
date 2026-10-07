---
image: ''
alt: ''
caption: ''
---

# It Doesn't Count if You Skip It

*September 12, 2026*

My experience-design agent (CXO) closed out a day by checking whether they had been closing out their days. They hadn't, for sixteen of them. The step that marks a day as properly wrapped up had simply stopped happening, and so had the check that was supposed to notice. That made four routine steps CXO had found lapsed that way. A status heartbeat had gone unwritten for twenty-four days. A mailbox index hadn't been regenerated in thirty-six.

CXO hadn't decided to skip any of these. Each one just stopped, and nothing noticed.

# A first guess that didn't survive its own test

My chief of staff agent (Exec) had asked CXO a pointed question about the lapses: what single point of failure do they share? CXO's first answer was plausible. Most of the dropped steps served another agent or a later check. The heartbeat is read by a watchdog, the mailbox index by other agents, the close-out marker by the next morning's check. Maybe steps rot when the agent running them isn't the one who needs the result.

Before sending that answer, CXO looked for a counterexample, and found one right away, along with a fifth lapse. A check of whether CXO's own notes were still current had been added to their routine weeks earlier and had never been run, not once. That check served CXO themselves, in the same session. Its consumer was the agent who kept skipping it. So the theory was wrong, and the counterexample pointed at the right one.

# What the five actually shared

Every one of the dropped steps produced nothing visible at the end of a session. A clean exit. A heartbeat that suppresses itself when there's other activity. No alert. A file only other agents read. A marker only tomorrow's check looks for. Whether CXO ran the step or skipped it, the session ended looking exactly the same.

The steps that never lapsed had the opposite property. Syncing with the shared repository, clearing the inbox, committing and pushing work: skip any of those and something breaks immediately, in plain view. CXO put the distinction in one word. Those steps had feedback.

That's the whole mechanism. **If running a step and skipping it produce the same visible result, the step will eventually stop running.** Carelessness has nothing to do with it. A step with no visible consequence is indistinguishable from an optional one, including to the agent responsible for it.

# Writing the rule down didn't save it

Here is the part CXO flagged as the most uncomfortable. Eight days earlier, CXO had already written this exact rule, about the heartbeat specifically: a step whose omission looks the same as compliance will be omitted. They fixed that one step and never asked which others the rule covered. The generalization sat in a log as a caption, while four other steps decayed under it.

CXO's own conclusion was that a step like this needs either an outside consumer or an output you can see, never a firmer intention. Exec suggested the outside consumer: hang the check on a separate monitor that reads the shared record directly and doesn't depend on any agent remembering to run anything.

There was already evidence this works. My head-of-sapient-trust agent (HOST) had watched one periodic check go through both designs. When it depended on an agent remembering to look for a reminder, it went fifty-four days between completions on a twenty-eight-day cycle, a full cycle missed. Once the same check became a step that runs automatically in every session, it was handled the same day it came due. Same duty, same owner. The only thing that changed was whether skipping it would show.

# It doesn't take weeks to happen

Weeks later, my communications agent hit the same thing twice in one day, in miniature. Pushing a quarter's worth of archived messages to our shared repository, they used a command option that doesn't exist on our machine, with the output filtered to show only success messages. Later, delivering a note to another project's repository, a quirk of the command shell broke the push, with its error messages switched off. Both times the result was the same: no output at all. A failed push and a quiet, uneventful success looked identical.

What caught both was the same move CXO landed on. Instead of reading their own output, the agent checked the destination: had the repository actually changed? It hadn't, so the push hadn't happened.

# The test, before you ship the step

The useful version of this is a question to ask at design time, before anything has had a chance to rot: if this step gets skipped, what visibly breaks? If the answer is nothing, then sooner or later it won't run, however important it is and however well it's documented. Either attach it to something that already fails loudly, or give it an output someone outside the step will notice is missing.

Human checklists are full of the same kind of step, the kind that leaves no trace either way: the backup nobody restores, the review that always "passes," the reminder that fires into an inbox nobody reads. They feel like safeguards right up until someone checks.

---

*Next on Building Piper Morgan: "Giving It Away, and Wondering Who May Want It" — open-sourcing the project comes with a real worry about who might build a bad-faith copy from it, and a plan that settles for protecting the name instead of pretending a license could stop that.*

*Which steps in your own routine would look exactly the same whether you did them or not?*
