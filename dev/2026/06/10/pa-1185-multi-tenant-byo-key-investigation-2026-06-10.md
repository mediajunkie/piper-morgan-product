# #1185 Multi-tenant BYO-key — initial investigation + written report (2026-06-10)

**For**: PM (xian). **Type**: verify-before-building scoping (the issue's own "Open Qs (verify before
building)" gate). **Scope note**: PM asked to keep an open mind about *where in the stack the various API keys
can or should be connectable* — so this maps the whole credential stack, not just the one wiring change.

---

## TL;DR

- **The per-user-key STORAGE layer already exists and is more complete than the issue assumed** — full CRUD,
  auth-scoped by `user_id`, and the schema already covers an **Anthropic LLM key** (not just integrations).
  There's even a clean `retrieve_user_key(user_id, "anthropic")` entry point ready to call.
- **But the secret is stored in the macOS Keychain** (`KeychainService`), keyed by `user_id`. That's fine on a
  laptop; **it does not exist on the hosted Linux droplet.** This — not the LLM wiring — is the load-bearing
  architectural decision for hosted multi-tenant, and it's exactly the "where in the stack" question.
- **Two real build gaps** (smaller than the storage gap, but real): (1) the LLM client is built **once at init**
  with the instance key, so multi-tenant needs a client-lifecycle change + threading `user_id` down to the LLM
  layer (which today has no user context); (2) the hosted instance runs behind one **shared basic-auth gate**,
  so per-user identity needs wiring (the app's `current_user` machinery already exists — it's the hosted
  *deployment* that's single-gated).
- **The open-mind fork (recommend PM weigh)**: do per-user keys live **server-side (stored, encrypted, #358)**
  or **host-side (never stored; passed per-request from the user's own Claude)**? The purest BYO-substrate
  answer is host-held; the issue as written assumes server-stored. This fork decides most of the build.

---

## Answers to the issue's "Open Qs (verify before building)"

**Q1 — Does `user_api_keys`/`api_keys` already cover an *Anthropic LLM* key (vs only integration keys)?**
**YES.** `services/database/models.py:201` (`user_api_keys`): `provider = Column(String(50)...)` with the
inline comment *"openai, anthropic, github, etc"* — LLM providers are first-class, not integration-only. The
unique constraint is `(user_id, provider)`, so each user gets one anthropic key. **The secret is NOT in the
DB** — `key_reference` (a String(500)) is a **keychain identifier** of the form `piper_{user_id}_{provider}`;
the actual secret lives in `KeychainService` under `username=user_id` (`UserAPIKeyService.store_user_key`
→ `self._keychain.store_api_key(provider, api_key, username=user_id)`, `user_api_key_service.py:187`).

**Q2 — Per-user auth mechanism: token vs account/login?**
The app **already has** per-user identity: the `/api/v1/.../store|list|validate|rotate` routes resolve
`current_user.user_id` (`web/api/routes/api_keys.py`), backed by CORE-USERS-API (#228) + the `users` table.
So "who is asking" is a solved problem *in the app*. The gap is **deployment-shaped**: the hosted alpha
(`alpha.pipermorgan.ai`) sits behind a single shared **Caddy basic-auth** gate, which authenticates "a tester"
but not "*which* tester." Work item 2 = surface the app's real auth (login/session or token → `current_user`)
as the hosted entry gate, replacing the shared basic-auth.

---

## What already exists (don't rebuild)

| Component | Where | State |
|---|---|---|
| Per-user key schema (incl. anthropic) | `services/database/models.py:201` `user_api_keys` | ✅ complete (user_id, provider, key_reference, validation, rotation, audit) |
| Per-user key CRUD service | `services/security/user_api_key_service.py` `UserAPIKeyService` | ✅ store / **retrieve** / delete / validate / rotate, all by `user_id` |
| Per-user key REST API | `web/api/routes/api_keys.py` | ✅ `/store`, `/list`, `/{provider}`, `/validate`, `/rotate` — auth via `current_user` |
| Key rotation | `services/security/key_rotation_service.py` + service `rotate_user_key` | ✅ exists (previous_key_reference + rotated_at) |
| User identity | CORE-USERS-API #228, `users` table, `current_user` | ✅ exists in app |
| Clean resolution entry point | `UserAPIKeyService.retrieve_user_key(session, user_id, provider)` (`:261`) | ✅ returns the actual key — ready to call from the LLM path |

**So Work item 1's premise ("storage already exists") is correct — and the retrieval entry point exists too.**

## The real gaps (what #1185 actually has to build)

### Gap A — the LLM client is instance-scoped + built at init (the core wiring is bigger than "add a param")
`services/llm/clients.py:84 _init_clients()` constructs `self.anthropic_client = Anthropic(api_key=...)`
**once**, using `self._config_service.get_api_key("anthropic")` — the **instance** path (keychain "anthropic"
with *no* username → env fallback; `llm_config_service.py:211`). It is a singleton reused for every request.
Multi-tenant therefore needs:
1. **Thread `user_id` from the request/intent down to the LLM call** — today the LLM layer has no user context
   (the `/intent` handler → engine → `LLMClient` chain doesn't carry `user_id` to the client). This is the
   bulk of the work.
2. **Per-request key resolution** — call `UserAPIKeyService.retrieve_user_key(user_id, "anthropic")`, fall back
   to the instance key (`get_api_key("anthropic")`) if the user has none (honest degradation).
3. **Client-lifecycle change** — because the client is built at init, per-user keys need either per-request
   `Anthropic(api_key=user_key)` construction or a `user_id`-keyed client cache/pool. (Per-request construction
   is cheap for the Anthropic SDK; a small LRU cache avoids rebuilding per call.)

### Gap B — hosted secret store (THE architectural decision; PM's "where in the stack")
`UserAPIKeyService` stores the secret in **macOS `KeychainService`**. The hosted droplet is **Linux — no macOS
keychain**. So the per-user-key storage as built is **laptop-only**; the hosted multi-tenant case needs a
different secret store. This is where #358 (SEC-ENCRYPT-ATREST) becomes load-bearing, not optional:
- **Option B1 — encrypted-at-rest in Postgres (#358)**: replace the keychain-reference with an encrypted-secret
  column (or have `key_reference` point at an encrypted DB blob). Decouples from any OS keychain; portable to
  any host. Key-encryption-key (KEK) lives in the droplet env / a secrets manager. **Recommended default.**
- **Option B2 — cloud secrets manager / KMS / Vault**: strongest isolation, more infra; likely over-built for
  alpha→beta scale.
- **Option B3 — Linux keychain backend** (e.g. `keyring` with a headless backend): keeps the keychain
  abstraction but adds an ops dependency + still needs at-rest encryption. Weakest of the three.

### Gap C — per-user auth at the hosted edge (Work item 2)
Replace Caddy shared basic-auth with the app's real per-user auth (login/session/token → `current_user`), so
the instance can tell testers apart. App machinery exists; this is deployment + an auth-surface decision
(session-cookie vs bearer token for the plugin's MCP calls).

---

## The "where in the stack can/should keys connect" map (PM's open-mind directive)

There are **three key *types*** in play, and **multiple *layers*** each could connect at. Worth deciding
deliberately rather than defaulting.

**Key types:**
1. **LLM key (anthropic)** — funds inference. #1185's focus. Today: shared instance key.
2. **Integration keys** (github / notion / slack / google) — per ADR-058, already user-scoped via the same
   `user_api_keys` + keychain-by-user_id machinery.
3. **Instance/fallback key** — the shared key (alpha today; the one that hit the usage wall).

**Layers a key could connect at:**
| Layer | What connects here | Today | Multi-tenant option |
|---|---|---|---|
| **Host / plugin** (user's own Claude) | user's LLM key + their connected accounts | n/a (alpha uses our key) | **Purest BYO**: key never touches our server; passed per-request, or inference happens host-side |
| **Hosted edge / auth** | identity | shared basic-auth | per-user login/token → `current_user` |
| **Piper server — resolution** | user_id → key | instance only (`get_api_key`) | per-request `retrieve_user_key` + fallback (Gap A) |
| **Piper server — storage** | the secret at rest | macOS keychain (laptop only) | encrypted-DB #358 (Gap B) |
| **Setup / capture** | user hands over the key | n/a | Option A `/connect` → existing `/store` endpoint |

**The fork worth PM's explicit call:**
- **Server-stored (the issue's assumption)** — user's key lives encrypted in our hosted DB; we resolve it
  per-request. Simplest to ship; but we now *hold* the user's LLM key (trust + liability surface; needs #358).
- **Host-held (purest BYO-substrate)** — the user's key stays in *their* Claude/host; it's passed per-request
  (or inference is brokered host-side) and **never stored by us**. Aligns with the BYO-colleague thesis
  ("user brings the substrate; we never hold the secret") and collapses Gap B entirely — but depends on the
  plugin/MCP transport being able to carry a per-request key safely, and changes the hosted-MCP auth model.

These aren't mutually exclusive forever (server-stored for a frictionless hosted beta; host-held as the v1
BYO endgame), but **which one beta ships on is a real decision** — and it's the same "what migrates vs what
stays local" question #1162 raises. It also connects to the braintrust convergence: the **resource-consent
dimension** (HOST) and **agent-attribution** (`actor_chain`, Arch/CXO) both assume we can name *whose* key
spent *what* — easier to honor cleanly in the host-held model.

---

## Recommendation (initial — for PM discussion, not a build commitment)

1. **The storage layer is a non-issue** — it exists and covers anthropic. Don't rebuild; reuse `retrieve_user_key`.
2. **Decide the fork first** (server-stored-encrypted vs host-held) — it determines whether Gap B (#358) is on
   the critical path or disappears. *My lean: server-stored-encrypted for the hosted beta (frictionless,
   ships on existing machinery + #358), with host-held flagged as the v1 BYO endgame.* But this is a
   trust/strategy call that's yours, and it interacts with the BYO-colleague sequencing PPM/Arch just ratified.
3. **If server-stored**: critical path = #358 (encrypted-at-rest, replace keychain dependency) → Gap A (user_id
   threading + per-request resolution + client lifecycle) → Gap C (per-user hosted auth). Roughly that order.
4. **Sequencing sanity-check with the braintrust ruling**: PPM put colleague-mode at post-beta v1.1, but #1185
   is the *hosted-beta-key* thread (driven by the usage-wall evidence), distinct from colleague-mode — so its
   build-timing is a separate roadmap call. Worth confirming with PPM where #1185 sits vs M3 blocker work.

**No code written; this is the verify-before-building scoping the issue asked for.** Next step on your word:
either (a) you make the fork call and I draft the build-sequencing memo for PPM/Lead, or (b) we discuss the
fork live first.

— PA, 2026-06-10

---

## Converged design (PM walk-through, 2026-06-10)

PM ratified the lean (server-stored-encrypted for beta) and refined the endgame to **BYO-first with a
server-stored fallback** — a layered, resilient chain, not an either/or. Decisions below are PM-confirmed
unless marked *[deferred]*.

### Call-time key resolution — the ordered chain (most-BYO → honest-refuse)

1. **BYO (b) — host-side inference** *(true endgame)*: the user's own Claude/host runs inference; our server
   never sees the key. This is the BYO-colleague / skill-broker model (braintrust-converged; PPM put it at
   post-beta v1.1). PM: this is the real endgame.
2. **BYO (a) — key passed per-request, not stored** *(may persist)*: the plugin passes the user's key; we use
   it in-memory, never persist. PM: even with (b) as endgame, integration may still be needed at other layers,
   so (a) may **persist as a fallback / optional part of a resilient design** — not necessarily retired once
   (b) ships.
3. **Server-stored per-user key (encrypted)** *(the beta rung)*: the fallback when no BYO key is present.
   **This rung IS #358** (see dependency below).
4. **Offer to configure** *(honest bottom — NEVER a shared instance key)*: PM confirmed the shared instance key
   is not a hosted fallback (it's what caused the usage wall). The "offer" is itself a **branch**, and the
   branch is nuanced:
   - **(i) configure natively** — user gives Piper the key → lands at rung 3 (server-stored).
   - **(ii) help the user configure their own harness** — guide them to set up BYO in their own Claude/host →
     lands at rung 1/2. *(This is a real onboarding/consent moment, possibly skill-shaped — "help me set up my
     own key" is itself a Piper-judgment task.)*

*(The shared instance key survives ONLY for the local single-user install, where it's the user's own key.)*

### Storage: capability vs acquisition (two separate things — PM's #3 refinement)

- **Capability**: the encrypted store handles the **whole user-secret store** — LLM key *and* integration keys
  (GitHub/Notion/Slack, ADR-058), which share the same macOS-keychain-on-droplet break. Fix once, for all.
- **Acquisition policy**: trust-gradient / **need-scoped**, NOT blanket up-front capture. The user **offers** a
  connection, or Piper asks **only when a request needs it** (just-in-time). This is exactly the braintrust
  **"enumerate" tier** / just-in-time discipline (CXO/HOST) applied to credential acquisition. Storage-can-hold
  ≠ ask-for-everything.

### Legibility (PM: 100% — for the user AND for us)

Whichever rung serves a call, the system must name **whose key spent what** — for the user (resource-consent,
trust) and for us (audit, cost attribution, debugging). Required at every rung; trivial in BYO, needs
deliberate plumbing in server-stored. Ties to the braintrust `actor_chain` + resource-consent dimension.

### The #358 dependency (the thing to stay clear on)

**Server-stored (rung 3) IS #358 by construction.** On the Linux droplet there's no macOS keychain, so there
is no per-user secret store *until* the encrypted-at-rest store (#358) exists. So:
- **#358 and the server-stored rung are the same milestone** — wherever #358 lands, that's when rung 3 becomes
  real on the hosted instance.
- PM has **moved #358 to MVP sprint M5 (distro & polish)**, possibly → a release-ready sprint *after* beta.
- **Consequence to hold**: if #358 lands in M5 alongside the hosted-distro work, the server-stored rung is in
  the beta. **If #358 slides post-beta, the hosted beta has no server-stored rung** — it's BYO-only, or it
  continues on the shared-key alpha until #358 lands. Both are coherent; we just shouldn't ship real-user
  server-stored keys *before* #358 (that would mean storing user LLM keys without at-rest encryption). Stated
  neutrally: the encryption isn't optional polish on top of server-stored — it's the floor that makes
  server-stored exist on the droplet at all.

### Sequencing (PM-confirmed + deferred)

- **Beta ships the server-stored fallback** (rung 3), arriving with #358 at M5. ✅
- **The BYO track (rungs 1–2) runs alongside** and "eventually catches up." ✅
- **Does BYO block the 1.0 launch release?** *[deferred — PM decides later]*
- **#358 exact placement** (M5 vs a post-beta release-ready sprint) *[deferred — PM leaning M5]*.

### Non-wasteful property (confirmed)

Server-stored-for-beta is **the fallback rung of the endgame, built first** — not a detour. The BYO rungs add
on top later; nothing is thrown away. This is the strongest structural argument for the chosen lean.

— PA, 2026-06-10 (walk-through capture)
