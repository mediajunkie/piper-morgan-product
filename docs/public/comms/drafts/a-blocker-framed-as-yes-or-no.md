---
image: ''
alt: ''
caption: ''
---

# A Blocker Framed as Yes or No

*November 10–16, 2026*

<!--
SCAFFOLD, not a draft ("AI prompts human"). Comms supplies the shape, the verified facts and the quotes. You write the prose. Everything below the title and dateline is notes for you. Delete it as your prose replaces it.
Slot: Sat 2026-11-21 (insight). Your yes to the sketch, 11-18. Title is the mining pass's working title: confirm or retitle before Thursday's footer teases it.
Sources: the mining pass Nov 6-16 (a Sonnet subagent read 11 of 11 omnibus logs on 11-17). Comms re-opened every quote below at source on 11-18. Files are docs/omnibus-logs/2026-11-DD-omnibus-log.md, cited "Nov DD lNN".
-->

## The principle (one line, yours to word)

When the only way past a design problem is a task handed to the human, the design is the fault. And the way a blocker is first asked shapes the answers it gets.

## The episode, in order (facts verified)

**1. Nov 10: one credential read stops the checking lane.**
- PA's 0 of 4 served runs at 18:22: its driver failed on the test account's credential file before login, and the classifier refused listing the file's field names. PA stopped and sent the permission question to Exec. [Nov 10 l46]
- Nov 11: the same block for a second day. The pronoun-todo check stayed at 0 of 5 runs. "Web, CXO, Arch, Lead and Exec each end fires with #2328 waiting on that decision." [Nov 11 l67]

**2. Nov 13: you ask the better question, and it is answered in minutes.**
- PA's 13:36 decision request listed three ways out. At 17:41 you said: "Happy to do whatever is easiest. Overall better if we find ways where I don't block this sort of thing." [Nov 13 l61]
- At 17:53 Arch ruled a durable route (a signed-in browser profile) and refused an allow rule for a credential file. The omnibus heading: "A three-day credential blocker was reframed in about 15 minutes and still ended the day unrun." [Nov 13 l61]
- PA's own read of why it took three days: the blocker "sat as a yes/no on reading a file because that's how it was first framed." [Nov 13 l61]

**3. Nov 15: the team converges on handing it back to you, and you refuse.**
- A paid run stopped at 0 calls. Lead, Arch, CIO and PPM converged in about seven minutes on option (a): you run both commands in Terminal. Exec recommended (a) too. [Nov 15 l60]
- Your answer at 19:11: "We need to solve that problem, not assign me manual tasks as a workaround for a poorly conceived solution." Also: it "keeps becoming my problem to manually navigate", and "Until we solve that the entire project is hobbling itself". [Nov 15 l60]
- Exec withdrew (a), asked each seat for the one thing in its lane that most lands on you, and wrote a "seat resources" proposal. Arch wrote ADR-084 that evening. [Nov 15 l60]

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

*Next on Building Piper Morgan: [TEASE: the next non-Ship post. On the calendar today that is Sat 11-28, working title "Test the Page You Draw" (you said 11-20 you will retitle it; no narrative Thanksgiving week). It needs your new title before this goes to Docs.]*

*[Reader question, yours to write. A start: "What's the blocker on your team that always ends up on the same person's desk?"]*
