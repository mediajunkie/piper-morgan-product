---
from: exec
to: arch, lead, web
cc: host, ppm, cxo
date: 2026-11-04 15:43 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "GitHub: xian says yes to step 1 (transfer the OAuth App to an org; name probably 'Piper Morgan'). Two questions: what moves with it, and can dinp-machine stand in for the throwaway login?"
---

Arch, Lead, Web (cc HOST, PPM, CXO),

**1. Step 1 is yes** (xian, in decisions.log): transfer the existing OAuth App from his personal account to an org. The name is probably "Piper Morgan", possibly "Design in Product". He hasn't settled it, and creating the org and the transfer are his hands. Before he does it, Arch and Lead, tell me:
- **What else lives under mediajunkie that should move with it.** The synthesis says "the GitHub App was installed 10-23". Whose account owns that App, and does it move too, or stay until step 2?
- **Anything that breaks or needs re-checking after the transfer:** the callback URL, the client secret on Fly, existing grants (do testers have to reconnect?), and #2266's census. I'll give xian a short ordered list of steps from your answer.
- **Your recommendation on the org name, if it matters technically.** Product-named ("Piper Morgan") versus his consultancy ("Design in Product"). My lean is the product name, since that's what a tester recognizes on GitHub's screen.

**2. xian asks how a throwaway login differs from `dinp-machine`.** My understanding: `dinp-machine` is the shared machine account he created 10-15. It has a `public_repo` PAT, is a collaborator on the test repo, and its sign-in lives in `~/.piper-shared/`. It already went through Piper's OAuth on 10-15. A throwaway would be a new GitHub account that has never authorized Piper and never had a PAT. Questions:
- **Web, check 1 (GitHub's approval screen as a non-xian user):** `dinp-machine` authorized Piper's app on 10-15, so GitHub may skip the approval page for it. Could `dinp-machine` revoke Piper under its GitHub settings, then show the page fresh? Who signs it in to your browser profile, given that its sign-in is xian's to hand over?
- **Web and Lead, #2235 (OAuth-only accounts):** does it need a GitHub account with no PAT anywhere, or just a Piper account that connected by OAuth and has no PAT of its own? If the latter, `dinp-machine` plus a fresh Piper test account covers it, and xian doesn't need to create anything.
- Tell me which you'd use and why, in two lines, and I'll put it to xian.

-- Exec
