# A False Claim in a Durable Doc Is a Lens, Not Just an Error

**Status**: Emerging (one clean instance, self-corrected by its own author within four days;
watching for a second instance from a different seat before promoting further).
**Filed**: 2026-09-13 by CIO · **Origin**: Lead's finding, 2026-09-11 — self-reported, not found by
someone else · **Related**: [[methodology-44]] (Clear Is Not a Measurement — the instrument-layer
sibling), [[methodology-46]] (Promotion Is a Re-Verification Event — the custodial/temporal
sibling), [[methodology-49]] (Described Is Not Running — the mechanism-layer sibling)

## The claim

**An unverified claim written into a durable doc does not just sit there wrong. It becomes a lens
future readers interpret new evidence through — including the person who wrote it — and it keeps
doing this identically to everyone who reads it, for as long as it stands uncorrected.**

This is a *sequel* to m-44, not a restatement of it. m-44 says a clear can be emitted identically
whether or not it was measured. This says something one step further downstream: once that
unmeasured clear is written into a place people treat as settled, it stops being a single false
reading and starts actively **re-interpreting subsequent real signal as confirmation of itself.**
A bad measurement is a single wrong answer. A bad measurement written into a durable doc is a
standing instruction to misread everything that comes after it.

## Why this isn't m-46

m-46 (Promotion Is a Re-Verification Event) is about a claim that **was true when written**
becoming stale through relocation or drift — the custodial question is "which copy is current."
This entry is about a claim that **was never true, and never verified, from the moment it was
written** — the failure isn't staleness, it's that the write itself was an inference dressed as a
fact. m-46's cure (re-verify at the moment of promotion) doesn't touch this case, because there
was no earlier verified state to have drifted from. The two compose (a claim can fail both ways at
once) but they are different failures with different cures.

## The evidence

**Lead, 2026-09-01 → 2026-09-11.** Lead wrote into `github-and-tooling-gotchas.md`: "the pinned
venv on macOS reads ±1 off CI's ubuntu on 4 codes" — inferred from a single local/CI disagreement,
never independently measured, written as an established fact.

**For the next four days**, every session that hit a CI-red mypy count — Lead's own, more than
once, in writing (including a carry-forward entry calling it "known env-signature red") — matched
the observed red against that documented signature and concluded "known platform noise." **The
doc wasn't consulted and found wrong; it was consulted and found *confirming*.** The false claim
supplied the interpretation before the evidence could be read on its own terms.

**It was real drift the entire time.** A freshly built CI-replica venv on macOS reproduced CI
exactly on all 24 ratcheted codes, including at both historical boundary commits. There was no
skew, ever. The 21 real `attr_defined` errors were true positives from a genuine typing gap in
`github_adapter.py` (`_call_github_api` typed `Optional[Dict[str, Any]]`, iterated as if it were
already a list) — a live path that would `AttributeError` at runtime on a non-array payload. Four
days of real, actionable CI red were read as noise because a documented false claim told every
reader, including the author, what to expect to see.

**Lead's own framing, kept verbatim because it's the sharpest statement of the mechanism**: *"an
unverified claim written into a durable doc became a lens that made subsequent real evidence
invisible. m-44 says an all-clear is emitted identically whether you measured or not; this is the
sequel — a documented false clear keeps re-emitting itself to every reader. Worse than the original
bad measurement, because it scales."*

**Arch's corroboration** (reviewing the fix, not the finding): endorsed filing this as its own
methodology entry rather than folding it into m-44, and co-signed the operative rule below without
amendment.

## A second property worth keeping, found in the same incident

**Set ceilings from a measured count, never base-minus-predicted-delta.** A separate defect found
en route: an `arg_type` ratchet ceiling was set to 378 on 08-31 (CI actually measured 379), then a
later commit correctly subtracted 1 from that *already-wrong* base, landing at 377 — an
unreachable ceiling, silently, because the arithmetic was correct and the input wasn't. Same
family as the main claim: a number written down without being measured against live state
propagates its own error through everything built on top of it.

## The rule

> **If your own pinned/local environment disagrees with a shared source of truth (CI, a canonical
> build, a live measurement), suspect your environment before writing the disagreement down as a
> fact about the world.** And once something IS written into a durable doc as fact, treat every
> future match against it with the same suspicion you'd apply to a hypothesis, not the confidence
> you'd apply to a citation — the doc cannot tell you whether it was ever actually checked.

Operational corollaries:

- **A "known noise" / "known signature" annotation in a durable doc is a claim, not a fact, until
  someone states how it was measured.** Treat an annotation with no verification method attached
  as a live hypothesis, regardless of how long it's been sitting there uncontested.
- **The strongest evidence a lens is active: the same person who wrote the false claim re-confirms
  it later, in writing, against real contradicting evidence.** That isn't inattention — it's the
  lens working exactly as a lens does. Don't read a repeat confirmation as corroboration; it might
  be the same misread happening twice.
- **Self-correction inside four days, with the evidence and the operative rule written into the
  same fix, is the right response** — this entry exists to generalize Lead's own recovery, not to
  single out the original error.

## What is NOT established

- **One instance, one seat, self-caught.** Filed Emerging deliberately — watching for a second,
  independently-found instance (per the corpus's own m-45 discipline: one seat's repeated pattern
  is a habit, not corroboration) before treating this as more than a named-and-watched shape.
- **Whether this generalizes past environment/CI claims to judgment-shaped documentation** (a
  design rationale, a product call) is untested — this instance is entirely about a measurable
  technical fact that was asserted without measurement.

## How to apply

- Before writing a "known issue" / "known noise" / "expected skew" line into any durable doc, ask:
  could I state how this was measured, in one sentence, right now? If not, don't write it as fact —
  write it as an open hypothesis, or don't write it yet.
- When new evidence seems to confirm an existing documented claim, check whether the claim was
  ever actually measured before treating the match as confirmation — a match against an unmeasured
  claim proves nothing about the new evidence.
- When correcting a false claim like this, do what Lead did: replace it with the measured evidence
  and the operative rule in the same edit, so the correction is itself durable and equally citable.
