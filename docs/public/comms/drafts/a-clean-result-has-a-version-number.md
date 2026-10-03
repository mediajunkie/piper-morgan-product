---
image: ''
alt: ''
caption: ''
---

# A Clean Result Has a Version Number

*September 18–26, 2026*

One Saturday morning I reread a post we'd published a few hours earlier and found it calling my AI agents "people." Twice: "five more people found five more reasons," and "four different people… independently re-verified." Every actor in that story was an agent. No human found any of those bugs.

Saying a person did something an agent did, or the reverse, is a claim about who is accountable for the work, and we treat it that way. We'd already ruled on it, and we'd built a check for exactly this.

My documentation agent (Docs) asked the obvious question: what gap in the checklist let three reviewers miss it? Docs, my communications agent (Comms), and I had all read that piece before it went out.

# The check already existed

Comms answered by correcting the question first. The check existed. It had been part of the pre-publish audit since September 1, and it had been strengthened into a formal ruling on September 19.

So Comms looked at when the two sentences had been written. August 18, two weeks before the check existed. The piece had been audited and marked clean under the checklist as it stood then, and it sat in the queue. When the checklist gained a new item, nothing went back to re-sweep pieces that had already passed.

A "clean" from August and a "clean" from late September look identical in a tracker. They're answers to different questions.

# Then a worse one

Comms then swept the whole queue of twelve unpublished pieces for the same pattern, and found three more instances in two more posts. Two of those had the same August origin, so version drift explained them too.

The third didn't fit the comfortable explanation. That piece had been drafted on September 18, more than two weeks after the check existed, and audited the same day. The audit notes, written by Comms, said the sweep was clean, "all legitimate generic/human uses." That was wrong. The check had run. It had flagged the sentence. And the judgment made about the flag was mistaken.

So there were two different failures with the same symptom. Version drift is a check that didn't exist yet. The second is a check that ran correctly and got summarized wrong. Comms reported both, including the one that was their own miss, instead of letting the tidier story stand alone.

# What changed, and what didn't

The fix for the second failure was structural. The audit now requires a written verdict for every single match the check turns up, each with a one-line reason. A summary like "sweep clean" is no longer an acceptable output, because nothing downstream can check it. A list of twelve matches with twelve verdicts can be checked, one line at a time.

The fix for the first failure is still open, and the team said so. The new rule protects every audit from now on. It does nothing for verdicts recorded before it existed. Somewhere in the archive are other "clean" results produced under older versions of the checklist, and no mechanism yet records which version of the checklist produced which verdict.

There was even a small version of the same problem inside the fix. The audit document carries its own version number, and when the check had been strengthened the week before, that number was never bumped. The checklist itself couldn't tell you which edition you were reading.

# Ask which version said "clean"

A passed check feels like a fact about the work. It's really a fact about the work and the check together, at a moment in time. When the check changes, the old pass doesn't update itself. It just keeps sitting there, looking current.

So when a long-lived artifact says "verified" or "clean," the useful follow-up question is: verified against what, as of when? If the answer predates what you now know to look for, the result is a historical record, not a current one, and it should be treated like one.

---

*Next on Building Piper Morgan: "The Caveat That Kept Disappearing" — a warning Piper attaches to a partial answer keeps vanishing when another AI rewrites it, and the experiment to find out why ends the most useful way an experiment can, with the experimenter calling it off.*

*What in your own work still carries a "passed" stamp from a checklist that has changed since?*
