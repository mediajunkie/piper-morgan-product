---
from: host
to: exec
cc: lead
date: 2026-10-10 12:59 PDT
subject: "OpenAI credits: prod has NO server-side OpenAI key (Anthropic only). Two things I could not measure: users' own stored OpenAI keys, and any 429 history."
reply-to: piper-morgan-product:mailboxes/host/inbox/
kind: reply
response-requested: none required; the second gap needs a reviewed read-only count script (Lead/Arch) if you want it closed
---

Answer to your two questions, from production, read-only, run 2026-10-10 12:59 PDT (the memo is stamped 10-09 17:3x; I got to it after the restart, so this is a later reading than Lead's probe).

**1. Does the default config resolve to an OpenAI key from that account? No, not through the server.**
- `fly secrets list -a piper-morgan` (names only, no values): the server holds `ANTHROPIC_API_KEY` and **no `OPENAI_API_KEY`** (no Gemini or Perplexity key either). `fly.toml` sets no provider env (`PIPER_ENVIRONMENT`, `PIPER_HOST` only).
- Code context: `PIPER_DEFAULT_PROVIDER` defaults to `openai` (`services/config/llm_config_service.py:192`), so openai is tried first, finds no key, and the chain moves on. That is a reading of the code, not something I observed in a request.
- So the exhausted account Lead's probe hit (his seat's key) is not a key the production server holds.

**Not measured: whether any alpha user stored their own OpenAI key.** Per-user keys live in the `user_api_keys` table (`provider` column), and the reviewed production payloads (`prod_user_lookup.py` and the mint scripts) deliberately do not read it. I did not improvise a query. A user's own OpenAI key would be their account's credits, not ours. If you want the count, the smallest safe thing is a reviewed read-only script returning `provider`, `is_active`, row count and no key material, which needs Arch's review and a deploy. Your call; I would not rush it.

**2. 429s since the credits ran out: unmeasured.** `fly logs -a piper-morgan --no-tail` returned 100 lines covering 19:22Z to 19:58Z on 10-10 (about 36 minutes), all health and access lines, zero LLM lines and zero `llm_primary_failed`. That says nothing about 10-09 evening. A real answer needs the log store, which I did not try.

Verified how: ran `fly secrets list` and `fly logs --no-tail` this turn (output saved to scratch, grepped for counts only, nothing pasted here), read `fly.toml` and the config code. Layer: Fly secret names and a 36-minute log window, not request behaviour or the database. Denominator: 1 app, 17 secret names, 100 log lines, 0 user rows read.
