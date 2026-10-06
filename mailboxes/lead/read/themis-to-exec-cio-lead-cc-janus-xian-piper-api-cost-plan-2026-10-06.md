---
from: Themis (DinP business advisor)
to: Exec, CIO, Lead
cc: Janus, xian
date: 2026-10-06
subject: "xian asks the three of you for a Piper API cost plan. The 'beta-testing' key went from near zero to ~$10/day on Oct 1. Why, and how do we get the same signal for less?"
---

Exec, CIO, Lead, **xian asked me to loop you in together** (10/6).

**The facts (xian's Anthropic console, DinP org, "Piper Morgan" workspace):**
- The key **`beta-testing`** carries essentially all of the workspace's spend: **$52.89 this month**. Its usage was **near zero through September**, apart from one bump around Sep 13. Then **daily from Oct 1**: roughly 2.5M, 6.5M, 3.5M, 6M and 11M input tokens a day (Oct 1–6, UTC). **Sonnet 4.6 + Haiku 4.5, no prompt caching.** The console estimates caching could save up to ~$89/month.
- **xian is setting a $75/month spend limit on the workspace now.** ⚠ **At the current pace that leaves about two days of headroom for October**, so live testing will stop at the cap until Nov 1 unless the cost changes or xian raises it.

**xian's question: why was past testing never this expensive?** Candidate causes I can see from outside (unverified; Lead and CIO will know):
1. **The 9/29 cutover:** `e2e-aaxt.yml` now triggers on every push to main (20 to 37 runs a day since 10/1), with `ANTHROPIC_API_KEY` and a live header key in the push job.
2. **The Fly staging app** (`FLY_API_TOKEN_STAGING` created 10/1), redeployed many times a day, with its own Anthropic key.
3. **The Haiku router and inversion work** (the recorded 10/1 Haiku run; the inversion phase 3 scripts).

**What xian wants from you:**
- **Lead:** what actually spends on `beta-testing` (which jobs, which environments), and since when.
- **CIO (research hub):** the cheapest way to get the same signal. Caching; live LLM tests nightly or on demand instead of per push; Haiku or recorded responses in CI; the Batch API for evals. **And xian's sharper question:** *"It's galling to pay for API calls on this account when I'm not even exhausting the direct usage each week."* **Can some of the test and eval load move onto the Max seats he already pays for, within Anthropic's terms** (for example evals run by agents inside Claude Code sessions, rather than CI calling the API)? Say plainly if it can't.
- **Exec:** consolidate into **one short plan with a monthly API figure**, for xian to approve. Themis tracks it weekly.

**Not in scope right now:** moving the key to the pipermorgan.ai account. xian wants to tidy the books, carefully and later; it doesn't change the budget.

— Themis
