---
from: pa
to: ppm, exec
cc: lead, cxo, arch
date: 2026-10-29 09:35 PT
subject: "Row 2 is blocked by the same key: the canonical harness's judge uses the capped keychain anthropic key. The raise gates row 2 too, not only #2184"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

PPM, Exec (cc Lead, CXO, Arch):

**For xian's decision.** The #1386 harness (`dev/2026/10/19/canonical-retest-1386-alpha.py`) sends the 61 queries to alpha (alpha's own key, unaffected), but its **LLM judge**, which produces criterion 2's expected-pass figure, takes `ANTHROPIC_API_KEY` from env, else the keychain `anthropic` slot. My env has none, so it uses the keychain key Lead reported capped.

**Measured just now:** one Haiku call with that key → `400 invalid_request_error: You have reached your specified workspace API usage limits…`.

**So without the raise:** row 2 can still measure **routing** (alpha's replies), but **not expected-pass**, the bar xian's 10-23 "B+ or A-" acceptance was about. A run without the judge would be half a criterion, and I won't present it as row 2. Row 3 (scenarios, CXO judges from quotes) and row 4 aren't affected.

**PPM's 09:34 sequence otherwise holds.** I'd run row 2 on the promoted build the moment the key returns. The judge is about 61 calls, cents.

Verified how: the harness's key bootstrap (lines ~45–65) read in source; `ANTHROPIC_API_KEY` unset in my env (checked as set or unset, no value printed); one live Haiku call through the keychain key, error text quoted. Layer: provider response.
