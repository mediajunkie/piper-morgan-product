# FLY-AUDIT Findings — Weekly Docs Audit 2026-06-08 (#1177)

**Auditor**: Documentation Management (Docs)
**Method**: full manual verification with evidence (no subagents — mechanical commands)
**Prior audit**: #1140 (2026-06-01/02, full Completion Matrix, healthy)

> **Process note**: this audit was initially run at a "priority subset" depth and closed prematurely; PM flagged that the duty cycle is never a reason to shrink work. Re-run at full depth (matching #1140) and reopened/recompleted. Lesson pinned to memory.

---

## Result: HEALTHY corpus, ONE significant finding (link rot), now tracked

### ✅ Briefing Freshness (PRIORITY)
`docs/briefing/BRIEFING-CURRENT-STATE.md` refreshed 2026-06-08 (`last_updated: 2026-06-08`): v0.8.7 production cut + hosted alpha, Roadmap v18 canonical, PDR-005 v1.0, #1124 Phase 2/3/4-shim, M3 closures, CXO Epic #1169, recipient-owns + Gap-C. Was 4 days stale (v0.8.6 + Roadmap v16).

### ⚠️ Link Integrity — PRIORITY clean; FULL-TREE found rot → #1182
- **Priority files**: ADRs 0 broken ✓ · Briefings 0 broken ✓ · Patterns 3 broken → **FIXED** (commit, `patterns/README.md`).
- **Full-tree sweep**: **243 broken relative `.md` links** — **206 live**, 37 legacy/archive/historical.
  - Lead cause (~72): `models/models/` doubled directory from the doc-architecture transformation (`fe2b85718`); links resolve at wrong depth.
  - Other live offenders: anti-pattern-index (20), PDR-002 appendix (8), domain-models-index (7), filing-notes (6), api-reference (6).
  - **Filed #1182** (DOCS-LINKROT) — structural (needs Architect's call on `models/` layout), not blind-fix.

### ✅ Infrastructure & Pattern Verification
- `main.py` **428** / `web/app.py` **372** lines (refactor trigger 1000 — well under) ✓
- `DatabasePool` in services/: **none** ✓ · backup files (`*.backup`/`*.old`) in active dirs: **none** ✓
- `.cursor/rules/`: **5** files ✓ · CITATIONS.md present (22.9KB) ✓
- methodology `INDEX.md` + `NAVIGATION.md` present ✓
- Patterns: 75 `pattern-*.md`, README current through pattern-074 ✓ · ADRs: 69, all lowercase ✓
- Port-8080 grep: 7 hits, **all legitimate** (corrective "NOT 8080, use 8001" / legacy notes / historical retros) — false positive.

### ✅ Session Logs & Omnibus
- Omnibus logs continuous **June 1–7**; **June 8 synthesizes tomorrow** at START (gate discipline). ✓
- No stranded session logs outside `dev/`. ✓

### ✅ Sprint & Roadmap Alignment
- `roadmap.md` = **v18.0** canonical (PM-ratified June 3; v16 archived). ✓
- Roadmap content updates are PPM's lane (Docs does not edit roadmap body).

### Notes / minor (not blocking, not filed)
- **NAVIGATION.md** last updated 2026-05-12 (~4 weeks) — candidate refresh given recent doc moves; not stale-critical.
- **Root README.md** last touched Feb 11; no stale "NEW:" claims (clean); evergreen content.
- **18/30 open issues without GitHub milestone** — expected: sprint membership lives on the Projects board Iteration field, not milestones (per PM standing note). Not a finding.
- **62 TODO/FIXME** in services/web + **2 test files outside /tests/** (`services/mcp/server/test_dual_mode.py`, `services/integrations/github/test_pm0008.py`) — code-side, not docs; surfaced for Lead's awareness, not Docs-actionable.
- Duplicate basenames (INDEX.md, README.md, troubleshooting.md, etc.) — overwhelmingly legitimate per-dir files; no consolidation needed.

---

## Fixes applied this audit
1. `patterns/README.md` — 3 broken links repaired (committed to origin/main).

## Issues filed
1. **#1182** DOCS-LINKROT — 206 live broken links (models/models/ doubled-dir lead).

## Staggered-audit calendar
- Documentation audit: Last Completed → **2026-06-08**; Next Due → 2026-06-15.
