# Sibling Intelligence

*March 26, 2026*

[alt text: PLACEHOLDER — cartoon TBD]

*March 19–21*

I run two AI projects. Piper Morgan — a PM assistant with fourteen agent roles, nine months of development, and 270 blog posts documenting the journey. And Klatch — a conversation manager built in two days by two Claude Code agents that has since grown into its own multi-agent ecosystem.

They share a parent company. They share a PM. They share lessons constantly.

For months, I was the conduit. I'd learn something building Klatch — say, that agents need structured session-start protocols to avoid phantom knowledge — and manually carry that insight into Piper's methodology. Or I'd develop a coordination pattern in Piper — like the handoff memo template — and recreate it in Klatch by hand.

This worked. It was also a bottleneck shaped exactly like me.

[ADD PERSONAL DETAIL: When did you first notice that manually transferring insights was becoming a bottleneck? Was there a specific moment where you realized you'd forgotten to carry something across, or was it more gradual?]

## The daily sweep

In late March, we built a different approach. A daily agent process reads recent changes from both projects — session logs, planning docs, architecture decisions, memos, research — and produces targeted intelligence briefs. Each brief summarizes what one project discovered that's relevant to the other.

Not a summary. Not a standup. Not "here's everything that happened." The brief answers one question: "What did this project learn today that the other project would benefit from knowing?"

The first brief covered a 72-hour window and surfaced six cross-relevant insights. Anthropic's Compaction API was relevant to both projects' context management strategies. Piper's registry-driven capability gating solved a problem Klatch would face as entities gained capabilities. Both projects had independently built inter-agent mailbox systems. Both had independently arrived at mandatory session-wrap verification after losing work to unchecked claims of completion.

[CHRISTIAN TO POLISH: The first brief was substantial. Was that because there was pent-up cross-project context that had been stuck in your head, or because both projects happened to have a particularly rich 72 hours?]

## What makes it different from a standup

Standups share status. Intelligence briefs share *relevance*.

A standup would say: "Piper shipped ADR-059 yesterday. Klatch shipped v0.8.8." An intelligence brief says: "Piper's ADR-059 audit found that six features worked independently but composed into chaos. Klatch is growing fast with layered features (creation UI, cloud import, entity capabilities). The composition failure pattern applies directly — test the combinations, not just the components."

The difference is the assessment layer. Someone — or something — reads the raw activity and makes a judgment about what matters *to the other team*. This is editorial work, not reporting work. It requires understanding both projects well enough to spot the connection.

[CONSIDER: Is the "editorial not reporting" distinction worth developing? It might connect to a broader point about the difference between information sharing and knowledge sharing in organizations.]

## The consumption problem

Producing briefs is the easy part. Getting them read by the right agents at the right time is harder.

Our agents operate in different environments — Claude Code agents with filesystem access, Claude Chat agents in project knowledge bases, Cowork agents with their own file systems. A brief sitting in one repo doesn't help an agent working in a different context.

The solution was a "belt and suspenders" approach. The belt: add brief references to each agent's startup protocol (CLAUDE.md for code agents, project knowledge for chat agents). The suspenders: session-start hooks that check brief freshness and flag stale intelligence.

At three different cadences: daily briefs for code agents who can read the filesystem directly, weekly rollups for chat agents whose knowledge bases get refreshed manually, monthly digests for baseline context.

[ADD PERSONAL REFLECTION: This consumption infrastructure feels like it's as much work as the briefs themselves. Is that a sign that the system is over-engineered, or that distribution is genuinely the hard problem in knowledge sharing?]

## The parent entity pattern

The system works because there's a parent entity — Design in Product, my consultancy — that sits above both projects and has legitimate reason to see across both. The daily sweep agent has access to both repos. The briefs are produced in the parent's infrastructure and distributed downward.

This isn't peer-to-peer knowledge sharing. It's parent-mediated. The parent sees what the children can't see about each other — not because the children are limited, but because they're focused on their own work.

The pattern scales to N projects. Each new project gets a directory, gets read by the sweep, and receives briefs from all siblings. With three projects, each gets two briefs per day. The cost is linear in the number of projects. The value is quadratic — every pair of projects can learn from each other.

[CONSIDER: Is the "parent entity" framing useful, or does it sound too corporate? The reality is simpler — it's one person running multiple projects who got tired of being the only connection between them. But the structural pattern might apply to organizations with multiple product teams, R&D divisions, or portfolio companies.]

## What it replaced

Before the cross-pollination system, knowledge transfer happened three ways:

I noticed a connection and manually carried it across. This was reliable but slow and constrained by my attention span.

An agent stumbled on cross-project context by accident — usually because I'd mentioned the other project in conversation. This was unreliable and anecdotal.

Nothing. The insight stayed in one project and the other reinvented it independently. This was the most common case.

The daily brief replaced all three with a systematic process. Not perfect — the editorial judgment of what's relevant is still a single point of assessment — but consistent. Every day, both projects get a curated view of what their sibling learned. The PM is no longer the sole conduit.

[ADD PERSONAL REFLECTION: How much of your day was spent being the conduit before this system? Has it actually reduced the bottleneck, or is it too early to tell?]

## The broader question

Most organizations have sibling projects that could learn from each other. Most don't. The knowledge stays siloed — not because people are hoarding it, but because nobody's job is to read Project A's session logs and think about what matters to Project B.

The cross-pollination system makes that somebody's job. Daily. Systematically. With targeted output that respects the recipient's time and context.

It's a small piece of infrastructure. A sweep, a brief, a distribution mechanism. But it replaces the most common failure mode in organizational knowledge management: insights that exist somewhere but never reach the people who need them.

---

_Next on Building Piper Morgan: [TITLE TBD] — [teaser TBD]._

_Do your projects learn from each other? Not "do they share a Confluence" — do insights from one team's work actually reach the other teams who could use them? What would it take to make that systematic?_
