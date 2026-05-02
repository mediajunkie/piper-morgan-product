# The Drift You Don't Notice

*March 26, 2026*

[alt text: PLACEHOLDER — cartoon TBD]

*February 23*

Our omnibus logs had stopped following the methodology. Nobody decided this. Nobody objected to the format. Nobody even noticed — until I read three logs in a row and realized they didn't match the spec.

The documented methodology — Methodology-20, carefully designed, with explicit requirements for chronological timelines, compression ratios, actor naming, and quality checklists — was sitting right there in project knowledge. The agents weren't ignoring it. They were ignoring it by accident.

They were copying the last agent's output instead of reading the source.

[ADD PERSONAL DETAIL: When did you notice? Was it a specific log that triggered the realization, or a gradual sense that something was off?]

## Imitation drift

The pattern is simple. Agent A writes an omnibus log following the methodology. Agent B writes the next day's log — but instead of reading Methodology-20, they look at yesterday's log and match its format. This is faster and easier. It also produces a correct-looking result.

But Agent A had made a small deviation. Maybe they used a "Sessions Overview" table instead of a chronological timeline. Maybe they compressed a section slightly differently. Maybe they used a role abbreviation instead of the full name.

Agent B copies the deviation along with the format. Agent C copies Agent B. By the time Agent F is writing, the format has drifted four generations from the spec and nobody can tell by looking at recent examples.

This is how standards erode. Not through rebellion — through imitation. Each agent does a reasonable thing (match the recent examples) that produces an unreasonable outcome (progressive drift from the canonical format).

[CHRISTIAN TO POLISH: Is this specific to AI agents, or have you seen the same pattern with human teams? Style guides that drift because people copy the last deliverable instead of checking the guide?]

## Why examples are dangerous

In human organizations, we use examples as teaching tools. "Here's a good one — make yours look like this." It works because humans can abstract the principles from the example. They don't just copy the formatting — they understand *why* the formatting is the way it is and can adapt appropriately.

AI agents are better at copying than abstracting. When they see a recent example and a canonical spec, the example often wins — because the example is concrete and the spec is abstract. The example shows exactly what the output should look like. The spec describes what properties the output should have.

The gap between "looks like the example" and "follows the spec" is where drift lives.

[CONSIDER: Is there a connection to the broader "prompt engineering" discourse? The advice is usually "give examples" — but examples without specs create this exact drift pattern. Maybe the advice should be "give specs, use examples as illustrations, never let the examples supersede the spec."]

## The fix

My response when I noticed: "This is not documentation busy-work. This is institutional memory."

Methodology-20 got updated with:

Explicit requirements that agents read the methodology document, not just recent examples. A checklist at the end — not a suggestion to check, but a list of specific items to verify against the spec. And a clear statement that the methodology document is authoritative and recent examples are illustrative.

But the deeper fix was understanding *why* the drift happened. Agents pattern-match recent examples because it's faster and contextually cheaper than loading and parsing a methodology document. The methodology was 800+ lines. A recent omnibus was right there in the conversation.

So we also added a compression step: the most critical format requirements — the ones that drift most easily — are now stated in a short-form checklist at the bottom of the methodology. Twenty lines instead of eight hundred. Still the canonical spec, but with a fast-reference summary that competes with "just look at yesterday's."

[ADD PERSONAL REFLECTION: Has the checklist actually prevented drift since February? Or does drift keep finding new channels — new places where agents copy examples instead of reading specs?]

## The transferable lesson

Any team that relies on templates, style guides, or standard formats will experience this drift. The mechanism is universal:

**Standards degrade through imitation, not through deviation.** People (and agents) don't decide to ignore the standard. They copy the last output, which copied the output before it, which copied the output before that. Each copy is a lossy transmission.

**Recent examples outcompete canonical specs.** The example is concrete, local, and easy to pattern-match. The spec is abstract, distant, and requires interpretation. In a contest between "look like this" and "follow these principles," "look like this" almost always wins.

**The fix is structural, not motivational.** Telling people "follow the spec, not the examples" doesn't work for long. Making the spec as easy to use as the examples does. Short checklists. Fast-reference summaries. The canonical document needs to compete on convenience, not just on authority.

If you maintain standards for any recurring deliverable — reports, documentation, code reviews, meeting notes — check whether your team is reading the spec or copying the last one. The answer might surprise you.

---

_Next on Building Piper Morgan: [TITLE TBD] — [teaser TBD]._

_Do your team's deliverables actually follow the documented standard, or have they been slowly drifting toward "whatever the last person did"? When was the last time anyone checked?_
