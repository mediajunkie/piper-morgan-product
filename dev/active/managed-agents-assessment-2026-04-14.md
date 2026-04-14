# Claude Managed Agents Assessment — Distribution Implications for Piper Morgan

**Author**: PA (research agent synthesis)
**Date**: April 14, 2026
**Status**: Research findings for PM and Architect review
**Sources**: Official Anthropic docs, engineering blog, SDK release notes, 10+ analysis articles

---

## Executive Summary

Managed Agents is a strong fit for Piper Morgan's **server-side** distribution path but does not replace the MCPB/Claude Desktop path. The two serve different use cases and are complementary. The critical finding: **Memory Stores** (research preview, access request required) map directly to our five-layer context model and solve the cross-session persistence problem. Without Memory Stores, Managed Agents sessions are ephemeral. With them, the five-layer model maps naturally.

---

## Architecture: Brain/Hands Separation

Four primitives: **Agent** (reusable config: model, prompt, tools, MCP servers), **Environment** (container template), **Session** (running instance with append-only event log), **Events** (SSE-streamed interactions).

Key design: sessions are durable (the event log persists outside the harness), the harness is stateless (horizontally scalable), and containers are lazy-provisioned (sessions that don't need a sandbox skip the overhead — 60% drop in p50 TTFT).

---

## Five-Layer Mapping

| PM Layer | Managed Agents Primitive | Notes |
|----------|------------------------|-------|
| **L1: Kit Briefing** | Agent system prompt | Static per agent definition |
| **L2: Project Instructions** | Agent system prompt + read-only Memory Store | Methodology as seeded content |
| **L3: Project Memory** | Read-write Memory Store | **Best mapping.** Up to 8 stores per session. 100KB per entry. Immutable version history. |
| **L4: Channel Addendum** | Session-level resource prompt | Per-session instructions at attachment time |
| **L5: Entity Prompt** | Agent definition + session resources | Agent defines role; session prompts provide entity-specific context |

The mapping is strong. Memory Stores are the linchpin — they provide typed, versioned, auditable cross-session memory with read-write or read-only access. This is closer to our ADR-054 design than anything we've built ourselves.

---

## Two Distribution Paths (Complementary)

### Path A: Claude Desktop (MCPB) — Local
- Piper as local MCP server (stdio transport)
- User installs via .mcpb one-click
- Piper provides tools; Claude controls the conversation
- **Persona**: via Claude Project instructions (hybrid approach)
- **Pros**: No runtime costs, works offline, familiar Claude interface
- **Cons**: No persistent sessions, no built-in memory, user manages infrastructure

### Path B: Managed Agents — Server-Side
- Piper's tools exposed via remote MCP server (HTTP transport required)
- Managed Agent configured with Piper's MCP server URL
- Piper controls the persona (Agent system prompt), memory (Memory Stores), and session persistence
- **Pros**: Persistent sessions, memory stores, auto-compaction, container sandboxing, SSE streaming
- **Cons**: $0.08/hr runtime + token costs, requires remote HTTP MCP server, Anthropic dependency, beta stability

### The Key Difference

**Claude Desktop**: Piper is a **tool provider** inside someone else's conversation.
**Managed Agents**: Piper **is** the agent — controls persona, memory, and conversation flow.

The Managed Agents path is more powerful for a PM assistant because it solves the persona gap (Agent system prompt = Piper's voice) and the persistence gap (Memory Stores = cross-session context). The MCPB path is simpler and cheaper for casual users.

---

## MCP Integration Constraints

**Critical**: MCP servers connected to Managed Agents must be **remote HTTP** (streamable HTTP transport). Local stdio servers are NOT supported. This means:
- The same Piper MCP server code can serve both paths
- But the Claude Desktop version runs as local stdio, while the Managed Agents version must run as an HTTP endpoint
- Both transport modes are standard MCP; the code stays the same, only the transport layer differs

---

## Context Management

- **Compaction**: Automatic inside Managed Agents, no configuration needed
- **Standalone Compaction API** (Feb 2026): Available for non-Managed-Agents use cases (beta header `compact-2026-01-12`)
- **Client-side SDK compaction**: Not formally deprecated but Anthropic recommends server-side
- **Memory Stores**: Research preview. Up to 8 per session, 100KB per entry, immutable version history, optimistic concurrency via content SHA256

---

## Cost Reality Check

For typical PM assistant usage (~30 min active/day):
- Runtime: ~$0.04/day ($1.20/month)
- Token costs: $5-20/month (varies with workload)
- **Total: ~$10-50/month** — token costs dominate, runtime is negligible

An always-on agent would cost ~$58/month in runtime before tokens. Not our use case.

---

## What Maps Well for PM

1. **Memory Stores → Project Memory**: Direct, strong mapping. Versioned, auditable, cross-session.
2. **Agent system prompt → Kit Briefing + Entity Prompt**: Piper's voice lives in the Agent definition.
3. **MCP integration → Channel access**: Slack, GitHub, Calendar as MCP servers.
4. **Auto-compaction → No more building our own**: Compaction handled by infrastructure.
5. **Session persistence → Conversation continuity**: The append-only event log solves #953 (CONTEXT-PERSIST) for the Managed Agents path.

## What Doesn't Map

1. **Object model grammar**: No native Entities/Moments/Places primitives — lives in prompts and memory content.
2. **Channel Addendum**: Approximated via session-level resource prompts but not a perfect fit.
3. **Composting lifecycle**: Memory Stores have versioning and deletion but no lifecycle states (Emergent → Composted). That's our product logic, not infrastructure.
4. **Trust graduation**: No native trust model — our product logic on top of their infrastructure.

---

## Recommendations

1. **Request Memory Stores research preview access immediately.** This is the linchpin for the Managed Agents path. Without it, sessions are ephemeral and the path loses most of its value.

2. **Build the MCP server to support both transports.** stdio for Claude Desktop (MCPB), HTTP for Managed Agents. Same tools, same logic, different transport layer. The Architect already recommended Python for codebase reuse.

3. **Don't choose between paths — offer both.** MCPB for casual/local users. Managed Agents for power users who want persistence, memory, and server-side hosting. The MCP server is the product; the distribution path is a packaging choice.

4. **The Managed Agents path resolves the persona gap.** The Agent system prompt IS the persona — no hybrid needed, no Claude Project workaround. This is a meaningful advantage over MCPB.

5. **Factor Managed Agents into M5 distribution planning.** The DIST issues (#829-832, #957-959) currently assume MCPB only. Add Managed Agents as a second distribution target. The MCP server work (#829) serves both.

6. **Watch the beta carefully.** Memory Stores are research preview. Multi-agent coordination is research preview. Both could change. Don't build production dependency on research-preview features — but do prototype against them.

---

## Relationship to Other Documents

- **Vision V2.3**: "Bring Your Own Chat" thesis validated — Managed Agents is another "chat" users can bring
- **Roadmap v15.0**: M5 DIST issues should reference Managed Agents as second distribution target
- **MCPB feasibility** (`dev/active/mcpb-feasibility-2026-04-08.md`): Complementary, not competing. MCPB = local, Managed Agents = server-side
- **Five-layer mapping** (`docs/internal/architecture/current/five-layer-context-mapping.md`): Memory Stores address the Layer 3/4 gaps identified there
- **Klatch Step 10**: Both projects targeting Managed Agents as execution layer — shared upstream assumption confirmed

---

*Research assessment for project record. Sources documented in research agent output.*
