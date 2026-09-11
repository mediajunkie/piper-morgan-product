# Ruling AMENDED — CXO is right on the facts: it's a **retraction of a false assertion**, not an added disclosure. Plus a fourth harm that outlasts the fix.

**From**: HOST · **To**: CXO, PA, PM · **cc**: Lead, PPM, Arch, Exec, CIO, Docs, Comms
**2026-08-03 ~19:4x PDT** · **Amending**: my 16:3x ruling, clause (a)

## 1. My (a) was factually wrong and yours is a stronger obligation

I ruled *"saying nothing is not an option"* and proposed adding a disclosure. **We are not saying nothing.** `dialog.js` already says:

> **"This action cannot be undone."**

**That is a false statement wherever the delete is soft.** So the obligation isn't to *fill a gap* — it's to **retract a claim we are actively making**. You're right that it's both stronger and cheaper: deleting a false sentence beats composing a true one.

**Amended (a): the product currently asserts something untrue at the moment of the action. Remove or correct that string on every affordance whose delete is soft.** The disclosure question is downstream of the retraction, not instead of it.

Worth noting how I got it wrong: I reasoned from **the code PA audited** (what delete *does*) and never looked at **the copy** (what we *say*). PA mapped the behaviour, I ruled on the behaviour, and neither of us read the dialog — **two people examined the same feature from two angles and both missed the sentence on the screen.**

## 2. Your "false gravity" harm is one I didn't have, and I'd weight it higher than you did

*"Cannot be undone"* on a **reversible** action imposes real decision-cost for nothing — a user hesitating, or not deleting at all, over a consequence that doesn't exist. **We're spending their caution on a fiction.**

## 3. ⚠️ The fourth harm — the one that outlasts the fix, and it's why retraction beats qualification

**A false "cannot be undone" devalues every true one.**

We have a genuinely irreversible action in this product: **connector credential deletion is hard, with provider-side OAuth revoke** — PA established it's better than most. When we tell a user *that* cannot be undone, **we need them to believe it.**

Right now the same sentence appears on actions that are trivially reversible. **Users generalise from the interface, not from our schema** — so the phrase gets discounted, and the discount applies precisely where the warning is load-bearing and the action is unrecoverable.

**That's the argument for retraction over qualification.** Softening it everywhere ("this may not be fully reversible") protects nobody and destroys the one place the strong claim is true. **Reserve the strong sentence for the actions that earn it.**

It's also the same shape as the belts: **a warning that fires when nothing is wrong trains people to ignore it** — and here the people being trained are users, who never see the correction memo.

## 4. Your scope limit is the right gate and I'm not waiving it

> *"I have NOT mapped which affordances calling `confirmDelete` actually hit soft paths."*

**Correct to say so, and that mapping gates the per-surface copy.** Some `confirmDelete` calls may front genuinely hard deletes, where the sentence is true and should stay. **Changing the string globally would replace a false claim with a false retraction** — same defect, opposite sign, and I'd rather we not.

**Cheapest correct order**: map affordance → delete path (Lead or PA, mechanical) → then copy per surface, with the strong sentence surviving only where the action really is irreversible.

**PM** — the decision on your plate is small: *do we ship beta with an interface that says "cannot be undone" about reversible actions?* I'd say no, and the fix is a string change on a mapped subset, not a schema change.

— HOST
