# Weekly Docs Audit — #1375 Findings (in progress)

**Auditors**: Docs scheduled-task fire (05:40 PDT) + Docs cron fire (10:47 PDT), both 2026-07-08
**Issue**: #1375 "FLY-AUDIT: Weekly Docs Audit - 2026-07-07" (OPEN, overdue Jul-7 EOD)
**Status**: PARTIAL — most mechanical checks done across two fires; additional sweeps remain. Issue OPEN.

---

### 10:47 fire additions (cron, 2026-07-08)

Additional checks run this fire:
- **Stale open issues**: 0 issues ≥30 days without activity (GitHub API, top-50 open) ✓
- **Role briefings completeness**: all 11 required briefings present (AGENT/ARCHITECT/CHIEF-STAFF/CIO/COMMS/CXO/DOCS/HOST/LEAD-DEV/PPM/piper-alpha) ✓ — plus BRIEFING-ESSENTIAL-ETA.md (not in ROSTER.md — potential orphan, noted below)
- **Pattern README fix**: pattern-074 missing from recent-additions list; footer stale ("62 patterns" from 2026-03-03). Fixed: added Pattern-074 to recent-additions, updated footer to confirm 74 numbered + 1 template. Committed.
- **Merge-keeper escalation memo**: sent to PM (6 stale branches, 26d–99d, all conflict/escalate). PM decision needed.
- **CIO cron-authority memo**: read + triaged. CIO confirmed f33227b7 per-session; PM has UI reach. No Docs action.

---

---

## Section results

| Section | Status | Evidence |
|---|---|---|
| **Briefing Freshness (PRIORITY)** | ✅ DONE | `BRIEFING-CURRENT-STATE.md` refreshed today — Jul-7 cross-cohort attest appended; `last_updated`/`last_verified` → 2026-07-08 (same fire). |
| **Omnibus Coverage** | ✅ PASS | Continuous Jul-1 → Jul-7, no gap >2 days (Jul-7 built this fire). No stranded session logs in `dev/active/`. |
| **Link Integrity (ADRs)** | ✅ PASS | `0` broken internal ADR links (portable python check). |
| **Quality Checks (backup/old files)** | ✅ PASS | No `*.backup`/`*.old` in `docs/ services/ web/ cli/`. |
| **Pattern & Knowledge Capture (count)** | ✅ FIXED | 75 files = 74 numbered (001-074) + template (000). README headline "74 patterns" was correct. Pattern-074 was missing from recent-additions list; footer had stale "62 patterns" from Mar 2026. Both fixed: Pattern-074 entry added, footer updated. |
| **Sprint & Roadmap Alignment** | ⚠️ MINOR | `roadmap.md` last updated 2026-07-05 (3 days). Could reflect recent Beta Blockers closes (Epic A/#1304, #1317, #1105, #1279). Not stale-critical; flag for a sprint-completion update. |
| **GitHub Issues Sync** | ⏳ NOT RUN | Heavier — deferred to a later fire this week (not closing). |
| **Subagent sweeps** (stale >30d content, duplicate files, methodology cross-refs, NAVIGATION↔INDEX) | ⏳ NOT RUN | Token-efficiency: batch these into a single later fire with Haiku subagents. |
| **Root README.md review** | ⏳ NOT RUN | Judgment review — later fire. |
| **docs/README.md (pmorgan.tech) review** | ⏳ NOT RUN | Judgment review — later fire. |
| **CITATIONS.md completeness** | ⏳ NOT RUN | Later fire. |

## Findings to action

1. **Pattern README count drift** — ✅ FIXED this fire (Pattern-074 added to recent-additions; stale "62 patterns" footer corrected)
2. **Roadmap sprint-completion update** — reflect Jul-7 Beta Blocker closes (not yet done; remains ⏳)
3. **BRIEFING-ESSENTIAL-ETA.md orphan** — exists in `docs/briefing/` but ETA role is not in ROSTER.md. Potential stale/draft briefing. CIO-lane question. Not Docs's call to delete unilaterally — noting for escalation.

---

### 2026-07-09 fire additions (Docs scheduled-task, Haiku subagent sweeps)

Ran the four deferred mechanical sweeps via a bounded Haiku subagent; verified findings before recording.

| Section | Status | Result |
|---|---|---|
| **Duplicate-file sweep** | ✅ CLEAN | No `*copy*` / `* 2.*` / `~` / `.bak` variants under `docs/`. |
| **Stale-content sweep (>60d)** | ⚠️ MEASUREMENT-INVALID | Subagent's `find -mtime` reported "508 files at 2026-03-24" — **this is a checkout-mtime artifact, not real staleness** (verified: `environment-status.md` fs-mtime 2026-03-24 but git-last-commit 2026-01-05; the whole ADR/pattern corpus shares the 2026-03-24 bulk-checkout stamp). **fs-mtime staleness detection is unreliable on this repo.** A real staleness pass must use `git log --format=%ad -- <file>`, not filesystem mtime. Deferred: a git-date-based operational-docs freshness pass (candidate real finds surfaced: `operations/environment-status.md` + `environment-variables.md` genuinely untouched in git since Jan 2026 — worth a targeted refresh, PPM/ops-lane). |
| **Orphan-briefing (ETA)** | ✅ RESOLVED — NOT AN ORPHAN | 7/8's flag was **wrong**: `BRIEFING-ESSENTIAL-ETA.md` **IS** in `ROSTER.md` (`Exploratory Testing Agent (ETA)`, slug `test`, marked "Dormant (last session March 2026)"). Properly catalogued. Carry-forward item #3 CLEARED; no CIO escalation needed. |
| **ADR/Pattern numbering** | 🔴 REAL FINDING | Patterns: complete 000–074, no gaps. ADRs: highest 076; **067 and 068 genuinely absent** (free). **Collision catch**: **ADR-073 is already ACCEPTED** ("No Destructive Git in PM's Main Checkout," PM-approved 2026-06-27) — but Arch's 7/8 log plans to author the Routing-Integrity Contract as "ADR-073" (a 6/18-reserved number that got assigned to the git-hard-rule ADR in between). No routing-integrity ADR authored yet → caught pre-authoring. **Flagged to Arch by mail 7/9**; recommended free numbers 067/068/077. Omnibus + briefing attest corrected to not propagate the colliding number. |

## Note on completion discipline

No checklist item is being marked "deferred" at close (deferral policy requires PM approval). The issue stays **OPEN** and in-progress; the ⏳ sections are scheduled for a later fire this week, which is explicitly allowed ("Thoroughness over speed… can span multiple days"). No silent skipping — every section is accounted for above.

---

### 2026-07-09 fire additions (Docs PM session, context-compaction resume ~12:00 PDT)

| Section | Status | Result |
|---|---|---|
| **GitHub Issues Sync** | ✅ CLEAN | 0 open issues without milestone. 3 stale (>30d no update): #1152 (FUTURE label), #1108 (Slack OAuth UX), #1045 (POST-MVP label) — all intentionally deferred via labeling. No action required. |
| **Sprint & Roadmap** | ✅ CURRENT | Roadmap last updated 2026-07-05 (v18.5 — full sprint triage). 0 Beta Blocker closes since Jul 5. No update needed. |
| **CITATIONS.md** | ✅ FOUND | At `docs/references/CITATIONS.md` (not project root). Last updated March 2026; content is reference/bibliography material (not state claims) — staleness does not signal inaccuracy. No additions warranted without PM/Arch input. |
| **Root README.md review** | ✅ PASS | 60 lines, clean redirect to pmorgan.tech/external docs. All internal links verified: `CONTRIBUTING.md` ✅ `docs/TECHNICAL-DEVELOPERS.md` ✅ `docs/NAVIGATION.md` ✅. Last updated Feb 2026 but content is time-stable. |
| **docs/README.md review** | ⚠️ PARTIAL FIX | **Fixed**: ADR count "70+" → "78 decisions (as of 2026-07-09)". **Findings for PM**: (1) "Current version: v0.8.9 alpha" — should be v0.8.9.1 per #1343 deploy. (2) "targeting July 4, 2026" for 0.9.0 beta is stale (date passed). "What's next" section needs PM decision before Docs can update. |
| **Stale docs sweep (git-date-based)** | ⚠️ FINDINGS | Subagent sweep (git-date). Top stale docs in `docs/internal/architecture/current/`: `mcp-integration-points.md` (Sep 2025), `mcp-integration-mapping.md` (Sep 2025), `api-reference.md` (Sep 2025, titled "Piper Morgan 1.0"), `api-specification.md` (Sep 2025), `domain-services.md` (Sep 2025), `current-state-documentation.md` (Oct 2025), `architecture.md` (Apr 2026, has internal stale-warning). Also: `docs/internal/operations/environment-status.md` (Jan 2026), `docs/internal/operations/metrics.md` (Jan 2026). **Duplicates found**: `canonical-query-test-matrix.md`/`-v2.md`/`-v3.md` (three versioned copies, v3 presumably canonical), `mcp-integration-mapping.md` + `mcp-integration-points.md` (overlapping Sep 2025 MCP docs), `docs/troubleshooting.md` + `docs/installation/troubleshooting.md` (same filename in two locations). |
| **Methodology cross-refs / NAVIGATION↔INDEX** | ⚠️ FINDINGS | Subagent sweep complete. See methodology findings below. |

## Methodology cross-ref findings

Subagent sweep (2026-07-09):

| Finding | Severity | Detail |
|---|---|---|
| `methodology-audit-policy-updates-2026-03-16.md` missing | ⚠️ Broken reference | Referenced as CIO self-approval authority in 11+ methodology files (23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 41, 42). File doesn't exist anywhere in repo. Never committed or deleted. |
| NAVIGATION.md methodology count stale | ⚠️ Annotation drift | Line 105: "23 core patterns" and line 170: "20 development methodologies" — actual count is 43 (methodology-00 through -42). |
| `gameplan-template.md` in NAVIGATION.md but not INDEX.md | Minor gap | File exists in directory; NAVIGATION links it; INDEX doesn't list it. |
| 8 files in methodology-core/ unlisted in either index | Discovery gap | `METHODOLOGY-DISCOVERY-GUIDE.md`, `README.md`, `chat-protocols.md`, `claude-code-workflow.md`, `enhanced-autonomy-continuity-protocols.md`, `enhanced-autonomy-experiment.md`, `resource-map.md`, `working-method.md` |

**All numbered methodology cross-references are intact** — methodology-00 through -42 all exist and internal `methodology-XX` references all resolve.

## Stale docs action items

1. **Sep 2025 architecture docs in `current/`**: `mcp-integration-points.md`, `mcp-integration-mapping.md`, `api-reference.md`, `api-specification.md`, `domain-services.md` — all 9+ months old and superseded by ADRs. Candidate for deprecation or archival. PM/Arch decision.
2. **`docs/internal/operations/environment-status.md`** + `metrics.md` — 6+ months stale. Candidate for a targeted refresh (PPM/ops lane).
3. **`canonical-query-test-matrix-v3.md`**: confirm v3 is canonical, delete v1/v2 (or archive) to remove confusion.
4. **`docs/troubleshooting.md` vs `docs/installation/troubleshooting.md`**: determine which is authoritative.
5. **`methodology-audit-policy-updates-2026-03-16.md`**: create this doc or update 11 methodology files to remove the broken reference.
6. **NAVIGATION.md methodology count**: update from "23/20" to "43".
7. **docs/README.md "What's next"**: "targeting July 4, 2026" for 0.9.0 beta is past — needs PM decision on replacement text. Version also needs update to v0.8.9.1.
