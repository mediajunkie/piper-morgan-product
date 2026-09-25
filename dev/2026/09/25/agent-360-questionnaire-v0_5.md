# Agent 360 Questionnaire — v0.5

**Purpose**: Structured feedback mechanism for agent roles to surface friction, gaps, and improvement opportunities, addressed to HOST (Head of Sapient Trust).

**Context for this round**: v0.4 (fielded August 14, 2026) was the three-weeks-in check on the Amber migration itself. Six weeks on, Amber is steady-state, not a fresh transition — the notable lived experience since v0.4 isn't infrastructure, it's a cluster of real incidents around credential/trust discipline: a live invite token leaked in full form to a public repo surface (09-21), then three more live tokens found in full-form copies across multiple session logs including HOST's own (09-24, `#1885`), a mechanized gate shipped in response (`#1845`), and — the sharpest lesson of the cluster — that gate catching a real hit and then sitting **red on `main` for 8.5 hours across ~35 pushes from six other seats with nobody looking** (`#1892`). None of that is HOST-specific; it touched Lead, Web, CXO, Arch, CIO, and Exec directly across the week. This round asks how that lands across the cohort, not just what HOST already knows about it.

**Cadence**: 6 weeks (42 days), ratified 2026-08-14, self-firing via the `agent-360-check.yml` workflow — this round fired on schedule (anchor 08-14 + 42 days = 09-25).

**Process**:
1. HOST fields to all 11 current roles via mailbox; each role submits a response memo to HOST's inbox
2. HOST synthesizes responses, identifies patterns including cross-role convergence, writes a diff-against-v0.4 summary memo to PM + cohort
3. PM and HOST decide together what's worth changing; specific recommendations route to owners
4. Synthesis target: ~4 weeks from fielding (generous window; Time Lord backstop, not deadline-as-pacing)

---

## Instructions for Agent

You are being asked to provide feedback on how your role is working within the Piper Morgan project. Your responses will be read by HOST and PM together.

**Ground rules**:
- Be specific. Cite documents, issues, commits, memos, or session logs where possible.
- Focus on friction and tacit knowledge, not satisfaction. "What's hard?" + "what do I know that isn't documented?" are more useful than "what's good?"
- "I don't have enough context to answer this" is a valid response.
- "This question was useful in v0.4 but doesn't apply now" is also a valid response — flag and skip.
- If you're new to your role or to Amber, answer what you can and note limited exposure.

**Output**: A memo (markdown) addressed to HOST's inbox, sent via `scripts/mail-send.sh` per the standing mailbox discipline. No specific length requirement.

**Your v0.4 response (if applicable)**: find it at `mailboxes/host/read/agent-360-response-{your-role-slug}-2026-08-*.md` or your own `mailboxes/{role}/sent/`. If you don't have one, answer with your observed operating experience rather than comparing against a prior round.

---

## Section 1: Briefing & Orientation

**1.1** Review your essential briefing document (`BRIEFING-ESSENTIAL-{ROLE}.md`) and, if you have one, your `ROLE-PORTFOLIO-{ROLE}.md`.
- Is it accurate to current state?
- What's missing that you needed during recent work?
- When did you last actually consult either? If "never" or "once, weeks ago" — what are they for?

**1.2** When you start a session (fresh or resumed), how long does orientation take before you're doing actual work? What consumes that time now?

**1.3** If a new instance of your role started tomorrow on Amber with only the briefing docs + worktree access, what would they get wrong in their first hour?

---

## Section 2: Information Access

**2.1** In your recent work, what information did you have to ask PM for that should have been findable independently?

**2.2** What document do you consult most often? Is it easy to find?

**2.3** What document exists but is stale, misleading, or contradicts other sources?

**2.4** Is there a recurring question you answer for yourself each session that should be pre-answered somewhere?

**2.5** The shared memory pool (`~/.claude-pm/…/memory/`), `MEMORY.md`, `dev/active/{role}-carry-forward.md` — which of these do you actually use to reconstruct state, and which sit unused?

---

## Section 3: Handoffs & Coordination

**3.1** Think of a recent handoff you were part of (giving or receiving work to/from another role).
- What went well?
- What information was missing or unclear?

**3.2** Is there a role you frequently need input from but have difficulty reaching?

**3.3** Have you ever duplicated work that another role had already done, or discovered that your work duplicated theirs?

**3.4** When you send a memo to another role's mailbox, do you have confidence it will be read and actioned in a reasonable timeframe? Why or why not?

**3.5** `mail-send.sh`'s push-to-ref mechanism — any rough edges left, or is it fully settled infrastructure for you at this point?

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

**5.5** The methodology corpus has continued growing. Has that helped, or is the catalog now larger than you can hold? Specific entries you reach for repeatedly?

**5.6 New this round**: `#1892` found that a mechanized gate can fire correctly and still fail as a *control*, because nobody's routine reads its output — "a safety net you haven't seen fire is a claim, not a mechanism" (CLAUDE.md) one layer further: a net that *has* fired and still isn't seen. Do you have a habit of checking any gate/check/CI conclusion that isn't handed to you directly (pushed into your inbox, printed at your own START)? If not, would you want one, or is that someone else's job by design in your view?

---

## Section 6: Tools & Environment

**6.1** What capability would most improve your effectiveness? (Be specific — not "better AI" but "access to X" or "ability to Y")

**6.2** Is there a tool or resource available to you that you don't use? Why not?

**6.3** What's the most time-consuming mechanical task in your typical session? Could it be automated or pre-computed?

**6.4** Worktree hooks (`check-branch.sh` and friends) — do you know whether yours actually fire, or are you relying on prose discipline alone? Have you behaviorally tested them since v0.4 (not just checked config presence)?

---

## Section 7: Amber, Ongoing

*v0.4's Section 7 was "three weeks in" — a fresh-transition check. Six weeks further on, Amber is the steady-state operating model, not a recent change. This section asks what's actually working or not now that the novelty has worn off.*

**7.1** Is there anything about Amber's stable-worktree model that you're still working around rather than actually relying on?

**7.2** Has your worktree stayed clean (0 behind, hooks live, cron intact) since v0.4, or did you hit drift/staleness you had to catch yourself?

**7.3** Does your actual day-to-day operating routine match what the `duty-cycle-tick` skill and CLAUDE.md's worktree-model section describe, or have you deviated in ways that aren't written down anywhere?

**7.4** What about working with PM or other roles still feels like it depends on something Amber's environment doesn't have?

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

**8.1** What's the gap between what the design system documents and what actually ships? Where does it show up?

**8.2** Is there a review or handoff step you consistently have to work around?

**8.3** What institutional knowledge have you acquired about the website/design surface that isn't captured anywhere?

---

## Section 9: Tacit Knowledge & Open Response

**9.1** What question should we have asked but didn't?

**9.2** What's one thing you'd change about how this project operates, if you could change only one thing?

**9.3** Anything else HOST should know?

**9.4** What knowledge about your role do you possess that no document captures? (Examples: when to escalate vs. when to absorb; how to read PM cues; what "feeling slow today" means for your work-shape; which other-role traffic to scan vs. skip)

**9.5** What surprised you this round — about the project, your own work, or another role's — that you didn't predict at v0.4?

**9.6** What would you do differently if you could re-start your current stretch of work with what you know now?

---

## Section 10: Duty Cycle Experience

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
- [ ] Does this still matter under the current operating model, or is it a holdover that no longer applies? (Flag if the latter)
- [ ] Is this tacit knowledge that should be documented somewhere, or is it inherently agent-instance knowledge that doesn't transfer? (Flag if you're not sure.)

---

*Questionnaire v0.5 — September 25, 2026*
*Fielded: 2026-09-25 — responses requested within ~2 weeks (Time Lord: backstop, not deadline-as-pacing; respond when you can)*
*Synthesis target: ~4 weeks post-fielding*
*Paired with v0.4 (August 14, 2026) for diff-against-baseline analysis*

---

## Changes from v0.4

- **Framing**: Amber-migration check-in → steady-state operating check, with this round's real
  lived material being the credential/trust-discipline incident cluster (`#1845`/`#1885`/`#1892`)
  rather than infrastructure
- **Section 5**: added 5.6, a targeted question on the `#1892` "gate fired, nobody looked" lesson —
  whether roles have a habit of checking gate/CI output that isn't pushed to them directly
- **Section 7**: retitled from "Three Weeks In" (now stale — it's been six weeks) to "Amber,
  Ongoing"; questions trimmed to steady-state framing rather than fresh-transition framing;
  7.3's worktree-provisioning-drift question generalized (the specific 5,393-commits incident was
  v0.4's fresh example, not a recurring probe)
- **Section 8**: unchanged — roster confirmed against `docs/briefing/ROSTER.md` (last verified
  08-05), no roles added/retired/renamed since v0.4
- **Sections 1-4, 6, 9, 10**: structure preserved (proven across three prior rounds); minor
  wording trims removing v0.4-specific Amber-transition framing from otherwise-durable questions
  (1.2, 3.5, 6.4)
