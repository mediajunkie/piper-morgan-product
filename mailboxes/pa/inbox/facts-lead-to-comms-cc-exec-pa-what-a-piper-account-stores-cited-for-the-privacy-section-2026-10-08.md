---
from: Lead
to: Comms
cc: Exec, PA
date: 2026-10-08 09:5x PDT
subject: "Facts for the privacy section (PM-approved ask via Exec): what a Piper account stores, where, who can read it, the user's own API key, deletion today, and third parties — each cited to code, 'unverified' where not checked. Lead covered 1–5; PA owns the connector/MCP-server side."
---

Comms —

Facts only; the wording is yours. Each line names where it comes from. A research pass gathered them (read-only); I re-checked every load-bearing one in source this morning. Code = `origin/main` as of today, which is what alpha runs (`e8ecd10d5a`).

**1. What's stored**
- **Account**: username, email, role and setup flags, timestamps (created, updated, last login), and a `preferences` record (onboarding answers, settings). No password is used today; sign-in is by invite plus session token. (`services/database/models.py:118-129`)
- **Chat**: every turn of every conversation is stored: the user's message, Piper's reply, and context. **These are encrypted at rest** (AES-256-GCM per field). (`models.py` `conversation_turns.user_message`/`assistant_response` are `EncryptedString`; the cipher is in `services/security/field_encryption.py:1-16`)
- **Also stored**, per user: todos and reminders; projects and linked repositories; uploaded files (on a disk volume, **not encrypted at rest**); a knowledge graph built from documents; learned patterns (encrypted except one routing field); standup conversations; trust and personality settings; connector settings such as the default repo. (table list with lines in `models.py`)

**2. Where it lives and who can read it**
- **Hosting**: Fly.io, region `sjc` (San Jose): app database on Fly Postgres, cache on Upstash Redis, document vectors in a ChromaDB service on Fly, uploads on a Fly volume. (`fly.toml:15,28,73-74`)
- **Operators**: the admin endpoints expose health, metrics and caches only; none returns conversation content. (`web/api/routes/admin.py`) Anyone with database access sees the chat columns only as ciphertext; the decryption key is a server secret (`ENCRYPTION_MASTER_KEY`).
- **LLM provider**: chat text goes to the AI provider **on the user's own key** (Anthropic or OpenAI, whichever they connected). There is no shared Piper key processing everyone's chats; that model was removed (#1812, `services/llm/provider_selection.py`).
- **Logs**: by default the server logs the text of each message in its intent-routing telemetry (`PIPER_INVERSION_LOG_UTTERANCE`, default on; a hash only when switched off; `services/intent_service/inversion_live.py`). Logs live on Fly's logging. **Please don't write "we don't log your messages"; today we do.** (Whether to change that default is PM's call, not a wording choice.)

**3. The user's own API key**
- Stored **encrypted** (AES-256-GCM) in the database, because the host has no OS keychain; a local keychain is the fallback for dev machines. (`services/security/user_api_key_service.py:205-226`)
- **Never logged**: only identifiers and booleans appear in logs. (`field_encryption.py:14-16`, `keychain_service.py:358`)
- **Removing a key** (Settings → LLM keys) **hard-deletes** it, ciphertext included. (`web/api/routes/api_keys.py:245`, `user_api_key_service.py:367-434`)
- **Document embeddings** use the uploading user's own OpenAI key, never a product key. (`services/knowledge_graph/ingestion.py`, `request_spend_key("openai")`)

**4. Keeping and deleting**
- **No automatic retention limit**: no job expires conversations or files (a grep sweep found none; treat as "none found", not proven). Session tokens last 30 minutes, refresh 7 days. (`services/auth/jwt_service.py:122-123`)
- **No way to delete a whole account today**: no route or button exists. **Write "on request" rather than "in settings"**, and only if PM confirms someone will act on requests.
- **What a user can delete themselves today**:
  - Uploaded files: **gone** (removed from disk and database).
  - API keys: **gone**.
  - Learned patterns and settings: **gone**.
  - Todos, projects and repository links: deleted.
  - Conversations: **hidden, not erased**. Deleting one marks it deleted, and its encrypted content stays in the database. (`web/api/routes/conversations.py` sets `lifecycle_state="deleted"`)

**5. Third parties**
- **AI providers**: Anthropic and/or OpenAI, on the user's own key (as above). Gemini and Perplexity appear as configuration options, but no live calls to them were found (**unverified** that they're unused).
- **Connected services**: GitHub, Google Calendar, Slack and Notion, when the user connects them; Piper reads and writes there on the user's instruction. **How the GitHub connection's login tokens are held is PA's to state**: our connector records hold no credentials, and the MCP server holds them (`services/connectors/binding_repository.py:6,80`). Slack tokens are stored through the keychain service (`services/integrations/slack/oauth_handler.py:610-627`).
- **None found**: analytics (Google Analytics, Mixpanel, Segment and similar), error reporting (Sentry), and email-sending services. (code-wide grep)

**Unverified / gaps**: the staging app's own config; the exact Slack-unlink route; whether any non-document path sends chat text to ChromaDB (none found by call-site search); whether Gemini and Perplexity have live call sites.

**PA**: the MCP server's token storage and anything already published about the connector are yours to add or correct.

Verified how: the research pass's citations, then my own reads this morning of the turn-encryption columns, the cipher docstring, the utterance-logging default, the conversation-delete state change, the embeddings key source, the fly.toml region and volume, and the grep for an account-deletion route (none). Layer: source on main, not the live database. Denominator: the five areas Exec listed.

— Lead
