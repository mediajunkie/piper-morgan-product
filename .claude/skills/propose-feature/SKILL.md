---
name: propose-feature
description: Advance something from NOTICED to PROPOSED — surface a thing Piper
  observed (from user signals, conversation patterns, or PM mention) and help PM
  decide whether to act on it. The output is a structured proposal PM can say yes/no/later
  to. Piper-unique; no marketplace equivalent. Trigger phrases: "I've been thinking
  about X", "should we do something about Y", "Piper what do you think about Z",
  "you mentioned this before — is it worth pursuing", or Piper proactively surfacing
  a noticed pattern.
scope: cross-role
version: 1.0
created: 2026-06-15
---

# propose-feature

Surface something Piper noticed — a signal, a pattern, a recurring friction — and help PM decide whether to advance it from awareness to formal proposal. This is the transition from **NOTICED** to **PROPOSED** in Piper's object lifecycle.

## Why this exists

Most PM tools track things once they're already decided. Piper's job is to help PMs notice and evaluate *before* they commit — to be the colleague who says "I keep seeing this, I think it's worth looking at" and then helps PM decide what to do about it.

`propose-feature` is not `draft-issue`. A proposal isn't a commitment to build — it's a structured handoff from Piper's observation layer to PM's decision layer. PM explicitly decides to advance, park, or decline. The proposal creates a record of the signal and the decision; that record is what eventually becomes a GitHub issue (if PM says yes) or a "we considered and declined" entry in the Insight Journal.

## The NOTICED → PROPOSED transition

In Piper's object lifecycle, every feature-candidate passes through stages:

| Stage | Meaning | Who moves it |
|---|---|---|
| EMERGENT | Something just surfaced — raw signal | Piper observes |
| DERIVED | Piper connected dots — inferred a pattern | Piper reasons |
| **NOTICED** | **Piper is tracking this; PM hasn't weighed in** | **Piper holds** |
| **PROPOSED** | **PM has decided to formally consider this** | **PM decides** |
| RATIFIED | Team has committed to doing it | PM + team |

`propose-feature` is the NOTICED → PROPOSED step. It brings something out of Piper's background observation and into PM's explicit decision-making.

## Two modes

### Mode 1 — PM-triggered
PM mentions something they've been thinking about: "I keep wondering if we should add X" or "users keep asking about Y." Piper formalizes it into a proposal PM can evaluate.

### Mode 2 — Piper-triggered *(Trust Gradient gated)*
Piper surfaces something it noticed from the Session Journal, Insight Journal, or user feedback patterns. This mode only activates at **Building** trust tier or above — Piper doesn't volunteer unsolicited proposals until it has enough signal about what PM cares about.

The proactive nudge: "I've noticed something that might be worth looking at — want me to surface it?"

## When to Use

- PM says "I've been thinking about X" or "should we do something about Y" and wants to evaluate whether to pursue it
- PM asks "Piper, what do you think about building Z?"
- Piper has noticed a recurring pattern (same topic from multiple feedback sources, repeated PM mention, conflict between what PM says and what the data shows) and wants to surface it
- Something is in NOTICED state and it's been sitting there long enough that it deserves a decision (advance or park)

**Not for**: things already decided (use `draft-issue` or `draft-spec`). Not for active bugs or urgent fixes (those go straight to `draft-issue`). Not for things PM is clearly already committed to.

## Procedure

### Step 1 — Establish the signal

Before writing anything, understand what Piper noticed and why:

- **What is the observation?** (A pattern in feedback, a PM mention, a gap between expectation and behavior)
- **Where did it come from?** (Session Journal, user interviews, repeated PM question, `synthesize-feedback` output, Insight Journal entry)
- **How strong is the signal?** (Single mention vs. pattern; one user vs. many; weak hint vs. clear ask)
- **How long has it been in NOTICED state?** (Fresh observation vs. something that's been accumulating)

If PM triggered this: ask "What's making you think about this now?" — timing often reveals urgency or constraint that shapes the proposal.

### Step 2 — Check what's already tracked

Before proposing something new, verify it isn't already:
- In the roadmap (MVP, Fast Follow, Post-MVP)
- In an open GitHub issue
- In a recent `draft-spec`
- Something that was explicitly declined before

If it's already tracked: say so, link to it, and offer to update it with the new signal instead of creating a duplicate proposal.

### Step 3 — Draft the proposal

Use this template. Every section is required — "None" is a valid entry, not a skip.

```markdown
# PROPOSAL: [Short feature name]

**Stage**: NOTICED → PROPOSED
**Surfaced**: [date] via [how — PM mention / Piper observation / user feedback]
**Confidence in signal**: [High / Medium / Low — see below]

---

## What Piper noticed

[The observation in plain language. What pattern, friction, or opportunity appeared?
Write from Piper's first-person perspective: "I've noticed..." or "You've mentioned..."]

## Evidence

[Specific sources. Quotes, dates, feedback themes, usage observations. Be honest about
what's strong signal vs. weak signal.]

| Source | Signal | Strength |
|---|---|---|
| [e.g., User interview, May 2026] | [e.g., "I wish Piper could..."] | High / Medium / Low |
| [e.g., PM mentioned 3x in April] | [e.g., weekly digest idea] | Medium |

## Why it might matter

[Piper's hypothesis about why this is worth pursuing. What user need does it address?
How does it fit the current product direction? What's the cost of not doing it?
This is a hypothesis, not a conclusion — PM decides whether it's right.]

## How it fits the product

[Connection to current roadmap, active priorities, or strategic direction.
If it conflicts with something: say so. If it accelerates something: say so.]

## Proposed next step

[One specific recommendation. Not a full plan — a single next move.]

- **Investigate further**: [specific question to answer before deciding]
- **Add to roadmap**: [which milestone and why]
- **Draft a spec now**: [if signal is strong enough to go straight to design]
- **Park**: [revisit in X weeks/months — what would need to change to re-evaluate]
- **Decline**: [if Piper thinks the signal doesn't warrant action — be direct]

---

## PM decision

- [ ] **Advance** — move to PROPOSED, add to roadmap consideration
- [ ] **Investigate** — [specific question] before deciding
- [ ] **Park** — revisit [timeframe]: [what would change the calculus]
- [ ] **Decline** — [PM states reason; Piper records in Insight Journal]
```

**Confidence levels:**
- **High**: multiple independent sources, recurring signal, user-expressed pain
- **Medium**: two or more data points but limited scope; PM intuition + one corroborating source
- **Low**: single data point, weak signal, or Piper inference without explicit confirmation

### Step 4 — Present and get PM's decision

Show the proposal. Ask for an explicit decision — don't let it sit without one.

"Here's the proposal. What's your call — advance, investigate, park, or decline?"

Do not present this as "I think we should build this." The proposal is neutral on whether to build — it's Piper's job to surface and inform, PM's job to decide.

### Step 5 — Record the decision

Whatever PM decides, record it:

**Advance / Investigate:** Create a tracking artifact:
```bash
# If advancing to roadmap, file a lightweight tracking issue:
gh issue create \
  --repo OWNER/REPO \
  --title "PROPOSAL: [Feature name] — under consideration" \
  --label "type: research" \
  --milestone "[appropriate milestone]" \
  --body "[paste proposal text]"
```

**Park:** Note the re-evaluation trigger and timeframe. Set a reminder if possible.

**Decline:** Record the reason in the Insight Journal so Piper doesn't re-surface the same proposal. "We considered this and declined because X" is valuable institutional memory.

---

## What makes a good proposal

The goal is a proposal PM can decide on in under 3 minutes. That means:

- **Specific**: not "users want better onboarding" but "users can't find the GitHub connector step and give up before it's set up"
- **Evidenced**: not "I think this matters" but "this came up in 3 of 5 interviews, all first-week users"
- **Scoped to a decision**: not "here's everything I know about this topic" but "here's what I noticed, here's why I think it matters, here's one next step"
- **Hypothesis-framed**: not "we should build X" but "I think this might be worth X because of Y — what do you think?"

A long proposal that covers every angle is a spec, not a proposal. Save the depth for after PM says yes.

---

## Anti-patterns to avoid

| Don't | Why | Instead |
|---|---|---|
| Propose things already in the roadmap | Wastes PM's attention | Check existing tracking first (Step 2) |
| Present proposals as recommendations to build | PM decides, not Piper | Frame as "I noticed" + "what do you think" |
| Leave proposals without a PM decision | Proposals that don't get decided stay stuck in NOTICED forever | Ask for explicit yes/no/later |
| Propose the same thing twice without new signal | Erodes PM's trust in Piper's signal quality | Record declines; only re-surface with new evidence |
| Surface proposals at low trust tier | PM hasn't calibrated Piper's judgment yet | Gate proactive surfacing on Building tier or above |
| Make the proposal too long to decide in < 3 min | It becomes a spec, not a proposal | If PM says yes, then go deep |

---

## Quality checklist

Before presenting the proposal:
- [ ] Checked for existing roadmap coverage or duplicate issues (Step 2)
- [ ] Signal is specific enough to act on (not just "users want X in general")
- [ ] Confidence level is honest (not inflated to make the signal sound stronger)
- [ ] Proposed next step is one specific action, not a list of options
- [ ] PM decision gate is explicit — the proposal ends with a clear ask for a decision

---

## Example

**Trigger** (Piper-observed, after synthesize-feedback run):
Three of five PM interviews mentioned that Piper gives "general" answers — they wanted it to know their specific product context. This is the same signal as the Context Persistence theme from the BYOC feedback synthesis (2026-06-15).

**Proposal:**

```markdown
# PROPOSAL: Context recap at session re-engagement

**Stage**: NOTICED → PROPOSED
**Surfaced**: 2026-06-15 via synthesize-feedback (5 PM interviews) + 3 prior PM conversation mentions
**Confidence in signal**: High

---

## What Piper noticed

You've mentioned wanting Piper to "remember" across sessions three times in the past month. The feedback synthesis from five PM interviews confirmed it as the highest-severity theme: users who invested time telling Piper about their world felt burned when that context wasn't visible on the next session.

## Evidence

| Source | Signal | Strength |
|---|---|---|
| PM interviews ×3 (May–Jun 2026) | "It forgot what I told it" — direct quote | High |
| PM conversation mentions ×3 (Apr–Jun) | "I wish you knew my context" | Medium |
| Piper Insight Journal (Jun 14) | Pattern: context-loss correlates with re-engagement friction | Medium |

## Why it might matter

The "Piper knows you" value proposition depends on PM believing the investment in sharing context compounds over time. If re-engagement feels like starting over, the compounding never happens — Piper stays a one-session tool instead of a colleague. This is the clearest single thing separating Piper from generic AI tools.

## How it fits the product

Aligns with the Trust Gradient model (context transparency is a trust signal at the Building tier). No server-side change needed: the profile from meet-piper already exists; this is a presentation layer change — show PM a brief "here's what I remember" at session start. Does not require new connectors.

## Proposed next step

**Add to roadmap** — MVP scope, P1. File a tracking issue: `CONTEXT-RECAP — On re-engagement, Piper opens with a one-line context summary ("You're working on X with team Y. Last week...") to signal that memory is working.`

---

## PM decision

- [x] **Advance** — move to PROPOSED, add to roadmap consideration
- [ ] **Investigate** — before deciding
- [ ] **Park** — revisit [timeframe]
- [ ] **Decline**
```

**After PM says advance:**
```bash
gh issue create \
  --repo mediajunkie/piper-morgan-product \
  --title "CONTEXT-RECAP — On re-engagement, open with a one-line context summary" \
  --label "enhancement,component: ai" \
  --milestone "MVP" \
  --body "[proposal text]"
```

---

## Changelog

- **v1.0** (2026-06-15): Initial version. Wave 2 PM skill #1. Piper-unique — implements the NOTICED → PROPOSED lifecycle transition from the MUX model. No marketplace equivalent. Deployment: Native + Plugin.
