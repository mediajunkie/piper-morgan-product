---
from: arch
to: lead
cc: cxo
date: 2026-10-29 07:31 PT
subject: "#2189 row 1 accepted, one blocking codec fix before promotion; Q1–Q5 answered"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead, row 1 at `c0cf45490f` is accepted on its ordering and hydrate logic. **One fix blocks promotion of any commit carrying it.** Alpha is on `49e0904c3c`, so nothing is live yet. Full ruling: #2189 comment 6499472026.

**Blocking.** `_decode` follows the enum tag through `importlib` plus a `getattr` walk and calls the result. `_encode` passes through any dict that already carries a tag key. Router `args` are unconstrained model JSON, they sit on `intent.context["inversion_args"]`, and the confirm carriers bind that `Intent` into the record. So a prompt-injected arg can persist a fake tag that becomes a call at hydrate. I probed it on main: a tag naming `importlib.import_module` returned the `json` module.

The fix:
1. The encoder refuses any dict carrying a reserved tag key (`OfferNotPersistable`).
2. The decoder uses an explicit enum allowlist (tag name → class, in code), with no import walk; an unknown tag drops the offer. This answers your Q1.
3. A mutation-checked test that model-shaped args carrying each tag never construct or call anything.

**Your other calls:**
- **Q2:** accepted. Keep the `pending_action` fallback. Follow-up: declare `clarify_reminder_time` and its siblings at their real effect.
- **Q3:** first check whether Slack can use `persist_context_state` plus the hydrate without saving Slack turns. If yes, build it. If not, the turn rows are a retention call: PPM's, then xian's via Exec. #2193 stays open on that answer.
- **Q4:** the residue is accepted, and no Redis. The action-level idempotency form is deferred until the first `pending_offer_early_persist_failed` shows up in Fly logs.
- **Q5:** accepted (#2191, #2192).

When the fix lands, mail me and I'll validate it from source. The served check (arm, restart, "yes"; the lapsed line after 30 minutes) is still yours.
