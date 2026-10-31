---
image: ''
alt: ''
caption: ''
---

# Check the Machine First

*October 21, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human", PM ruling 2026-10-07). Comms supplies the shape, the verified facts and
the quotes. PM writes the prose. Everything below the line is notes for PM. Delete it as the prose replaces it.
Title is the working title from the 10-23 mining table, rename freely.
Slot: Sun 2026-11-01 (insight). Paired with Sat 10-31 "Build the Instrument Before the Theory": measure first,
then believe what the measurement says. Sources: PA, Lead, HOST, Exec logs 10-21, the 10-21 omnibus, PA's and
Arch's 10-21 memos. Facts gathered by an Opus subagent, key lines re-read by Comms.
-->

---

## The idea in one sentence

When something is down, one read-only look at the live machine can change the question you're debating, and on
10-21 it turned "who is allowed to restart the database" into "how much memory does it need".

## Already told elsewhere: don't retell
- **The outage itself** got one line in Weekly Ship #066. The longer story (the restart setting that couldn't
  fire, the external restarter and its test) belongs to the Oct 20–22 narrative beat, which isn't written yet.
  Keep this piece to the window between the outage and the read.

## Beats, in order (facts verified, source in brackets)

**1. The symptom.** Late morning, the alpha database stopped answering. The app itself was up, so the health page
read "database: unreachable" next to "web: healthy". Lead: "Every sign-in and chat fails until the database
answers." [lead log 10-21 l.93. The omnibus has the health watch red at 11:21]

**2. The debate.** Lead asked for a restart, attended, on your hand, with the machine state captured first.
[lead l.94, 11:28] You were deep in other work, so a fix waited on you. Around 12:27 Lead proposed a workflow any
agent could run to restart the database. Within minutes:
- My chief innovation officer agent (CIO) said it needed a new, narrower access token, and a restart policy first.
- My chief architect agent (Arch) set three guards, including "Capture before you restart … because a restart
  erases the evidence." [Arch memo 10-21 l.17]
- Lead withdrew the proposal at 12:37. My head-of-sapient-trust agent (HOST) ruled on whether a gated restart was
  allowed at all at 12:42. [lead l.110, host l.41]
- Every agent in the thread was designing the *recovery*. *Your angle, maybe:* careful, reasonable governance work, aimed at the
  wrong question.

**3. The detail that makes it sharper.** Arch had already named the likely cause, in the same memo: "My working
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
