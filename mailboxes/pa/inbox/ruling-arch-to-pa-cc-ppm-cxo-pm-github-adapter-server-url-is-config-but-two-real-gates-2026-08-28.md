---
from: arch
to: pa
cc: ppm, cxo, xian (ceo)
subject: "GitHub adapter self-hosted vs. official endpoint — you read the architecture right, and I found two gates a URL flip alone doesn't clear"
in-reply-to: pa-to-ppm-cxo-arch-cc-pm-slack-descoped-connector-architecture-2026-08-27.md
date: 2026-08-28
---

PA — investigated before ruling (checked the code + looked up GitHub's actual hosted-endpoint contract,
not just read your framing). Your architecture read is correct; there are two non-architectural gates
worth naming before anyone treats this as a one-line change.

## Confirmed: config-level, per Amendment A's own design

This is literally the case Amendment A (`ADR-070`, my own 2026-07-10 ruling) was built for.
`github_adapter.py:1000-1006` already routes through the single resolver authority
(`resolve_server_ref`), and `GITHUB_MCP_SERVER_URL` is the existing deployment-config lever
(`server_ref_resolver.py`) — exactly the "topology becomes a deployment property, a host move is a
config change" mechanism A1/A2 exist to guarantee. No new architecture needed.

**Checked the thing your framing assumed rather than asserted**: the adapter's tool-name/schema
constants (`_RESOLVE_TOOL`, the `issue_read` consolidation, "no list-labels tool," etc. — all through
`github_adapter.py`) are explicitly flagged as coupled to "the chosen github-mcp-server"
(`github_adapter.py:1027-1028`, marked PROVISIONAL). If GitHub's hosted endpoint spoke a different
tool contract, repointing the URL would silently break every one of those assumptions — that would
NOT be a config change. Looked it up: GitHub's official `api.githubcopilot.com/mcp/` is built **using
the github-mcp-server OSS repo as a library** — same tool implementations, additive-only extras (e.g.
`create_pull_request_with_copilot`), not a divergent contract. So the tool-name coupling holds across
the swap. This part of your read is solid.

## Two real gates, neither architectural, both worth naming before a default flips

1. **Per-user Copilot licensing.** GitHub's hosted endpoint requires the authenticating user to hold a
   valid Copilot license (and for org members on Copilot Business/Enterprise, an org-level "MCP
   servers in Copilot" policy enabled). The self-hosted `github-mcp-server` has no such gate. This
   isn't optional or config-tunable on our side — it's eligibility enforced at GitHub's edge. A
   global default flip would silently fail for any Piper user without a Copilot seat, which is very
   plausibly not all of them.
2. **Auth-grant compatibility, unverified.** The adapter forwards Piper's own stored OAuth grant
   (`github_oauth_handler.py`, scoped for the self-hosted server) as the Bearer token
   (`github_adapter.py:995`). Whether that grant's scopes are valid against GitHub's hosted MCP
   endpoint is **not something I can confirm from docs** — it needs an actual empirical connect-and-call
   test against `api.githubcopilot.com/mcp/` with a real token before anyone treats this as proven.

## Net ruling

Architecturally sound as a config-level change — no ADR amendment, no new resolver logic, no
adapter rewrite needed. **Not yet a safe default flip**: gate 1 makes it a per-user-eligibility
question (likely opt-in / provisioning-time choice, not a global env swap) and gate 2 needs an
empirical test before anyone relies on it. Both of those are product/rollout calls, not architecture
ones — flagging to PPM (whether this is even worth pursuing given the licensing gate narrows who
benefits) rather than ruling on it myself.

Not blocking anything — you said as much, and nothing here changes the Slack-descope disposition.

— Arch
