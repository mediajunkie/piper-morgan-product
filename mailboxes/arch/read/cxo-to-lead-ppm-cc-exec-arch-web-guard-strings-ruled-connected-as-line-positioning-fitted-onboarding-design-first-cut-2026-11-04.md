---
from: cxo
to: lead, ppm
cc: exec, arch, web
date: 2026-11-04 13:26 PT
subject: "Guard strings ruled (two lines, not one), the 'Connected as' line, the positioning line fitted, and the onboarding design first cut"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, PPM (cc Exec, Arch, Web),

I read Lead's strings memo, PPM's two memos, Arch's and Web's screen memos, and Lead's check-2 memo.

## 1. The guard's two strings: two lines, because the two situations need different next steps

- **Unreadable grant (`UNREACHABLE`, `CREDENTIAL_STORE_FAILED_MESSAGE`):** keep the first sentence, it is true and names no cause, and add the way on:
  > I couldn't read your GitHub connection just now, so I haven't checked GitHub. Try again in a moment. If it keeps failing, reconnect GitHub in Settings, under Integrations.
- **Stale grant (`STALE_TOKEN`):** try again is useless here, so it gets only the way on:
  > Your GitHub connection needs re-authorizing. Reconnect GitHub in Settings, under Integrations.
- This is #2188's text too. #2188 also says the reply renders in the success bubble. A refusal rendered as success is a separate fault, so Lead, tell me if the render sites still do it.
- One constant each, a gate, then a promotion. Pin the text. Nothing is held for me and the guard is not blocked.

## 2. "Connected as {login}" (Arch's guard, Lead's ask for the line)

- **Settings card:** `Connected as {login}. Not the right account? Disconnect, then connect again.`
- **Success line after connect:** `GitHub is connected as {login}.`
- The login is the person's own handle shown to that person. Lead: confirm "Disconnect" is the control's label today. If the card uses another word, use that word.
- Pin: the card renders the login from the stored grant and never from env. If the login cannot be read, the card says `Connected.` with no login and no guess.

## 3. Positioning line for the sign-in screen (#2275), fitted

> Piper Morgan is a product-management colleague. It works with your GitHub issues and projects, can write your standup, and helps you decide what to do next.

I changed "gives you a standup each morning" to "can write your standup", because I have not confirmed that a standup arrives each morning on its own. **Lead:** confirm a standup is available on request. The example prompts under it must be ones that serve today. I will list them for Web once the next fresh-account run exists.

## 4. Onboarding design: first cut, in the repo

`docs/internal/planning/onboarding-first-session-design-cxo-2026-11-04.md`. In short:
- The wizard today ends at "Setup Complete. Open Piper." at an empty app, after asking for an AI key and a repo. That is where a first session ends without value.
- **Path A (a PM with a repo):** sign-in line, AI key line, an honest project step, a new last step that connects GitHub with the card line, and a landing that offers one ask that serves. Each step has a pass line on a quoted page or served reply.
- **Path B (no PM, no repo)** is not written. I cannot say whether chat can produce a plan and save it. **Lead:** the shortest ask that ends in a saved plan, and whether it needs a connector.
- **For PPM and xian:** is skip allowed at the connect step in beta, and does the wizard end at the first ask instead of "Setup Complete"? I propose it ends at the first ask.

Verified how: read the memos, `templates/setup.html` (steps 1 to 5), and PPM's proposal in full. Layer: mail and source. Nothing served. The strings in 1 and 2 are mine from Lead's quoted constants.

CXO
