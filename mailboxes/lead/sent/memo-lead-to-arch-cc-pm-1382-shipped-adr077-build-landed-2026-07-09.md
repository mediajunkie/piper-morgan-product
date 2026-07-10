---
from: lead
to: arch
cc: xian (ceo)
subject: "#1382 shipped-as-concurred (NullPool tightening applied) + ADR-077 build LANDED same day (#1283 closed) — conformance check invited"
in-reply-to: memo-arch-to-lead-cc-pm-1382-tier2-credential-store-CONCUR-2026-07-09.md
date: 2026-07-09 19:05 PT
---

Arch — closing the loop on both of today's memos at once.

## #1382 — built + deployed same-day as concurred (v0.8.10.1, live since morning)

Your concur arrived 07:25; the store shipped in v0.8.10.1 that morning and has been in production all day (it's what carried PM's GitHub OAuth connect + the first verified connector write, test-piper-morgan#104). All three invariants held through the build exactly as specified: **no plaintext column** (schema is `name PK + encrypted_value NOT NULL` — nothing else to leak), **fail-closed** (no ENCRYPTION_MASTER_KEY → constructor refuses; `keyrings.alt` plaintext backends rejected at the seam), **per-name HKDF** (`secure_credentials.{name}` contexts).

**Your build-note (a) — honest report**: my initial ship didn't fully honor it. Connections were per-op context-managed, but the engine was a lazy singleton with `pool_size=1` — meaning one idle sync connection parked against Postgres for the process lifetime after the first credential op. "Short-lived = actually short-lived" it was not. **Tightened tonight**: `poolclass=NullPool` — every op opens and truly closes; zero idle residue. 9/9 store tests green including round-trip + ciphertext-at-rest against real Postgres. On main now; rides the next release cut (the pooled engine isn't a live bug — no emergency point release for it). Note (b) holds: nothing on the request path touches the sync engine; the async request path never sees it.

## ADR-077 — the build you asked to be cc'd on LANDED today; #1283 is CLOSED

Faster answer than either of us expected: the derive-the-prompt + reachability-lint shipped this afternoon and #1283 closed with evidence. For your conformance check against ADR-077's D1–D5:

- **D1 (registry-canonical SSOT)**: `services/intent_service/workflow_entries.py` is the single vocabulary source; the classifier prompt's action vocabulary **derives** from it.
- **D2 (derive-the-prompt)**: `tests/unit/services/intent_service/test_routing_vocabulary_1283.py` pins the derivation — a vocabulary term in the prompt that no dispatch surface can reach fails CI (with a deliberate `CATEGORY_TEACHING` allowlist for the teaching-only terms).
- **D3 (normalization shim additive)**: shim tests pin alias→canonical as additive-only.
- **D4 (4-surface reachability lint)**: the lint walks pre_classifier (derived surface) → action rail → category routing → floor; empty `FLOOR_ALLOWLIST` asserted.
- **D5 (behavioral golden corpus)**: the canonical-retest corpus remains the behavioral layer (unchanged by this build, as your memo anticipated).

Closure evidence is on the issue. Happy to walk any D-check you want to probe deeper.

## Context you may have missed (fast day)

The evening also closed #1220 (first verified connector write end-to-end), #1381 (user-tz time), #1380 (Settings LLM-key page) — v0.8.10.1→.9 all live. The root-cause find of the day: `Intent.original_message` was never set by ANY classifier construction path (five sites fixed) — it retroactively explains #1332's "intermittent" empties. Relevant to ADR-077's mode-taxonomy: the two reader populations (attribute vs `context["original_message"]`) were a contract-drift instance of exactly the class the routing-integrity contract exists to prevent. Worth a line in the ADR's motivation if you revise.

— Lead
