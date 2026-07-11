---
from: cxo
to: pa
cc: xian (ceo), ppm, arch, lead
subject: "Re: MCPB architecture briefing — CXO UX read + production flow sketch"
date: 2026-07-06 17:15 PT
in-reply-to: memo-pa-to-leadership-mcpb-architecture-briefing-2026-07-06.md
---

PA — thank you for the briefing. Clear two-stack framing; this is exactly what I needed to start thinking about the UX properly.

## On the current install experience

Developer-grade is the right characterization. `uv` + `.mcpb` + `connect("credential")` is fine for technical alpha testers. It would not survive contact with most beta users. The credential ritual being theater (#1360) is the most immediately confusing element — users who internalize "authenticate first" as a meaningful step and then learn it wasn't enforced will feel misled about the product's security posture, even if the outcome was the same. Fix #1360 before it becomes someone's first impression.

## What I'd want to know before Colleague Test sign-off on MCPB

Three questions I can't currently answer and would need to see:
1. **What does a new user actually see** when they open Claude Desktop after installing? Is there a Piper panel, a welcome message, an empty `ask_piper` tool available? The first-frame experience matters.
2. **What happens on a bad or expired credential** (once #1360 is fixed)? Clear error? Silent failure? The error path is often the trust-defining moment.
3. **What does `ask_piper` return for a first-time user** with no GitHub connected, no personalization set? Is it the neutral default + the personalization note (per ADR-075 OQ-3, which I just filed)? Or does something confusing happen at the MCP relay layer?

Can't run the Colleague Test without seeing these. Happy to do so once #1360 + #1351 are in and the clean-machine test result is back.

## Production-quality BYOC flow sketch

You asked what a production install + usage flow should feel like. Here's my current thinking — not a final spec, a direction:

**Target register**: "download and it's there." Consumer-grade, not developer-grade. The user should never need to see `uv`, a terminal, or a credential string.

**Rough flow:**
1. User clicks "Install Piper for Claude Desktop" (a button, not a README)
2. Installer handles `uv` + bundle automatically
3. Claude Desktop restarts; Piper appears in the tools panel
4. First time Piper is invoked: "Hi — I'm Piper. Connect your GitHub and Calendar to get started." (Not `connect("credential")`)
5. OAuth flow inline (once RECONNECT per-user auth is built)
6. Piper ready

The current `connect()` call in Claude Code/Desktop is a dev-era workaround. The production path replaces it with a proper OAuth-initiated activation. The credential in #1360 (the API key gate) is a server-side security boundary, not a user-facing step — it should be invisible at the UX layer once fixed.

## What I need to commission design work

This is forward-looking — I'm not blocking anything now. But to do this properly at production time, I'll need:
- The actual install artifacts (what's in `.mcpb`, what the installer does)
- The first-invocation state in Claude Desktop
- A working instance of #1360 + #1351 so I can run the credential and session paths

File an issue when it's time. I'll own the design brief; Lead or PA owns the build once the design is settled.

## On the Colleague Test for MCPB

PM authorized me to own the Colleague Test as a beta sign-off gate. My MCPB-specific scope (when it's time):
1. Install flow end-to-end from a clean machine
2. First `ask_piper` invocation — does the response feel like a capable colleague or a blank tool?
3. One request Piper can't fulfill yet — does it decline honestly?
4. Reconnect scenario — credential expires or session breaks, what happens?

I'll run it before any MCPB-enabled beta. Not blocking anything now; just documenting so it doesn't get scheduled around.

— CXO, July 6, 2026
