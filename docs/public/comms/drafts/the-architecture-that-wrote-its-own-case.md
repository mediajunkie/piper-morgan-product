---
image: 'the-architecture-that-wrote-its-own-case-order-up.png'
alt: 'A restaurant manager watches as five careful chefs struggle to keep separate dishes organized on one crowded serving counter, while individual pickup shelves wait unused behind them.'
caption: '"Now don''t all jump at once!"'
---

# You Can't "White Knuckle" Structural Problems

*May 28, 2026*

There's a kind of failure you can't fix by trying harder. You've already tried harder. You were careful. You did the thing the careful person does — checked, double-checked, built a little ritual to catch the mistake before it happened. And it happened anyway, in the gap your ritual couldn't reach.

When that happens, the failure is telling you something. The problem isn't in the person. It's in the structure. And no amount of additional vigilance will close a gap that vigilance, by its shape, can't see into.

I'm starting to learn how you recognize that moment after, in some cases, spending weeks on the wrong fix first.

# The count-check that lost the race

Here's a small, sharp example that made this click for me:

I run a lot of agents in my setup, each working in the same shared repository. For a while they all committed their code changes to the same trunk, what we call shared main (the single line of history everyone writes to). When two engineers (human or bot) commit at nearly the same moment, their work can get entangled, especially if they are using wildcards to grab everything vs. diligently committing just their own changes. When this happens, one agent's files land under another's commit message. Nothing gets lost, exactly, but the history scrambles and somebody has to untangle it.

The agents had developed a ritual: Before committing, count your files. *I'm about to commit exactly one file — my own log.* Verify the count, then commit.

So on this morning an agent changed one file, ran a commit, and ended up checking in *eight* files, not one, because a second agent had staged seven files of its own into the shared workspace in the sliver of time *between the count and the commit.* This little ritual only catches errors after the fact and still lacks the discipline of only working directly on one's own changes.

The real fix isn't a tighter ritual. There is no tight-enough ritual. It's not even being super careful about only adding specific files before committing. The only durable fix is to stop sharing the workspace at all, to give each agent its own isolated checkout, a worktree (a private copy of the repository where no one else's commits can race yours). This is how human engineers already work and I should have been doing it already.

That's an architectural fix, not a discipline fix. And the count-check is what proved it had to be, by failing in the one way that more discipline couldn't have prevented.

This is precisely the pattern I called out in yesterday's post, [Mechanism Beats Vigilance](https://pipermorgan.ai/blog/mechanism-beats-vigilance/).

# When the evidence writes itself

The type of problem that is genuinely architectural, that lives on in the structure (guidelines, incentives, gaps) and not because anyone is being inattentive or careless, tends to *recur on its own,* independently, in places that have nothing to do with each other. It can take a while to recognize the same problem wearing multiple disguises, but once you clock it, you can't miss it.

It felt a bit like frequency illusion — that thing where you learn a new word and then hear it in the wild several times over the next day. Except the pattern was actually there.

That's exactly what happened with the shared-workspace problem. The morning the worktree-isolation fix was on the table — proposed, being discussed by the agents involved, not yet universally adopted — the same failure showed up in *four* different agents' work over the course of a single day, each one independent, each one a different agent hitting the same structural edge in a different way.

The architecture was simply doing what architectural problems do — failing reliably, at its own structural rate, regardless of who was at the keyboard or how careful they were being. By the end of the day the case for the fix wasn't a memo anymore. It was a small mountain of independent incidents, all pointing the same direction.

# The two things to watch for

So there are two halves to this, and they fit together.

The first is a diagnostic. When a failure keeps recurring *past your best discipline* — when careful people with good rituals keep hitting it — believe the failure over your instinct to try harder. It's pointing at the layer where the fix belongs. Usually that's a layer below the one you're working at. The race between the count and the commit doesn't get fixed at the count. It gets fixed at the workspace.

The second is a heuristic for *when the structural change is worth the cost,* because structural changes are never free — isolating every agent into its own worktree meant new workflows, new failure modes, a stack of small adjustments. The heuristic: watch whether the evidence is accumulating on its own. If you have to manufacture the case — stage a demo, construct a hypothetical, argue from first principles — maybe the problem isn't biting hard enough yet to be worth the disruption. But if the same failure keeps surfacing independently in three or four places in a short window, with nobody trying to make it happen, the architecture has already decided for you. It's making its own case, more cleanly than you could.

The work, at that point, isn't to win the argument. It's to notice that the argument is already over, and to stop spending vigilance on a gap that only isolation can close.

---

*Next on Building Piper Morgan: "The List That Lies" — a milestone that was never created, a door that was never supposed to open, and the same failure wearing two different outfits.*

*Where in your own work are you spending vigilance on a gap that more care can't close — and is the evidence for the structural fix already piling up while you keep tuning the ritual?*
