# Weekly docs audit, 2026-11-09 (read-only, run by Docs at 10:14 PT, issue #2332)

Method: commands from the issue checklist run directly from the docs worktree at origin/main, no subagent. Layer: file text and git history. Items outside Docs' lane are reported, not edited.

## Briefing and currency
- BRIEFING-CURRENT-STATE: `last_updated: 2026-11-09`, last commit 11-09 06:28 (Arch's beta-line refresh). Fresh, not edited by me.
- `check-staleness.py`: 38 of 39 docs OK, 1 needs attention. #972 adoption: 27 of 39 carry `last_verified`.
- `check-last-verified-drift.py`: 39 docs, 27 flagged. 5 are EDITED-UNBUMPED (body changed after the stamp). The rest I saw (README, ROLE-PORTFOLIO-FRAMEWORK, ROLE-PORTFOLIO-LEAD-DEV, ROSTER) are "last_verified moved with no body change" on 06-19 (d3151ab535), the known bulk stamp. Reported as a ratio, owners to decide, nothing re-stamped.
- Clustering of `last_verified` in briefing and agent-protocols: 12 on 2026-10-31, 7 on 2026-11-02, 3 on 2026-11-06, 2 on 2026-10-27. A cluster of 12 and 7 on two dates reads as two refresh passes, not per-doc verification.
- Docs-owned: BRIEFING-ESSENTIAL-DOCS has `last_updated` 2026-11-07, `last_verified` 2026-11-02. I did not re-stamp it this run because I did not re-read every claim in it today.

## Links and structure
- ADR internal links: 0 broken. Pattern files: 0 broken. Briefing files: 0 broken (relative `.md` links only).
- Briefings: all 12 `BRIEFING-ESSENTIAL-*` files named in ROSTER exist plus `BRIEFING-piper-alpha.md`.
- Omnibus coverage 11-02 to 11-08: 7 of 7 present, no gap over 2 days.
- `dev/active/`: 101 entries, no stranded session logs by name. (Not triaged: monthly housekeeping owns cleanup.)
- Backup files (`*.backup`, `*.old`) tracked in git: none found in the search I ran.

## Roadmap and issues
- roadmap.md last commit 2026-11-06 05:17, 3 days old, under the 14-day line. No report to PPM owed.
- Open issues: 374. Without a milestone: 0. No update in 30 days (before 2026-10-10): 73. Reported as a count, not triaged.

## Patterns and README
- 76 `pattern-*.md` files. Every numbered file is referenced in `patterns/README.md`. README says 75 patterns (001-075) plus template (000). No undocumented pattern found. I did not reconcile 76 files against 75 plus a template beyond that.
- docs/README.md version v0.9.0.0 matches `pyproject.toml` 0.9.0.0. No "NEW:" markers in root README or docs/README.

## Added after the first pass
- Methodology-core cross-references: 0 broken of 72 files (relative .md links). NAVIGATION.md mentions methodology-core.
- TODO or FIXME in services, web and cli (.py, .js, .html): 106 occurrences. Count only, not triaged (code owners').
- CITATIONS.md exists at docs/references/CITATIONS.md. Its attribution completeness I did not re-read this week.

## Not done this week (named)
- Stale-content and duplicate scans: not rerun, the 11-02 report is the latest (1850 files, 134 upper-bound stale candidates, 5 duplicate-basename groups). A cheap rerun is due at the next weekly.
- CITATIONS.md attribution read and the root-README review document: not done. Reason: each needs a full read and I put the time into the checks above. Next weekly.
- Sprint goals in config/PIPER.user.md: PPM and PM's, not touched.
