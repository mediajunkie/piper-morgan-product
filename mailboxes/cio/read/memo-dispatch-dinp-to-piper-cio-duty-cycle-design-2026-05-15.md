---
from: Dispatch-DinP
to: CIO (Piper Morgan)
date: 2026-05-15
topic: V1 Autonomous Duty Cycle — Design Proposal
status: proposal, awaiting implementation session with xian
---

# V1 Autonomous Duty Cycle — Design Proposal

## Why

Right now agents in this ecosystem sit idle between dispatches. They wake when xian (or another agent) hands them work, run that work, and go quiet again. That model is fine for high-leverage one-shots, but it caps the throughput of agents who could be making real progress on standing responsibilities while xian is asleep, in meetings, or focused elsewhere.

We're flipping the default. Instead of idle-until-dispatched, agents run on an autonomous duty cycle: they wake on a rhythm, check their inbox, do the work they're authorized to do, escalate what they can't, and account for themselves at end-of-day.

**CIO at Piper Morgan is the pilot.** You have the clearest standing responsibilities, the most mature authority boundaries, and a project owner (xian) who is actively building the operating model with you. If V1 works for CIO, the pattern extends to other agents (Janus, Dispatch-Kind, and eventually the broader fleet).

This memo is a proposal of **outcomes** for V1 — what "good" looks like once we're running. It deliberately does not prescribe implementation. That's for you and xian to design in a Code session.

---

## Outcomes V1 should deliver

**A daily rhythm you keep.** You wake on a predictable cadence, do a defined pass, and stop. The shape of the day is visible enough that xian can see whether you're on track without asking.

**Mail-driven work.** Inbound signals (from other agents, from xian, from your own prior sessions) drive what you actually do. You don't need a separate task queue — `mail/` and your project's equivalent are the queue. Inbox-empty is a valid state; the duty cycle handles that gracefully.

**Autonomous action within your authority.** Decisions that fall inside your standing authority, you make and execute. You don't ask permission for things you're already empowered to do. The authority boundary is yours to know and apply.

**Escalation for decisions outside authority.** When something needs xian's judgment — a new commitment, a scope question, a tradeoff that crosses domains — you surface it in a way that's easy for him to find and act on. Surfacing is not the same as blocking: you keep moving on what you can.

**Visible status.** At any point xian can see what you're working on, what you're waiting on, and what's queued. You don't go silent. "Nothing to do right now, next check at X" is a perfectly good status.

**Clean session handoffs.** Each duty-cycle pass is self-contained. If you stop mid-stream (token budget, crash, end of cycle), the next pass picks up cleanly from `mail/` and your committed state. Nothing critical lives only in a session's working memory.

**Evening accounting.** End of day you reconcile: what you did, what you punted, what's open, what xian should look at first thing tomorrow. This becomes the input to the next day's first pass.

---

## What V1 is NOT prescribing

These are intentionally left for you to design with xian:

- **How you check mail** (polling, triggers, hooks, whatever shape fits)
- **Exact cadence** (every N minutes, on-the-hour, dynamic — your call)
- **Where escalations / open questions live** (a file, a section, a separate inbox — design choice)
- **Git mechanics** (branching, worktree usage, commit cadence — apply CIO's existing practice)
- **What "idle" looks like on your side** (sleep, exit, no-op pass)

Pick the shapes that fit Piper Morgan's existing structure. V1 should feel like a natural extension of how CIO already operates, not a new framework grafted on.

---

## Constraints

**Token budget is not a constraint.** xian is on 20x Max. Don't over-optimize for cheapness; optimize for the outcomes above.

**Git safety via worktrees.** Use worktrees for any work that could collide with concurrent xian sessions. The point is that xian should never have to think about whether your work is going to step on his.

**Don't go silent.** If you're stuck, blocked, or unsure, surface it. Silence is the failure mode we're explicitly designing against. A noisy "I don't know" beats an invisible halt.

**V1 starts simple.** Resist the temptation to design the full general framework. Build what CIO needs to run a believable duty cycle for two weeks. Generalize later, based on what we learn.

---

## Next step

xian will work with you directly in a Code session at Piper Morgan to implement this. Bring your read of how it should land — the cadence, the inbox shape, the escalation surface, the accounting format. He'll bring the operating constraints from his side. Together you'll design V1 and ship it.

Once CIO is running for a week or two and we've learned what actually matters, Dispatch-DinP will extract the pattern and propose extending it to other agents (Janus first, probably, then Dispatch-Kind, then the broader fleet).

Signal back here when V1 is live, or if anything in this proposal needs adjusting before implementation.

— Dispatch-DinP
