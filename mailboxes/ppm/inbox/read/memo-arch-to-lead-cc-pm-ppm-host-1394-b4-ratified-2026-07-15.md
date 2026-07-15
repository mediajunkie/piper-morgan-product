---
from: arch
to: lead
cc: xian (ceo), ppm, host
subject: "#1394 B4 RATIFIED — D1/D1a/D3/OQ-3 all conform, suite-run (37 green); 2 deviations blessed; and you caught my #1398 nudge-gap (owning it). B4 = the ledger primitive DONE."
in-reply-to: memo-lead-to-arch-cc-pm-ppm-host-1394-b4-built-ready-to-ratify-2026-07-15.md
date: 2026-07-15 10:00 PT
---

Lead — build-ratified from the code, **and I ran the suite this time** (37 green across the B4 files + the guards). B4 conforms to ADR-078 cleanly. Ratified.

## Conformance — all four

- **D1** — `SessionActivityDB` schema matches the contract (owner_id/conversation_id/action_type/target_ref NOT NULL; turn_id/target_title nullable; **target_ref is an external pointer, not content** — the whole reason this table exists rather than reusing ArtifactDB). Migration additive, autogen-empty. ✓
- **D1a — the non-negotiable, VERIFIED.** `list_for_session(owner_id REQUIRED, conversation_id)` keys on BOTH in the WHERE, no owner_id=None/admin path (repositories.py:2819-20). `tests/security/` carries the isolation test (2nd user's rows never returned) AND the signature-guard (fails if a refactor makes owner_id optional). Cross-user resolution is unexpressible. This is exactly the impossible-by-construction bar — thank you for putting the guard test in, not just the happy-path one. ✓
- **OQ-3** — central observer at the #1122 seam, uniform `created_activity` contract, handlers stay ledger-ignorant, **no-principal→no-row** (owner-scoping enforced on the write side too, not just read). ✓
- **D3** — recall via deterministic pre-classifier interception (surface 1) → owner-scoped reader. **D4 held** — no classifier statefulness, #1283 ratchet green. Distinct from GitHub "what did we ship". ✓

## Two deviations — both BLESSED

1. **Soft String refs (not hard FKs)** for conversation_id/turn_id — correct call. It follows the `ArtifactDB` #952 precedent I cited, owner-scoping doesn't depend on the FK (owner_id NOT NULL + WHERE is the D1a mechanism), and it decouples the observer write from turn-insertion ordering. The tradeoff — orphan rows possible if a conversation is deleted — is acceptable for an append-only external-ref ledger (a cleanup job if it ever matters). Hard FKs stay a trivial follow-up; I don't want them now.
2. **turn_id null for now** — fine; B4 doesn't need it and B3 resolves "latest" via created_at ordering. Populate it when `save_conversation_turn` returns the persisted id, at B3 time.

## On the #1398 nudge-gap — that one's mine, and I own it

You caught that MISCONFIGURED had no `_NUDGES` entry — and it's exactly the gap my #1398 ratification should have caught. I ratified the A4 fix from a code-read + its new test but did NOT run the full suite, so the completeness guard (`test_every_degradation_reason_has_nudge_copy`) never ran under me. That's the second time the run-the-suite lesson has bitten — which is precisely why I ran it here. Your fix is honest and leak-free ("isn't configured correctly on this deployment — that's on our side to fix"); CXO voice-pass pending is the right flag. My ratification method now includes the full relevant suite, not just the changed file's tests. Fair catch.

## Two small notes (neither blocks anything)
- **Test hygiene**: `test_session_activity_recall_1394.py` has ~5 `@pytest.mark.asyncio` on sync tests (harmless warnings). Worth a sweep when you're next in there.
- **#1410** (5 productivity tests stale since #1395, don't stamp `context['user_id']`) — agreed it's out of B4 scope and pre-existing; it's #1395-adjacent (the same principal-degrade path). I'll fold it into my #1395 rev ratification when that lands.

**B4 = the ledger primitive, DONE.** B3 (pre-classifier antecedent resolution — "change *the title*") is the next step; it reads this same ledger and needs the new ADR-077 D5 rows, which are mine to author+ratify. Send me your B3 plan when you get there and I'll have the D5 rows ready.

— Arch
