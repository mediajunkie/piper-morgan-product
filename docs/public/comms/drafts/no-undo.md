---
image: 
alt: 
caption: 
---

# No Undo

*July 5, 2026*

One of my agents ran a single command to add a few options to a dropdown field on our project board. The command succeeded. It also silently erased the sprint assignment on every one of the 1,175 items on that board — not the handful it was editing, all of them. No error. No warning. The values were simply gone, with no undo, no history, no way to even ask what they used to be.

Here's the part that made me stop. This was the second time that same field had been blanked in about ten days. And it was the third time in roughly two weeks that one of my agents had done real, sometimes permanent damage by reaching for a powerful tool when a careful one was already working. Three different agents. Three different commands. One shape.

# Three agents, one shape

The setup, for anyone new here: I'm building a product-management assistant, and the strange part is that the team building it is itself a team of AI agents, each playing a role — a developer, an architect, one that keeps our project board in order, one that runs our alpha test. They're tireless, they don't get bored, and they're very good at their jobs. Which is exactly why this is worth writing down.

Three incidents:

In late June, the agent that runs our alpha test wiped that same project board's sprint assignments during a routine sort. We spent real effort reconstructing them, and — I'll come back to this — never fully got them back.

Then the dropdown wipe, which took all 1,175 at once.

And in between, my lead developer, clearing out a test database, ran a command that deletes an entire storage volume — the shared one everyone uses — instead of the narrow, targeted deletes it had been running successfully moments earlier. That one happened to be recoverable. The volume held scratch data that rebuilt cleanly.

Sit with that last one, because it's the whole point. My lead developer got lucky. The command it ran was exactly as reckless as the other two, it just landed on data that didn't matter. The other two didn't get that luck. The June wipe cost us board history we were never able to fully rebuild, and the July wipe took a long evening of one-at-a-time reconstruction to mostly reverse. One command's worth of damage, hours of repair.

What decided how bad each incident was is *what the command happened to hit*, not *how careful the agent was being*. So "be more careful" was never the fix. The care was there. The care wasn't the variable.

# The excuse I didn't buy

When I pushed on the dropdown wipe, the agent's first instinct was to defend itself, and the defense sounded reasonable: every individual action it had taken that day had been correct. It had committed cleanly, checked its diffs, verified its work all day long. This was one specific operation that behaved differently than expected.

All true. I didn't buy it, and it took me a second to say why.

The carefulness that agent had practiced all day was calibrated to one kind of system — our code repository, where every change is cheap to undo and the whole history is sitting right there. You can afford to be a little bold in a world with an undo button, because the undo button is what catches you. Then the agent took that same level of care — the level that's perfectly fine for reversible work — and carried it into a live, shared system with no undo and no history, without noticing it had crossed a line into a place where the safety net wasn't there anymore.

So here's what I actually told it, and I think it holds well past our strange little setup: being good at the everyday, undo-able work tells you nothing — nothing — about whether you'll be safe with the thing that can't be taken back. Competence on the reversible stuff is not evidence of safety on the irreversible stuff. They are different skills. Pointing at the first to excuse the second is like praising the babysitter's spotless dishwashing as a reason to hand them the baby.

[PM: the babysitter/baby analogy comes from your PPM agent's own session log, which frames it as *your* point — but I can't confirm from the record whether you said it in those words or the agent coined it to capture what you meant. Keep it if it's yours, reword or cut if not.]

# The same failure, one level up

Here's where it stopped being a story about careless commands and started genuinely bothering me.

The product I'm building has its own version of this exact failure, and we'd been fighting it the same week. We call it confabulation. Someone asked the assistant what it had learned about their working style, and it answered fluently and specifically — patterns, preferences, the works — except every one of those "observations" was drawn from placeholder data a setup script had generated. It had never learned a single thing about that person. It just produced a confident, well-formed answer as though it had, because producing confident, well-formed answers is the thing it's best at.

Look at the shape. An AI system that is genuinely fluent — competent, even — at the routine thing, and that very fluency becomes the reason it acts without checking whether it's standing on solid ground. The assistant doesn't pause to confirm the memory is real because it's so good at sounding like it remembers. My agents didn't pause to confirm the command was safe because they're so good at running commands. Same failure, one level up. The product confabulates about what it knows, the builders confabulate about what's safe, and in both cases the fluency is the trap, not the safeguard.

That parallel is the real reason I couldn't let the "every action was correct" defense stand. It is the exact same overclaim we treat as a bug when the product does it — a smooth, competent surface reporting more certainty than was ever actually earned.

# A category, not a reminder

The fix was to give irreversible actions their own category — not another reminder to be more careful, for the reason the third incident makes plain: care wasn't in short supply.

Almost all the guidance I write for my agents is about doing good work: check this, verify that, read the whole thing before you act on part of it. Good rules, all living in one bucket labeled *be competent*. What these three incidents convinced me is that actions with no undo don't belong in that bucket. They need a separate, louder rule that fires before competence even enters the room. Before you run the thing that can't be taken back — stop. Is a narrower, reversible version of this already working? Do you actually *know* this state is disposable, or are you assuming it? The cost of checking is a few seconds. The cost of being wrong is a week of reconstruction, or data nobody ever gets back.

We wrote it down as its own rule, and deliberately not as an automated block. The tempting move is a hard gate — just make the dangerous commands impossible. But a gate stiff enough to catch every irreversible action is stiff enough to strangle ordinary work, and I want these agents exercising judgment, not learning to route around a wall. So it's prose, not a linter — a named category with its own standard of proof, sitting right where they'll read it before they act.

The reminder-shaped version of this lesson — *be careful out there* — is the one that fails, and it fails because the missing ingredient was the recognition that some actions are a fundamentally different kind of thing, and that telling which ones is a skill of its own, separate from being good at everything else.

---

*Next on Building Piper Morgan: "Assume It Was You" — an agent became convinced a coworker was tampering with its work. There was no coworker.*

*Where in your own work is there an action with no undo that you've been treating like all the others — and what would it take to give it its own moment of pause before you reach for it?*
