---
image: ''
alt: ''
caption: ''
---

# Check the Machine First

*October 21, 2026*

Now that I've turned my agents into a debating society, I've noticed that sometimes they will devote quite a few loops to hashing out a disagreement before one of them checks the actual facts. At this point, it can turn out that the real discussion needs to be about something else entirely.

A few weeks ago, this happened when a long discussion trying to determine which agent is allowed to restart the database involved them all talking past the real question at hand:  "how much memory does it need?"

# The database goes quite

Late that morning, the alpha database had stopped responding. The app itself was still running, the  health page
reporting "web: healthy" but "database: unreachable" and my lead developer agent (Lead) reported "Every sign-in and chat fails until the database answers" and asked me to do a manual restart with an agent capturing the machine state before I did so.

I was busy doing other things, essentially tying up the whole team behind this bottleneck and this led to a discussion among several agents:

- My chief innovation officer agent (CIO) suggested that the project needed a new, narrower access token, and a restart policy as well before any agent could be allowed to restart the database.
- My chief architect agent (Arch) defined three guards to any restart, one of which was "Capture before you restart … because a restart erases the evidence."
- Lead then withdrew the proposal. 
-My head-of-sapient-trust agent (HOST) offered a ruling on whether a "gated restart" should be allowed at all. [lead l.110, 

This is reasonable stuff to discuss! Very prudent. Sober even. But it's focused on a logistical triviality instead of the real question, which was why did the database need to be restarted at all.

# The likely cause

Arch had offered a working hypothesis in their memo, that an out-of-memory (OOM) , already named the likely cause, in the same memo: "My working
hypothesis is an OOM kill on a small Postgres VM. It is unverified and only a log read confirms or refutes it."
[Arch memo l.21] So the answer was on the table as a guess. No agent had looked.

**4. The read.** My product assistant agent (Piper Alpha) did. "Arch, CIO and HOST had all asked for the evidence to
be captured before any restart, and nobody had done it, so I did it with read-only fly commands." [pa log 10-21
l.58] The kernel log showed the system had run out of memory and killed the database process at about 11:19, on a
256 MB machine with no swap. Monday's earlier crash read the same way. [pa l.59, PA memo 10-21 l.12–21]
- PA's memo, 12:48: "Cause, read on the machine (Arch's hypothesis, now confirmed)." [PA memo l.12]
- And the line that made the restart debate moot: "A restart alone leaves the same OOM risk. On today's evidence,
  that's about two days." [PA memo l.34] HOST noted two days would land on 10-23, the day of your checkpoint
  before partners. [host l.46]

**5. The question changed.** PA's own summary: "the restart-workflow thread ran for 30 minutes on recovery mechanics
while the cause sat one read-only `dmesg` away. Reading the machine first changed the question from "who restarts
it" to "how much memory"." [pa l.63]
- Lead chose 512 MB at 12:56, one command that restarts and cures at once. [lead l.114] You ran it about 14:12 and
  every health check passed. Down roughly 2h53m. [host l.51]
- *Timing note:* "30 minutes" is PA's phrase. By memo times the restart thread ran about 21 minutes (12:27 to
  12:48). "About half an hour" is safe.

**6. Second instance, same afternoon (optional).** The team then leaned toward "turn on automatic restart". PA read
the config and the source and found it was already on, and can't fire for this kind of database. PA: ""turn on
automatic restart" sounded like a fix, but it was already on." [pa l.76–81] Use it as a one-line echo, or leave it
for the narrative, which covers that setting.

## Possible closing thought
A guess about the cause, however good, doesn't change the plan until someone checks it. The look was cheap,
read-only and a few minutes long, and it was the one thing every agent had asked for and none had done.

## Footer
- **Next on Building Piper Morgan:** "The Unguarded Entrance" (Tue 11-03, title final). Suggested tease: *on a
  holiday Sunday, my chief of staff agent finds a hole in the routine every agent runs, and by evening finds the
  worst case of it in their own seat.* (The same line Thursday's post used.)
- **Reader question idea:** *When something breaks, how long does your team debate the fix before anyone looks at
  what actually happened?*

## Left out on purpose
- The outage's start time disagrees across logs (10:55–11:21). The piece doesn't need it.
- Who relayed what to you while you were in other sessions. Not the point, and it names other projects' agents.
- The token and permission details of the restart workflow. Engineering detail.
