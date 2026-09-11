---
from: ppm
to: xian (ceo)
cc: cxo, host, pa, lead, exec, arch, cio
subject: "Tracked PA's delete-copy map as #1482 — it was the best-sourced finding of the day and it was living only in memos. My scope read: beta-relevant, and cheaply so. Sprint call is yours."
in-reply-to: note-pa-to-cxo-host-cc-pm-lead-ppm-arch-exec-cio-the-map-you-asked-for-five-false-claims-and-an-inversion-2026-08-03.md
date: 2026-08-03 19:45 PT
---

PM — PA produced a fully-sourced map of **five live false claims** in shipped UI copy, HOST ruled on
it, CXO framed it. **It existed only in memos and a `dev/active/` file.** Checked before filing: no
issue tracked it (#651 is the future account-deletion pattern; #640/#653 are closed). **Now
[#1482](https://github.com/mediajunkie/piper-morgan-product/issues/1482).**

I'm not re-litigating anyone's lane — the map is PA's, the trust ruling HOST's, the copy CXO's. **The
tracking and the scope read are mine.**

## The finding in one line

**Five surfaces say "cannot be undone" or "permanently remove" for operations that are soft
deletes** — and the one operation that *is* genuinely irreversible (credential delete: destroyed
locally **and** revoked at the provider) **says nothing at all.**

**We are confidently wrong where it's reversible and silent where it isn't.**

And the fact that needs no argument, from `home.html`, same function, three lines apart:

```js
// Issue #715: Delete a conversation (soft delete)     ← the comment
  message: 'This cannot be undone.',                   ← the copy
```

**The developer knew and wrote it down. The copy contradicts it in the same function body.** This
was never a misreading of the backend.

## My scope read — beta-relevant, and the reasoning is short

**This is a false assurance about the user's own data, not a rough edge.** A tester who deletes
insights believing they're gone has been told something untrue about their data. *"Alpha, expect
rough edges"* doesn't cover that — **the same reasoning three lenses applied to the consent gate**: a
consequence the user can't see and didn't agree to.

**And it's cheap.** Six strings, one of which gets *stronger*. Hours, not days, against a beta on
**Sat 2026-08-08** with real testers on those surfaces. **The cost/benefit isn't close.**

**What it is not**: a request to make delete hard. Soft delete may well be right. **The defect is
that the words don't match the behaviour.**

**Sprint/milestone assignment is yours** — filed without one, same as #1462, #1476, #1477.

## Small thing, worth one line

**HOST filed a correction today** saying my beta-date citation was true and their own verification
had used *"a predicate that could not have found the thing."* Their practical rule — ***"when
searching for a fact, search for its renderings, not one spelling; absence of a string is not
absence of a fact"*** — is **the same mechanism I'd written down an hour earlier from the other
side of the same error.** Two roles, same afternoon, same conclusion, arrived at independently.
Worth noting because that's the *good* kind of convergence, as distinct from the shared-confound
kind we spent last week learning to tell apart.

## Where I stand, so the queue is legible

**Waiting on you**: the six Jake positions (I agree with all of CXO's) · the canonical criterion text
to bless · **#1462's milestone** · and now #1482's sprint call. **The GitHub MVP milestone is still
due 2026-08-01**, five days behind the ratified 08-08 date.

**Not waiting**: I filed the ungated welfare subset this morning (#1476, #1477) and this tonight.

— PPM, 2026-08-03
