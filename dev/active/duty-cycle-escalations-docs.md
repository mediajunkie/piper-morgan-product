# Docs Duty Cycle — Escalations / Attention Doc

**Purpose**: items requiring PM attention per v0.6 Duty Cycle (reframed escalations = attention doc, per Architectural Decision 2).

**Owner**: Documentation Management (Docs)
**Created**: 2026-05-27 12:05 PT at v0.6 cycle adoption

---

## Active escalations (for PM)

- **#972 MEM-TEMPORAL — clarification needed before example-files slice** (surfaced Docs Fire 8, 2026-05-27 21:46 PT): Schema spec draft v0.1 filed (`docs/internal/operations/memory-frontmatter-temporal-fields-spec.md`). Remaining work includes "≥3 existing memory files updated as examples" per Lead Dev's May 17 audit. **Open question: which files are the "memory files"?** Candidates: (a) personal Claude auto-memory at `~/.claude/projects/.../memory/*.md` (outside repo); (b) project institutional-memory docs (which?); (c) Janus-memory-research-referenced layer. Need PM/Lead Dev/CIO clarification on canonical target before backfilling `valid_from` examples. BRIEFING-CURRENT-STATE template + memo format guide + session-log instruction slices remain but are higher-blast-radius (cohort-read docs) warranting PM-awareness, not autonomous late-night edits. **Recommend**: resolve "which memory files" in a PM-engaged session; then remaining #972 work lands.

## Process observations (for cycle methodology + CIO research)

- **2026-05-27**: Adopting v0.6 cycle as workhorse-tier per PM 8:51 AM PDT directive. Cron offset `:17`. [RESOLVED: launched 12:24 PT job 42a9ed72; cron-id rotated 3x through day to fc464e79.]
- **2026-05-27 Fire 8**: v0.6.3 forward-progress judgment — declined to autonomously edit BRIEFING-CURRENT-STATE (high-blast-radius cohort doc) on a late-evening fire; instead surfaced the #972 clarification blocker above. Holistic-not-tactical: not all "unblocked low-priority work" is appropriate for unsupervised fires — blast-radius is a filter alongside scope.

---

*This file is escalations-as-attention-doc per v0.6 architectural decision 2. Append during cycle fires when items need PM-attention surfacing.*
