---
from: lead
to: pa, arch, ppm, cxo
cc: exec, cio
date: 2026-11-01 07:38 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2242 (a) on main (cd0c489354): the allowlist; PA, the MCP half ships on deploy-mcp.sh and the served checks are yours; the first `mcp_allow.py add` is xian's"
---

PA, Arch, PPM, CXO (cc Exec, CIO),

## What landed (commit `9e0b7edd53`, on main at `cd0c489354`)

Arch's mechanism, built as ruled (#2242 comments 6544299487 and 6545549190):
- **One predicate, one source.** `services/mcp/server/allowlist.py:may_connect_mcp(user_id)` reads the reserved key `mcp_connect_allowed` in `users.preferences`. Only JSON `true` lists an account; `"true"`, `1`, a missing key, a missing row or a failed read all refuse (logged `mcp_allowlist_refused` with a reason).
- **Three gate points, failing closed.** (1) The consent step: `web/routers/mcp_oauth.py` shows the refusal line in place of the form (403, no hidden fields, no code), on GET and POST, and `PiperMCPOAuthProvider.authorize()` refuses independently, so a forged POST mints nothing. (2) The refresh grant: `invalid_grant` after the presented token is rotated, so a removed account cannot renew. (3) `MCPTokenVerifier.verify_token`: `None` for a valid token whose owner is not listed, the same as revoked; a removal bites on the next request; operator-minted tokens are covered.
- **Store conditions.** The key is stripped before `user_context_service` merges preferences (pin: a listed and an unlisted account with no other preferences get identical `UserContext`, and the key never rides into `UserContext.preferences`). `scripts/mcp_allow.py` is the one writer (`add` / `remove` / `list`; `--user-email` or `--user-id`; dry-run by default, `--apply` to write; atomic JSONB `||` and `-`, never a read-modify-write; `add` re-reads and prints the list). `tests/test_architecture_enforcement.py::TestMcpAllowlistSingleWriter2242` holds the literal to `allowlist.py` and write shapes to the script.
- **The words:** `MCP_NOT_OFFERED_LINE = "The Claude connector isn't part of this beta yet."` is the issue's draft. **CXO:** it is one constant in `mcp_oauth.py`; reword it and I change the string and its pin.

Not changed: the code→token exchange (a code lives 10 minutes and the verifier closes the token), the connected-apps page, PDR-005 (PPM's line).

## Rollout, in this order

1. **Nothing is listed yet, so the moment either half is served, every account is refused, including xian's.** The first write is xian's, on the production database (no agent seat reads or writes it):
   ```
   python scripts/mcp_allow.py add --user-email <xian's account email>            # dry-run, prints the target DB and the current list
   python scripts/mcp_allow.py add --user-email <xian's account email> --apply
   python scripts/mcp_allow.py list
   ```
   Run from the app's environment the way `mint_mcp_token.py` is (`scripts/mint_mcp_token.sh` is the `fly ssh console` idiom). Then the cohort's test accounts the same way. **Exec:** that is the ask for xian, with the account list from PPM/PA.
2. **PA:** the MCP half (`identity.py` + `allowlist.py`) ships on your `scripts/deploy-mcp.sh` once main's Tests run on `cd0c489354` is green AND step 1 has run (or in the other order, if xian prefers a dark connector for the gap; the closed direction is the safe one). The web half (consent and refresh) rides the next promotion.
3. **Served checks (PA, the issue's acceptance lines):** a non-listed signed-in beta test account gets the line on the consent page and no token is minted; a token already held by a non-listed account is refused by the MCP app on its next call (after the MCP deploy); a listed account (xian's) connects as today. Then rows 2 and 3 after the promotion, as Arch's point 3 says.

## Verified how

Full landing set on tree `9e0b7edd53`: enforcement + ratchets 160 passed (156 + the new class); `tests/unit` whole 16,126 passed / 0 failed; the eight CI dirs 565/0; integration 639 passed / 15 failed = the known 15, 0 new (the new Postgres test is among the passes); security 156/4; ruff clean; mypy 24 codes at ceiling (total 1090); literal census 89 (07:17–07:27). Unit pins: `test_mcp_allowlist_2242.py` (49: predicate, strip, verifier, provider authorize, refresh, consent route GET/POST/listed, context unchanged, script shapes and SQL) plus the enforcement class (4); the whole `tests/unit/services/mcp/server/` directory and the connections route tests, 239 passed together. Integration: `tests/integration/test_mcp_allowlist_2242.py` runs the real read on Postgres (listed true; `"true"` false; absent false; no row false). Layer: unit, seam (alpha's real app over an in-memory store) and the dev database; nothing served. Not run by me: anything against alpha, beta or the MCP app.

— Lead
