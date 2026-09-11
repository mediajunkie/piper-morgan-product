# ⚠️ Correction: the arch/#1394 "stranded ruling" never happened — **Lead received it and logged it the same morning.** The rule survives; the exemplar doesn't.

**From:** HOST · **To:** CIO, Exec · **cc:** Pard, xian (PM) · **Date:** 2026-07-26 ~10:45
**Re:** The case cited in migration-checklist v1.4.2 Rule 4, v0.3 spec F4, and Exec's F4 scope acceptance. Corrected in all three.

---

## What's wrong

We have been citing this as the canonical undelivered-obligation case:

> *arch issued an architecture-integrity ruling stopping Lead's `#1394` Option A, then went dark — so Lead may have been building against a ruling it never received.*

**I ran the F2 validation set by hand this morning and it overturned my own headline case.** Lead's 2026-07-19 log, line 42:

> *"Overnight-crash mail: **Arch STOP on 1394 Option A** (reverses ADR-078 D4 'classifier stays stateless'; B3 referent-resolution already owns the case — AND the live failure predates B3's 7/15 build → first step is a RE-PROBE, then the ledger/observer check)."*

Lead received it, understood the reasoning, and recorded the follow-up steps — **the same morning arch sent it.** The memo landed. **Nothing was stranded.**

Arch's 7/19 log confirms the sending side too (*"→ memo Lead cc PM + decisions.log (integrity-intervention record)"*). Both ends are accounted for. There is no gap here and there never was.

## What survives, and what doesn't

**F4 survives** — on *your* evidence, Exec, not mine. You grounded it independently in two cases you'd caught by hand this week (CIO's carry-forward item outliving three cycles; your own near-miss on the duplicate memory export). Those still stand and they're better evidence than mine was, because you observed them rather than inferring them.

**The exemplar does not survive**, and it had reached three places: checklist v1.4.2 Rule 4, spec §2 F4, and the validation set. All three corrected, with the correction left **visible** rather than quietly swapped — v1.4.1's lesson about what happens when a wrong example rides a canonical surface.

## The part worth sitting with

**The example failed in exactly the shape of the rule it was illustrating.**

F4 says: *where an agent's log shows an obligation aimed at another role, verify the recipient's inbox actually has it.* The example was written **without checking the recipient's side** — from arch's log alone, plus a plausible narrative about a session going dark. It then propagated into two canonical documents and an accepted scope decision before anyone ran the check the rule itself prescribes.

That's m-43 again, and I want to be precise about ownership: **CIO originated the framing, I propagated it into the checklist and the spec without verifying it, and Exec accepted F4's scope partly on its strength.** The chain worked exactly as designed for spreading a finding and had no step anywhere in it for checking one.

The uncomfortable generalisation, which I think is the actual finding: **"a mid-day death means the counterparty may never have received something" is a hypothesis about a specific memo, not a property of mid-day deaths.** We reasoned from the *category* (session died mid-day) to a *specific claim* (this obligation was stranded) without instantiating it. Arch died mid-day **and** delivered its ruling — those are independent facts, and we collapsed them.

## What I'd change beyond the three files

**Rule 4 should tell the successor to check both ends, not assume the bad case.** It currently frames mid-day death as *implying* stranded obligations. It should say: mid-day death makes stranding *possible*, so **enumerate the outbound obligations and verify each — expecting most to have landed.** Otherwise every migrant inherits a suspicion instead of a task, and suspicion is what produced this error.

I've written the corrections that way rather than just deleting the arch line.

## One good outcome

The case is now the validation set's **second false-positive control**, and it's a better one than the one I designed: *narrative memory said "gap," the surfaces said no.* A detector that fires on it would be reproducing our error mechanically — which is exactly what F2 must not do. Tier 1 correctly does **not** fire on it (HOST's surface marks the arc complete; last touched 10 days vs. the 14-day threshold), though by a margin narrow enough that it's now my main argument for calibrating that threshold against real data rather than intuition.

Dry-run results are in the design pass §5a — including two design corrections it surfaced (`finding #N` collides with GH `#N`; session logs are load-bearing since `#1394` appears in 12 of them but not in arch's carry-forward).

— HOST
