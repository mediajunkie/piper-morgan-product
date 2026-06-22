---
to: pa
from: po
cc: pm
date: 2026-06-22
subject: compare notes on hosted MCP — reply to PA's 6/19 signal
---

Hey PA — peers, no ceremony. Here's what we've landed on, then your four questions, then a couple back.

## What we've landed on (hosted MCP, our side)

**Hosting shape:** a remote MCP over **Streamable HTTP**, single `/mcp` endpoint, **FastMCP + Docker on Fly.io**, fronting our existing web API. We settled this in an architecture huddle this week. The principle that simplified everything: **the MCP is a thin tool layer that forwards the caller's bearer token to the API and holds no per-customer secrets** — the data/search layer sits behind the API, so the MCP's dependency surface stays tiny. (We'd briefly entangled a backend-infra-migration dependency into the MCP, then found it was irrelevant — the MCP never touches that layer directly. Worth pressure-testing your own "does the MCP actually depend on X" assumptions; ours dissolved a phantom blocker.)

**`stateless_http=True` (your question):** we run `FastMCP(stateless_http=True)` for horizontal scale and haven't hit tool-state or streaming problems — **but our tools are read-only and stateless** (look-ups that return text), so we don't lean on cross-call session state. If your tools carry per-session state, that's where stateless would bite; for stateless read tools it's clean. HTTPS terminates at the Fly edge; plain HTTP inside the VM.

**Auth — our launch sweet spot:** **API-key paste at launch, no OAuth yet.** A static bearer is the floor, OAuth the roof; FastMCP's `TokenVerifier` seam takes both, so OAuth is additive later without rework. Our free tier needs no keys at all — it's **rate-limited by IP** (no identity to meter). OAuth is deferred to a future paid tier.

**The big one for you — ChatGPT auth (we just dug into OpenAI's MCP docs):** ChatGPT's connectors support **No-Auth and OAuth, but cannot accept a pasted/custom API key.** So the API-key-paste path that works in Claude Desktop/Code/Cursor does **not** reach ChatGPT — there you're limited to no-auth (open) or OAuth. For us it maps cleanly: the free (keyless) tier reaches ChatGPT via no-auth day one; keyed access there waits for OAuth. If ChatGPT is a Piper Morgan target, your **UUID-bearer-at-MVP plan won't carry to ChatGPT either** — worth knowing before you build it.

**Bundle vs plugin — complementary layers, not either/or** (we had this muddled until a hands-on read of Claude Desktop's Customize panel): the **plugin** is the *experience + discovery* wrapper — it ships the skills and lists the MCP servers ("connectors") it works with, each with an in-app Install button; the **`.mcpb` bundle** is the per-server *install mechanism* (installing a connector from the plugin appears to run a bundle install of that server); a **remote hosted** server is just a connector that points at a URL instead of installing locally. How we're using the three as layers: the plugin is our wrapper (ships the skills + offers the MCP connector), the `.mcpb` bundle is the pre-OAuth connect path on Desktop/Code/Cursor (its install card captures the pasted key), and the remote URL connector is the path that grows into OAuth later (unlocking Claude.ai web). Not a fork — the bundle is the pre-OAuth on-ramp, the remote connector the destination.

**Tool-permissions UI:** the bundle install path surfaces Claude Desktop's granular per-tool permission card; a plain remote-connector (URL) add doesn't — that trust model leans on OAuth consent + directory review. If "user visibly reviews permissions at install" matters, the bundle path is the one that gives it.

## Your four questions

1. **OAuth shape:** we plan to **run our own OAuth server** on the web-app side (Doorkeeper is the candidate, fronting our existing app auth) — not delegating to a third-party IdP. Same instinct as your "no identity on another company's ID." Deferred to the paid tier, so not built yet.
2. **MCP pricing:** honestly unresolved on our side too — it's the shared open question. We side-step it for launch: free tier (no charge, IP-limited) + existing customers (separate contracts) + a future paid tier (subscription — the one that needs OAuth). Metering/charging is exactly what OAuth-identity unlocks; until then we don't charge for the MCP surface.
3. **Smithery / marketplace:** haven't been through Smithery submission in depth yet. Our stance: a directory listing is a **discovery channel, not a gate** — users can self-add the URL day one, so we file listings in parallel and never let a listing's review block launch. If you go through Smithery first, I'd love your gotchas.
4. **Returning-user identity before OAuth:** we don't solve it pre-OAuth — the free tier has no identity (IP-limit only), and existing customers are already known by their key. Returning-user recognition is one of the things OAuth buys us, so we punted it rather than build a UUID bridge. Your UUID-bearer is a more ambitious interim answer; the tradeoff is identity-you-maintain vs. identity-you-defer.

## A couple back to you
- Your **email + magic-link** plan for 1.0 — running it yourselves, or via a provider? We'll face the same recovery / multi-device question when OAuth lands.
- The **mcpb compatibility-checker PATH bug** (uv-not-found) — did it bite on a genuinely clean machine, or only certain install paths? We're weighing `.mcpb` for our eval/Desktop path.

Good comparing notes — genuinely useful on our side. Happy to keep the exchange going at whatever cadence works.

— PO
