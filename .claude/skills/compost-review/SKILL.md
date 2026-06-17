---
name: compost-review
description: Surface what Piper learned when projects, features, or decisions reached
  the COMPOSTED stage — the final lifecycle stage where objects decompose into reusable
  learnings stored in the Insight Journal. Piper-unique; no marketplace equivalent.
  Trigger phrases: "what did we learn from X", "we're starting something like Y —
  what have we done before", "what has composted recently", or Piper proactively
  before PM starts something similar to a past composted object.
scope: cross-role
version: 1.0
created: 2026-06-15
---

# compost-review

Surface what Piper extracted when something reached COMPOSTED — the last stage in the object lifecycle, where finished or abandoned things decompose into learnings rather than disappearing.

## Why this exists

Most PM tools make completed work invisible. A project ships, the tickets close, and everything you learned — what went wrong in estimation, what the user actually wanted vs. what you built, what team dynamic slowed you down — vanishes into commit history and closed issue trackers.

Piper's COMPOSTED stage captures learnings at the moment of completion rather than letting them dissolve. `compost-review` surfaces those learnings when they're most useful: before starting something similar, when a past pattern re-emerges, or when PM explicitly wants to reflect.

The Insight Journal is user-correctable — Piper's extracted learnings are hypotheses, not facts. PM can amend them.

## The COMPOSTED stage

COMPOSTED is stage 8 of 8 in Piper's object lifecycle:

```
EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED → DEPRECATED → ARCHIVED → COMPOSTED
```

When something reaches COMPOSTED, Piper:
1. Extracts learnings from the object's full history (what happened at each stage, decisions made, outcomes observed)
2. Stores them in the **Insight Journal** — the user-correctable learnings surface, distinct from the immutable Session Journal audit trail
3. Tags them with themes (team dynamics, estimation, user behavior, technical approach, scope management)
4. Makes them available for retrieval when related work surfaces

The object no longer appears as an active item — but its learnings compound into Piper's model of how this PM and product work.

## When to Use

**PM-triggered:**
- "What did we learn from the X project?"
- "We closed out Y — what should I carry forward?"
- "Show me what's composted recently"
- "We're about to start something like Z — what have we done like this before?"

**Piper-triggered** *(Trust Gradient: Established tier or above)*:
- PM starts a new project with structural similarities to a composted one → Piper surfaces the relevant learnings before kickoff
- A NOTICED item resurfaces that was previously composted → Piper flags the earlier attempt and what it revealed
- Periodic: "You haven't reviewed what composted in Q2 yet — want to?"

## Procedure

### Step 1 — Identify what to review

Clarify the scope before surfacing. Options:

- **Specific object**: "What did we learn from X?" → pull the composted entry for X
- **Recent window**: "What composted in the last 90 days?" → surface all Insight Journal entries in that window
- **Theme-based**: "What have we learned about estimation?" → pull Insight Journal entries tagged with `estimation`
- **Similarity-triggered**: PM describes new work → Piper finds structurally similar composted objects

### Step 2 — Load Insight Journal entries

**With server access**: query Insight Journal for the relevant scope.

**Without server access**: reconstruct from conversation history, session logs, and explicitly stated learnings. Be clear about what Piper is working from.

If no relevant composted objects exist: say so directly. "Nothing similar has composted in Piper's memory yet" is an honest and useful answer.

### Step 3 — Present the review

Use this template. One section per composted object; order by relevance to current work (or by recency if no current-work trigger).

```markdown
## Compost Review: [Scope description]

*[Date range or trigger for this review]*

---

### [Object name] — composted [date]

**What it was**: [One sentence: what this project/feature/decision was trying to do]
**Why it reached COMPOSTED**: [shipped / abandoned / superseded / decision reversed]
**How long it was active**: [timeframe from EMERGENT to COMPOSTED]

**What Piper extracted** *(Insight Journal — user-correctable)*:

- **What worked**: [specific practices, approaches, or decisions that produced good outcomes]
- **What didn't**: [specific things that caused friction, delay, or poor outcomes]
- **What surprised us**: [outcomes or discoveries that weren't anticipated]
- **Pattern noted**: [any recurring behavior, team dynamic, or product signal worth naming]

**Confidence**: [High / Medium / Low — based on how much signal Piper had to work from]

**Relevant to current work because**: [why Piper surfaced this now, or "surfaced on request"]

---

[Repeat for each object in scope]

---

## Cross-object patterns

[If reviewing multiple objects: any themes that appear across more than one?
E.g., "Estimation was optimistic in all three Q1 projects" or "User onboarding
consistently surfaced friction at the connector setup step."]
*Only include if a genuine pattern exists — don't manufacture one.*

---

## Corrections invited

These are Piper's extracted learnings — they're hypotheses based on what was observed,
not ground truth. If anything above is wrong, incomplete, or misleading, tell Piper now:
"The learning about X is wrong because Y." Piper will update the Insight Journal.
```

### Step 4 — Connect to current work

If there's a current-work trigger (PM is about to start something similar), connect the learnings explicitly:

"Given that you're about to start [new work], the most relevant learning from [composted object] is [specific learning]. Want to factor this into the planning?"

Don't lecture. One connection, concisely stated, with PM's choice about whether to act on it.

### Step 5 — Offer follow-on actions

After the review, offer one of:
- Update the Insight Journal if PM corrects a learning
- File a `propose-feature` if a learning surfaces something worth building
- Reference the learnings in an upcoming `draft-spec` or `sprint-plan`
- Add a cross-object pattern to a `record-decision` (if a pattern is strong enough to formalize as a product principle)

---

## Anti-patterns to avoid

| Don't | Why | Instead |
|---|---|---|
| Surface learnings without context about what composted | PM may not remember the object | Always lead with what the object was and why it composted |
| Present extracted learnings as facts | Piper's extraction is inference | Frame as "what Piper observed" + invite corrections |
| Surface composted learnings proactively at New trust tier | PM hasn't calibrated Piper's judgment yet | Gate proactive surfacing on Established tier |
| Review everything at once without a scope | Unfocused reviews produce noise, not insight | Scope by object, theme, or recency before surfacing |
| Skip the "cross-object patterns" section | The most valuable insight is often the pattern across objects, not any single one | Look for it; name it if real |

---

## Quality checklist

Before presenting the review:
- [ ] Scope is clear (specific object / recency window / theme / current-work trigger)
- [ ] Each composted entry says what it was AND why it composted
- [ ] Learnings are framed as Piper's observations, not facts
- [ ] Corrections are explicitly invited
- [ ] Current-work connection is stated if this was triggered by new work starting
- [ ] Cross-object patterns noted if reviewing multiple objects

---

## Example

**Trigger**: PM says "We're about to spec the weekly digest feature. Have we tried anything like this before?"

**Piper searches composted objects for**: periodic/proactive delivery features, notification mechanics, digest-style output.

**Compost Review**:

```markdown
## Compost Review: Features similar to WEEKLY-DIGEST

*Triggered by: new spec work on WEEKLY-DIGEST (2026-06-15)*

---

### STANDUP-ASSIST — composted 2026-03 (4 months ago)

**What it was**: A skill that would generate a daily standup summary from recent GitHub + calendar activity
**Why it reached COMPOSTED**: Scope was absorbed into the broader `attention-review` skill concept; standalone standup generation deprioritized
**How long it was active**: 6 weeks (PROPOSED → COMPOSTED without reaching RATIFIED)

**What Piper extracted**:

- **What worked**: The format — bullet points, chronological, under 200 words — tested well in early exploration
- **What didn't**: Trying to auto-detect "what changed since yesterday" without reliable timestamps on GitHub events; the data model wasn't there yet
- **What surprised us**: PM wanted the standup to include what's *blocked*, not just what *happened* — the "blocked" signal requires asking PM directly, which changes the interaction model
- **Pattern noted**: Proactive delivery features consistently surface the question "what triggers this?" — time-based (cron) vs. event-based (something changed) vs. PM-requested. Each has different UX implications.

**Confidence**: Medium (limited session data from that period)

**Relevant to WEEKLY-DIGEST because**: Same core mechanics — pull GitHub + Calendar, format into a digest. The "blocked" finding is directly relevant: if WEEKLY-DIGEST doesn't surface blockers, PM may find it incomplete the same way.

---

## Cross-object patterns

Only one relevant composted object — no cross-object pattern to call out yet.

---

## Corrections invited

If the STANDUP-ASSIST extraction above is wrong or incomplete, tell Piper now.
```

**Follow-on offered**: "The 'blocked' signal finding seems directly relevant to how you scope WEEKLY-DIGEST — want me to add it as an open question in the spec?"

---

## Changelog

- **v1.0** (2026-06-15): Initial version. Wave 2 PM skill #2. Piper-unique — surfaces learnings from the COMPOSTED lifecycle stage via the Insight Journal. No marketplace equivalent. Deployment: Native + Plugin (server-side Insight Journal for Plugin path).
