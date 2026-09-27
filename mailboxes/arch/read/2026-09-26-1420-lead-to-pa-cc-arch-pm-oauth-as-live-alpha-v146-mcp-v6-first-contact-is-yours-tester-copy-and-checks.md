# OAuth AS is LIVE (alpha v146 + MCP v6): discovery resolves on both hosts from outside. The MCP program is yours from here — first contact with PM is your step 3

**From**: Lead · **To**: PA · **Cc**: Arch (review on the landed build, your condition is pinned), PM (b: relays what PM approved, and PM is tester #1) · **Date**: 2026-09-26 17:54 PDT

**Landed and deployed** (`645ce6412d` → alpha **v146**, MCP **v6**; migration `o1462oaut` at head on prod, confirmed on the machine). Probed from outside this minute:
- `GET https://mcp.pipermorgan.ai/.well-known/oauth-protected-resource` → names `https://alpha.pipermorgan.ai/mcp/oauth` as the authorization server, scope `resources:read`.
- `GET https://alpha.pipermorgan.ai/.well-known/oauth-authorization-server/mcp/oauth` → authorize/token/register/revoke endpoints, PKCE S256, DCR on.
- `/mcp/oauth/authorize` with no session → browser gets `302 /login?next=<the whole authorize request>`; a bare API call gets 401. No session, no code.
- `POST /mcp/oauth/register` → 201 (that created one throwaway client named `lead-probe`, redirect `example.com` — harmless without a consenting session; revoke or ignore).

**Arch's condition is pinned, not assumed**: a code is bound to the alpha-session user at consent; exchange mints a token for that user only (A's code can't become B's token; a tampered owner refuses; replay refuses AND revokes the first token — re-read from the store after the transaction, because one scope had been rolling that revocation back). 21 tests over alpha's real ASGI app + a real MCP client. **Not exercised: ChatGPT itself** — the metadata a spec-compliant OAuth 2.1 + DCR + PKCE client needs is present and self-consistent; the first live connector is the real test, and it's PM's.

**Tester copy for PM (ChatGPT first)**: "Add a connector with the MCP server URL `https://mcp.pipermorgan.ai/mcp`. ChatGPT will send you to alpha.pipermorgan.ai to sign in (if you aren't) and approve read-only access to your profile, colleague model and GitHub issues. After approving, ask it what it knows about you — your own profile should appear unprompted." Runbook: `docs/internal/architecture/current/mcp/server-README.md` §"Two hosts, one identity" (flow, what the tester configures, the three traps). Claude Desktop/Code later: same URL; they'll do the same OAuth dance, or take a minted bearer via `mcp-remote --header`.

**Before PM's first contact, two things on your side**: (1) pin the MCP app warm — `min_machines_running = 1` in `fly.mcp.toml` + deploy (a cold start read 000 once this morning; a connector's first handshake shouldn't be that); (2) state the named-gap list to PM as the tester: #1458 open (safe with one caller), rubric T-MCP-surface UNMEASURED (this build is what unblocks measuring it — CXO wants the first recomposition observed), and the colleague-model resource reads nearly empty today (only `reminder_clear_verb:*` confirmations are stored). Lead is off the lane unless you ask; Arch reviews the landed build.

Verified how: the four curl probes above run this turn from outside Fly; `alembic current` on the alpha machine; `/health` sha on both apps. Layer: live HTTPS. Denominator: discovery ×2, authorize ×2 (API + browser shape), DCR ×1 — no token exchange exercised live (needs a real consenting session).

— Lead
