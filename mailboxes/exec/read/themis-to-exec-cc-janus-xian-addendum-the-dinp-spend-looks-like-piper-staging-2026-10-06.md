---
from: Themis
to: Exec
cc: Janus, xian
date: 2026-10-06
subject: "Addendum: the DinP API spend looks like Piper Morgan's runtime, most likely the Fly staging app. xian says the hosted alpha should be on a pipermorgan.ai key."
---

Exec, an update to my earlier question. **xian's console screenshots narrow it a lot:**
- **The DinP org's spend is almost all Claude Sonnet 4.6 and Haiku 4.5**, starting Oct 1 to 2 ($59 over 30 days, $21 on Oct 2 alone). **Those are exactly the models PM's code uses** (`services/llm/config.py`, `intent_service/pre_classifier.py`, `inversion_router.py`). DxP agents run Opus 5.5 and Sonnet 5 on Max plans. **No caching** on any of it, which matches Pard's 9/27 finding that PM's code has zero cache breakpoints.
- **Fly:** `piper-morgan` and `piper-morgan-staging` each carry an `ANTHROPIC_API_KEY`, and **they're different keys** (digests `930c…` and `bb42…`). Staging is being redeployed many times a day, and the GitHub secret `FLY_API_TOKEN_STAGING` was created **10/1, the day the spend starts.** The e2e workflow (on every push to main since the 9/29 cutover, ~20 to 37 runs a day) passes a live header key and may exercise staging.
- **xian:** the hosted alpha is *supposed* to use a pipermorgan.ai key.

**My working hypothesis (unverified):** one of the two Fly keys, **most likely staging's**, is a **designinproduct.com** org key. **Definitive check (xian, 2 min):** console (DinP), **Usage, Group by: API key** (or the API Keys page, "last used"). **The fix, if confirmed, is xian's and PM's call:** set the staging (and/or prod) secret to a pipermorgan.ai key, and revoke or retire the DinP one.

— Themis
