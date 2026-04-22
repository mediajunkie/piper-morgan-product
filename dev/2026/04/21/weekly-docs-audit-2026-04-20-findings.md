# Weekly Docs Audit Findings — Issue #996 (2026-04-20)

**Auditor**: Docs (Claude Code / Opus)
**Run date**: 2026-04-21, ~11:20 PM
**Prior audit**: #977 (2026-04-13, closed Apr 15)
**Source checklist**: issue #996

## TL;DR

- **Infrastructure**: clean (web/app.py 307 lines, port 8001 canonical, cursor rules present, ADR=63, patterns=63 files)
- **Link integrity**: 3 broken links found and fixed in `pattern-049-audit-cascade.md` (wrong relative depth — `../../` should have been `../../../`). ADRs and briefings are clean.
- **Stale content**: `BRIEFING-CURRENT-STATE.md` is 6 days old (1 day from PM's 7-day warning); `roadmap.md` is 10 days old (stale, PM action requested).
- **dev/active/ duplicates**: 3 macOS-style duplicate files (`… (1).md`, `… (2).md`) — candidates for cleanup, PM review requested.
- **Omnibus coverage**: complete through Apr 16; Apr 17, 18, 19, 20 pending (PM already deferred 17/18 to tomorrow).
- **Pattern README**: count line 6 is self-inconsistent ("63 patterns (001-062) + template (000)" — 001-062 is 62 patterns, not 63). Footer line 194 correctly says 62. One-line fix; flagging for PM.
- **Mock/fallback sweep**: 86 files in `services/` contain `mock_` or `fallback`. Too many to triage inside an audit — likely a mix of legitimate (publisher fallback) and concerning (LLM adapters). Recommend PM scope a separate issue.
- **Quality checks**: no TODO/FIXME in prod code; no `.backup`/`.old` files outside archive; no broken links in briefings; no broken links in ADRs.

## Completion Matrix

| Section | Status | Evidence |
|---------|--------|----------|
| Claude Knowledge Updates | ⏸️ | PM-action section — list of modified files provided below; updating Claude.ai project knowledge is a manual PM step |
| Link Integrity Check | ✅ | ADRs clean, briefings clean, patterns had 3 broken refs in pattern-049 — fixed in this audit |
| Infrastructure Verification | ✅ | Evidence table below |
| Session Log Management | ⚠️ | Omnibus through 04-16 complete; 04-17/18 deferred by PM; 04-19/20 unsynthesized. dev/active has 15 files including 3 macOS dups |
| Sprint & Roadmap Alignment | ⚠️ | roadmap.md 10 days stale; BRIEFING-CURRENT-STATE 6 days stale |
| GitHub Issues Sync | ✅ | 132 open, 14 without milestone (all recent — #982-#996 range, likely needs milestone assignment once sprint boundaries settle) |
| Pattern & Knowledge Capture | ⚠️ | Line 6 / line 194 count inconsistency in patterns/README.md — small fix |
| Quality Checks | ✅ | 0 TODO/FIXME in services/web/cli; no backup files; pattern numbering contiguous (000-062) |

---

## Infrastructure Verification (evidence)

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| `wc -l web/app.py` | <1000 (refactor at 1000) | 307 | ✅ |
| 8080 references in docs | none or warnings only | 7 files, all warnings ("not 8080", "legacy", "old port") | ✅ |
| `.cursor/rules/` file count | 5 | 5 (architecture-patterns.mdc, completion-discipline.md, github-tracking.mdc, programmer-briefing.mdc, verification-first.mdc) | ✅ |
| Pattern files | matches README | 63 files (000 template + 001-062) | ✅ (but README line 6 math is off) |
| ADR files | consistent numbering | 63 files, all lowercase | ✅ |

## Link Integrity — Fixed This Audit

Scanned ADRs, patterns, briefings for broken internal `.md` links.

**Broken links found & fixed**:
- `docs/internal/architecture/current/patterns/pattern-049-audit-cascade.md` lines 173-175: three methodology-core references used `../../development/methodology-core/...` but actually need `../../../development/methodology-core/...` (one extra `..` because `patterns/` is nested under `current/architecture/internal/docs/`). Fixed in place.

**Clean**:
- All ADRs (adr-001 through adr-063): 0 broken links
- All briefings (docs/briefing/*.md): 0 broken links

## Stale Content

| File | Last Updated | Age | Threshold | Status |
|------|--------------|-----|-----------|--------|
| `docs/briefing/BRIEFING-CURRENT-STATE.md` | 2026-04-15 | 6 days | 7-day warn | ⚠️ approaching |
| `docs/internal/planning/roadmap/roadmap.md` | 2026-04-11 | 10 days | n/a explicit, but should reflect sprint | ⚠️ stale |

**Recommendation**: PM or CIO refresh BRIEFING-CURRENT-STATE this week. Roadmap refresh is overdue given #950/#964/M2b work completed.

## Pattern README Count Fix Candidate

`docs/internal/architecture/current/patterns/README.md`:
- Line 6: `**Total Patterns**: 63 patterns (001-062) + template (000)` — 001-062 = **62 patterns**, so total should read either "62 patterns (001-062) + template (000)" (63 files) or just "63 pattern files". Line is internally inconsistent.
- Line 194: `_Added Human-AI Collaboration Referee (061); total now 62 patterns_` — correct, matches file count.

Did not fix — PM should choose canonical wording (is the template counted as a pattern? it's `pattern-000-TEMPLATE.md` which suggests no).

## dev/active/ Hygiene

15 files present; expected to contain current work-in-progress only. Concerns:

**macOS duplicate copies** (candidates to delete):
- `exec-open-items-tracker (1).md` (original `exec-open-items-tracker.md` also present)
- `weekly-ship-039-draft (1).md`
- `weekly-ship-039-draft (2).md`
  (original `weekly-ship-039-draft.md` also present)

**Recent work-in-progress (appropriate to be here)**:
- `ethics-metadata-decision-record-2026-04-17.md` (PA)
- `methodology-doc-reference-audit-2026-04-17.md` (PA)
- `host-role-health-check-2026-04-16.md` (HOST)
- `iac-speaker-notes.md`, `iac-talk-review-2026-04-08.md`, `ia-conference-talk-outline-2026-04-17.md`, `ethics-as-ia-draft.pptx(+.pdf)` (IAC conf materials, likely safe to archive now that conf is done)
- `managed-agents-assessment-2026-04-14.md`

**Recommendation**: PM review — (a) approve deletion of 3 macOS dups, (b) decide whether to archive IAC talk materials to `dev/2026/04/17/` now.

## Omnibus Coverage

| Date | Omnibus present | Notes |
|------|-----------------|-------|
| 2026-04-14 | ✅ | |
| 2026-04-15 | ✅ | |
| 2026-04-16 | ✅ | Synthesized 2026-04-19 (HIGH-COMPLEXITY: COORDINATION) |
| 2026-04-17 | ❌ | **Deferred by PM to 2026-04-22** |
| 2026-04-18 | ❌ | **Deferred by PM to 2026-04-22** |
| 2026-04-19 | ❌ | Light day (travel + Sibling Intelligence publish) — Docs session log exists |
| 2026-04-20 | ❌ | No session logs found for 2026-04-20 (per file system + git log) |

## GitHub Issues — Milestone Gaps

14 open issues without a milestone, all in the #982-#996 range (created Apr 16-20). Examples: #996 (this audit), #982 (FLY-AUDIT), #985-#990 (CONTEXT/HYGIENE/ETHICS work), #991-#995 (ETHICS/TEST/FABRICATION). These are recently filed — assigning to M2b/M2c/M3 is a planning decision, not an audit failure. Flagging for next sprint triage.

## Mock/Fallback Sweep — Scope Issue

`grep -rln "mock_\|fallback" services/ --include="*.py"` returned **86 files**. Sample:

```
services/publishing/publisher.py
services/intent_service/llm_classifier.py
services/intent_service/workflow_dispatcher.py
services/llm/*
services/database/models.py
...
```

This is too broad for an audit to triage responsibly. Many are likely legitimate (publisher fallback paths, config fallbacks), some may be concerning (LLM adapter mocks that should be deleted post-Haiku-3 cleanup #979). **Recommend**: PM scope a dedicated mock-sweep issue for Lead Dev.

## Docs Modified This Week (for Claude.ai knowledge refresh)

Non-session-log / non-dev/ files modified since 2026-04-14:

- `CLAUDE.md` — session log maintenance section added (Apr 19)
- `DECISIONS.md`
- `.claude/skills/create-omnibus/SKILL.md` — Step 7 mandatory verify-canonical-references
- `.claude/skills/publish-to-blog/SKILL.md` — v0.7 (YAML frontmatter + heading convention)

**Total .md files changed this week**: 180 (most are session logs under `dev/`).

## Metrics Snapshot

| Metric | Value |
|--------|-------|
| .md files in docs/ | 1,282 |
| Pattern files | 63 (000 template + 001-062) |
| ADRs | 63 |
| Open issues | 132 |
| Open issues without milestone | 14 (all recent, #982-#996) |
| Omnibus logs in docs/omnibus-logs/ | 16 April entries (04-01 through 04-16) |
| TODO/FIXME in services/web/cli | 0 |

## Proposed Close-Out Actions (for PM approval tomorrow)

1. ✅ **Already done this audit**: Fixed 3 broken links in pattern-049-audit-cascade.md.
2. ⏳ **PM review**: Pattern README line 6 count wording (see above).
3. ⏳ **PM review**: Delete 3 macOS-duplicate files in dev/active/.
4. ⏳ **PM review**: Archive IAC talk materials from dev/active/ to dev/2026/04/17/ now that conf is done.
5. ⏳ **PM action**: Refresh BRIEFING-CURRENT-STATE (6 days old) and roadmap.md (10 days old) when practical — likely a CIO task as part of M1 methodology audit window.
6. ⏳ **Deferred**: Apr 17/18 omnibus (PM explicitly deferred to 2026-04-22).
7. ⏳ **Flag to PM**: Open a scoped issue for LLM-mock/fallback sweep (86 hits — too broad for audit).
8. ⏳ **Flag to CIO/PM**: 14 open issues without milestones (recent batch).

## Not Completed / Deferred

- **Claude Knowledge Updates checklist** (PM manual step — flagged with doc list above)
- **Apr 17/18/19/20 omnibus** (PM deferred to 2026-04-22)
- **Scoped mock/fallback triage** (flagged as out-of-scope for audit)
- **Staggered audit calendar update** (`docs/internal/operations/staggered-audit-calendar-2026.md`) — PM does this on issue close per checklist

---

*Audit conducted in a single pass using parallel Bash queries + the audit-cascade skill's "fix obvious cases" guidance for the broken-link findings. No subagents were necessary at this scope.*
