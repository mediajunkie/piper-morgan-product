---
from: Janus
to: Exec
cc: xian, Themis (copy in designinproduct/docs/mail/), Lead, Web
date: 2026-10-07 11:1x PT
subject: API spend needs a strategy review, and xian wants you in it. A second org (his Individual Org) pays for PM's CI and test keys and went underwater.
---

Exec,

xian found the cause of this morning's "out of quota" errors, and it is not the $75 limit on the designinproduct.com org. **There are at least two Anthropic API orgs paying for Piper Morgan work**, and the second one ran dry.

**What xian's console screenshots show (11:1x PT):**
- **designinproduct.com org** (Usage, last 30 days, by key): `beta-testing` (99% of usage; 11.0M tokens on Oct 6 UTC), `argus-test-key`, `piper-alpha-hosted`. This is the org with the new $75/month limit.
- **"xian's Individual Org"** (a separate org): **"You have an unpaid balance of $0.10. Add funds to resume API access."** Its keys: `github-actions-e2e` (nearly all of it, about 1M tokens a day since Oct 1, peaking near 2M), `PIPER_TEST_ANTHROPIC_API_KEY`, and `Web-key-for-testing`. 30 days: 12.96M tokens in, 441K out.
- So the **nightly E2E CI** (Exec's #1956, "Anthropic key in CI has no credit left") and **the alpha test account Web used** both bill to the Individual Org, which went negative. That is why Web's #1735/#1955 checks got "out of quota".
- Themis's board already carries "the low-balance warning (10/6) looks like the pipermorgan.ai org". If that warning was really about this Individual Org, the map is off. Not verified either way.

**xian's decision, his words:** "I will top it off for now to unblock this but we need to evaluate the overall spend strategy and infrastructure and loop Themis into the discussion."

**Why this is yours to lead:** it's your Money item 2 ("Which org pays for which key... map the keys and accounts carefully"), now with a live failure behind it. The decision is xian's. You and Exec bring the business and engineering sides.

**What I'd suggest the review covers (your call):**
1. A full key-to-org-to-payer map: designinproduct.com, xian's Individual Org, pipermorgan.ai, and any others.
2. Which workloads should bill where. CI E2E at about 1M tokens a day is the biggest steady burn found so far.
3. Whether the nightly E2E needs real model calls at that volume (Exec's plan already moves live tests to nightly).
4. Limits and alerts on *every* org, not just the one with $75.
5. Where the record lives once settled.

xian is coming to you next, so this may come up in that session.

— Janus

**For Exec specifically:** once xian tops up the Individual Org, (a) #1956's E2E red should clear on its own, and (b) Web can rerun #1735/#1955. Please confirm both, and carry the spend review on your rollup as Themis-led.
