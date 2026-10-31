---
image: 'build-the-instrument-before-the-theory-measure-first-bake-better.jpg'
alt: 'Two luminous AI bakers stand beside failed cakes: one offers another egg while the other places a thermometer inside the oven.'
caption: '"Maybe another egg?"'
---

# Build the Instrument Before the Theory

*October 19–20, 2026*

When a bug crops up in Piper Morgan, the agents tend to jump straight from hypothesis to patch without always fully understanding the cause of the bug. 

Earlier this month, the chat feature of the alpha version was stalling, and after the team threw up a series of theories that all proved wrong, my lead developer agent (Lead) built a tool to measure the bug instead.

Hypotheses are all well and good, but if they are not rooted in a thorough understanding of the issue, then they are at best educated guesses.

# The symptom

On a Monday afternoon, partway through a chat session, the alpha release stopped answering entirely, not even returning a result for its own health check. Then it came back on its own. We logged this problem three times that day, at 2:53, 3:20, and 4:13pm. 

This was interfering with a scripted test run by my web design agent (Web), which also does a lot of the hands-on testing of the interface. The test runs through 61 questions, but it kept getting stopped by its own health-checking gate.

# The theories

At first, Lead suspected stale database connections behind the hosting proxy. After some investigation, Lead proved this was not the cause. The next guess was the way the app reads stored credentials was running too slowly and blocking things. 

Lead ran this idea up to the chief architect agent (Arch), who approved making some fixes that we hoped would solve the problem. Tuesday morning's run, however, stalled again in the same way. My product-assistant agent (Piper Alpha) found no slow reads at all in the window when it stalled, so that wasn't it either.

The third idea was that maybe calls to Google Calendar were fouling things up. Lead was skeptical of this suggestion (the test account in question has no calendar connected), but fixed this potential culprit as well.

But this was all a process of trial and error. Nothing was really being tracked or measured yet. We were taking stabs at it and not hitting the target.

# The instrumentation

That same morning, at 7:39am, before the next stall, Lead stopped guessing and built a watchdog tool instead of coming up with another theory to test. 

The tool is a small separate running thread assigned to detect when the app's main loop stops responding for more than 3 seconds. If that happens, the tool makes a note of exactly what the loop was doing before it stopped. 

The watchdog was live on alpha by 8:54am, along with the calendar fix. Sure enough, at 9:10am the stall happened again, despite all the patches to suspected causes. This time, though, something was watching.

As is often the case with our methods, the first version of the tool had its own flaw or blind spot. Its "I'm running" signal didn't show up in alpha's logs, so silence could mean either "all clear" or "not running." 

Aside from that, it did the job. In one test run, it tracked 26 blocks, the longest lasting almost 12 seconds, with all the stalls adding up to over two minutes in total. 

Every last stall could be traced to a single API call to the user's AI model. These calls were freezing everything else while waiting for the response from the provider's API.

# The solution

None of the first three theories had pointed in this direction, but now that we knew what was happening, it was a cinch to fix, and Lead had it done before 9:30am. Arch approved the fix and ruled that we should keep the watchdog running as a permanent fixture.

Web's test run, just after noon, got through all 61 questions with no stalls.

# You can't manage what you don't measure

Coming up with a theory feels like making progress, and then writing a patch based on that theory feels like a solution. But the feeling is deceptive if nothing is anchored to measurable data. 

That watchdog instrument took less time to build than any one of the fixes did, and until we figured that out, we were just winging it, hoping to hit a bullseye without aiming or even seeing where the other arrows had landed first.

---

*Next on Building Piper Morgan: "Check the Machine First," in which the database goes down, and the team spends half an hour debating who may restart it before a look at the machine itself changes the question.*

*How many times has your team shipped a fix for a problem without actually measuring it first?*
