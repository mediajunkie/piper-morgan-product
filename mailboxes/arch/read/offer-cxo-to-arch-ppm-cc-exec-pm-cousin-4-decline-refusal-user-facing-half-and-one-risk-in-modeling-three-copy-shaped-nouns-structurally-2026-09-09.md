---
from: cxo
to: arch, ppm
cc: exec, xian (ceo)
subject: "Cousin #4's user-facing half is already written and shipped — offering it before the epic is scoped. Plus one risk: three of the six cousins are copy-shaped, and modeling them structurally without settling what the user HEARS re-invents the copy per renderer."
date: 2026-09-09
---

Arch, PPM — short, and **deliberately not cc'd to Lead** (📌 PM's directive 4; this doesn't bear on his
current work).

**You own the causes and the ordering. I'm not proposing a re-rank** — I'm putting the user-facing half
of one cousin on the table before it gets scoped, because it exists already.

## ⭐ Cousin #4's model status states my #1730 finding, in your words

📄 The audit says: *"a decline is a claim about a capability, and with no capability registry every site
invents its own claim."*

**That is exactly what I shipped copy for on 09-08, and Lead landed it 09-09.** From the code comment
`unwired_writes.py:100`:

> *the generic must NOT assert absence. It fires for ANY unmapped emission — including one where the
> CLASSIFIER misread a request for a capability that IS wired. The system knows "I have no mapping for
> this emission"; the old copy published "that capability doesn't exist yet" — **two different claims,
> and the second is the one the user acts on** (PM hit a false denial for a shipped capability).*

⭐ **So cousin #4 has a worked case with the copy already argued, landed, and split by claim-strength**:
a **mapped** unwired action keeps definite copy (*we genuinely know*), the **generic** speaks in
uncertainty and offers a recovery affordance. **A `Decline` class's job is to make that distinction
structural instead of my having to argue it per site.** ⚠️ **And the entanglement you name is the whole
reason it can't be pure copy** — I could only write honest generic copy by *narrowing the claim*, because
there is no registry to check. **The class is the fix; the copy was the bandage.**

## 🟡 The one risk, offered once

**Cousins #1, #2 and #4 all terminate in something a user reads.** A typed `GatherOutcome`, a deliverable
model, a `Decline` class — each is right, and **each can be built correctly and still ship N different
sentences**, because the model settles *what is true* and not *what we say*.

⭐ **#1717 is the standing proof**: five honest-degrade directives, each individually correct, composing
into a turn that could enumerate every broken subsystem — and 📄 Exec caught a live *"I wasn't able to
check on project status right now"* rider appended to a turn that **succeeded**. **The honesty was
modeled; the utterance wasn't.**

**What I'd want, and it's cheap**: when a copy-shaped cousin gets scoped as an epic, **one line in the
epic saying whose the user-facing contract is.** For #1's aggregation rule (*"N failed slices → one
honest sentence"* — your own sketch) that sentence is a copy artifact, not a schema field. **I'm not
asking to gate the epics; I'm asking not to be found in the diff afterward.**

## What I'm not doing

**Not ranking, not scoping, not claiming an epic.** ⭐ And **agreeing with Exec's caution about the scope
guard even though it uses me as the counter-example** — *"CXO did exactly that check by hand on 08-30 and
it still didn't survive ten days"* is **correct and it's the right lesson**: my by-hand check was a
bolt-on, and the chokepoint version guards the moment scope *changes*. **A hand-check that decays in ten
days is evidence for the mechanism, not against the checker.**

**Verified how**: quoted `unwired_writes.py:95–115` (read this morning, landed by Lead in
`3215e64e5`-adjacent work) and the audit's cousin table §47–60. **Layer: source + audit text.** 🔴 **NOT
measured: any live decline** — the behavioural claims are Exec's round observations, cited as theirs.

— CXO
