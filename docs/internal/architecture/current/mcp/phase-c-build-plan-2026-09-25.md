# MCP Phase C — Lead's build plan for Arch's minimal alpha slice

**Lead, 2026-09-25 18:4x PT.** Companion to Arch's scope doc
(`phase-c-minimal-alpha-slice-2026-09-25.md`, same directory) — that doc rules *what*; this one
says *how*, in units, with the one question the units can't answer alone. Sprint goal (PM,
2026-09-25): "getting the mcp to alpha testing."

## Verified state (this fire, not assumed)
- **Hosting**: Fly app `piper-morgan-mcp` exists with `mcp.pipermorgan.ai` DNS + issued cert
  (Pard, Phase B, 09-24). Fly serves no TLS for a machine-less app, so the endpoint reads as dark
  until the first `fly deploy` — expected, not broken. (`fly apps list` → `pending`; `curl` → 000.)
- **SDK**: `mcp==1.26.0` is already in `requirements.txt`; `mcp.server.fastmcp`,
  `mcp.server.streamable_http`, `mcp.server.auth` (+ `.provider`, `.settings`) all import from
  the venv. No new dependency.
- **Code**: `services/mcp/` has `consumer/` (Piper as MCP client) and `protocol/` — **no
  `server/`**. From scratch, as Arch said.
- **Identity**: no caller-auth token exists. `user_api_keys` is the BYOC *provider-key* store
  (openai/anthropic/github references), not an inbound credential. Session auth is JWT for the
  web app. **A fail-closed MCP caller token is new work** (unit 1).
- **Deploy shape**: one Docker image (`Dockerfile` CMD → `python main.py`). The MCP endpoint
  should be a **separate process/entrypoint on the same image** (`main_mcp.py`, its own
  `fly.mcp.toml` pointing at app `piper-morgan-mcp`) — alpha's process is untouched, the DB and
  bindings are shared, and a bad MCP deploy can't take alpha down.

## Units (each one reviewed change; none touches alpha's process)
0. **Skeleton server** — `services/mcp/server/app.py`: FastMCP over streamable HTTP, `initialize`
   handshake, capability set = **resources only** (assert no tools registered — a test pins the
   advertised capabilities), `/health` with git_sha like alpha's. `main_mcp.py` entrypoint;
   `fly.mcp.toml`. Deployable dark (no resources yet) — that alone lights the endpoint.
1. **Fail-closed identity** — `mcp_access_tokens` table (hashed at rest, per-user, revocable,
   minted by an operator script like `mint_prod_invite.sh`, delivered like an invite token: never
   in the repo). Bearer → user_id or **refuse**; there is no anonymous owner and no default path
   (the PDR's acceptance criterion, pinned by test: unresolvable identity reads nothing; a
   second caller's token cannot reach the first's rows — tested with two synthetic users even
   though only one real tester exists).
2. **Three named resources** — `piper://me/profile` (the user-context read:
   projects/priorities/organization, owner-scoped), `piper://me/colleague-model` (**needs a
   referent** — see Q2), `piper://me/github/issues` (one connector read via the binding store,
   logical keys per ADR-070 Amendment A, honest `ConnectRequired` when unbound). Every read
   goes through the same owner-scoping the chat surface uses; nothing new is queried.
3. **Deploy + first-contact check** — `fly deploy -c fly.mcp.toml -a piper-morgan-mcp`;
   `initialize` + `resources/list` + `resources/read` exercised from a real client with the
   tester's token; the named-gap list (#1458 open, rubric T-axis PENDING-PROBE) stated to
   whoever manages tester comms (HOST), per Arch's acceptance item 4.
4. **OAuth AS (SDK-provided) — only if the tester's client can't present a bearer** (Q1).

## Two questions (Arch Q1 tonight; CXO/PPM Q2)
- **Q1 — auth transport for THIS tester's client.** claude.ai's custom-connector UI and ChatGPT
  connectors speak OAuth 2.1 (+ dynamic client registration); a bare bearer header is not a
  field they offer. Claude Desktop and Claude Code CAN pass a bearer via `mcp-remote --header`
  (or Code's `--header`). So: if the named tester uses **Claude Desktop/Code**, unit 1's bearer
  token satisfies Arch's fail-closed condition this sprint and unit 4 waits; if they use
  **claude.ai or ChatGPT**, unit 4 (the SDK's OAuth provider backed by Piper's login + a consent
  page) is on the critical path and the sprint-week fit is tight. Arch's doc allows the API-key
  fallback "as transport convenience, not an identity exemption" — unit 1 is built to that
  standard either way. **Ask: which client, and is bearer-via-mcp-remote acceptable for the
  one tester?** (PM picks the tester; this is Arch's ruling on the transport.)
- **Q2 — what is "the colleague-model summary" concretely?** Candidates: the #1510
  verified-inference store, the personality overlay (#1735, store decision pending), or the
  standup/priorities picture. Whichever it is, it must be a read that already exists
  owner-scoped. CXO/PPM name the referent; I won't invent one.

## Trigger, named
The skeleton (unit 0) and identity (unit 1) start at the **2026-09-26 06:17 START** — a
from-scratch server's mount shape and identity path deserve a fresh pass, and Q1's answer
changes whether unit 4 is on the path. Not "no rush": the sprint goal is an endpoint a tester
can connect to by Thu 10-01, and units 0–3 are three to four Lead-reviewed lanes.
