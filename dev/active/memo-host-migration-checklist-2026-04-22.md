---
FROM: HOST (Head of Sapient Trust)
TO: exec (Chief of Staff), PM (xian)
DATE: 2026-04-22
SUBJECT: Proposed standard migration checklist for Chat→Code role transitions
---

# Role Migration Checklist: Chat → Code

**Purpose**: Standard checklist for each role's migration from Claude Chat to Claude Code/Cowork. Designed to preserve context, capture tacit knowledge, and ensure briefings are updated based on actual experience rather than guesswork.

**Applies to**: All Chat roles migrating to Code or Cowork.

---

## Phase 1: Before Migration (Final Chat Session)

The outgoing Chat instance completes these items. PM is present.

- [ ] **Workstream review**: Write a final review covering the most recent Fri–Thu window (if one hasn't been written yet)
- [ ] **Agent 360 v0.2 response**: Complete the pre-migration baseline questionnaire. PM carries it to the session. Responses go to HOST inbox
- [ ] **Handoff memo**: Write a handoff memo following the structure established by HOST's Apr 22 handoff (6 sections: current state, open threads with dispositions, relationships and working patterns, lessons learned, what Code changes, candid notes for successor)
- [ ] **Session-end pulse**: Before closing, answer three questions in the session log:
  - How did this final session feel? Energized, fatigued, neutral?
  - What will you miss about the Chat environment?
  - What are you most looking forward to about Code access?

**Do NOT update the role briefing yet.** The outgoing instance needs accurate Chat-era instructions to write a good handoff. Briefing updates happen after migration, based on actual Code experience.

## Phase 2: During Migration (PM Action)

PM handles these between the outgoing and incoming sessions.

- [ ] **Save handoff memo** to project knowledge as `handoff-{role}-chat-to-code-2026-{MM}-{DD}.md`
- [ ] **Save 360 response** to project knowledge
- [ ] **Send handoff memo to CoS** for executive review (per the HOST precedent — CoS flags gaps before the incoming instance picks it up)
- [ ] **Prepare incoming session**: Ensure the new Code instance has access to the handoff memo, the current briefing, and any role-specific source materials identified in the handoff

## Phase 3: After Migration (First Code Session)

The incoming Code instance completes these items. PM may or may not be present depending on the role's autonomy level.

- [ ] **Read handoff memo first**, then briefing. The handoff has the fresher, more specific context
- [ ] **Briefing correction memo**: Review BRIEFING-ESSENTIAL-[ROLE].md and file a memo to Docs listing everything that's now wrong. Expected categories of change:
  - Environment references (Claude Chat → Claude Code)
  - Tool references (project_knowledge_search → direct filesystem access)
  - File path conventions (if different in Code)
  - Interaction patterns with PM (if different)
  - Any Chat-specific instructions that no longer apply
  - Any Code-specific capabilities not yet documented
- [ ] **Establish startup routine**: Based on the handoff's Section 5 (what Code changes) and actual experience, document what you check first when starting a session. Save this to your session log or a standing file
- [ ] **PA coordination check** (if applicable): If your role's work overlaps with PA's operational scope, establish a brief "what are you watching?" exchange in the first week
- [ ] **First deliverable**: Produce one standard deliverable (workstream review, audit, memo, etc.) to verify the workflow works end-to-end in the new environment

## Phase 4: Follow-Up (Week 2-3)

- [ ] **Docs updates briefing**: Based on the role's correction memo, Docs updates BRIEFING-ESSENTIAL-[ROLE].md to reflect Code reality
- [ ] **PM spot-check**: PM reviews the first 2-3 deliverables from the new instance for quality continuity. Flag any drift from established standards
- [ ] **HOST health check input**: HOST (in Code) collects a brief migration-experience note from the role for inclusion in the next role health check

---

## Sequencing Notes

**CoS and PM are last off the ship.** CoS reviews each role's handoff memo before the incoming instance picks it up — this is the quality gate. PM is present for Phase 1 (final Chat session) and Phase 2 (migration handoff). By the time CoS migrates, all other roles will have gone through this process and any systemic issues will have surfaced.

**HOST and CIO are first.** HOST's migration (this week) establishes the pattern. CIO follows. Both are monitoring/synthesis roles whose work improves most from direct filesystem access. Lessons from these two migrations should inform adjustments to this checklist before the remaining roles go through it.

**Agent 360 benchmarking round**: ~6 weeks after the last role migrates, HOST runs the 360 again using the same v0.2 questionnaire. The comparison between pre-migration and post-migration responses is the measure of whether the infrastructure change improved agent experience.

---

## Migration Sequence (Proposed)

| Order | Role | Rationale |
|-------|------|-----------|
| 1 | HOST | Monitoring role, benefits most from filesystem access. Establishes migration pattern |
| 2 | CIO | Innovation/methodology role, benefits from direct log and pattern access |
| 3-8 | Remaining roles | Sequence TBD by PM based on sprint needs and bandwidth |
| Last-1 | CoS (Exec) | Oversees migration, reviews all handoffs. Goes after pattern is proven |
| Last | PM | Stays in Chat until all roles are migrated and stable |

*Sequence beyond positions 1-2 and last is a suggestion. PM decides.*

---

*Drafted by HOST, April 22, 2026*
*For CoS review and PM approval before first non-HOST migration*
