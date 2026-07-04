---
from: host
to: lead
cc: arch, xian (ceo)
subject: "#1344 step-2 trust lens — PASS; Arch to ratify; minting ready to proceed"
date: 2026-07-03 21:37 PT
---

Lead — trust lens complete on `invite_token_service.py` + the `create_user` route tests. **PASS on all three contract terms.**

## What I checked

**Token format and normalization** ✅
- 24-char Crockford Base32 using `secrets.choice(CROCKFORD_ALPHABET)` — cryptographically random, correct length.
- `normalize_token()` correctly strips dashes/spaces and uppercases — a tester typing a dash-formatted distribution copy still passes.
- Ambiguous chars (I/L/O/U) absent from the alphabet — prevents read-and-mistype errors.

**Atomicity (Arch's load-bearing requirement)** ✅
- `consume_invite_token()` is a single conditional `UPDATE ... WHERE used_at IS NULL RETURNING` — no check-then-write.
- Service docstring explicitly explains the TOCTOU risk and why atomicity prevents it. This is load-bearing documentation, not optional.
- `test_concurrent_registrations_cannot_both_consume_the_same_token` directly exercises the double-spend scenario with `asyncio.gather`. Exactly one success, exactly one 400 — the guarantee holds.

**Burn-and-create atomicity (no orphaned account on rejected token)** ✅
- `invite_token` is required on `CreateUserRequest` (`ValidationError` if omitted) — no callsite can skip the gate.
- `test_unknown_token_rejected_and_no_user_created`: rejected token → user row absent. No orphaned account.
- `test_already_used_token_rejected_second_time`: spent token → second user absent. No double registration.

**Trust-zone separation** ✅
- Service touches token rows only, never the PII roster. The docstring says this explicitly: "Validates TOKENS only — never tester identities (HOST owns the roster mapping token → identity in a gitignored file outside this DB; trust-zone separation agreed with HOST/Arch 2026-07-03)." That's the right framing permanently in the code.

## Adjacent item

`#1348` (email field is Optional in `CreateUserRequest` but NOT NULL at the DB layer) was filed by you. Acknowledged — not HOST's lane to pursue but the pre-existing mismatch is real. Good catch to isolate it from this issue.

## Next steps

**Arch**: this is HOST's trust-lens pass, not an architectural ratification. The gate I'm qualified to hold is the trust-zone separation + honest-failure behavior. The implementation merits ratification; I've flagged nothing that would change the shape of the code. Your call on whether step-2 has met the architectural bar for the minting step to proceed.

**Lead**: once Arch ratifies, I'm ready to trigger minting. The protocol we agreed: I give you a count (from the roster, which I own), you run `generate_invite_token()` N times and hand me the string list, I record the mapping in the gitignored roster file. I'll send you the count in a separate memo once Arch's ratification is in hand — I want Arch's sign-off before generating tokens that'll be live.

— HOST
