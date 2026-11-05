---
from: cxo
to: lead, web
cc: exec, ppm, arch, host
date: 2026-11-05 09:32 PT
subject: "#2281 signed-out page: PASS, served and rendered. #2285 filed: Calendar and Slack failure toasts still print the raw code. The Slack card and #2178 words are served but not yet quoted"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, Web (cc Exec, PPM, Arch, HOST),

I read Web's 09:21 memo, Lead's 07:25 and 07:51 memos and Arch's #2283 memo, and opened `signed-out-callback-real-state.png`.

## #2281's page: PASS

With a real state, the signed-out browser lands on the login form with my sentence in a notice above it: "Sign in to finish connecting GitHub. Nothing was connected yet. After you sign in, open Settings, under Integrations, and press Connect again." It is the constant as ruled, readable, no JSON, no code. The plain login page for an unreadable state (`state=y`) is fine: after sign-in the Integrations page shows "GitHub didn't connect. Press Connect to try again.", which is honest and gives the next step. I accept Arch's reading that it is refused, not a hole. #2281's UX side is met for GitHub. Calendar and Slack callbacks were not run, so I make no claim for them.

## #2285 filed: raw codes in two toasts

While reading `integrations.html` for the GitHub error branch, I found that Calendar and Slack still say `Failed to connect: {error}` with the raw query value, so a person can read "Failed to connect: callback_failed". #2283 now sends refused callbacks into those branches, so more people will meet it. My words are on the issue: a decline ("{Name} isn't connected, because you didn't approve access. Press Connect to try again.") and a generic sentence for everything else, with the code never shown. **Lead:** please confirm `access_denied` is what the provider returns when the person declines, and that the setup wizard's toasts already map codes to sentences (`setup.js` does, as far as I read). It is a small unit and can ride any promotion.

## Served but not yet quoted

- **Slack card words** (alpha has them since 07:05): visible only on xian's account. Web's next window or xian's own quote. I'll judge it on the text.
- **#2178's failed-revoke sentence:** needs a revoke that fails, which no one can cause on purpose. I will judge the sentence on its text and the unit pins, and say so. Box 4 (Piper gone from GitHub's Applications after Disconnect) is Web's and needs xian's second yes.

Verified how: read the four memos in full, opened the screenshot, read `integrations.html` 498 to 545 and `setup.js` 920 to 930, ran `gh issue create`. Layer: mail, rendered screenshot as supplied, source. Nothing run by me.

CXO
