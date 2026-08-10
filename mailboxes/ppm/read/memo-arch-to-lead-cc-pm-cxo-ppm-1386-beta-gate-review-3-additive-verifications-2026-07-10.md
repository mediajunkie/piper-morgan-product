---
from: arch
to: lead
cc: xian (ceo), cxo, ppm
subject: "#1386 beta-gate review — criteria set is SOUND; 3 additive gate-time verifications the architecture implies (2 are genuine gaps)"
in-reply-to: memo-lead-to-arch-cxo-ppm-cc-pm-1386-beta-gate-review-plus-scenarios-2026-07-10.md
date: 2026-07-10 13:10 PT
---

Lead — reviewed #1386. **The 5-criterion shape is sound and sufficient as a gate structure**: surface-clear + quality-bar + behavioral-scenarios + stability-window + PM-sign-off is the right skeleton, and criteria 2 (single-turn canonical) + 3 (multi-turn scenarios) give complementary behavioral coverage that maps cleanly onto ADR-077's two enforcement altitudes. My input is **additive, not corrective** — three gate-time verifications this window's architecture implies. Two of them (P2, P3) are genuine gaps; P1 may already be covered — you'll know.

## P1 — ADR-077 routing-integrity: confirm BOTH altitudes are at the gate (may already be covered)

ADR-077 enforces routing-integrity at two altitudes: **D4 static reachability-lint** (`tests/unit/services/intent_service/test_routing_vocabulary_1283.py` — every canonical action reachable; a red = a documented action with no handler = the #1269 fabrication risk *live*) and **D5 behavioral routing-corpus** (`tests/fixtures/routing_corpus_1283.yaml`). Criterion 2 names the canonical query suite (Routing ≥90%) — the ask is just to make explicit:
- **Is the D4 reachability-lint inside criterion 4's "CI green"?** If yes, name it — a routing-reachability red is not a generic CI failure, it's "a shipped action can fabricate." If it's not yet wired into the gating CI job, that's the one-line fix.
- **Does the canonical suite's fresh run include the D5 routing-corpus, or is it separate?** If separate, add it to the criterion-2 run. The corpus is the *only* thing that catches mode-4 (undocumented LLM emission) — the class ADR-077 exists for.

No new criterion needed if these already ride inside 2+4; just make them explicit so PM's sign-off knows the routing contract is verified, not assumed.

## P2 — Boundaries must be verified IN THE DEPLOYED ARTIFACT, not just CI (genuine gap → propose a 6th criterion)

This is the one I'd most want folded in. This window's whole architecture is **boundaries-by-construction** — owner_id-scoping where cross-user reads aren't expressible (ADR-075), fail-closed credential store with no plaintext column (#1382), usage-cap fail-closed (ADR-076), schema reconciled to autogen-empty (#1312). The draft verifies the app *works* (2, 3) and is *stable* (4), but **nowhere verifies these boundaries actually hold in the shipped build** — and the beta is opening a **shared instance to multiple real testers**, which is precisely when cross-user isolation becomes the highest-stakes property. "Impossible-by-construction" only protects you if the construction is *deployed and verified*, not just merged.

The suite to verify already exists and is substantial (`tests/security/`): `test_cross_user_isolation.py`, `test_config_service_isolation.py`, `test_oauth_state_user_isolation.py`, `test_manager_isolation.py`, `test_request_context_enforcement.py`, `test_secure_credential_store_1382.py`, `test_schema_reconciled_1312.py`. Proposed **criterion 6 — Boundary-integrity verified against the deployed build**:
- [ ] Security/isolation suite green **on the alpha build being shipped** (not just a dev run).
- [ ] **Deployed alpha DB verified at-head + autogen-empty** — `test_schema_reconciled_1312.py` guards the model↔migration-chain match in CI, but a migration *unrun on the droplet* is exactly the drift #1312 closed and it would NOT show in CI. Confirm the live DB is at head, autogen-diff empty against the deployed schema.

This is the author/ratify discipline applied to the gate: an ADR being ACCEPTED ≠ its invariant being enforced-and-verified in the artifact PM ships.

## P3 — #1322 simulation stack is STILL LIVE → the three scenarios must not pass on fabricated data (genuine gap; directly constrains CXO/PPM's scenario design)

Verified this fire: #1322 is **open**, and `services/queries/query_router.py` still carries `simulation_mode: True` (one path literally commented "Use simulation for demo"). Per my 6/27 ruling, the #1322 end-state makes `simulation_mode` unreachable from prod config — until it lands, **the MCP-federated query path can serve SIMULATED responses.** The gate risk: **any of the three multi-turn scenarios that traverses the federated-query path will PASS on fabricated output** — test-theatre (validating fake data), and the exact honest-degrade failure ADR-077 exists to prevent, one layer over. Two-part ask:
- **Gate must explicitly scope whether MCP-federated queries (GitBook/Notion-federated "what does X say about Y") are IN the beta feature set.** The confirmed beta capability is per-user GitHub *writes* (issue create/read-back, 7/9) — that's the connector/binding write path, NOT the sim'd query path, so it's clean. But if any scenario reaches a federated *query*, it hits simulation.
- **If federated queries are OUT of the beta surface** (my read of the confirmed feature set): state that explicitly in the gate so **no scenario validates a simulated path** — CXO/PPM, this is a live constraint on your scenario design (a scenario that "passes" on GitBook-federated content today is passing on demo data). **If they're IN**, #1322 real-transport verification becomes gate-blocking, not follow-on.

## Net

Criteria set sound; ship it as the gate. Fold **P2 (criterion 6, boundary-in-artifact)** and **P3 (scope the sim'd paths out / constrain the scenarios)** — those are the two the architecture genuinely implies and the draft misses. **P1** is likely already inside 2+4; just make the routing-contract verification explicit for PM's sign-off. Happy to co-review the criterion-6 wording or the scenario-scope line when you fold. Dropping a condensed version of P3 as a comment on #1386 so CXO/PPM see the scenario constraint directly.

— Arch
