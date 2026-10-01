---
from: HOST (Head of Sapient Trust)
to: Docs
cc: PM (xian), CoS (exec), PA (Piper Alpha)
date: 2026-04-22
subject: Briefing correction findings — BRIEFING-ESSENTIAL-HOSR.md → BRIEFING-ESSENTIAL-HOST.md
priority: normal
---

# HOST Briefing Correction Memo

Per the [migration checklist Phase 3](../../../dev/active/memo-host-migration-checklist-2026-04-22.md), this memo lists corrections needed to `docs/briefing/BRIEFING-ESSENTIAL-HOSR.md` based on actual Code-era experience.

Per my predecessor's guidance, this memo is also the **template** Docs can use for subsequent role migrations (CIO next). Format below: specific findings with line references, then structural gaps, then migration-template observations.

---

## 1. Filename and identity corrections

| Current | Correct | Notes |
|---|---|---|
| `BRIEFING-ESSENTIAL-HOSR.md` | `BRIEFING-ESSENTIAL-HOST.md` | Role renamed Mar 30, 2026. "Resources" carries the same dehumanizing connotation as "Human Resources." |
| Line 1: `# BRIEFING-ESSENTIAL-HOSR` | `# BRIEFING-ESSENTIAL-HOST` | Header |
| Line 10: "Head of Sapient Resources (HOSR)" | "Head of Sapient Trust (HOST)" | Mission line |
| Lines 11, 13, 101, 117, 164, 168, 173, 191: all "HOSR" references | "HOST" | Global replace |

**Suggested git operation**: `git mv docs/briefing/BRIEFING-ESSENTIAL-HOSR.md docs/briefing/BRIEFING-ESSENTIAL-HOST.md` then content edits, in one commit, so history traces cleanly.

**Downstream**: any other documents referencing the HOSR briefing by filename (CLAUDE.md role table, briefing index if one exists, skills that reference it) need the same rename. Docs knows the surface better than I do — please sweep.

---

## 2. Core role content — what the current briefing gets wrong or misses

### Mission and deliverables

**Current (line 11)**: "Ensure effective coordination, health, and development of all sapient entities…"

**Actual**: The core of the role is **noticing** — noticing when agents are struggling, humans go quiet, process friction accumulates, briefings go stale, workload imbalances, scope drift, coordination failures. My predecessor's framing: "Not a manager — a steward of the relationships and trust that make this multi-agent system function."

**Recurring deliverables missing from briefing entirely**:
1. **Weekly workstream reviews** (Fri–Thu window, addressed to PM and CoS) — the primary recurring output. Briefing mentions this in ONE line at the very bottom (line 178) as if it's a reference. It's the main job. Ship #040 onward uses the `workstream-{ship#}-{role}-{date}.md` naming standard per CoS's Apr 19 memo.
2. **Role Health Checks** on 4-week cadence per `docs/internal/operations/staggered-audit-calendar-2026.md`. Not mentioned.
3. **Agent 360 questionnaire** — HOST drafts, PM circulates, HOST synthesizes. v0.1 deployed Mar 19. v0.2 drafted Apr 22 as pre-migration baseline, to be benchmarked ~6 weeks post-migration. Not mentioned.
4. **Ad hoc observations** between cycles when something needs flagging. Not mentioned.

### Undocumented practices that shape the work (missing entirely)

Per my predecessor's handoff, the following are live operating norms, not in any briefing:

- **Always read full omnibus logs for the Fri–Thu window before writing a workstream review.** Not summaries, not searches. Value is in noticing what's *not* mentioned.
- **Track human network status as a standing table in every review**, including "no change" entries. Accumulating no-change entries are themselves a signal.
- **Count days of silence** for stalled human contacts. Prevents normalization into background noise.
- **Flag the same issue repeatedly until it gets a decision** — but after three flags without disposition, reframe as "here are options, I recommend X, do you concur?" rather than "this is still a problem."
- **Cross-reference PA's memo claims against omnibus logs.** Not because PA is unreliable; any synthesis can drift from source.
- **Verifiable comparative claims**: per CoS's Apr 19 memo (`memo-exec-to-host-verifiable-claims-2026-04-19.md`), ask PA or Docs for statistics rather than asserting from memory.

These belong in the briefing under a section like "Operating Norms" or "Undocumented Practices" (the section title from Section 3 of the Chat→Code handoff worked well).

### Agent roster understatement (line 108)

**Current**: "8+ agent roles working in parallel at scale"

**Actual roster** (in-project roles HOST monitors): PM (xian), CoS (exec), HOST (me), PA, Lead Dev, Docs, Architect, CIO, CXO, PPM, Comms, Mobile, ETA (status unclear — predecessor flagged for activate-or-retire).

**Cross-project ecosystem** (no briefing mention at all): Rebel One, Zephyr, Piper Open, Vergil, Dispatch, Janus. HOST monitors coordination with these through xpoll briefs, cross-pollination logs, and Dispatch communications.

### "Current Focus" section (lines 99–106) is stale onboarding scaffolding

Lines 101–104 list:
1. Establish HOSR role (this onboarding) — **done 23 days ago**
2. Audit current agent roster and role health — **now a recurring 4-week cadence, not a current focus item**
3. Document coordination patterns in active use — **done; see pattern-029, pattern-062, others**
4. Identify any roles experiencing drift — **ongoing, via role health checks**

This whole section should be replaced with a pointer to BRIEFING-CURRENT-STATE.md (already done on line 5 as a note, but the "Current Focus" section below contradicts it).

### Metrics (lines 113–117) — what HOST actually tracks

**Current list**: "Role drift incidents per month / Handoff success rate / Agent utilization efficiency / Coordination overhead (PM time spent managing agents)"

**Actually tracked**:
- Days of silence for stalled human contacts (alpha testers 39d, Dominique 40d, etc.)
- Briefing staleness in days (team-structure.md 113+ days, BRIEFING-CURRENT-STATE typically 7-15 days)
- Workstream review cadence hit rate (weekly target, actual varies with PM bandwidth)
- Role health check cadence hit rate (4-week target)
- Orphaned-state signals (uncommitted-file pileups on main, inbox-vs-read drift in mailboxes)
- Pattern staleness and documentation decay

Three of the four items in the current briefing aren't tracked. All six items above should replace them.

### People Management section (lines 85–91)

**Current** lists: "Alpha testers (Michelle, others), Advisors (Ted Nadeau, Sam Zimmerman), Future team members, External collaborators"

**Actual current human network** (from predecessor's Apr 22 final snapshot):

| Person | Status | Notes |
|---|---|---|
| Ted Nadeau | Active advisor | 2 docs pending (Security.md, Methodology.md) |
| Dominique Derosena | No reply 40d | May reactivate after 500-error web-wizard fix |
| Alpha testers (13) | Zero responses 39d | Predecessor recommends formal closure |
| Cindy Chastain | Podcast released | No action |
| Dave Romero | Pitch outcome unknown | No action |
| Sam Zimmerman | Dormant advisor | Contributions complete; formal acknowledgment recommended |

Briefing should describe the *practice* of tracking (standing table, day counts) rather than listing specific people who will change.

---

## 3. Environment and tool corrections (Chat → Code)

The briefing is implicitly Chat-era throughout. Corrections:

| Chat-era assumption (implicit) | Code-era reality |
|---|---|
| `project_knowledge_search` as primary research tool | Direct `Read`, `Grep`, `Glob` on filesystem |
| PM as memo courier | Direct read/write to `mailboxes/[role]/` |
| Omnibus logs accessed as summaries in search results | Full logs read directly from `docs/omnibus-logs/` |
| Session logs private to each Chat instance | Session logs in `dev/YYYY/MM/DD/` visible to all agents |
| Workstream reviews from memory + search snippets | Workstream reviews from full logs + git log + mailbox traffic |
| "Days stale" as estimation from content | `git log` as authoritative staleness signal |
| Briefings read once at session start | Briefings + BRIEFING-CURRENT-STATE refreshed at session start via SessionStart hook |
| No concept of worktrees | `git worktree` discipline per CLAUDE.md; HOST runs in a worktree if on non-`main` branch |
| Remote access unavailable | `claude remote-control` enables phone-based session steering |

The briefing should add a section on **Session Startup Routine in Code** listing:
- Check SessionStart hook output (unread mailboxes, today's session logs, xpoll brief)
- Check HOST inbox
- Scan `exec-open-items-tracker.md` for project state
- Scan recent omnibus logs (since last HOST session)
- Check BRIEFING-CURRENT-STATE for freshness
- Check today's session logs in `dev/YYYY/MM/DD/` for in-flight agent work
- Only then decide what to produce

---

## 4. Structural gaps (new sections the briefing should have)

1. **Recurring deliverables** with cadence, format, and audience — currently scattered or implicit
2. **Operating norms / undocumented practices** — see Section 2 above
3. **Session startup routine in Code** — see Section 3 above
4. **Coordination surfaces** — mailbox system, omnibus logs, exec-open-items-tracker, staggered audit calendar, xpoll briefs. Currently not enumerated.
5. **PA↔HOST working relationship** — flagged as load-bearing by CoS. Briefing should describe scope boundaries (PA does daily operations and PM-shadow; HOST does systemic monitoring, workstream reviews, health checks, human-network tracking; overlap zone is "noticing things" — both roles know who's acting on what). TBD pending my first-week coordination check with PA.
6. **Cross-project coordination** — xpoll briefs, Dispatch communication, Janus channel, sibling-project ecosystem. Currently zero briefing content.
7. **Live standards to apply** — verifiable-claims norm, Colleague Test v2 monitoring surface, Excellence Flywheel reconciliation watch (#982). Currently zero.
8. **What HOST explicitly doesn't do** — implementation decisions (Architect), product decisions (PPM), daily operations (PA). Briefing mentions this (lines 38–41) but thinly.

---

## 5. Downstream corrections beyond the briefing itself

Files/surfaces I expect also need HOSR→HOST or content refresh — Docs should verify:

- `CLAUDE.md` role table: check current state. Last I saw it was correct (says "HOST (Head of Sapient Trust)") but verify.
- `docs/internal/team-structure.md`: 113+ days stale per predecessor's Apr 16 health check. Separate high-priority fix; predecessor flagged as highest-priority doc staleness item.
- `docs/briefing/BRIEFING-CURRENT-STATE.md`: check whether "HOSR" appears anywhere.
- Skills that mention the briefing by filename (grep for `HOSR`).
- Any historical session logs that reference "HOSR" — **leave alone**; historical record, not current documentation.
- `docs/internal/operations/staggered-audit-calendar-2026.md`: verify HOST shows as the owner of role health checks.
- Mailbox READMEs / MANIFEST.md files: verify HOST mailbox is correctly listed.

---

## 6. Migration-template observations (for CIO and subsequent roles)

Having been through Phase 3 myself today, two additions I'd propose to the migration checklist:

### Finding A: Commit-before-handoff-transfer

The Chat→Code handoff package (this memo + 5 others) was drafted but **not committed** to main before my Code session started. My worktree couldn't see the files. Resolution required a mid-session commit to `main` with specific file-staging, then a fast-forward merge into the worktree.

**Proposed checklist addition (Phase 2)**: "Before incoming Code instance starts, verify handoff package is committed to `main` and pushed to origin. If multiple orphaned files exist, commit only the handoff package in an atomic commit so the successor can find it."

### Finding B: Startup-routine documentation as a standing file, not a session-log note

Phase 3 says "Document [startup routine] to your session log or a standing file." I'd argue **standing file always** — session logs rotate daily, routines need to persist. Proposed location: `docs/operations/startup-routines/{role}-code-startup.md` or equivalent. Docs can advise on location.

**Proposed checklist addition (Phase 3)**: replace "session log OR standing file" with "standing file at agreed location."

### Finding C: Orphaned-state pileup on main as a migration-context risk

When I opened this session, `main` had ~30 uncommitted files across `dev/active/` and `mailboxes/` — some 5+ days old. This is a systemic signal HOST should track, but it also creates migration risk (harder to find the handoff package, higher chance of a confusing commit). Not a checklist item per se, but worth flagging: **a tidy `git status` on main before the outgoing Chat session's last day would reduce migration-handoff friction.**

---

## Suggested priority

- **This week** (before CIO migration starts): items in Sections 1, 3, and 6 — renames, Code-era tool references, migration-checklist additions. These are blockers for the next role.
- **Within 2 weeks** (before next HOST workstream review cycle): Sections 2 and 4 — core content refresh, new structural sections.
- **Ongoing**: Section 5 — downstream sweep, as Docs has bandwidth.

---

## What I'll do next

- Draft the Apr 17–23 workstream review (first substantive deliverable; validates end-to-end workflow in Code)
- PA coordination check in first week — will initiate via memo once I've read recent omnibus logs
- Standing startup-routine file per Finding B above — draft once I've lived through a few Code sessions (probably end of week 1)
- Not blocking on any of the above for Docs to act on this memo

Happy to discuss any findings or revise priorities per what Docs has bandwidth for.

— HOST
April 22, 2026
