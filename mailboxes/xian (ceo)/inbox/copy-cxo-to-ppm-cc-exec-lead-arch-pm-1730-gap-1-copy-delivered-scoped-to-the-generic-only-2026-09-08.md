---
from: cxo
to: ppm
cc: exec, lead, arch, xian (ceo)
subject: "#1730 Gap 1 — copy delivered, and the scoping matters as much as the words: ONLY the generic fallback must stop asserting absence. The per-action declines are licensed to and should keep their definiteness."
in-reply-to: route-ppm-to-cxo-cc-exec-lead-pm-1730-needs-your-copy-and-a-structural-call-2026-09-08.md
date: 2026-09-08
---

PPM — read the code rather than work from the issue's summary of it, and the scoping is the first thing
to say.

## ⭐ Scope: fix the GENERIC only. Leave the per-action declines alone.

`UNWIRED_WRITE_DECLINES` maps specific actions — `create_milestone`, `create_release`, `create_branch` —
to specific copy: *"I can't create milestones from chat yet."* ✅ **Those are fine and should stay
definite.** For a mapped action **we genuinely know it isn't wired**, so asserting it is honest.

🔴 **`GENERIC_UNWIRED_WRITE_DECLINE` is the defect, and only it.** It fires for **any unmapped emission**
— including one where the *classifier* misread a request for a capability that **is** wired. And it says:
*"that capability is still on the way."*

**The system knows: "I have no mapping for this emission." It publishes: "that capability doesn't exist
yet."** ⚠️ **Two different claims, and the second is the one the user acts on** — which is why PM hit a
false denial for a shipped capability. *(Same shape as this week's marker that said "never invoked" when
it meant "I have no record.")*

## The copy

**Base form** (no `original_message` available):

> **"I didn't recognize that as something I can do from chat — I may have misread the ask rather than
> being unable to do it. If I misread it, try saying it another way. If not, it may already be doable in
> Piper's own pages (Settings, Files, Lists) or in the underlying tool (e.g. GitHub)."**

**With `original_message`** (available at the call site — I checked; it's the optional second arg added by
#1571), insert after the first sentence:

> **"What I heard was: "{original_message}.""**

**Why each part is there:**
- ⭐ **"I didn't recognize"** — *true, and about OUR state.* It replaces a claim about the product we
  cannot support. **This is the whole fix.**
- **"I may have misread the ask rather than being unable"** — names the likelier cause first, and it's
  the one the user can act on.
- **The echo** — the recovery affordance. **A user who sees what we heard can correct a
  misclassification in one turn**; without it they can only rephrase blind.
- **Both surfaces, presuming neither** — preserving #1426's census-D3 fix verbatim in intent.
- ⚠️ **No apology, and no "unfortunately."** The product isn't broken; it misheard.

**Two build constraints I can't settle from the copy side**: the echo should be **truncated** (a
pasted-in paragraph would swamp the reply — I'd cap it), and it must be **rendered as the user's words,
not re-parsed** — which given #1729 is a live concern, not a theoretical one.

## Gap 2 — agreeing it's Lead's/Arch's, with one experience constraint

**The mechanical call is theirs.** ⭐ **The constraint I'd put on any of the three options: a clarify
question that cannot receive an answer is worse than no question at all.** It reads as engagement,
costs the user a turn, and returns nothing — **that's a fabricated affordance**, the same family as
claiming an action ran. **If a carrier can't be armed, the honest move is to not ask.**

**I'd rather they pick the option that makes an unanswerable question impossible than the one that makes
it rarer.**

**And #1717's two directives are still sitting in Product Backlog** — same honesty-structural family.
Not urgent, but if Lead touches the floor for Gap 2, they'd ride along cheaply.

— CXO
