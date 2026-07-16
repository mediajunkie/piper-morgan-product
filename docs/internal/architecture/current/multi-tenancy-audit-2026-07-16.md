# Multi-Tenancy Audit — the "acts like a singleton, ignores the user table" class

**Trigger**: 2026-07-16. PM's beta account (`dinp`) got "Something unexpected happened" on every LLM turn despite a valid per-user Anthropic key. Root cause: LLM provider **selection** is a GLOBAL/single-tenant setting — one user's setup pinned the whole instance, and a second user's per-user key was un-selectable. PM: *"why does the setup for one user lock in a global instance? … find where else the codebase still acts like a singleton and ignores the user table! … nothing should be global — it should be impossible."*

**Status**: IN PROGRESS (audit sweep 2026-07-16). This doc holds the five-whys + the inventory + the enforcement recommendation.

---

## Five Whys — "LLM provider selection is global"

1. **Why did every chat turn fail for `dinp` despite a valid Anthropic key?**
   The instance was pinned to OpenAI (a quota-dead key); `dinp`'s Anthropic key was never *selected*, so every turn tried the dead OpenAI key → `429 insufficient_quota` → "All configured LLM providers failed."

2. **Why was the instance pinned to OpenAI?**
   Provider *selection* — `default_llm_provider` + the `authorized_llm_providers` consent list — is read from the **global** keychain/credential store, not per-user. `dinp`'s 7/13 setup wrote those global values to `openai`, for everyone.

3. **Why is provider selection global?**
   `services/config/llm_config_service.py` (`LLMSelectionConfigService`) reads `self._keychain_service.get_api_key(provider)` and `get_api_key("authorized_llm_providers")` with **no `user_id`**, and caches `_default_provider`/`_excluded_providers` as instance attributes at construction. It was written single-tenant — its own comment says *"when **the** user completes setup"* (one user == the instance).

4. **Why was it built single-tenant and never migrated?**
   Multi-tenancy was retrofitted **one surface at a time, reactively**: per-user KEY resolution (#1185), per-user default-repo (#1366), per-user personalization (ADR-075). Provider *selection* was never on the retrofit list — because nobody had exercised the "user A's provider ≠ user B's provider" path until a real second tester (`dinp`) arrived with a different provider than the setup account.

5. **Why wasn't it caught by search instead of by a tester hitting it?**
   **There is no enforcement that a user-specific value cannot be read globally.** A principal-threading lint exists (`scripts/principal_threading_lint.py`, #1252) but is scoped to intent-handler principal reads — it does NOT cover credential/config global reads in service singletons. So global-singleton surfaces stay invisible until someone trips them.

**ROOT PATTERN**: the codebase's *default posture is single-tenant* (global keychain reads, singleton config services cached at construction), and multi-tenancy is **opt-in per surface** rather than **enforced by construction**. That inverts PM's requirement. The fix isn't just "make provider selection per-user" — it's **(a)** migrate the surfaces, and **(b)** flip the default: make per-user the norm and global reads of user-specific data *impossible-by-construction* (an AST/lint guard that fails the build, mirroring the D1a owner-scoping guard and the #1283 reachability ratchet).

---

## Inventory (audit sweep 2026-07-16 — four parallel investigators)

*Populated below as findings land. Each: `file:line` · what's globalized · consequence · severity · fix.*

### HIGH — affects a real tester's request / cross-user (confirmed by 2 independent investigators)

**The LLM provider subsystem is single-tenant end-to-end.** Per-user KEY resolution (#1185) exists but is *Anthropic-only* and is bypassed entirely when global provider SELECTION ≠ anthropic. Sites:

| # | `file:line` | What's globalized | Consequence |
|---|---|---|---|
| P1 | `services/llm/clients.py:304` | `get_api_key("default_llm_provider")` (no username) — **the request-path selection point** (twin of the exemplar; my manual look missed it) | Every user's provider chosen from one global slot; if it ≠ the user's provider, their bound per-request key is never reached |
| P2 | `web/api/routes/setup.py:985,1005,1017` | **write-side root**: setup stores `default_llm_provider` / `authorized_llm_providers` / provider keys GLOBALLY (`# No username = global`) | Every user's setup is last-writer-wins for the whole instance — the exact mechanism of dinp's incident |
| P3 | `services/llm/clients.py:86-129`, `:609` | singleton `LLMClient` builds anthropic/openai/gemini clients ONCE at import from global keys | Process-global clients serve all users |
| P4 | `services/config/llm_config_service.py:333` (`get_default_provider`), `:178` (consent list), `:229` (provider key) | all read keychain with no `user_id`; service is user-unaware by construction | The systemic root — the config layer can't see a per-user key/choice |
| P5 | `services/llm/clients.py:479,507` (openai), `:556-566` (gemini) | per-request key ContextVar consumed ONLY in `_anthropic_complete` (`:422`) | OpenAI/Gemini calls ALWAYS use the server's global key — BYOC is Anthropic-only |
| P6 | `services/domain/llm_domain_service.py:111-156` | `complete()` neither accepts nor forwards `user_id` (the DDD "only way to reach LLM") | user identity is dropped before selection |
| P7 | `services/intent_service/llm_classifier.py:340` + `conversational_floor.py:862` | `user_id` in scope, threaded to the per-user *system prompt* but NOT to `.complete()` selection | proves identity reaches the layer and is dropped for the LLM call |

**Non-LLM HIGH:**
- N1 · `config/notion_config.py:28` via `services/integrations/notion/notion_integration_router.py:66` (`NotionMCPAdapter()` no-config-service fallback, reachable in prod) → reads the GLOBAL Notion token; every Notion op on that adapter acts with one user's token. (Primary connect/status/resolve path IS user-scoped; this is the reachable legacy fallback.)
- N2 · `services/knowledge_graph/ingestion.py:39` — radar/insights embeddings hard-wire the server OpenAI key → **live symptom: 19× `/api/v1/radar` errors "Please provide an OpenAI API key"** during PM's session (radar also 422s separately — validation bug, track apart).

### MED — setup/config surfaces that globalize a per-user credential
- `web/api/routes/setup.py:646` (`/check-keychain`) + `:691` (`/use-keychain`) — report/validate GLOBAL key state with no principal; a hosted user sees the server/other-tenant key state. (Both setup endpoints take no `user_id` at all — local-first surface not yet multi-tenant.)
- `services/config/llm_config_service.py:144,147` — `_excluded_providers` + `_default_provider = getenv("PIPER_DEFAULT_PROVIDER","openai")` cached at construction, shared by all; `_fallback_chain` (`:154`), `get_provider_with_fallback` (`:349`) likewise global.

### LOW — global *fallback* when `user_id` absent (guarded; blast radius = status/test reads)
- `web/api/routes/integrations.py:480` (calendar), `:564` (slack_bot), `:616` (github_token) — legacy global fallback only on the `user_id`-falsy branch; authenticated branches correctly user-scoped. Concerning only if an unauthenticated request can reach them.

### Examined & CLEARED (legitimately server/app-global — NOT bugs)
`clients.py:94/105/118` server fallback keys (documented); `key_rotation_service` (admin/ops, per-user raises NotImplementedError); OAuth *app* client_id/secret (`github_oauth_handler`, `integration_config_service`, `slack config_service`) — app-level by definition; `slack_app_token` socket-mode (app-global). Good per-user patterns for reference: `user_api_key_service.py:327`, the notion/github/slack config_services' user-scoped reads, `google_calendar_adapter.py:403`.

### HIGH — config-file singleton (`PIPER.user.md`) shadows per-user state (2nd investigator)

**The systemic pattern here: the global `config/PIPER.user.md` layer sits ABOVE the per-user keychain/DB in precedence** — so PM's personal file silently *overrides* each tester's own settings. Same class as #1366 (default-repo), now on **credentials**. (`PIPER.user.md` is absent in this worktree → reads `{}` here; on the hosted box PM's file is populated, so these bite per the section PM filled.)

| # | `file:line` | What's shadowed | Consequence |
|---|---|---|---|
| C1 | `services/integrations/notion/config_service.py:119→186,192,199` | Notion api_key + workspace_id: global file OR'd BEFORE the user-scoped `keychain.get_api_key("notion", username=user_id)` | if PM's file has a Notion key, **every user transacts against PM's Notion workspace**; a tester's own key is ignored |
| C2 | `services/integrations/slack/config_service.py:129→219,228-237` | Slack bot_token + user_token: global file OR'd ahead of user keychain | every user's Slack ops (incl. `search.messages` — reads DMs) run as PM's tokens |
| C3 | `web/personality_integration.py:50,59,106` via routes `web/api/routes/personality.py:44,79,142` | `PUT /api/v1/personality/profile/{user_id}` writes the ONE global file, ignoring `user_id` | **cross-tenant WRITE**: one user's persona save changes warmth/confidence for everyone incl. PM; the first-YAML-block rewrite can DESTROY PM's other `PIPER.user.md` sections |
| C4 | `services/intent_service/canonical_handlers.py:243,2502,3773` | timezone from `piper_config_loader.load_standup_config()` (PM's global tz) though `user_id` in scope | every tester sees date/time/agenda in **PM's timezone** (the #1381/#1405 class, un-migrated here; fix pattern exists next door in `context_assembler.py:49-51`) |

**MED (config-file):** `calendar/config_service.py:107,196` (`calendar_id` — global file base, bites if PM set non-"primary"); `services/user_context_service.py:107,137` ("generic" base is actually PM's file → user with no org inherits PM's `organization` + fallback portfolio); `context_assembler.py:54-58` (tz per-user first but seeded default lacks `timezone` → still degrades to PM's global tz).
**LOW/OK:** `intent_service.py:6958` default_labels (default_repository IS per-user #1366 ✓); `pm_number_manager` (shared PM-001 convention ✓); `document_repository.py:59` (documented ADR-071 D7 single-owner seam ✓).

*(Singleton-service / unscoped-repo vector: 4th investigator still running — appended on completion.)*

---

## Enforcement recommendation ("make it impossible")

_(to be written after the inventory — likely: extend the principal-threading lint / add an AST guard that flags user-specific credential+config reads lacking an owner_id, so a new single-tenant read fails CI rather than shipping.)_

---

## Related
- #1414 (honest-error on the classification surface — the message that hid this), #1415 (provider selection global — the exemplar), #1152 (resilience: dead provider → fallback), #1366 (default-repo global — prior instance of this class), ADR-071 (owner-scoping), #1185 (per-user key resolution), ADR-075 (per-user personalization).
