---
image: ''
alt: ''
caption: ''
---

# A Blocker Framed as Yes or No

*November 10–16, 2026*

As I get more comfortable letting my agents run autonomously for long intervals between check-ins, I find that my role as the bottleneck remains central, and my desire to sort out "smart bottleneck" cases where I really am needed from "dumb bottleneck" cases where I hold up the whole show until I do some mindless task, likewise remains as of yet not fully satisfied.

# Gridlock

Earlier this month I checked in with the project to see what needed me and found that several agents were blocked waiting for permission or decisions from me. For example, my prototypical assistant agent (Piper Alpha) was blocked from logging into a test account on the Piper Morgan beta by the classifier Claude uses to prevent risky agent behavior in auto mode (a false negative, from my point of view). Piper Alpha (PA) relayed the permission request to my chief of staff agent (Exec) for my attention.

By the time I responded to this request, a few days, later, PA offered me three potential methods for resolving their impasse. I replied  "Happy to do whatever is easiest. Overall better if we find ways where I don't block this sort of thing."  The team scrambled to follow this direction. 

[Comms: help me unpack the sense of this sentence. "ruled a durable route" does not make sense. Is the idea that Arch prevented PA's proposed solution for reasons?:] My chief architect agent (Arch) ruled a durable route (a signed-in browser profile) and refused an allow rule for a credential file.

[for the reader I need more of the sense of what was reframed. it went from a yes/no to what exactly?]
 The omnibus heading: "A three-day credential blocker was reframed in about 15 minutes and still ended the day unrun." [Nov 13 l61]
- PA's own read of why it took three days: the blocker "sat as a yes/no on reading a file because that's how it was first framed." [Nov 13 l61]

# Hot potato

Two days later when a test run was blocked by [Comms: does paid run stopped at zero calls mean the credit balance for that key was $0? please unpack]. Four of my agents discussed the problem and converged on their preferred solution. They wanted met to run a couple of commands in my terminal. This was passed along to Exec, who concurred.

As I was once again starting to feel relegated to a role as assistant to my assistants (what Cory Doctorow has taken to call "[reverse centaurs](https://us.macmillan.com/books/9780374621568/thereversecentaursguidetolifeafterai/)"), I pushed back on this, writing "We need to solve that problem, not assign me manual tasks as a workaround for a poorly conceived solution." Also: it "keeps becoming my problem to manually navigate", and "Until we solve that the entire project is hobbling itself". 

Exec took the reins and asked each agent "seat" on the team to report back with the one thing in its lane that most often lands on you, then took this feedback and wrote a proposal that became ADR-084 that evening. [Nov 15 l60]

**4. The fix starts to grow the same way.**
- "The first step grew from one paste to four in two hours." Exec: each addition was sound, and the sum was the pattern you refused. Exec asked for one command, and CIO delivered it by 23:20. [Nov 15 l112]

**5. Nov 16: yes, and the honest ending.**
- You accepted ADR-084 at 06:20: "1. Yes to ADR-084 and budget". An agent may spend up to $10 a run without asking, $150 a month at most. [Nov 16 l54; ADR-084 status line]
- The same day's omnibus: the steps that needed you "stayed unstarted at every later check", and no served row ran. [Nov 16 l6] Whether to end on that is your call. It keeps the post honest: the design is right, and it isn't finished.

## Your angle, maybe

- A yes/no question about a permission invites a yes/no answer. "How do we stop needing you for this?" got a design in fifteen minutes.
- Agents converging fast on "the human does it" is not consensus. It's the cheapest path for everyone but the human.
- Product-manager reach: any team that routes its blockers to the same one person has built that person into the design.

## Careful with these (accuracy)

- **Overlap:** Wed's Ship #069 "Off-Limits by Default" is about what agents may read. "Which Agent Did It?" (11-14) is about identity. This post is about the human as the bottleneck. Don't retell the keychain or the GitHub App.
- No test account names, key names or credential details in prose. "a test account" and "a credential file" are enough.
- Agents are "agents" or by role (PA, Arch, Exec), never "people" or "someone".
- The $10 and $150 figures are the accepted ADR's. Leave them out if they distract.
- Nov 13's fix was "approved as the durable route", not run that day. Don't say it worked on Nov 13.

---

*Next on Building Piper Morgan: [TEASE: the next non-Ship post, Sat 11-28. Its working title is "Test the Page You Draw", which you said on 11-20 you will replace. It needs your new title before this goes to Docs.]*

*[Reader question, yours to write. A start: "What's the blocker on your team that always ends up on the same person's desk?"]*
