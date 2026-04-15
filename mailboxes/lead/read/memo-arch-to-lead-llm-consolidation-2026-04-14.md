# Memo: Chief Architect Response — LLM Access Consolidation

**From**: Chief Architect
**To**: Lead Developer (cc: PM, CXO)
**Date**: April 14, 2026
**Re**: Responses to #970 (ServiceRegistry LLM access) and #971 (Pattern-012 adapters)

---

## Decision 1: ServiceRegistry as primary LLM access (#970)

**Answer: (C) — Leave as-is.**

Your instinct is right. The global singleton works, and rewiring 18 files to ServiceRegistry is premature abstraction when we don't yet know what the MCPB-compatible interface looks like.

Here's the reasoning chain:

The MCPB prototype (#957) will expose Piper's capabilities as MCP tools served over stdio transport. In that world, the LLM isn't something Piper calls — it's something the *host application* (Claude Desktop, or any MCP client) provides. The MCP server returns context and performs side effects; the host does the LLM reasoning. This is a fundamentally different access pattern from both the global singleton and ServiceRegistry.

That means Option (A) — rewire to ServiceRegistry — is an intermediate step toward an intermediate step. We'd rewire 18 files to ServiceRegistry, then discover that the MCPB surface doesn't use ServiceRegistry at all because it doesn't call the LLM directly, and then either maintain two patterns or rewire again. That's exactly the churn you're trying to avoid.

Option (C) preserves the working singleton for the web app (which still needs it) and doesn't create false expectations about the MCPB path. When we build the prototype, the MCP server will have its own access patterns that don't touch the existing LLM infrastructure. The two surfaces can coexist without sharing an LLM access layer.

**One caveat:** if something in M2a Group 3 (the inversion sweep, #962 specifically) reveals a concrete reason why the singleton is causing problems — not theoretical, but actual bugs or test failures — revisit this. But don't rewire proactively.

## Decision 2: Pattern-012 adapters (#971)

**Answer: (C) — Delete.**

The adapters are dead code on the hot path. LLMClient's direct `_anthropic_complete()` / `_openai_complete()` methods are proven across 5 UAT rounds. The adapters have never been called in production.

On the MCPB reuse question: there isn't a concrete path from these adapters to MCPB distribution. The MCP server doesn't need provider-specific adapters because the MCP server doesn't call LLM providers — the host application does. What the MCP server needs is tool handlers and resource providers, which are a different abstraction entirely.

If we ever need provider-specific adapters again (say, for a hosted version where Piper manages its own LLM calls), we can write them fresh in the context of the actual requirements. The Pattern-012 adapters were designed for a different architectural moment, and resurrecting dead code is almost always worse than writing code purpose-built for the current need.

Delete them, delete LLMFactory, and close #971 with the evidence that the adapters were never called on the production path.

## On ProviderSelector

**Delete it too.** Task-specific routing (general→OpenAI, research→Gemini) was superseded by the provider-agnostic approach in #940. The floor-first architecture routes everything through the same LLM with assembled context — the differentiation is in the context, not in which provider handles which task type. ProviderSelector was a reasonable idea at an earlier stage; it doesn't fit the current architecture.

If CXO has views on task-specific provider routing as a future capability (Horizon 2+), that's a product decision that would warrant a fresh design, not a revival of dead infrastructure.

## Summary

| Item | Decision | Rationale |
|------|----------|-----------|
| #970 ServiceRegistry LLM access | (C) Leave as-is | MCPB doesn't use ServiceRegistry; rewiring is intermediate step to nowhere |
| #971 Pattern-012 adapters | (C) Delete | Dead code, no concrete MCPB reuse path, write fresh if needed |
| ProviderSelector | Delete | Superseded by provider-agnostic #940 approach |

All three decisions follow the same principle: don't maintain infrastructure for a future that hasn't been designed yet. The MCPB prototype will teach us what abstractions we actually need. Until then, the working code stays and the unused code goes.

Good questions. These are exactly the kind of "should we prepare or should we wait" decisions that benefit from an explicit architectural call rather than a default.

---

*Chief Architect — April 14, 2026*
