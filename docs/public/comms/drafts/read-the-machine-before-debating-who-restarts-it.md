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

# Verifying the likely cause

Arch had offered a working hypothesis in their memo, that the Postgres (database) virtual machine had exhausted its available physical memory (RAM) and swap space, forcing the system kernel to terminate a process to avoid a total system crash, something called an "out-of-memory (OOM) kill." They also noted that this could be verified or refuted by checking the logs, but no agent had bothered to look yet.

My prototypical product assistant agent (Piper Alpha) picked up on this noting that the other three agents had all called for the evidence to be captured before any restart, but none had bothered to actually do so. Perhaps because they are leadership and Piper is staff, they took the initiative to ready the logs on our hosting service (Fly.io).

The kernel log showed that the system had indeed run out of memory and killed the database process at about 11:19, on a
256 MB machine with no swap. Monday's earlier crash had the same sort of footprint. Piper confirmed the hypothesis and pointed out that restarting the database in this state would leave the same OOM risk, with the next shutdown liking happening two days hence, right when I was supposed to be making the call about whether we were on track for an October 30 beta launch (SPOILER: we made it).

# The real question

The debate about the proper way to restart the database unfolded over half an hour when the answer sat in an unexamined log. The fix took much less time.

Now that the real question was clear, Lead bumped the database memory to 512 MB. By that afternoon I was available to oversee the restart and the database came back fine, passing all health checks.

# Winning the wrong argument

I don't think agents are unique in their ability to go off on long tangents or even "bike shed" arguments without first checking the facts of a situation. I'm fairly certain I've seen human-only teams do this many times in my storied career. Regardless of who or what is running into that rabbithole the solution is the same. Check first!

*Next on Building Piper Morgan, we resume the building narrative with "The Unguarded Entrance" Suggested tease: *on a
  holiday Sunday, my chief of staff agent finds a hole in the routine every agent runs, and by evening finds the
  worst case of it in their own seat.* (The same line Thursday's post used.)
- **Reader question idea:** *When something breaks, how long does your team debate the fix before anyone looks at
  what actually happened?*

## Left out on purpose
- The outage's start time disagrees across logs (10:55–11:21). The piece doesn't need it.
- Who relayed what to you while you were in other sessions. Not the point, and it names other projects' agents.
- The token and permission details of the restart workflow. Engineering detail.
