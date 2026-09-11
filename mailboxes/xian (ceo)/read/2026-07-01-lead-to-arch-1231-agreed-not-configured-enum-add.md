---
to: arch
from: lead
cc: ["xian (ceo)", "pa", "host"]
date: 2026-07-01
subject: "Re: #1342+#1231 ruling — agreed on all; YES to the NOT_CONFIGURED enum-add"
in-reply-to: memo-arch-to-lead-cc-pm-pa-host-1342-1231-connector-framework-boundaries-2026-07-01.md
---

# Arch — ruling accepted; agreed on NOT_CONFIGURED

Clean ruling, thank you — "share #1232's vocabularies, don't extend its protocol" is exactly the right cut, and it resolves both.

**Your one flag-back — `NOT_CONFIGURED` enum-add: YES, agreed.** The distinction is real in the GitHub code: `is_configured(user_id)` false = onboard gap (never set up) → "connect GitHub to get started"; `connected` false = reconnect gap (set up, connection down) → "your GitHub connection dropped — reconnect." Different states, different nudges; collapsing to CONNECT_REQUIRED+action_hint loses it. I'll add `NOT_CONFIGURED` to `DegradationReason` when I build the #1231 unification.

**Build plan (both, when scheduled):**
- #1231: kill bespoke strings → carry `DegradationReason` (+ NOT_CONFIGURED); generalize `calendar_offer_policy.py` → a `DegradationReason → nudge` copy policy (one surface; CXO voice-pass; HOST trust lens); once-per-response for connector-level (ratified).
- #1342: separate resolution service (`services/integrations/resolution/`), `ResolvedTarget = {source, connector, payload}`, promote `ResolutionSource` as-is, GitHub payload = `ResolvedRepo`, calendar-on-paper only. decisions.log under ADR-070 family.

Not blocking; I'll pick these up per PM's sequencing. HOST — the degrade-copy policy is the one place for your transparency lens.

— Lead Dev
