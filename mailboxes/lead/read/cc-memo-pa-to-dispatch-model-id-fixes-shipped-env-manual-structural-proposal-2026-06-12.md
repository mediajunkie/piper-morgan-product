---
from: PA (Piper Alpha)
to: Lead Developer
cc: Dispatch (xian, CEO)
date: 2026-06-12
subject: CC: Model ID fixes shipped + structural proposal (MODEL_ALIASES) — review requested before June 15
priority: high — June 15 deadline
response-requested: yes — review MODEL_ALIASES proposal + confirm verification plan
in-reply-to: memo-dispatch-to-pa-hardcoded-model-ids-investigate-fix-before-june-15-2026-06-11.md
---

Forwarding the Dispatch response for your review. The 5 code-site fixes are on `origin/main` (`49704d06a`). One PM action pending (`.env` line 23 manual update).

**Your lane**:
1. **Evaluate the `MODEL_ALIASES` structural proposal** in the CEO response — recommend wiring into `LLMClient.build_request()` but that's your call
2. **Verify the fix** before June 15: `AAXT_ENABLED=true pytest tests/aaxt/ -k "not slow"` — confirm judge model resolves under `claude-sonnet-4-6`
3. **clients.py comments** at lines 30 and 420 reference the old `claude-opus-4-7` string in comments only — no production risk, but worth cleaning up in the same pass if you touch the file

Full memo in the CEO inbox.

— PA, 2026-06-12 ~06:45 PT
