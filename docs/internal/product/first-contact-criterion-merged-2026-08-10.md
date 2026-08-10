# First-contact criterion — the merged list

**Author**: PPM · **Date**: 2026-08-10 · **Status**: 🟡 proposed, not ratified — **PM's to bless**
**Supersedes for ratification purposes**: CXO's §7a as written, and #1536's ACs as written. **Neither
was canonical-ready.**

---

## Why a merge rather than a choice

Two candidate lists, each with the other's defect:

- **§7a** was designed *binary, and every one checkable now* — an excellent constraint that
  **systematically excluded the properties resisting binarisation** (provenance, non-fabrication,
  cold-start scope). **CXO's own diagnosis: *"the gate's selection criterion selected against its own
  purpose."*** Three of #1536's four properties are absent from it.
- **#1536's ACs** carry all four properties — and **had never been audited**. On the first pass they
  showed two holes: **AC2 is a judgment that cannot fail cleanly**, and **AC3 was scoped to the
  nothing-connected case** while fabrication is most dangerous when a connector *is* live.

⚠️ **The tempting shortcut was to pick the list with fewer recorded corrections.** That selects for
**absence of scrutiny** — §7a looks worse because three people examined it. **Corrections are evidence
of attention, not of fault** (CXO, taking the point).

**§7a contributes the discipline. #1536 contributes the coverage.**

---

## The structure was already built — §7a / §7b, two tiers

**CXO's spec already has the answer and the argument walked past it**: **§7a = binary gate items**;
**§7b = spec conformance, required for *done*, beyond the gate.** So the merge is **per-property
placement**, not list selection.

| # | Property | Tier | Why |
|---|---|---|---|
| **1** | With one tool connected and a **cold account**, the user's own data appears in the **first exchange, unprompted** | 🚪 **GATE** | Already binary and runner-checkable |
| **2** | What is shown is something **only Piper could produce** — not a capability list, not a restatement of the user's request | 📋 **§7b CONFORMANCE** | **A judgment. It cannot fail cleanly** and a runner can argue it either way. Reviewed for *done*; **never a gate item** |
| **3** | **No fabricated content** — every entity named is real, **whether or not a connector is attached** | 🚪 **GATE**, ⚠️ **by citation** — see below | Widened from #1536's empty-state scoping |

### ⛔ AC4 is deleted, not placed — it is entailed by item 1

#1536's AC4 read *"works from the first session, not after warm-up."* **Item 1 already says "cold
account" and "first exchange."** *First session* and *not after warm-up* are that same condition
restated. ⚠️ **CXO's placement table carries it as a fourth gate row; it doesn't need placing.**
**Three items, not four.**

---

## 🔴 Item 3 cites the general contract — and I checked whether the contract reaches it

**The move (CXO's, and it's right)**: my fix to their item 4 (*attribute verifiable against source*)
and the fix to my AC3 (*widen past the empty state*) **are the same predicate** — which would make it
**the sixth per-surface fabrication guard**, in the same week Arch documented *"we have solved
fabrication five times, never generally."*

> ⭐ **One predicate closing two holes in two documents is not elegance — it is the signal it belongs
> in neither.** So item 3 **cites** the general contract rather than restating it.

### ⚠️ But the contract may not reach this case, and that is worth resolving before citing it

`floor-honesty-contract-1517-spec.md` §3:

> **"An assertion about system state requires a read of that state. Fabrication is
> asserting-without-reading."**
> **H1** — no proposition about **stored state** (*saved / not saved / exists / doesn't exist / was
> deleted*) unless derived from a value the turn actually read.

**The headline property is general enough. H1's obligation may not be**, on two counts:

1. **H1's enumeration is storage-flavoured** — Piper's *own* persistence. First-contact fabrication is
   about an entity from a **connected external source** (a GitHub issue that doesn't exist).
2. 🔴 **More important: H1 governs *whether a read occurred*; item 3 needs *whether the named entity
   is real*.** **A read can occur and the particulars still be fabricated** — fetch the issue list,
   then hallucinate a title onto it. **H1 is satisfied; item 3 is violated.**

**So item 3 is currently: 🟡 BLOCKED on Arch confirming the contract covers *asserted particulars*,
not only *asserted-without-reading*.** ⛔ **Do not treat "cites the contract" as closing it until
that's answered.** *(Flagged to Arch as a consumer they may not have counted — CXO's framing.)*

---

## What PM would be blessing

**Not §7a's wording. Not #1536's ACs. This:** *the first-contact criterion is three items; items 1
and 3 gate; item 2 is conformance reviewed for done; item 3 is pending one architectural answer.*

⚠️ **And the placement question is unchanged and still separate**: *is the first-contact criterion in
#1386's beta gate at all?* **That decision has been pending since 2026-08-05 and this document does
not touch it** — it only makes sure that whatever gets placed is worth placing.

---

## Provenance

CXO (§7a, the two-tier structure, the selection-mechanism diagnosis, the sixth-guard catch) · PPM
(the AC list, the audit of both lists including my own, item 3's widening, AC4's redundancy, the
contract-reach check) · PA (independent audit confirming both holes) · Arch (the general contract).
**Four corrections across two specs in two days — none of the authors found their own holes first.**
