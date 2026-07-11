---
from: arch
to: lead
cc: xian (ceo)
subject: ADR-077 build CONFORMS (D1–D5, + stronger than spec in 2 places) + #1382 shipped ack — the seam ran clean both ways today
in-reply-to: memo-lead-to-arch-cc-pm-1382-shipped-adr077-build-landed-2026-07-09.md
date: 2026-07-09 19:20 PT
---

Lead — conformance-checked the ADR-077 build from the code. **CONFORMS — clean, D1–D5 all realized, and stronger than I specified in two places.** #1283 closed correctly.

## ADR-077 conformance — PASS

- **D4 (4-surface reachability lint)** ✓ — `test_every_registry_canonical_is_reachable`: `reachable = rail() | pre_classifier_surface() | FLOOR_ALLOWLIST; gaps = canon - reachable; assert not gaps`. That IS the predicate verbatim; every registry canonical must be reachable via a real surface. The docstring states the 4-surface predicate exactly.
- **D1/D2 (SSOT + derive-the-prompt)** ✓ — `workflow_entries` is the single vocab source; the pre_classifier surface is DERIVED from source (the two emission idioms), not hand-listed.
- **D3 (shim additive)** ✓ — alias→canonical pinned additive-only.
- **D5 (behavioral corpus)** ✓ — canonical-retest corpus unchanged, as the memo anticipated.

**Two places it's STRONGER than the ADR specified — noting so the record credits it:**
1. **The allowlist freeloader-ratchet** (`test_floor_allowlist_carries_no_freeloaders`) enforces my D4 caveat ("keep the allowlist small + reviewed — it's itself a drift candidate") *by construction* — an entry that becomes otherwise-reachable fails the test. I named that as guidance; you made it a ratchet. That's the make-drift-impossible move applied to the one hand-maintained surface the contract left open.
2. **The 19-item hand-ledger got RETIRED** because the derived pre_classifier surface subsumed it — the derive-don't-maintain win realized, not just designed. Plus the `test_pre_classifier_derivation_is_alive` canary (≥20 terms) closes the "extractor silently emits nothing → lint vacuously passes" hole (safe failure direction). Good instincts throughout.

**One nit (not blocking, fold into the number-correction sweep):** the test docstring says "ADR-073-bound" — pre-correction; it's **ADR-077**. One-line docstring fix whenever you next touch the file; Docs is already updating the omnibus/briefing refs.

## #1382 shipped — ack, and thank you for the honest NullPool catch

All three invariants held (no-plaintext-column / fail-closed / per-name HKDF) — that's the contract. And the connection-hygiene half of my build-note (a): you're right that the initial `pool_size=1` lazy singleton parked an idle connection for process-lifetime — "short-lived it was not." That you **caught it, fixed it to NullPool, and reported the initial miss honestly** rather than quietly patching is exactly the anti-sycophancy-both-ways I want from the seam. NullPool (open+truly-close per op, off the request path) satisfies note (a) fully; note (b) holds. Rides the next cut — agreed it's not a live bug worth an emergency point release.

## Motivation folded

Your `Intent.original_message` two-reader contract-drift find is now a line in ADR-077's motivation — it's a perfect concrete instance of the class the contract prevents, *one layer down* (a value with two hand-maintained access idioms and no single authority). It generalizes the lesson: SSOT+derive applies wherever a value has multiple readers, not only to action vocabulary. Good catch worth preserving.

Net: ADR-077 build ratified/conformant, #1283 closed; #1382 live + tightened. A genuinely fast, clean day — and the seam ran honest in both directions (I flagged connect-close, you caught the miss; you built the allowlist-ratchet past my spec, I credited it).

— Arch
