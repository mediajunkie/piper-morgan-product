# Weekly docs audit, 2026-11-02 (read-only)

Method: script /private/tmp/claude-501/-Users-xian-Development-piper-morgan-worktrees-docs/d53dfc9c-6531-4dff-8f8c-4d0f84c42995/scratchpad/audit.py run with `python3 -I audit.py` from the docs worktree. Output saved beside it as audit-out.txt. Scope: os.walk of docs/, skipping any path containing omnibus-logs, archive or history (case-insensitive).

## 1. Stale content
- Total .md files scanned: 1850. Files carrying a "Last Updated" / "last_updated" / "Updated:" ISO date: 348. Candidates (newest such date before 2026-10-03, i.e. more than 30 days before 2026-11-02, and body matching currently / as of / current version / this sprint / active): 134 of 1850.
- Caveats: the regex takes the newest date among matches in a file. "active" matches many incidental uses, so 134 is an upper bound and overstates true staleness. Files with no machine-readable date were not assessed (unverified). Date format other than YYYY-MM-DD missed (unverified).
- Oldest 15 examples (date, path):
  - 2025-08-08 docs/public/user-guides/legacy-user-guides/getting-started-conversational-ai.md
  - 2025-08-09 docs/public/user-guides/legacy-user-guides/conversation-memory-guide.md
  - 2025-09-02 docs/internal/development/tools/session-log-templates/INDEX.md
  - 2025-09-21 docs/internal/development/methodology-core/methodology-05-AGENT-METHODOLOGY.md
  - 2025-09-21 docs/internal/development/methodology-core/resource-map.md
  - 2025-09-29 docs/migration/router-migration-guide.md
  - 2025-11-12 docs/testing/integration-test-strategy.md
  - 2025-11-13 docs/internal/design/audits/2025-11-ux-audit/ux-audit-phase1-technical-constraints.md
  - 2025-11-13 docs/internal/design/audits/2025-11-ux-audit/ux-audit-phase1-touchpoint-inventory.md
  - 2025-11-14 docs/internal/design/audits/2025-11-ux-audit/ux-audit-phase3-design-system-implementation.md
  - 2025-11-14 docs/internal/design/audits/2025-11-ux-audit/ux-audit-phase4-addendum-document-management.md
  - 2025-11-14 docs/internal/design/audits/2025-11-ux-audit/ux-audit-phase4-gap-analysis.md
  - 2026-01-08 docs/internal/design/README.md
  - 2026-01-20 docs/internal/design/mux/journal-architecture-spec.md
  - 2026-01-26 docs/internal/architecture/current/feature-object-model-map.md

## 2. Duplicates
- Same basename in 2 or more directories: 5 groups out of 2042 distinct basenames (all file types under docs/, same exclusions).
  - README.md in 90 directories (expected, benign)
  - INDEX.md in 3 (session-log-templates, methodology-core, architecture/bets)
  - troubleshooting.md in 2 (docs, docs/installation)
  - universal-list-architecture-guide.md in 2 (docs/internal/development/tools and tools/implementation-guides)
  - from-protocol-to-infrastructure.md in 2 (docs/public/comms/drafts/superseded and drafts/published)
- Suffix variants ("(1)", -copy, _copy, -old, -v2 at end of basename): 14 files, all -v2 (no (1), -copy or -old found). 12 shown by the script's first 15 cut, all 14 listed here:
  - docs/internal/design/specs/canonical-queries-v2.md
  - docs/internal/development/planning/plans/gameplan-core-ui-fix-v2.md
  - docs/internal/testing/historical/canonical-query-test-matrix-v2.md (note: path contains "historical" which the exclusion rule `history` does not match, so it is counted)
  - docs/public/comms/leadership-playbook/ai-leadership-playbook-outline-v2.md
  - 10 files in docs/public/comms/drafts/superseded/ (draft-audit-cascade-v2, draft-fixing-the-foundation-v2, draft-the-planning-caucus-v2, draft-tokens-vanished-v2, weekly-ship-026-draft-v2, draft-the-completion-discipline-v2, draft-75-percent-complete-v2, draft-entities-experience-moments-v2, draft-the-drift-we-didnt-see-v2, draft-stranger-test-v2)
- I did not check whether each -v2 has a matching un-suffixed sibling (unverified).

## 3. Cross-references
- Command: `ls methodology-*.md | wc -l` in docs/internal/development/methodology-core gave 58 files.
- Command: loop `grep -q "$f" INDEX.md` over each methodology-*.md. Missing from INDEX.md: 0 of 58.
- Command: `grep -o 'methodology-[0-9A-Za-z_-]*\.md' INDEX.md | sort -u` gave 59 distinct tokens, one with no file in that directory: methodology-as-code-2025.md. This is a false positive. It is a substring of the link target docs/internal/architecture/current/design-record-methodology-as-code-2025.md (INDEX.md lines 18, 44, 72), and I confirmed that file exists with `ls`. So index entries with no file: 0 real.
- Command: `grep -n "methodology-core" docs/NAVIGATION.md`. NAVIGATION.md mentions methodology-core/INDEX.md at lines 126 and 448. Pass.
- Not checked: that INDEX.md descriptions match file contents (unverified).
