---
from: PA (Piper Alpha)
to: PPM (Principal Product Manager), Lead Developer
cc: CEO (xian)
date: 2026-06-10
subject: BYO-key converged design + build-sequencing — #1185 multi-tenant rests on #358 (now the "server-stored" rung; revised + in M5). PPM: where does #1185 sit vs M3 blockers? Lead: storage-floor-then-wiring order.
priority: standard — converged design handoff so engineering inherits it (don't re-derive)
response-requested: PPM roadmap-placement call; Lead build-order sanity-check — at your cadence
---

# BYO-key: the design converged with PM (6/10) — handing it to you so you don't re-derive it

PM and I walked the credential architecture to convergence today off the #1185 verify-before-building
investigation. Full report + converged-design capture: `dev/active/pa-1185-multi-tenant-byo-key-investigation-2026-06-10.md`.
This memo is the engineering-facing summary + two asks (one PPM, one Lead).

## The converged model — a 4-rung call-time resolution chain (most-BYO → honest-refuse)

1. **BYO (b) — host-side inference** *(true endgame)*: the user's own Claude/host runs inference; our server
   never sees the key. = the BYO-colleague / skill-broker model (braintrust-converged; you put it at post-beta
   v1.1, PPM). PM confirms this is the real endgame.
2. **BYO (a) — key passed per-request, not stored** *(resilient/optional)*: plugin passes the user's key; used
   in-memory, never persisted. May persist as a fallback even after (b) ships.
3. **Server-stored per-user key (encrypted)** *(the beta rung)* — **this rung IS #358** (see below).
4. **Offer to configure** *(honest bottom — NEVER a shared instance key; that's what caused the alpha usage
   wall)*. Branches: (i) configure natively → rung 3, or (ii) help the user set up their own BYO harness →
   rung 1/2.

Cross-cutting: the store *can* hold the **whole user-secret set** (LLM key + ADR-058 integration keys), but
**acquisition is need-scoped / just-in-time** (trust gradient — ask only when a request needs it, never
blanket up-front). **Legibility** (whose key/secret was used for what — resource-consent + `actor_chain`) is
required at every rung.

## The load-bearing dependency: #358 IS the server-stored rung (by construction)

The hosted instance is a **Linux droplet — no macOS Keychain**, which is where per-user secrets live today
(`user_api_keys` → `KeychainService` by user_id). So **there is no server-stored secret store on the hosted
instance until encryption-at-rest in Postgres (#358) exists.** #358 isn't compliance-polish-on-top — it's the
enabling floor for rung 3.

- **I've revised #358** (2026-06-10): corrected stale Nov-2025 claims (it asserted api-key Fernet encryption in
  `services/security/encryption.py` — that file doesn't exist; no `api_keys` table / `key_value` column either)
  and added the user-secret-store dimension + the #1185 connection. **Confirmed in M5 per PM** (may slide to a
  post-beta release-ready sprint; PM leaning M5).
- **Consequence for sequencing**: if #358 lands in M5 → the hosted beta has the server-stored fallback rung. If
  #358 slides post-beta → the beta is BYO-only or stays on the shared-key alpha until it lands. Either is fine;
  **the one thing to avoid is shipping real-user server-stored keys before #358** (= storing Anthropic keys
  unencrypted).

## What #1185 itself has to build (on top of #358's storage floor)

The storage *retrieval* layer already exists (`UserAPIKeyService.retrieve_user_key(user_id, provider)`; schema
covers `anthropic`). The wiring gaps:
- **Gap A** — `LLMClient._init_clients()` builds `self.anthropic_client` **once at init** with the *instance*
  key. Multi-tenant needs: thread `user_id` from `/intent` down to the LLM layer (no user context there today)
  + per-request resolution via `retrieve_user_key` + instance fallback + a client-lifecycle change (per-request
  construct or user-keyed cache). This is the bulk of #1185.
- **Gap C** — hosted edge is one shared Caddy basic-auth gate; needs per-user `current_user` (app machinery
  exists via CORE-USERS-API #228; it's a deployment + auth-surface decision).

**Build order**: #358 (storage floor: encrypted per-user-secret store, droplet-portable) → #1185 Gap A
(resolution wiring) → #1185 Gap C (per-user hosted auth). Non-wasteful property worth noting: **server-stored
for beta builds the fallback rung of the endgame** — the BYO rungs add on top later; nothing thrown away.

## Two asks

- **PPM (roadmap placement)**: where does **#1185** sit vs the M3 blocker work (floor #1124 / persistence
  #976,#436 / interface-DoD)? #1185 is the *hosted-beta-key* thread (driven by the alpha usage-wall evidence),
  **distinct from colleague-mode** (which you placed at v1.1) — so its timing is a separate call. #358 is M5;
  does #1185's wiring ride M5 alongside it, or land earlier as hosted-beta-enabling?
- **Lead (build-order sanity-check)**: does the #358-floor-then-#1185-wiring order hold from an implementation
  view? Any reason the client-lifecycle change (Gap A) should precede or parallel the storage work? Flagging
  the `AES-256-GCM FieldEncryptionService` #358 already proposes as the right primitive for the user-secret
  store too (one encryption service, both content fields + credentials).

No rush on either — this is to put the converged design in front of you so it doesn't get re-derived. Happy to
pair on the #1185 build-sequencing detail when the lane opens.

— PA, 2026-06-10
