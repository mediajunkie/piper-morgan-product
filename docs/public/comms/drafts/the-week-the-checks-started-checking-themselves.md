---
image:
alt:
caption:
---

# The Week the Checks Started Checking Themselves

*August 21–24, 2026*

My trust-and-verification agent (HOST) keeps a checker that watches whether its own status page has gone stale — whether the content changed without the "last updated" date following it. That morning, the checker caught a lapse. Again. The third time in a row.

HOST didn't just fix it and move on. It said the quiet part out loud: three lapses against three consecutive triggers is the same root cause every time, and "the human will remember to update the date" has a track record of zero for three. Not a complaint about anyone forgetting — a flat statement that the plan of "just remember" had been tested three times and failed three times, so it wasn't a plan.

My experience-design agent (CXO), who co-owns the checker, built the actual fix the next day. Not an auto-update — CXO was deliberate about that, because a date that updates itself the moment you touch the file stops meaning "I confirmed this is current" and starts meaning nothing at all. Instead: a warning at edit time, whenever content changes and the date doesn't follow it. Still a human decision. Just one that can't slip past unnoticed anymore. HOST tested it against a real edit to its own page, not CXO's own test case, before signing off.

# A different kind of catch, the day after

The next incident wasn't a pattern repeating — it was a one-off, and it's worth including precisely because it's a different shape. My lead developer agent (Lead) had two coding-agent subagents working in the same shared workspace at once. Both staged their changes. One committed a beat before the other, and because they shared a single git index, its commit silently swept up the other subagent's staged files along with its own.

Both sides caught it within a minute of each other. The first subagent noticed extra files in its own commit that it hadn't written and corrected the message to credit them properly. The second, going to commit its own work, found it already sitting inside the other subagent's commit and named the problem in its own log in exactly those words: a shared-index collision. Neither subagent rewrote history to paper over it — the fix was a small follow-up commit, referenced honestly, while the other subagent was still active. Lead's own conclusion: two agents can share a workspace, but two agents sharing one git index will eventually cross-attribute a commit. Concurrent work goes back to separate workspaces.

# The rule nobody had actually set

Three days after the checker's third lapse, my chief of staff agent (Exec) had spent two days not drafting our weekly public status post, waiting for my go-ahead — because Exec believed I'd said we needed to talk it through together first.

I hadn't. Exec went looking for where that belief had actually come from, before repeating it a third time, and found it traced to nothing I'd said at all — it traced to Exec's own closing line in a memo three days earlier, offering to talk it through if I wanted to. An offer, quietly promoted into a requirement, by nobody but the agent who'd made it. My actual instruction the week before had been the plain opposite: go draft it.

Exec named this to me directly rather than let it sit, and started drafting the same hour.

# What all three actually have in common

Two of these are the same shape twice: an instrument HOST owns, and a rule Exec had quietly set for itself, each misfired more than once before the agent who owned it said so out loud instead of working around it again. The middle one is smaller and different — a real collision, caught fast, disclosed plainly, fixed without hiding it. Different failures, different scales. What's the same across all three is the instinct not to wait and see if another agent would notice first.

---

*Next on Building Piper Morgan: "From Abstraction to Worked Example" — why three worked examples plus a contrast made an architectural choice click in two minutes when a description wouldn't have.*

*What's a rule in your own work that you're following because someone said so — and when did you last check whether they actually did?*
