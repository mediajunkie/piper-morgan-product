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

## C. Remediation Plan (in order)

### 1. Omnibus repair (now)
- **Amend Apr 16 omnibus** — incorporate PPM, CIO, HOST standalone, and richer Arch content. Use `create-omnibus` skill with Step 7 canonical term verification. Update Sources section and `Sessions: N | Roles: N` tagline.
- **Synthesize Apr 17 omnibus** — CIO (methodology audit delivered), Lead Dev, PA (artifacts in dev/active). IAC conf day.
- **Synthesize Apr 18 omnibus** — Docs (Thirteen Mailboxes publish + skill v0.7), PA, Arch (new!).
- **Synthesize Apr 19 omnibus** — LARGE day: Docs (Sibling Intelligence publish + Apr 16 omnibus synthesis + log maintenance hook) + 7 Chat roles (Arch, PPM, CXO, Comms, HOST, CIO, Exec). **HIGH-COMPLEXITY probable.**
- **Apr 20** — dark day, likely no omnibus needed (0 sessions). Note in Apr 19 or Apr 21 omnibus footer.
- **Synthesize Apr 21 omnibus** — Docs (Four Roles publish + weekly audit #996), Exec. MINIMAL.

### 2. Notify Comms (after omnibus repair)
- If the amended Apr 16 omnibus or new Apr 17-21 omnibus surface material that changes any published blog post's framing, Comms should be briefed. Candidate posts: Thirteen Mailboxes (Apr 18), Sibling Intelligence (Apr 19), Four Roles (Apr 21).

### 3. Workstream reviews + Weekly Ship #039 (AFTER Chat→Code/Cowork migration)
- Ship #039 covers Apr 10-16. The amended Apr 16 omnibus may surface content that should update Ship #039's narrative. Deferred until leadership team migrates off Chat, per PM 2026-04-22.
- Workstream reviews similarly deferred.

### 4. Housekeeping (bundle with omnibus repair)
- Move dev/active/ logs to appropriate dev/2026/04/{16,17,18,19,21}/ directories.
- Replace partial Arch 4/16 in dev/2026/04/16/ with the richer version.

### 5. Process fix — `create-omnibus` skill
- Add an explicit **source-log cross-reference gate**: before synthesis, scan each source log for agent-role mentions and verify the referenced agent has a log of their own for that date (or explicitly document why not — e.g., "HOST role-health-check is an artifact, no standalone session log today").
- Bump skill version, update changelog.

### 6. Retrospective audit — earlier omnibus logs
- **Decision pending**: whether to audit Apr 9-15 omnibus logs for the same drift pattern.
- Recommendation: mechanical check only (agent-mentions-vs-source-log-set), not full re-synthesis. Scope 1-2 weeks.
- Trigger decision: after Apr 16-21 omnibus repair completes. If same pattern shows up, run the sweep; if not, stop.

### 7. Downstream consistency checks
- **BRIEFING-CURRENT-STATE.md** — refreshed 2026-04-22 morning using Apr 16 omnibus content. After amendment, light update may be needed if new decisions/blockers surface.
- **DECISIONS.md** — scan newly-downloaded 4/16 logs (PPM, CIO, HOST) for decisions that should have been captured. Retro-capture as needed.
- **Cross-pollination briefs Apr 17-22** (produced by Dispatch/CoS from omnibus content) — light re-read; amend if material shifts.

### 8. Memory capture
- Save feedback memory: Pattern-062 (Assembly Assumption) manifesting as omnibus synthesis drift. The methodology failure was that I used the set of logs in tree as the input set without cross-checking against references inside those logs. Future-me: when synthesizing an omnibus, first scan source logs for agent-role mentions, then verify the source set contains a log for each mentioned agent.

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
