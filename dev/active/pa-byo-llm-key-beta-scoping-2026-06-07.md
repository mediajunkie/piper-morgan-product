# BYO-LLM-key for beta testers — scoping (2026-06-07)

**Question (PM)**: make it easy for **beta** testers to add their own LLM keys (or OAuth, ideally) when
setting up their Piper backend — whether **hosted** or **locally installed**. Forward-looking (beta, not
the current alpha). Feeds #1162 + the cost model (BYO-key removes our Anthropic spend). Grounded in the
actual Piper code (read 2026-06-07), not assumed.

## Good news: the per-user key substrate already exists

Piper already models per-user keys — most of the storage half is built:
- **`user_api_keys` table** (`services/database/models.py`) — per-user key storage (one of the 36 tables
  the hosted instance migrated).
- **`web/api/routes/api_keys.py`** — list / validate API-key endpoints.
- **`web/api/routes/setup.py`** — setup counts `user_api_keys` (`SELECT COUNT(*) FROM user_api_keys …`)
  to decide if keys are configured.
- **`services/security/key_rotation_service.py` + `key_rotation_reminder.py`** — rotation lifecycle.
- **CLI**: `run_setup_wizard`, `validate_api_key`, `rotate_key_interactive` (`main.py`).

## The gap: the LLM call path doesn't USE per-user keys yet

The actual LLM client resolves keys **instance-level**:
`services/llm/clients.py` → `self._config_service.get_api_key("anthropic")` →
`llm_config_service.get_api_key(provider)` → reads **env var first, then macOS keychain**. No `user_id`;
it does **not** read the `user_api_keys` table. So today every request uses the *instance's* key
(our hosted key), regardless of who's asking.

→ **BYO-key wiring = make the LLM call path resolve the authenticated user's key** from `user_api_keys`
(per-request, scoped by user) and fall back to the instance key only if none. This is the core build.
*(Confidence: based on reading the call path; verify the full resolution chain before implementing.)*

## OAuth reality (be honest — don't conflate two things)

PM said "or OAuth ideally." Two different auth axes:
1. **LLM-provider keys (Anthropic/OpenAI/Gemini)**: these are **API-key based**; the providers do **not**
   offer OAuth for third-party apps to use a user's account programmatically. So "BYO LLM key" realistically
   = the user **pastes/stores an API key** (via the existing `api_keys` route / setup), not an OAuth flow.
   (Claude Code's own subscription-OAuth is host-app inference, not exposed to a plugin/MCP — the
   "seamless, no key" dream needs a platform primitive that doesn't exist yet; tracked already.)
2. **Connector OAuth (Google Calendar, GitHub, Notion, Slack)**: these **are** OAuth, and that's the right
   path for *connectors* — a separate axis from the LLM key, separate work. (Also Linux-hosted-OAuth is
   harder: redirect URIs + the macOS-keychain dependency for stored tokens — see the deploy findings.)

So: **BYO-LLM-key = paste-a-key (easy, substrate exists); connector-auth = OAuth (separate, harder).**
Worth keeping these distinct in any beta "setup your Piper" UX.

## Two deployment modes (the UX differs)

| Mode | Key-setup UX | Difficulty |
|---|---|---|
| **Locally installed** (tester runs their own Piper) | tester sets their own key — already supported via setup wizard / CLI / `api_keys` route / `.env`. "Make it easy" = a clean first-run prompt ("paste your Anthropic key") + the BYOC plugin's `connect`/meet-piper step could drive it. | **Low** — substrate + UX mostly there; polish. |
| **Hosted, multi-tenant** (shared instance, our droplet) | needs **per-user auth** (who's asking) + **per-user key resolution** in the LLM path + secure per-user key storage. The wiring gap above. | **Higher** — the real build. |
| **Hosted, single-tenant-per-tester** (one instance each) | each instance uses that tester's key (instance-level — works today). Simpler auth, more infra (N instances). | **Medium** — infra-heavy, no code gap. |

## How to "make it easy" (the UX target)

A first-run **"connect your Piper" setup step** (converges with Option A's `/piper-morgan:connect`):
1. Prompt: "Paste your Anthropic API key" (link to where to get one).
2. Validate it (the `validate_api_key` route already exists).
3. Store it — per-user via `user_api_keys` (hosted) or local config/keychain (local install).
4. From then on, the LLM path uses *their* key. Honest degradation if missing ("add a key to continue").

This is the same setup surface as Option A (decouple the plugin credential) — **one "connect/setup" step
that captures both the Piper access credential AND the user's LLM key.** Build them together.

## Recommendations
1. **Beta target = BYO-API-key (paste), not OAuth** for the LLM provider — it's the only available
   mechanism, and the substrate (`user_api_keys` + routes + validate + rotation) is largely built.
2. **The build is the LLM-path wiring** (resolve per-user key from `user_api_keys`) + per-user auth on the
   hosted instance. Locally-installed needs only UX polish.
3. **Fold the LLM-key setup into the same `connect`/setup step as Option A** — one place captures Piper
   access + LLM key. Avoids two setup flows.
4. **Connector OAuth (Calendar/GitHub/etc.) is a separate, later track** — don't entangle it with the
   LLM-key story.

## ✅ DECISION (PM 2026-06-09): Multi-tenant, per-user keys
Driven home by live evidence — the shared-our-key hosted alpha hit a usage limit that **blocked testers**
(our limit = everyone's ceiling). So: **one hosted instance; each authenticated user uses their OWN stored
LLM key.** What it requires (the beta build):
1. **Wire the LLM path to per-user keys** — `services/llm/clients.py` → resolve the authenticated user's
   key from `user_api_keys` (per-request, by user_id) instead of the instance-level env/keychain. This is
   THE gap (substrate exists: `user_api_keys` table + `api_keys` route + validate + rotation).
2. **Per-user auth on the hosted instance** — know *who's* asking (replaces the single shared basic-auth).
3. **Capture the user's key at setup** — fold into the **Option A `/connect` step** (one step captures
   Piper access + the user's LLM key). Honest degradation if no key.
4. **Encrypt per-user keys at rest** (#358 SEC-ENCRYPT-ATREST).
→ It's a **beta-build** (product code: LLM client + auth + routes), not a today-task — belongs on the
roadmap (PPM sequencing + Arch feasibility, both now in the braintrust ask). The alpha rides the shared
key (post-Wed-reset) in the meantime. Tracked: GitHub issue (filed 6/9).

## Open questions (remaining)
- Does the existing `user_api_keys` / `api_keys` route already cover storing an *Anthropic* LLM key (vs
  only integration keys)? Verify the table's scope before building.
- Per-user auth mechanism (token vs account/login) on the hosted instance.

## Refs
- `pa-option-a-decouple-credential-plan-2026-06-07.md` (same setup surface)
- `pa-byoc-hosted-distribution-exploration-2026-06-07.md` + `…-alpha-scope-…` (BYO-key, Pro≠key caveat)
- #1162; #358 (encrypt-at-rest, relevant to per-user key storage)
