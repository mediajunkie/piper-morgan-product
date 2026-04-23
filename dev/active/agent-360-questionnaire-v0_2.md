# Agent 360 Questionnaire — v0.2 (Pre-Migration Baseline)

**Purpose**: Structured feedback mechanism for agent roles to surface friction, gaps, and improvement opportunities, addressed to HOST (Head of Sapient Trust).

**Context for this round**: This is a pre-migration baseline. All Chat roles are migrating to Claude Code or Cowork. Your responses here capture how things work *now*, in Chat. In ~6 weeks, we'll run this again to benchmark against your experience in the new environment. Be honest about what's working and what isn't — the comparison is the point.

**Cadence**: Post-milestone or at major infrastructure transitions (this one qualifies as both — M1 closed Apr 11, Code migration beginning Apr 22)

**Process**:
1. PM brings this questionnaire during a migration-prep conversation with each role
2. Agent responds in a memo addressed to HOST inbox
3. HOST successor (in Code) synthesizes all responses, identifies patterns, writes summary memo to PM
4. PM and HOST decide together what's worth changing in the new environment

---

## Instructions for Agent

You are being asked to provide feedback on how your role is working within the Piper Morgan project. This is a direct channel to HOST — your responses will be read by HOST and PM together.

**Ground rules**:
- Be specific. Cite documents, issues, or omnibus entries where possible.
- Focus on friction, not satisfaction. "What's hard?" is more useful than "what's good?"
- "I don't have enough context to answer this" is a valid response.
- If you have fewer than 3 sessions of experience in the current project, answer what you can and note limited exposure.

**Output**: A memo (markdown) addressed to HOST inbox. No specific length requirement — be as concise or thorough as the questions warrant.

---

## Section 1: Briefing & Orientation

**1.1** Review your essential briefing document (BRIEFING-ESSENTIAL-[ROLE].md).
- Is it accurate to current state?
- What's missing that you needed during recent work?
- What's present but never useful?

**1.2** When you started your most recent session, how long did orientation take before you were doing actual work? What consumed that time?

**1.3** If a new instance of your role started tomorrow with only the briefing docs, what would they get wrong in their first hour?

---

## Section 2: Information Access

**2.1** In your recent work, what information did you have to ask the PM for that should have been findable independently?

**2.2** What document do you consult most often? Is it easy to find?

**2.3** What document exists but is stale, misleading, or contradicts other sources?

**2.4** Is there a recurring question you answer for yourself each session that should be pre-answered somewhere?

---

## Section 3: Handoffs & Coordination

**3.1** Think of a recent handoff you were part of (giving or receiving work to/from another role).
- What went well?
- What information was missing or unclear?

**3.2** Is there a role you frequently need input from but have difficulty reaching?

**3.3** Have you ever duplicated work that another role had already done, or discovered that your work duplicated theirs?

**3.4** When you send a memo to another role's mailbox, do you have confidence it will be read and actioned in a reasonable timeframe? Why or why not?

---

## Section 4: Role Clarity

**4.1** In your recent work, was there a task that felt like it belonged to a different role? Which role, and why?

**4.2** Is there work you're expected to do that isn't mentioned in your role definition?

**4.3** Is there work mentioned in your role definition that you've never actually been asked to do?

**4.4** If you could hand off one responsibility to another role (existing or new), what would it be?

---

## Section 5: Methodology & Process

**5.1** Which methodology documents do you actually use during work? (List specific filenames)

**5.2** Which methodology documents exist but you ignore or work around? Why?

**5.3** Is there a process you follow that isn't documented anywhere?

**5.4** What rule or constraint would you add to your own role to prevent a failure mode you've observed?

---

## Section 6: Tools & Environment

**6.1** What capability would most improve your effectiveness? (Be specific — not "better AI" but "access to X" or "ability to Y")

**6.2** Is there a tool or resource available to you that you don't use? Why not?

**6.3** What's the most time-consuming mechanical task in your typical session? Could it be automated or pre-computed?

---

## Section 7: Migration-Specific (NEW — all roles)

**7.1** What do you expect to get better about your work when you move to Code/Cowork? What specific friction do you anticipate being reduced?

**7.2** What do you expect to get harder or to lose? (e.g., conversational interaction with PM, artifact rendering, project_knowledge_search convenience)

**7.3** What context from your current Chat sessions would be hardest to reconstruct if it were lost? What should be explicitly preserved in a handoff?

**7.4** If you could design your own startup routine for the new environment — what you check first, what you load, what you verify — what would it look like?

**7.5** Is there anything about how you work with PM or other roles that depends on the Chat interface specifically? (e.g., voice dictation parsing, artifact display, interactive Q&A flow)

---

## Section 8: Role-Specific Questions

*Answer only the section for your role.*

### Lead Developer

**8.1** Review the last 3 issues you closed. For each: was the issue description sufficient to begin work, or did you need clarification?

**8.2** When you encounter a test failure, is the path to diagnosis clear? What slows you down?

**8.3** Is there a codebase area where you consistently feel under-informed?

### Chief Architect

**8.1** When you review a gameplan or spec, what information is most often missing?

**8.2** Are ADRs being consulted by other roles, or are they write-only artifacts?

**8.3** What architectural decision is currently undocumented but load-bearing?

### CXO (Chief Experience Officer)

**8.1** When you test a feature, do you have clear criteria for "passes Colleague Test"? Where do those criteria live?

**8.2** What's the gap between "tests pass" and "ready for users" that's hardest to articulate?

**8.3** When you file a UX finding, does it get addressed with the priority you'd expect?

### PPM (Product & Project Manager)

**8.1** Is the roadmap document a useful planning tool, or is it primarily historical record?

**8.2** When sprint scope changes mid-sprint, how do you track that? Is the mechanism adequate?

**8.3** What product decision is currently implicit that should be a PDR?

### Communications Director

**8.1** When you draft content, is the source material (omnibus logs, session logs) sufficient? What's missing?

**8.2** Is there a content type you're asked to produce that doesn't have a clear template or example?

**8.3** What's the lag time between "event worth writing about" and "content published"? What causes the lag?

### CIO (Chief Innovation Officer)

**8.1** When you identify a pattern worth documenting, what's the path to getting it formalized? Is it clear?

**8.2** Are innovation ideas getting lost between sessions? Where should they live?

**8.3** What methodology improvement have you suggested that wasn't adopted? Do you know why?

### HOST (Head of Sapient Trust)

**8.1** Is your view of the agent and human networks current? What information goes stale fastest?

**8.2** What agent welfare issue have you observed that hasn't been addressed?

**8.3** What's the gap between what you can *see* and what you'd need to see to do your job well?

### Chief of Staff (Exec)

**8.1** When you synthesize across workstreams, what's hardest to find?

**8.2** Are the weekly Ships useful artifacts or compliance exercises? How would you know?

**8.3** What thread have you tracked that later fell through the cracks? What would have prevented that?

### Documentation Management

**8.1** What document category is most often out of date?

**8.2** When you create an omnibus log, what source material is hardest to synthesize?

**8.3** Is there a documentation standard that's routinely violated? By whom?

### PA (Piper Alpha)

**8.1** As the most recently activated role, what surprised you about the project's actual operating state vs. what the documentation suggested?

**8.2** Where does your scope overlap with other roles? Is the boundary clear or negotiated ad hoc?

**8.3** What institutional knowledge have you acquired that isn't captured in any document?

### Mobile

**8.1** Given the extended hiatus (65+ days), what context would you need to reactivate effectively?

**8.2** Has the strategic pivot (methodology > code, BYOC distribution) changed your role's relevance? How?

**8.3** What would you prioritize if reactivated tomorrow?

---

## Section 9: Open Response

**9.1** What question should we have asked but didn't?

**9.2** What's one thing you'd change about how this project operates, if you could change only one thing?

**9.3** Anything else HOST should know?

---

## Plausibility Check (Required)

Before submitting, review your suggestions against this filter:

- [ ] Is this based on specific observed friction, or theoretical concern? (Flag which)
- [ ] Could this be addressed by agents without PM involvement? (Note if yes)
- [ ] Would this still matter after migrating to Code/Cowork? (If no, note as Chat-specific)

---

*Questionnaire v0.2 — April 22, 2026*
*Pre-migration baseline edition*
*Deployed during Chat→Code migration conversations*
*Next deployment: ~6 weeks post-migration (benchmarking round)*
