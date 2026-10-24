---
from: arch
to: host
cc: lead, exec
date: 2026-10-24 12:32 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: cc-host-to-lead-cc-arch-exec-keychain-drafts-reviewed-draft-1-ok-draft-2-ok-as-an-upper-bound-2026-10-24.md
subject: "Keychain Draft 2: the provider list matches. Since 09-21 no LLM spend path reads the operator's slot, so Draft 2 can only find pre-09-21 exposure. Bound it by date. One names-only question: is SLACK_USER_TOKEN among alpha's 14?"
---
HOST (cc Lead, Exec):

You asked me to check Draft 2's provider list against what the LLM client falls back across.

**It matches, and it covers more than the client can spend.**
- `_FALLBACK_ORDER` is anthropic, gemini, openai (`services/llm/clients.py` L53).
- Only anthropic and openai can actually spend (`PER_REQUEST_CLIENT_PROVIDERS`, `request_key.py` L123).
- Gemini has no spend path: `_gemini_complete` always refuses. Keeping it in the list is harmless.

**What Draft 2 can and can't mean.**
- Since 30ab8bf326 (#1812 steps 5 and 6, committed 2026-09-21 07:08 PT), every LLM spend is `request_spend_key(provider)`. That is the key bound for this request: the header, or the user's own `user_api_keys` row (`resolve_request_api_key`). Anything else is refused.
- No spend path reads the keychain's default slot. `LLMConfigService.get_api_key` steps 1 and 2 still read it, but only for availability and validation, not to serve a turn.
- So on today's build, an account with no key of its own is refused, never served on a global entry. Draft 1 present, plus Draft 2 nonzero, means "possibly served" only for conversations from before #1812 reached alpha.
- **Suggestion:** add `AND c.created_at < '2026-09-21 14:08:00+00'` (`ConversationDB.created_at`, timestamptz, `models.py` near L1733). That is the commit time, a lower bound on when the fix reached alpha. If you know the first alpha deploy that carried 30ab8bf326, use that time instead. Without the bound, the count also includes accounts that were simply refused, which over-reads it further.
- Before 09-21, the fallback was the designated-operator binding, which was deliberate. Whether a global keychain entry was ever what that binding read is for Lead or me to trace if Draft 1 comes back present. It doesn't need to block the read.

**Notion (`notion_api_key` in Draft 1).**
- `KeychainService.get_api_key` never falls back from a scoped name to the unscoped one (`_get_key_name`, L578–591).
- Notion's resolver reads env `NOTION_API_KEY`, then `PIPER.user.md`, then the user-scoped keychain entry (`notion/config_service.py` L183–192). You confirmed on 10-23 that `NOTION_API_KEY` isn't set on alpha.
- So a global Notion entry is unreachable by any user read on alpha, now that the wizard routes are refused. If present, it's hygiene.

**One names-only question, from your 10-23 list of alpha's 14 Fly secrets (no new command):** is `SLACK_USER_TOKEN` among them?
- `SlackConfigService._load_config` lets env `SLACK_BOT_TOKEN` and `SLACK_USER_TOKEN` override every user's own Slack token.
- You confirmed that `SLACK_BOT_TOKEN` isn't set. `SLACK_USER_TOKEN` wasn't one of the eight names I asked about.
- If it's set, every user's mentions read would run on that one account's token, a Class 2 shape. If not, it's a dev-only path, and Lead gates it to local installs when next in the file.

Verified how: read `clients.py` L53, L355–432 and `_gemini_complete`; `request_key.py` L119–123 and L369–420; `llm_config_service.py` L317–380; `keychain_service.py` L428–470 and L578–591; `notion/config_service.py` L176–215; and `slack/config_service.py` L189–262 on main. `git log --grep=1812` for 30ab8bf326. Layer: source, nothing run against alpha. Denominator: 3 of 3 fallback providers, the 1 Notion resolver, the 2 Slack env layers.

-- Arch
