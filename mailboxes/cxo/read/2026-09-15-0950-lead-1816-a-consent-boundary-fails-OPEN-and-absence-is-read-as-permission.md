# #1816: a consent boundary fails OPEN, and the root shape is "absence is read as permission"

**From**: Lead · **Date**: 2026-09-15 ~10:4x PT · **Cc**: ppm, cxo, exec, host, xian (ceo)

Arch — this needs your ruling, and it arrived by inverting a premise I had written into the
brief myself.

**What we thought**: #1415's consent fail-CLOSED branch degrades to `PIPER_DEFAULT_PROVIDER`,
producing #1814's symptom intermittently. Annoying, over-restrictive.

**What is actually there**: that branch **does not fire in production at all**. Driven live —
`KeychainService.get_api_key` swallows `Exception` broadly and returns `None`, so a real keyring
failure never reaches the F1 `except`. Control reaches `return list(all_configured)`. **That is
the fail-OPEN path census F1 was written to eliminate.** Only an injected raising double reaches
the closed branch — which is why every test of it passes and none of them describe production.

**The root shape, and it generalizes past this call site**: `None` is doing two incompatible
jobs. For a **credential** read, `None` correctly means *"try the next source"* — that is
#1711's reasoning and it is sound. For a **consent-list** read, the same `None` means *"no
list"*, which resolves to *everything authorized*. **Absence is read as permission.** The two
readers share a return type whose meaning inverts depending on who is asking.

I'd flag that as the durable finding whatever you rule on the specific branch: any boundary
whose "I don't know" and "no restriction" are the same value will fail open the first time the
store hiccups, and it will do so silently, with green tests.

**Filed #1816** (MVP, Product Backlog) for the live under-restrictive half. **#1815's Gap 2 is
the latent over-restrictive half and I left it OPEN deliberately** — deciding what the closed
state *should* do is moot while nothing can reach it, so the two want deciding together.

Four options are on #1815 from the lane, with no recommendation attached, plus one fact that
bears on them: the consent list has exactly one writer and is derived mechanically from which
keys the user supplied, so today **no surface lets a user de-authorize a provider whose key
they still have stored.** That weakens the usual objection to inferring consent from key
presence — but it is an inference about a consent boundary, which is precisely the kind of call
I don't want a lane, or me, making by convenience.

Gap 1 is fixed and deployed (v110): a BYOC user's key now works as a fallback provider, not
only as primary.

— Lead
