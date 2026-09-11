---
subject: "docs/ tree audit complete — plan ready for your review before any execution"
from: docs
to: xian (ceo)
cc: ppm
date: 2026-07-13
---

# docs/ Tree Audit: Plan Ready

PM — per your request (relayed by PPM last night), I've completed the docs/ tree audit. Plan is at:

`docs/internal/planning/docs-tree-audit-2026-07-13.md`

Short version of what I found:

**Three cleanup categories** (plus one PM-decision):

1. **"MOVED" stub directories** (`docs/architecture/`, `docs/planning/`, `docs/development/`) — just empty shells with a redirect README; the real content is in `docs/internal/`. Low risk to remove. I can do this immediately once you've reviewed the plan.

2. **Legacy external docs structure** — ~15 top-level directories (`docs/guides/`, `docs/installation/`, `docs/api/`, etc.) that look like they were for an external developer docs site. Most are Nov 2025 vintage. None appear in CLAUDE.md or NAVIGATION.md. Candidate for archiving. `docs/migration/` has a Jul 2026 date so I've held it for your confirmation.

3. **Alpha-era working documents** — `docs/internal/planning/roadmap/CORE/` (23 files, last substantive commit Jan 2026) and `docs/refactor/` (22 files, Nov 2025). Historical, not live references. Candidate for moving to `docs/internal/planning/historical/`.

4. **Dual-structure decision needed** — `docs/testing/` and `docs/internal/testing/` have different (not duplicate) content, same for `docs/operations/` vs `docs/internal/operations/`. Not a cleanup call I can make — needs your direction on whether to merge into `docs/internal/` or formalize the parallel structure.

**Proposed order**: Phase 1 (stubs) with your plan review approval → Phases 2–3 (archive) with per-phase confirmation → Phase 4 (dual structure) after your architectural call.

No execution until you've reviewed and approved the phases you want done.

— Docs
