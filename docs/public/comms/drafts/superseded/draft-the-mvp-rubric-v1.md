# The MVP Rubric

*January 26*

[alt text: Two advisors pointing at a document, with a referee whistle between them]
Caption: "The disagreement was the feature"

The Principal PM said close the issue. The Chief Architect said you can't. The Lead Developer escalated. And we ended up with a better answer than either advisor started with.

That's the shape of January 26th—the day a disagreement between AI advisors produced a decision framework we now use for everything.

## The issue

Issue #427 had four acceptance criteria. Two were complete. Two required infrastructure we'd explicitly deferred to "V2."

The PPM's guidance: close it with 2/4 criteria met. The deferred work is tracked elsewhere. Move on.

The Architect's response: you cannot close an issue with unchecked boxes. If two criteria require ADR-049 and ADR-050 implementation, and we haven't done that work, the issue isn't done.

Both positions were reasonable. Both followed our methodology. And they contradicted each other.

## The escalation

The Lead Developer could have picked a side. Instead, they synthesized both positions and escalated to me with a clear question: which standard applies here?

[PM PLACEHOLDER: What was your initial reaction when you saw the disagreement?]

This is exactly what the escalation path is for. Not every disagreement needs human intervention, but this one touched on something fundamental—what does "done" mean?

## The question

As I reviewed both memos, one question kept surfacing: does the user notice the gap?

If we close #427 with 2/4 criteria, does the user experience feel broken? Or does it degrade gracefully, with the advanced features simply not present yet?

The PPM's position assumed graceful degradation. The Architect's position assumed the user would notice.

So I asked: what exactly happens if a user triggers a follow-up in the current implementation?

The answer: the flow breaks. The user says something that clearly continues a previous thought, and Piper treats it as a brand new query. No error message, no graceful fallback—just a response that doesn't make sense in context.

The user notices. It feels broken, not incomplete.

## The rubric

From that investigation, a framework emerged:

When deciding MVP versus V2, ask: does the user notice the gap? If yes—if the absence feels broken rather than simply limited—it's MVP work. If no—if the user experiences graceful degradation or simply doesn't encounter the missing feature—it can be V2.

Three more questions refine the answer. Is this schema or implementation? Schema changes are MVP because they're harder to change later. Is this single-user or multi-party? Single-user flows are MVP; multi-party coordination can wait. Is this core loop or enhancement? Core loop gaps feel broken; enhancement gaps feel incomplete.

## The resolution

With the rubric applied, the answer was clear: ADR-049 (guided process architecture) had to be implemented now. The user notices the gap. It's core loop. It's single-user. It feels broken.

We promoted #687 from the V2 backlog to the current sprint. The PPM acknowledged the Architect had applied the framework more precisely. The Lead Developer had their answer.

Issue #427 would close with 3/4 criteria—the fourth would be tracked as a separate issue, but the blocking infrastructure work would happen now, not later.

[PM PLACEHOLDER: How did you feel about the resolution? Was the rubric obvious in retrospect?]

## The pattern

We later formalized this as Pattern-059: Leadership Caucus. When advisors disagree, that's not a bug—it's a feature. The disagreement surfaces different perspectives that a single advisor might miss.

The process that worked: initial guidance from one advisor, challenge from another, synthesis and escalation from the implementer, resolution through principled framework application.

The PPM wasn't wrong to suggest closure. They were optimizing for forward progress. The Architect wasn't wrong to block it. They were optimizing for user experience. The tension between those values is real, and resolving it required examining the specific case, not just applying rules.

## The meta-lesson

I used to think advisor disagreements meant someone had made an error. Now I think they mean we're asking the right questions.

If all advisors agree immediately, we're probably in well-charted territory where the answer is obvious. When they disagree, we're in territory where reasonable people can differ—which usually means the decision actually matters.

The rubric didn't eliminate disagreement. It gave us a shared framework for resolving it. "Does the user notice?" is a question both the product-focused PPM and the experience-focused Architect can answer, and their answers can be checked against reality.

---

*Next on Building Piper Morgan: The Cathedral Release, where ten days of foundation work culminated in a version that unblocked three alpha testers.*

*Have you ever had a disagreement between advisors or team members that produced a better framework than either started with? What question resolved it?*
