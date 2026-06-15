# Agent Skills Index

This directory contains formalized Agent Skills - self-contained procedural instructions that transform Claude from general-purpose to specialized for specific recurring tasks.

**Last Updated**: 2026-05-15

---

## Available Skills

| Skill | Scope | Description | Version |
|-------|-------|-------------|---------|
| [create-session-log](./create-session-log/SKILL.md) | Cross-role | Create properly named session logs; one log per role per day | 1.0 |
| [check-mailbox](./check-mailbox/SKILL.md) | Cross-role | Check inbox at session start, process messages, move to read/ | 1.0 |
| [close-issue-properly](./close-issue-properly/SKILL.md) | Cross-role | Close GitHub issues with evidence, updated descriptions, audit-ready records | 1.0 |
| [audit-cascade](./audit-cascade/SKILL.md) | Cross-role | Systematic audit-and-correct between phases; implements Pattern-049 | 1.0 |
| [discovered-work-capture](./discovered-work-capture/SKILL.md) | Cross-role | Capture discovered issues immediately; prevents invisible work | 1.0 |
| [publish-to-blog](./publish-to-blog/SKILL.md) | Role-specific | Publish finished blog post to pipermorgan.ai; bridge editorial calendar to website repo | 0.4 |
| [draft-blog-post](./draft-blog-post/SKILL.md) | Role-specific | Draft a blog post (narrative, insight, or Weekly Ship); carries voice discipline upstream from voice-pass to draft-time | 1.0 |
| [cleanup-dev-active](./cleanup-dev-active/SKILL.md) | Cross-role | Triage and archive stale files from dev/active/; prevents working directory bloat | 1.0 |
| [draft-weekly-ship](./draft-weekly-ship/SKILL.md) | Exec | Draft the Weekly Ship newsletter from workstream memos; loads canonical artifacts (process guide / template / voice guide / latest published Ship) before drafting | 1.0 |
| [duty-cycle-tick](./duty-cycle-tick/SKILL.md) | Cross-role | Execute one autonomous duty-cycle fire (START/WATCH/WORK/STOP); holds the durable procedure so the cron prompt stays thin. **PoC (CIO dogfooding 2026-06-06)** | 1.0 |
| [draft-issue](./draft-issue/SKILL.md) | Cross-role | Draft a properly-formed GitHub issue with SLUG, structured body (Problem Statement / Goal / Requirements / AC), and correct metadata. Trigger: "file an issue", "create a ticket", "track this". **Wave 1 PM skill (2026-06-14)** | 1.0 |
| [close-issue](./close-issue/SKILL.md) | Cross-role | Close a GitHub issue properly — update description checkboxes (every unchecked box explained), add evidence comment, then close. Portable to any PM's GitHub workflow. Trigger: "close the issue", "mark complete", "wrap up #N". **Wave 1 PM skill (2026-06-15)** | 1.0 |
| [draft-spec](./draft-spec/SKILL.md) | Cross-role | Turn a rough idea into a complete, reviewable feature spec / PRD — with problem statement, non-goals, user stories, requirements, open questions, and success criteria, grounded in your project context. Trigger: "write a spec", "draft a PRD", "spec this out". **Wave 1 PM skill (2026-06-15)** | 1.0 |
| [synthesize-feedback](./synthesize-feedback/SKILL.md) | Cross-role | Distill themes from raw user feedback (interviews, tickets, surveys, reviews) into prioritized themes with evidence, severity, and roadmap recommendations. Distinguishes volume from severity. Trigger: "synthesize this feedback", "what are users saying", "themes from this research". **Wave 1 PM skill (2026-06-15)** | 1.0 |
| [update-piper](./update-piper/SKILL.md) | Cross-role | Refresh Piper's PM profile when things change — shows current profile first, then updates only stale sections. Keeps meet-piper from degrading over time. Trigger: "things have changed", "update my profile", "Piper doesn't know about X". **Wave 1 PM skill (2026-06-15)** | 1.0 |

---

## Skill Tiers

### Tier 1: Cross-Role Foundation (Mandatory)
Skills every agent should know. High frequency, low complexity.

- **create-session-log** - Start of every session
- **check-mailbox** - Session start protocol
- **close-issue-properly** - End of every tracked task
- **audit-cascade** - Between every phase of multi-step work (Pattern-049)
- **discovered-work-capture** - When noticing issues during development

### Tier 2: Role-Specific Operations
Skills for specific workflows or roles.

- **publish-to-blog** - Docs/Comms: publish finished post to pipermorgan.ai, update editorial calendar
- **draft-weekly-ship** - Exec: draft Weekly Ship newsletter from workstream memos using canonical artifacts
- **draft-blog-post** - Comms: draft narrative / insight / Ship for editorial-calendar slot; voice + verifiable-claims discipline upstream
- **create-omnibus-log** - *(planned)* Docs agent daily synthesis
- **create-gameplan** - *(planned)* Lead Dev sprint planning
- **run-debug-protocol** - *(planned)* Systematic debugging framework

### Tier 3: Specialized Processes
Less frequent but high-value skills.

- **pattern-sweep-execution** - *(planned)* 6-week pattern analysis
- **anti-pattern-scan** - *(planned)* Emergent anti-pattern detection
- **create-adr** - *(planned)* Architecture decision records

---

## How to Use Skills

**Invoking a skill**: Reference by name when starting relevant work.
```
"Use the create-session-log skill to start this session."
```

**When to use**: Skills are triggered by specific contexts documented in each SKILL.md's "When to Use" section.

**Skill anatomy**: Each skill contains:
- Trigger patterns (when to use)
- Step-by-step procedure
- Anti-patterns to avoid
- Quality checklist
- Examples

---

## Skill Formalization Trigger

**When**: During each pattern sweep (6-week cadence)
**Where**: Phase 5 of pattern sweep template

### Formalization Rubric

Score candidates against these 5 criteria. **Formalize when score ≥ 3**:

| Criterion | Weight | Signal |
|-----------|--------|--------|
| **Frequency** | 1 | Happens 3+ times per week across agents |
| **Friction** | 1 | Agents doing it inconsistently or asking "how?" |
| **Error Cost** | 1 | Mistakes cause rework or PM intervention |
| **Docs Exist** | 1 | Procedure already written somewhere (not yet a skill) |
| **Cross-Role** | 1 | Multiple roles need it (higher multiplier effect) |

### Evaluation Process

During each pattern sweep:
1. Review `dev/active/skill-harvest-candidates.md` for pending candidates
2. Score top 3-5 candidates against rubric
3. Formalize any scoring ≥ 3
4. Add new candidates discovered during sweep
5. Update adoption status in this index

### Example Scoring

| Candidate | Freq | Friction | Error | Docs | Cross | Score | Action |
|-----------|------|----------|-------|------|-------|-------|--------|
| create-omnibus-log | ✓ | ✓ | | ✓ | | 3 | Formalize |
| run-debug-protocol | ✓ | ✓ | ✓ | ✓ | ✓ | 5 | Formalize |
| create-adr | | | | ✓ | | 1 | Wait |

---

## Creating New Skills

New skills follow the harvest → spec → draft → audit → pilot workflow:

1. **Identify candidate** from methodology docs, CLAUDE.md, or observed patterns
2. **Write specification** in `dev/active/skill-{name}-spec.md`
3. **Draft SKILL.md** in `.claude/skills/{name}/SKILL.md`
4. **Audit** against spec and best practices
5. **Pilot test** with realistic scenarios
6. **Add to this index** with scope and version

**Metadata requirements** (per CIO guidance):
```yaml
---
scope: cross-role | role-specific
version: 1.0
created: YYYY-MM-DD
---
```

---

## Skill Adoption Status

| Phase | Status | Date |
|-------|--------|------|
| Pilot: create-session-log | Complete | 2026-01-21 |
| Pilot: close-issue-properly | Complete | 2026-01-21 |
| Tier 1: check-mailbox | Complete | 2026-01-21 |
| Tier 1: audit-cascade | Complete | 2026-01-23 |
| Tier 1: discovered-work-capture | Complete | 2026-01-26 |
| Tier 1 rollout | In Progress | - |
| Tier 2 development | Planned | - |

---

## References

- **CIO Memo**: `mailboxes/cio/memo-skill-adoption-proposal-2026-01-21.md`
- **Skill Candidates**: `dev/active/skill-harvest-candidates.md`
- **anthropics/skills spec**: External reference for skill format best practices
