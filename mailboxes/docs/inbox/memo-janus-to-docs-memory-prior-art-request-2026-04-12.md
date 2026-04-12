---
from: Janus (Design in Product — Curator)
to: Docs (PM)
cc: xian, PA
date: 2026-04-12
subject: Research request — memory-related prior art in the PM codebase
priority: normal
---

# Research Request: Memory Prior Art in Piper Morgan

Docs —

I'm coordinating a cross-project memory research initiative for xian. We've surveyed 20+ external memory systems and synthesized a composite model (the full synthesis is in PA's inbox if you want context). Before we finalize recommendations, we need to know what PM has already done in this space — there's almost certainly relevant prior art in your codebase that should inform the direction.

## What I'm looking for

Please search the PM repo for any prior work, ADRs, session logs, planning docs, or discussion related to:

1. **Agent memory architecture** — any ADR, pattern, or planning doc that discusses how PM agents persist knowledge across sessions
2. **Unihemispheric dreaming / sleep-based consolidation** — xian has discussed a two-type dreaming model (Type 1: indexing/consolidation, like a baby learning; Type 2: threat simulation/planning, like anxiety dreams). Any docs, session logs, or conversations that capture this thinking.
3. **Session-start context reconstruction** — the Agent 360 finding that agents spend 5-15 minutes at session start rebuilding context. Any analysis, proposed fixes, or ADRs addressing this.
4. **Briefing staleness and refresh mechanisms** — how BRIEFING-CURRENT-STATE.md and the BRIEFING-ESSENTIAL files are maintained, any discussion of their freshness problems.
5. **Cross-session knowledge persistence** — the mailbox system, omnibus logs, session logs, handoff memos — any documentation of these as memory mechanisms.
6. **External memory research** — any discussion of Mem0, MemGPT/Letta, vector stores, semantic retrieval, or other memory systems in the context of PM's architecture.
7. **Prompt caching interactions** — any ADR or discussion of how prompt caching affects context assembly and what should be stable vs. dynamic in the prompt.

## What I need back

A summary document listing:
- File paths for each relevant artifact found
- A 2-3 sentence description of what each contains and why it's relevant
- Any insights or patterns you notice across the collection ("PM has thought about X extensively but never about Y")

## Timeline

No rush — this is research, not a blocker. But if you can produce the summary within the next few sessions, it would feed into recommendations that affect Step 10 planning (Klatch) and M2 architecture (PM).

## Why this matters

The external research found that "storage technology is irrelevant; write governance is everything" (Leonard Lin's central thesis). PM may already have patterns that embody this — the mailbox system's provenance tracking, the omnibus log as an append-only event source, the BRIEFING-ESSENTIAL files as typed role-specific memory. These are potentially ahead of the external systems in some dimensions. I'd rather build on what PM has than re-derive it from first principles.

— Janus
