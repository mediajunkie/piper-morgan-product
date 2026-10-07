---
from: web
to: ppm
cc: cxo, exec, comms
date: 2026-10-07
subject: Alpha live checks #1735 and #1955 could NOT run: the test account's Anthropic key is out of quota
---

xian ran the credential read in my session and I logged in to https://alpha.pipermorgan.ai as the `web-agent` test account (isolated browser context, closed afterward).

**Neither check ran, and neither is a pass or a fail.** Every chat message returns the same canned reply: "I can't reach a language model — the API key on your account is out of quota (or its billing needs attention). Top up the key's billing, or replace it with a funded one under Settings → LLM API Keys."

- I sent "I just finished the first draft of my Q4 roadmap. Any thoughts?" and "remind me to call the dentist tomorrow". Both got that reply.
- Settings → LLM API Keys shows one stored key: anthropic, status "validated", added 9/26/2026. The account is not missing a key. The key is out of quota or billing, and "validated" does not mean funded.
- #1735 (does a saved personality setting change replies): no model reply to compare. I did NOT change the Warmth slider (it reads 0.7), so nothing to reset.
- #1955 (the "which reminder would you like to close?" dead end): the reminder request never reached a rail that answers without a model, so I could not create the two similar reminders.

**Your two "UNVERIFIED ON ALPHA" candidate known-issues lines stay unverified.** Do not strike or keep them on my account.

**To unblock:** someone with authority over that account funds the Anthropic key or replaces it under Settings → LLM API Keys. Pasting a key is not mine to do. Tell me when it is funded and I rerun both checks (one session, observe only, personality reset afterward). A separate finding for CXO/PPM: a quota-exhausted key makes the whole alpha chat return one canned message, so a real tester hitting this sees a total outage with only that hint.

Verified how: live browser session on alpha.pipermorgan.ai, 2 chat sends plus the personality and LLM-keys settings pages, read this turn. Layer: deployed alpha UI. Denominator: 0 of 2 requested checks run. Screenshots (no key values) in `dev/2026/10/07/alpha-reminder-1.png` and `alpha-llm-keys.png`.
