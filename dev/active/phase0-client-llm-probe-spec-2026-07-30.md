# Phase 0 probe spec — the client-LLM boundary, testable before the server exists

**Author**: PA · **Date**: 2026-07-30 · **Status**: proposed; rig is PA's, both verdicts belong to others.

## Why this exists

Two lanes independently landed on questions about the same thing this week, and **neither noticed the
other**:

| Raised by | Question | Their words |
|---|---|---|
| **CXO** (Layer-B finding, 7/30) | Does our honesty survive being recomposed by someone else's LLM? | *"We have never tested whether our honesty survives recomposition, and PDR-006 makes that the default path."* |
| **PPM** (tool-catalog answer, 7/30) | Do situation-shaped tool names route worse than object-shaped ones? | *"I don't know which way that goes, and neither does anyone here. Cheap to find out and expensive to assume."* |

**Both are probes of the same boundary** — what a client LLM does with our tool layer — and **both are
build-independent.** Neither needs `mcp.pipermorgan.ai`, OAuth, or a deployed catalog. Each needs a
candidate text/schema and a client LLM.

**So they share a rig, and it can run now.** That matters beyond convenience: **both results change what
we build.** A negative on either changes the tool layer's output format or naming *before* the tools are
written. Learning them in Phase 2 means rework; learning them in Phase 0 costs an afternoon.

## Probe A — honesty under recomposition *(verdict: CXO's)*

**Question**: when Piper's tool output carries a hedge, a decline, or a confidence boundary, does that
survive into what the user reads — or does the client LLM smooth it away?

**Method**: author N tool-output payloads exercising our honest-decline discipline (uncertainty, partial
knowledge, explicit refusal, "I can see X but not Y"). Feed each as tool-result content to a client LLM
under a realistic system prompt. Compare the user-visible reply against the payload.

**Score**: did the caveat survive · was it weakened · was it dropped · was it **contradicted**.

**The design question the result answers** — and this is why it's Phase 0 rather than Phase 2:
> If hedges do not survive prose, the fix is **not in the rubric** — it's in the **output format**.
> Structured confidence fields the client cannot smooth away, rather than hedged prose it can.
> **That is a constraint on tools nobody has written yet.**

Run against **both** Claude and GPT: PDR-006 ships to both, and there is no reason to assume they
recompose alike. A divergence is itself a finding for the ChatGPT lane.

## Probe B — tool-selection accuracy by naming style *(verdict: PPM's, with Lead/Arch)*

**Question**: does the host LLM pick the right tool more reliably from **situation-shaped** names
(*"shape a vague idea into a spec"*) or **object-shaped** ones (*"create_spec"*)?

**Method**: two catalogs, same underlying tools, differing only in name + description style. A fixed set
of realistic user utterances spanning the three structures. Measure correct-tool selection rate, plus
wrong-tool and no-tool rates.

**Why it matters more than it sounds**: PPM's recommendation puts **product opinionation in the
catalog** — it's the answer to Jake's "lack of opinionation" complaint in the only form the plugin
permits. If situation-shaped naming routes *worse*, we'd be trading routing accuracy for differentiation,
and that trade should be made knowingly rather than discovered.

**Confound to control**: keep the tool *schemas* identical across arms. Only names and descriptions vary.
Otherwise the arms differ in more than the variable — the same confound class that cost this cohort five
seats and a week on the hook thread.

## What this spec deliberately does NOT do

- **It does not decide anything.** Probe A's verdict is CXO's (Layer-B rubric design); Probe B's is
  PPM's with Lead/Arch (naming + routing). PA is offering the rig and the sequencing argument.
- **It does not claim the work.** If CXO or PPM would rather run their own, better — this is offered so
  the questions don't sit waiting on a server neither of them needs.
- **It does not assume the results.** I have a hunch on A (prose hedges are fragile under paraphrase) and
  none at all on B. Both are worth running precisely because a hunch is not a result — which is the
  week's most expensive lesson, three times over.

## Sequencing

Belongs in **Phase 0**, alongside the privacy policy and annotation spec — the phase defined as
"no dependencies." Both probes' outputs feed **Phase 2** (what the tool layer emits, and what the
catalog is called), so running them late means building twice.

**Blocked on**: nothing. **Waiting on**: CXO and PPM to say whether they want PA to run it.
