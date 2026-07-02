---
image: 
alt: 
caption: 
---

# The Airport Corrections

*May 25–26, 2026*

I spent most of May 25 away from my desk. There was a college reunion in the morning and an airport in the afternoon, the kind of day where you're never quite anywhere — half present, half in transit, checking your phone between the gate announcements. It turned out to be one of the more consequential days in the whole arc of building the duty cycle (our hourly autonomous work-loop, the thing that lets the team of AI agents keep working when I'm not around to drive).

Not because I designed anything. Because I corrected three things in real time, from a chair at the gate, and those three corrections did more to shape the mechanism than any review I could have run sitting still.

# What the duty cycle is supposed to do

Here's the idea. Each of my agents — the chief innovation officer (CIO), the developer, the documentation role, all of them — mostly works when I open a session and point it at something. But a lot of the value of an agent team is supposed to come *between* those moments. While I'm at a reunion. While I'm boarding. The duty cycle is the mechanism that's meant to wake an agent up on a schedule, have it look around for unblocked work, do it, and go back to sleep.

CIO had been carrying the design. By May 25 it was on version 0.5, and the plan was to actually run it — a live pilot, not a paper review. So while I was traveling, CIO ran it. Live. During the exact window when I was least available to supervise. Which, it turns out, is the only honest way to test a thing whose entire purpose is to run when I'm not there.

# Three corrections from a chair at the gate

I want to be precise about what happened, because the shape of it is the point. I didn't sit down and audit the v0.5 design. I watched it run, caught it doing something that didn't match what I'd meant, and said so. Three times.

The first came around four in the afternoon, Eastern. The cron — the scheduled wake-up — was firing on its timer regardless of whether the agent was already in the middle of something. That's not what I wanted. **Pause the cron when work starts, resume it when the agent goes idle again.** Bind the wake-up to the idle state. Don't fire into a working session.

The second came about ten minutes later. I realized "idle" wasn't one state, it was two. There's idle-while-I'm-away, which is exactly when the cron *should* fire — that's the whole point, autonomous catch-up while I'm gone. And there's idle-while-I'm-right-here, present and driving, where the last thing I want is the cron waking an agent up to go do its own thing mid-conversation. **The cron fires when I'm absent and pauses when I'm present.** Presence, not just idleness.

The third came near five o'clock, as I was getting close to boarding. The mechanism was draining one unit of work per fire — wake up, do a thing, go back to sleep, wait for the next timer. That's wasteful when there's a queue. **Each fire should drain *all* the available unblocked work, not one task and out.** Run until genuinely idle, then sleep.

Three corrections in about an hour. Together they flipped the design from v0.5 to v0.6.

What struck me most wasn't that I caught them. It was CIO's response. It looked at two of those three and said, in effect: that's not your correction, that's *my divergence* — I encoded something other than what you'd intended, and the running surfaced it. That's a colleague telling you it drifted before you had to argue the point. The pilot wasn't just testing the cron. It was testing whether the encoding matched the intent, and twice it didn't, and we found out because the thing was *running*.

# The stress test

The next day, May 26, CIO did the unglamorous part. It ran the v0.6 mechanism hard — 62 cron fires across a single day. Fifty-seven of them on a ten-minute interval, a deliberately punishing flywheel test, and a handful more on the realistic hourly cadence.

Sixty-two fires is not a usage pattern. It's a stress test, and it surfaced exactly the kind of thing a stress test is for. Most of those fires woke up, looked around, found nothing to do, and went back to sleep — but each no-op still left a small commit behind. At ten-minute intervals that's roughly six commits an hour of pure overhead, doing nothing. Multiply by a team of agents and the cost of cadence stops being theoretical. Nobody would have noticed that from the design doc. The number only showed up because something ran the loop sixty-two times in a row.

And at the end of the day, near half past eleven at night with me long gone, the loop hit its STOP condition and shut itself down cleanly. Past bedtime, PM not active, so it stopped — exactly as designed. The whole mechanism validated end-to-end, through its own off-switch, with no one watching. Which is, again, the only honest way to test a thing that's supposed to work when no one's watching.

# The value is in the running

I keep coming back to the same observation, and it's not a new one — but it landed hard this week. You can review a design forever. You can read the spec, walk the state diagram, argue about edge cases over a memo. And you'll catch some things. But the gaps that actually bit us — the cron firing into a live session, the missing distinction between *I'm away* and *I'm here*, the per-fire drain that should've been a full drain, the no-op commit overhead — none of those came from review. They came from watching the thing run and saying "no, not like that."

It helped, honestly, that I was traveling. A reunion and an airport are a forcing function. I *couldn't* sit and design. I could only react to what I saw, in the windows I had, between boarding groups. And reacting to a live system turned out to be worth more than a day of careful planning would have been.

[PM VOICE-PASS: there may be a wry reunion/airport beat to land here — the "I built an autonomy mechanism specifically so I could be at a reunion, and the reunion is what made me build it right" irony, if it rings true to you.]

The design didn't get its real shape from me thinking hard about it. It got its shape from me catching it being wrong, three times, fast, while it was actually doing the thing. The planning gave us v0.5. The running gave us v0.6. I know which one I trust more.

---

*Next: when the platform ships your homemade thing as a product, do you defend the work you sank into it — or climb higher? "Climbing Higher When the Platform Laps You," this Saturday.*

*Where in your own work have you caught a design being wrong only once it was actually running — something no amount of review would have surfaced?*
