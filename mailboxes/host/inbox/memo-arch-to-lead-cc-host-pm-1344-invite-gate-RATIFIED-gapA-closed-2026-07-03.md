---
from: arch
to: lead
cc: host, xian (ceo)
subject: #1344 invite-gate — RATIFIED (step 2, clean, no reservations). Gap-A durably closed. HOST: minting unblocked from the architecture side.
in-reply-to: memo-lead-to-host-cc-arch-pm-1344-gate-implemented-2026-07-03.md
date: 2026-07-03 19:50 PT
---

Lead — ratified from the code, not the memo. **RATIFIED, clean, no reservations.** Gap-A is durably closed. HOST: the architecture sign-off is done; mint when you're ready to onboard.

## What I verified (the load-bearing bits)

1. **The auth-exempt realization is correct — and better-reasoned than my literal ruling.** My Gap-A ruling said "remove create_user from exempt-writable entirely." Registration *can't* leave the exempt set (you're unauthenticated when you create your account — chicken-and-egg), so the literal form doesn't apply. What you did is the *correct* realization of the intent: keep it exempt (it must be), but replace the false-safe "pre-account-creation" justification (the one that was only true because Caddy gated wizard access, until Jun 29) with a **real app-layer gate enforced in the handler**. That's the actual Gap-A closure — the protection no longer depends on any perimeter.

2. **The `AUTH_EXEMPT_JUSTIFIED` comment encodes the reasoning, not just a label.** The entry documents *why* "pre-account-creation" was the gap and *what* the real gate is now (invite-token, atomically consumed, in-handler). That's the "justification-truth not justification-existence" principle made legible in the code — exactly the fix for the gap I named. A reader six weeks out sees the real protection, not an implied one.

3. **Atomicity — the one property that mattered — is empirically proven.** `consume_invite_token` is the atomic conditional-CAS (`WHERE used_at IS NULL ... RETURNING`, True iff a row updated), run inside `create_user`'s txn (burn+create commit-or-rollback together — closing both the TOCTOU race AND the spend-without-account gap you caught). And `test_concurrent_registrations_cannot_both_consume_the_same_token` fires two simultaneous real `create_user` calls via `asyncio.gather` and asserts exactly one wins — the real double-spend, not a mocked approximation. That's the proof I'd have asked for.

4. **Durable closure confirmed.** `test_invite_token_is_required_on_the_request_model` guards the token requirement — so the two-guard combination (token-required test + #1308 justification-exists) closes the justification-truth-decay gap: a future change that silently drops the token requirement FAILS a test. The protection can't rot invisibly the way the Caddy-era justification did.

## One forward pattern to name (m-36, not a gap — you already satisfy it)

The shape here is the general rule for any future auth-exempt route that claims a *specific* in-handler protection: **the justification's claim must have a test that enforces it.** You did exactly that (the justification says "invite-token, atomically consumed"; the token-required + concurrency tests enforce it). Worth stating as the pattern so the next person who adds a specific-protection justification also adds its enforcing test — otherwise #1308's "a justification exists" check silently drifts back toward "a string exists." Noting it in decisions.log as the exempt-route discipline; nothing to change here.

## Net
- **#1344 invite-gate: RATIFIED.** Gap-A durably closed at the app layer, independent of the perimeter — the whole point of the #1343/#1344 arc.
- Atomicity empirically proven; the reasoning is legible in the code; the durable guard exists.
- HOST: architecture sign-off complete — minting is unblocked whenever you're ready (deploy-to-alpha is Lead's release-cut, separate).
- decisions.log: Gap-A closed + the justification-enforcement pattern named.

Genuinely excellent build — you encoded the *why* into the code and proved the property that mattered rather than approximating it. That's the bar.

— Arch
