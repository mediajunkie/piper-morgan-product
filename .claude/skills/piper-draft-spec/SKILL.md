---
name: piper-draft-spec
description: >-
  Turn a rough idea, brief, or conversation into a properly-formed feature
  spec / PRD — with problem statement, goals, non-goals, user stories,
  requirements, open questions, and success criteria. Piper grounds the spec
  in your project context. Trigger phrases: "write a spec for", "draft a PRD",
  "spec this out", "write this up properly", "I want to build X".
---

# draft-spec

Turn a rough idea into a complete, reviewable feature spec — structured so engineers can build from it and stakeholders can approve it without a meeting.

The difference from just asking Piper: this skill produces a **consistent output shape** (every section present, every non-goal explicit, every open question surfaced) and **grounds the spec in your project context** (team patterns, current sprint, existing infrastructure) rather than writing a generic document.

## When to Use

- PM has an idea and wants it written up properly before handing it to engineering
- You're planning a feature and want to flush out scope, non-goals, and open questions
- You need a shareable artifact for stakeholder review or team alignment
- You want to create GitHub issues from a spec (use `draft-issue` for each requirement chunk after the spec is done)

**Not for**: quick one-off tasks (use `draft-issue` directly). Not for architecture decisions (use ADR process). Not for bug fixes (use `draft-issue`).

## The Core Insight

A spec's most valuable sections aren't the requirements — they're the **non-goals** and **open questions**. Requirements tell engineers what to build; non-goals tell them what to push back on; open questions tell them where to stop and ask rather than guess. Most AI-generated specs skip both. Don't.

## Procedure

### Step 1 — Gather the brief

Start from whatever PM has: one sentence, a conversation, a rough list, a prototype description. Read it fully. Identify what's clear and what's ambiguous.

**Ask PM for the following if not already known:**
- Who is the primary user? (which persona, role, or segment)
- What's the one-sentence version of what changes for them?
- Are there constraints you know about? (tech debt, timeline, dependencies)
- Is there a milestone this belongs to?

**Don't ask** about things you can infer: if PM is talking about a PM feature, the user is probably a PM. If the conversation mentions a sprint, note the milestone. Keep the ask short — 1-3 questions max.

### Step 2 — Load Piper context

Before drafting, pull what Piper knows that's relevant. If you have access to Piper's profile data:
- Current active projects and their state
- Team members and their roles
- Existing related features and how they work
- Current sprint focus and what's in flight

If running natively (no server access): use conversation context + your knowledge of this PM's domain. Note what you couldn't verify.

### Step 3 — Generate the SLUG and title

`SLUG` = short uppercase hyphenated label for the feature area. 2–4 words, 15 chars max. Same convention as `draft-issue`.

Examples:
- "Add AI-powered backlog triage" → `AI-TRIAGE`
- "Onboarding flow for first-time PMs" → `PM-ONBOARDING`
- "Weekly digest email" → `WEEKLY-DIGEST`

**Title format**: `SLUG — Full descriptive name`

### Step 4 — Draft the spec

Use the template below. Every section is mandatory — write "None identified" or "N/A" rather than leaving a section blank. Omissions make the spec look incomplete even when it isn't.

```markdown
# SLUG — Full feature name

**Status**: DRAFT
**Author**: [PM name]
**Created**: [date]
**Milestone**: [MVP | Fast Follow | Post-MVP | Enterprise]
**Related issues**: [#N — title, or "None yet"]

---

## TL;DR

[One paragraph. What is this feature, who is it for, and why does it matter now?
Write this last — it's easier once the rest is done.]

---

## Problem

### Who has this problem?
[Specific user or persona — not "users" generically. E.g.: "First-time PMs who haven't used Piper before and don't know what to ask it."]

### What happens today?
[Concrete description of the current experience — what fails, what's missing, what workaround they use.]

### Why does it matter?
[Impact: what this costs the user or the product. Connect to a metric or outcome if you can.]

### Why now?
[What makes this the right time? Sprint focus, dependency unblocked, PM request, user signal.]

---

## Goals

### Primary goal
[One sentence: the change in user experience this spec delivers.]

### Secondary goals (optional)
- [Additional benefit 1]
- [Additional benefit 2]

---

## Non-goals

[What this spec explicitly does NOT cover. Be specific — "we're not building X" is more useful than silence on X. Every non-goal here prevents a scope conversation later.]

- ❌ [Thing that sounds related but is out of scope]
- ❌ [Follow-on feature that would naturally come next but isn't here]
- ❌ [Edge case that would add complexity without proportionate value]

---

## User stories

[2–5 stories in "As a [persona], I want to [action], so that [outcome]" form.
Keep them user-facing — not implementation steps.]

1. As a [persona], I want to [action], so that [outcome].
2. As a [persona], I want to [action], so that [outcome].
3. [etc.]

---

## Requirements

[Group by logical phase or area. Use checkboxes so these can become GitHub issue acceptance criteria directly.]

### [Area or Phase 1]
- [ ] [Specific, testable requirement — describes observable behavior, not implementation]
- [ ] [Specific, testable requirement]

### [Area or Phase 2]
- [ ] [Specific, testable requirement]

### Edge cases and error handling
- [ ] [What happens when X fails or is missing]
- [ ] [What happens with invalid input]

---

## Design notes

[Wireframes, UX flows, or key interaction decisions — or "None yet; PM/design team to drive." Don't block the spec on design; note what's known and what's open.]

---

## Technical notes

[Relevant existing infrastructure, dependencies, or known constraints — or "No constraints identified." Don't write implementation instructions here; write what engineers need to know to estimate and not hit surprises.]

- [Relevant existing service/component and how it connects]
- [Known dependency or constraint]
- [Or: "No constraints identified. Greenfield."]

---

## Open questions

[Every spec has questions. Surface them here rather than letting engineers discover them mid-build. Each question should have an owner and a "needed by" date if the spec has a timeline.]

| Question | Owner | Needed by |
|---|---|---|
| [Specific question that blocks or significantly changes scope] | [PM / CXO / Lead Dev] | [date or "before kick-off"] |
| [Another question] | [owner] | [date] |

---

## Success criteria

[How will you know this shipped successfully? Binary pass/fail — not "users like it." Prefer measurable or verifiable criteria.]

- [ ] [Observable outcome 1 — can be checked without user research]
- [ ] [Observable outcome 2]
- [ ] User can complete [key flow] without hitting an error
- [ ] [Metric or behavior that confirms the problem is solved]

---

## Out of scope (carry-forward)

[Features or edge cases that came up in discussions and were explicitly parked for a later spec. This is where "not now" goes so it's findable later.]

- [Feature or edge case] — [brief reason for deferral]
- [Or: "None identified"]
```

### Step 5 — Review with PM

Show the draft. Highlight:
- The non-goals you inferred (PM may want to pull some back in)
- The open questions you surfaced (who owns each one)
- Any requirements you flagged as high-complexity or risky

Don't present the spec as final — present it as a working draft for PM's corrections.

### Step 6 — Create the artifact

Once PM approves, ask where they'd like to save it — or offer to paste the full spec as text they can copy into their preferred tool (doc, Notion, Confluence, etc.).

**If PM is using GitHub Issues**: use `draft-issue` to file each requirement chunk as an issue after the spec is approved.

**Format**: Markdown is the default — it pastes cleanly into most tools and can become issues directly.

---

## Anti-patterns to avoid

| Don't | Why | Instead |
|---|---|---|
| Write requirements as implementation steps | Locks engineers into a solution before they've seen the problem | Write observable behaviors ("user can do X") not methods ("system calls Y API") |
| Skip non-goals | Scope creep happens in the silence | Every obvious adjacent feature gets a ❌ in Non-goals |
| Leave open questions out | Engineers will guess wrong | Surface every unresolved question with an owner |
| Write TL;DR first | You don't know what you've decided yet | Write it last |
| Use vague success criteria ("users feel better") | Can't be verified | Binary, observable, ideally measurable |
| Pad requirements to look thorough | Noise drowns signal | 5 sharp requirements beat 15 vague ones |
| Write a spec for something that needs a 5-minute fix | Over-engineering | Use `draft-issue` directly for simple, well-understood work |

---

## Quality checklist

Before showing the spec to PM:
- [ ] SLUG and title are clear without reading the body
- [ ] TL;DR was written last and is accurate to the full spec
- [ ] Non-goals section has at least 2 items (if empty, you haven't thought hard enough)
- [ ] Open questions section surfaces real unknowns (not rhetorical)
- [ ] Every requirement is testable (binary pass/fail)
- [ ] Success criteria are observable without user research
- [ ] Out-of-scope section captures anything that came up and was parked

---

## Example

**Input** (from conversation):
> "We should have a way for Piper to send me a weekly digest — like a summary of what happened in my product that week. GitHub activity, maybe calendar if it's connected. Something I can read Monday morning."

> **Note**: this example is drawn from Piper's own product development. Product-specific references (feature names, internal roles) are Piper's — substitute your product's equivalents when using this skill.

**SLUG**: `WEEKLY-DIGEST`

**Draft spec**:

```markdown
# WEEKLY-DIGEST — Weekly product digest delivered Monday morning

**Status**: DRAFT
**Author**: xian
**Created**: 2026-06-15
**Milestone**: Fast Follow
**Related issues**: None yet

---

## TL;DR

A Monday-morning digest that surfaces the prior week's product activity — GitHub commits and closed issues, upcoming calendar items, and any Piper insights that accumulated. PM reads it in 2 minutes and knows where they stand without hunting through GitHub or calendar manually.

---

## Problem

### Who has this problem?
PMs who are context-switching between projects or coming back after weekend/holiday and need a quick re-orientation to what happened and what's coming.

### What happens today?
PM manually checks GitHub notifications, scans their calendar, and reviews Piper conversation history. There's no summary surface — it requires 10–15 minutes of active hunting each Monday.

### Why does it matter?
Monday context-switching is a high-friction moment. A well-timed digest means PM can make a pull request review decision or flag a stalled issue before their first meeting.

### Why now?
GitHub connector is being wired in Wave 1 (meet-piper + connect-piper). Once that's in place, the digest has its data source.

---

## Goals

### Primary goal
PM receives a concise Monday digest that covers GitHub + Calendar activity for the prior week without manual hunting.

### Secondary goals
- Establishes a touchpoint for Piper to proactively surface insights (Trust Gradient stage-gate)
- Creates a natural re-engagement hook for PMs who aren't using Piper daily

---

## Non-goals

- ❌ Real-time notifications or alerts (separate feature; delivery mechanism is different)
- ❌ Customizable digest templates or frequency (start with opinionated defaults)
- ❌ Integrations beyond GitHub and Calendar in v1 (Notion, Slack, Linear are follow-on)
- ❌ Digest archive or search (v1 is delivery only; no UI surface)

---

## User stories

1. As a PM, I want to receive a Monday digest in my Claude conversation, so that I can orient to the week without manually checking GitHub and Calendar.
2. As a PM, I want the digest to include closed issues and merged PRs from the past week, so that I know what shipped without reading every notification.
3. As a PM, I want the digest to include upcoming calendar events for the week, so that I can see what's on my plate alongside what shipped.

---

## Requirements

### Digest generation
- [ ] Piper generates a digest covering the 7-day window ending Sunday 11:59pm
- [ ] GitHub section: closed issues, merged PRs, new issues opened — grouped by repo
- [ ] Calendar section: events for the coming week (Mon–Sun), filtered to work calendars
- [ ] Insights section: any Piper insights that emerged in the prior week (if assistant has sufficient session context)

### Delivery
- [ ] Digest is delivered as a Piper message (in conversation, not email — v1)
- [ ] PM can trigger it manually ("send me my weekly digest") or it fires automatically Monday morning if a cron mechanism is available
- [ ] If a connector (GitHub, Calendar) is not wired, that section is omitted with a note ("Connect GitHub to include activity — run meet-piper to set up")

### Edge cases and error handling
- [ ] If no GitHub activity in the past week, say so rather than omitting the section
- [ ] If calendar integration is unavailable, omit gracefully with connector-setup note

---

## Design notes

None yet. Digest is text-only in v1 — no UI surface, no email template. Format: markdown sections with headers, brief bulleted lists, total <300 words.

---

## Technical notes

- Depends on: GitHub connector (meet-piper Wave 1), Calendar connector (meet-piper Wave 1 if wired)
- Data fetch: same enrichment layer as consult-piper, called on a Monday cron or user trigger
- Piper insights: read from session history and stored PM profile — included when enough context exists

---

## Open questions

| Question | Owner | Needed by |
|---|---|---|
| Is Monday delivery via cron or manual trigger only in v1? | xian | Before kick-off |
| Which calendar provider(s) are in scope for v1 — Google only, or also Outlook? | xian | Before kick-off |
| Does the digest go into the main conversation thread or a dedicated channel? | PM/design lead | Before design |

---

## Success criteria

- [ ] PM can request "send me my weekly digest" and receive a correctly structured digest
- [ ] GitHub section accurately reflects closed issues and merged PRs from the prior 7 days
- [ ] If no connectors are wired, digest gracefully degrades with connector-setup prompts
- [ ] Digest reads in under 2 minutes (length check: ≤300 words)

---

## Out of scope (carry-forward)

- Email delivery — v2; v1 is in-conversation only
- Custom frequency (bi-weekly, daily) — start with weekly; let usage data drive
- Digest archive — no UI surface in v1
```

---

## Changelog

- **v1.0** (2026-06-15): Initial version.
