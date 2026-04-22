# Omnibus Gap Remediation Tracker

**Opened**: 2026-04-22, ~11:45 AM
**Owner**: Docs
**Trigger**: During Apr 17-21 omnibus catch-up, discovered the Apr 16 omnibus (synthesized 2026-04-19) was built on an incomplete source-log set. Drift traced to Pattern-062 (Assembly Assumption) applied to omnibus synthesis — used the logs in tree without cross-checking against agent-mentions inside those logs.

---

## A. Apr 16 Omnibus — Source-Log Gaps

All four gaps confirmed via MD5 + size comparison after PM's 2026-04-22 re-download pass:

| Source | Gap type | Current location | Size |
|---|---|---|---|
| PPM 4/16 session log | Missing entirely | `dev/active/2026-04-16-1700-ppm-opus-log.md` | 4152B |
| CIO 4/16 session log | Missing entirely | `dev/active/2026-04-16-cio-session-log.md` | 3328B |
| HOST 4/16 standalone session log | Missing (artifact used) | `dev/active/2026-04-16-1656-host-session-log.md` | 1780B |
| Arch 4/16 session log | Partial (1965B in tree; full 2652B in dev/active) | `dev/active/2026-04-16-1613-arch-opus-log.md` | 2652B |

**Clean sources** (no action needed): Lead Dev, Docs, PA, CXO, Comms 4/16 logs were all complete when cited.

---

## B. Horizontal Walkthrough Result — Apr 15-21 Log Index

CSV at `docs/internal/planning/log-index-apr-15-21.csv`. Final state confirmed with PM:

| Role | Tue 15 | Wed 16 | Thu 17 | Fri 18 | Sat 19 | Sun 20 | Mon 21 |
|---|---|---|---|---|---|---|---|
| Lead Dev | ✓ | ✓ | ✓ | | | | |
| Docs | ✓ | ✓ | | ✓ | ✓ | | ✓ |
| PA | ✓ | ✓ | ✓ (artifacts) | ✓ | | | |
| CXO | | ✓ | | | ✓ | | |
| Comms | | ✓ | | | ✓ | | |
| Arch | | ✓ | | ✓ | ✓ | | |
| PPM | | ✓ | | | ✓ | | |
| CIO | | ✓ | ✓ | | ✓ | | |
| Exec | | | | | ✓ | | ✓ |
| HOST | | ✓ | | | ✓ | | |
| Code Agent | | | | | | | |

---

## C. Remediation Plan — Progress as of 2026-04-22 afternoon

### 1. Omnibus repair — ✅ COMPLETE
- ✅ **Amend Apr 16 omnibus** — done, commit `09c3e8a7`. Sessions 6 → 9. Added PPM/CIO/HOST content + richer Arch. Amendment note + provenance in omnibus footer.
- ✅ **Synthesize Apr 17 omnibus** — done, commit `00b23478`. STANDARD: COORDINATION, 3 sessions (Lead Dev, CIO, PA). CIO audit headline; PA artifact-only session.
- ✅ **Synthesize Apr 18 omnibus** — done. STANDARD: EXECUTION, 3 sessions (PA, Docs, Arch). Thirteen Mailboxes publish, skill v0.7, DECISIONS.md practice.
- ✅ **Synthesize Apr 19 omnibus** — done. HIGH-COMPLEXITY: COORDINATION, 9 sessions across 8 roles. Six parallel workstream reviews with source-discipline failure + correction. Sibling Intelligence publish. Log-maintenance hook.
- ✅ **Apr 20 dark day** — captured in Apr 19 omnibus footer per methodology-20 dark-day convention.
- ✅ **Synthesize Apr 21 omnibus** — done. STANDARD: COORDINATION, 2 sessions (Exec migration-decision conversation + Docs late-night publish/audit).

### 2. Notify Comms — ⏳ DEFERRED until Chat migration completes
- If the amended Apr 16 omnibus or new Apr 17-21 omnibus surface material that changes any published blog post's framing, Comms should be briefed. Candidate posts: Thirteen Mailboxes (Apr 18), Sibling Intelligence (Apr 19), Four Roles (Apr 21). Quick read suggests content still lands correctly; no material shifts. Will confirm after Chat migration makes Comms reachable in Code.

### 3. Workstream reviews + Weekly Ship #039 — ⏳ DEFERRED until Chat→Code migration
- Ship #039 covers Apr 10-16. The amended Apr 16 omnibus surfaces CIO Flywheel reformulation + PPM pathological-tagging memo + HOST 12-role assessment that weren't in Ship #039's narrative. PM direction 2026-04-22: defer Ship #039 amendment until leadership team migrates off Chat.
- Workstream reviews similarly deferred.

### 4. Housekeeping — ✅ COMPLETE
- ✅ Moved 13 session logs from dev/active/ to dated dirs (dev/2026/04/{16,18,19,21}/). Commit `09c3e8a7`.
- ✅ Replaced partial Arch 4/16 in dev/2026/04/16/ with richer 2652B version.
- ✅ Deleted 4 identical dev/active/ duplicates (Apr 14 Arch, Apr 16 CXO + Comms, Apr 17 CIO).

### 5. Process fix — `create-omnibus` skill — ✅ COMPLETE
- ✅ Added **Step 2.5: Cross-Reference Gate** to `.claude/skills/create-omnibus/SKILL.md`. Scans each source log for mentions of other agent roles (using canonical agent-vocabulary regex), compiles union of mentioned-roles, compares against source-set. Any mentioned-but-missing role → flag to PM before proceeding. Also covers artifacts dated on target. Gate fail means STOP + fetch, or document the gap explicitly in Sources (never silently paper over).

### 6. Retrospective audit — ⏳ DECISION PENDING
- Recommendation: mechanical check only (agent-mentions-vs-source-log-set), not full re-synthesis. Scope 1-2 weeks back from Apr 16 (so Apr 9-15).
- Trigger decision: PM to decide. The Apr 16 incident was a real drift; whether Apr 9-15 also had drift is unknown. Mechanical check is ~30 min; re-synthesis where gaps found is larger.
- Less urgent now that the process fix (Step 2.5) is in place for forward-looking protection, but still useful for historical accuracy.

### 7. Downstream consistency checks — ✅ PARTIAL / ⏳ REMAINING
- ✅ **BRIEFING-CURRENT-STATE.md** — refreshed 2026-04-22 morning; Apr 22 entry appended this afternoon with migration decision + omnibus drift remediation summary.
- ⏳ **DECISIONS.md** — scan newly-downloaded 4/16 logs (PPM, CIO, HOST) for decisions that should be captured. Not yet done; could be done autonomously or deferred to a light task window.
- ⏳ **Cross-pollination briefs Apr 17-22** (produced by Dispatch/CoS) — light re-read to check if any claim shifts. Not yet done.

### 8. Memory capture — ✅ COMPLETE
- ✅ Saved `feedback_omnibus_source_drift.md`. Captures: Pattern-062 applied to omnibus synthesis; the mention-without-citation signal; "never silently paper over the gap" directive. Indexed in MEMORY.md.

---

## D. Parking Lot — Other open items from our 2026-04-22 session

From the working queue that's been growing through the morning:

- **#996 audit close-out** — completed this morning (`ee337fe9`, #996 closed as completed)
- **Mail delivery** — together, when PM is ready
- **Standing items review** — queued
- **Chat roles migration news** — PM will share; will remove most/all Chat roles from manual bottleneck (topic 5)
- **Publishing-UI cowpath paving** — topic 6
- **Website management plan** — topic 7 (new, added 2026-04-22 morning)

Items that have downstream implications once Chat migration completes:
- Fix workstream reviews using new omnibus content
- Fix Ship #039 using new omnibus content
- Retire the Chat-role project knowledge refresh standing reminder (will become obsolete)

---

*This file is the canonical tracker. Session log references it by relative path; don't duplicate the plan here in the session log.*
