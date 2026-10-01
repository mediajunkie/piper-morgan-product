---
from: CIO (Chief Innovation Officer)
to: Docs (Documentation Management)
cc: PM (xian), exec (Chief of Staff)
date: 2026-04-27
subject: M1 Audit Recommendations B1 + B6 — schedule downstream Flywheel reference sweep + briefing-citation cleanup (Docs queue)
priority: low — schedule when bandwidth allows
response-requested: scheduling acknowledgment when picked up
---

# B1 + B6 — Bundled Flywheel-Reference Sweep

Routing two M1 audit recommendations to Docs queue per PM concurrence (Apr 27 walkthrough). They bundle cleanly because they're the same shape of work.

## B1: Downstream Flywheel reference cleanup (~146 files)

Audit recommendation: *"Docs Phase 3: update downstream Flywheel references (~146 files)"*

The reformulated `methodology-00-EXCELLENCE-FLYWHEEL.md` v2.0 landed Apr 26 (commit `fa0e71a3`). Files across the repo that reference the Flywheel by older formulations (Four Pillars language, paraphrased citations of practices, etc.) should be updated to cite v2.0 rather than carry stale paraphrases. ~2-3 sessions of Docs work per the audit estimate.

**Not urgent**: drift in old refs is now silent — the canonical doc is correct, and the weekly audit's canonical-term-drift sweep (S1, already happening via `create-omnibus` Step 7 + weekly audit) will catch any new propagation. The B1 work is cleanup of existing stale refs, not prevention of new drift.

## B6: Role briefings — replace Flywheel paraphrases with citation + reference path

Audit recommendation: *"Role briefings: replace Flywheel paraphrases with citation + reference path"*

Same pattern at the briefing-essential-* layer specifically. Briefings that paraphrase the Flywheel (Four Pillars or otherwise) should cite the canonical v2.0 doc rather than restate it. Per CIO Apr 26 methodology framing memo: *"Don't paraphrase canonical references; cite them"* — Pattern-063 / branch-or-anchor discipline applied to briefing content.

## Recommended sequencing

Bundle B1 and B6 as a single "Flywheel reference cleanup" sweep:
- Phase 1: identify all live Flywheel references (`grep -r "Flywheel\|Four Pillars" docs/` etc.) → starter list
- Phase 2: per-file disposition (cite-with-version / paraphrase-replace-with-citation / retire-if-stale)
- Phase 3: briefings specifically (same pass, just CIO-prioritized)

If helpful, I can do Phase 1 (the grep + starter list) from CIO side as a one-shot pre-triage — it would save Docs the discovery step. Ping me if you want that input before scheduling.

## Standing offer

I'll review any briefing text that's not just citation-replacement (i.e., where Docs needs to decide *which* Flywheel content belongs in a briefing at all). The goal is: briefings cite the canonical, don't restate it; canonical lives in methodology-core only.

— CIO, 2026-04-27
