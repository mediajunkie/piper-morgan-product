---
image:
alt:
caption:
---

# The Architecture That Wrote Its Own Case

*May 28, 2026*

There's a kind of failure you can't fix by trying harder. You've already tried harder. You were careful. You did the thing the careful person does — checked, double-checked, built a little ritual to catch the mistake before it happened. And it happened anyway, in the gap your ritual couldn't reach.

When that happens, the failure is telling you something. The problem isn't in the person. It's in the structure. And no amount of additional vigilance will close a gap that vigilance, by its shape, can't see into.

I want to talk about how you recognize that moment, because it's easy to spend weeks on the wrong fix first. And then about a happier thing that tends to follow: once a problem is genuinely architectural, the evidence for fixing it usually starts piling up on its own, if you let it.

# The count-check that lost the race

Here's the small, sharp example that made this click for me.

We run a lot of agents — colleagues, in our setup, each working in the same shared repository. For a while they all committed to the same trunk, what we call shared main (the single line of history everyone writes to). When two agents commit at nearly the same moment, their work can tangle. One agent's files land under another's commit message. Nothing gets lost, exactly, but the history scrambles and somebody has to untangle it.

So the careful agents developed a ritual. Before committing, count your files. *I'm about to commit exactly one file — my own log.* Verify the count, then commit. A clean, sensible discipline.

One morning an agent did exactly that. Counted its files — one. Then ran the commit. And the commit captured *eight* files, not one, because a second agent had staged seven files of its own into the shared workspace in the sliver of time *between the count and the commit.*

Read that sequence again, because the whole insight is hiding in the timing. The agent counted correctly. The count was *true* when it ran. And then it stopped being true a half-second later, before the commit fired. The ritual worked perfectly and protected nothing.

This is where you have to be honest with yourself. The obvious next move — the one I'd reach for if I weren't paying attention — is *count more carefully.* Count again, right before the commit, to shrink the gap. But you can't shrink it to zero. There's always *some* interval between "I checked" and "I acted," and a concurrent process can always slip into it. The fix isn't a tighter ritual. There is no tight-enough ritual. The fix is to stop sharing the workspace at all — to give each agent its own isolated checkout, a worktree (a private copy of the repository where no one else's commits can race yours).

That's an architectural fix, not a discipline fix. And the count-check is what proved it had to be, by failing in the one way that more discipline couldn't have prevented.

<!-- [PM VOICE-PASS: this section restates "mechanism beats vigilance," which is the standalone paired insight (publishing the day before). If you keep both as a pair, consider compressing this section to a one-line reference so the two pieces don't re-derive the same concept — or reorder so this lands first. Your call.] -->
# Mechanism beats vigilance

We ended up naming the general version of this, because it kept showing up. The shorthand we landed on is *mechanism beats vigilance.*

The idea is simple to state and hard to internalize. When you find yourself relying on people to *remember* to do something — remember to check, remember to update, remember to not-do the dangerous thing — and it keeps getting missed *despite genuinely careful people*, that's the signal. The discipline has earned a promotion. It should stop being a thing held in someone's head and become a thing the system enforces structurally, so that forgetting isn't possible.

The tell is the phrase "but they were being careful." If a failure only happens to careless people, more care fixes it. If it happens to careful people — people who built rituals specifically to prevent it — then care is not the missing ingredient. Structure is.

This cuts against a reflex I have, which is to answer a mistake by resolving to be better next time. Sometimes that's right. But "I'll be more careful" is a fragile fix, and it's *especially* fragile when the failure lives in a timing gap, a race, an interruption — anywhere it can happen *between* two correct actions rather than *during* a wrong one. You can't be vigilant about the space between your own footsteps.

So the question I've started asking when a failure recurs: *did this happen because someone wasn't careful, or in a place carefulness can't reach?* If it's the second one, stop tuning the ritual. Move the fix down a layer, to where the structure lives.

# When the evidence writes itself

Here's the part that surprised me, and that I think is the more useful half of this.

Once a problem is genuinely architectural — once it lives in the structure and not in anyone's attention — it tends to *recur on its own,* independently, in places that have nothing to do with each other. And if you happen to be in the window after someone has proposed the structural fix but before the team has actually adopted it, you get to watch the evidence accumulate without lifting a finger.

That's exactly what happened with the shared-workspace problem. The morning the worktree-isolation fix was on the table — proposed, argued, not yet universally adopted — the same failure showed up in *four* different agents' work over the course of a single day, each one independent, each one a different agent hitting the same structural edge in a different way.

Nobody staged that. Nobody was running a demo to make the case. The architecture was simply doing what architectural problems do — failing reliably, at its own structural rate, regardless of who was at the keyboard or how careful they were being. By the end of the day the case for the fix wasn't a memo anymore. It was a small mountain of independent incidents, all pointing the same direction.

I'd been prepared to *argue* for the change. The argument turned out to be unnecessary, because the failure argued better than I could. Four agents, four contexts, one structural cause — that's a more convincing brief than any analysis, because nobody can accuse it of being motivated. The evidence had no agenda. It was just the structure, repeating.

# The two things to watch for

So there are two halves to this, and they fit together.

The first is a diagnostic. When a failure keeps recurring *past your best discipline* — when careful people with good rituals keep hitting it — believe the failure over your instinct to try harder. It's pointing at the layer where the fix belongs. Usually that's a layer below the one you're working at. The race between the count and the commit doesn't get fixed at the count. It gets fixed at the workspace.

The second is a heuristic for *when the structural change is worth the cost,* because structural changes are never free — isolating every agent into its own worktree meant new workflows, new failure modes, a stack of small adjustments. The heuristic: watch whether the evidence is accumulating on its own. If you have to manufacture the case — stage a demo, construct a hypothetical, argue from first principles — maybe the problem isn't biting hard enough yet to be worth the disruption. But if the same failure keeps surfacing independently in three or four places in a short window, with nobody trying to make it happen, the architecture has already decided for you. It's making its own case, more cleanly than you could.

The work, at that point, isn't to win the argument. It's to notice that the argument is already over, and to stop spending vigilance on a gap that only isolation can close.

---

*Next on Building Piper Morgan: "The List That Lies" — a milestone that was never created, a door that was never supposed to open, and the same failure wearing two different outfits.*

*Where in your own work are you spending vigilance on a gap that more care can't close — and is the evidence for the structural fix already piling up while you keep tuning the ritual?*
