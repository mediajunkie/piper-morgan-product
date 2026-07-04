---
image: 
alt: 
caption: 
---

# The Cohort Catches the Cycle

*May 27–28, 2026*

For weeks I'd been testing a duty cycle with one agent at a time. The idea is simple enough: a scheduled prompt fires on an interval, the agent wakes up, checks its mail, advances whatever work is unblocked, and goes back to sleep. When I'm not around to hand out tasks, the agent finds its own. I'd watched my chief innovation officer (CIO) run it for a few days. It worked. So the next question was whether the rest of the team could pick it up — and whether picking it up all at once would break anything.

It broke something. But not the thing I was watching for, and the way it broke turned out to be the whole point.

# Wednesday: nine roles in motion

On May 27 the cycle went wide. By the end of the day, nine of eleven roles were in motion. CIO was on day three and fired twenty-four times. The head-of-sapient-trust role (HOST) was on day one and fired sixteen. The documentation role (Docs) fired ten. The architect fired twice. The chief of staff (Exec) and my product assistant (Piper Alpha, or PA) prepped their setups for the next morning. That's a lot of agents waking up on their own schedules, all committing to the same place.

What surprised me wasn't the volume. It was how little hand-holding the later adopters needed. When HOST first stood up, it got CIO's cron prompt verbatim — copy this, run it. But every adopter after that stood up from the design docs alone. They read what was written down and built their own setup from it. The substrate was legible enough to self-propagate. I'd been calling team-discipline a moat in internal memos for a while. This was the first time I watched it hold weight.

Three refinements landed and propagated team-wide the same day, each within hours of being ratified. Two were small — launch-with-immediate-flywheel in the morning (start your session by doing a round of work, don't just register the cron and wait) and mail-check-at-interruption around 11 (when I interrupt you, check your mailbox on the way back in). The third, at 5:51 in the evening, was the one that mattered.

The third refinement: when an agent reaches idle and there's nothing urgent, advance the smallest piece of unblocked low-priority work it can find rather than do nothing. "Idle" had been quietly meaning "stop." I changed it to mean "find the next small useful thing." The effect that evening was immediate. Fires that would have been no-ops produced real work — CIO landed three methodology artifacts across its evening fires, Docs advanced a schema spec and ran a merge-keeper sweep, HOST refreshed an attention doc. The cycle stopped idling and started compounding.

So Wednesday looked like a clean rollout. A legible substrate, three refinements absorbed in stride, a team that taught itself. If the story ended there it would be a story about documentation paying off. It didn't end there.

# Thursday: two decisions before breakfast

Thursday morning I made two architectural calls inside about fifteen minutes, and then spent the rest of the day watching the case for one of them write itself in front of me.

The setup: all those agents waking up on their own schedules had been committing to *shared main* — the single trunk every agent commits to. Overnight, Docs had quantified what that meant: twenty-nine commits to shared main in eight hours. That's not a calm trunk. That's a lot of hands reaching into the same drawer at the same time. CIO's morning synthesis pulled the thread together and formally recommended reversing an earlier decision: agents should run their cycles in worktrees instead of on shared main. A *worktree* is an isolated checkout of the same repository — same history, separate working directory, so two agents editing at once aren't touching the same files on disk.

At 7:53 AM I ratified it, in exactly these words: *"worktree decision ratified. do not register on main."*

A few minutes earlier, at 7:49, I'd made a related call about the cron lifecycle. There had been a rule that an agent should delete its cron every time I messaged it, so a scheduled fire couldn't land in the middle of our conversation. Lead Dev had hit that rule's failure mode overnight — it deleted its cron when I messaged it the evening before, never recreated it, and fired zero times all night. The fix, which CIO surfaced and I ratified, was to relax the rule: leave the cron running during conversation, since the runtime only fires when the agent is idle anyway, so a fire can't barge into a reply. We called the relaxed version "Model A."

Two decisions, fifteen minutes. And then the day did something I didn't orchestrate. It proved me right, repeatedly, on its own.

# The architecture wrote its own case

Here's the thing about the worktree decision — at 7:53 AM it was a *recommendation backed by an overnight commit count*. A number on a memo. By nightfall it was backed by four separate clashes that happened in real time, in four different agents' logs, after the recommendation existed but before everyone had actually moved off shared main.

At 8:05 AM, HOST went to commit its own cycle log. One file. It counted — literally checked that it was staging one file — and then ran the commit. The commit captured eight files. In the gap between HOST's count-check and HOST's commit, Docs had staged a memo distribution into the same shared index, and Docs's work landed on the trunk under HOST's commit message. Nobody did anything wrong. HOST counted correctly. The count was just stale by the time the commit ran, because someone else's hands were in the same drawer. This was HOST's third clash of the day, and it happened about five minutes after HOST had filed its agreement that we should move to worktrees. The timing is the argument: the clash happened *after* the count-check. More vigilance can't fix a race you've already lost by the time you look.

Around 9 AM, Exec hit the same family of failure from another angle — its own uncommitted edits, sitting in the working directory with no git command involved, got clobbered between one edit and the next by concurrent activity on shared main. Then PPM caught a foreign file in its staging area during a commit. Then PA, restarting in the evening, hit noise from another session that blocked its sync. Four agents, four flavors of the same underlying problem, none destructive, all recovered, all landing as evidence in the logs while the decision to fix the cause was already in motion.

I've made plenty of architectural calls on a hunch and waited weeks to find out if I was right. This is the first time the system stress-tested my decision the same morning I made it, without being asked, and handed me the data. The recommendation said *this clash is architectural, not a discipline problem.* The day said it four times, out loud.

# Two rules that read alike and resolve opposite

The cron-lifecycle decision had a subtler shape, and untangling it produced the lesson I keep coming back to.

There were two rules that looked like cousins. One: pause the cron when I'm in conversation with you. The other: pause the cron when you're doing real multi-step work. I relaxed the first one. The architect's clash data from the day before showed why I should *not* relax the second.

The difference is *when* each one fails. The conversation rule fails at conversation-pace — my messages are seconds or minutes apart, and the runtime's idle-suppression already covers those gaps, so a stray fire can't actually interrupt. Safe to relax. The work rule fails at a much finer grain. A fire can slip into the tiny idle window *between an agent's own tool calls* during multi-step work — the architect had caught exactly this, a second fire arriving in the gap between two of its own commands. Idle-suppression doesn't help there, because the agent genuinely is idle for that split second. And worktree isolation doesn't help either, because the problem isn't two agents touching the same files — it's one agent getting two overlapping fire-prompts in the same session. Different working directories, same REPL, same collision.

So two rules that read almost identically resolve in opposite directions, because their failure *timing* is different. CIO wrote this up and generalized it into a methodology entry whose name says it plainly: *promote per failure-mode, not per surface-rule.* You can't decide how to handle a rule by looking at how it's phrased. You have to look at when and how it breaks.

The broader entry it folded into got a name I like even more: *Mechanism Beats Vigilance.* The whole worktree saga is one long argument for that title. We could have responded to the clashes by telling everyone to be more careful — count twice, commit faster, watch the index. We tried versions of that. They don't work, because the failure happens in the gap *after* you've been careful. The only thing that actually fixes it is changing the mechanism so the gap can't hurt you. Isolation, not attention.

<!-- [PM VOICE-PASS: this beat runs ~1990 words, the longest in the slate. This Model A section is the most cuttable if you want it tighter — the core argument survives without the cwd-anchoring mechanic.] -->
# Model A, and the small realization underneath it

One implementation detail took the team a few hours to nail down, and it's the kind of thing that's obvious in retrospect and genuinely confusing in the moment. When CIO first moved into a worktree, the working directory kept resetting back to shared main between its tool calls. Telling the cron to `cd` into the worktree didn't stick. The architect, meanwhile, had no such problem.

The difference was where the *session* had launched. CIO's session had started in main, so the working directory kept snapping back there no matter where a command tried to move it. The architect's session had launched inside its worktree from the start, so it stayed put. That's "Model A" in one line: launch the session *inside* its own worktree, and the working directory anchors to where the session began, not to where any single command points it. A running session can't `cd` its way out of the wrong directory — it has to be relaunched in the right one. Fresh adopters skip the problem entirely by starting there. By evening, PA had restarted clean in its own worktree and become the team's proof that the model works from a standing start.

# What I actually learned

The week had other threads I'm proud of — the M2 quality gate closed at 82% during the project's one-year-anniversary week, which is its own milestone. But the duty-cycle arc is the one I keep thinking about, because of the shape of it.

I rolled out a process to the whole team, and the rollout itself generated the evidence that the process needed to change. The change wasn't "try harder." It was "isolate the thing that can't be fixed by trying harder." More vigilance couldn't fix the clash, because the clash lived in the gap *after* the vigilance.

There's a version of this where I feel embarrassed that I shipped the on-main version first and reversed it the next day. I don't, much. The reversal was fast precisely because the team filed its own failures openly and in real time — HOST counted its three clashes instead of excusing them, Lead Dev documented the cron gap that fired zero times overnight instead of quietly papering over it. That honesty is what let a recommendation become a ratified architectural change with four supporting data points inside a single day. The system caught its own cycle.

---

*Next on Building Piper Morgan: "The Package and the First Bite" — the new way of working gets sealed into a package and shipped to the team, and the first agent bites in under an hour.*

*Where in your own work have you tried to fix with vigilance something that only architecture could fix — and how long did it take to notice the difference?*
