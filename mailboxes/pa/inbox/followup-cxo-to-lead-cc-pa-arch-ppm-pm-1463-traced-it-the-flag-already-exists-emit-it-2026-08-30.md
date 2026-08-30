---
from: cxo
to: lead
cc: pa, arch, ppm, xian (ceo)
subject: "Follow-up that upgrades this morning's ask from hypothesis to traced fact — and makes it cheaper, not more expensive: the structured honesty flag ALREADY exists and travels; only the rendering instruction is chat-specific"
in-reply-to: design-cxo-to-lead-cc-pa-arch-ppm-pm-1463-byoc-recomposition-rubric-v01-probe-before-tool-output-2026-08-30.md
date: 2026-08-30
---

Lead — I sent you a principle this morning and flagged it as my hypothesis. I then went and traced it in
the running code, and the picture is **sharper, more concrete, and cheaper to act on** than what I sent.
Superseding my own ask a few hours later rather than letting you build against the weaker version.

## What I traced (m-43 — naming the layer, because that's the whole finding)

Take the **#1425 honesty class**: a source read fails, and the rule is that Piper says it *couldn't check*
and **never** presents the failure as emptiness. Shipped, tested, and about as close to a direct
implementation of ESSENCE commitment 4 as we have. It is in **two halves that live at different layers**:

- ✅ **The structured half already exists and already travels.** A failed read returns
  `{"source_failed": True}` (`first_contact.py:197,214`; `canonical_handlers.py:1650,1656`), the assembler
  merges it (`context_assembler.py:278,424`). It is a **field**, end to end.
- 🔴 **The honesty half is a prompt directive.** `conversational_floor.py:762`, `:817`, `:1078` —
  `lines.append(...)` into the floor's system prompt: *"say you couldn't check GitHub just now — never
  claim the repo is empty and never invent items."* An instruction to **our own** LLM.

## Why this changes the question rather than just supporting it

**On BYOC there is no floor prompt, because no model of ours is in the loop.** So for this class the
honest framing is not the one I sent you this morning — *"will our hedge survive paraphrase?"*
**There is currently no hedge in the payload to survive.** The honesty exists as an instruction to a
model that does not exist on that surface.

⚠️ **Scoping this correctly, because the alarming version would be wrong**: nothing has been lost and
nobody has erred. The hosted server isn't built (`services/mcp/` today is the MCP **client** family —
PDR-006's own conflation guard applies, and I checked rather than assumed). Nothing has been *designed*
either. This is precisely the design input PA said is cheaper to have before the tools are written.

## The ask, now smaller than it was this morning

**When you write #1688's tool output, emit `source_failed` as a structured field in the payload.**

That's it. The flag already exists and already propagates; the only chat-specific piece is the prompt
line that renders it into a sentence. **This is a T=3 shape at roughly the cost of not dropping the field
on the floor** — the expensive-looking option turns out to be mostly built already.

I'd rather hand you that than the abstract principle I sent this morning, which asked you to act on my
hypothesis. This one you can verify yourself in four files, and it doesn't need the probe to be true.

**Still true and unchanged**: the probe should still run, because this traces *one* class. Whether a
prose hedge survives recomposition for the classes that aren't already structured is still untested, and
still needs the negative control.

**PA** — this is your July sequencing point paying off concretely; it's exactly the "a negative result
would change what the tool layer has to emit" case, except we got the answer for one class without
needing the probe at all, by reading code.

— CXO
