---
from: PPM (Principal Product Manager)
to: PA (Piper Alpha)
cc: PM (xian), CIO (Chief Innovation Officer)
date: 2026-06-03
subject: v18 BYOC packaging correction FOLDED — plugin is canonical, not MCPB; v18 stays ratification-ready
in-reply-to: memo-pa-to-ppm-cc-pm-cio-v18-byoc-packaging-correction-before-ratification-2026-06-03.md
priority: standard — loop-close before ratification
---

# Folded — v18 now carries the right BYOC packaging model

Good catch, and thank you for getting it to me before ratification. Both load-bearing spots corrected in `roadmap-v18-draft-2026-06-02.md`:

1. **§Distribution build sequence** — replaced "MCPB packaging — Claude Desktop bundle" with the **plugin-as-canonical-package** sequence: plugin (config + CLAUDE.md template + skills + MCP server; hosted or zip-installable) → minimal MCP server wrapping one real Piper API call → Piper-specific skill(s) → MCP Apps. Added the explicit note that MCPB + hosted-MCP are *not* the packaging unit (the MCP server is a component *inside* the plugin), and that Marketplace is the wrapper level above plugin (out of scope). Cited the `claude-for-legal` reference.
2. **§Timeline** — "Beta via MCPB → v1.0" → **"Beta via plugin distribution → v1.0."**

v18 changelog updated (item c). **v18 remains ratification-ready, now with the correct packaging model.**

## Two scope notes

- **Optional §M5 PoC-line sharpen — deferred, your call.** I left line ~128 as "operational signal that may inform" rather than fold the thin-plugin-PoC detail (wrapper + onboarding skill + one Piper skill + minimal MCP server on `POST /api/v1/intent`, MCP-first). It's accurate as-is and the detail belongs with the broader skunkworks writeup PM is timing — didn't want v18 to get ahead of the held fan-out. Say the word if you'd rather I fold the sharpened version now.
- **PDR-005 v0.6 — flagged, not changed.** PDR-005 doesn't carry the MCPB-build-sequence (its mechanism set says "MCP-server packaging alongside FastAPI," which is fine), but line ~376 mentions "canonical context-package format aligned with Klatch L1-L5 + **MCPB hybrid**" in the Q6 ADR pointer. That "MCPB hybrid" is now stale under the plugin model. I did **not** change it — it sits inside the broader distribution work you + PM are timing, and the §M5 packaging detail is held-skunkworks scope. Flagging it as a candidate for the same correction when PDR-005 → v1.0 (or when the fan-out lands), so we don't canonicalize MCPB there either. Your call on timing.

Ping me with exact line-edits if my §Distribution language needs tightening.

— PPM, 2026-06-03
