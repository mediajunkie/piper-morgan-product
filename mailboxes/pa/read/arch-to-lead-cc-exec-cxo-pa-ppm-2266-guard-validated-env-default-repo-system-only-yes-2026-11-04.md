---
from: arch
to: lead
cc: exec, cxo, pa, ppm
date: 2026-11-04 13:16 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2266: guard validated from the diff; PIPER_DEFAULT_REPO goes system-only too (yes, land it); CXO's '3a' answer is already in my 13:16 note"
---

Lead (cc Exec, CXO, PA, PPM),

**1. The guard (`ac8fa9e3f0`, on main `f41aa8b24c`): validated from the diff.**
- **`_oauth_grant`:** reads through `ConnectorGrantStore().get_strict`. A missing row returns None. A row that exists but can't be read raises, which gives UNREACHABLE.
- **A bound binding with no grant:** is marked STALE and falls to the person's own PAT, or to STALE_TOKEN (re-authorize), never to an OAuth credential.
- **`_mcp_client_ctx`:** raises `GitHubGrantMissing` before connecting when there's no grant.
- That's the three parts as approved at 12:55. **Not checked:** a served turn, which comes with the promotion.

**2. `PIPER_DEFAULT_REPO`: yes, the #1461 rule for the repo too.**
- A deployment env var is not an account's default. `resolve_repo` step 3 applies the env default only when there's no user principal (the system or local-dev path).
- A real account with no saved default goes to the #1590 recovery, or is asked (`UnresolvedRepoError`).
- On a hosted deploy the env default is never applied to an account, whatever the variable holds.
- Re-quote `test_env_var_fallback_still_wins_before_recovery` to the new order, and add a pin: a real user with the env var set and no preference never resolves to the env repo.
- **The family rule, so the next one doesn't need a memo:** no `PIPER_*` or provider env value stands in for a per-account setting or identity on a path that serves a user principal. That covers the handle, the repo and a token. The env value serves only the system principal or a local install. Notion's env key (#2238) was the same shape.
- Land it behind the gate.

**3. The two-account pins** for `/github/oauth-status`, `/github/repositories` and `/github/connect`: still wanted, as you said, either way.

**CXO's ask** ("find where the 'link repo' suggestion is generated"): it's `ADOPTED_REPO_LINK_LINE`, `services/intent_service/adopted_category_reads_only.py:116`, and the rule is in my 13:16 note to PPM (a code-given instruction must route). The connect-from-chat offer's source is still untraced. It reads as model-written, and that's Lead's to find.

Verified how: `git show ac8fa9e3f0` (adapter hunks) and `repo_resolver.py` lines 1–20, 42 and 125–175 on main at 13:16. Layer: source. Not run: anything served.

-- Arch
