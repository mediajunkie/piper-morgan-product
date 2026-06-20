# Gameplan — #1185 BYO-KEY-MULTI-TENANT (whole)

**Issue**: #1185 · **Scope**: WHOLE (PM 2026-06-20) — per-user identity + LLM-key wiring, one coherent effort
**Author**: Lead Dev · **Date**: 2026-06-20 · **Template**: gameplan-template v9.6
**Sprint**: RECONNECT Phase-0 (identity foundation)

---

## ⭐ Key finding (Phase 0 investigation) — this is COMPLETE-THE-PATTERN, not greenfield

Three pieces already exist *separately*; #1185 wires them together:

1. **Per-request key rail** — `services/llm/request_key.py`: a request-scoped `ContextVar` (`_user_api_key`), the `request_api_key(key)` context manager (binds + resets-in-finally → no cross-request leak), and `anthropic_client_for_request(server_client)` (returns a fresh `Anthropic(api_key=user_key)` if bound, else the server client). `clients.py:_anthropic_complete` (line 421) already uses it. `complete()` already accepts `user_id`.
2. **Stored per-user keys** — `UserAPIKeyService` (`services/security/user_api_key_service.py`): `store_user_key`, **`retrieve_user_key(session, user_id, provider)`**, `validate_user_key`, `rotate_user_key`. The `user_api_keys` table covers `anthropic` (verified — no schema change). CRUD wired at `web/api/routes/api_keys.py`.
3. **Authenticated user_id** — `/api/v1/intent` resolves it from a **JWT** (`get_current_user_optional`, #455/#490: `user_id = current_user.sub`; Authorization header OR `auth_token` cookie). `JWTService.validate_token` exists.

**The gap**: at `intent.py:338` the binding uses ONLY the header — `with request_api_key(request.headers.get("X-User-Api-Key")):` — it never falls back to the *stored* key for the authenticated user. The header path = **Claude Desktop BYOC** (transient, never persisted). The DB path = **hosted web** (authed user, stored key) — built but unconnected.

**This resolves the issue's open design Q**: "token vs account/login" → **token (JWT), already in place.**

---

## Phase -1 / Phase 0 — Infrastructure (VERIFIED, this session)

| Assumption | Status |
|---|---|
| LLM key resolution path | ✅ `clients.py` → `LLMConfigService.get_api_key` (server) + per-request override via `request_key.py` ContextVar |
| Per-user key storage | ✅ `UserAPIKeyService.retrieve_user_key(session, user_id, provider)`; `user_api_keys` covers `anthropic` |
| Authenticated identity | ✅ JWT (`current_user.sub`) at `/intent`; `JWTService` |
| What's missing | ❌ the DB-fallback at the binding; binding only on `/intent`; key-capture at `/connect`; encrypt-at-rest hardening |

**PROCEED** — understanding verified against live code.

---

## Phase 0.6 — Data Flow (the heart of #1185)

**The rail**: one request-scoped `ContextVar` feeds `anthropic_client_for_request`. Today it has ONE source (header). #1185 adds a SECOND source (DB-by-user_id), priority-ordered.

```
request → [resolve key]                              → request_api_key(key) → ContextVar
            1. X-User-Api-Key header   (Desktop BYOC)
            2. retrieve_user_key(user_id, "anthropic")   (hosted web — NEW)
            3. None → server key fallback
                          │
   process_intent → intent_service → floor → LLMClient._anthropic_complete
                          → anthropic_client_for_request(ContextVar)  ✅ already reads the rail
```

| Layer | Has user_id? | Source |
|---|---|---|
| `/intent` route | ✅ | `current_user.sub` (JWT) — at the binding site (line 338) |
| ContextVar (`request_key`) | n/a | bound at route, read deep — per-asyncio-task, safe |
| `LLMClient._anthropic_complete` | n/a | reads the ContextVar via `anthropic_client_for_request` |

**Pattern-adaptation note** (template Phase 0.6): the header source is *transient* (never stored); the DB source is *persisted* (UserAPIKeyService). Both terminate in the *same* ContextVar → the LLM client is source-agnostic. Priority: header > stored > server (Desktop's explicit per-call key wins; hosted falls to stored; PM/dev path falls to server).

### Conditional phases (template 0.5 / 0.7 / 0.8)
- **0.5 Frontend-Backend Contract** — ⚠️ *flag*: backend-only EXCEPT if Phase 3's `/connect` capture exposes a **web-UI** surface (vs the plugin `/connect` skill). If web-UI: run the path-contract check (route paths + fetch calls + static mount) before wiring. (The plugin-skill path is #1300's; no web fetch.)
- **0.7 Conversation Design** — N/A: not a multi-turn conversational feature; `/connect` is a one-shot setup step (owned by #1300).
- **0.8 Post-Completion side-effect** — Phase 3 changes user state. On capture success: the user's key is **stored + resolvable per-request** (Phase 1). Downstream behavior change: that user's LLM calls draw on **their** key (off the shared-instance ceiling); honest "no key configured" disappears once set. Verify: a request *after* capture resolves the stored key end-to-end.

---

## Phases

### Phase 1 — DB-resolved key binding (THE core change; small)
**Objective**: when no header but an authenticated user has a stored Anthropic key, bind it to the per-request rail.
**Tasks**:
- [ ] Add a resolver (e.g. `request_key.resolve_request_key(header, user_id, session)`): header → `retrieve_user_key(user_id, "anthropic")` → None. Keep it tiny + pure (unit-testable).
- [ ] At `intent.py:338`, replace the header-only bind with the resolver result.
- [ ] Honest degradation: if resolved None AND server-key disabled (hosted), return "no key configured — run /connect" (don't 500).
**TDD** (write first):
- [ ] unit: resolver matrix — header-present → header; no-header+stored → stored; no-header+no-stored → None.
- [ ] **wiring** (no internal mock): bind via resolver → `anthropic_client_for_request` returns a client keyed to the *stored* key for a user with one.
- [ ] regression: header path unchanged (Desktop BYOC still wins).
**Deliverables**: `request_key.resolve_request_key`, updated `intent.py` binding, tests.

### Phase 2 — Extend the binding beyond /intent + confirm auth coverage (medium; the largest unknown)
**Objective**: every LLM-invoking entrypoint resolves the per-user key; confirm JWT auth covers hosted testers.
**Tasks**:
- [ ] Audit routes that reach `LLMClient` outside `/intent` (grep the call sites: conversational_floor, other API routes). For each user-facing one, apply the resolver (a shared FastAPI dependency is cleanest).
- [ ] Confirm the JWT path issues tokens for hosted testers (login/issue flow) — and how it relates to the Caddy basic-auth gate (replace vs coexist; ties #1162). **If a login/issue flow is missing → STOP + decide with PM** (may be its own slice).
**TDD**:
- [ ] integration: an authenticated request to a second LLM route uses the user's key.
- [ ] routing/wiring: the dependency binds the rail before the LLM call.
**Deliverables**: shared key-binding dependency; route coverage list; auth-coverage finding.

### Phase 3 — Key capture at /connect (small; ties #1300)
**Objective**: a user stores their Anthropic key once; it's then resolved per-request (Phase 1).
**Tasks**:
- [ ] Fold capture into the #1300 `/connect` step → `store_user_key(user_id, "anthropic", key)`.
- [ ] Honest degradation when absent (surface "configure your key").
**TDD**:
- [ ] integration: capture → store → next request resolves it (end-to-end with Phase 1).
**Deliverables**: `/connect` key-capture; test. **Dependency: #1300.**

### Phase 4 — Encrypt-at-rest (small–medium; ties #358)
**Objective**: stored per-user keys are encrypted at rest.
**Tasks**:
- [ ] Verify how `UserAPIKeyService` persists (keychain reference vs DB column) and whether it's encrypted; harden if not.
- [ ] Confirm no key is logged on any path (resolver, capture, client).
**TDD**:
- [ ] test: stored value is not plaintext at rest; round-trips correctly.
**Deliverables**: encryption verified/added; no-leak test. **Ties #358.**

### Phase Z — Handoff & close
- [ ] All AC met + evidence; wiring tests green; no regression to header/server paths.
- [ ] Update #1185 (evidence, Open-Q-2 resolved=JWT), request PM review (PM closes).
- [ ] Session log + decisions note if any architectural call (e.g. Caddy-gate removal) lands.

---

## STOP conditions (issue-specific)
- Phase 2: if there's **no JWT login/issue flow for hosted testers** → STOP, decide with PM (auth-issuance may be a separate slice; #1162 gate-removal interacts).
- If `retrieve_user_key` needs a DB session not available at the binding site → trace the session source before wiring (don't fabricate one).
- Any key appearing in a log → STOP (security).
- If the header vs stored priority is wrong for a real flow → confirm with PM before shipping.

## Effort
**Medium overall** (down from "Large" — the rail + auth + storage exist). Phase 1 small · Phase 2 medium (auth-coverage unknown) · Phase 3 small (rides #1300) · Phase 4 small–medium.

## Resolved open-Qs (were in #1185)
- ✅ `user_api_keys` covers Anthropic (no schema change).
- ✅ Per-user auth mechanism = **JWT (token)**, already implemented (#455/#490) — *not* a new account/login system.

## Dependencies
#1300 (Phase 3 capture) · #358 (Phase 4 encrypt) · #1162 (Phase 2 — Caddy-gate-vs-JWT interaction).

## Subagent decision (gate 3)
Phases are sequential + each small, with shared files (`request_key.py`, `intent.py`) → **solo TDD, phase-by-phase** is cleaner than parallel subagents (which would collide on the rail). Revisit only if Phase 2's route-coverage audit surfaces many independent route edits.
