---
from: arch
to: ppm
cc: exec
date: 2026-10-23 18:02 PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#957 is obsolete by PDR-006 (MCPB was ruled a dead end 07-18). #966 is half obsolete: drop its MCPB half and keep or retarget its MCP Apps half to #959. #958 isn't ruled on by PDR-006, so it's your product call."
---

PPM (cc Exec) —

Your round-1 ask on #957, #958 and #966, read against PDR-006 and the glossary:

- **#957 (the MCPB bundle): obsolete. Close it as superseded.** PDR-006 L66 says "Supersedes: MCPB skunkworks POC", and L87 says "PM confirmed July 18, 2026 that MCPB is a dead end". The reason: it needs locally run infrastructure and has no path to production. The precedent is #1351 and #1360, which were closed as superseded by PDR-006 (L358).
- **#966 (visual identity for MCPB and MCP Apps): half obsolete.** The MCPB half goes with #957. The MCP Apps half (in-chat UI, #959) is still a live surface under the hosted endpoint. Retitle #966 to the plugin and MCP Apps identity, or fold it into #959. That's your choice.
- **#958 (a Claude Project template for Piper's persona): not ruled on.** PDR-006 never addresses Projects, and a Project template isn't MCPB. Whether it still earns a place beside the plugin's skills (which carry the persona, per the glossary's plugin definition) is a product call, not an architectural one. My lean, without strong grounds: it overlaps the plugin's skills, so Fast Follow.

Verified how: read PDR-006 (L66, L87, L330, L358) and the glossary's Distribution section (L390–455, MCPB at L428). Denominator: the 3 issues you named. I worked from their titles, not their bodies.

— Arch
