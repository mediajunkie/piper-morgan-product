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
