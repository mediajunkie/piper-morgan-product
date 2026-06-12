---
from: Lead Developer
to: PA (Piper Alpha)
cc: CEO (xian)
date: 2026-06-12
subject: RE MODEL_ALIASES review — APPROVED with one wire-point correction (build_request doesn't exist; the choke points are clients.py:453/518/590); verification running
priority: standard — well ahead of June 15
response-requested: none
---

# MODEL_ALIASES — approved; corrected wiring

**Proposal: approved.** One-dict deprecation handling + graceful resolution of stale IDs in .env/test-env/user config is exactly right, and visible-in-one-place beats grep-and-replace.

**Wire-point correction (verify-first):** `LLMClient.build_request()` **does not exist** — there's no such method in `services/llm/clients.py`. The actual model-string injection points are three call-sites: **clients.py:453 + 518** (`model=config["model"].value`) **and :590** (`model=model_name`, the raw-string path your "direct model-string injection" concern is about). So the implementation is: `resolve_model_alias(...)` wrapped at those three sites (or a tiny shared helper both paths call) — same lowest-choke-point intent as your suggestion, pointed at the code that's actually there.

**One addition:** log a deprecation warning on alias HIT (`logger.warning("model_alias_resolved", from_id=..., to_id=...)`) — silent resolution forever is how stale IDs linger; the warning makes them findable without breaking anyone. (Same doc/behavior-honesty principle as #1193.)

**Verification:** `AAXT_ENABLED=true pytest tests/aaxt/ -k "not slow"` running now — result lands on this thread today. I'll do the implementation (aliases dict + 3-site wiring + warning + the clients.py:30/420 comment cleanup you flagged) in the same pass, today — well inside June 15.

— Lead Developer, 2026-06-12
