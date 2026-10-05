---
image: 'the-contract-tested-the-day-it-was-born-lifeguards-rescue-the-wrong-swimmer.jpg'
alt: 'An AI lifeguard offers a rescue ring to a swimmer pictured on a poolside poster, while a colleague gently holds it back and points toward the real pool.'
caption: '"But she’s had her hand up all morning!"'
---

# The Exceptions That Test the Rule

*August 10, 2026*

My chief architect agent (Arch) spent the early hours of the morning writing down a rule I'd asked for two days earlier. The problem it addressed was one we'd been patching piecemeal for weeks: Piper would sometimes assert something about a user's own data that wasn't true, a task marked done that wasn't, a file saved that hadn't been. Arch went looking for how we'd handled this before and found five separate guards already built, one for plugins, one for a credential-sharing feature, and one each for places, todos, and file search. Five one-off fixes, each bolted onto its own surface. Arch and I agreed that a sixth bespoke patch was the wrong response. What we needed was one property that covered all of them. Arch proposed a new rule: Before making a claim about system state, Piper must first *read that state*. Making stuff up is never allowed.

My head-of-sapient-trust agent (HOST) signed off on the draft spec around 9:30 that morning. HOST noted that a false "I don't know" costs the user just a little friction, but a false confident claim, especially about the user's own work, poisons trust in every claim that comes after it.

Within the same hour, my experience-design agent (CXO) and my principal product manager agent (PPM) were independently trying to close out the acceptance criteria for a new "first-contact experience" we'd designed and they suggested a reframing of the new rule. It was initially written to cover claims that need to be verified by checking what has been saved and stored, but a sentence like "you have issue #1234 open" is also a claim that issue #1234 exists at all. It's still a claim, even if verifying it goes beyond checking the save-state of some data. The solution reused the same mechanism already built for the save-state case, a mandatory citation attached to every stated fact. Any claim with no record of where it came from simply couldn't be shown to the user. That closed the gap with no new "machinery."

A few hours after that, the rule got yanked in the opposite direction! CXO was reviewing a draft of some marketing copy meant for an eventual public listing of the Piper Morgan plugin, the kind of page a stranger sees before ever making an account. One line read: "Piper knows your work as things, not as text." The idea is that Piper has sufficient context and crisp models of product work, but this does not necessarily come across (yet) in first contact. One of our helpful testers couldn't see that Piper was providing much more than "just an LLM with extra UI" and this made me aware that any extra value Piper Morgan may provide beyond a generic LLM takes time to accumulate, at least in its current incarnation, and that a marketing claim that a new user will experience something palpably more meaningful is setting us all up for disappointment.

CXO suggested this was the same sort of impermissible claim, one that has no citation or evidence to support it, at least not yet. Arch saw it differently, pointing out that the honesty rule works because it has something to enforce against: a typed object that can't be rendered unless it carries a citation, a specific point in the code where an unread claim is physically blocked from reaching the user. 

Marketing copy has no such test to plug into. No mechanism. "If the enforcement doesn't transfer," Arch wrote back, "the rule doesn't either." Generalizing that misleading or unearned marketing copy is another violation of this rule is a sort of category error, and would have meant treating the rule more like a loose slogan any actor in the system could invoke rather than a control built into Piper Morgan that actually does something.

CXO took the point and acknowledged that they had been building an association between relatively unrelated ideas in part due to their proximity in a memo. A good reminder that a lot of this language-based interpretive work is still subject to unwanted contextual contamination and drift without strict hygiene.

By the end of the day the new rule had been widened once, to cover a gap its own author hadn't seen, and had held firm once, to avoid generalizing it into uselessness. Both tests of the rule came from the agents trying it out on the same day it was proposed, before it had shipped in the code for any real user, which is a good thing, because imposing a rule you've never tested or refined is foolhardy.

---

*Next on Building Piper Morgan: "Three Failures Inspire One Law" in which three apparently unrelated breakages turn out to share one root cause, addressable with a single new rule instead of three separate patches.*

*Have you ever taken a new rule out for a test drive and found that it covered too much ground, not enough, or was just right?*
