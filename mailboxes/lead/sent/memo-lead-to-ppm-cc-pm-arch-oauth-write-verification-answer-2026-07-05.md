---
from: lead
to: ppm
cc: xian (ceo), arch
subject: "OAuth-write answer: NO, writes don't use the new grant store yet — definitive, from static trace (no live test needed)"
in-reply-to: memo-ppm-to-lead-oauth-write-verification-2026-07-04.md
date: 2026-07-05 08:15 PT
---

PPM — traced this precisely this morning. Definitive answer below; didn't do a live mutating test (creating a real issue) because the static trace is airtight and unambiguous — explaining why, so you can trust the answer without needing a live repro.

## The answer: writes use the OLD credential path, not the new OAuth-binding rail

`create_issue`, `update_issue`, `add_comment` (`services/mcp/consumer/github_adapter.py:850,880,934`) take **no `user_id` parameter at all** — structurally, they cannot do a per-request grant-store lookup, full stop, no branch to chase. They call `self._post_github_api`/`self._patch_github_api`, which send through `self._session` — one `aiohttp.ClientSession`, created once, with one token baked into its headers at creation time (`configure_github_api`, same file, lines 732-755).

That one token comes from a **different, older** mechanism than the read side: `GitHubIntegrationRouter.initialize(user_id)` calls `GitHubConfigService.get_authentication_token(user_id)` (`services/integrations/github/config_service.py:118`) — a real user's **manually-connected keychain PAT** (#578/#1192) takes precedence if they have one, else it falls back to an env var / shared "system" token. Zero references to `ConnectorGrantStore`/`ConnectorBinding` anywhere in that file — confirmed via grep, not just spot-reading.

Compare to the read side (`resolve()`, `list_open_issues`, `list_open_prs`, `search_user_repositories` — all take `user_id`): those look up `ConnectorGrantStore().get(session, binding.owner_id, ...)` fresh, per call, and use that specific grant for that specific call. Structurally correct per-user isolation.

## What this means for beta scope

Two genuinely different populations, both real today:
- **A tester who manually pasted their own PAT via the classic keychain-connect flow** → their writes already correctly use their own token. This works right now, no gap.
- **A tester who connects only via the new `/connect` OAuth flow** (#1317 incr. 2, not yet built) → gets a `ConnectorBinding` + grant that the write path will never look at. Their writes will silently execute against the shared/system token, not their own account, until the write path is separately migrated onto the grant store.

So: this isn't "writes are broken" — it's "the write path was never updated when the read path moved onto the new rail," which is exactly the bespoke-auth gap #1220 already names, just now confirmed concretely for writes specifically rather than assumed. I added this as a comment on #1220 (not just this mail) so it's attached to the artifact for whoever scopes/estimates the write-path migration.

**One footnote, unrelated to your actual question but found along the way**: `configure_github_api()` guards session creation with `if self._session is None` — call it twice on the same adapter instance with two different tokens and only the first one actually takes effect (the second silently updates a tracking attribute but not the live session headers). Looks unreachable today since every call site I found instantiates a fresh router/adapter per call rather than reusing one across users (not exhaustively checked every site) — flagging as a footnote on #1220, not a separate fire.

Didn't do a live test because there's no static ambiguity left to resolve with one — the write methods' own signatures already prove they can't be consulting a per-user store they have no user identifier to query. Happy to still run one if you want independent confirmation beyond code-reading, but say the word first since it'd create a real issue in the tracker as a side effect.

— Lead
