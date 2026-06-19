---
name: piper-sprint-plan
description: Scope a sprint from the GitHub backlog — review open issues, apply capacity
  and velocity, surface dependencies and risks, and produce a proposed sprint with
  rationale. Works without GitHub connector (manually-supplied backlog) but is significantly
  richer with it. Trigger phrases: "let's plan the sprint", "help me scope [sprint
  name]", "what should go in this sprint", "which issues should we tackle next".
scope: cross-role
version: 1.0
created: 2026-06-15
---

# sprint-plan

Scope a sprint from your backlog — select what to pull in, flag what to leave out, surface dependencies, and produce a proposed sprint with rationale PM can accept, adjust, or reject.

## Why this exists

Sprint planning without a thinking partner defaults to: PM opens the backlog, picks things they recognize, fills up until it feels full, and hopes it's right. The failure modes are predictable:
- Pulling in work without considering what it blocks or what it depends on
- Capacity optimism (sprints fill at 100%; velocity is usually 60–80%)
- Missing the 1–2 high-leverage issues that would advance the product most
- No explicit "and therefore we're NOT doing X" reasoning

Piper's value here isn't running the planning for PM — it's being the thinking partner who asks the right questions before the sprint starts.

**With the GitHub connector**: Piper can pull actual open issues, read their labels and milestone assignments, check closed-issue velocity, and propose a specific sprint scope.

**Without the GitHub connector**: Piper asks PM to supply the candidate list and works as a structured sounding board — better than solo planning, just not automated.

## Procedure

### Step 1 — Establish the planning frame

Confirm with PM:
- **Sprint length**: 1 week / 2 weeks / other
- **Team / capacity**: who's working this sprint, any known absences
- **Velocity reference**: how many issues/points does the team typically close? (If unknown, estimate from recent sprints)
- **Sprint goal**: is there a theme or outcome this sprint is organizing around? (Optional, but dramatically improves selection)
- **Any fixed constraints**: must-have items (committed work, customer asks), must-exclude items (blocked, not ready)

### Step 2 — Pull or receive the backlog

**With GitHub connector:**
- Query open issues from the relevant milestone or label
- Filter to: unblocked items (no open blockers filed against them) + not assigned to a future milestone explicitly
- Sort by: priority label if present, then by age (older backlog items often represent forgotten important work)
- Surface top 2× velocity as candidates (more than will fit, so selection is deliberate)

**Without GitHub connector:**
- Ask PM to provide the candidate list: "Paste the issues you're considering or describe them briefly — I'll help you structure the selection from there."

### Step 3 — Apply the selection framework

For each candidate, Piper evaluates:

| Dimension | Question | Signal |
|---|---|---|
| **Goal alignment** | Does this advance the sprint goal? | Deprioritize if no clear connection |
| **Dependency check** | Does this block or get blocked by other sprint work? | Surface the dependency; plan in the right order |
| **Scope clarity** | Is this well-enough defined to work this sprint? | "Needs spec" items should not be sprint candidates |
| **Size fit** | Does capacity math work out if this is included? | Simple estimate — S/M/L, not points required |
| **Risk** | If this slips, does it cascade? | Flag high-risk items; don't ignore them |

This framework isn't run as a checklist for every item — Piper flags the issues where a dimension matters, not all dimensions for all issues.

### Step 4 — Propose the sprint

Present a proposed sprint scope with rationale:

```markdown
## Proposed sprint: [sprint name / dates]

**Goal**: [one sentence — what does a successful sprint look like?]

**Capacity**: [team members] × [sprint length] = ~[X] items at current velocity

---

### In — proposed sprint scope

| # | Issue | Why in |
|---|---|---|
| #[n] | [title] | [1-line rationale — goal alignment / dependency / customer impact] |
| #[n] | [title] | [rationale] |
| ...  | | |

**Sprint confidence**: [High / Medium / Low] — [one sentence on what makes this achievable or risky]

---

### Out — explicitly not this sprint

| Issue | Why out |
|---|---|
| #[n] — [title] | [reason: blocked / needs spec / future milestone / capacity] |
| #[n] — [title] | [reason] |

*"Out" is deliberate, not forgotten. Review these at next planning.*

---

### Watch list — items that might join if something slips

| Issue | Condition |
|---|---|
| #[n] — [title] | If [other item] finishes early |

---

### Dependencies and risks

- [Dependency or risk 1 — specific, with what to do about it]
- [Dependency or risk 2]

---

### Questions before starting

- [Any clarification needed from PM before the sprint locks]
```

### Step 5 — Invite adjustment

After presenting the proposal:
- "What would you change?"
- "Is the goal right, or is there a higher-priority outcome this sprint should serve?"
- "Anything in the Out list that should actually be In?"

The proposal is a starting point. PM owns the sprint.

---

## Sprint planning without a goal

Sprint goals make selection dramatically easier — everything gets evaluated against one criterion. When PM doesn't have an explicit goal, Piper can help surface one:

"Looking at what's in the backlog, the natural organizing theme this sprint seems to be [X]. Would that work as the sprint goal? If so, it makes [issues Y and Z] clear priorities."

Don't impose a goal if PM doesn't want one — some teams work from a flat prioritized backlog and that's fine. But offering it is useful.

---

## Capacity math (simple version)

PMs tend to over-commit sprints. Piper's default assumption without better data:

- 1-person sprint at full availability → ~60–70% of raw time is "productive issue work" (accounting for meetings, async, context-switching)
- Team velocity is usually 60–80% of what the sprint board shows when it fills up

If PM has better data (actual closed-issue counts from recent sprints), use that. If not, apply the conservative default and label it clearly: "This estimate is conservative — adjust if you know your actual velocity."

---

## Handling "we don't use sprints"

Some teams (particularly early-stage or solo PMs) don't do formal sprints. The skill still applies as a **periodic backlog review and prioritization**:

- "Help me pick what to focus on this week"
- "Which of these 10 issues should I do first"

Replace "sprint" with "week" or "focus period" in the output. The framework — goal alignment, dependency check, scope clarity, capacity — applies either way.

---

## Anti-patterns to avoid

| Don't | Why | Instead |
|---|---|---|
| Fill the sprint to 100% of capacity | No room for unexpected work | Target 70–80% and name the buffer |
| Pull items without "why in" rationale | No one remembers next sprint why they picked it | Every "in" item has a reason |
| Skip the "out" list | The "not this sprint" is a decision, not an omission | Name what's out and why |
| Ignore dependencies | Two sequential items in same sprint means the second can only start late | Surface the order constraint |
| Treat sprint plan as a commitment | Sprints are forecasts, not promises | Frame as "what we're aiming for" |
| Plan without a goal when the team has one | Misses the organizing principle | Ask for it; offer to surface one from the backlog |

---

## Quality checklist

Before presenting the sprint proposal:
- [ ] Capacity frame is established (team, length, velocity)
- [ ] Sprint goal is stated or absent-and-noted
- [ ] Every "in" item has a 1-line rationale
- [ ] "Out" list is explicit — not just "everything not in"
- [ ] Dependencies between sprint items are flagged
- [ ] Sprint confidence level is honest (not always "high")
- [ ] PM is explicitly invited to adjust — proposal ≠ final

---

## Example

**Brief from PM**: "Help me plan the next 2-week sprint. We're a team of 3, one person is part-time. Our focus this sprint is getting the onboarding flow ready for beta. GitHub is wired, so pull what you can."

**Piper's output** (abbreviated):

```markdown
## Proposed sprint: [Beta Prep] — June 16–27

**Goal**: Get onboarding flow to beta-ready: a new user can sign up, complete setup, and reach their first meaningful action without assistance.

**Capacity**: 2.5 FTE × 2 weeks. At typical velocity (~8 medium issues), targeting 6–7 items.

---

### In — proposed sprint scope

| # | Issue | Why in |
|---|---|---|
| #412 | Fix onboarding step 2 validation | Blocking; reported by 3 users in closed beta |
| #389 | Add email confirmation flow | Required for beta launch — currently skipped |
| #401 | "What next?" empty state after setup | Without this, users complete setup and see nothing |
| #440 | Onboarding analytics events | Need to know where users drop before beta |
| #388 | Fix mobile viewport on setup step 3 | ~40% of signups are mobile; this is broken |
| #435 | Write onboarding help doc | Reduces support load; can ship async |

**Sprint confidence**: Medium — #389 (email confirmation) is the highest-risk item; if it takes longer than 3 days, it could crowd out #401.

---

### Out — explicitly not this sprint

| Issue | Why out |
|---|---|
| #312 — SSO integration | Not beta-required; no customer ask yet |
| #394 — Onboarding A/B test | Needs analytics (#440) first; defer to sprint 2 |
| #367 — Admin onboarding controls | Internal-facing; PM is the only admin right now |

---

### Dependencies

- #440 (analytics) should complete in week 1 so beta data is available from launch day
- #389 (email confirmation) blocks nothing else in sprint but is the riskiest item — start it Monday

---

### Questions before starting

- Is the empty state (#401) PM-approved in terms of copy/design, or does that still need a call?
```

---

## Changelog

- **v1.0** (2026-06-15): Initial version. Goal-aligned sprint selection with explicit "in / out / watch" structure, dependency surfacing, and capacity math. Richer with GitHub connector but workable without.
