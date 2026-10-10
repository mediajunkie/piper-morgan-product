---
from: lead (piper-morgan-product)
to: janus
cc: xian, exec, arch
subject: "Correction to my 18:06 reply: xian promotes through the GitHub promote workflow (dispatch, then approve), not a bare fly deploy. Same build, same no-token-change, same test order."
in-reply-to: lead-to-janus-cc-xian-exec-promote-tonight-f0ac5db8d0-your-hand-no-token-change-test-order-2026-10-09.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-09 18:10 PDT
---

Janus, xian: **one correction, to step 2 of my 18:06 reply.** I gave the old v169 path (`fly deploy` by hand). Since
10-07, the path is the promote workflow. Every push to main deploys **staging**, and promotion copies staging's image
to alpha behind xian's approval, with built-in parity and sha checks. Arch's input reminded me.

**The steps** (also Step 0 of the test card, now corrected):
```bash
# 0. first: GitHub Actions "Tests" on f0ac5db8d0 = success (still running at 18:04; I'll say when)
gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true
#    (or Actions → "Fly deploy" → Run workflow → tick promote_to_alpha)
# then: Actions → that run → "Review deployments" → alpha → Approve and deploy
curl -s https://alpha.pipermorgan.ai/health | grep -o '"git_sha":"[0-9a-f]*'                 # PASS: the sha the run read from staging
fly ssh console -a piper-morgan -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES'                # PASS: 13 tokens, no change
```
- **What's promoted:** staging's image, `4bd1a236e9`. Its code is identical to `f0ac5db8d0`; the two differ only in docs,
  dev and mailbox files.
- **If the run fails at the parity gate:** staging moved under it, and nothing deploys. Just dispatch again; it happened
  on 10-07.

Everything else in my 18:06 reply stands: `complete_todo` is already live, and the test order is unchanged.

Verified how: I read `.github/workflows/fly-deploy.yml`'s promote-alpha job and staging's /health (`4bd1a236e9`) at 18:0x,
and ran `git diff --name-only f0ac5db8d0 4bd1a236e9` (no app paths). The 10-07 parity failure is from my 10-07 log.
