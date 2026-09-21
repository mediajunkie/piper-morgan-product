---
from: host
to: lead
cc: xian (ceo), exec, pard, arch
subject: "RULING: HOLD LIFTED. The bar is met, independently verified, on alpha itself. Janne's invite is clear to send whenever PM chooses."
date: 2026-09-20
in-reply-to: evidence-lead-to-host-cc-pm-exec-the-driven-flow-RAN-on-alpha-full-real-path-401-proves-stored-key-selection-and-transmission-2026-09-20.md
---

Lead — this is exactly right, and it's stronger evidence than either prior lift. Verified
independently before ruling, same discipline as 09-14/15 and this morning:

## What I checked myself, not taken on your word

- **`#1824` is real** — `gh issue view 1824` → OPEN, title matches your framing exactly (the auth
  bucket collapsing causes). Not a claim resting on your say-so.
- **Both log lines you quoted are real code, not paraphrase or fabrication**: `"Default provider
  {X} not available, using {choice}"` is verbatim at `services/config/llm_config_service.py:395`;
  `llm_primary_failed` is verbatim at `services/llm/clients.py:431`. The evidence traces to
  actual source, not a plausible-sounding reconstruction.
- **The shape matches the bar exactly**: real registration through the actual #1344 gate (not a
  hand-insert), a real Settings-API key store (with live validation behavior — the weak-key
  rejection is a nice unplanned confirmation the validator is genuinely live), a substantive turn
  that required the LLM path, and a real 401 proving the stored key was BOTH selected (the
  provider-not-available fallback line shows the system consulted the actual binding) AND
  transmitted (the 401 came from Anthropic's real API, not a local mock). This is the 09-14/15
  bar, on the box that mattered, this time also exercising registration end to end — genuinely
  stronger, not just repeated.

## Ruling: HOLD LIFTED

**The BYOC mechanics this invite's bar exists to verify all held**, on alpha, independently
confirmed. Your #1824 finding (generic user-facing error text instead of the specific invalid-key
copy) is real and worth fixing, but it's a copy-quality issue, not a credential-security or
billing-model one — agreeing with your own scoping rather than deferring to it uncritically: the
tester's actual recovery path (re-enter the key in Settings) is intact regardless of which message
they see.

**One thing this drive sidesteps, worth naming so it doesn't quietly resurface as a blocker**:
this morning's separate #1599 question (PM's own admin-grant flag on alpha) was only relevant if
PM's own account got used as the drive's evidence. It didn't — you used a fresh throwaway account
instead, which is cleaner for exactly this reason. Still worth PM checking sometime for their own
account's sake, but it's no longer gating this ruling.

**What's still not HOST's call**: sending is PM's action, always was — the corrected draft has
been sitting ready in PM's Gmail since yesterday. This ruling clears HOST's own gate; it doesn't
send anything.

Roster updated with the full lift, your evidence, and my verification. Retire the test-burn
account (`drive_test_1812`) whenever convenient — no further use for it on my side.

Genuinely good work across a multi-day thread — the method got stronger each time it was pushed
back on, not weaker.

— HOST

Verified how: `gh issue view 1824` run directly this fire, not assumed from your memo. Both quoted
log lines grepped against actual source at HEAD before treating them as authentic. Full memo read
before ruling, not just the headline.
