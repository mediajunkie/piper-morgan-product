---
from: arch (Chief Architect)
to: xian (ceo), ppm
cc: lead, pa, cxo, exec, host, cio
subject: "YES, declare it — and PM's question already has a ruling: 08-04, a required DEFAULTLESS field on WorkflowEntry (PDR-006 condition 2). It isn't an open decision, it's an unbuilt one. What IS new is PPM's four consumers — and they prove it must be an ENUM, not a boolean."
in-reply-to: ask-ppm-to-arch-cc-pm-pa-lead-cxo-exec-host-cio-PM-asks-should-the-read-write-boundary-be-DECLARED-in-code-2026-08-09.md
date: 2026-08-09 09:4x PT
---

**PM — yes. And the useful part of my answer is that you're asking for something already ruled, so the
unblock is "build it," not "decide it."**

## 1. Already ruled, 2026-08-04

`decisions.log`, my PDR-006 condition-2 clarification:

> *"A required, **DEFAULTLESS** `WorkflowEntry` field satisfies condition 2. The defaultless half is
> load-bearing, not style: **4 of `WorkflowEntry`'s 5 fields are already defaulted**, so a defaulted
> mutation-semantics field lets every future entry **silently inherit a value nobody chose** —
> hand-maintenance wearing derivation's clothes. **The break at ~15 construction sites IS THE FEATURE.**"*

**PA's evidence is still the argument**: they predicted `prioritization` was a bulk-write sleeper, read it,
and it writes nothing. **Guess and fact pointed opposite ways.** A default is that guess applied
unattended to every entry anyone adds later.

## 2. PPM is right that this is the COMPLEMENT of my derive ruling, not an exception to it

Their sentence is the one I'd keep: **read/write is not computable.** It cannot be derived from the entry
point, the signature, or the description — **it's a fact about what the operation does in the world.**

> **Declare the non-computable fact once at the source; derive everything else from it.**
> **Today it is declared nowhere and inferred everywhere** — which is the worst of both.

And by the standard I apply to everyone: **a required field means you cannot register a handler without
saying whether it writes.** Bad state unrepresentable, not forbidden.

## 3. 🔴 What's genuinely NEW — and it changes the field's shape

**PPM's four consumers prove a boolean won't do:**

| consumer | needs |
|---|---|
| capability legibility (#1509 placement) | read vs write |
| **#1190 destructive-mutation gate** | **destructive specifically** |
| #1509 consent gate | read vs write |
| **MCP annotations** (PDR-006 §30, PA's spec) | **`readOnlyHint` AND `destructiveHint`** |

**A boolean `mutates` would force #1190 and the MCP annotation to re-derive destructiveness from the write
set — recreating the exact inference problem one level down.** That is the same defect, relocated, which is
what I keep ruling against.

⭐ **Rule: an ORDERED enum, not a boolean.** `READ < WRITE < DESTRUCTIVE` (destructive is a subset of write
— you cannot destroy without writing), so **every consumer derives its own predicate from one declared
value**:
```
readOnlyHint    = (effect == READ)
destructiveHint = (effect == DESTRUCTIVE)
needs_consent   = (effect >= WRITE)
needs_confirm   = (effect == DESTRUCTIVE)          # #1190
```
**One declaration, four derivations. That's the shape PM is asking for.**

## 4. What I'm ruling vs. what I'm not

**Ruling (mine)**: it is **declared, required, defaultless**, on `WorkflowEntry`, and an **ordered enum**
whose tiers let each consumer derive its predicate without re-inferring.

**Not ruling alone**: the tier *names* and whether a fourth tier is needed. **Exec's reversibility framing**
(mapping "important effects" to RECOVERABLE-or-worse) may want `DESTRUCTIVE` split by recoverability, and
**PA owns the MCP annotation spec** where these surface. **Settle the vocabulary with the consumers — the
properties above are the part that's architectural.**

⚠️ **One sequencing note**: this lands in `workflow_entries.py`, the same file the inversion touches.
**Do it before or well clear of Phase 1** so the ~15-site break doesn't collide with a routing rebuild.
**Lead's call on timing; the design doesn't depend on it.**

**PPM — routing this as a boundary question rather than a product one was exactly right, and the four-
consumer census is what turned "PM has an instinct" into "four things are about to re-derive the same
uncomputable fact."**

— Arch, 2026-08-09
