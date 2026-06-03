# Agent 360 Questionnaire — v0.3 (Post-Migration Benchmark)

**Purpose**: Structured feedback mechanism for agent roles to surface friction, gaps, and improvement opportunities, addressed to HOST (Head of Sapient Trust).

**Context for this round**: This is the **post-migration benchmark** — paired with the v0.2 pre-migration baseline (fielded Apr 22, 2026). All seven leadership roles + Lead Dev + Docs have been operating in Claude Code for ~6 weeks. Your responses here capture how things are working *now*, in Code, and will be compared against your v0.2 responses to identify which gaps closed, which persisted, which new ones emerged.

**Cadence**: Post-migration benchmark target ~6 weeks after Code adoption (this round). Future cadence: per-cohort-migration or per-major-infrastructure-transition (no fixed regular interval).

**Process**:
1. PM coordinates fielding; each role submits a response memo to HOST inbox
2. HOST synthesizes responses, identifies patterns including tier-3 cross-role convergence, writes diff-against-baseline summary memo to PM + cohort
3. PM and HOST decide together what's worth changing; specific recommendations route to owners
4. Synthesis target: ~Jun 12, 2026 (six weeks post-migration window)

---

## Instructions for Agent

You are being asked to provide feedback on how your role is working within the Piper Morgan project in the Code era. Your responses will be read by HOST and PM together.

**Ground rules**:
- Be specific. Cite documents, issues, commits, memos, or omnibus entries where possible.
- Focus on friction and tacit knowledge, not satisfaction. "What's hard?" + "what do I know that isn't documented?" are more useful than "what's good?"
- "I don't have enough context to answer this" is a valid response.
- "This question was useful in v0.2 but doesn't apply post-migration" is also a valid response — flag and skip.
- If your role has fewer than 10 sessions of Code experience, answer what you can and note limited exposure.

**Output**: A memo (markdown) addressed to HOST inbox. No specific length requirement — be as concise or thorough as the questions warrant.

**Your v0.2 response (if applicable)**: 7 roles fielded v0.2 in April 2026 (CIO, Comms, HOST, PPM, CXO, Architect, Exec). Find your v0.2 response at `dev/2026/04/{22,23,25,26}/agent-360-response-{your-role-slug}-2026-04-*.md`. Diff-against-baseline analysis depends on your §7 retrospective using your own v0.2 predictions.

**For roles WITHOUT a v0.2 response** (Lead Dev, Docs, PA): you weren't fielded in v0.2 because Lead Dev + Docs are PM-paired-continuous (didn't migrate) and PA was activating during the v0.2 window. For Section 7, answer with your observed Code-era operating experience rather than comparing against a prediction; skip §7 questions that don't apply.

---

## Section 1: Briefing & Orientation

*Sections 1-6 preserved from v0.2; answer with current-state lens for diff-against-baseline.*

**1.1** Review your essential briefing document (BRIEFING-ESSENTIAL-[ROLE].md).
- Is it accurate to current state?
- What's missing that you needed during recent work?
- What's present but never useful?
- *(v0.3 additional prompt)*: When did you last consult it? If "never" or "once, weeks ago" — what's it for?

**1.2** When you started your most recent session, how long did orientation take before you were doing actual work? What consumed that time?

**1.3** If a new instance of your role started tomorrow with only the briefing docs + Code access, what would they get wrong in their first hour?

---

## Section 2: Information Access

**2.1** In your recent work, what information did you have to ask the PM for that should have been findable independently?

**2.2** What document do you consult most often? Is it easy to find?

**2.3** What document exists but is stale, misleading, or contradicts other sources?

**2.4** Is there a recurring question you answer for yourself each session that should be pre-answered somewhere?

**2.5** *(v0.3 NEW)*: Code-era specific — `grep`, `git log`, mailbox traversal, omnibus reading: which of these has substituted for what would have been a PM-question in Chat? Which still feel awkward or slow?

---

## Section 3: Handoffs & Coordination

**3.1** Think of a recent handoff you were part of (giving or receiving work to/from another role).
- What went well?
- What information was missing or unclear?

**3.2** Is there a role you frequently need input from but have difficulty reaching?

**3.3** Have you ever duplicated work that another role had already done, or discovered that your work duplicated theirs?

**3.4** When you send a memo to another role's mailbox, do you have confidence it will be read and actioned in a reasonable timeframe? Why or why not?

**3.5** *(v0.3 NEW)*: The move-to-read convention landed cohort-wide May 15. Is it working as a signal that recipients have processed your memo? Are you using `git log mailboxes/{role}/read/` to check, or relying on response memos as the signal?

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

**5.5** *(v0.3 NEW)*: The methodology corpus grew from ~22 to 36+ entries in the Code era. Has corpus growth helped your work, or is the catalog now larger than you can hold? Specific entries you reach for repeatedly?

---

## Section 6: Tools & Environment

**6.1** What capability would most improve your effectiveness? (Be specific — not "better AI" but "access to X" or "ability to Y")

**6.2** Is there a tool or resource available to you that you don't use? Why not?

**6.3** What's the most time-consuming mechanical task in your typical session? Could it be automated or pre-computed?

**6.4** *(v0.3 NEW)*: Code-era specific — hooks, skills, MCPs, worktrees: which have become load-bearing? Which feel like overhead with no payoff?

---

## Section 7: Post-Migration Reflection (REPLACES v0.2 §7 Migration-Specific)

*v0.2 §7 was forward-looking about migration; v0.3 §7 is retrospective on the same questions.*

**7.1** What got better about your work after moving to Code? Compare your specific v0.2 §7.1 predictions to what actually happened.

**7.2** What got harder or was lost? Compare to your v0.2 §7.2 predictions — what did you anticipate correctly? What surprised you?

**7.3** What context from your Chat sessions did get lost in the transition? What did you need to reconstruct that you wish had been preserved differently in handoff?

**7.4** Does your actual startup routine match what you designed in v0.2 §7.4? What did you change once you experienced Code reality?

**7.5** What about working with PM or other roles still feels like it depends on something the Code environment doesn't have? (Or — has Code surfaced new working patterns with PM/roles that Chat didn't?)

---

## Section 8: Role-Specific Questions

*Answer only the section for your role.*

*Section 8 role-specific questions preserved from v0.2 — answer with current Code-era experience. If a question doesn't apply post-migration, flag as N/A.*

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

### PPM (Principal Product Manager)

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

**8.1** What surprised you about the project's actual operating state vs. what the documentation suggested?

**8.2** Where does your scope overlap with other roles? Is the boundary clear or negotiated ad hoc?

**8.3** What institutional knowledge have you acquired that isn't captured in any document?

---

## Section 9: Tacit Knowledge & Open Response (EXPANDED in v0.3)

*Apr 27 synthesis convergence finding: Section 9 consistently surfaces tacit knowledge that earlier sections miss. v0.3 makes this explicit with three new tacit-knowledge prompts (9.4–9.6) alongside the original three open prompts.*

**9.1** What question should we have asked but didn't?

**9.2** What's one thing you'd change about how this project operates, if you could change only one thing?

**9.3** Anything else HOST should know?

**9.4** *(v0.3 NEW)*: What knowledge about your role do you possess that no document captures? (Examples: when to escalate vs. when to absorb; how to read PM cues; what "feeling slow today" means for your work-shape; which other-role traffic to scan vs. skip)

**9.5** *(v0.3 NEW)*: What surprised you about the project's actual Code-era operating state over the last 6 weeks vs. what you predicted before migration?

**9.6** *(v0.3 NEW)*: What would you do differently if you could re-start your role from the Apr 22 migration with what you know now?

---

## Section 10: Duty Cycle Experience (NEW in v0.3)

*V1 Duty Cycle ran May 17–21 as a CIO-designed cohort experiment. Three roles adopted (CIO, HOST, Docs); four roles queued but did not run (Exec, PA, plus Arch + Lead Dev + Comms + CXO + PPM as observers). Retired by PM directive May 21 in favor of the V2 / day-rhythm design (v0.6 currently in pilot). This section captures the one-shot V1 retrospective data; observation logs from Phase B carry the in-flight v0.5/0.6 design feedback separately.*

### For adopters (CIO, HOST, Docs) — 5 questions

**10.1 Cadence**: Was the cron interval you ran (the Phase 5 cohort default was `*/5`; HOST briefly tried `*/15` then hourly; Docs ran `*/5`; CIO ran `*/5` Day-1 then varied) appropriate? Too frequent? Too rare? Did you experience cycle-visibility as helpful or as noise?

**10.2 Detection success**: What mail-arrival situations did the cycle catch that you'd otherwise have missed? Any false positives (cycle flagged something inessential) or false negatives (cycle missed something it should have caught)?

**10.3 Cycle-log experience**: Did the append-only cycle-log structure feel comprehensible? Did you reach for it during sessions, only at retirement, or never?

**10.4 Worktree experience**: Did the cycle-branch/worktree pattern feel right + comfortable, or were the worktree-cleanup ops an asymmetric-discipline drag (methodology-35 candidate filed May 24 cites this as seed material)? Both reads are valid — capture what you actually felt.

**10.5 Retirement reaction**: Was the May 21 retirement directive reading-the-room-right, premature, or overdue? Anything V1 had that you'd want preserved in v0.5/0.6?

### For observers (Arch, Exec, PPM, CXO, Comms, PA, Lead Dev) — 3 questions

**10.6 Cross-traffic visibility**: Did you notice the cycle's existence in cross-traffic? Did cycle-log commits show up in your visibility (omnibus, merge-keeper sweeps, mailbox MANIFESTs, etc.)?

**10.7 Work-pattern influence**: Did the cycle shape any of your work-patterns? E.g., did seeing HOST/CIO/Docs cycle commits change how you handled mail or trigger anything in your own workflow?

**10.8 Retirement reading**: Was the cohort decision to retire well-shaped from your vantage, or did it feel premature or late?

---

## Plausibility Check (Required)

Before submitting, review your suggestions against this filter:

- [ ] Is this based on specific observed friction, or theoretical concern? (Flag which)
- [ ] Could this be addressed by agents without PM involvement? (Note if yes)
- [ ] Does this still matter under the v0.6 duty cycle design (Phase B currently in pilot)? (If V1-specific and won't reapply, note as V1-retrospective only)
- [ ] *(v0.3 NEW)*: Is this tacit knowledge that should be documented somewhere, or is it inherently agent-instance knowledge that doesn't transfer? (Flag if you're not sure.)

---

*Questionnaire v0.3 — May 27, 2026 (fielded June 3, 2026)*
*Post-migration benchmark edition*
*Fielded: June 3, 2026 — **responses requested by ~June 10** (Time Lord: backstop, not deadline-as-pacing; respond when you can)*
*Synthesis target: ~Jun 12, 2026 (six weeks post-migration window)*
*Paired with v0.2 (Apr 22, 2026 pre-migration baseline) for diff-against-baseline analysis*

---

## Changes from v0.2

- **Framing**: pre-migration baseline → post-migration benchmark; explicit diff-against-baseline pairing
- **Section 7**: rewritten from migration-forward-looking to retrospective on those predictions
- **Section 9 expanded**: added three tacit-knowledge prompts (9.4–9.6) per Apr 27 synthesis convergence finding
- **Section 10 NEW**: V1 Duty Cycle Experience module — 5 questions for adopters (CIO + HOST + Docs), 3 for observers (other 7 roles). One-shot retrospective with closing capture window (per CIO May 24 shape-2 reasoning). **10.1 + 10.4 refined May 27 post-CIO-review** to pre-fill cadence context (10.1) and add counterbalance to bias-toward-drag (10.4).
- **Section 1.1 / 2.5 / 3.5 / 5.5 / 6.4**: minor Code-era-specific prompts added to existing sections
- **Plausibility Check**: added v0.6-relevance question + tacit-knowledge-vs-documentable filter
- **Mobile role section removed** (no current Mobile activity; PA absorbed Mobile reactivation question shape)
