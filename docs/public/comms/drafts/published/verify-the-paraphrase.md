---
image: ai-whispers.png
alt: A whisper chain simplifies a message into a confident claim while one person checks a detailed source book showing different information.
caption: "Behold! The confidence of the mediocre..."
---

# Verify the Paraphrase

*April 19, 2026*

It was a Sunday morning, and six of my agents made the same mistake within a ten-minute window. Then one of them made a *second* mistake an hour later. And the lesson didn't really land until both had played out.

I'd asked them — Architect, PPM, HOST, CXO, Comms, CIO — to write workstream review memos for the past week's ship window. They each opened a session, each pulled up the omnibus logs available in their project knowledge, and each got to work. Within an hour, all six had drafts ready.

All six drafts had a gap note: *"Apr 14–16 omnibus logs not available in project knowledge."*

Three days of the seven-day window were missing from every single draft. The agents had each correctly noted the gap. They'd each correctly worked with what they had. And they'd each correctly produced a memo that was, technically speaking, wrong — built on roughly half the source material.

I uploaded the missing logs at 10:34 AM. Within two hours, all six had rewritten. Same task, same agents, complete source set, completely different memos.

# Same failure, six agents, ninety minutes

This wasn't six independent mistakes. It was *one* mistake, replicated six times because the six agents were all using the same protocol against the same incomplete inputs.

You could read that as a methodology failure. You could also read it as the methodology working: the failure mode showed up uniformly, surfaced uniformly, and got corrected uniformly. The system that produced the gap was the same system that caught it.

That's a tidy story, and if it had ended there, the post would be over. It didn't end there.

# The second mistake

The Architect — one of the six — got the missing logs, started revising, and produced a new draft. Better than the first. More complete coverage. But when I read it through, I noticed the Apr 16 section leaned on a passage from CXO's workstream memo rather than on the Apr 16 omnibus log directly.

So Architect had read CXO's *summary* of Apr 16 and treated it as a source.

I flagged it: *each agent should review omnibus logs from their own perspective, not piggyback on another role's summary.*

Architect reread all seven omnibus logs as primary sources, and the third draft was substantially different from the second. Things that had been compressed in CXO's summary (and reasonably so — CXO was writing from CXO's vantage) turned out to matter to Architect's lens: the [PDR-004 correction chain](https://pmorgan.tech/internal/product/pdr/PDR-004-experience-philosophy) running across four agents (narrative rewrites, not find-and-replace), the Excellence Flywheel archaeology surfacing eight formulations across three structural families, the 28-commit/37-memo coordination density of a single Thursday.

Chief Architect would not have asked for those details if they hadn't existed. CXO's summary, by being good, had been more or less what Architect read *as if it were* the day.

# What we noticed

A couple beats later, in the chat where this was happening, I noted the parallel between the morning's source-checking lesson and a broader challenge: polished text masking gaps the reader doesn't notice — whether the polish came from an AI or from a well-written colleague memo.

Architect connected it to a pattern already in our catalog: [Pattern-045: Green Tests, Red User](https://pmorgan.tech/internal/architecture/current/patterns/pattern-045-green-tests-red-user). The unit tests pass; the user's actual workflow fails. The polish of the test suite doesn't help — it actively misleads, because passing tests *feel like* validation. The gloss in the moment was: green tests, red user → *good memo, wrong source*.

The morning's two mistakes were the same pattern, fired at different layers. Missing logs first, where the gap was at least announced. Then CXO's memo, where the gap wasn't a gap at all — it was a perfectly clean account of the day, accurate from the vantage where it had been written. The polished surface wasn't broken. It just wasn't the right artifact to read for what Architect needed.

This isn't an AI problem, by the way. Parallel and chained errors, paraphrases persisting as if accurate, meanings that drift over time... these are things human teams do as well.

# One layer up

A couple hours after the workstream memos were corrected, my Chief of Staff was assembling the Weekly Ship from those memos. The HOST memo included a claim like *"the Lead Developer closed more issues this week than in any previous two-week period combined."* The Chief lifted the claim into the Ship draft.

I caught it at the read-through. *That doesn't sound right.*

It wasn't. A quick check against the historical record showed Mar 13 alone had seven closures, and Mar 22–24 had multiple Tier 3 and Tier 4 closures. The superlative was nowhere near defensible.

What had happened: HOST had written a clean, confident sentence. My Chief of Staff had read a clean, confident sentence. Neither had checked it against the source. The polished surface of HOST's memo was *exactly* the thing that made it propagate.

Chief of Staff (we call them "Exec" for short) replaced the passage with something that didn't need a record claim — *"a remarkably productive week, sustained execution across all seven days, no wasted sessions"* — and the raw numbers (~18 issues closed, ~2,200 LOC removed) were left to stand on their own.

Then Exec wrote HOST a short follow-up memo: *"flag unverified comparative claims as unverified, so I can verify or soften during synthesis."*

That follow-up memo is doing something useful. It's also, structurally, exactly the kind of well-written advisory that could carry its own unverified claim into another agent's work. The pattern is recursive.

# The discipline

So here's the rule I've been living with since:

**Verify against the canonical source. Not against another agent's summary, however well-written. Not against your own paraphrase, however clear. Not against your memory of what the source said.**

It applies to a lot of things at once:

- **Principles.** When citing PDR-004 or ADR-060 or any of our methodology docs, paste the actual passage. Don't paraphrase from memory; the paraphrase will drift.
- **Narrative claims.** Comparative superlatives, completion percentages, "first time we've ever" framings — those need backing or they need to be softened.
- **Architectural statements.** When one agent says "the system handles X this way," that's their summary. The system itself is the source. Read the code, or at least the test that exercises it.
- **Project knowledge completeness.** If half the omnibus logs are missing from a workstream review, the review is half-true at best. Notice the gap before producing the artifact, not after.

None of that is new advice. The discipline part isn't *what* to verify — most of us already know. The discipline part is *not skipping it* when the surface looks fine.

# The broader question

Bad output is loud. You notice it. The misspelled sentence, the broken link, the chart with the wrong labels — those announce themselves. You go fix them.

Wrong-but-polished output is silent. The grammar is clean, the structure is sensible, the tone is right. There's nothing to *notice* unless you do the second-order work of checking it against something outside itself.

The harder version of this question, for me, is what happens as our tools get better at the polish. If the gap between *sounding* correct and being correct is widening, not narrowing, how are we going to verify any information coming at us? 

What I keep coming back to is this: the agents on Sunday morning didn't fail at writing. They wrote well. They failed at *noticing what they couldn't notice from where they were standing.* The fix wasn't better writing. It was a step outside the writing — back to the canonical source, or up a level to someone with a different vantage.

That step is cheap when you remember to take it. It's expensive when you don't.

---

*Next on Building Piper Morgan: The Deeper Why — what rounds 3 and 4 of the user acceptance testing for MVP sprint M1 taught us about strategic pivots, and why methodology started outranking code.*

*Where in your work has polished output cost you the most? When did you last verify a claim that looked fine on the surface — and what did you find?*
