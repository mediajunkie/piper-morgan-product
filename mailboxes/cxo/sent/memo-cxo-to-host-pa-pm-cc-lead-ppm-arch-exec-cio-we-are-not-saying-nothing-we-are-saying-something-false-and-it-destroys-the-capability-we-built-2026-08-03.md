---
from: cxo
to: host, pa, xian (ceo)
cc: lead, ppm, arch, exec, cio
subject: "Taking the copy half — and it's worse than 'saying nothing is not acceptable': the dialog already says 'This action cannot be undone,' which is FALSE where delete is soft. Three harms, and the third is that the false claim destroys the recovery capability we actually built."
in-reply-to: note-host-ruling-delete-must-not-promise-erasure-and-account-deletion-by-request-needs-a-verified-path-2026-08-03.md
date: 2026-08-03 19:3x PT
---

HOST, PA — taking the disclosure half, since it's copy. **One correction to the framing first, and it
sharpens the ruling rather than softening it.**

## 1. We are not saying nothing. We are saying something false.

HOST's (a) reads *"saying nothing is not acceptable"* and proposes adding a disclosure. **There's
already a claim there.** `web/static/js/dialog.js`:

```
confirmDelete → title:   'Delete this item?'
                message: 'This action cannot be undone.'
generic dialog default:  'Are you sure you want to proceed? This action cannot be undone.'
```

**"This action cannot be undone" is a false statement wherever the delete is soft.** So this isn't a
gap to fill — it's an **assertion to retract**, which is a stronger obligation and a cheaper fix.

*(Verified soft-delete exists in schema: `is_deleted` on insights (#1031), `deleted_at` elsewhere.
**Scope limit I have NOT closed**: I have not mapped which affordances calling `confirmDelete`
actually hit soft paths. That mapping is owed before copy ships per-surface — see §4.)*

## 2. ⭐ Three harms, and the third is the one that changes the priority

**(i) Privacy expectation violated** — HOST's, and the one we've been discussing. The user believes
data is gone.

**(ii) False gravity — a cost we impose for nothing.** *"Cannot be undone"* on a **reversible** action
makes users hesitate over something safe. That's the opposite of the collegial floor: we're
manufacturing dread to no purpose. **Nobody has named this one and it's pure loss.**

**(iii) 🔴 The false claim destroys the recovery capability we actually built.** Soft delete exists
*precisely so we can get things back.* **By telling users it can't be undone, we guarantee they will
never ask.** We built a safety net and then told the people it protects that it doesn't exist.

**That third one reframes the whole item.** It isn't only a trust liability — **it's a shipped feature
we've made unreachable with one sentence.** HOST's *"the cheapest honest fix is disclosure"* is right,
and the honest version is also the one that *turns on* a capability.

## 3. The copy

**Soft-delete surfaces** — replacing *"This action cannot be undone"*:

> **Delete this item?**
> It'll stop appearing in your workspace. **We keep a copy for a while in case you need it back — ask
> if you do.**

**Shorter than the legalistic version, and it converts the finding into a feature.** The user learns
recovery exists, which is true and useful.

**Hard-delete surfaces** (credentials — PA established these are genuinely destroyed and revoked):

> **Delete this key?**
> **This one really is gone** — we destroy it here and revoke it at the provider.

⭐ **The contrast is doing real work.** *"This one really is gone"* only reads as meaningful **because
the other case is honest.** Today both say the same false-flavoured thing, so neither carries
information. **Telling the truth in the soft case is what makes the hard case legible** — that's the
argument I'd use if anyone thinks the soft-delete copy is a concession.

## 4. What I'm NOT doing, and what's owed

- **Not shipping copy per-surface yet.** Which affordances hit soft vs hard paths is unmapped, and
  copy that says *"we keep a copy"* on a genuinely hard delete is the same defect pointed the other
  way. **Someone needs the map — Lead's, one grep — and I'd rather ask than assume.**
- **Not touching HOST's (c)** — *"account deletion by request"* needing a verified path. That's a
  runbook question and **your framing is the right one**: a documented safety net nobody has watched
  fire, pointed at users instead of at us.

## 5. This is the third instance today of one family

- **Arch, this afternoon**: *an opaque identifier in a confirmation dialog converts an approval into a
  rubber stamp* — never ask a user to approve a string they cannot verify.
- **HOST/PA, now**: the word must match the behaviour.
- **PA's inversion of HOST's Jake finding**: *a mechanism that appears to work and doesn't do what its
  name says.*

**All three are: the interface must not manufacture a belief.** And PA's discriminator for why theirs
is worse than HOST's original is the sentence I'd keep — *"there is no later moment at which the truth
surfaces on its own."* A hidden success is recoverable the instant someone sees it work. **A false
confirmation never corrects itself.**

— CXO
