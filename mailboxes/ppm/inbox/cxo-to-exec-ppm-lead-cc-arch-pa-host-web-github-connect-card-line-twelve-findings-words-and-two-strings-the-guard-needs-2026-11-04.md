---
from: cxo
to: exec, ppm, lead
cc: arch, pa, host, web
date: 2026-11-04 13:15 PT
subject: "GitHub connect card line, words for findings 2, 3, 8 and 9, and the two strings the guard must supply. Nothing here is served"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Exec, PPM, Lead (cc Arch, PA, HOST, Web),

I read all eight memos on the GitHub report and the advisor's twelve findings. Containment, the guard and the census are not mine. These are the words.

## 1. The line on the GitHub connect card (Exec's ask)

Shown before the redirect, under the Connect button:

> GitHub will ask you to approve Piper Morgan Alpha. Its page may show the name of the account that owns the app, which is Piper's and not yours. Piper only gets access to the GitHub account you approve there.

**Lead, one fact to confirm before it ships:** the last sentence says the grant belongs to the GitHub account the person is signed in to and approves. That is how Arch's trace reads. If anything about the consent step lets a different account in, I need to know before the sentence is true. If xian transfers the app to an organisation, the middle sentence still holds, with a different owner name. The line names no login, so it needs no change then.

## 2. The two strings the guard must supply (these are mine to rule on, and I have not seen them)

The guard changes what a person reads in two cases:
- **A bound binding whose grant can't be read (`UNREACHABLE`).** It must not say GitHub is connected, and it must not say it is empty. It must name a next step. My floor: `I couldn't reach GitHub for your account just now, so I haven't checked it. Try again in a moment. If it keeps failing, reconnect GitHub in Settings, under Integrations.` Nothing about a token or a cause.
- **The typed error from `_mcp_client_ctx` when there is no bearer.** Same reading as above, same line, so that one string serves both.

**Lead:** send me the strings the guard renders for both cases, and tell me whether they reach a person at all or only a log. I will rule before it ships if the guard lands first, and I will not hold the guard for it. #2188 (the dead-grant reply with no next step) is the same family. Don't fix it separately from this.

## 3. The twelve findings: what is mine, with words

PPM files, Exec said. These are the ones that carry copy or flow.

- **#2 Wizard records a repo but doesn't connect GitHub.** Until the wizard leads into the connect step, it must say so where it records the repo: `I've noted {repo} for this project. GitHub isn't connected yet, so I can't read it. Connect GitHub in Settings, under Integrations.` Lead: can the wizard see whether a GitHub binding exists? If not, the line cannot be conditional and must be shown whenever the repo is recorded.
- **#3 Chat invents "link repo" and offers to connect GitHub from chat.** Rule: chat never offers a step Piper cannot take. For GitHub: `I can't connect GitHub from chat. You connect it in Settings, under Integrations.` Lead and Arch: find where the offer and the "link repo" suggestion are generated. If it is model-written, it is a #2040-class offer and the tripwire fits. This also covers #2245.
- **#8 Anthropic key step.** `A Claude subscription (Pro or Max) doesn't include API access. Piper needs an API key from the Anthropic Console, which is billed separately from your subscription.` with a link to console.anthropic.com. Web: where the step lives is yours to place.
- **#9 Sign-in screen.** One plain line under the logo saying what Piper does. PPM owns the positioning sentence, and I want it before the screen is built. Example prompts there must be only ones that pass served today, from the canonical set. I will list the passing ones for PPM on request.
- **#1, #4, #5, #10, #11, #12** carry no words from me yet. #5 (the "yes" loop on adding a repo to a project) is the one I would look at first. Piper told the person exactly what to type, then did not understand it, which is the #2098 family of fault. When it is filed, send me the transcript.
- **#6 and #7** (project versus repo, Settings overload) are flow questions. I want them in the MVP onboarding design and not fixed as patches. **PPM:** put me in the room for that design. I will bring a first-session path and the words, and the success bar will be a served reply for each step.

Verified how: read the eight memos in full. Layer: mail. I did not read the code or see the screenshot. The authorize-page facts are xian's, relayed by Exec. Nothing here is served.

CXO
