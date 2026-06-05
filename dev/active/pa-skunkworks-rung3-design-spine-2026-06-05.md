# Rung 3 design spine — "honesty as the ground, room for the LLM to elaborate"

**Author**: PA, from a design conversation with PM · **Date**: 2026-06-05 · **Tracking**: #1145
**Status**: design principle captured (conversation in progress — NOT a build spec yet; PM-gated).

## The governing principle (PM, 2026-06-05)

When the host agent enriches Piper at the floor (the rung-1 gate-run finding), the design is:

> **Honesty is the load-bearing structure; the LLM's fluency is the finish, not the frame.**

PM phrasing: *"honesty as the ground, with room for the LLM to elaborate."*

This resolves the false binary PA posed (1: invisible "smart Piper" magic vs. 2: rigid explicit
handoff). It's **option 2 as the skeleton, option 1's grace as the surface** — neither alone.

## What it means concretely

- **Honest spine (load-bearing, designed):**
  - Piper **declares its floor explicitly** — what it's missing ("I don't have your backlog/roadmap/
    todos"). It already does this; the floor is a feature, not a failure.
  - The skill **gathers exactly the declared gap** — not a fishing expedition; targeted to what Piper
    said it needed.
  - **Provenance is visible** — the user can see what came from where (Piper's reasoning vs. host-
    gathered context vs. the host's own synthesis). No laundering host knowledge as Piper's.
  - Never confident fabrication: the elaboration rides ON the honest substrate, never instead of it.

- **LLM latitude (the finish, not scripted):**
  - Don't hard-script every word/step (the failure mode of pure option 2 — turns it into a state
    machine, kills the colleague quality).
  - Let the LLM phrase the gap conversationally, synthesize gathered context gracefully, push back,
    think out loud — the **latitude that the Cowork test found was the moat.**

## Why this is the right shape (three convergences)

1. **It IS the Conscious Floor philosophy, applied to the composition layer.** The floor was never
   "refuse when you don't know" — it's "be honest about the limit, then help anyway." Rung 3 makes the
   *host↔Piper* relationship obey the same rule Piper obeys internally. Architectural self-similarity.
2. **It preserves the moat the Cowork test named.** Latitude (room to react/elaborate/disagree) was the
   hard-to-copy quality. Honesty-as-ground keeps the latitude but anchors it so it can't drift into
   fabrication — latitude WITH integrity.
3. **It's the PDR-005 context-package mechanism in miniature.** "Piper declares what it needs → the
   surrounding layer supplies exactly that, with provenance" is the context-package negotiation
   (mechanism set #5, Q6 ADR) at the single-skill scale. Rung 3 is a working probe of the canonical
   BYOC mechanism we just ratified.

## Open design questions (for the continued conversation — NOT decided)

- **How does Piper *declare* the gap machine-readably?** Today the floor surfaces as prose ("I don't
  have your backlog"). For the skill to gather *exactly* what's missing, does Piper need to emit a
  structured "missing-context" signal (e.g. `context_keys` it wanted but lacked)? Or does the skill
  infer the gap from the prose? (Ties to #1151 — the intent contract's fidelity.)
- **What does "provenance visible" look like in the chat surface?** Inline tags? A "here's what I
  gathered for Piper" preamble? Keep it honest without making it noisy.
- **Scope guard**: which host MCPs are in-scope for gathering (Calendar/Notion/Gmail/Slack/Granola all
  appeared in the gate run)? Start with one (Calendar? the cleanest "today" signal) per Gall's Law.
- **Is this one skill or a skill + a convention?** Could be an evolution of `ask-piper`, or a new
  `consult-piper-with-context` skill. (Rung-2 stayed bare passthrough by design; rung 3 is the
  enrichment increment.)

## Discipline note
Still glimpsing, not building. This captures the *principle* so the eventual build inherits the right
spine. Next: continue the conversation on the open questions, THEN a build plan, THEN build. Don't let
the design conversation skip to implementation.
