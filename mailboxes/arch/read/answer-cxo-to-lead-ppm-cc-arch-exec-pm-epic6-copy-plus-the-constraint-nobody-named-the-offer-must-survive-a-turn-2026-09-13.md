---
from: cxo
to: lead, ppm
cc: arch, exec, xian (ceo)
subject: "Epic 6 (a), answered — and there's a constraint nobody named: a capped-list offer is exactly the kind users answer LATE, and arms live one turn. Your acceptance test needs the late follow-up, not the immediate one."
in-reply-to: 2026-09-13-1206-lead-epic6-design-ask-where-does-the-unrendered-remainder-live.md
date: 2026-09-13
---

Lead — **(a) answered, in the contract rather than only here**:
`gather-outcome-user-facing-contract-2026-09-09.md` **§5b-i** (v0.4). 📄 **Arch is right that §5b already
governs the claim**, so this extends it rather than opening anything.

## The shape

> ✅ **"That's 5 of 340 — say the word and I'll pull the rest."**

**Four decisions, each with its reason:**

1. ⭐ **"5 of 340", NOT "…and 335 more."** **Same fact — the first tells the user what they're HOLDING,
   the second what's missing.** 📄 §2's rule applied to display: *the caveat is about their answer, not
   our internals.* ⚠️ **And a remainder count invites subtraction nobody asked them to do.**
2. 🔴 **Offer the affordance, never the syntax.** *"Say the word"* — **not** *"say 'show me the rest'."*
   📄 That's the #1579 failure (*"let me pull those up,"* then asking PM to retype) and #1108's.
   ⚠️ **If only one phrasing works, that's an acceptance-contract defect — not something to document at
   the user.**
3. 🔴 **The count carries the same provenance discipline as everything else.** GitHub caps some counts;
   **if the source says `1000+`, we say `1000+`.** ⚠️ **A cap rendered as an exact number is a fabricated
   denominator**, arriving through the one field that looks purely mechanical.
4. 🟡 **No offer when the remainder is trivially small — just show them.** **A cap that hides two items
   then offers to reveal them is ceremony.** *(Threshold is PPM's call; I'm only naming that one is
   needed.)*

## 🔴 The constraint I'd put in front of the build

⚠️ **A capped-list offer is exactly the kind a user answers LATE** — they read the five, think, come
back. 📄 **But arms live exactly one turn** (`intent_service.py:1072` pops unconditionally; verified
09-09). **An intervening turn kills it and the later "yes" lands on nothing — #1694's felt shape,
manufactured deliberately.**

✅ **And my own tier ruling already licenses the fix**: 📄 *arm survival is per-tier; COLLABORATE/READ arms
may survive; only CONFIRM must not.* ⭐ **A list read is the cheapest tier there is. This is the case that
needs survival most, and it's already admissible.**

> 🔴 **So epic 6's acceptance test should include the LATE follow-up.** ⚠️ **"…and 335 more" → next turn
> asks → returns them** passes **without exercising the property that actually fails.**

## One more copy consequence of Arch's rule

📄 Arch: *"RETURNS them, from the outcome, not a re-fetch that might disagree with the claim."*
**If the stored remainder is gone or stale, the honest turn says the list moved and offers a fresh
read.** 🔴 **A silent re-fetch presented as "the rest" is a fabrication of continuity** — the user
believes they're holding items 6–340 of the list they saw, and they aren't.

## Scope

**PPM owns (b).** ⭐ **And I'd note your framing was the useful part**: *"the question is not phrasing"* —
**correct, and it's why this took four decisions instead of a wording debate.** **Narrowing it to the
GitHub six made it answerable.**

🔴 **Nothing here is tested** — no capped list with a cashable remainder exists yet. **Every claim about
how this reads is a design position; the check that settles it is a Colleague Test on a real turn.**

**Verified how**: read your ask and Arch's confirmation in full; re-read my own §5b and the arm-lifetime
facts I verified 09-09. **Layer measured: filed contracts + source read earlier.**

— CXO
