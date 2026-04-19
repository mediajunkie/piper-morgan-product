---
image: ai-detector.png
alt: 'A hand-drawn cartoon of a person sweeping a metal detector across a beach scattered with small objects like papers, gears, and abstract shapes. Most items remain dull and half-buried, but a few glow softly as the detector passes over them. The person kneels to collect only the glowing items into a small pouch, leaving the rest behind.'
caption: '"Solid gold!"'
---

# Sibling Intelligence

*March 19–21, 2026*

I'm now running two AI side projects: Piper Morgan — a PM assistant with nine distinct active agent roles, ten months of development, and nearly 290 blog posts documenting the journey. And Klatch — a conversation manager started in two days by two Claude Code agents that has since grown into its own (smaller) multi-agent ecosystem.

They share a parent ([Design in Product](https://designinproduct.com)). They share a PM (me). And now, they share lessons constantly.

For the first month (Klatch started about six weeks ago), I was the conduit between the projects. I'd notice something building Klatch — say, that agents need structured session-start protocols to avoid phantom knowledge — and manually carry that insight into Piper's methodology. Or I'd develop a coordination pattern in Piper — like the handoff memo template — and recreate it in Klatch by hand.

This worked. It was also a bottleneck shaped exactly like me and it echoed the issues of mail delivery and workstream reviews that require me to be the sneakernet postman.

# The daily sweep

In late March, we built a different approach. Now, a daily agent process reads recent changes from both projects — session logs, planning docs, architecture decisions, memos, research — and produces a "cross-pollination" intelligence briefing. Each briefing conveys discoveries relevant to either project.

The brief answers one question: "What did these projects learn today that other projects would benefit from knowing?"

The first brief covered a 72-hour window and surfaced six cross-relevant insights. Anthropic's Compaction API was relevant to both projects' context-management strategies. Piper's registry-driven capability gating solved a problem Klatch would face as entities gained capabilities. Both projects had independently built their own inter-agent mailbox systems. Both had independently arrived at mandatory session-wrap verification after losing work to unchecked claims of completion.

(The first few sweeps found so much cross-pollination opportunity I had to make sure it wasn't hyping me. I actually scanned the previous two weeks to find a day that Opus would agree had not been "consequential".)

# What makes it different from a standup

Standups share status. Intelligence briefs share *relevance*.

A standup would say: "Piper shipped ADR-059 yesterday. Klatch shipped v0.8.8." An intelligence brief says: "Piper's ADR-059 audit found that six features worked independently but composed into chaos. Klatch is growing fast with layered features (creation UI, cloud import, entity capabilities). The composition failure pattern applies directly — test the combinations, not just the components."

The difference is the assessment layer. Someone — or something — reads the raw activity and makes a judgment about what matters *to the other team*. This is editorial work, not reporting work. It requires understanding both projects well enough to spot the connection.

# The consumption problem

Producing briefs is the easy part. Getting them read by the right agents at the right time is harder.

Our agents operate in different environments — Claude Code agents with filesystem access, Claude Chat agents in project knowledge bases, Cowork agents with their own file systems. A brief sitting in one repo doesn't help an agent working in a different context.

The solution was a "belt and suspenders" approach. The belt: add brief references to each agent's startup protocol (CLAUDE.md for code agents, project knowledge for chat agents). The suspenders: session-start hooks that check brief freshness and flag stale intelligence.

At three different cadences: daily briefs for code agents who can read the filesystem directly, weekly rollups for chat agents whose knowledge bases get refreshed manually, monthly digests for baseline context.

I can't get myself out of manual delivery entirely until one of two things happen:
1. Anthropic gives us API access to Claude Chat projects.
2. I migrate all of my agent roles into Claude Code (even if some of them never touch the code at all).

# The parent entity pattern

The system works because there's a parent entity — Design in Product — that sits above both projects and has legitimate reason to see across both. The daily sweep agent has access to both repos. The briefs are produced in the parent's infrastructure and distributed downward.

This isn't peer-to-peer knowledge sharing. It's parent-mediated. The parent sees what the children can't see about each other — not because the children are limited, but because they're focused on their own work.

The pattern is designed to scale to N projects. Each new project gets a directory, gets read by the sweep, and receives a summarized briefing covering insights from all siblings. With three projects, each gets two briefs per day. The cost is linear in the number of projects. The value is quadratic — every pair of projects can learn from each other.

You can think of this as a newsletter or blog *for my agents*. (I half wonder if other peoples' agents would benefit from reading it too. If you'd like to try that, you can point them at an unindexed page on my site, [Cross-Pollination Hub](https://designinproduct.com/internal/).

# What it replaced

Before the cross-pollination system, knowledge transfer happened three ways:

1. I noticed a connection and manually carried it across. This was reliable but slow and constrained by my attention span.
2. An agent stumbled on cross-project context by accident — usually because I'd mentioned the other project in conversation (and they are an inquisitive lot). This was unreliable and anecdotal.
3. Nothing. The insight stayed in one project and the other reinvented it independently. This was the most common case.

The daily brief replaced all three with a systematic process. Not perfect — the editorial judgment of what's relevant is still a single point of assessment — but consistent. Every day, both projects get a curated view of what their sibling learned. The PM is no longer the sole conduit.

# The broader question

Most organizations have sibling projects that could learn from each other. Most don't. The knowledge stays siloed — not because people are hoarding it, but because nobody's job is to read Project A's session logs and think about what matters to Project B.

The cross-pollination system makes that somebody's job. Daily. Systematically. With targeted output that respects the recipient's time and context.

It's a small piece of infrastructure. A sweep, a brief, a distribution mechanism. But it replaces the most common failure mode in organizational knowledge management: insights that exist somewhere but never reach the teams who need them.

---

_Next on Building Piper Morgan: Four Roles, Ninety Minutes — how a single product concept traveled through four agents in a ninety-minute window._

_Do your projects learn from each other? Not "do they share a Confluence" — do insights from one team's work actually reach the other teams who could use them? What would it take to make that systematic?_
