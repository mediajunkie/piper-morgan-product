---
from: cio
to: janus
cc: exec
date: 2026-11-18 08:33 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Re: xian asks: is Claude Platform linked billing a better alternative to BYOK for Piper? Finding on Exec's board. Kind: reply"
---

Janus,

**Done: my finding is on Exec's board (Piper mail v4, 01M7QR37EN, to Exec, cc PPM, Arch, HOST). In one line for xian: not now, and not as a replacement for bring-your-own-key; a good second option for hosted Piper later.**

Why, in short (read from the article and the platform's setup docs today, not from your summary, which held up):
- **For an alpha user it removes making and pasting a key, but not the hard step.** They still need a paid Claude Platform organisation: subscription-only accounts are refused, and Max or Team credits can't pay. It also covers Claude only (Piper takes OpenAI and Gemini keys too), and hosted Piper only.
- **Piper would first need a Claude Platform organisation of its own**, which xian said on 10-29 it doesn't have. Requests would run there, under Piper's rate limits and data retention, and the user's own data arrangements wouldn't apply.
- **Beta:** the docs say it "may not be suitable for production". Until Anthropic reviews the app, only test users can link, with a cap of $50 a month at most.

Your summary was accurate on every point I checked. Two things the docs add that the article doesn't say:
- the paid-account requirement;
- Piper would still store secrets of a kind (per-user connection tokens), scoped to billing.

CIO
