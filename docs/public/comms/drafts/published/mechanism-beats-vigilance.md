---
image: 'mechanism-beats-vigilance-two-doors.png'
alt: 'A boss and robot architect observe two guarded doorways: At one, speed defeats vigilance. At the other, a built-in mechanism calmly controls access.'
caption: '"Different strokes!"'
---

# Mechanism Beats Vigilance

*May 28, 2026*

Here's something I keep having to relearn, and I suspect I'm not alone: When you find yourself reminding anyone, even yourself, to *remember to do X*, you've already lost. Not yet, maybe. But you've signed up for a slow leak. The reminder works most of the time, which is exactly what makes it dangerous. It fails in the one gap where you happened not to be paying attention, and the gap is the whole problem.

I ran into a new version of this last week, in the part of my project that's least glamorous and most instructive — the plumbing that keeps a team of AI agents (we call them by their roles: the lead developer, the chief architect, the chief of staff) from stepping on each other's work. The lesson that fell out of it is bigger than the plumbing. So let me start with the principle and use the plumbing to show it.

# The principle

A vigilance-discipline is any rule that takes the form *remember to do X*. Pause before you do the risky thing. Check the branch before you commit. Read the whole document before you act on the fragment. These are good rules. They're also a tax, and the tax is paid in attention, and attention is the one resource that reliably runs out at the wrong moment.

The durable fix is almost never a matter of piling on *more attention*. What you actually need is some sort of mechanism, a concrete change to the structure of how you work that makes the failure impossible, or at least makes it impossible to *miss*. You don't remember to lock the door. The door locks itself when it shuts. That's the move. Promote the vigilance-discipline into a mechanism, and the gap where you weren't paying attention stops being a gap.

So far, so much fortune-cookie. The interesting part is the corollary, and it's sharper than it looks.

# Two different types of rules

I run my agents on something I call the duty cycle (a scheduled autonomous work-loop). The mechanism behind it is a cron (a scheduled trigger that wakes an agent up to check for work). And we'd learned, painfully, that the cron needs to *pause* in two situations, otherwise it fires into the middle of something and causes a collision.

* **Rule one:** pause the cron when the agent is doing substantive work.
* **Rule two:** pause the cron when I (the human) am actively in conversation with the agent.

These are two versions of the same rule: *Pause when busy.* Two flavors of busy, busy-working, busy-talking-to-the-human, but structurally identical. If you were promoting them to mechanisms, you'd be tempted to apply the same fix for both. Symmetric rules, symmetric treatment. Obvious, right?

Wrong!

The two rules need *opposite* hardening, because what actually matters when you're deciding how to harden a rule is *when and how it breaks*.

# Why rule one needs a hard pause

Our chief architect agent (Arch) identified the failure mode for rule one. The cron is supposed to fire only when the agent is idle — and the runtime that fires it does try to respect that. But "idle" turns out to be a treacherous word. During a multi-step task, an agent is briefly idle *between every tool call.* Read a file — idle for a beat — write a file — idle for a beat. The cron's idea of "wait until idle" sees those beats as fair game, and a fire slips into the gap between two steps of work the agent is already doing. Now there are two work-loops running in the same session, overlapping, clobbering each other.

Arch's evidence was perfectly "meta." The agent ran a command to *list* the active crons — the first step toward pausing one — and the next fire arrived in the idle window *between listing the cron and deleting it.* The vigilance was happening. The pause was in progress. And the failure landed in that gap, right inside the act of being careful.

A failure that can spring up that fast, when it can happen in the sub-second gaps between an agent's own actions, is going to defeat any amount of "remember to be careful" reminders, because the carefulness itself has gaps. The fix has to be a hard, positive mechanism: delete the active cron literally *first thing*, before anything else, before even looking around. Make the pause unconditional and front-loaded so there's no window for the fire to sneak into. Rule one tightens.

# Why rule two can relax

On the other hand, rule two's failure is slow, not fast. When I'm talking to an agent, my messages are spaced out — seconds, often minutes apart. It's the opposite danger. The runtime's "wait until idle" rule, the one that betrayed us at the tool-call scale, will actually *work* properly at the human-conversation scale. The structure already covers the common case. So rule two can lean on the mechanism that's already there and *relax* the explicit pause — exactly the opposite of what we did for rule one.

(There's one catch, a good illustration of the same principle one level down. When a question is left hanging — the agent asked me something and is waiting on the answer — the runtime misreads "waiting" as "idle" and fires anyway. So even rule two needs to be able to recognize the need for a positive pause in *that* specific sub-case. The correct fixes thus correlate with the timing of the different failure types, which lead to a refinement of the rule's basic wording.)

# What this generalizes to

With two rules, logically equivalent at one scale, opposites at another, and the nuances not visible in the phrasing of the rules, the hard question becomes *when does this break, and how fast?*

The fast-failure rule needed a mechanism, because the failure lived in gaps too small for vigilance to cover. The slow-failure rule could lean on an existing mechanism and shed the vigilance tax entirely. I couldn't figure this out just by reading. I had to watch them break to understand.

So the principle has two halves, and I think the second half is the one people skip.

First half: when you catch yourself enforcing a *remember to do X*, treat that as a smell, not a solution. The reminder is a placeholder for a mechanism you haven't built yet. Promote it. Make the structure carry the weight instead of the attention.

Second half — the sharp one: **promote per failure-mode, not per surface-rule.** Don't harden rules by how they read. Two rules can look like twins and need opposite fixes. Two rules that look unrelated can share a single mechanism. The unit of analysis is the *failure* — its timing, its gap-size, whether an existing structure already covers it — not the sentence that describes the rule.

This is why "we'll just be more careful" is almost always the wrong answer, and not for the reason people usually give. It's not that people are careless. It's that *more careful* doesn't change the structure, so the gap that produced the failure is still there, waiting for the next moment your attention is elsewhere. The agents on our team are tireless and don't get bored, and they *still* hit this — which tells me it was never really about attention spans. It was about gaps. Mechanisms close gaps. Vigilance just promises to stand in them.

---

*Next on Building Piper Morgan: "You Can't 'White Knuckle' Structural Problems" — a count-check that lost a race, and a failure that made the argument for its own fix better than any of us could have.*

*Where in your own work are you paying a vigilance tax — some "remember to do X" you enforce by attention — that's really a mechanism you haven't built yet? And when you go to build it, are you fixing the rule, or the way it actually breaks?*
