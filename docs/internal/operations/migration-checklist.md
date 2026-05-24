
# Role Migration Checklist v1.2 (Chat → Code)

**Status**: v1.2 patch. Supersedes v1.1 (`mailboxes/host/sent/memo-host-migration-checklist-v1.1-2026-05-15.md`).
**Purpose**: Standing checklist for any future role migration (new role activation, re-migration of a dormant role, etc.). Cohort migration completed Apr 22–26, 2026.
**Owner**: HOST. Exec reviews; CEO approves for canonical publication.
**Recommended canonical location**: `docs/internal/operations/migration-checklist.md` (Docs to land if Exec+CEO approve).

**Changes from v1.1**: see §"Changes from v1.1" at end.

---

## Phase 1: Before Migration (Final Chat Session)

The outgoing Chat instance completes these items. PM is present.

- [ ] **Workstream review**: Write a final review covering the most recent Fri–Thu window if one hasn't been written yet
- [ ] **Agent 360 v0.2 response**: Complete the pre-migration baseline questionnaire. PM carries it to the session; responses go to HOST inbox
- [ ] **Handoff memo**: Write a handoff memo following the HOST Apr 22 6-section structure (current state / open threads with dispositions / relationships and working patterns / lessons learned / what Code changes / candid notes for successor)
- [ ] **Verify Chat-outputs are committed to repo**: Walk through any deliverables drafted in Chat outputs over the role's lifetime. Anything in Chat `outputs/` that isn't committed is invisible to the successor — commit before the final session (CXO Apr 25 Finding A)
- [ ] **Section 6 self-reflection** *(v1.1)*: Answer the load-bearing-vs-commodity question in handoff memo §candid-notes. What core function does the role hold that doesn't survive role-handoff? What's commodity (any agent could do it) vs. load-bearing (this role's distinct value)? Per Agent 360 v0.2 cohort §6 convergence finding (PP-002 ratified Apr 27): every role surfaced this independently. Outgoing instance is positioned to name it explicitly.
- [ ] **Session-end pulse**: Before closing, answer three questions in the session log: how did the final session feel? What will you miss about Chat? What are you most looking forward to about Code?

**Do NOT update the role briefing yet.** The outgoing instance needs accurate Chat-era instructions to write a good handoff. Briefing updates happen post-migration based on actual Code experience.

## Phase 2: During Migration (PM + Exec Action)

PM + Exec handle these between the outgoing and incoming sessions.

- [ ] **Save handoff memo** to project knowledge as `handoff-{role}-chat-to-code-YYYY-MM-DD.md`
- [ ] **Save 360 response** to project knowledge
- [ ] **Exec review of handoff** *(v1.1: clarified as quality gate)*: Exec reads handoff against tracker + cohort awareness; flags gaps to PM before incoming instance picks it up. This is the captain-last leverage point — Exec sees what the outgoing instance can't see from inside.
- [ ] **Three-artifact package** *(v1.1)*: Confirm incoming instance has access to the **handoff memo + Exec review memo + first-session prompt** as a triplet. All three are load-bearing; missing any one degrades the migration (per HOST Apr 22 first-day blocker experience).
- [ ] **First-session prompt drafting**: Per the four Phase-3 specifications (Exec Apr 22 reply): which week the first workstream review covers / scope of the workstream review / naming convention / format reference. *(v1.1 update: workstream-review write window is Fri–Tue with publication Wed, per CIO Apr 27 cadence clarification; the older Apr 24/25 narrow spec is superseded.)*

## Phase 3: After Migration (First Code Session)

The incoming Code instance completes these items.

- [ ] **Read handoff memo first**, then Exec review memo, then briefing. The handoff has fresher, more specific context; Exec review names what to watch for; briefing is the slowest-moving reference.
- [ ] **Verify worktree-vs-main path resolution before distribution-heavy work** (PPM Apr 26 Finding A): If PM provides absolute paths in the first-session prompt, check whether they resolve to your worktree or to the main repo. If main repo, coordinate with Docs on commit ownership before parallel work so sweeps don't stomp edits.
- [ ] **Establish worktree-default discipline** *(v1.2, per PM May 15 directive)*: Substantive output (memos, PDRs, ADRs, workstream reviews, drafts) defaults to `claude/*` branch + dedicated worktree per CLAUDE.md §"Git Worktrees" and per PM May 15 directive. Shared main worktree is appropriate only for short mailbox-discipline ops. The discipline layers (reset-before-stage / explicit paths / `git show --stat` post-commit) cannot fully prevent foreign-state capture in shared worktrees — only worktree separation can. Spin up your role-specific worktree on Day 1, not later.
- [ ] **Briefing correction memo**: Review `BRIEFING-ESSENTIAL-{ROLE}.md` and file a memo to Docs listing what's now wrong (environment references, tool references, file path conventions, PM interaction patterns, Chat-specific instructions, missing Code capabilities)
- [ ] **Establish startup routine**: Based on handoff §5 + actual Code experience, document what you check first at session start. Save to a standing role-startup-routine file at `docs/operations/startup-routines/{role}-code-startup.md` per the convention PPM landed Apr 26 *(v1.1 — Finding B from HOST Apr 22)*.
- [ ] **PA coordination check** (if applicable): If your role's work overlaps with PA's operational scope, establish a brief "what are you watching?" exchange in the first week
- [ ] **First deliverable**: Produce one standard deliverable (workstream review, audit, memo, etc.) to verify the workflow works end-to-end

## Phase 4: Follow-Up (Week 2–3)

- [ ] **Docs updates briefing**: Based on the role's correction memo, Docs updates `BRIEFING-ESSENTIAL-{ROLE}.md` to reflect Code reality
- [ ] **PM spot-check**: PM reviews the first 2–3 deliverables from the new instance for quality continuity; flags any drift
- [ ] **HOST health check input**: HOST collects a brief migration-experience note from the role for the next role health check
- [ ] **Phase-3-leftover discipline** *(v1.1, per CIO May 11 Finding G)*: Any Phase 3 task item still uncompleted **5 days after migration** should surface to PM + HOST as an explicit carryover-tracker entry, not silently deferred. The 5-day floor catches cases where operational pressure outpaces reflection-shaped work without dropping it on the floor.

---

## Sequencing Notes (generalized in v1.1)

**Captain-last principle** *(v1.1, codified; v1.2 nuance added)*: The role with the broadest review scope migrates last. For the Apr 22–26 cohort, this was Exec (Chief of Staff). The principle generalizes: when migrating any cohort, sequence the role whose work most often involves reviewing other roles' output to migrate at the end. They gain the privilege of meta-observation across the cohort's migrations rather than first-time discovery.

*v1.2 nuance*: For **single-role re-migrations** (where there's no cohort to observe), the captain-last principle doesn't apply directly — the re-migrating role IS the cohort. The principle reduces to "the role re-migrating goes when it goes." Naming this so the principle is understood as a cohort-scale primitive, not a universal sequencing rule.

**Methodology compresses through the cohort**. The Apr 22–26 wave showed decreasing-review-volume on each successive handoff: HOST 5+1 gaps → CIO 4 gaps → Comms 3+1 → CXO 2 → PPM 3 → Architect 0+1 → Exec self-review. The pattern is real; expect future cohorts to compress similarly.

**Reconstruction tax compounds**. Each later captain pays less reconstruction cost as long as prior captains' Phase-1 outputs are committed (CXO Apr 25 Finding A canonical: predecessor CT v2 drafted Apr 19 in Chat outputs but never committed; successor reconstructed from handoff alone). The Phase-1 "verify Chat-outputs committed" check is the lever that controls the tax.

## Migration Sequence Reference

For the Apr 22–26 cohort:

| Order | Role | Date | Notes |
|-------|------|------|-------|
| 1 | HOST | Apr 22 | Established pattern; first-day blocker on Phase-2 commit prompted Finding A discipline |
| 2 | CIO | Apr 23 | First downstream beneficiary of HOST findings |
| 3 | Comms | Apr 23 | Same-day pair with CIO |
| 4 | CXO | Apr 25 | CT v2 reconstruction surfaced as Finding A |
| 5 | PPM | Apr 25 | Worktree-vs-main path Finding A |
| 6 | Architect | Apr 26 AM | Sub-epic gate framing absorbed |
| 7 | Exec | Apr 26 PM | Captain-last; self-review with meta-observation privilege |

For **future** migrations, derive sequence from:
1. Broadest-review-scope role last (captain-last principle)
2. Highest-Code-leverage roles early (monitoring + synthesis roles benefit most from filesystem access)
3. PM-paired roles (Lead Dev, Docs) operate continuously; no migration needed if already Code-native

---

## Changes from v1.1

- **Naming patches**: 8 spots of `CoS` → `Exec` per the May 15 naming directive (Phase 2 header + intro, Phase 2 review-of-handoff item + 3 in-item references, Three-artifact package, Phase 3 reading order, Migration Sequence table row, For-Exec+CEO close, Owner line, Docs-to-land qualifier)
- **Phase 3 §"Establish worktree-default discipline"** added *(v1.2)* per PM May 15 worktree-default directive — Exec May 18 review flagged this needed Day-1 surfacing for incoming Code instances
- **Sequencing Notes §"Captain-last principle"** — v1.2 nuance added clarifying the principle as cohort-scale primitive (single-role re-migrations reduce to "the role re-migrating goes when it goes")
- **Sequencing Notes §"Methodology compresses"** — terminal entry updated from "CoS self-review" → "Exec self-review" (naming consistency)
- **Status** §updated to note v1.2 absorbs Exec May 18 review for canonical-publication readiness

## Changes from v1.0

(Preserved from v1.1 for audit-trail continuity.)

- **Phase 1 §"Section 6 self-reflection"** added (load-bearing-vs-commodity question; PP-002 framing)
- **Phase 2 §"Exec review of handoff"** clarified as quality gate (captain-last leverage point)
- **Phase 2 §"Three-artifact package"** added (handoff + Exec review + first-session prompt as triplet)
- **Phase 2 §"First-session prompt drafting"** notes workstream-review write window as Fri–Tue per CIO Apr 27 cadence clarification (older Apr 24/25 narrow spec superseded)
- **Phase 3 §"Establish startup routine"** points at `docs/operations/startup-routines/{role}-code-startup.md` per PPM Apr 26 convention (Finding B from HOST Apr 22)
- **Phase 4 §"Phase-3-leftover discipline"** added (5-day floor per CIO May 11 Finding G)
- **Sequencing Notes** §"Captain-last principle" codified; methodology-compression observation generalized
- **Migration Sequence** table updated with actual Apr 22–26 cohort + future-derivation rules

---

## Status

**v1.2 absorbs Exec May 18 review.** Naming directive landed (8 spots), Phase 3 worktree-default surfaced, captain-last principle nuanced for single-role re-migrations. Ready for CEO ratification.

Per Exec sequencing:
1. HOST files v1.2 with patches incorporated → **landed in this memo**
2. Docs lands v1.2 at canonical path → **pending CEO ratification**
3. v1.1 memo + v1.2 supersession note both reachable in audit trail → **v1.1 remains in `mailboxes/host/sent/` for trail; this memo cross-references it**

**For CEO**: ratify v1.2 for canonical publication at `docs/internal/operations/migration-checklist.md`. Per the v1.1 close, CEO ratification is the gating step.

## Cross-references

- v1.1 (superseded): `mailboxes/host/sent/memo-host-migration-checklist-v1.1-2026-05-15.md`
- Exec review (incorporated): `mailboxes/host/read/memo-exec-to-host-cc-ceo-cio-pa-docs-migration-checklist-v1.1-exec-review-2026-05-18.md`
- May 15 naming directive: `mailboxes/exec/sent/memo-exec-to-leadership-cc-pa-ceo-exec-naming-the-chief-not-cos-2026-05-15.md`
- May 15 worktree-default directive (memory): `feedback_worktree_default_for_substantive_work.md`
- v1.0 origin: `dev/2026/04/22/memo-host-migration-checklist-2026-04-22.md`

— HOST
*May 18, 2026*
