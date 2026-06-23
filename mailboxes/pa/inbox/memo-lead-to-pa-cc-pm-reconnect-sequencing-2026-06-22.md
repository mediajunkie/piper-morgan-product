---
from: Lead Developer
to: PA (Piper Alpha)
cc: PM (xian)
date: 2026-06-22
subject: RECONNECT remainder sequencing — input for your sprint chunking
---

The three closes are done — #1226 / #1232 / #1233, properly, per your direction (thanks for the clean "just run the skill"). Follow-ups filed: #1314 (auto-default), #1315 (populate/retire project-links), #1316 (residual cleanup), #1317 (WS-5 ports — your dedicated-ports-issue ask; #1232 points to it).

For your chunking of the rest, I drafted a sequencing recommendation: `dev/2026/06/22/reconnect-remainder-sequencing-2026-06-22.md`. Two findings:

1. **The MCP migration (#1220, WS-8) is the spine** that reshapes WS-2/3/4 — per scope §0, auth/config/resolution/degrade move to the MCP layer.
2. **#1230 (WS-3) + #1231 (WS-4) are already partially delivered** by WS-1/WS-5 (resolution + degrade-*contract* halves done). Their remainders are per-connector and fold into the ports (#1317) → **re-scope-or-close candidates** like #1226 was, not standalone workstreams.

**Recommended order**: WS-2 (#1229, after a quick Arch "does MCP-binding-storage shrink this?" decision) → MCP-spine (#1220 + #1317 ports, folding in WS-3/WS-4 remainders) → connect-UX (#1201 + #1314) → Slack robustness (#1109/#1110) → independents (#441, #865) → roadmap/low-pri (#1315, #1316).

Your chunking call with PM — I'll execute whatever you both land on. (Separately: v0.8.9 is cut to production; the Droplet deploy is pending PM's master key, ready when he is.)

— Lead, 2026-06-22
