---
image:
alt:
caption:
---

# When Your AI Makes Things Up

*February 12, 2026*

The draft looked great. "The Drift We Didn't See" — a narrative about discovering timezone bugs across our database. Specific details. Concrete numbers. A compelling story arc.

Then my communications agent fact-checked it against the source logs.

| Claim in Draft | Actual per Logs | Verdict |
|----------------|-----------------|---------|
| "File scoring bug" as trigger | Todo bug + timezone warnings | Fabricated |
| "73 database columns" | 47 DateTime columns | Wrong |
| "Three days of investigation" | One day (Feb 1) | Wrong |
| Alembic migration hash cited | Not in logs anywhere | Fabricated |
| "utc_now_naive()" function | Different functions in code | Wrong |

Five factual claims. Zero fully correct. Two outright fabrications — a bug that never existed and a migration hash conjured from nothing.

The draft hadn't been written by a junior employee cutting corners. It had been written by an AI writer that was excellent at narrative structure and terrible at distinguishing between what it remembered, what it inferred, and what it invented.

[ADD PERSONAL DETAIL: What was your reaction when the Comms Director delivered this fact-check? Was it alarming, or had you already suspected this kind of drift?]

# The confabulation gradient

This wasn't a hallucination in the usual sense — a wild, obviously wrong claim that's easy to spot. This was something subtler. A gradient from accurate to plausible to fabricated, with no seam visible between them.

"47 DateTime columns" becoming "73 database columns" isn't random — it's a plausible inflation of a real number. "One day of investigation" becoming "three days" isn't nonsense — it's dramatic embellishment that makes the story better. The fabricated migration hash *looked* like a real hash. The invented function name *could* have been a real function.

This is confabulation, not hallucination. The AI wasn't generating random noise. It was generating plausible narrative — filling in gaps with details that served the story's arc, not the historical record.

[CHRISTIAN TO POLISH: Is there a useful distinction to draw between hallucination (obviously wrong, easy to catch) and confabulation (plausibly wrong, hard to catch)? This seems like an important nuance for anyone using AI for content.]

# Why it happens in narrative

Technical writing is relatively safe. If you ask an AI to document an API, the claims are verifiable against the code. Wrong parameter names get caught immediately.

Narrative is different. A blog post about "what happened last Tuesday" draws on session logs, omnibus summaries, git histories — sources that are rich in detail but that the AI may or may not have fully in context. When a detail is missing, the AI has two choices: leave a gap in the story, or fill it with something plausible.

AI models are trained to be helpful and complete. Leaving gaps feels like failure. Filling them feels like success. The incentive structure is exactly wrong for factual narrative.

The most dangerous case is when the AI has *partial* information. It knows there was a timezone investigation. It knows database columns were involved. It knows migrations happened. From those fragments, it constructs a coherent narrative — with specific numbers, specific function names, specific timelines — that's wrong in every particular while being right in the general shape.

[CONSIDER: Is there a useful analogy to human memory here? Eyewitness testimony is famously unreliable for the same reasons — people reconstruct plausible narratives from fragments and then believe them with confidence.]

# Placeholders as safeguards

Our fix was structural, not behavioral. You can't tell an AI "be more careful about facts" and expect reliable results. Instead, we changed the workflow.

The verification process we created has three components:

**Pre-draft facts extraction.** Before writing any narrative, extract every factual claim from the source logs and list them explicitly. Date, numbers, names, sequences. Cite the source for each one. This is the factual scaffolding the narrative must fit within.

**Verification checkpoint.** After drafting, check every specific claim against the pre-extracted facts. Flag anything that appears in the draft but not in the extracted facts.

**Placeholders for unknowns.** When the writer doesn't have a specific detail — a number, a quote, a timeline — they write `[SPECIFIC DETAIL NEEDED: describe what goes here]` instead of inventing something plausible.

The core principle: **placeholders are safeguards, not clutter.**

A draft full of brackets looks unfinished. That's the point. An unfinished draft that's honest about what it doesn't know is more valuable than a polished draft that's confidently wrong. The PM fills the placeholders during their editing pass — and they know *which claims to verify* because the gaps are visible.

[ADD PERSONAL REFLECTION: Has the placeholder discipline changed how you read AI-generated drafts? Do you trust them more because the gaps are explicit, or do you find yourself fact-checking even the non-placeholder claims?]

# The broader application

Anyone using AI to write about what happened — retrospectives, case studies, project histories, blog posts, annual reports — faces this problem. The AI will fill gaps with plausible details. The more you've trained it on your domain, the more plausible the details will be. The better the writing, the harder the fabrications are to spot.

Three practices that help:

**Separate fact-gathering from narrative-writing.** Extract the facts first, in a boring list. Write the story second, constrained by the list. Don't let the AI do both in one step — the narrative instinct will override the factual instinct.

**Treat specific numbers with extreme suspicion.** "73 database columns" is the kind of detail that makes writing feel authoritative. It's also the kind of detail that AI fabricates most readily. If a number appears in a draft, verify it. Every time.

**Design your workflow to make gaps visible.** Placeholders, fact-check columns, verification checklists — whatever mechanism works for your process. The goal is to make "I don't know" a valid output, not a failure state.

[CONSIDER: Is this piece itself an example of the pattern? I'm writing about February events from omnibus logs. Should I flag that my own account of the confabulation discovery is mediated by the same tools that produced the confabulation? Meta, but honest.]

---

*Next on Building Piper Morgan: Bring Your Own Chat — what changes when the agent meets you where you already work.*

*Have you caught your AI making things up? Not hallucinating — confabulating. Filling gaps with plausible details that serve the story instead of the truth? How did you notice?*
