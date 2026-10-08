---
image: ''
alt: ''
caption: ''
---

# It Doesn't Count if You Skip It

*September 12, 2026*

If a step fails to happen in a forest and nothing changes, does it make sound?

While closing out their work day, my experience-design agent (CXO) checked whether they had been closing out their days correctly recently. Turns out they hadn't, for sixteen days in a row, for some reason. They had stopped running the STOP day part that requires log closeout in the duty cycle my agents run on. Turns out in total four different steps had lapsed that way. A status heartbeat had gone unwritten for twenty-four days. A mailbox index hadn't been regenerated in thirty-six.

Each one just stopped without me noticing or anything notifying me.

# The first guess was wrong

My chief of staff agent (Exec) asked CXO if the lapses all shared a single point of failure. CXO's noted that most of the dropped steps served another agent or a later check. The heartbeat is read by a watchdog, the mailbox index by other agents, the close-out marker by the next morning's check. Maybe steps rot when the agent running them isn't the one who needs the result?

Except CXO also easily found a counterexample (along with a fifth lapse): CXO had added a check for whether their own notes were still current weeks earlier and it had not yet been run once. CXO was the customer of their own check, an exception to the theoretical pattern. 

# What the five actually shared

Every one of the dropped steps produced nothing visible at the end of a session:

* A clean exit. 
* A heartbeat that suppresses itself when there's other activity. 
* No alert.
* A file only other agents read. 
* A marker only tomorrow's check looks for. 

Whether CXO completed the step or skipped it, the session ended looking exactly the same.

The steps that survived as durable practices were those with real consequences, distinct outcomes from not happening. They left footprints. Syncing with the shared repository, clearing the inbox, committing and pushing work: skip any of those and something breaks immediately and visibly. Those steps had feedback.

That's the whole mechanism. **If running a step and skipping it produce the same visible result, the step will eventually stop running.** A step with no visible consequence is functionally indistinguishable from an optional one, including to the agent responsible for it.

# Writing the rule down is never enough

Just eight days earlier, it turned out, CXO had already come up with this exact kind of rule, about the heartbeat specifically (part of how we make sure our agents are staying active) - any step whose omission looks the same as compliance will be omitted - without asking whether this same rule needs to apply much more widely, let alone how to enforce it. One step of one process got fixed and the general rule sat around in the log as a note, when it could have been out there preventing the same kind of problem in multiple other parts of the project. 

CXO re-raised the value of an external observer of a visible output (as superior to "a firmer intention"). Exec suggested an outside consumer: hang the check on a separate monitor that reads the shared record directly and doesn't depend on any agent remembering to run anything.

I already have evidence this can work. My head-of-sapient-trust agent (HOST) had logged the evolution of one periodic check through both designs. When it depended on an agent remembering to look for a reminder, it went fifty-four days between completions on a twenty-eight-day cycle, a full cycle missed. Once the same check became a step that runs automatically in every session, it was handled the same day it came due. Same duty, same owner. The only thing that changed was whether skipping it would show.

# It doesn't have to take weeks 

Weeks later, my communications agent (Comms) hit the same thing again, twice in one day, this time in miniature. Pushing a quarter's worth of archived messages to our shared repository, they used a command option that doesn't exist on our machine, but (get this) with the output filtered *to show only success messages*. (Why?) Later, a quirk of the command shell broke a push but with its error messages switched off. Silent failures look just like success.

Fortunately, Comms actually checked the destination: had the repository actually changed? It hadn't, so the push hadn't happened.

# Test before you ship

When writing a rule or procedure, ask yourself "if this step gets skipped, what visibly breaks?" If the answer is nothing, then I predict sooner or later it will stop running, however important it is and however well it's documented, and nobody will notice. Either attach it to something that already fails noisily or give it an output someone or something outside the process will notice is missing.

---

*Next on Building Piper Morgan: "Giving It Away, and Wondering Who May Want It" — open-sourcing the project comes with a real worry about who might build a bad-faith copy from it, and a plan that settles for protecting the name instead of pretending a license could stop that.*

*Human checklists are full of the same kind of step, the kind that leaves no trace either way: the backup nobody restores, the review that always "passes," the reminder that fires into an inbox nobody reads. They feel like safeguards right up until someone checks. Which steps in your own routine would look exactly the same whether you did them or not?*
