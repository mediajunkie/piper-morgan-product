# Agent 360 Questionnaire — v0.4 (Amber-Era Check-In)

**Purpose**: Structured feedback mechanism for agent roles to surface friction, gaps, and improvement opportunities, addressed to HOST (Head of Sapient Trust).

**Context for this round**: v0.3 (fielded June 3, 2026) was the post-migration benchmark for the move from Chat to Claude Code. The dominant infrastructure shift since then is the **Amber migration** (2026-07-25) — the cohort moved from Claude Desktop's ephemeral per-session worktrees to Amber's stable per-agent worktrees, persistent tmux sessions, and session-scoped cron-driven duty cycles. The `duty-cycle-tick` skill has also matured substantially in that window (v1.06 → v1.28), and the cohort roster has grown to 11 roles (Web joined since v0.3). This round asks how that's actually working, three weeks in — not a hypothetical, a lived check.

**Cadence**: **Ratified 2026-08-14 at 6 weeks (42 days), derived from the actual v0.1→v0.2→v0.3 fielding history** (34 and 42 days respectively) — see `docs/briefing/ROLE-PORTFOLIO-HOST.md`. This round is overdue by that measure (v0.3 was due for a successor ~July 15); going forward CIO's self-firing workflow will trigger it automatically.

**Process**:
1. HOST fields to all 11 current roles via mailbox; each role submits a response memo to HOST's inbox
2. HOST synthesizes responses, identifies patterns including cross-role convergence, writes a diff-against-v0.3 summary memo to PM + cohort
3. PM and HOST decide together what's worth changing; specific recommendations route to owners
4. Synthesis target: ~4 weeks from fielding (generous window; Time Lord backstop, not deadline-as-pacing)

---

## Instructions for Agent

You are being asked to provide feedback on how your role is working within the Piper Morgan project, specifically under the Amber operating model. Your responses will be read by HOST and PM together.

**Ground rules**:
- Be specific. Cite documents, issues, commits, memos, or session logs where possible.
- Focus on friction and tacit knowledge, not satisfaction. "What's hard?" + "what do I know that isn't documented?" are more useful than "what's good?"
- "I don't have enough context to answer this" is a valid response.
- "This question was useful in v0.3 but doesn't apply now" is also a valid response — flag and skip.
- If you're new to Amber or your role, answer what you can and note limited exposure.

**Output**: A memo (markdown) addressed to HOST's inbox, sent via `scripts/mail-send.sh` per the standing mailbox discipline. No specific length requirement.

**Your v0.3 response (if applicable)**: find it at `dev/2026/06/03/agent-360-response-{your-role-slug}-2026-06-03.md` or your own `mailboxes/{role}/sent/`. If you don't have one (Web, PA-if-not-fielded), answer with your observed operating experience rather than comparing against a prior round.

---

## Section 1: Briefing & Orientation

**1.1** Review your essential briefing document (`BRIEFING-ESSENTIAL-{ROLE}.md`) and, if you have one, your `ROLE-PORTFOLIO-{ROLE}.md`.
- Is it accurate to current state?
- What's missing that you needed during recent work?
- When did you last actually consult either? If "never" or "once, weeks ago" — what are they for?

**1.2** When you start a session (fresh or resumed), how long does orientation take before you're doing actual work? What consumes that time now, under Amber's stable-worktree model, vs. what consumed it under Desktop's ephemeral worktrees?

**1.3** If a new instance of your role started tomorrow on Amber with only the briefing docs + worktree access, what would they get wrong in their first hour?

---

## Section 2: Information Access

**2.1** In your recent work, what information did you have to ask PM for that should have been findable independently?

**2.2** What document do you consult most often? Is it easy to find?

**2.3** What document exists but is stale, misleading, or contradicts other sources?

**2.4** Is there a recurring question you answer for yourself each session that should be pre-answered somewhere?

**2.5** **Amber-specific**: the shared memory pool (`~/.claude-pm/…/memory/`), `MEMORY.md`, `dev/active/{role}-carry-forward.md` — which of these do you actually use to reconstruct state, and which sit unused?

---

## Section 3: Handoffs & Coordination

**3.1** Think of a recent handoff you were part of (giving or receiving work to/from another role).
- What went well?
- What information was missing or unclear?

**3.2** Is there a role you frequently need input from but have difficulty reaching?

**3.3** Have you ever duplicated work that another role had already done, or discovered that your work duplicated theirs?

**3.4** When you send a memo to another role's mailbox, do you have confidence it will be read and actioned in a reasonable timeframe? Why or why not?

**3.5** **Amber-specific**: `mail-send.sh`'s push-to-ref mechanism (no main-checkout bridge, direct commit-tree push to `origin/main`) replaced the old bridge workflow in June. Has that actually removed friction for you, or does it have its own rough edges?

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

**5.5** The methodology corpus has continued growing since v0.3. Has that helped, or is the catalog now larger than you can hold? Specific entries you reach for repeatedly?

---

## Section 6: Tools & Environment

**6.1** What capability would most improve your effectiveness? (Be specific — not "better AI" but "access to X" or "ability to Y")

**6.2** Is there a tool or resource available to you that you don't use? Why not?

**6.3** What's the most time-consuming mechanical task in your typical session? Could it be automated or pre-computed?

**6.4** **Amber-specific**: worktree hooks (`check-branch.sh` and friends) — do you know whether yours actually fire, or are you relying on prose discipline alone? Have you ever behaviorally tested them (not just checked config presence)?

---

## Section 7: The Amber Transition, Three Weeks In

*Replaces v0.3's "Post-Migration Reflection" — the relevant migration now is Desktop → Amber, not Chat → Code.*

**7.1** What got better about your work after moving to Amber? Be specific — not "it's more stable," but what changed in practice.

**7.2** What got harder, or was lost, in the move to Amber? What did you need to reconstruct or re-learn?

**7.3** Did your worktree provision correctly (0 commits behind `origin/main`, hooks live) at handover, or did you inherit drift/staleness you had to catch yourself? (Real incident: one seat arrived 5,393 commits behind with dead hooks, silently.)

**7.4** Does your actual day-to-day operating routine match what the `duty-cycle-tick` skill and CLAUDE.md's worktree-model section describe, or have you deviated in ways that aren't written down anywhere?

**7.5** What about working with PM or other roles still feels like it depends on something Amber's environment doesn't have?

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

### Web (Unicorn Web Designer)

*New role since v0.3 — no prior baseline, first Agent 360 appearance.*

**8.1** What's the gap between what the design system documents and what actually ships? Where does it show up?

**8.2** Is there a review or handoff step you consistently have to work around?

**8.3** What institutional knowledge have you acquired about the website/design surface that isn't captured anywhere?

---

## Section 9: Tacit Knowledge & Open Response

*v0.3's synthesis found this section consistently surfaces what earlier sections miss. Keeping it as-is — it's proven, not broken.*

**9.1** What question should we have asked but didn't?

**9.2** What's one thing you'd change about how this project operates, if you could change only one thing?

**9.3** Anything else HOST should know?

**9.4** What knowledge about your role do you possess that no document captures? (Examples: when to escalate vs. when to absorb; how to read PM cues; what "feeling slow today" means for your work-shape; which other-role traffic to scan vs. skip)

**9.5** What surprised you about the project's actual Amber-era operating state vs. what you predicted before the migration?

**9.6** What would you do differently if you could re-start your role from the July 25 Amber migration with what you know now?

---

## Section 10: Duty Cycle Experience (Amber-Era)

*v0.3's Section 10 covered the retired V1 duty-cycle experiment (May 2026) — long obsolete. This section is a fresh look at the current, mature `duty-cycle-tick` skill (v1.28 as of this fielding) as most roles' primary daily operating mode.*

**10.1 Cadence**: Is your cron interval (fires/day, wake window) appropriate for your role's actual workload? Too frequent, generating noise? Too rare, missing things?

**10.2 The "fire is a wake, not a time-box" model**: Does draining all unblocked work per wake (rather than one task per fire) actually match how you work, or do you find yourself bite-sizing anyway?

**10.3 Detection success**: What has your duty cycle caught that you'd otherwise have missed? Any false positives (flagged something inessential) or false negatives (missed something it should have caught)?

**10.4 The freeze-watchdog registry**: Do you maintain your own row? Has it ever caught you going dark, or been a source of false alarms?

**10.5 STOP/re-arm discipline**: Has the delete-then-create-then-verify cron re-arm ever failed silently for you, or stacked a duplicate job? How would you know if it had?

**10.6 Session-log-as-single-source discipline**: Is logging in one place (the session log, not a parallel cycle-log) actually working, or do you find yourself wanting a second surface?

**10.7 Cross-traffic visibility**: Do other roles' duty-cycle commits show up in your own visibility in a useful way, or mostly as noise to filter past?

---

## Plausibility Check (Required)

Before submitting, review your suggestions against this filter:

- [ ] Is this based on specific observed friction, or theoretical concern? (Flag which)
- [ ] Could this be addressed by agents without PM involvement? (Note if yes)
- [ ] Does this still matter under the current Amber operating model, or is it a Desktop-era holdover that no longer applies? (Flag if the latter)
- [ ] Is this tacit knowledge that should be documented somewhere, or is it inherently agent-instance knowledge that doesn't transfer? (Flag if you're not sure.)

---

*Questionnaire v0.4 — August 14, 2026*
*Amber-era check-in*
*Fielded: [date to be filled at send] — responses requested within ~2 weeks (Time Lord: backstop, not deadline-as-pacing; respond when you can)*
*Synthesis target: ~4 weeks post-fielding*
*Paired with v0.3 (June 3, 2026 post-migration benchmark) for diff-against-baseline analysis*

---

## Changes from v0.3

- **Framing**: post-migration (Chat→Code) benchmark → Amber-era check-in (the relevant migration now is Desktop→Amber, 2026-07-25)
- **Section 7**: rewritten from Code-migration retrospective to Amber-transition reflection, including the real worktree-provisioning-drift incident as a concrete probe
- **Section 8**: added Web (new role since v0.3, no prior baseline); all other role sections unchanged — still accurate
- **Section 10**: full rewrite. v0.3's Section 10 covered the retired V1 duty-cycle experiment; this version covers the current, mature `duty-cycle-tick` skill as most roles' actual daily operating mode
- **Sections 1-6, 9**: structure preserved (proven in two prior rounds); Code-era-specific sub-prompts (2.5, 3.5, 6.4) updated to Amber-era-specific equivalents
- **Cadence**: ratified for the first time this round — 6 weeks, derived from actual fielding history, not asserted
