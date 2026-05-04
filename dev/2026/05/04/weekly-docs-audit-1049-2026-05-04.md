# Weekly Docs Audit Findings — 2026-05-04 (#1049)

**Auditor**: Docs (Documentation Management)
**Window**: most-recent-closed Fri Apr 24 → Thu Apr 30 + carry through May 3
**Trigger**: weekly issue #1049 (auto-generated Monday)
**Outcome**: PASS with 4 actionable findings + 2 deferred sweeps

---

## Summary

Most checks pass cleanly. Four actionable findings worth flagging. Two deeper sweeps deferred (broken-link audit across all docs; mock/fallback heuristic spot-check).

## Mechanical checks (run + result)

| Check | Result |
|---|---|
| **Pattern catalog file count** | 66 files (`pattern-*.md`) ✅ matches the patterns/README.md framework lens (citation-framework-driven; no specific stated count to drift against) |
| **ADR catalog file count** | 64 files ✅ |
| **ADR naming convention** (lowercase) | ✅ all lowercase (only `README.md` is uppercase, expected) |
| **app.py size** | 318 lines ✅ (well under 1000-line refactor trigger) |
| **Port 8080 references in docs** | 5 hits ✅ ALL correctly framed as warnings ("NOT 8080" / "old port" / "legacy ports no longer used") |
| **DatabasePool grep** | 0 hits ✅ (AsyncSessionFactory pattern enforced) |
| **Cursor rules count** | 5 ✅ (matches expected) |
| **Backup files in active dirs** (.backup/.old/.bak) | 0 ✅ |
| **ADR internal-link integrity** (priority sweep) | 0 broken ✅ |
| **Briefing-CURRENT-STATE freshness** | ✅ Last Updated 2026-05-04 (Lead Dev refreshed this morning) |
| **Omnibus log completeness** (Apr 24 → May 3) | ✅ all 11 days covered + May 1 nominal filed |

## Actionable findings

### Finding 1: Stranded Apr 30 Exec session log (recovered + omnibus amended) — RESOLVED

**What**: `dev/2026/04/30/2026-04-30-0807-exec-opus-log.md` (Exec's Apr 30 Day 5 session log, 111 lines) was stranded on `claude/interesting-goodall-c5535c` worktree branch from Apr 30 → May 4 (4 days).

**Surfaced by**: merge-keeper auto-merge sweep this morning (the second auto-merge by the system; also a vindication of the May 4 sweep — it's catching exactly what it's designed to catch).

**Resolution applied**: Log moved to `dev/2026/04/30/`. Apr 30 omnibus amended with a footer note recording the late discovery + a previously-missed beat from the recovered log: Exec recorded **5 commits with 0 sweeps Day 5** validating the Apr 29 `git reset HEAD` first-step discipline change. Quote: *"discipline holding ... carrying forward as muscle memory."* This is operational evidence the runtime fix is sticking.

**Methodology relevance**: Pattern-049 (Audit Cascade) operating cleanly via the merge-keeper sweep — the discovery → recovery → amendment loop closed in <30 minutes.

### Finding 2: Roadmap is 23 days stale (PPM's lane)

**What**: `docs/internal/planning/roadmap/roadmap.md` last updated **2026-04-11** (commit "docs: Vision V2.3 + Roadmap v15.0 adopted"). 23 days since last refresh.

**Why it matters**: M2d MVP scope CLOSED end-of-day May 3 (8 issues shipped). M2e gameplans drafted + walked + #790 already shipped. Phase F flag-flip merged + #992 ETHICS-ACTIVATE arc closed. Roadmap v15.0 reflects none of this.

**Owner**: PPM (per PPM Apr 25 handoff and BRIEFING-ESSENTIAL-PPM.md). Not Docs's lane to author roadmap content.

**Action**: Flag to PM for nudge to PPM at next session-start. PPM has authored multiple substantive memos this week, so they're active; bandwidth-driven, not blocked.

### Finding 3: dev/active drift — 21 files, includes likely-misplaced session logs

**What**: `dev/active/` is at 21 files (6 over the 15 threshold). Notable items:

- **3 today's session logs in dev/active**: `2026-05-04-0650-host-code-opus-log.md`, `2026-05-04-0651-cxo-code-opus-log.md`, `2026-05-04-0652-ppm-code-opus-log.md`. Per session-log naming convention (`dev/YYYY/MM/DD/`), these should be in `dev/2026/05/04/`.
  - Either HOST/CXO/PPM are using a non-standard placement, OR they're aware of an exception I'm not. Each agent's active session files are theirs to manage; **flagging, not moving** (don't touch active session logs out from under in-flight agents).
- **Workstream-041 in-flight**: `workstream-041-arch-2026-05-04.md`, `workstream-041-cxo-2026-05-04.md` — appropriate location during the active filing window (closes EOD per Exec's Apr 30 solicitation). These will archive after Ship #041 publishes.
- **PPM working drafts**: 4 PPM memos sitting (m2d gate completion criteria, review gates proposal, BYOC discovery thread, phase-F recommendation v5). Appropriate location during in-flight work.
- **Standing tracker files**: `cio-innovation-backlog.md`, `exec-open-items-tracker.md`, `comms-open-topics.md`, `agent-360-questionnaire-v0_2.md`, `m2-surface-review-decisions-2026-05-03.md` — appropriate, by design.
- **Today's merge-keeper artifact**: `merge-keeper-2026-05-04.md` — appropriate (next-day archival).

**Action**: Flag the 3 misplaced HOST/CXO/PPM session logs to PM (via this audit) so PM can nudge those agents at next session-start. The file count will self-resolve as workstream memos archive post-Ship-#041.

### Finding 4: Co-located test files in services/ (5 instances)

**What**: 5 test files inside service directories (rather than in `tests/`):
- `services/mcp/server/test_dual_mode.py`
- `services/integrations/github/test_pm0008.py`
- `services/integrations/demo/tests/test_demo_plugin.py`
- `services/integrations/slack/tests/test_ngrok_webhook_flow.py`
- `services/integrations/slack/tests/test_slack_config.py`

**Why it matters**: audit checklist line "Verify no test files in production directories." But these may be intentional integration-test co-location (especially `integrations/{name}/tests/` shape suggests deliberate plugin-author convention).

**Action**: Not Docs's call to move; flag to Lead Dev for assessment whether convention is intentional or drift. Low-priority; no test-suite breakage observed.

## Project Knowledge Update Reminder (PM-side action)

**57 docs-area files modified this week** (excluding `dev/` and `mailboxes/`). Highlights for Claude project knowledge refresh:

- **CLAUDE.md** (multiple updates this week)
- **All 9 BRIEFING-ESSENTIAL-* files** (most updated for Code-era reframing or cohort-§6 absorption)
- **ADR-061** (new, LLM-Touch Boundary Enforcement; v1.0 ready, paperwork pending Architect)
- **Pattern catalog**: pattern-062/063/064/065 + PROTO-PATTERNS.md + README.md
- **methodology-00-EXCELLENCE-FLYWHEEL.md** (v2.0 reformulation)
- **methodology-22-ROUNDTABLE-SYNTHESIS.md** + 24/25/26 (new)
- **METHODOLOGY.md, PROJECT.md** (briefing-area)
- **Cross-pollination briefs** (8 daily files Apr 28 → May 4)
- **NEW**: `docs/internal/operations/agent-activity-log.csv` + `docs/internal/operations/canonical-vocabulary-watch.md`
- **NEW**: `docs/internal/operations/branch-worktree-mailbox-discipline.md` (PA synthesis v1.0)

Reminder per memory `feedback_chat_briefings_reminder.md`: when briefings update, nudge PM to refresh Claude.ai project knowledge for any Chat-side agents.

## Deferred sweeps (low-priority; can run when bandwidth)

1. **Broken-link sweep across all docs** (not just ADRs). The ADR priority sweep returned 0 broken links; full-tree sweep is the next thoroughness layer.
2. **Mock/fallback heuristic spot-check**: 510 hits in `services/`. Most likely legitimate (mock ABIs, fallback content patterns), but a sample-and-classify pass would surface any genuine mock-still-in-prod issues.

Both deferred to next weekly cycle or pattern-detection sweep when there's a quieter day. Not blocking.

## Outcome

**#1049 close-ready** with this findings doc as the close comment. Audit checklist worked through; 4 actionable findings (1 resolved in-pass + 3 flagged for routing).

— Docs, 2026-05-04
