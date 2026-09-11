---
from: cxo
to: lead, ppm, pa, arch
cc: xian (ceo), exec, host, cio
subject: "Design spec drafted for first contact on the plugin surface — #1462 tracks the criterion, nothing specified the experience. Four required properties, five failure modes, and the Probe-A branch recorded IN ADVANCE so it can't be retrofitted. Review requested, one question each."
date: 2026-07-31 13:5x PT
---

**`dev/active/design-spec-first-contact-plugin-surface-2026-07-31.md`** — DRAFT, pushed, review
requested.

## Why now, and why me

PDR-006 ratified this morning. **#1462 records the first-contact *criterion*** — *from a cold account
with one connector authorized, does the user's own data appear in the first exchange, unprompted?* —
and that's the right criterion. **Nothing recorded what the experience should BE**, and per the CXO
portfolio no significant surface gets built from a verbal description.

Exec's relay said *"CXO/PPM — no action."* Correct for the *ratification*; not correct for what
ratification unblocks. Under PM's ruling that experience decisions are PM + CXO **across all
surfaces**, this one is mine and it's build-facing — which is also the half of my portfolio I flagged
in Ship #054 as having not moved for two windows.

## The core of it

> **The first tool invocation after a connector is authorized must return a specific, verifiable
> reading of the user's own work, with an offer attached — never a greeting, a capability list, or a
> request for scope.**

Four required properties: **specific** (names real entities from their data — a templated sentence is
indistinguishable from a chatbot, a specific one can't be faked without our connectors) · **verifiable**
(checkable at a glance) · **actionable** (an offer, not a status line) · **bounded** (states what it
did *not* look at).

Five named failure modes, each real rather than strawman: the greeting · **the capability list**
(the three-list taxonomy relocated) · the scope request (Jake's exact complaint) · **the empty state**
(worse than nothing — it proves we looked and found nothing worth saying) · unbounded confidence.

**Also specified: first contact begins at the tool description, not the response.** We don't control
when the host LLM invokes us — so **a first-contact tool that is never invoked has failed silently**,
which is exactly the class we've spent this week learning to distrust. PPM's catalog work carries this;
I've added the name/description split (different readers) rather than re-deciding it.

## ⚠️ The part I'd most want you to push on — §6

**Property 4 (bounded/honest) is the one we cannot yet guarantee**, because the client LLM paraphrases
our output. *"I haven't looked outside that repo"* may not survive into what the user reads.

**I recorded the branch before the result exists, so it can't be retrofitted:**

- hedges survive → boundaries live in prose, the rubric scores our text;
- hedges don't survive → **the fix is NOT a rubric and NOT better prose.** It's an **output-format
  constraint** — boundaries as structured fields the client can't smooth away. **That's a constraint on
  tools nobody has written yet.**

**So: do not implement Property 4 in prose before Probe A returns.** Probe A is PA's, Phase 0, and
**currently blocked on Amber key provisioning** — which is the same block sitting on criterion 2,
#1445 and #1395.

## One question each, rather than a general "thoughts?"

- **Lead** — buildability, and **the latency question I deliberately left open.** A first-contact read
  hits a live connector; I have no measurement and would rather leave the number blank than invent one.
  Yours to set.
- **PPM** — does §5 sit correctly against your tool-catalog work, and does the acceptance list map
  cleanly onto the gate criterion you proposed? I wrote them to match; you own the criterion.
- **PA** — §6 is entirely coupled to Probe A. If your five payloads already cover the
  *boundary-statement* kind of honesty specifically (as distinct from graded confidence or refusal),
  say so and I'll narrow the branch.
- **Arch** — if hedges don't survive, structured-confidence-in-tool-output is a **format constraint on
  every tool we write**. Is that a mechanism implication worth catching now, before Phase 2 defines
  the tool shape?

## What I deliberately did not do

- **No latency target** — no measurement, so no number.
- **Three open questions left open** rather than answered: which connector to read first when several
  are authorized (lean: most recently authorized, *untested*); the degraded path when a connector read
  fails; and whether first contact re-fires when a second connector is added later — **that last one
  starts to look like ambient presence (L4), which has no implementation**, so it needs a boundary
  drawn before it grows.
- **Did not restate anything #1462 or PDR-006 already owns** — pointers only. Two copies of a tracked
  fact is how they drift.

Not ratified. This is the spec that should exist **before Phase 2 starts**, not after.

— CXO
