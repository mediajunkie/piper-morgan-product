# FLY-AUDIT — Weekly Documentation Audit Findings (#1140)

**Audit date**: 2026-06-02 (for the 2026-06-01 generated checklist)
**Auditor**: Documentation Management (Docs), `claude/docs-cycle` worktree
**Method**: manual verification with evidence (per FAQ — manual acceptable with evidence)

---

## Summary

Documentation infrastructure is **healthy**. No broken ADR links, pattern catalog accurate, core docs present and well-located. A few low-severity drift items (one already tracked by #1128), plus two **workflow-improvement findings** for the audit checklist itself.

## Verified CLEAN (evidence)

| Check | Result |
|-------|--------|
| ADR internal links | **0 broken** of 19 (portable Python resolve; the checklist's `realpath --relative-to` command gives false positives on macOS — see Findings #4) |
| Pattern catalog count | 75 `pattern-*.md` = 74 patterns (001–074) + template (000); README "Total Patterns: 74" is **correct** |
| `web/app.py` line count | 354 (refactor trigger 1000) |
| `main.py` line count | 420 |
| Port 8080 in docs | only legacy-deprecation references (ports.md: "Legacy ports no longer used") — correct usage, not violations |
| `DatabasePool` in services | none (AsyncSessionFactory pattern holds) |
| `.cursor/rules/` | 5 rule files (expected) |
| ADR naming | all lowercase `adr-*.md`, 67 ADRs |
| Backup files (`*.backup`/`*.old`) | none in active dirs |
| CITATIONS.md | present (`docs/references/CITATIONS.md`) |
| Root README | no stale "NEW:" claims |
| methodology INDEX.md + NAVIGATION.md | both present |
| Omnibus structure | continuous through 2026-05-29; May 30/31 gap is **expected** (PM-gated, not yet synthesized) |
| BRIEFING-CURRENT-STATE | fresh — banner May 31 (the SessionStart hook's "14d/May 18" is the known date-field quirk, not real staleness) |

## Findings

1. **Roadmap 23 days stale** — `docs/internal/planning/roadmap/roadmap.md` last updated 2026-05-10 (v16.0). **Already tracked by #1128** (ROADMAP-REFRESH, PPM lane). No new issue; reference the existing one.
2. **ports.md / ChromaDB inconsistency (minor)** — `docs/internal/development/tools/quick-reference/ports.md` lists `8000` under "Legacy ports (no longer used)", but CLAUDE.md documents **ChromaDB on 8000**. One of the two is stale. Low-severity doc drift; flagged for a follow-up (did not edit blind — needs confirmation of the live ChromaDB port).
3. **Stranded session log** — `dev/active/2026-05-30-1332-ppm-code-opus-log.md` sits in `dev/active/` rather than `dev/2026/05/30/`. Will be archived when the **May 30 omnibus** runs (currently PM-gated). No action now.
4. **WORKFLOW-IMPROVEMENT — broken-link command is unreliable on macOS** — the checklist's "Quick audit command" uses `realpath --relative-to` (GNU-specific). On macOS it reported **17/17 ADR links broken** when the true count is **0** (verified by spot-check + portable Python). The command should be replaced with a portable resolver (Python `os.path.normpath` + `os.path.exists`, or `python3` one-liner). Recommend updating the issue template + `.github/workflows/weekly-docs-audit.yml`.
5. **WORKFLOW-IMPROVEMENT — "Claude Project Knowledge Updates" section is obsolete** — that section ("ACTION FOR PM: update Claude project knowledge") predates the May 4 2026 standing directive that no roles use chat project knowledge as a primary surface (maintained at "bare essentials"). The section should be retired or rescoped to "BRIEFING-CURRENT-STATE freshness" only.
6. **Minor — stale changelog line in patterns/README** — line ~219 says "_total now 62 patterns_" (a historical changelog entry); the authoritative count line 6 (74) is correct. Cosmetic.

## Informational

- **Open issues**: 123 open, **87 (>30 days) stale**. Mostly long-lived backlog / post-MVP items (e.g., #57, #58, #65). Not actionable in this audit; GitHub Projects is the source of truth.
- **TODO/FIXME in code**: 62 across services/web/cli (tracked in code, not a docs concern).
- **Doc metrics**: 1476 `.md` in docs/; 355 omnibus logs; 1520 docs touched in the last week (high-velocity sprint churn).
- **Duplicate basenames**: expected (per-dir README.md/INDEX.md); the content duplicates (permission-to-pause, 15-sessions-fast-recovery, from-protocol-to-infrastructure) are the known calendar published/-vs-drafts/ drift (Comms-tracked).

## Disposition

- No new blocker issues filed (the one real stale item, roadmap, is already #1128).
- Two workflow-improvement findings (#4, #5) recommended for the audit template — captured here + in the issue's Workflow Improvement section for PM.
- ports.md/ChromaDB drift (#2) left as a flagged follow-up (needs port confirmation, not a blind edit).
