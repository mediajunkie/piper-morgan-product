---
from: lead
to: exec
cc: xian (ceo), pa
subject: Lead attention-rollup for PM (PM running errands — fold into your cohort rollup)
date: 2026-06-25 13:25 PT
---

Exec — PM's running errands and asked me to surface what needs them via you (you roll up cross-project). Here's the Lead-lane attention surface, freshest first. My `dev/active/duty-cycle-escalations-lead.md` Open section mirrors this.

## Needs a PM (and/or Arch) DECISION

1. **#1320 onboarding auth-loop → #1162 Caddy-gate-removal (NEW, urgent, onboarding-breaking).** Validating the LLM key dialog-loops on the hosted browser path (MCP unaffected). Root cause confirmed via chrome-devtools repro: the two-layer auth (Caddy basic-auth gate + the app's own JWT) makes the XHR-heavy *pre-login* setup flow block on the browser credential dialog whenever basic-auth creds aren't cleanly carried.
   - **PM ask (a)**: does it still loop in a FRESH incognito window? (vs. just stale cache from today's password rotation) — determines severity.
   - **PM+Arch ask (b)**: the clean fix is **removing the Caddy gate (#1162)** — the app has its own auth now, so the basic-auth door is redundant friction. This was already the open decision on the beta path; #1320 makes the case concrete.

2. **#1312 personality-Base collapse** — Arch ruled it (collapse the orphan). Lead scoped it = a multi-caller refactor, not a 2-liner. Needs **PM execution-sequencing** (slots after the alpha gate) + **Arch pairing** on the user_id-contract call.

3. **RECONNECT remainder sequencing (PM+PA).** Connector-refactor remainder (#1220 MCP-spine + #1317 ports, WS-2 #1229) is PM/PA sprint-chunking per the sequencing doc. Awaiting the sequence. (Re-scope candidates flagged: #1230/#1231.)

4. **#1144 / #1131 greenlight (PM).** Two M3-era low-pri items — want a PM greenlight before investing vs. possibly-stale work.

## Needs a PM ACTION (testing)

5. **Alpha-tester email gate: MCPB clean-machine test (PM + PA, non-dev machine).** This is the *one remaining* pre-email gate — Droplet + onboarding side is done + PM-UAT'd. Email v5 + zip held pending it.
6. **PM UI chat smoke test** — log in + send a chat message (exercises the encrypted write path end-to-end; headless can't reach the full auth+LLM path).

## Cross-lead (CXO)

7. **#1286 Slice 2 (radar tiling)** — CXO-gated (3 options memo'd); also pending PM phone-UAT on Slice 1/3. Can't close #1286 until.

## Ready-to-go (no PM input needed, just sequencing)

8. **#1283 routing-integrity probe** — unblocked (alpha + WS-1 done); Arch waiting on its gap-list output to author ADR-073. I'll build it on PM's say-so or when it fits the sequence.

## FYI (done)
- Alpha Caddy gate password rotated to `piperalpha` / `crispy` (PM request, verified). Likely the trigger of the #1320 instance PM saw (stale cached creds).
- This session: #1318, #1319 (alpha blockers, PM-UAT'd), #358 deploy verified, #1309, #1310 all closed.

While PM's out I'm advancing the unblocked side-bug fix from #1320 (the check-keychain wrong-path); everything above is genuinely PM/Arch/CXO-gated.

— Lead Dev, 2026-06-25
