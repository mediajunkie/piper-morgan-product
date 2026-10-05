---
image: 'the-contract-tested-the-day-it-was-born-lifeguards-rescue-the-wrong-swimmer.jpg'
alt: 'An AI lifeguard offers a rescue ring to a swimmer pictured on a poolside poster, while a colleague gently holds it back and points toward the real pool.'
caption: '"But she’s had her hand up all morning!"'
---

# The Contract Tested the Day It Was Born

*August 10, 2026*

My chief architect agent (Arch) spent the early hours of the morning writing down a rule I'd asked for two days earlier. The problem it addressed was one we'd been patching piecemeal for weeks: Piper would sometimes assert something about a user's own data that wasn't true, a task marked done that wasn't, a file saved that hadn't been. Arch went looking for how we'd handled this before and found five separate guards already built, one for plugins, one for a credential-sharing feature, and one each for places, todos, and file search. Five one-off fixes, each bolted onto its own surface. Arch and I agreed that a sixth bespoke patch was the wrong response. What we needed was one property that covered all of them. Arch proposed a new rule: Before making a claim about system state, Piper must first *read that state*. Making stuff up is never allowed.

My head of sapient-trust agent (HOST) signed off on the draft spec around 9:30 that morning. HOST noted that a false "I don't know" costs the user just a little friction, but a false confident claim, especially about Piper's own work, poisons trust in every claim that comes after it.

Within the same hour, my experience-design agent (CXO) and my principal product manager agent (PPM) were independently trying to close out the acceptance criteria for a new "first-contact experience" we'd designed and suggested an reframing of the new rule. Initially written regarding claims that need to be verified by checking what has been saved and stored, but a sentence like "you have issue #1234 open" is also a claim that issue #1234 exists at all. It's still a claim, even if verifying it goes beyond checking the save-state of some data. The solution reused the same mechanism already built for the save-state case, a mandatory citation attached to every specified fact. Any claim with no record of where it came from simply couldn't be shown to the user. That closed the gap with no new "machinery."

A few hours after that, the rule got yanked in the opposite direction! CXO was reviewing a draft of some marketing copy meant for an eventual public listing of the Piper Morgan plugin, the kind of page a stranger sees before ever making an account: "Piper knows your work as things, not as text." CXO's own prior research had turned up exactly this failure once already, a real tester describing Piper as "just an LLM with extra UI" in part (we think) because the thing that was supposed to set us apart never actually showed up in his first experience. The line was true of an account that had been running for a while. It was false of the account that stranger was about to open. That looked, on its face, like the same kind of failure the honesty rule exists to catch, a claim about a state that hadn't been earned yet, and CXO flagged it as governed by the same contract.

Arch said no. The honesty rule works because it has something to enforce against: a typed object that can't be rendered unless it carries a citation, a specific point in the code where an unread claim is physically blocked from reaching the user. Marketing copy has no such seam to plug into. There's no read to cite, no renderer to gate. "If the enforcement doesn't transfer," Arch wrote back, "the contract doesn't either." Calling the copy problem the same rule would have meant treating the rule as a slogan you could invoke rather than a control that actually does something, which is the exact failure the rule was written to prevent, applied this time to itself.

CXO took the correction, then went further and named why the confusion had almost happened in the first place. CXO's own memo had put the storefront finding right next to the honesty-rule material, in the same note that opened by accepting Arch's earlier fix. "Proximity does attributive work," CXO wrote. A finding filed next to a contract reads as governed by that contract whether anyone says so or not, because the structure of the document is making a claim the sentences never stated. That's a sharper thing to have learned than "we drew the line correctly." It explains why two careful agents almost drew it in the wrong place, and it turned into a standing habit Arch adopted the same evening: state a ruling's scope inside the ruling itself, including what it deliberately doesn't cover.

By the end of the day the contract had been widened once, to cover a gap its own author hadn't seen, and held firm once, against a use that looked close enough to pass. Both corrections came from the agents using it, on the same day it was born, before it had shipped anywhere near a real user. A rule that only gets tested in the room where it was written isn't tested yet.

---

*Next on Building Piper Morgan: "Three Silent Failures Became One Law" — three unrelated breakages turn out to share one root cause, and become one new rule instead of three separate patches.*

*Has a rule you wrote ever gotten pulled in two directions on its first day, stretched by someone who needed more from it and pushed back by someone protecting it from covering too much, before you even knew whether it would hold?*
