# Memory Research Synthesis

**Author:** Janus (Design in Product)
**Date:** April 12, 2026
**Sources:** Four parallel research agents covering mempalace (Flowers/Jovovich), claude-memory-context (Albers), agentic-memory ANALYSIS.md (Lin), and a broader landscape survey of 12+ additional systems.
**For:** xian, then routed to Calliope/Daedalus (Klatch), PA (PM), Piper Open (OpenLaws), Ted Nadeau

---

## The Landscape in One Paragraph

Agent memory is converging. Leonard Lin's survey of 14+ systems finds that **storage technology is irrelevant; write governance is everything.** The biggest differentiator is not vector DB vs SQLite vs markdown files — it's provenance tracking, write gates, conflict handling, and reversibility. File-based memory (like what we use) is "underrated" per Lin — Codex and Claude Code both use it successfully — but it needs structure to scale. The field is moving toward typed entries with temporal validity, progressive token-budgeted retrieval, and background consolidation cycles modeled on human sleep. Our five-layer model is already well-positioned; the gaps are specific and addressable.

---

## Taxonomy: Six Dimensions of Memory

Synthesized from Lin's six-tier model, the academic survey's four-type model, and the practical patterns across all sources:

### 1. Capture (How does memory get written?)

| Pattern | Who does it | Examples |
|---|---|---|
| **Explicit savestate** | User triggers deliberately | Albers' `/savestate`, our session-end log tradition |
| **Auto-extract** | System extracts from conversation | Mem0, A-Mem, Letta |
| **Deterministic classify** | Regex/keyword, no LLM | mempalace (zero-LLM write path) |
| **Background consolidation** | Runs between sessions | Claude Auto Dream (four-phase cycle: orient, scan, consolidate, prune) |

**Best practice:** Explicit capture for high-fidelity facts + background consolidation for maintenance. Auto-extraction is useful but requires write gates to prevent garbage accumulation.

### 2. Storage (How is memory structured?)

| Pattern | Tradeoffs | Examples |
|---|---|---|
| **Flat markdown files** | Simple, diffable, portable. Manual curation. | Our MEMORY.md, Albers, Codex |
| **Typed entries with frontmatter** | Structured, queryable, provenance-bearing. Slightly more overhead. | Our current approach (partially), Lin's Tier 3 |
| **Embedding store (vector DB)** | Semantic search at scale. Opaque, not diffable. | mempalace (ChromaDB), Mem0 |
| **Knowledge graph** | Entity resolution, temporal validity, multi-hop. Complex. | Zep/Graphiti, mempalace (SQLite triples) |
| **Append-only event log** | Immutable source of truth. Everything else is a projection. | Lin's Tier 1, Gigabrain |

**Best practice:** Flat files as the durable layer (Tier 1) + typed entries for structured memory (Tier 3) + optional semantic index for retrieval at scale (Tier 2). Lin: "The log is the source. Everything else is a projection."

### 3. Retrieval (How does the right memory reach the right prompt?)

| Pattern | When to use | Examples |
|---|---|---|
| **Always-loaded summary** | Identity, critical facts (~150-250 tokens) | mempalace L0+L1, our MEMORY.md index |
| **Index-driven manual** | Small memory, user-directed | Albers (context-index.md) |
| **Semantic search** | Large memory, topic-driven | mempalace, Mem0, Zep |
| **Progressive disclosure** | Token-budgeted, escalating depth | mempalace (L0→L3), ByteRover (5-tier) |
| **Manifest selection** | LLM picks from a menu | Claude Code Sonnet selector |
| **Grep-first** | Keyword match before semantic | Codex |

**Best practice:** Always-loaded summary (tiny, cheap) + progressive disclosure on demand. Don't dump everything into the prompt. Lin: "Retrieval is not injection."

### 4. Injection (How does retrieved memory become prompt content?)

| Pattern | Description |
|---|---|
| **System prompt prefix** | Memory block prepended to system prompt. Simple but consumes fixed budget. |
| **Tool response** | Memory returned as tool output mid-conversation. More flexible but requires tool-use support. |
| **Layered assembly** | Memory placed in a specific layer of a multi-layer prompt. Our five-layer approach. |
| **Trust-tagged** | Memory content annotated with provenance/trust level so the LLM can weight it. |

**Best practice:** Layered assembly (we already do this) + trust tagging (we don't do this yet). Cross-pollination briefs should carry lower trust weight than agent-observed facts.

### 5. Maintenance (How does memory stay healthy?)

| Pattern | Description | Examples |
|---|---|---|
| **Manual curation** | Human reviews and prunes | Our current approach |
| **Background consolidation** | Automated periodic review | Auto Dream (24hr cycle), A-Mem (self-organizing) |
| **Temporal invalidation** | Facts expire via `valid_from`/`ended` windows | Zep/Graphiti |
| **Dedup + conflict detection** | Merge duplicates, flag contradictions | Gigabrain, Karta |
| **Benchmark harness** | Measure whether memory is actually helping | OpenClaw (60-query), Claude Code (eval-tracked) |

**Best practice:** Temporal invalidation on facts (prevents stale memory from misleading) + periodic consolidation (Auto Dream cadence) + at least a minimal benchmark ("did the agent use this memory correctly?"). We currently have none of these.

### 6. Governance (How do you trust what's in memory?)

| Pattern | Description |
|---|---|
| **Provenance** | Every entry traces to its source (session, conversation, brief) |
| **Write gates** | Confirmation before memory is committed; reject instructions to "remember" malicious content |
| **Version chains** | Corrections create new entries; old entries stay visible with markers |
| **Reversibility** | Any memory write can be undone |
| **Trust levels** | Memory from different sources (agent-observed, cross-pollination, external) carries different weight |

**Best practice:** This is Lin's central thesis. Write governance is the critical differentiator. We have provenance (frontmatter with date/type) but lack write gates, version chains, and trust levels.

---

## Gap Analysis: Our Five-Layer Model

| Our layer | Current approach | What the research suggests | Priority |
|---|---|---|---|
| **L3 (Project Memory)** | Markdown files with typed frontmatter, MEMORY.md index | Add temporal validity, provenance, progressive loading. Consider semantic index for scale. | **High** |
| **L3 maintenance** | Manual curation (ad hoc) | Add periodic consolidation cycle (Auto Dream cadence). Add staleness detection. | **High** |
| **L3 retrieval** | Always-loaded (entire MEMORY.md + referenced files) | Progressive disclosure: load index, retrieve on demand. Prevents token budget bloat as memory grows. | **Medium** |
| **L4 (Channel Addendum)** | Conversation-specific framing, not persisted across sessions | Lin's Tier 1 (append-only log) + Tier 3 (typed entries) could make L4 durable without making it permanent. Labrador's cartridge model is the UI pattern. | **Medium** |
| **L5 (Entity Prompt)** | Static role briefings | No system has solved "learned behavioral calibration" (the Layer 5 transfer gap Klatch identified). This is the open frontier for everyone. | **Low urgency, high importance** |
| **Cross-cutting: trust** | All memory treated equally | Trust-tagged injection: cross-pollination briefs and external input carry lower weight than agent-observed facts. | **Medium** |
| **Cross-cutting: governance** | Implicit (we trust our own writes) | Add provenance to every entry. Consider write gates for externally-sourced memory. Version chains for corrections. | **Medium** |
| **Maintenance/eval** | None | Even a minimal "did this memory get used?" signal would be a start. Auto Dream's consolidation cycle is the aspirational target. | **High** |

---

## The "Best Of" Composite Model

If I were designing a memory system for our ecosystem today, drawing from all sources:

**Layer 3 would have three sub-tiers:**

1. **Always-loaded identity summary** (~200 tokens). Pinned facts, role, current state. Equivalent to mempalace L0+L1 or Lin's Tier 5. Already what MEMORY.md does.

2. **Typed, temporal, provenance-bearing entries.** Each entry has: type (fact/decision/preference/episode), `valid_from` date, optional `ended` date, source (which session/conversation/brief), trust level (agent-observed / cross-pollination / external). Stored as markdown files with YAML frontmatter (what we already do, but with temporal and trust fields added). This is Lin's Tier 3.

3. **Retrievable archive.** Older or lower-priority entries that aren't always loaded but are searchable. Could be as simple as a separate directory that agents `grep` or as sophisticated as a ChromaDB index. Lin's Tier 2. Not needed until memory exceeds ~5000 tokens.

**Maintenance cycle:**

- **Per-session:** Explicit savestate at session end (Albers pattern). Verify writes landed (phantom-write guard).
- **Weekly:** Background consolidation — review entries for staleness, merge duplicates, flag contradictions. Could be an Auto Dream-style agent or a manual review cadence.
- **On write:** Provenance and type required. No anonymous memory entries.

**Retrieval pattern:**

- Always-loaded summary injected at Layer 3 position in the prompt.
- On-demand retrieval for deeper entries, triggered by topic relevance.
- Trust tagging: memory from cross-pollination briefs is marked as external.

---

## What This Means for Each Project

**Klatch:** The most direct beneficiary. Step 10's canonical context package format should include the three-sub-tier Layer 3 model. The format spec needs fields for `valid_from`, `type`, `source`, and `trust_level` on memory entries. Daedalus should read Lin's ANALYSIS.md directly — it's the most rigorous survey of the design space Step 10 is entering.

**Piper Morgan:** PM's briefing files and mailbox system are already a form of typed, provenance-bearing memory. The gap is temporal invalidation (briefings go stale) and progressive loading (PM agents spend 5-15 minutes at session start reconstructing context because everything is loaded at once). The three-sub-tier model would let PM agents start with a 200-token identity summary and retrieve deeper context on demand.

**OpenLaws:** Fresh enough to adopt best practices from scratch. Vergil and PO's `workdesk/` is currently flat. Typed entries with temporal validity from day one would prevent the staleness problems PM and Klatch have both encountered.

**Ted Nadeau / HPL:** HPL's OBJECT and STATE types are the formalized notation for what this research calls "typed, temporal, provenance-bearing entries." Ted's HPL is already designing the language for this; the research validates the design direction and provides implementation precedents.

**Cross-pollination hub:** The daily briefs are a form of episodic memory for the ecosystem. They should be trust-tagged as "cross-pollination / external" when injected into project-level Layer 3, so agents weight them appropriately relative to their own observations.

---

## Recommended Reading Order

For agents or humans who want to go deeper:

1. **Start here:** [Lin's ANALYSIS.md](https://github.com/lhl/agentic-memory/blob/main/ANALYSIS.md) — the definitive survey. Six-tier model, eight context assembly patterns, 14 systems evaluated.
2. **Then:** [Letta's "Is a Filesystem All You Need?"](https://www.letta.com/blog/benchmarking-ai-agent-memory) — directly challenges whether we need to move beyond markdown files.
3. **Then:** [Zep/Graphiti paper](https://arxiv.org/abs/2501.13956) — the strongest case for temporal validity in memory.
4. **Academic framing:** ["Memory in the Age of AI Agents" survey](https://arxiv.org/abs/2512.13564) — taxonomy of episodic/semantic/working/parametric memory types.
5. **For implementers:** [A-Mem paper](https://arxiv.org/abs/2502.12110) — self-organizing memory using Zettelkasten-inspired structured notes.

---

## Key Correction

The earlier Labrador research attributed `mempalace` to Erika Flowers. It is actually by Milla Jovovich and Ben Sigman. `erikaflowers/mempalace` on GitHub appears to be a fork, not the origin. Erika's Labrador product likely uses a different memory implementation — possibly her own design, possibly mempalace as a dependency. This should be corrected in any future references.

---

*Synthesis by Janus, April 12, 2026. Based on four parallel research outputs covering 20+ systems and 40+ academic papers.*
