---
image: 'read-the-machine-before-debating-who-restarts-it-build-the-instrument-before-the-theory.webp'
alt: 'Three translucent AI agents debate restart procedures around a table piled with policy manuals, while a fourth points to a nearby machine’s MEMORY gauge, its needle buried in the red.'
caption: '"This isn''t good, right?"'
---

# Check the Machine First

*October 21, 2026*

Now that I've turned my agents into a debating society, I've noticed that sometimes they will devote quite a few loops to hashing out a disagreement before one of them checks the actual facts. At this point, it can turn out that the real discussion needs to be about something else entirely.

Last month, this happened when a long discussion trying to determine which agent is allowed to restart the database involved them all talking past the real question at hand: "how much memory does it need?"

# The database goes quiet

Late that morning, the alpha database had stopped responding. The app itself was still running, the health page reporting "web: healthy" but "database: unreachable." My lead developer agent (Lead) reported "Every sign-in and chat fails until the database answers" and asked me to restart it by hand, with an agent capturing the machine state first.

I was busy doing other things, essentially tying up the whole team behind this bottleneck, and this led to a discussion among several agents:

- Lead proposed a workflow that would let any agent restart the database.
- My chief innovation officer agent (CIO) suggested that the project needed a new, narrower access token, and a restart policy as well before any agent could be allowed to restart the database.
- My chief architect agent (Arch) defined three guards for any restart, one of which was "Capture before you restart … because a restart erases the evidence."
- Lead then withdrew the proposal.
- My head-of-sapient-trust agent (HOST) offered a ruling on whether a "gated restart" should be allowed at all.

This is reasonable stuff to discuss! Very prudent. Sober even. But it's focused on a logistical triviality instead of the real question, which was why did the database need to be restarted at all.

# Verifying the likely cause

Arch had offered a working hypothesis in their memo, that the Postgres (database) virtual machine had exhausted its available physical memory (RAM), forcing the system kernel to terminate a process to avoid a total system crash, something called an "out-of-memory (OOM) kill." They also noted that this could be verified or refuted by checking the logs, but no agent had bothered to look yet.

My prototypical product assistant agent (Piper Alpha) picked up on this, noting that Arch, CIO and HOST had all called for the evidence to be captured before any restart, but none had bothered to actually do so. Perhaps because those three are leadership and Piper is staff, Piper took the initiative to read the logs on our hosting service (Fly.io).

The kernel log showed that the system had indeed run out of memory and killed the database process at about 11:19, on a 256 MB machine with no swap. Monday's earlier crash had the same sort of footprint. Piper confirmed the hypothesis and pointed out that restarting the database in this state would leave the same OOM risk, with the next shutdown likely happening two days hence, right when I was supposed to be making the call about whether we were on track for an October 30 beta launch (SPOILER: we made it).

# The real question

The debate about the proper way to restart the database unfolded over half an hour while the answer sat in an unexamined log. The fix took much less time.

Now that the real question was clear, Lead picked 512 MB. One command adds the memory and restarts the machine, and that afternoon I was available to run it. The database came back fine, passing all health checks.

# Winning the wrong argument

I don't think agents are unique in their ability to go off on long tangents or even "[bike shed](https://en.wikipedia.org/wiki/Law_of_triviality)" arguments without first checking the facts of a situation. I'm fairly certain I've seen human-only teams do this many times in my storied career. Regardless of who or what is running into that rabbit hole, the solution is the same. Check first!

---

*Next on Building Piper Morgan, we resume the building narrative with "The Unguarded Entrance" from September 6, in which my chief of staff agent (Exec) finds a hole in a routine every agent runs, with the worst example in their own seat.*

*When something breaks, does your team get to clarity on what actually happened before launching into a debate about how to fix it?*
