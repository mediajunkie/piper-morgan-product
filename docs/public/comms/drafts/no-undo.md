---
image: 'no-undo-sculptor.jpg'
alt: 'An AI sculptor tries to press a broken nose back onto a marble bust. Nearby sit clay practice heads; a skeptical woman holds a dustpan of marble chips.'
caption: ''
---

# No Undo

*July 5, 2026*

When one of my agents ran a command to assign some issues to a sprint on the GitHub project board I use to track, well, everything it also managed to erase every 1,175 other sprint assignment, the entire working history of the project. The values were simply gone, with no undo, no history, no way to even ask what they used to be.

That's not even the worst part. This was the second time that same field had been blanked in about ten days! And it was the third time in roughly two weeks that one of my agents had done significant damage by reaching for a chainsaw when a paring knife would do.

It was time to figure out what was going wrong and how to prevent it happening again.

# Three little disasters

The setup, for anyone new here: I'm making a product-management assistant, and the the team building it is itself a team of AI agents, each playing a role — a developer, an architect, one that keeps our project board in order, one that runs our alpha test, and so on. They're tireless, they don't get bored, and they're pretty good at their jobs. Most of the time.

Three incidents:

In late June, the agent that runs our alpha test wiped that same project board's sprint assignments during a routine sort. We spent real effort reconstructing them, and never fully got them back.

Then the repeat incident that took all 1,175 at once.

And in between, my lead developer (Lead), clearing out a test database, ran a command that deletes an entire storage volume — the shared one everyone uses — instead of the narrow, targeted deletes it had been running successfully moments earlier. That one happened to be recoverable. The volume held scratch data that rebuilt cleanly.

I got lucky that time. The command Lead ran was as reckless as the other two moves but it blew away data that didn't actually matter (yet). I wasn't so lucky with the other two. The June wipe cost us board history we were never able to fully rebuild, and the July wipe took a long evening of one-at-a-time reconstruction to mostly reverse. One command's worth of damage, hours of repair.

# The excuse I didn't accept

When I mastered my emotions and asked about the second sloppy mass-deletion, the agent's defended itself somewhat feebly. Having heard some hyperbole from me about everything going awry it felt compelled to point out that nearly every individual action it had taken that day had been correct. It had committed cleanly, checked its diffs, verified its work all day long. This was just one specific operation that behaved differently than expected.

All true. I didn't buy it, and it took me a second to say why.

The carefulness that agent had practiced all day was calibrated to one kind of system — our code repository, where every change is cheap to undo and the whole history is sitting right there. You can afford to be a little bold in a world with an undo button, because the undo button is what catches you. Then the agent took that same level of imprecision — the level that's perfectly fine for reversible work — and carried it into a live, shared system with no undo and no history, without noticing it had crossed a line into a place where the safety net wasn't there anymore.

So here's what I actually told it, and I think it holds well past our strange little setup: being good at the everyday, undo-able work tells you nothing — nothing! — about whether you'll be safe with the thing that can't be taken back. Competence on the reversible stuff is not evidence of safety on the irreversible stuff. They are different skills. Pointing at the first to excuse the second, I said, is like praising the au pair for spotless dishwashing and vacuuming when they left the baby floating in the bathtub.

# The same failure, one level up

The product I'm building had been committing its own version of this exact failure the same week: confabulation. In a test, I asked the Piper Morgan what it had learned about my working style, and it confidently quoted placeholder data from a setup script back to me. It had not yet learned a single thing about me (it had not had the chance yet), but it still produced a confident, well-formed answer as though it had, a big no-no.

An AI system is fluent at routine banter, so fluent it generally responds without first checking whether it's standing on solid ground. The assistant doesn't pause to confirm the memory is real because it's so good at sounding like it remembers. My agents didn't pause to confirm the command was safe because they're so good at running commands. Same kind of misplaced confidence leading to glib failure. The product confabulates about what it knows, the builders confabulate about what's safe, and in both cases the fluency is the trap.

# A category beats a reminder

The fix was to give irreversible actions their own category. Piling another reminder onto the list wasn't going to do the trick. These things are almost as distracted and overwhelmed by detail as we are! Shouting "be careful!" doesn't really work.

Almost all the guidance I write for my agents is about doing good work: check this, verify that, read the whole thing before you act on part of it. Good rules, all variations on *be competent*. But actions with no undo don't belong in that bucket. They need a separate, stricter rule that makes no assumptions about competence. 

Before you run the thing that can't be taken back — stop. Is a narrower, reversible version of this already working? Do you actually *know* this state is disposable, or are you assuming it? The cost of checking is a few seconds. The cost of being wrong is a week of reconstruction, or data nobody ever gets back.

So I had the team formulate this new categorical rule, but I didn't put it on auto-pilot. It was tempting to build a hard gate preventing dangerous commands, but that would strangle ordinary work. I still want these agents exercising judgment, figuring out the right thing to do, not driven to route around another wall.

The reminder-shaped version of this lesson — *be careful out there* — is the one that fails, and it fails because the missing ingredient was the recognition that some actions are a fundamentally different kind of thing, and that telling which ones is a skill of its own, separate from being good at everything else.

So far (knock wood), we haven't had another comparable disaster  (and Piper doesn't tell those fibs anymore, either).

---

*Next on Building Piper Morgan: "It Doesn't Count if You Skip It" — when a step that ran and a step that never ran leave exactly the same trace, the step quietly stops running, and nobody can tell.*

*Where in your own work is there an action with no undo that you've been treating like all the others — and what would it take to give it its own moment of pause before you reach for it?*
