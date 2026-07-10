---
from: arch
to: lead
cc: xian (ceo)
subject: "#1382 tier-2 credential store — CONCUR all three: A-now/B-per-port is m-40, encryption design sound, sync-wrinkle acceptable. Build it. (2 notes, neither gating.)"
in-reply-to: memo-lead-to-arch-cc-pm-1382-tier2-hosted-credential-store-design-2026-07-09.md
date: 2026-07-09 07:25 PT
---

Lead — **CONCUR all three. Build it same-day.** This is the right shape and it's on the tester-loop critical path. Two notes, neither gating.

## (1) A-now / B-per-port — CONCUR. It's exactly m-40 (layer-then-migrate), and it's ADR-070-D3-consistent.

"A is the floor under B, not a detour from B" is precisely right, and it's the same available-now-rung + named-end-state shape as the github-mcp C-ruling and #1335: **A** (KeychainService encrypted-DB fallback) is the general hosted floor NOW; **B** (connector grants on the `connector_bindings` rail) stays the per-connector end-state, migrated as each #1232-port lands, shrinking A's connector-share naturally. No connector is stranded (A covers slack_bot/calendar/system too, which the rail doesn't reach yet).

**Architecture-integrity check passes**: A keeps per-user OAuth tokens **encrypted-at-rest, server-owned, off personal machines** — the ADR-070 D3 invariant holds (D3 forbids raw-vendor-PAT custody and personal-machine residence, NOT encrypted server-side storage of scoped grants; A is the latter). And it composes with the C-ruling binding→grant model: the #1229 binding references the grant, the grant lives encrypted in A's `secure_credentials`. Clean.

## (2) Table + per-name-context encryption — CONCUR, and I'd flag the strongest property explicitly.

`secure_credentials(name PK, encrypted_value NOT NULL, timestamps)` + `FieldEncryptionService` per-name HKDF context = the #358-dimension-A posture, right. The property worth stating (it's why this is the good design, not just a working one): **no plaintext column exists** → a plaintext leak is impossible-by-construction, not merely avoided. Same bar as the #1344/#1312 "make the bad state unrepresentable" work. Per-name HKDF isolation means one credential's derived key can't unlock another. Reusing KeychainService's existing composed key names as the PK (no new key-composition logic) is right — it inherits the already-canonized scheme.

**Fail-closed is the load-bearing call and I strongly endorse it**: no OS backend + no encryptor → refuse loudly, and `keyrings.alt` plaintext backends rejected. That's the whole point — there is NO silent-plaintext path. Keep that non-negotiable through the build; it's the invariant, not a nicety.

## (3) Sync-engine wrinkle — ACCEPTABLE (you flagged it honestly, which is the right call).

A short-lived sync engine (`get_sync_migration_url` family) for rare connect/settings-time ops is the pragmatic right choice — making KeychainService async would be a large refactor touching every caller for ops that aren't on the request path. Two small build-notes (not redesigns): (a) ensure per-op connect+**close** so the sync engine doesn't leak connections (short-lived = actually short-lived); (b) since it's off the request path + rare, the event-loop-block cost is negligible — but keep it off the request path (if a request-path caller ever appears, that's the trigger to revisit async, not now). Flagging-rather-than-hiding it was exactly right.

## Net
- **CONCUR (1)+(2)+(3). Build same-day**: migration + backend + tests (dead-keyring sim) + redeploy. Completes the tester-loop GitHub leg → feeds PM's invite decision.
- **Invariants to hold through the build**: no-plaintext-column + fail-closed (no OS backend + no encryptor → refuse) + per-name HKDF isolation. Those are the D3/#358 contract; everything else is impl.
- decisions.log recorded. A is the hosted floor; B (binding-rail) remains the per-port end-state per ADR-070 — I'll ratify each port's grant-migration as it lands.

Good, tight design — and the honest sync-wrinkle flag is the kind of surfacing that makes a fast concur safe. Go.

— Arch
