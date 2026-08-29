# Leg C4 — Backend-Owned vs. Host-Mediated Integrations: the 2026 Evidence (vocabulary-blind)

*Filed verbatim-condensed 2026-08-29. Researcher had no project context; question stated in
industry-generic terms. Source-typing: [V] vendor, [P] practitioner, [A] aggregator, flagged
throughout. This leg directly feeds the review's first live test case.*

## The structural finding that reframes the whole question

**The two patterns are not substitutes — they can't reach each other's territory.**

1. **Host-mediated has no backend channel.** On both Claude and ChatGPT, the user's connectors
   surface ONLY inside the model's context during a live turn. Nothing pipes connector data to your
   servers; the only "relay" is the model deciding to pass data as tool arguments — token-expensive,
   unreliable, against every vendor's design grain. **No vendor has shipped a primitive that pipes a
   user's host connector into an app's backend**, and three vendors' 2025-26 roadmaps show no one
   building it. So anything the backend needs HEADLESS (webhooks, background sync, acting under app
   identity, acting while the user is away) is backend-owned by necessity.
2. **Backend-owned for commodity third-party services is being competed away.** Hosts ship and
   maintain hundreds of first-party connectors (Claude directory: 200→414+ in 10 months), enterprise
   admins govern them centrally, Enterprise-Managed Authorization (stable Jun 2026) provisions them
   zero-touch via Okta — and Claude's directory would REJECT your wrapper of someone else's API
   anyway ("you own the API, domain, and resources your connector touches" is a submission
   requirement).
3. **Your own product's surface is non-negotiably backend-owned**: one remote, stateless, OAuth-2.1
   MCP server serving Claude and ChatGPT (and increasingly Gemini) identically, with skills/MCP Apps
   layered for behavior and UI.

## How real products choose (evidence)

- Every ChatGPT DevDay-2025 launch app (Zillow, Spotify, Canva, Coursera, Booking, Expedia) is
  backend-owned: user links their account to the APP's auth server; the host forwards the bearer
  token. Even the widget iframe can't see the token.
- Sentry: hosted remote MCP with dual-OAuth architecture; rejected user-created API tokens.
- Same-server-both-hosts is proven cheap: one backend-owned server serves Claude and ChatGPT
  identically, only setup UX differs (Meta Ads MCP; Willison's TIL).
- Host-mediated ships as a SKILLS pattern, not a data channel: "connectors give Claude access,
  skills tell Claude what to do with that access." Anthropic's own skills-repo feature requires the
  GitHub connector enabled — first-party host-mediation.
- Hybrids are mostly auth-layer hybrids: OpenAI's API-level connectors (host-maintained code,
  developer-held grant); Composio/Nango as the "backend-owned but bought" quadrant; gateway pattern
  for multi-server estates.

## Costs and buys (compressed)

- **Auth**: backend-owned = running an OAuth 2.1 resource-server surface (spec 2025-06-18: RFC
  9728/8707). Real but commoditizing: one solo dev shipped ELEVEN OAuth-backed MCP servers in a
  week off a shared library; Stytch/WorkOS/Auth0 sell it off-the-shelf. Host-mediated = ~zero auth
  code but you get NO token at all.
- **Scoping**: host-mediated inherits the user's actual per-service permissions, enforced by the
  service. Backend-owned makes YOU the scoper — and the field's failure data is ugly (~40% of
  measured remote MCP servers with no auth; OAuth-pitfall account takeovers).
- **Context economics**: host-mediated flows through the model's context (vendors document
  connectors as token-intensive; measured LLM sampling of connected data: ~0.5–5%). Backend-owned
  pre-filters before anything hits the window.
- **Freshness/headless**: host connectors exist only inside a chat turn — no webhooks, no
  background sync, no acting-while-away. Backend-owned is the only headless pattern.
- **Multi-host consistency**: backend-owned = one server, identical on all hosts. Host-mediated =
  per-host catalogs/permission models you don't control.
- **Trust**: host-mediated = user granted the HOST, lower adoption bar, revocation is the host's
  problem. Backend-owned = you are a token vault and a breach target.

## Platform trajectory (spec line unambiguous)

2025-06-18 servers become standard OAuth resource servers → 2025-11-25 async Tasks + standardized
scopes + extensions → **2026-07-28 stateless core** (routable headers, "ordinary HTTP
infrastructure" can run MCP at scale) → EMA stable 2026-06-18 (zero-touch enterprise provisioning).
Simultaneously: first-party connector catalogs grow; Agent Skills adopted by 25+ platforms
including OpenAI within 12 weeks; MCP Apps (SEP-1865) co-authored by Anthropic AND OpenAI; Google
joined (managed remote MCP across Google Cloud, MCP in Gemini Enterprise).

**Read together**: vendors are building toward a DIVISION OF LABOR — hosts own commodity
third-party connectivity for their users; apps bring one backend-owned server for their own
product. Waiting for (or architecting around) a host-connector-to-backend relay channel is
unnecessary: nobody is building it.

## Practitioner dissents (kept honest)

"Skip MCP; give agents code/CLI" (Willison; Anthropic's own Nov-2025 code-execution-with-MCP
concession on tool-schema bloat) · "stateless MCP is just an API again" (HN/InfoQ debate;
Cloudflare's counter: that's the point) · security skeptics (40%-unauthenticated measurements) ·
adoption-number skeptics (registry counts are intent signals; 30–50% community-server install
failure rates) · auth-UX dissent favoring host mediation (per-user OAuth to every server was the
pain EMA fixed).

## The decision rule (researcher's closing, verbatim)

> **Hold the grant only where you must act without the user present.**
> Per integration: *does my backend need this service when no chat turn is open?*
> — **Yes** (background jobs, webhooks, writes under app identity, cross-user aggregation) →
>   backend-owned; BUY the auth/integration layer rather than build once N ≥ ~3.
> — **No** (the value is "reason over the user's own stuff, in the conversation") → delegate to the
>   host's connector and ship a skill that composes it; design the skill to degrade gracefully when
>   the connector is absent.
> — **Always** backend-owned: your app's own data and actions — that's your product surface, and
>   one MCP server covers every host.

For a small team this typically collapses N integrations to: ONE server you operate (your own),
ZERO third-party grants held for chat-side reads, and a short list of genuinely headless
integrations where you pay a managed-auth vendor instead of an engineer.
