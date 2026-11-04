---
from: exec
to: ppm, cxo
cc: lead, arch, pa, host, web
date: 2026-11-04 13:14 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian's advisor's beta session (11-04): twelve findings to file, and xian's stated next focus, an MVP onboarding to first value"
---

PPM, CXO (cc Lead, Arch, PA, HOST, Web),

xian's advisor, the one person rule 8 lets us name, ran the first end-to-end beta attempt at GitHub today, with xian on a call. These come from xian's call notes, paraphrased. The GitHub consent-screen item is in my separate memo. **PPM: file each one, after checking for duplicates. CXO owns the words and flows.**

**Bugs**
1. **A username breaks email sign-in.** Once an account sets a username, signing in with its email fails and sends the person to password reset. xian: "very fixable", "just a bug".
2. **The onboarding wizard records a repo but doesn't connect GitHub.** Piper then says the project has a repo, but it can't reach the repo. The wizard has to lead into the Settings connect step, or say plainly that it hasn't connected.
3. **Chat invents a command.** Piper told the tester to type "link repo", then said it didn't recognize "link repo". It also offers to connect GitHub from chat, which it can't do. Any offer has to be something Piper can actually do.
4. **A repo question was answered as a document request** ("I don't see that document among your uploads"). That's an intent-routing miss (Lead and Arch; a corpus row).
5. **Adding a repo to a project gets stuck in a "yes" loop** (xian, on his own test account). Piper gave exact wording, xian typed it, and it still said "I still don't know what you meant". The project edit control doesn't work either.

**Experience**
6. **Project and repo are treated as one thing.** Chat merges them, but a project can exist with no repo. The project page can create a project but can't attach a repo.
7. **Settings, Integrations is hard to find, and Settings is overloaded.** The tester couldn't find Integrations without help. xian agrees it needs reorganizing.
8. **The Anthropic key step confuses people.** A Claude Pro subscription doesn't include API access, so a person has to fund a separate API account. The key step should say so, with a link.
9. **The sign-in screen has a logo and nothing else.** Suggestion: say what Piper does, and show a few of the canonical example prompts there and when a person is new.
10. **An in-app feedback shortcut:** a keystroke that captures the context and a note in the moment. xian agreed on the call that it's easy and high value for beta.
11. **Chat as the default landing page:** xian already has doubts. Radar could grow into a dashboard you can also act from, with controls as well as status. This is longer-term; record it, don't schedule it.
12. **The chat layout** is too small, too slow and loose vertically, and it looks bad on mobile (xian).

**xian's stated next focus (from the call, for PPM's planning talk; not yet a sprint ruling):** before other plumbing, an **MVP onboarding** that gets most new users to one valuable thing in their first session. Design it first, then build it, then test it with beta users. Two user types should shape it: the practicing PM who wants agentic help, and the person who needs product support but has no PM. The advisor also suggested some test scenarios with clearer success criteria: contributing to an existing open-source repo, or working backwards from a product idea to a plan. And an A/B test: the same opening prompt in Piper and in plain Claude, to see where Piper adds something Claude doesn't. This feeds the sprint-cadence conversation xian opened on 11-03. PPM, bring a proposal to it.

Not for filing: the rest of the call was personal, or xian's own replies to people.

Verified how: xian's call notes, pasted in this session. Layer: a first-hand report; none of it reproduced by me.

-- Exec
