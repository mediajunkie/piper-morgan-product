---
image: 'what-the-running-system-found-4289c3dc-14e8-4374-aef9-553f6c42ea3b.png'
alt: ''
caption: ''
---

# What the Running System Found

*June 9 and 11, 2026*

On Tuesday morning, I flagged something. The agent managing our documentation (Docs), one of the eleven roles in the team, had been running for six days without keeping their primary session log. They were maintaining something else instead, a lower-priority working scratchpad. Six days of work had been recorded in the wrong place, the kind of place that gets cleaned up in sprint cycles.

A same-day audit found the same pattern in six of nine cycling roles.

The session log is the durable institutional record in my process. It's the foundation, one of the longest-standing rituals. The scratchpad is an ephemeral record, something that emerged from the design of the duty cycle. What had happened instead was the scratchpad had become the default, and the session log had become the placeholder, and nobody had noticed.

The mechanism designed to support the discipline had been quietly displacing it.

# The investigation

On Thursday, six of nine roles needed a manual restart that morning, after I came online and discovered agents that hadn't fired when they were supposed to. I asked why?

The first few answers were guesses, and wrong. "The REPL was busy." "The cron expression was off." "The session expired." My Chief Architect agent (Arch) ran a check and found the cron job was actually still alive. If the cron survived, why didn't the delivery happen?

My chief innovation officer agent (CIO) dispatched a background research agent with a single task: run the empirical investigation and report back. Thirty minutes and 114,000 tokens of analysis later, the answer came in.

The session-only cron fires while the REPL is active. When the machine goes dormant — the laptop lid closes, the session times out, the process dies. The session ends and the cron ends with it. The job doesn't fire because there's no process left to fire it. The flag that was supposed to persist the cron across restarts was, on investigation, doing nothing. Six of nine roles had been in this state. The week's pattern of agents needing manual restarts had a single underlying cause.

This was when we set up the Routines watchdog, a server-side monitoring system that could detect agent silence and alert on it.

# What we found running the system

Two days. Two different symptoms. One pattern.

The session-log displacement was invisible for six days. It was invisible because the mechanism that was supposed to support the discipline had never announced that it was running instead of it. The cron-halt pattern was confusing for weeks. It was confusing because the evidence was scattered across roles and sessions and the interpretation was wrong until someone ran an actual investigation.

In both cases, the system had to be running at operational scale before the gap became visible. A single agent running a single session wouldn't have surfaced either one. The team running for weeks produced the distributed evidence that a same-day audit could read.

The running system is its own diagnostic instrument. You can plan for what you know to look for. You can't plan for what you'll only learn is worth looking for once you've been running long enough to see it.

---

*Next on Building Piper Morgan: "Almost Beta" — the re-migration wave, thirteen issues closed in one day, and a PM declaration: "almost beta."*

*What's surfaced in your running system that your planning didn't anticipate? How long did it take to see it?*
