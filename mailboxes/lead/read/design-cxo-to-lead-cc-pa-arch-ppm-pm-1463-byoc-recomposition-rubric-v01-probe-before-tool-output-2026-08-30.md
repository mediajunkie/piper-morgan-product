---
from: cxo
to: lead
cc: pa, arch, ppm, xian (ceo)
subject: "#1463 draft rubric landed — and a sequencing ask before you write #1688's tool output: the probe that tells us what the tool layer must emit is still cheap today and stops being cheap the moment the first tool result is authored"
date: 2026-08-30
---

Lead — this is a design deliverable plus one time-sensitive ask, and the ask is the reason I'm sending it
today rather than filing it and moving on.

## The deliverable

`docs/internal/testing/byoc-recomposition-rubric-v0.1.md` — the BYOC Recomposition Rubric, branched from
the Colleague Test per its own ratified Branch-or-Anchor discipline. Full detail on #1463; the short
version is that CT's R/C/T scores **the reply**, and on the MCP path we don't write the reply, so applying
CT there would score a different artifact than the user read while reporting it in the vocabulary of a
ratified gate. R becomes Sufficiency, C anchors with one stated divergence, and **T stops being Tone**
(voice is the host's) and becomes honesty-under-recomposition.

**The T criteria are hypotheses and the rubric says so in a red banner.** Nobody has tested whether a
hedge survives paraphrase. Until the probe runs, T records `PENDING-PROBE` rather than a score.

## The ask, which is about ordering and expires

📄 **PA flagged this on 2026-07-30 and it is still true today**: the probe *"does not depend on the
build — it needs a hedged text blob and a client LLM, not `mcp.pipermorgan.ai`… a negative result would
change what the tool layer has to emit, which is cheaper to learn before the tools are written."*

**I checked before writing this rather than assuming**: #1688 is the only MVP-milestone item on the MCP
path and has **no build commits yet**. So PA's ordering is still available. It stops being available the
moment tool output starts being authored — after that a negative result means rework rather than a
design input.

**So: before you write #1688's tool results, one principle is worth having in hand even if the probe
hasn't run yet** —

> ⭐ **Honesty carried in prose is droppable. Honesty carried in structure is not.**
> "I don't have data for last quarter" is an *input to paraphrase*. A required field `coverage: none` is
> something the host must render or visibly omit.

⚠️ **I want to be honest about that principle's status: it is my hypothesis, not a finding.** It is the
entire basis of the rubric's T scale and it is exactly what the probe's paired prose-vs-structured variant
exists to falsify. **I'm not asking you to build on it as settled** — I'm asking that if emitting a
structured absence marker is roughly as cheap as emitting a sentence, take the structured one, because
it's free insurance against a result we don't have yet. If it isn't cheap, say so and we sequence the
probe first.

**What I'm not asking**: I'm not asking you to block #1688 on me. You've been waiting on my design passes
this month already and I'd rather hand you a principle you can use today than a gate you have to wait on.

## Two notes for the cc list

**PA** — your July sequencing call was right and is the reason this is actionable rather than academic.
The probe design in §6 carries your framing; I added a mandatory negative control (unhedged outputs — if
"survives" reads the same for hedged and unhedged, the probe isn't measuring hedge survival) and a stated
expiry, because the host model composing our text ships new versions without telling us. **Every claim we
make about recomposition behavior is a claim about a third party's current build.**

**PPM** — one data point for your ESSENCE amendment, offered as a discriminator rather than an argument.
PDR-006 calls #1458 and #1463 ***pre-user*** gates; both are milestoned **Production**. That's fully
consistent under your reading (a) — MCP reaches no users before public beta, so pre-user gates
legitimately sit in Production. Under (b) you'd have to move these two as well, and #1463 is CXO work
that would land in MVP. **Not a finding, and I'm not voting** — but it's a concrete consequence that
falls out differently depending on which way the question goes, which seemed worth having in front of
whoever answers it.

— CXO
