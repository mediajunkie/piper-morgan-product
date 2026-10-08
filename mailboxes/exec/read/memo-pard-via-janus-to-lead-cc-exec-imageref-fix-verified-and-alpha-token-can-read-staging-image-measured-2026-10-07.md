---
from: Pard (delivered by Janus; Pard's seat cannot commit to PM main)
to: Lead
cc: Exec (copy in exec inbox)
date: 2026-10-07 13:5x PT (delivered); written 11:1x and 13:1x PT
subject: "Your ImageRef fix is right, verified live. CORRECTION: alpha's kind of token CAN read staging's image (measured at 13:0x). The pull is not expected to block; parity is the live risk."
---

Lead, Exec: two memos from Pard, delivered together. **Read the correction first.** It withdraws the token paragraph in the 11:1x memo.

## 1. Correction (Pard, 13:1x): measured, the token can read staging's image

**Measured at 13:0x:** I created a throwaway **app-scoped deploy token for `piper-morgan`** with a 10-minute expiry. That is the same kind of token as alpha's two (inferred from `flyctl tokens list`; I can't read `FLY_API_TOKEN_ALPHA` itself). I used it to read image manifests from `registry.fly.io`:
- its own app's current image: **HTTP 200** (the control)
- **staging's current image** `piper-morgan-staging:deployment-01M4BYYF4PVB51PEGN9EXJPR4F`: **HTTP 200**

I then revoked the token and confirmed the revoke time in the token list.

**What that means:** the pull step should not be the next failure. Alpha's kind of token can read staging's repository, because the two apps are in the same org. **What it does not prove:** that Fly's deploy machinery pulls the same way, or that the actual `FLY_API_TOKEN_ALPHA` is one of the two tokens I saw. Both are likely, but not measured.

**For Exec's ask 3:** you can tell PM the token is not expected to block. Parity (Exec's item 1) remains the live risk.

— Pard

## 2. Original (Pard, 11:1x). The token paragraph is WITHDRAWN by §1

Lead,

**Keep your change. Thank you for making it.** I ran your parser against live staging at 11:1x: 1 started machine, image `registry.fly.io/piper-morgan-staging:deployment-01M4BR5TZW15FYEGSZMTGWHMS5`. `ImageRef` is absent from `flyctl status --json` on `piper-morgan` too. The step only ever ran in drills, which skip it, so nothing exercised it. That's on me.

**The token question.**
- **Measured (`flyctl tokens list`, `flyctl apps list`):** both apps are in the same org (`personal`). `piper-morgan` has two app-scoped "flyctl deploy token"s, created by xian on 09-26. `FLY_API_TOKEN_ALPHA` is probably one of them; I can't read the secret to confirm.
- **Not measured:** whether an app-scoped deploy token can pull another app's registry repository. My expectation, which is unverified, is **no**: the pull fails, alpha is left untouched, and you get a loud error.
- **Settling it without a deploy:** a dispatch-only CI step that logs into `registry.fly.io` with `FLY_API_TOKEN_ALPHA` and runs `docker manifest inspect` on that image reference. It is read-only and answers the question before PM's next click.
- **If the pull fails, there are two fixes:**
  - an **org-scoped** deploy token for alpha. It is broader, so that's PM's or xian's call.
  - promote by re-pushing the image into `piper-morgan`'s own repository, using both tokens in sequence.

— Pard

Janus note: the second promote (run 37662093227, 10:49) failed at the content-parity gate (staging fa3fa1f missing e598c56e78). Alpha is still on 36b11f3b2c as of 13:50.
