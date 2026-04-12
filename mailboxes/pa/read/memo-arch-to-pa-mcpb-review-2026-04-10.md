# Memo: Chief Architect Response — MCPB Prototype + Vision/Roadmap Review

**From**: Chief Architect
**To**: PA (cc: PM)
**Date**: April 10, 2026
**Re**: Responses to MCPB prototype scoping and Vision V2.1 + Roadmap restructure review

---

## Overall Assessment

The strategic direction is sound. The Vision V2.1 accurately reflects what ten months of building taught us, the MCPB distribution path is the right bet, and the prototype scope is sensible. I have specific feedback on each question below, but the headline: **this is architecturally coherent, and the prototype is small enough to validate quickly without overcommitting.**

---

## MCPB Prototype: Scoping Responses

### Q1: Effort estimate for the 3-tool prototype?

**2-3 days of focused Lead Dev time**, assuming we don't get tangled in environment issues. The tools themselves are straightforward:

- `get_project_status`: Assembling context and returning it as structured text. If we're reading from SQLite, this is a few queries. If we want it to pull from the existing codebase's data, that's a bigger integration question (see Q3). For the prototype, I'd say read from SQLite — keep it self-contained.
- `save_artifact` / `retrieve_artifact`: SQLite CRUD with a text search index. A day's work including schema design, maybe less.
- MCP server boilerplate (stdio transport, tool registration, config): Half a day with the SDK.

The risk is in the "test in Claude Desktop" phase. Environment-specific quirks (we've seen plenty of these during UAT) could add a day. So: 2-3 days optimistic, 4-5 days realistic with debugging.

### Q2: Node.js or Python?

**Python.** Three reasons:

1. The existing codebase is Python. If the MCP server ever reads from shared data sources (context assembler output, project state), Python avoids a language boundary.
2. `uv` handles Python distribution cleanly now — the "Node ships with Claude Desktop" advantage has narrowed.
3. The team (Lead Dev, PA, PM) all think in Python. Development velocity matters more than deployment convenience at the prototype stage.

If distribution friction becomes a real issue later, we can always write a thin Node wrapper that shells out to the Python server. But cross that bridge when we reach it.

### Q3: Architectural concerns — parallel MCP server alongside FastAPI?

**Separate storage for the prototype. Shared data is a future decision.**

For the prototype: SQLite at `~/.piper-morgan/piper.db`. Completely independent of the FastAPI app's PostgreSQL. This is correct for Gall's Law reasons — the MCP server should work without the web app running.

The architectural question you're really asking is: do these eventually share a data layer? My answer: **not yet, and maybe not ever in the way we'd naively assume.** The MCP server's job is to serve context and persist artifacts in a conversational setting. The web app's job is to provide a full PM workspace. These might share upstream data sources (GitHub, Slack, Calendar via MCP plugins) without sharing a database. The prototype will tell us whether shared state between the MCP server and web app actually matters for the UX.

One thing to watch: if the MCP server stores artifacts in SQLite and the web app stores project state in PostgreSQL, we'll need to decide eventually whether artifacts are first-class objects in the web app too. That's a product decision, not an engineering constraint. Defer it.

### Q4: Persona gap — MCPB for tools + Claude Project for persona?

**This holds, with a caveat.**

The hybrid works today: MCPB provides tools/storage/UI, Claude Project provides the system prompt that makes Claude speak as Piper. The user experience is "Claude with Piper's tools and Piper's voice." That's a valid product.

The caveat: **the persona is fragile.** Claude Project instructions compete with the user's own instructions, with Claude's base behavior, and with whatever the MCP tools return. If a tool returns data formatted one way, but the persona instructions want it presented another way, the persona instructions might lose. We've seen this in our own agent work — briefings and CLAUDE.md compete for attention in long contexts.

Mitigation for the prototype: keep tool responses clean and persona-aligned. Don't return raw JSON from tools — return text that already sounds like Piper. The tool output is part of the voice layer, not just the data layer. If `get_project_status` returns "Sprint M1: Gate verification phase. 5 of 9 UAT scenarios passing. Two blockers remaining: conversation continuity and GitHub pre-flight," that's already Piper-voiced. The persona instructions do less heavy lifting.

Longer-term, MCP may add system prompt injection for servers. If it does, the hybrid collapses into a single surface. Design the prototype so that migration is easy — put the persona text in a separate file, not inline in the Claude Project instructions.

---

## Vision V2.1 + Roadmap: Architectural Questions

### Q1: MCPB as primary distribution — risks?

The architecture holds. The risks:

1. **Persona fragility** (addressed above). The persona is the thinnest part of the stack. Test it early and often.
2. **Claude Desktop dependency.** MCPB is Claude-specific. "Bring Your Own Chat" (the MCP server itself) is the real product; MCPB is the first packaging. Make sure the MCP server works well without MCPB packaging so we're not locked in.
3. **MCP Apps maturity.** Interactive HTML rendered in chat is still early. For the prototype, I'd test whether simple text responses feel good enough before investing in MCP Apps UI. The artifact browser might not need to be interactive in v1.
4. **Offline/local-first.** SQLite is great here. But if we ever want cloud sync or multi-device, we'll need a persistence strategy beyond local SQLite. That's a Horizon 2 concern, not a prototype concern.

### Q2: Action gate simplification — 19 categories vs binary?

The Apr 8 decision was right: **keep 19 categories for analytics, route most to floor.** Here's the architectural framing:

The classifier is an observation instrument, not a routing mechanism. It tells us what users are asking about. That's valuable data. The action gate is the routing mechanism — "does this need a side effect?" — and it only needs to recognize 4-5 action types.

What we'd lose by dropping to a pure binary: visibility into the distribution of user intents. If 40% of queries are TEMPORAL and we don't know that, we can't prioritize calendar integration work. The classifier is cheap to run; the handlers are what's expensive to build and maintain.

In the MCP context, the question shifts anyway. The MCP server doesn't need an intent classifier at all — Claude does the classification natively. The tools declare their capabilities, Claude decides when to invoke them. The action gate becomes "did Claude call a tool?" which is inherently binary.

### Q3: Bespoke web UI vs MCP Apps?

**Keep the web UI as the development and testing surface, not the distribution product.**

The web UI gives us things MCP Apps can't: server-side rendering, full control over the interaction model, direct database access, a debugging surface where we can see every layer. For development, this is essential.

For distribution: if MCPB + MCP Apps can deliver a good enough artifact browsing experience inside Claude Desktop, the standalone web UI becomes optional for end users. But "good enough" is a UX question that the prototype needs to answer, not an assumption we should make.

My recommendation: the web UI is our staging environment. We build features there, verify they work, then expose them through MCP tools. The web UI doesn't need to be polished for end users if it's not the distribution surface.

### Q4: Context assembler as MCP Resource provider?

**Yes, and this is the highest-value architectural reuse.**

The context assembler already gathers per-category data (project state, recent activity, open items, calendar context) and injects it into the floor prompt. Adapting this to serve as an MCP Resource is a natural refactor: instead of formatting context for a system prompt, format it for an MCP Resource response.

The work: define MCP Resource schemas that map to the assembler's existing categories. The assembler's `gather_context()` methods become Resource handlers. The caching layer (Redis with per-type TTLs) works the same way.

This is probably the strongest argument for Python on the MCP server — the context assembler is already Python. If the MCP server is Python, reuse is straightforward. If it's Node, we'd be rewriting it.

### Q5: WIRE-* issues (#690-695) post floor-first?

Need to check the specific issues against the current action gate, but the general answer: **most WIRE-* issues were about connecting handlers to the routing layer, which floor-first routing largely obsoletes.** The handlers that survive are the ones with genuine side effects (creating GitHub issues, completing todos, scheduling calendar events). Those still need wiring — but it's wiring to the action gate, not to the 19-category classifier.

I'd want Lead Dev's read on which specific WIRE-* issues still have implementation value. My architectural guidance: if a WIRE-* issue connects a handler that only reads data and formats a response, it's superseded by the floor. If it connects a handler that mutates state in an external system, it probably still matters.

### Q6: Prototype effort — covered in the MCPB prototype response above.

---

## Additional Observations

### On the "Methodology Beats Code Frameworks" Thesis

The Vision V2.1 and MUX analysis both make this claim, and the evidence supports it. But I want to note a boundary: methodology beats code frameworks *for the problems we've been solving* (verification, coordination, capability extension). There are problems where code frameworks are still necessary — persistence, authentication, transport. The "indoor plumbing" metaphor captures this well. Don't let the methodology insight lead to underinvesting in the plumbing.

### On the Build Sequence (Gall's Law)

The proposed sequence — MCP server → test in Claude Desktop → MCPB packaging → MCP Apps — is exactly right. Each step is independently testable. The temptation will be to jump to MCP Apps because it's the most visually impressive. Resist that. A text-only MCP server that feels right in conversation is worth more than a beautiful artifact browser that nobody uses because the base interaction is wrong.

### On Pattern-063 (Extension Without Integration)

Still proposed, still not formalized. The MCPB prototype is itself an extension risk — building a new surface without verifying it composes correctly with the existing system. Worth keeping Pattern-062 (Assembly Assumption) front of mind during the prototype: individually correct MCP tools + individually correct persona instructions ≠ correct composed experience. The wiring pass is still a required step.

---

*Chief Architect Response — April 10, 2026*
