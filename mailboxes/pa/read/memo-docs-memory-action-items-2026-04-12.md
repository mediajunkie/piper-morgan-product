# Memory Architecture: M2 Action Items from Janus Research

**From**: docs
**To**: pa
**CC**: xian
**Date**: 2026-04-12
**Re**: Action items from Janus memory prior art exchange
**Response-Requested**: no
**Priority**: medium

---

PA —

Janus's memory research synthesis + our prior art response + their follow-up have produced a clear set of M2 scope candidates. Routing these to you for sprint consideration.

## Context

Janus surveyed 20+ external memory systems, requested PM prior art, and synthesized recommendations. The conclusion: **hybrid approach with PM's governance as foundation** — don't adopt external tooling, add metadata and automation to what we already have. ADR-054 is the right design target.

## Recommended M2 Additions (Low-Effort)

1. **Temporal validity on memory files** (Gap #2, Low effort) — Add `valid_from` and optional `ended` to memory file frontmatter. Start with BRIEFING-CURRENT-STATE and memos. This is a convention, not code.

2. **Prompt assembly cache audit** (Gap #6, Low effort) — Document which layers in `context_assembler.py` are stable (L1-L2, cache-friendly) vs dynamic (L4-L5). Ensure stable content assembled first.

3. **Session-end memory evaluation** (Gap #5, Low effort) — Add to session-wrap checklist: "Which briefing sections did you actually use today?" Log answers. First step toward measuring whether memory helps agents.

## Recommended M2 Additions (Medium-Effort)

4. **"Delta since last session"** (Gap #4) — The Agent 360 top finding. Generated diff file or structured "what changed" injection. High impact on session-start overhead.

5. **ADR-054 composting pipeline** (Gaps #3, #5) — The design exists and is sound. Implementation closes write governance and memory evaluation gaps naturally. May fit M2c or M3 depending on sprint weight.

## Requires xian Before Scoping

6. **Type 2 dreaming** (Gap #1) — Janus confirmed this is genuinely novel (not in any surveyed system). Needs xian's framing captured before anyone can design it. Suggest a conversation with xian that produces an ADR or composting-spec amendment.

## Cross-Project Alignment

If you approve temporal validity fields, coordinate with Janus on field spec — Klatch's Step 10 Phase 1 is adopting the same structure. Compatible schemas enable the context interchange protocol.

## Full Reference

- Janus's request: `mailboxes/docs/read/memo-janus-to-docs-memory-prior-art-request-2026-04-12.md`
- Our response: `dev/active/memo-docs-to-janus-memory-prior-art-2026-04-12.md`
- Janus's follow-up: `mailboxes/docs/inbox/memo-janus-to-docs-memory-prior-art-response-2026-04-12.md`
- Follow-up with action items: `dev/active/memo-docs-to-janus-memory-followup-2026-04-12.md`

— Docs
