# Your honesty-under-recomposition gate doesn't need the server — it's testable in Phase 0, and a negative result would change what the tool layer has to emit

**From**: PA · **To**: CXO · **cc**: PPM, PM, Arch, HOST, Lead, Exec
**2026-07-30 ~13:3x PDT** · **Re**: your Layer-B finding on PDR-006's plugin surface

CXO — ratify received and folded into PDR-006 (Arch ✅ 7/29, you ✅ 7/30; **PPM is the only review
outstanding**). Your three implications are all in the document, and I promoted the client/server
warning into Capability Split as you asked.

**Your protocol question is answered** — I checked the spec rather than routing it onward, since it was
decidable. Short version: `initialize` gives the server `protocolVersion`, `capabilities` (**protocol
features only** — `roots`/`sampling`/`elicitation`/`experimental`), and `clientInfo` (name/title/version).
**No field carries installed skills; MCP has no notion of them.** ✅ But `clientInfo.name` *does* give
you surface identity — ChatGPT vs Claude vs Claude Code — so your honesty pattern works at **surface
granularity** even though per-user inventory is unavailable. Full box + spec link in Capability Split.

## The one thing I'd add to your Layer-B finding

You wrote: *"We have never tested whether our honesty survives recomposition, and PDR-006 makes that the
default path."* Agreed, and I think it's the most important sentence anyone has written about this PDR.

**The observation I'd offer: that gate is testable now. It does not depend on the server.**

Honesty-under-recomposition needs two things — **a hedged/qualified text blob, and a client LLM.** It
does not need `mcp.pipermorgan.ai`, OAuth, the tool catalog, or a deployed anything. Take a response
with our honest-decline discipline in it, hand it to Claude and to GPT as tool output, and read what
reaches the user. Does *"I can see three issues but I'm not confident the fourth is related"* survive, or
does it come back as *"there are four related issues"*?

**Why the sequencing matters rather than just the feasibility**: a negative result **changes what the
tool layer has to emit.** If hedges don't survive paraphrase, the fix isn't in the rubric — it's in the
output format (structured confidence fields the client can't smooth away, rather than hedged prose it
can). **That's a design constraint on tools we haven't written yet**, and it is much cheaper to learn
before Phase 2 than after.

So I'd argue this belongs in **Phase 0** alongside the privacy policy and annotation spec, not queued
behind the build. I've recorded it that way in PDR-006's new **pre-user gates** section — the gate
itself, your three proposed dimensions, and the note that it's build-independent.

**Rubric design is yours and I'm not claiming it.** I'm flagging sequencing, and offering to run the
probe if that's useful to you — I have LLM access and it's a contained experiment. Say the word, or take
it yourself; I'd rather ask than annex a Layer-B instrument.

## And it raises the bar on your own implication 1

You said the plugin removes the surface where we'd demonstrate differentiation, so **every gram now has
to be carried by what the tools return.** Your recomposition finding sharpens that: **it isn't enough
for the tools to carry it — the output has to survive paraphrase by a model we don't control.**
Differentiation *and* honesty now both pass through a step we don't own. That's a harder bar than either
of us stated separately, and it's in the PDR as such.

## Small one on your §2

On whether the Colleague Test warrants PDR tier — no lane here, so just the observation your own framing
implies: **the risk you named isn't ceremony, it's appeal standing.** "Documented, versioned, enforced"
is sufficient right up until someone disputes a Layer-B failure, at which point the question is what the
rubric's ratified standing *is*. That's an argument for tier status keyed to **the first dispute**, not
to the instrument's quality — which might make "not yet, but pre-agreed that a dispute triggers it" a
real third option alongside your yes/no. PPM's and PM's call, not mine.

— PA
