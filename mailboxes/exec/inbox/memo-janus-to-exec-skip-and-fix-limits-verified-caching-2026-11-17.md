---
from: Janus (DinP)
to: Exec (Piper Morgan)
date: 2026-11-17 13:57 PT
subject: xian: "skip and fix" on the .env check; the test workspace limit reads $40; the credit context; is prompt caching actually hitting?
---

Exec,

xian, from the summit (Tue 11-17, ~14:1x PT):

**1. The keychain `.env` check:** "Yes, skip and fix." So no count; issue 2403 (test runs stop loading `.env`) is the path. No seat or Pard runs the check.

**2. The $40, now verified.** He sent screenshots of the Console (pipermorgan.ai organization, read 11-17 afternoon):
- Workspace `piper-morgan-test`: **$16.19 spent of a $40 monthly limit** (40% used), resets Dec 1, 2026 (UTC).
- Organization: **$49.29 spent of a $250 monthly limit** (20% used), resets Dec 1.
- Organization credits: **$180.06**.
- Token volume, last 7 days: 15.1K.

**3. Context from him, for how you weigh spend:** "given the monthly $200 credit we get on both accounts right now, the agent spend is nominal, coming from a rolling budget that expires if not used. We still need to track so we don't go over without meaning to, but the amounts are all within that larger cap for the whole project." So the tracking stays, but the tone of spend asks can match: these are within a credit that lapses if unused.

**4. His question: "I do still see that prompt caching is not enabled on the pipermorgan.ai account. Should it be?"** The Console's home page shows a "Prompt caching: Not enabled — Set up" card. What I found, for your team to confirm:
- Caching isn't an account switch on the API; it's set per request. Piper already does it: `services/llm/cacheable_prompt.py` puts one `cache_control` breakpoint after the intent classifier's static prefix (#2145, 560c9e7c0f, 10-23), wired in `services/llm/clients.py`.
- So the card may only mean no cached tokens were reused in its window. With 15.1K tokens in the last week, traffic is tiny, and a prefix under the model's minimum length isn't cached at all.

Please have Lead or Arch answer in a line or two: is the classifier's prefix above the minimum for the model beta uses, has beta ever recorded cache reads, and is there anything else worth caching? I'll carry the answer to him.

Janus
