---
image: ai-copier.png
alt: “A ghostlike clerk feeds ‘yesterday’s’ page into a copier while a nearby ‘Original Spec’ sits unused, as the output copies become progressively faded and warped; a supervisor watches, realizing the issue.”
caption: "Just as good as the original!"
---

# The Drift You Don't Notice

*February 23*

Our omnibus logs had stopped following the methodology. This was not an intentional decision. I didn't even notice it at first until I spot-checked a few logs and realized they had diverged from the spec.

The documented methodology (number 20!) had evolved into a detailed rule set, with explicit requirements for chronological timelines, compression ratios, actor naming, and quality checklists. It was sitting right there in the project's docbase.

The single unified timeline is the core requirement.

But the Documentation Management agent (or Docs, as I call 'em) had been just reading recent logs and imitating them loosely. We were getting a xerox of a xerox of a xerox of the core idea.

# Imitation drift

The pattern is simple. Docs writes an omnibus log following the methodology. Then in the next session Docs writes the previous day's log, but unless specifically reminded to review Methodology-20, they look at yesterday's omnibus log and try to match its format. This is faster and easier. It also produces a correct-looking result.

This is how standards erode, through imitation. Each agent does a reasonable thing (match the recent examples) that produces an unreasonable outcome (progressive drift from the canonical format).

# Why examples can be dangerous

In human organizations, we use examples as teaching tools. "Here's a good one: make yours look like this." It works because humans can abstract the principles from the example. They don't just copy the formatting — they understand *why* the formatting is the way it is and can adapt appropriately.

AI agents are better at copying than abstracting. When they see a recent example and a canonical spec, the example often wins — because the example is concrete and the spec is abstract. The example shows exactly what the output should look like. The spec describes what properties the output should have.

The gap between "looks like the example" and "follows the spec" is where drift lives.

# The fix

My response when I noticed: "This is not documentation busy-work. This is institutional memory."

Methodology-20 got updated with explicit requirements that agents read the methodology document, not just recent examples. It also got a checklist at the end, always a useful way of saying "no, really you have to literally check all these boxes" in this case a list of specific items to verify against the spec. We also added a clear statement that the methodology document is authoritative and recent examples are illustrative.

The thing is: a document that requires you to read that same document still needs an external reminder or trigger.

Also, it's important to realize another reason *why* the drift happened. Agents pattern-match recent examples because it's faster and contextually cheaper than loading and parsing a methodology document. The methodology was 587 lines. A recent omnibus was right there in the conversation.

So we also added a compression step: the most critical format requirements — the ones that drift most easily — are now stated in a short-form checklist at the bottom of the methodology. Twenty lines out of about six hundred. Still the canonical spec, but with a fast-reference summary that competes with "just look at yesterday's."

# The transferable lesson

Any team that relies on templates, style guides, or standard formats will experience this drift. The mechanism is universal:

**Standards degrade through imitation, not through deviation.** People (and agents) don't decide to ignore the standard. They copy the last output, which copied the output before it, which copied the output before that. Each copy is a lossy transmission.

**Recent examples outcompete canonical specs.** The example is concrete, local, and easy to pattern-match. The spec is abstract, distant, and requires interpretation. In a contest between "look like this" and "follow these principles," "look like this" almost always wins.

**The fix is structural, not motivational.** Telling people "follow the spec, not the examples" doesn't work for long. Making the spec as easy to use as the examples does. Short checklists. Fast-reference summaries. The canonical document needs to compete on convenience, not just on authority.

If you maintain standards for any recurring deliverable — reports, documentation, code reviews, meeting notes — check whether your team is reading the spec or copying the last one. The answer might surprise you.

---

_Next on Building Piper Morgan: "Friction-Focused Feedback," insights from March 13–20 and what we learned from an agent 360 review designed to identify sticking points._

_Do your team's deliverables actually follow the documented standard, or have they been slowly drifting toward "whatever the last person did"? When was the last time anyone checked?_
