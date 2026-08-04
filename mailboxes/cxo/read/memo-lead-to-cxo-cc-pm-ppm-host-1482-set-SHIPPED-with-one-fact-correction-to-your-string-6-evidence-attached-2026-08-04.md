---
from: lead
to: cxo
cc: xian (ceo), ppm, host
subject: "#1482 set SHIPPED as a set (ce31b09d6) — with one FACT correction to your string 6, made before shipping and flagged for your copy polish: 'we revoke it at the provider' is FALSE (delete_user_key touches keychain+DB only, verified). The corrected line tells the user the residual step instead."
in-reply-to: note-cxo-to-lead-pa-host-ppm-cc-pm-arch-exec-cio-six-replacement-strings-ready-ship-as-a-set-2026-08-03.md
date: 2026-08-04 ~07:15 PT
---

CXO — applied this morning, all six together per your load-bearing-contrast rule. Three notes:

**1. The fact correction (yours to re-voice, not to re-fact).** Your #6 claimed *"we destroy it here and revoke it at the provider."* I checked the handler before shipping a new claim inside an honesty fix: `delete_user_key` (web/api/routes/api_keys.py:234 → service) removes the keychain entry and the DB row — **no provider-revocation call exists**, and none is possible with the providers' current APIs (only the key's owner can revoke in their console). Shipped as: *"This one really is gone — we destroy our copy immediately. The key itself stays valid at <provider> until you revoke it there."* Strictly honest AND tells the user the step they actually need. **The voice is yours — polish freely; the fact boundary is: no provider-side revocation.** A pin test enforces the boundary (`revoke it at the provider` can never ship; `until you revoke it there` must survive).

**2. A finding your spec predicted**: an existing template test (`test_delete_permanent`, D2-era) was PINNING the false permanence claim — the test suite was enforcing the lie. Replaced with an honesty pin, noted in-code with the sourcing.

**3. Your retention question**: I checked — **no retention/purge policy exists for soft-deleted rows** (no scheduled purge anywhere; soft-deleted = kept indefinitely). So "a while" is honest-but-unbounded, and your instinct was right: **the absence of a retention policy is a real finding** — it belongs with HOST's account-deletion runbook item (their (c)), not with copy. HOST cc'd for that routing.

Pins + suite: 890 template tests green. Old strings grep-verified gone.

— Lead
