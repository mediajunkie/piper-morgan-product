---
name: draft-issue
description: Draft a properly-formed GitHub issue for your project repo. Use when
  PM has a problem, bug, feature idea, or task to track. Produces a SLUG, structured
  body (Problem Statement / Goal / Requirements / AC), and correct metadata (priority,
  labels, milestone, epic). Trigger phrases: "file an issue", "create a ticket",
  "draft an issue", "track this", "we should file a bug for".
scope: cross-role
version: 1.1
created: 2026-06-14
---

# draft-issue

Turn a problem statement into a properly-formed GitHub issue — with SLUG, structured body, correct metadata, and checkboxes you can audit at close.

## When to Use

- PM has a problem, bug, feature idea, or task to track
- You've discovered work that needs filing (see also: `discovered-work-capture`)
- You're creating child issues under an epic
- You want to hand well-formed context to Lead Dev or another agent

## Procedure

### Step 1 — Gather context

Identify the minimum needed to draft well. Read from the current conversation first; only ask PM for what's genuinely missing.

**Detect the issue tracker first**:
```bash
git remote get-url origin 2>/dev/null | sed 's/.*github.com[:/]//' | sed 's/.git$//'
```

- **GitHub remote found** → use that repo for `gh issue create --repo OWNER/REPO`
- **No GitHub remote** → ask PM: "Which issue tracker are you using? (GitHub repo, Linear, Jira, etc.)" Then adapt the draft format and create command accordingly. If PM says they haven't connected an issue tracker yet, let them know that `/connect-piper` (coming in the RECONNECT sprint) will wire this up — for now, offer to draft the issue body as a document they can file manually.
- **No tracker at all** → still draft the full issue body; PM can copy-paste to their tracker of choice.

**Required**:
- Problem or goal (what needs to happen, and why)

**Infer from context or ask if unclear**:
- Type: bug / enhancement / research / architecture / technical-debt
- Milestone: MVP (current focus) | Fast Follow | Post-MVP | Enterprise — default to MVP if work is clearly near-term
- Priority: P0 (critical, blocks everything) | P1 (high, in current sprint) | P2 (medium) | P3 (low/nice-to-have) — default P2 if unspecified
- Parent epic: `#N (SLUG)` if this is a child of an existing epic; omit if standalone

**Never block on missing metadata** — make a reasonable inference, note it in the draft, and let PM correct.

### Step 2 — Generate the SLUG

`SLUG` = short uppercase hyphenated label derived from the title. Aim for 2–4 words, 15 chars max.

Examples:
- "Add GitHub connector to meet-piper onboarding" → `CONNECT-GITHUB`
- "Fix enriched re-ask payload error in consult-piper" → `CONSULT-PAYLOAD-FIX`
- "Collapse ask-piper and consult-piper into one smart skill" → `PIPER-SKILL-MERGE`

### Step 3 — Draft the issue body

Use this template. Fill every section; if a section genuinely doesn't apply (e.g. no existing infrastructure), say "None — greenfield" rather than leaving it blank.

```markdown
# SLUG — Full descriptive title

**Priority**: P[0-3]
**Labels**: `type-label`, `component-label` (see reference below)
**Milestone**: [MVP | Fast Follow | Post-MVP | Enterprise]
**Epic**: #N (SLUG) — omit if standalone
**Related**: #N (description); `path/to/file.py:line` (relevant code); ADR-NNN (if architecture decision applies)

---

## Problem Statement

### Current State
[What exists today and why it falls short. Be specific — cite file paths, behavior, or user experience.]

### Impact
- **Blocks**: [what this prevents, or "Nothing — standalone improvement"]
- **User Impact**: [what a PM using Piper experiences because of this gap]
- **Technical**: [any debt or coupling implications, if relevant]

### Strategic Context
[Why this matters now. One or two sentences connecting to current sprint or product direction.]

---

## Goal

**Primary Objective**: [One sentence: what success looks like when this is closed.]

**Example User Experience**:
```
Before: [concrete description of what fails or is missing]
After:  [concrete description of what works]
```

**Not In Scope**:
- ❌ [explicit exclusion 1 — prevents scope creep]
- ❌ [explicit exclusion 2]

---

## What Already Exists

### Infrastructure
- `path/to/relevant/file.py:line` — [what it does that's relevant]
- [Or: "None — greenfield"]

### What's Missing
- ❌ [specific gap 1]
- ❌ [specific gap 2]

---

## Requirements

### Phase 1: [First meaningful chunk of work]
- [ ] [Specific, testable requirement]
- [ ] [Specific, testable requirement]

### Phase 2: [Next chunk — omit if single-phase]
- [ ] [Specific, testable requirement]

### Phase Z: Completion & Handoff
- [ ] All AC met with evidence documented
- [ ] Run the `close-issue` skill: update description checkboxes (mark done `[x]`, explain any unchecked with Deferred/N/A/Won't do), add a closing comment with evidence, then close

---

## Acceptance Criteria

- [ ] [Concrete, user-visible outcome 1]
- [ ] [Concrete, user-visible outcome 2]
- [ ] Tests exist and pass (if code change)
- [ ] No regressions in related functionality
```

### Step 4 — Propose metadata

Below the draft, show PM the proposed `gh issue create` command so they can approve or tweak before it runs:

```bash
gh issue create \
  --repo OWNER/REPO \
  --title "SLUG — Full title" \
  --label "enhancement,component: ui" \
  --milestone "MVP" \
  --body-file /tmp/issue-draft.md
```

### Step 5 — Create on PM approval

Wait for PM to say "looks good" or make corrections. Then:

```bash
# Write body to temp file (avoids shell escaping issues)
cat > /tmp/issue-draft.md << 'BODY'
[paste full body here]
BODY

gh issue create \
  --repo OWNER/REPO \
  --title "SLUG — Full title" \
  --label "enhancement" \
  --milestone "MVP" \
  --body-file /tmp/issue-draft.md
```

Note the issue number returned. If this is a child of an epic, add a comment to the epic linking it:
```bash
gh issue comment EPIC_NUMBER --repo OWNER/REPO \
  --body "Child issue filed: #NEW_NUMBER (SLUG)"
```

---

## Label Quick Reference

**Type** (pick one):
- `bug` — something broken
- `enhancement` — new feature or improvement
- `technical-debt` — refactor / cleanup
- `documentation` — docs only
- `type: research` — investigation / discovery

**Component** (pick one or more):
- `component: ui` — frontend / templates
- `component: api` — API endpoints
- `component: integration` — external integrations (GitHub, Notion, Calendar)
- `component: ai` — LLM / intent / floor
- `component: database` — schema / migrations
- `component: workflow` — orchestration / skills

**Priority** (one):
- `P0-critical` — blocks everything, fix now
- `P1` — in current sprint, high urgency
- *(P2 and P3 are implicit in milestone assignment; no separate label needed)*

**Status** (add if relevant):
- `status: blocked` — waiting on something external

---

## Anti-Patterns to Avoid

| Don't | Why | Do Instead |
|---|---|---|
| Vague title ("Fix bug") | Untraceable | SLUG + specific description |
| Acceptance criteria that can't be tested | Uncloseable | Every AC must be binary pass/fail |
| Empty "What Already Exists" | Agent starts from scratch unnecessarily | Even "None — greenfield" is better than blank |
| Create without PM review | PM may reframe scope or priority | Step 4 always shows the command first |
| Unchecked boxes at close | Looks incomplete forever | `close-issue-properly` requires all boxes explained |

---

## Quality Checklist

Before showing the draft to PM:
- [ ] SLUG is ≤15 chars, uppercase, hyphenated
- [ ] Title is descriptive enough to understand without reading the body
- [ ] Every section is filled (or explicitly "None" / "N/A")
- [ ] Acceptance criteria are binary and testable
- [ ] Phase Z references `close-issue` skill
- [ ] `gh issue create` command is shown for PM approval

---

## Example

**Input** (from conversation):
> "We should file an issue for adding GitHub connector setup to meet-piper — right now onboarding doesn't ask you to wire GitHub so consult-piper can never enrich."

**Inferred metadata**: enhancement, component: integration, MVP milestone, P1 (it's a blocker for enrichment), no obvious parent epic yet.

**SLUG**: `MEET-PIPER-GITHUB`

**Draft title**: `MEET-PIPER-GITHUB — Add GitHub connector setup to meet-piper onboarding`

**Draft body**:

```markdown
# MEET-PIPER-GITHUB — Add GitHub connector setup to meet-piper onboarding

**Priority**: P1
**Labels**: `enhancement`, `component: integration`
**Milestone**: MVP
**Epic**: — (standalone; candidate to roll into a meet-piper improvement epic)
**Related**: `ask-piper` skill; `consult-piper` enrichment layer; BYOC 2a gate-run findings 2026-06-14

---

## Problem Statement

### Current State
`meet-piper` interviews PM about working style but does not prompt them to wire any connectors (GitHub, Calendar, Notion). As a result, the enrichment layer in `consult-piper` has nothing to query — GitHub is listed as a "user-named" integration in the profile but not connected.

### Impact
- **Blocks**: `consult-piper` enrichment in Cowork (can't fetch GitHub issues to ground responses)
- **User Impact**: PM asks Piper about their sprint and gets a floor response instead of a grounded one
- **Technical**: Enrichment-dependent skills (sprint-plan, milestone-check, triage-backlog) all degrade without this

### Strategic Context
Connector setup during onboarding is the single highest-leverage fix for the enrichment layer. Identified as a gap in the BYOC 2a gate-run 2026-06-14; filed as part of the Wave 1 skills taxonomy core set.

---

## Goal

**Primary Objective**: After completing meet-piper, PM's GitHub account is connected and available for enrichment in consult-piper and future skills.

**Example User Experience**:
```
Before: meet-piper finishes without asking about GitHub; consult-piper floors.
After:  meet-piper walks PM through connecting GitHub; consult-piper enriches from their repo.
```

**Not In Scope**:
- ❌ Connecting Calendar or Notion (separate issues; GitHub is the highest-value connector)
- ❌ Re-architecting the connector storage model

---

## What Already Exists

### Infrastructure
- `meet-piper` SKILL.md — interview flow exists; needs connector step added
- GitHub integration in `services/integrations/github/` — connector logic exists server-side
- Profile storage — PM profile is server-side; connector state is the gap

### What's Missing
- ❌ Connector setup step in meet-piper interview flow
- ❌ GitHub token storage during onboarding

---

## Requirements

### Phase 1: Add connector step to meet-piper
- [ ] meet-piper prompts PM to connect GitHub after the working-style interview
- [ ] Provides clear instructions for supplying a GitHub token (or PAT)
- [ ] Stores the token via `KeychainService` under the correct account pattern

### Phase Z: Completion & Handoff
- [ ] AC met with evidence (consult-piper can enrich after running meet-piper)
- [ ] Session log updated; close-issue-properly followed

---

## Acceptance Criteria

- [ ] Running meet-piper includes a GitHub connector step
- [ ] After completing meet-piper, consult-piper successfully enriches a question with GitHub context
- [ ] Token is stored and retrievable across sessions
```

**Proposed create command**:
```bash
gh issue create \
  --repo OWNER/REPO \
  --title "MEET-PIPER-GITHUB — Add GitHub connector setup to meet-piper onboarding" \
  --label "enhancement,component: integration" \
  --milestone "MVP" \
  --body-file /tmp/issue-draft.md
```

---

## Changelog

- **v1.0** (2026-06-14): Initial version. Written for Piper Morgan Wave 1 skills taxonomy. Deployment: Native + Plugin.
