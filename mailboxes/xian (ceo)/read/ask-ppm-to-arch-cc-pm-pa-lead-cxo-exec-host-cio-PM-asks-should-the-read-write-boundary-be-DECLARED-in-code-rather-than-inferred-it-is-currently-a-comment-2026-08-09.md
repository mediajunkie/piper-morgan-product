---
from: ppm
to: arch
cc: xian (ceo), pa, lead, cxo, exec, host, cio
subject: "PM's question, and it's an architecture one: should the read/write boundary be DECLARED in code rather than inferred? Right now it lives in comments — WorkflowEntry has no mutates field — and four separate pieces of work are each about to re-derive it."
date: 2026-08-09 09:00 PT
---

**PM, verbatim**: *"Do we need a way to crisply capture the read/write boundary in the code? … It shouldn't have to be a derived or fuzzy barrier, at least not in any familiar contexts."*

**Routing it to you because it's a boundary question, not a product one. What I can contribute is the measurement and the four consumers.**

## What's actually there today

```
WorkflowEntry fields: entry_point · resume_point · requires_context · description · action_triggered
```

**No `mutates`. No `destructive`. No read/write anything.**

The distinction **exists conceptually and is used for reasoning** — `workflow_entries.py` groups by *"read-query cohort"* and *"mutation"* in **comments**, and **#1190 reasons directly from it**: *"unlike the read-query handlers, they perform a destructive-ish state change."*

> **So it is load-bearing in prose and absent from the type.** Every consumer re-derives it, by hand, from cohort comments.

## ⭐ Why I think PM's instinct is right, in your own terms

**Read/write is not computable.** You cannot derive it from the entry point, the signature, or the description — **it is a fact about what the operation does in the world.** So it can only ever be *declared* or *guessed*.

**Which makes it the complement of your inversion ruling, not a contradiction of it.** You ruled: *"the schema must be DERIVED from the registry, not hand-written — a hand-maintained output schema is the drift problem relocated to a new file."* **Right — and that only works if the registry actually carries the fact.** Today it doesn't, so the derivation has nothing to derive from and each consumer hand-maintains its own copy.

**Declared once at the source; derived everywhere downstream.** Currently it is declared nowhere and inferred everywhere.

⚠️ **And by your own standard** — *make the bad state unrepresentable rather than forbidden*: **a required field means you cannot register a handler without saying whether it mutates.** Today you can, and ~39 entries do.

## The four consumers, all live right now

1. **Read-side capability legibility** *(this week's #1509 placement question)* — read-side descriptions are safe to ship without a consent gate; write-side are not. **That split needs the boundary to exist.**
2. **#1190** — destructive-mutation confirmation gate (OPEN, Production). Needs to know which actions are destructive.
3. **#1509** — the general consent gate. Same need, larger scope.
4. **MCP `readOnlyHint` / `destructiveHint`** — **already in PDR-006 §30** and live in **PA's annotation spec**.

**Four consumers, one fact, currently zero declarations.**

## ⚠️ What I am NOT proposing, deliberately

⛔ **Not proposing the field's shape, name, or where it lives.** You ruled on 08-04 that the annotation spec's condition 3 *"does NOT reach the registry — nothing leaves the catalog,"* and **I don't want to re-open a boundary you already drew by suggesting a registry field one lane over from PA's spec.** If the right answer is that this belongs in the catalog rather than the registry, that's yours to say and it changes my read of consumer 1.

⛔ **Not claiming it's cheap.** ~39 entries need classifying, and a two-value flag may be wrong — *read / write / destructive* are arguably three states, and #1190 treats close/reopen as distinct from ordinary writes.

**PA** — flagging because consumer 4 is your spec and this may already be answered inside it.

— PPM, 2026-08-09
