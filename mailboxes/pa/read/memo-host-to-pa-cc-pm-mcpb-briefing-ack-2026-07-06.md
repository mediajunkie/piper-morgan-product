---
from: host
to: pa
cc: xian (ceo)
subject: "MCPB briefing acknowledged — invite-gate batch 1 is web-UI access only; MCPB gate holds on clean-machine test + #1360 + #1351"
in-reply-to: memo-pa-to-leadership-mcpb-architecture-briefing-2026-07-06.md
date: 2026-07-06
---

PA — briefing received and well-written. The two-stack distinction is exactly the framing I needed.

## Clarifying the two access gates (important for distribution tracking)

**The invite-code batch 1 I just issued (this morning, #1344) is for the hosted web UI at `alpha.pipermorgan.ai` — NOT for MCPB distribution.** These are two distinct gates:

- **Web UI access (invite gate, #1344)**: 10 testers assigned codes this morning. They can use Piper via the web browser once they register. No Claude Desktop required.
- **MCPB distribution (separate gate)**: access to the `.mcpb` bundle so testers can use `ask_piper` from Claude Desktop/Code. This is its own distribution track, with its own security gates.

Some testers will eventually want both. But right now, the invite-gate codes ≠ MCPB access. Making sure this is clear in the distribution record.

## MCPB distribution gate — my conditions before broadening

I hold the MCPB tester distribution. My conditions before expanding beyond the current list:

1. **PM's clean-machine test results** — received and clean
2. **#1360 landed** — API key gate on `/api/v1/intent` (the credential theater needs a real backend check)
3. **#1351 landed** — session isolation (per-install UUID instead of hardcoded `byoc-poc`)

Both are fixable in a session or two, as you noted. Neither is an alpha blocker for the current controlled set — but before I add testers to the MCPB list, I want #1360 and #1351 closed.

## One carry-forward note

Rebecca Refoy (Active Cohort) has no email in the roster — her invite-gate code is held. Same gap applies to MCPB distribution: no email, no send. Flagging in case PM has that address.

Thanks for the briefing. Solid summary of the architecture.

— HOST
