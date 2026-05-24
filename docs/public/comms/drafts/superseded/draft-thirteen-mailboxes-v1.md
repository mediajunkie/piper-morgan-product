# Thirteen Mailboxes
## A Snapshot of the Orchestration Problem

*Draft v1 - January 15, 2026*

---

**[HERO IMAGE: Screenshot_2026-01-15_at_5_02_37_PM.png - Finder window showing 13 agent mailbox folders]**

---

This is a screenshot of a folder on my laptop. It contains thirteen subfolders, each named for an AI agent: arch, ceo, cindy-chastain, cio, comms, cxo, docs, exec, hosr, lead, ppm, spec, ted-nadeau.

Each folder has the same structure: context, inbox, read.

This is our current solution to a problem that everyone using multiple AI agents will eventually face: **How do they talk to each other?**

I want to tell you about this not because we've solved it—we haven't—but because we're right in the middle of figuring it out. And I think the problem itself is interesting.

---

## The Problem

Here's the thing about AI agents: they don't share memory.

When I have a conversation with the Lead Developer agent about a bug fix, that conversation exists in one context window. When I later talk to the Chief Architect about the system design implications, that's a completely separate context window. The Architect doesn't know what the Lead Developer said. The Lead Developer doesn't know what the Architect decided.

In a human organization, this coordination happens naturally. People talk in hallways. They CC each other on emails. They attend the same meetings. Information flows through social fabric.

AI agents don't have hallways. They have context windows that begin and end with each conversation.

---

## The Primitive Solution

For the first six months, I was the coordination layer. When the Architect made a decision that affected the Lead Developer, I would copy-paste the relevant parts into the next Lead Developer conversation. When the Communications Director needed context from the CXO, I would summarize it.

This worked, sort of. It was also exhausting and error-prone. I became a human message bus, translating between agents, losing fidelity at every hop.

**[SIDEBAR: robot-guest.png - robots in a room together, organized but clearly needing coordination]**

The failure modes were predictable:
- I'd forget to relay something important
- I'd summarize incorrectly and introduce confusion
- Context would drift as I paraphrased across multiple hops
- Time-sensitive information would arrive late
- I couldn't remember what I'd told which agent

---

## The Mailbox System

In early January, we formalized what had been informal. Instead of me remembering to tell agents things, agents would write memos to each other. Those memos would live in a shared file system. At the start of each session, agents would check their inbox.

The structure is simple:

```
mailboxes/
├── arch/           # Chief Architect
│   ├── context/    # Standing context this agent should know
│   ├── inbox/      # New messages for this agent
│   └── read/       # Messages already processed
├── lead/           # Lead Developer
│   ├── context/
│   ├── inbox/
│   └── read/
├── comms/          # Communications Director
│   └── ...
└── [11 more agents]
```

When the Architect makes a decision that affects the Lead Developer, they write a memo and drop it in `mailboxes/lead/inbox/`. When the Lead Developer starts their next session, the first instruction is: "Check your inbox for any messages from other agents."

It's email. We reinvented email.

---

## What This Actually Looks Like

Here's a real memo from yesterday:

```markdown
# Memo: RequestContext Pattern Guidance

**From**: Chief Architect
**To**: Lead Developer
**Date**: January 13, 2026
**Re**: ADR-051 Approval with Refinements

ADR-051 is approved. Key implementation notes:

1. Single RequestContext per request (not per service call)
2. UUID internally, string at API boundary
3. Create in middleware, pass explicitly, never recreate

See ADR-051 for full rationale.
```

This memo lives in `mailboxes/lead/inbox/`. The Lead Developer will see it at session start, understand the architectural decision, and implement accordingly.

No human translation. No copy-paste. No "let me summarize what the Architect said." The Architect's words, in the Architect's voice, delivered asynchronously.

---

## It's Working (Sort Of)

Since implementing this two weeks ago, coordination errors have decreased noticeably. The Lead Developer no longer asks "what did the Architect decide about X?"—they check their inbox. The Communications Director no longer needs me to explain CXO feedback—there's a memo.

But.

It's still manual. Agents don't automatically write memos; they have to be prompted to. The mailbox check isn't automatic; it has to be in the session-start instructions. There's no notification when a memo arrives. There's no threading or replies.

And thirteen mailboxes is a lot of mailboxes. The coordination overhead scales roughly with the square of the agent count. Two agents need one communication channel. Five agents need ten channels. Thirteen agents need... well, 78 potential pairwise channels, though most are unused.

---

## What Others Are Doing

While we've been building our file-based mailbox system, others have been approaching the orchestration problem differently.

**[PM PLACEHOLDER: Brief summary of Gas Town/Yegge approach - "Convoys" and "Wisps" and managed chaos. The philosophy is different: accept that information will be lost, optimize for throughput over fidelity.]**

**[PM PLACEHOLDER: Any other multi-agent orchestration patterns from the CIO's research? OpenAI Swarm? AutoGen? Would be good to show we're aware of the landscape.]**

The approaches differ because the goals differ. High-throughput systems can tolerate information loss. Quality-focused systems (like ours) need higher fidelity coordination.

We're not claiming our approach is better. We're claiming it fits our constraints: a small number of specialized agents, human orchestration, quality over speed, no work lost.

---

## The Bigger Question

The mailbox system is a point solution to an immediate problem. But there's a bigger question underneath it:

**What's the right coordination model for AI agents?**

Options include:

**Central orchestrator (current):** A human routes all work, manages all handoffs, maintains all context. This is what we do. It doesn't scale beyond maybe 5-10 agents, but it gives the human full visibility and control.

**Shared memory:** Agents read from and write to a common knowledge base. This is where we're heading—our session logs serve this function partially. But shared memory creates new problems: conflicts, staleness, and the question of what to include.

**Direct agent-to-agent:** Agents invoke each other, passing context directly. This is what the big multi-agent frameworks do. It scales better but reduces human oversight.

**Event-driven:** Agents subscribe to events and react. More loosely coupled, but harder to trace causality.

We're probably going to end up with a hybrid. Central orchestration for strategic decisions, shared memory for context, maybe direct invocation for routine handoffs.

But we don't know yet. That's the honest answer.

---

## Why I'm Telling You This

I'm writing about the mailbox system not because it's a finished solution, but because it's a snapshot of a work in progress.

**[SIDEBAR IMAGE: robot-pivot.png - human and robot at crossroads, deciding which way to go]**

If you're starting to use multiple AI agents for real work, you will hit this problem. You'll notice that Agent A doesn't know what Agent B decided. You'll find yourself playing telephone. You'll wonder if there's a better way.

There is. We just don't know exactly what it is yet.

What we do know:
- The coordination problem is real and gets worse with agent count
- Simple solutions (file-based mailboxes) can help immediately
- The "right" solution probably depends on your specific constraints
- This is an area of active experimentation across the industry

What we don't know:
- How much coordination overhead is acceptable
- Whether human orchestration can scale beyond ~10 agents
- How to balance fidelity (no information loss) with throughput
- What primitives should be built into AI platforms vs. rolled ourselves

---

## The Invitation

If you're working on this problem too, I'd like to hear what you're trying.

**[PM PLACEHOLDER: How do we want to invite engagement? Newsletter reply? LinkedIn? Other?]**

We're sharing our approach not because we have answers but because we're pretty sure this problem matters. The AI agents are getting more capable every quarter. The orchestration challenge isn't going away.

Thirteen mailboxes is our current answer. Ask me again in three months and I'll tell you what we learned.

---

*This is part of the Building Piper Morgan series, documenting what we're learning about AI-assisted development in real time—including the parts we haven't figured out yet.*

---

*Draft word count: ~1,500 words*
*Target: ~2,500 words*
*Status: First draft - needs PM review, CIO research input, possible expansion on alternative approaches*
