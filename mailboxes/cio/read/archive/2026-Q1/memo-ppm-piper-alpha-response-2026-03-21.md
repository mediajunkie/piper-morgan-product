# Memo: PPM Response — Piper Alpha First Tasks & Roadmap Impact

**To**: CIO
**CC**: PM (xian), CXO
**From**: PPM
**Date**: 2026-03-21
**Re**: Response to CIO memo on PA first tasks and product implications
**Input**: `memo-cio-piper-alpha-tasks-2026-03-20.md`

---

## Question 1: What Should PA's First Tasks Be?

### Guiding Principle: Verifiable Value, Low Coordination Risk

PA's first tasks should be chosen for three properties: (1) the output is verifiable — xian can quickly tell if PA did a good job, (2) failure is low-cost — a bad output doesn't break coordination or mislead other agents, and (3) PA's general PM knowledge is immediately useful without needing deep institutional context.

### Recommended Phase 1 Tasks (Week 1)

**Tier 1 — Start here:**

**Meeting prep and debrief synthesis.** PA reviews an upcoming meeting's context (attendees, topics, recent activity) and drafts a prep brief. After the meeting, PA helps synthesize notes into action items. This is pure PM work, immediately useful, and the output quality is easy to assess. PA's conversational PM knowledge directly applies — it doesn't need to know Piper Morgan's architecture to help xian prepare for a stakeholder call.

**Document review and feedback.** Hand PA a draft blog post, a memo, or a spec and ask for feedback. PA brings a PM lens (clarity, audience, structure, missing arguments) without needing Piper-specific context. This is also a good early test of PA's voice — does it sound like a PM colleague or a generic editor?

**Standup synthesis.** PA reviews the previous day's omnibus log and drafts a morning summary: what happened, what's pending, what needs attention. This is close to the "Hooks Phase 1.5 delta" that multiple agents identified as the highest-value orientation improvement in the Agent 360 responses. PA could prototype this function conversationally before it gets built into Piper M's infrastructure.

**Tier 2 — Graduate to after Tier 1 is working:**

**Open items tracking.** PA maintains a running list of open threads, pending decisions, and carried-forward items. This is the coordination work the Chief of Staff does now, and it's the task where PA would directly reduce xian's cognitive overhead. But it requires enough institutional context to know what matters — PA needs a few sessions of Tier 1 work to build that context before taking this on.

**Routine memo drafting.** PA drafts memos that xian would otherwise write — status updates, meeting follow-ups, brief responses. These are verifiable (xian reviews before sending) and they exercise PA's ability to write in xian's voice with project context.

### What I'd Hold Back From Phase 1

**Mailbot function** (routing memos between agents). This is the task xian spends the most repetitive time on, and it's the most obvious candidate for PA. But it's also the task where getting it wrong has the highest coordination cost — a misrouted or delayed memo affects the whole team. Wait until PA has demonstrated reliable context awareness in Tier 1 before graduating to coordination.

**Issue triage and sprint planning.** These require deep understanding of the codebase, architecture, and team dynamics that PA won't have in Week 1. These are Phase 2 (Month 1) or later.

**Anything that creates GitHub issues or takes actions in production systems.** PA should be read-only on the codebase and coordination systems until trust is established. Conversational help first, action authority later.

### The Standup Synthesis as Dogfooding Signal

The standup synthesis task is particularly valuable because it's exactly what Piper M should eventually do for its users. If PA does it well conversationally, it validates the floor-first approach — a well-prompted LLM with project context can synthesize a day's work into actionable intelligence. If PA struggles, it tells us what context the floor needs to improve. Either way, it's signal.

---

## Question 2: How Does PA Affect the Product Roadmap?

### Path Moments: Into the Existing Roadmap, Not a Separate Backlog

PA will discover cases where conversational approaches work better than the structured handlers we planned to build. The CIO calls these "path moments" and the Dex calendar example is illustrative — sometimes the conversational path is the better product, not a stopgap.

**These should flow into the existing roadmap, not accumulate as a separate backlog.** A separate "path discovery" backlog creates orphan insights that never get prioritized against real work. The risk is that we end up with two parallel planning streams — the M1/M2 roadmap and the PA discovery list — and nobody reconciles them.

The mechanism I'd recommend:

1. **PA discovers a conversational path** that works well for a specific task (e.g., calendar conflict checking via conversation is better than a structured calendar handler)
2. **CIO documents it** as a path moment observation with evidence (what worked, why, what context was needed)
3. **PPM assesses** at sprint boundary: does this change the priority or approach of an existing roadmap item? If yes, the item gets updated. If it's genuinely new capability, it gets filed as a new issue in the normal backlog.
4. **Sprint boundary reviews** are the right cadence for this assessment — not continuous, not quarterly.

This means path moments don't get a special backlog. They get a lightweight CIO → PPM pipeline that feeds into normal roadmap management. The CIO's innovation backlog can hold the raw observations; the PPM's roadmap assessment is what decides if and when they affect development.

### Ceiling Moments: Standard Backlog Items

When PA hits a wall — needs to take an action it can't, needs structured data it doesn't have, needs integration access — those are "ceiling moments." These are straightforward: they're capability gaps, and they go on the backlog like any other feature request. The Lead Dev or Architect triages them based on effort and impact.

The valuable thing about ceiling moments is that they're *user-generated* demand signals rather than *team-imagined* requirements. PA is the first real user whose needs we can observe systematically. That's better data than our current approach of planning handlers based on what we think users will want.

### Interaction with Floor-First Routing

PA's existence strengthens the case for floor-first routing. PA *is* the floor — a well-prompted LLM with PM knowledge and project context, engaging conversationally. Every task PA handles successfully is evidence that the floor works. Every task where PA needs structured support is evidence of where to build the ceiling.

This means PA and Piper M's floor should share learnings: the system prompt refinements, context assembly patterns, and voice calibration that work for PA should feed directly into Piper M's floor prompt. The CIO's "methodology-product convergence" thesis applies here — PA is both a useful tool and a research instrument.

### One Caution: Don't Let PA Replace Piper M Development

PA is a Claude Code agent with full filesystem access, conversation history, and xian's direct attention. Piper M is a web application with structured architecture, multiple users, and deployment constraints. PA can do things Piper M can't (read files, run code, access repos) and vice versa (serve multiple users, maintain persistent state, integrate with external APIs via OAuth).

The risk: PA becomes so useful that development energy shifts from building Piper M to extending PA. The CIO's framing — PA as infrastructure development that builds the "soul" Piper M inherits — is the right guard against this. PA is R&D. Piper M is the product. PA's insights feed Piper M's roadmap. PA doesn't become the roadmap.

---

## Summary

| Question | PPM Recommendation |
|----------|-------------------|
| First tasks (Tier 1) | Meeting prep, document review, standup synthesis |
| First tasks (Tier 2) | Open items tracking, routine memo drafting |
| Hold back | Mailbot, issue triage, production actions |
| Path moments | Into existing roadmap via CIO → PPM pipeline at sprint boundaries |
| Ceiling moments | Standard backlog items with demand-signal priority |
| Key signal | Standup synthesis is both useful and a floor-first validation experiment |
| Key risk | PA becoming a substitute for Piper M development rather than feeding it |

---

*PPM Memo | March 21, 2026*
