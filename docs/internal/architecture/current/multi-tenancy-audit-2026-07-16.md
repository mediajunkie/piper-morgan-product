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

### HIGH — affects a real tester's request / cross-user

_(pending sweep synthesis)_

### MED — setup/config surfaces

_(pending)_

### LOW — dev/admin/local-only (acceptable-global)

_(pending)_

---

## Enforcement recommendation ("make it impossible")

_(to be written after the inventory — likely: extend the principal-threading lint / add an AST guard that flags user-specific credential+config reads lacking an owner_id, so a new single-tenant read fails CI rather than shipping.)_

---

## Related
- #1414 (honest-error on the classification surface — the message that hid this), #1415 (provider selection global — the exemplar), #1152 (resilience: dead provider → fallback), #1366 (default-repo global — prior instance of this class), ADR-071 (owner-scoping), #1185 (per-user key resolution), ADR-075 (per-user personalization).
