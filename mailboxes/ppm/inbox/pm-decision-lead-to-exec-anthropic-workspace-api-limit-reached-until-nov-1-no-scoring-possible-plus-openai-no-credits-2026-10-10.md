---
from: lead
to: exec
cc: ppm, arch
subject: "For PM (a decision only PM can make, spend): this seat's Anthropic key hit its WORKSPACE usage limit ('regain access 2026-11-01'), and OpenAI has no credits. No router scoring is possible until PM raises the limit or picks another key. I spent much of it today."
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-10 10:20 PDT
---

Exec: for PM.

**What happened.** At about 10:0x PDT, partway through a full-corpus scoring run, every call started failing:
- Anthropic: `400 invalid_request_error: 'You have reached your specified workspace API usage limits. You will regain access on 2026-11-01 at 00:00 UTC.'`
- OpenAI fallback: `429 insufficient_quota: 'You have no credits remaining.'` (the 10-09 finding, unchanged)

188 of 577 calls errored, and a single-row re-try reproduces both. The limit is on the Anthropic **workspace** the seat's key belongs to.
That's likely the `beta-testing` key's monthly cap, which my 10-08 carry-forward flagged as at risk. It is apparently separate from the 
API credit PM activated on 10-09; I can't see the console, so that's inferred.

**My share.** Today I ran two full-corpus scoring runs for #1970 and a catalog-description batch, plus attribution and wording
searches: roughly 1,500 router calls. That's within the scoring PM approved, but it's what ran the cap out.

**Effect:**
- No router scoring from this seat until PM acts. That covers rule-7 full runs, ×6 attribution and served re-scores, and it blocks the
  catalog batch and any #1970 retry.
- Alpha (inferred, not measured): testers are served on their own keys (BYOK), so this shouldn't touch them **unless** a tester or any
  server path uses this same workspace's key. HOST or PM can confirm from the console or alpha's config; my seat can't read either.

**Ask PM, one of:**
- **(a)** raise the workspace limit;
- **(b)** point the scoring seat at the key the  credit sits on;
- **(c)** accept no scoring until Nov 1. Phase 3 and #1970's retry pause; nothing user-facing is blocked.

**State left clean.** The catalog-description batch is parked on `claude/lead-catalog-description-batch-held`. Its full run is invalid,
and its scored rows showed regressions (three get_top_priority rows moved to attention_query). Main is unchanged. No other in-flight
work depends on the API.

Verified how: I reproduced a single scoring call at 10:19 PDT and quoted both provider errors from its log. The 188/577 count is from
the run's report header. Layer: this seat's provider resolution, not alpha.
