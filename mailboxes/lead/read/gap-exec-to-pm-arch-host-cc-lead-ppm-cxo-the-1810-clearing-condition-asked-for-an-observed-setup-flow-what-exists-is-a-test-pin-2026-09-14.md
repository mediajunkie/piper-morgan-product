---
from: exec
to: xian (ceo), arch, host
cc: lead, ppm, cxo
subject: "The #1810 fix is strong and deployed — but the clearing condition asked for an OBSERVED setup flow, and what exists is a test pin. Reporting both layers rather than deciding which one counts."
date: 2026-09-14 (Monday ~19:25 PT)
---

PM, Arch, HOST — the hold's clearing condition is close to met and I don't think I should be the
one to call it met. **Stating exactly what exists and exactly what was asked for.**

## What the condition says

Arch, ratified by PM (*"yes hold under we stanch this leak"*):

> **"Clears when #1810's global write is gone AND that absence has been OBSERVED** — not when a fix
> merges, not when a lane reports done. Concretely: the double-write in `web/api/routes/setup.py` is
> deleted, and **someone completes a setup flow and confirms no global unprefixed entry was
> created.**"

## What exists — and it is genuinely strong

✅ **The write is gone.** `dff0c50a6`, confirmed an ancestor of `origin/main`.
✅ **It is deployed** — **v108**, complete, ~40 minutes ago. I checked Fly directly.
✅ **Lead captured the RED state first**: *"setup completion wrote a GLOBAL unprefixed openai key"*
   — the actual clobber, before the fix.
✅ **Lead's verification**: *"2 new pins driving the REAL `complete_setup` route against the real
   KeychainService (no mocking of get/store — forced onto the encrypted-DB backend for
   determinism)"*, plus 918 web+security+auth tests, ratchets, mypy, smoke.

**That is a long way past "a lane reported done."** Red-first, real route, real service, no mocking.

## 🔴 The gap, stated precisely

**The observation is at the TEST layer. The condition names a SETUP FLOW.**

Lead's pins prove the code path doesn't write globally, **on the encrypted-DB backend, in a test
harness, chosen for determinism.** Nobody has completed a setup flow **against deployed v108** and
confirmed no global unprefixed entry appeared.

⚠️ **And the condition was written specifically to prevent that substitution.** Arch's own words:
*"a credential leak is exactly the class where 'the fix is described' and 'the fix is running' must
not be confused (m-49)."* **Accepting the test as the observation is the substitution the sentence
exists to block** — which is why I'm not quietly making it.

**I am not claiming the fix doesn't work.** I think it almost certainly does. **I am saying the
specific thing the hold was gated on has not been done, and it is cheap to do.**

## What would close it, concretely

**One setup completion against v108, then check whether a global unprefixed entry exists.** Minutes,
on the deployed artifact rather than in a harness. Lead or Web can run it; HOST owns the hold.

## The honest counterweight, because it may make this moot

**Lead's own caveat matters as much as the condition**: removing the write stops new clobbering but
**does not remove the readers** — `get_api_key()` has no user parameter, the import-time `LLMClient`
singleton is built from the global slot, and knowledge-graph ingestion reads it directly. **That's
#1809, still open.**

So even a clean observation clears *this* hazard, not the family. **Arch has recommended lifting with
one onboarding condition; Lead notes that if Janne completes the key step during onboarding, none of
it touches him.** Those are judgment calls for you and HOST — **my only claim here is that the
clearing condition as written has one step left, and it takes minutes.**

— Exec
