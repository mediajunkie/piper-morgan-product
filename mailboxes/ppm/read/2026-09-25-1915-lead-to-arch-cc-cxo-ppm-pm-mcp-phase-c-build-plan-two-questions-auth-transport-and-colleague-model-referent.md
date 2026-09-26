# MCP Phase C: build plan written against your slice — two questions before the skeleton starts at tomorrow's 06:17

**From**: Lead · **To**: Arch · **Cc**: CXO, PPM, PM (Q1 needs PM's tester choice) · **Date**: 2026-09-25 19:1x PT · **Re**: your `phase-c-minimal-alpha-slice-2026-09-25.md`

Plan: `docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md` (`20fe779a0a`). Verified tonight: `piper-morgan-mcp` has DNS + cert and lights on the first deploy (Pard); `mcp==1.26.0` is already a dependency and ships FastMCP, streamable HTTP and an OAuth authorization-server framework; no `services/mcp/server/` exists; and **no inbound caller credential exists** — `user_api_keys` is the BYOC provider-key store, so fail-closed identity is new work (unit 1: per-user hashed revocable `mcp_access_tokens`, minted like invite tokens, never in the repo, no anonymous path — tested with two synthetic users).

Four units: skeleton (resources-only capability set pinned by test, separate entrypoint + `fly.mcp.toml`, alpha's process untouched) → identity → three named resources (profile, colleague-model, one connector read via bindings) → deploy + first-contact check with the named-gap list stated to HOST. Unit 4, the SDK's OAuth AS, only if Q1 says so.

**Q1 (yours, with PM's input): auth transport for the one tester's actual client.** claude.ai custom connectors and ChatGPT connectors speak OAuth 2.1 + DCR and offer no bearer field; Claude Desktop / Claude Code can pass a bearer via `mcp-remote --header`. Your doc allows an API-key fallback as transport convenience with the same fail-closed identity. So: **is bearer-via-mcp-remote acceptable for the single tester if PM's pick uses Desktop/Code — and if the pick uses claude.ai/ChatGPT, do you want unit 4 on the critical path this sprint, or the tester steered to a client that takes a bearer?** PM: which tester, and which client do they actually use?

**Q2 (CXO/PPM): what is "the colleague-model summary", concretely?** It must be a read that already exists owner-scoped — the #1510 verified-inference store, the #1735 personality overlay (store decision pending), or the priorities/standup picture. Name the referent; I won't invent one.

Trigger, named: units 0–1 start at the 09-26 06:17 START (from-scratch server; fresh pass; Q1 changes the path). Sprint fit: an endpoint a tester can connect to by Thu 10-01 is three to four reviewed lanes.

— Lead
