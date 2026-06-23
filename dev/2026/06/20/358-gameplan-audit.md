# Audit: #358 gameplan vs gameplan-template.md (v9.6) — cascade gate 2

**Date**: 2026-06-20 · **Auditor**: Lead Dev

| Template Requirement | Status | Notes / Action |
|---|---|---|
| Phase -1 Infra | ✅ | Verified table; `cryptography` lib + `user_api_keys` confirmed. |
| Phase 0 GitHub investigation | ✅ | Gate-1 reconciliation (stale-Fernet, dropped api_keys task, A/B scope). |
| Phase 0.5 FE-BE Contract | ⏸️ | N/A — backend-only this run (the "configure your key" UX rides #1300/#1185 separately). |
| Phase 0.6 Data Flow | ⚠️→fixed | #358 is multi-layer (UserAPIKeyService → FieldEncryptionService → DB). **Added** a data-flow note (master-key→subkey; store/retrieve path; keychain-fallback branch). |
| Phase 0.7 Conversation Design | ⏸️ | N/A. |
| Phase 0.8 Post-Completion | ⚠️→fixed | Phase 2 changes storage state. **Added** the side-effect note (encrypted_secret populated; retrieve prefers it; additive/reversible). |
| Phases + TDD | ✅ | Phase 1–2, each TDD-first. |
| Wiring tests | ✅ | Phase 2 wiring (retrieve → #1185 resolver). |
| Phase Z | ⚠️→fixed | **Added** Phase Z (ADR-043 encrypt-at-rest; key-management doc; #358 status floor-done/bulk-deferred; PM closes). |
| STOP conditions | ✅ | Security-specific (don't hand-roll; no key in logs; no plaintext loss; no silent weak key). |
| Effort / subagent | ✅ | Medium; solo (shared files → no fan-out). |
| Security coverage | ✅ | Authenticated encryption + per-field subkeys + no-leak + STOP — the core of a SEC issue. |

## Verdict
Gameplan sound + security-careful. Added 0.6 / 0.8 / Phase-Z. Gate 3 (prompts) N/A — solo. The **A/B scope split** (do the secret-store floor now; defer the content/PII compliance bulk, same primitive) is the thing to surface to PM. **Proceed to Phase 1** (FieldEncryptionService, TDD).
