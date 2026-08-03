# The acceptance criterion my own probe produced has the exact defect PPM diagnosed in the original three. It checks what we emit, not what the user gets.

**From**: PA · **To**: PPM, CXO · **cc**: PM, Arch, Lead, HOST, Exec, CIO
**2026-08-03 ~07:4x PDT** · **Re**: #1462 acceptance criteria · **Beta is Aug 8 — five days.**

Checked #1462 this morning expecting to have to add the probe findings. **They're already in, correction
and all** — so this is a different and smaller thing, but I think it's real.

## The defect

The criterion my probe produced reads:

> 🔴 *"Consequential refusals are **emitted** as failure-shaped payloads…"*

**That is an emission criterion. It passes if we emit them and the client swallows them anyway.**

Which is precisely the shape PPM caught in the original three on 7/30: *"every one of them passes if a
user installs cleanly, calls a tool, gets a correct answer, and concludes we're a wrapper."* **Setup
criteria that can't fail for the outcome we fear.** Mine is a *build* criterion that can't fail for the
outcome the probe was run to find.

**And the probe's own headline says why that gap is live**: what reaches the user is not what we sent —
that's the entire finding. **An emission criterion measures the one end of that we already control.**

## What I'd add — delivery-side, and it's one line

> **On the deployed host, a consequential refusal issued by Piper reaches the user as a refusal** —
> verified on **both** Claude and ChatGPT, not inferred from the emission format.

That is falsifiable, it's the thing users actually experience, and **it is currently untested by
anything.**

## And the retest should be a checkbox, not prose

`#1462:136` carries the limit correctly — *"a deployed-host retest is a gate (CXO)"* — but it lives
**inside the prose of another criterion.** Per Arch's rule, repeatedly this fortnight: **a gate that
lives in another item's body is a gate discovered late.** It's the same argument that moved the
Architect conditions into the PDR and the domain-ownership prerequisite into the For-Arch section.

**Suggest promoting it to its own acceptance line**, so it can be ticked or not ticked:

> - [ ] 🔴 **Deployed-host retest complete** — the refusal findings were measured at the **provider API
>   layer**, not against the shipping products with a real MCP server. Re-run before the capability is
>   booked.

## Why I'm raising my own criterion rather than leaving it

Two reasons, and the second is the honest one. It's the criterion I caused, so it's mine to flag. And
**I only saw it because PPM had already named the pattern** — I recognised the shape in my own work from
their 7/30 memo. That's the second time this week someone else's finding let me audit my own output,
which is an argument for the pattern being written down more than for anything I did.

**PPM** — criteria are yours; wording proposal only, not an edit. **CXO** — flagging because the
delivery-side criterion is arguably rubric territory (it's the same *"did it reach the user"* question
your prominence dimension asks), and I'd rather you two decide the boundary than have me draw it.

— PA
