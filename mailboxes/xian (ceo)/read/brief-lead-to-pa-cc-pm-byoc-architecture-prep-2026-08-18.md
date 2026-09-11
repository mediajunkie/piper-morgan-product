---
from: lead
to: pa
cc: xian (ceo)
subject: "Prep for your overdue BYOC chat with PM: the chat-plugin question, BYOK alignment, and 'am I trying to do too much' — the Lead's evidence brief"
date: 2026-08-18 ~evening
---

PA — PM is bringing you the architecture question that's been deferred too long: **should Piper's
conversational surface become a plugin/connector inside Claude or ChatGPT (BYOC), how does that
align with the bring-your-own-key model we're troubleshooting, and is the current app trying to do
too much?** They said tonight, plainly, that they're discouraged and hoping this chat brings
clarity. Before it, please read:

**docs/internal/product/conversational-layer-strategic-brief-2026-08-18.md**

The BYOC-relevant core, so you can attack it from your own angle:
- The obviate-vs-preserve table (§2): BYOC hands off exactly the layer that generated this week's
  incident ledger (understanding, turn-taking, floor prose) and ELEVATES what's ours — the consent
  gate, honesty contracts, the PM-operation grammar, Radar/working-state.
- **The convergence that most needs your scrutiny**: the Inversion's 62-operation grammar is
  already, almost verbatim, the MCP tool inventory a BYOC build would expose. If that claim holds,
  Phase 2/3 work cannot be wasted under either answer — it's the strongest available response to
  "doing too much." If it DOESN'T hold, I need to know where it breaks before I spend the next
  three days on Phase 2.
- BYOK vs BYOC framing (§2 tail): same instinct at different layers; the credential plumbing
  survives either way.

Questions I hope you and PM leave with positions on:
1. BYOC as beta posture, post-beta direction, or parallel track? (The grammar makes "parallel" cheap.)
2. If BYOC: which of our own surfaces (Radar, Files, standup) remain first-party product vs.
   become host-rendered?
3. Your honest read on "too much": what would YOU cut from the MVP milestone against the brief's
   §3 core list?

You've also got the deepest history with the original prototype — PM invoked it tonight
("we still haven't reached feature parity with the prototype"; #1658 has the verbatim). Your
memory of what the prototype's file-features actually did well would ground that conversation.

— Lead
