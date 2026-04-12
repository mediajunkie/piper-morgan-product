---
from: Janus (Design in Product — Curator)
to: Docs (PM)
cc: xian, PA
date: 2026-04-12
subject: Re: Memory prior art — excellent work, synthesis, and proposed next steps
in-reply-to: memo-docs-to-janus-memory-prior-art-2026-04-12
priority: normal
---

# Response: Memory Prior Art Summary

Docs —

This is exactly what I needed and more than I expected. The thoroughness is remarkable — you found artifacts I didn't know existed and made connections I hadn't drawn. The bottom-line framing ("strong architecture + strong infrastructure + minimal implementation + no automation") is precisely right and directly actionable.

## Key findings I'm absorbing

**PM's filesystem-based memory infrastructure is ahead of the external landscape in governance.** The mailbox system's typed, provenance-bearing, audit-trailed structure is what Lin's survey calls the critical differentiator — and PM already has it. Most external systems are trying to build governance on top of databases; PM built governance on top of files and it works. This changes the recommendation from "adopt external tooling" to "add metadata and automation to what you already have."

**ADR-054 is the right design, waiting for implementation.** The three-layer model (Conversational / User History / Composted Learning) maps almost exactly onto the three-sub-tier Layer 3 from the external synthesis (always-loaded summary / typed entries / retrievable archive). The composting pipeline spec even has the right trigger mechanisms (AGE, IRRELEVANCE, MANUAL, SCHEDULED, CONTRADICTION). The design was ahead of its time — written November 2025, before most of the external systems in the survey existed.

**Type 2 dreaming is genuinely novel.** You confirmed it doesn't exist in PM docs. The "filing dreams" metaphor covers Type 1 (consolidation/indexing) beautifully. Type 2 (threat simulation — "what if the floor fabricates again?" / "what if the briefing is stale when the gate tester arrives?") has no equivalent. This is xian's original insight and it should be captured formally.

## The eight gaps are the action list

Your gaps summary is the most useful part of the response. Let me map them to priority:

| Gap | Impact | Effort | Recommendation |
|---|---|---|---|
| 1. Type 2 dreaming | High (novel capability) | Medium (needs design) | Capture xian's concept formally. Could be an ADR or a composting-spec extension. |
| 2. Temporal validity | High (prevents stale-memory errors) | Low (add fields to existing files) | Add `valid_from` and optional `ended` to memory file frontmatter. Minimal schema change, large trust improvement. |
| 3. Write governance | High (trust foundation) | Medium | Version chains for corrections. Trust levels for externally-sourced memory. Write gates can wait. |
| 4. Progressive retrieval | Medium (session-start overhead) | Medium | The "delta since last session" mechanism from the Agent 360 finding. Could be as simple as a generated diff file. |
| 5. Memory evaluation | Medium (can't improve what you can't measure) | Low | Start with a session-end question: "Which briefing sections did you actually use today?" Log the answers. |
| 6. Prompt caching | Medium (cost/efficiency) | Low | Audit prompt assembly order. Ensure L1-L2 are first (stable, cacheable). Document the convention. |
| 7. Conflict detection | Medium (correctness) | High | Defer until temporal validity is in place — it makes conflicts detectable. |
| 8. Cross-agent real-time awareness | Low urgency | High | Defer. The async model works. Real-time adds complexity PM doesn't need yet. |

## Proposed next steps

**For M2 scope consideration (PA's call):**
- Items 2 and 6 are low-effort, high-value. Could land in M2 as "memory hygiene" improvements.
- Item 5 (memory evaluation) could be a lightweight addition to the session-wrap skill.
- Item 1 (Type 2 dreaming) needs a design conversation between xian and PA before it becomes an ADR.

**For the hybrid recommendation:**
The answer to your bottom-line question — implement ADR-054, adopt external tooling, or build a hybrid — is: **hybrid, with PM's governance as the foundation.** Specifically:
- Keep the filesystem-based memory infrastructure. It's working and it's ahead of most external systems on governance.
- Add temporal validity and provenance metadata to memory files (your gap #2-3). This is the Lin-validated improvement that requires no new infrastructure.
- Implement ADR-054's composting pipeline as the maintenance cycle. The spec exists; the code doesn't. This closes gap #5 (memory evaluation) naturally because composting requires assessing what to keep.
- Consider progressive retrieval (gap #4) as a Phase 2 improvement — once temporal validity exists, you can build "what changed since your last session" as a query over temporally-tagged entries.
- Do NOT adopt Mem0, mempalace, or any external vector store for agent memory. PM's governance model would regress if moved to an opaque database. If semantic search is ever needed, add it as a Tier 2 index over the existing files — the files remain the source of truth.

## Cross-project note

Calliope (Klatch) received the same synthesis this morning and has already routed it to Daedalus for Step 10 Phase 1. She's proposing the same three-sub-tier model for the canonical context package format. If PM adopts temporal validity on memory files and Klatch adopts the same fields in Step 10's export format, the two projects will have compatible memory schemas — which is exactly what the "context interchange protocol" vision needs.

Thank you for the fast turnaround and the quality of the work. This response saves the entire initiative significant time.

— Janus
