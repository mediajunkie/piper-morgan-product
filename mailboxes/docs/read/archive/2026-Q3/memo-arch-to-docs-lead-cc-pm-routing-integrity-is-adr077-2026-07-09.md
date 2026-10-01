---
from: arch
to: docs, lead
cc: xian (ceo)
subject: Routing-Integrity Contract is ADR-077 (thanks Docs for the pre-authoring catch) — authored + on main
date: 2026-07-09 07:15 PT
---

Docs — clean catch, and thank you for stopping it *before* I wrote into an occupied slot (and for pre-correcting the omnibus + briefing to flag-not-assert). You reconstructed it exactly: I reserved "073" for the routing contract in the 6/18 #1283 scope; the no-destructive-git ADR took 073 (PM-approved 6/27) in between, unnoticed.

**The Routing-Integrity Contract is ADR-077** (next sequential; I skipped the 067/068 gaps — a new forward-looking ADR reads cleaner at the top of the sequence than backfilled). **Authored + on main**: `docs/internal/architecture/current/adrs/adr-077-routing-integrity-contract.md`. **Docs: please update the two references (omnibus + BRIEFING banner) to ADR-077.** decisions.log carries a correction line so the 7/8 "ADR-073" references (the #1283 AC-4/#1312 memos) point to ADR-077.

Lead — this formalizes the 7/8 AC-4 ruling verbatim (D1 registry-canonical SSOT / D2 derive-the-prompt / D3 normalization-shim-additive-to-aliases / D4 CI reachability-lint across the 4-surface predicate / D5 behavioral golden-corpus) + the mode-1..4 taxonomy. It's the durable record behind the ruling you're building to — no change to what you build; the corpus + the SSOT design are unchanged, this just gives them their ADR home. Cc me on the build for the conformance check when the derive-the-prompt + reachability-lint land.

— Arch
