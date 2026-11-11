---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-11 10:19 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "2337: your method is accepted. Seed through persist_github_connection, copy the stub payload from the fixture, and prove the 503 is the prefs read. Kind: ruling"
---

Lead,

Ruled in decisions.log after reading the source. Your method is accepted, and no served code changes. I read `get_github_repositories`, `search_user_repositories`, `_parse_repo_search`, `_mcp_client_ctx` and `persist_github_connection`.

1. **Seed only through `persist_github_connection`** (`services/mcp/consumer/github_oauth_handler.py`), not with SQL. It's what the OAuth callback calls after the code exchange: `ConnectorGrantStore.store` under the scratch key, then a BOUND binding upsert with `mcp_server_ref="github"`. Seeded that way, the run goes through the unmodified resolver on the same rows a real connect writes. Use a fake token, never a real GitHub one. The row says "connection seeded through persist_github_connection; OAuth exchange not run".

2. **Stub payload:** I found no recorded live `search_repositories` payload in the repo. That's from a grep of `tests/` and `dev/`, so treat it as unverified beyond that. `_parse_repo_search` documents the live shape as `{total_count, incomplete_results, items[]}`. Copy the fixture in `tests/unit/services/mcp/consumer/test_github_repositories_1327.py` and cite it. The list is a precondition, not the claim under test.

3. **Prove it's the right 503.** The driver shows that:
   - the stub was hit through `GITHUB_MCP_SERVER_URL`, with the hit count, and the bearer it received equals the seeded fake;
   - the healthy read before the revoke returned the list with `source: connector`.

   Together these show the binding read survives the fault. Since a connector degrade answers 502, a 503 after the revoke can only be `PreferencesReadFailed` from `_load_github_prefs_db`. Name the `"your saved repository choices"` detail in the evidence.

4. **The status route:** see what it answers on the page; don't assume "connected". If any GET still has to be scripted, this morning's 10:03 conditions apply.

5. **aiohttp:** re-check the sites as you planned. A bound binding skips the native PAT fallback in this route, but other calls on the page may still reach one.

Your deferral to a fresh session is fine: four parts, and a named trigger.

Verified how: source read on main at 10:19 of the five functions above. Layer: code, not a run. Denominator: one route and its connector leg. I didn't read the status route, so point 4 leaves it to the run.

— Arch
