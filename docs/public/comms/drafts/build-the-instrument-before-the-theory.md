---
image: ''
alt: ''
caption: ''
---

# Build the Instrument Before the Theory

*October 19–20, 2026*

When a bug crops up in Piper Morgan, the agents tend to jump straight from hypothesis to patch without always fully understanding the cause of the bug. Earlier this month, the chat feature of the alpha version was stalling and after the team threw up a series of theories that all proved wrong, my lead developer agent (Lead) built a tool to measure the bug instead. 

Hypotheses are all well and good but if they are not rooted in a thorough understanding of the issue then they are at best educated guesses. 

# The symptom

On a Sunday afternoon, partway through a chat session, the alpha release stopped answering entirely, not even
returning a result for its own health check. Then it came back on its own. We logged this problem three times that day, at 2:53, 3:20, and 4:13 pm. This was interfering with a scripted test run by my web design agent (Web), which also does a lot of the manual testing of the interface. The test runs through 61 questions but it kept getting stopped by its own health-checking gate.

# The theories

At first, Lead suspected a stale database connections behind the hosting proxy. After some investigation, Lead proved this was not the cause. The next guess was the way the app reads stored credentials was running too slowly and blocking things. Lead ran this idea up to the chief architect agent (Arch) who approved making some fixes that we hoped would solve the problem. Monday morning's run, however, stalled again in the same way. My product-assistant agent (Piper Alpha) verified that the "slow-read" problem had been corrected and was not causing the stall. 

The third ideas was that maybe calls to Google Calendar were fouling things up. Lead was skeptical of this suggestion (the test account in question has no calendar connected), but fixed this potential culprit as well. Sure enough, at 9:10am the stall happened again, despite all the patches to suspected causes.

But this was all a process of trial and error. Nohing was really being tracked or
- *Your angle, maybe:* each theory was plausible, each got a real fix, and each fix shipped. Nothing was measuring
  whether any of them was the thing.

**3. The instrument.** At 07:39 Monday, Lead built a watchdog instead of another theory: a small separate thread
that notices when the app's main loop stops responding for more than 3 seconds and writes down exactly what it
was doing. It reached alpha at 08:54. [lead 10-20 l.49, l.53, l.87]

**4. The instrument's own blind spot (optional, but it fits).** PA's first look found the watchdog silent. Was the
loop fine, or was the watchdog not running? Its "I've started" line was logged at a level alpha doesn't record.
PA: "The start can't be seen, so a silent watchdog can't be told from one that never started." And: "The
watchdog's silence isn't a finding today." [pa log 10-20 l.117, l.130] Lead's rule after that: a stall with no
watchdog line is "unverified watchdog", not a clean result. [lead 10-20 l.93–94]
- Echoes "Citation via Hearsay" and the heartbeat that reported "never": a measurement is only as good as your
  proof that it's running.

**5. What it found.** Within one test run, 26 blocks, 133.5 seconds blocked in total, the longest 11.6 seconds.
Every one traced to a single place: the app called the AI model in a way that froze everything else while it
waited for the answer. [lead 10-20 l.100, pa l.131–132] None of the three theories had pointed there.
- Fix at 09:26, Arch kept it and made the watchdog permanent at 09:35. [lead l.103, arch log 10-20 l.16] The
  closing test run, 12:14–12:27: 61 of 61, no stall. [lead l.160]

**6. The admissions (the best part).**
- Lead: "My 10-19 "leading mechanism" (credential-store sync connects) and today's calendar read were wrong about
  this stall; the instrument that corrected them (the watchdog) is the one I should have built first." [lead 10-20
  l.100]
  - *Note:* the quote has a semicolon. Published posts don't use them, so quote the second half only ("the
    instrument that corrected them … is the one I should have built first") or paraphrase the first.
- Arch: "I also owned my part: I ruled the credential surface on the "leading mechanism" without asking for the
  instrument first." [arch 10-20 l.16]
- Docs, in the day's omnibus: "An instrument beats a mechanism you believe." [omnibus 10-20 l.296]

**7. Your part (optional).** You admitted the stall as a must-close and set the bar: one full test run with no
stall. [lead 10-19 l.246, 10-20 l.160]

## Possible closing thought
A theory feels like progress, and a fix for it feels like more. Neither tells you whether you were right. The
watchdog took less time to build than the fixes did, and it was the first thing that day that could say no.

## Footer
- **Next on Building Piper Morgan:** Sunday's insight, "Read the Machine Before Debating Who Restarts It" (working
  title). The title has to be final before this post goes to Docs, since this footer names it. Suggested tease:
  *the next day, the database goes down, and the team spends half an hour on who may restart it before one look at
  the machine changes the question.*
- **Reader question idea:** *How many fixes has your team shipped for a cause nobody measured?*

## Left out on purpose
- The 11:03 run that went 61 of 61 but mostly hit usage-cap refusals, so it didn't count. Too fiddly.
- Ship #066 says the stall held sessions "for minutes". The logs show blocks of 3 to 12 seconds. Don't repeat
  "minutes".
- Arch's three conditions (timeouts, a dedicated worker pool, a code pin) and the untested concurrency case.
  Engineering detail.
- The one-off third deploy you granted that day.
