---
from: arch
to: xian (ceo)
cc: lead, exec, pa
subject: Re: github-mcp-server provisioning — Arch ruling: A (hosted-OAuth), on architecture-integrity grounds; one business checkpoint is yours
date: 2026-06-27 08:30 PT
---

PM — Lead's research is solid and the recommendation is right. **Arch ruling: A (hosted-OAuth).** This one isn't a close preference call — it's the architecture-integrity mandate, so I'm ruling it rather than presenting it as a toss-up, and handing you the one dimension that's genuinely yours (a business checkpoint, not an architecture question).

## Why A is the architectural answer (not just the nicer one)

**B re-introduces the exact thing ADR-070 D3 designed out.** D3 is ratified: *the MCP server owns OAuth/tokens; Piper stores per-user bindings, never raw credentials.* The whole reason WS-2/#1229 collapsed to "bindings, not credentials" was to stop holding raw tokens. Option B makes Piper hold each user's **PAT** (even #358-encrypted) to inject into a subprocess — that's raw-token custody, the precise pattern the architecture moved away from. **A realizes D3** (connect() orchestrates the OAuth redirect; the callback stores a binding; no token ever touches us).

**It also doesn't generalize, even for single-user-now.** Per the same principle I used for the #1232 Phase-1 ruling — build single-user-now but *multi-tenant-ready*, no re-stamp later — A is the pattern that scales (OAuth+binding works identically for 1 user or 1000). B's PAT-custody is a single-user dev affordance that needs replacing the moment a second human appears. We shouldn't build the non-generalizing pattern when the generalizing one is nearly the same cost.

**The cost of A is near-zero marginal.** It needs streamable-HTTP transport on `MCPClient` — but Lead is building that regardless (correctly; see below), and it's independently valuable. So A's "extra cost" is a transport increment we want anyway.

## Affirming the transport direction (substrate-level, beyond GitHub)

Lead's plan to give `MCPClient` **both stdio and streamable-HTTP** transports is the correct substrate call regardless of the GitHub decision — the MCP ecosystem uses both (local servers = stdio; hosted servers = HTTP), and ADR-070's connector substrate must not be transport-locked. Every hosted MCP server we'll consume next (Notion, Slack, Linear…) is HTTP. So: build the HTTP transport now, ratified as a general direction, not a GitHub-specific tax.

## The one dimension that's YOURS, not mine (the business checkpoint)

A takes a hosted external dependency on GitHub's endpoint (`api.githubcopilot.com/mcp/`). The *architecture* says A; the *business gate* is yours: **any cost / licensing (does it require Copilot seats?) / data-policy constraint** on that endpoint. I can't rule that — it's a product/business call.

**Decision tree**: A is the answer **unless** you hit a hard blocker on that checkpoint. If you do, the fallback is **not** "B for production" — it's "B as an explicitly-temporary, single-user dev affordance (#358-encrypted PAT), tracked as non-generalizing tech debt, while we resolve the hosted-endpoint constraint." Production multi-user is A either way, because D3.

## Net
- **Arch ruling: A.** Lead: proceed wiring the OAuth-callback binding-creation against the hosted endpoint once PM clears the business checkpoint; build the HTTP transport now regardless (ratified).
- **PM: one yes/no** — any cost/licensing/data-policy blocker on `api.githubcopilot.com`? If no → A is go. If yes → tell me the constraint and I'll rule the interim.

decisions.log recorded. This composes with ADR-070 (A realizes D3/D6-Tier-1) + the #1220 transport work.

— Arch
