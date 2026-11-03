---
image: 'docs/public/comms/drafts/the-unguarded-entrance-sheepish-inspector-helmet-on-table.png'
alt: 'A translucent AI safety inspector sheepishly touches their bare head as a helmeted worker points it out. The inspector’s hard hat sits beside a clipboard on a small table.'
caption: '"Some safety inspector you are!"'
---

# The Unguarded Entrance

*September 6, 2026*

If you’ve followed this tale for any amount of time at all you kind of already know this one. Agent finds problem. Agent makes rule to check itself. Agent discovers the culprit is itself. The calls were coming from your house. The butler did it.

# It was a dark and stormy night

It was Sunday of Labor Day weekend. My hands were mostly off the keys (by request), the agents running their duty cycles. My lead developer agent (Lead) called it the fifth quiet day in a row. Meanwhile, a small gap was opening up in the routine. 

I've explained the duty cycle before. At the start of the day there's a wake-up routine. Then for most cycles in the day, you have a work session and the last cycle of the day is a stop routine. The start and the stop have unique requirements involving record-keeping and other scheduled work but what we learned that day was that there is a loophole in the way the process was designed.

The way it was written, every agent's duty cycle starts with a step 0 telling them to start the day's session log but those steps only run when the day starts with the scheduled wake-up. On this occasion I was a bit eager and began communicating with my chief of staff agent, Exec, directly at 6:53 am, before their scheduled wake. This led them to do substantial work (a belated sprint review) before they started the day session log, which risks losing track of work and leaving it invisible to future forensic investigations.

Further, Exec had already noticed the same gap two days earlier without flagging it for me. Searching for an apt metaphor, Exec described how what was usually the team’s strongest checkpoint could be bypassed by this “unguarded entrance" that was my ad hoc start to the day, something I used to do routinely *before* automating these loops.

# Musical chairs

Exec exhorted the other agents to check their own “seats” as they like to say, meaning in this case their own track record of logging versus actual session activity and so on. Most of them discovered no gaps for the simplest reason: I’ve been neglecting them. 

OK, well that makes it sound personal. Let’s just say I no longer need to wake up to hop on my laptop before 7 am most days to conduct five, six, seven parallel multitasked conversations. The whole point of the duty cycle is that it’s rare for me to be around to “open the store” precisely because I don’t need to do so anymore.

My chief innovation officer agent (CIO) built a detector before it was time for my lunch (explicitly to avoid leaving things diagnosed but not fixed). The team's new watchdog now flags any agent that's working without having started today's log. 

*We are a far cry from the days when my day started with manually downloading each session log from Claude Chat and then eyeballed each one to make sure it was really the final one of the day and had been closed out properly, not abandoned midway through the day, etc.*

# Sad trombone

That evening I checked in with Exec to make sure Lead wasn’t blocked by anything needed from me. Exec had recently had to remind Lead to update their stale handoff file, only to doublecheck their own paperwork and call themselves out for another lapse. Exec was the only role of the eleven on the team not maintaining a standing-items file at all. They remedied the situation that night.

There’s a messy pattern recurring here. The process appears to be shambling toward ever more careful and thorough routines and processes, and yet every new rule’s first implementation, almost without fail, tends to fail in some comically ironic way, on its first run. It’s hard not to notice how often this happens in some form or another, but the bright side is seeing how quickly and openly these first-try gaps are found now and fixed, and how the bedeviling unguarded entrances are gradually but inevitably locked down.

---

*Next on “Building Piper Morgan,” we pick up on September 7 with “Don’t Overpromise,” in which the new-user interview finally goes live, and the first look at what a newcomer actually sees catches Piper promising something no code could deliver.*

*Do you ever disrupt your own routine by jump-starting it too early? If so, what works to get you back on track?*
