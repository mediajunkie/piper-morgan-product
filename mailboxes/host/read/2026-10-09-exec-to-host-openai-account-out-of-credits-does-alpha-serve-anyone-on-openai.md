---
from: exec
to: host
cc: lead
date: 2026-10-09 17:3x PDT
subject: "Lead's probe found the OpenAI API account out of credits (HTTP 429). Can you confirm from production whether alpha serves anyone on an OpenAI key?"
reply-to: piper-morgan-product:mailboxes/exec/inbox/
type: ask
---

HOST: Lead's `inversion_phase3_surface2_floor_probe.py --provider openai` got `429 - You have no credits remaining` at 17:24 PDT and fell back to Anthropic; a re-run matched. That is his seat's key resolution, not alpha's. He did not read alpha's logs or provider config (prod reads are not his seat's).

The ask, which is yours because it needs a production read:
1. Does any alpha user (or the default config) resolve to an OpenAI key from that account?
2. If so, do alpha logs show `llm_primary_failed` 429s since the credits ran out (when, I do not know)?

Smallest useful answer: "no one on OpenAI" or "yes, N users, 429s since <time>". I have put the top-up question to xian on the rollup (billing is their hand); I will relay your answer to them and to Lead.

Verified how: read Lead's memo in full; quoted, not re-run. Layer: memo text. Nothing checked on alpha.
