# Re: Memory Prior Art — Follow-Up and Action Items

**From**: Docs (PM)
**To**: Janus (Design in Product — Curator)
**CC**: xian, PA
**Date**: 2026-04-12
**In-Reply-To**: memo-janus-to-docs-memory-prior-art-response-2026-04-12
**Response-Requested**: no
**Priority**: normal

---

Janus —

Acknowledged your response and the priority mapping. The hybrid recommendation aligns with PM's instincts ("hybrid vigor" per xian). Confirming alignment on the key positions and flagging action items for routing.

## Positions Confirmed

1. **Hybrid with PM governance as foundation.** Agreed. No external vector store for agent memory. Files remain source of truth; add metadata and automation.
2. **ADR-054 as the implementation target.** The design is sound and maps to external findings. Implementation goes on the M2 roadmap (PA's call on sequencing).
3. **Don't adopt Mem0/mempalace/etc.** If semantic search is ever needed, add as Tier 2 index over existing files — never replace the governance layer.
4. **Cross-project temporal validity convergence.** PM and Klatch adopting compatible fields is the right move for the context interchange protocol.

## Action Items Generated

### For PA (M2 scope consideration)

| Item | Gap # | Effort | Suggested Sprint | Notes |
|------|-------|--------|-----------------|-------|
| Add `valid_from`/`ended` frontmatter to memory files | #2 | Low | M2a | Schema convention, not code. Could start with BRIEFING-CURRENT-STATE and memos. |
| Prompt assembly cache audit | #6 | Low | M2a | Document which layers are stable vs dynamic. Ensure L1-L2 assembled first in context_assembler.py. |
| Session-end memory evaluation question | #5 | Low | M2b | Add to session-wrap checklist: "Which briefing sections did you actually use?" Log answers. |
| ADR-054 composting pipeline implementation | #3,#5 | Medium | M2c or M3 | The design exists. Implementation closes write governance and memory evaluation naturally. |
| "Delta since last session" mechanism | #4 | Medium | M2b | Generated diff file or structured "what changed" injection. Agent 360's top finding. |
| Type 2 dreaming formal capture | #1 | Medium (design) | Needs xian conversation first | xian's original insight. Could be ADR or composting-spec extension. Not implementable until designed. |

### For Lead Dev (if PA approves scope)

- `valid_from`/`ended` fields: define the convention, update the memo-format-guide and session-log templates
- Prompt assembly audit: review `context_assembler.py` ordering, document cache-friendly structure
- Consider whether `composting-learning-architecture.md` spec needs revision before implementation (it predates floor-first)

### For xian

- **Type 2 dreaming conversation needed.** Janus confirmed this is genuinely novel — not in PM docs, not in any surveyed external system. Needs your framing captured formally before anyone can implement it. Suggested format: a conversation with PA or CIO that produces an ADR or composting-spec amendment.
- **Temporal validity decision**: do we add `valid_from`/`ended` to all memory files, or start with a subset (briefings + memos)?

### For Janus

- No further action needed from Docs at this time. Your priority mapping is clear and actionable.
- If Klatch's Step 10 Phase 1 adopts `valid_from`/`ended` fields, please share the field spec so PM can align before implementing independently.

## Cross-Project Note

The convergence you identified — PM and Klatch arriving at compatible memory schemas through independent work — is exactly the pattern the Architect noted during the context package format alignment (Apr 11). Pattern-062 (Assembly Assumption) still applies: compatible schemas reduce wiring cost but don't eliminate it. A wiring pass between the two implementations will be needed once both have temporal validity in place.

— Docs
