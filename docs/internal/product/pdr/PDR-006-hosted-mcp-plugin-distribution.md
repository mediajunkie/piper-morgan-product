# PDR-006: Hosted MCP Endpoint + Plugin Distribution Model

**Status**: Draft v0.1
**Date**: 2026-07-19
**Author**: PA (Piper Alpha) — on behalf of PM
**Stakeholders**: PM, Arch, CXO, PPM, Lead Dev
**Supersedes**: MCPB skunkworks POC (not a formal PDR — superseded informally)
**Extends**: PDR-005 (Bring Your Own Chat — Distribution Model, ratified Jun 5, 2026)

---

## Decision

Piper's primary distribution model for alpha/beta is:

1. **Hosted MCP endpoint** at `mcp.pipermorgan.ai` — a pure tool server; no server-side LLM calls
2. **Claude plugin package** — CLAUDE.md (persona + instructions) + hooks/ (lifecycle) + skills/ (procedures) + the MCP URL, delivered as a single package; primary distribution for all Claude surfaces (Chat, Cowork, Code)
3. **ChatGPT integration** — the same hosted MCP URL as a remote MCP connection, plus individual SKILL.md files (zipped when dependencies are needed, plain `.md` when self-contained); BYOC ChatGPT user adds the MCP and each skill manually

Both clients connect to the same hosted MCP endpoint. The client LLM (Claude or GPT-4) provides reasoning; Piper's server provides tools, connectors, and persisted context.

---

## Context

PDR-005 (Jun 5, 2026) established the strategic split: *"server holds working memory + tools + persistence + trust-graduation; client holds LLM + conversation surface + client-side history."* That decision was abstract about how the server is accessed.

Through the MCPB skunkworks POC (May–July 2026), the team explored a locally-run MCP bundle approach. PM confirmed July 18, 2026 that MCPB is a dead end: it required users to run infrastructure locally, had no clean path to production, and obscured the real distribution pattern now available via hosted remote MCP support in both Claude and ChatGPT platforms.

The timing is right: both platforms have recently shipped native support for hosted/remote MCP, including plugin-directory listings (Claude) and remote MCP + skills (ChatGPT). The correct production path is hosted, not locally-run.

The BYOC LLM key question (raised during MCPB: "how does the user's LLM call happen without server-side LLM infrastructure?") **dissolves** in this model: the user's own chat platform provides the LLM. Piper's server provides connectors and context. No server-side LLM key is needed for the hosted MCP phase.

---

## User Need

A BYOC user wants to use their existing Claude or ChatGPT subscription to access Piper's capabilities — connectors, stored profile, colleague model, working memory — without running any Piper infrastructure locally. They want a one-time setup (add MCP URL + plugin) and then Piper works inside their normal chat environment.

Different BYOC users have different levels of technical comfort. The plugin package abstracts the setup; the skill files give power users explicit capability discovery.

---

## Decision Rationale

### Why hosted over locally-run

- No local infrastructure requirement for end users
- Piper maintains the server; users get updates automatically
- Auth model (OAuth or API key) is simpler than MCPB's credential theater
- Both Claude and ChatGPT now support remote hosted MCP natively

### Why Claude plugin package is the primary distribution

- A single package (CLAUDE.md + hooks + skills + MCP URL) gives Claude users the full Piper experience
- Supported by Chat, Cowork, and Code (with varying levels of hook support — Chat doesn't use hooks yet, but the package degrades gracefully)
- Claude's plugin directory provides organic discoverability
- The plugin format is familiar to Claude Code users (CLAUDE.md is already a known surface)

### Why the hosted MCP is a pure tool server (no server-side LLM)

- PDR-005 established this split; this PDR makes it concrete
- For the hosted MCP + plugin phase, Piper's "intelligence" is: stored user profile, colleague model, connectors, MUX lifecycle state, composted learning (ADR-054)
- The client LLM reasons over that context; Piper serves it
- This keeps Piper's server costs low and avoids needing a server-side API key during alpha/beta
- Exception (deferred to M4): proactive/scheduled server-side agentic flows would need a server-side LLM — three options under consideration: Piper's own key (subscription model), BYOC key stored encrypted via #1382, or all reasoning pushed to client

### Why ChatGPT alongside Claude

- ChatGPT users are a significant BYOC population
- The same hosted MCP URL works; skill files are ChatGPT's equivalent of Claude's plugin CLAUDE.md
- Reach both major AI chat platforms with minimal additional infrastructure
- GPT plugin directory provides a second discovery channel

---

## Capability Split: Plugin vs. Server

The following captures what lives in the plugin package vs. what stays on the server — important for implementation planning.

### In the plugin package (ships to user's device/chat)

| Component | Format | Purpose |
|---|---|---|
| CLAUDE.md | Markdown | Piper's persona, instructions, how to invoke skills |
| skills/ | .md files | Procedures Piper can run (fetch contacts, find meeting context, etc.) |
| hooks/ | .sh or .py | Lifecycle hooks (session start, pre-commit, etc.) — Claude Code only |
| MCP URL | String in CLAUDE.md | Connection point to `mcp.pipermorgan.ai` |
| Connector guidance | Section in CLAUDE.md | Which MCP tools correspond to which connectors |

### On the server (hosted at mcp.pipermorgan.ai)

| Capability | Notes |
|---|---|
| User profile | How user describes themselves, role, org |
| Colleague model | How user works — inferred patterns, preferences, contexts |
| Composted learning / InsightJournal (ADR-054) | What Piper has learned from prior sessions |
| Connector grants | Which connectors the user has authorized |
| MUX lifecycle state | Modeled User Experience state (active projects, current context) |
| Trust graduation state | Where user is in the trust model |
| Tools / connector implementations | The actual MCP tools (GCal, Notion, GitHub, etc.) |

---

## Alternatives Rejected

### Continue with MCPB (locally-run MCP bundle)
Rejected: requires local infrastructure, no clean production path, credential model was theater, now superseded by native hosted MCP support in both platforms.

### Build a bespoke web UI as primary surface
Not rejected entirely — PDR-005 already preserves this as an asymptotic target for discrete surfaces that can't work in chat. But it's not the primary distribution for alpha/beta; the BYOC chat + hosted MCP path is faster to ship and reaches users where they already are.

### Require server-side LLM for all Piper capabilities
Rejected for this phase: unnecessary for connectors + context serving, adds cost and infrastructure complexity, breaks the "client provides intelligence" principle from PDR-005. Revisit in M4 for server-side agentic flows.

---

## Implications

### For CXO
- Plugin package UX needs design: what does a user's first experience of the Piper plugin look like? Onboarding flow for connecting MCP + adding skills. ChatGPT manual-add flow is notably more friction than Claude's (each skill added separately).

### For Arch
- `mcp.pipermorgan.ai` subdomain: DNS, TLS, hosting on existing Fly.io infrastructure
- Auth model for the hosted MCP endpoint: OAuth preferred; API key as fallback for simpler clients
- MCP tool catalog design: which tools expose which server-side capabilities
- Colleague model and composted learning: how are they read/written via MCP resources vs. tools?

### For PPM / Lead Dev
- #1360 (API key gate for `/api/v1/intent`) and #1351 (MCPB credential) are both likely superseded by this decision — but PM should explicitly confirm closure
- Hosted MCP implementation is a new epic; issue TBD

### For Comms
- "Plugin" has a specific meaning here (Claude plugin = CLAUDE.md + hooks + skills + MCP URL) — distinct from "MCPB" (deprecated), "connector" (an integration within Piper), and "skill" (a procedure file). See glossary. Blog posts will need to be precise.
- The hosted MCP path is a good story for the Piper Alpha narrative: "Piper works inside your existing Claude/ChatGPT."

---

## Success Criteria

- A BYOC Claude Chat user can add the Piper plugin package (or just the CLAUDE.md + MCP URL) and interact with Piper's stored context without any local infrastructure
- A BYOC ChatGPT user can add `mcp.pipermorgan.ai` as a remote MCP and individual skills and get equivalent core capabilities
- Alpha testers confirm: setup is a one-time operation, not a recurring maintenance burden

---

## Open Questions (PM-gated)

1. **#1360 and #1351 closure**: These were MCPB-specific security issues. May PM explicitly confirm these can be closed as superseded by PDR-006?

2. **Colleague model build vs. serve**: Does building/updating the colleague model require server-side LLM inference (pattern recognition over conversation signals), or is it a pure database write from client-observable signals pushed by the client LLM? If it requires server-side LLM, that's a constraint for the M3 roadmap even under the "no server LLM" assumption for M2.

3. **Plugin directory applications**: PM mentioned both Claude and GPT have directories to apply to. Is this a "begin drafting applications now" direction, or wait until the plugin package and beta are more stable?

---

## References

- PDR-005: Bring Your Own Chat — Distribution Model (ratified Jun 5, 2026)
- ADR-054: InsightJournal / Composted Learning
- #1351: MCPB credential (likely superseded)
- #1360: Intent API key gate for MCPB (likely superseded)
- #1382: Encrypted API key store (future; relevant to M4 server-side LLM option)
- Architecture diagram (PA, Jul 18 2026): https://claude.ai/code/artifact/a146134e-2858-4c7c-a916-8f1b038fc8c6

---

## Changelog

| Version | Date | Author | Notes |
|---|---|---|---|
| v0.1 | 2026-07-19 | PA | Initial draft — captures PM's Jul 18 direction; pending PM + Arch review before ratification |
