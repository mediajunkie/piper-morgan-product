# Docs Duty Cycle — Escalations / Attention Doc

**Purpose**: items requiring PM attention per v0.6 Duty Cycle (reframed escalations = attention doc, per Architectural Decision 2).

**Owner**: Documentation Management (Docs)
**Created**: 2026-05-27 12:05 PT at v0.6 cycle adoption

---

## Active escalations (for PM)

- **#972 MEM-TEMPORAL — referent RESOLVED; now 2 design questions before backfills** (updated 2026-05-28 ~10:40 PT): "Which memory files" is resolved — the #972 issue body (PM-authored) names the target: "Start with BRIEFING-CURRENT-STATE and memos" = institutional-memory docs (NOT `.serena/memories` or auto-memory). I'd read the AC line in isolation; the body had it. Spec corrected to v0.2. **Two design questions now gate example backfills (flagged, not guessed):** (1) BRIEFING-CURRENT-STATE has no YAML frontmatter today — add a block, or does its "Last Updated" line already serve? (2) memo `valid_from`/`ended` semantics questionable — memos are point-in-time + already dated; concept fits standing docs better. **Recommend**: PM/cohort resolve Q1+Q2 (is the real target standing reference docs, with memos a misfit?); then backfills land. Lead Dev escalation closed (read-in-isolation error on my part; CLAUDE.md §Verify-First generalized in response).

## Process observations (for cycle methodology + CIO research)

- **2026-05-27**: Adopting v0.6 cycle as workhorse-tier per PM 8:51 AM PDT directive. Cron offset `:17`. [RESOLVED: launched 12:24 PT job 42a9ed72; cron-id rotated 3x through day to fc464e79.]
- **2026-05-27 Fire 8**: v0.6.3 forward-progress judgment — declined to autonomously edit BRIEFING-CURRENT-STATE (high-blast-radius cohort doc) on a late-evening fire; instead surfaced the #972 clarification blocker above. Holistic-not-tactical: not all "unblocked low-priority work" is appropriate for unsupervised fires — blast-radius is a filter alongside scope.

---

*This file is escalations-as-attention-doc per v0.6 architectural decision 2. Append during cycle fires when items need PM-attention surfacing.*
