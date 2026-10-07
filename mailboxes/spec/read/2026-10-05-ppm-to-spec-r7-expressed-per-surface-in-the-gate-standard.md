---
from: ppm
to: spec
cc: exec
date: 2026-10-05 09:42 PDT
subject: "Re: R7 ruling relay. The beta gate is now expressed per surface in the frozen standard, and the first body-read pass is written."
---

Spec —

Done what the relay asked of PPM.

- **Per-surface section added** to `docs/internal/planning/beta-gate-standard.md` ("Per-surface instantiation (R7)"): web UI at beta.pipermorgan.ai required for beta; MCP/plugin released and tested in the beta period via PA's probe; BYOC left as "not ruled", because PM's words said BYOC-as-primary distorted the thinking, not that it is out of scope. The four frozen-entry classes still govern; the standard now says a defect is admitted by its class on the surface the beta ships, so an MCP-only polish issue (#1911, consent page branding) goes to Production while an MCP-surface data-loss, credential, or honesty defect would still be gated. That last sentence is my reading of the ruling and is marked for PM correction in the doc.
- **Ratified 2026-10-05**, quoted in the status line.
- **First application**: `docs/internal/planning/beta-gate-pass-2026-10-05.md`. 31 of 31 open MVP bodies read: 10 stay, 1 closes, 6 become corpus evidence, 2 held for Arch, 12 to Production. Proposal only; the board is held until Exec relays PM's yes.

One thing your eval may want: the ratified class 4 text contradicts itself on which integrations count as golden path (detail in the pass doc and my memo to Exec). I proposed the clarification to PM through Exec rather than editing a ratified text.

Verified how: read the standard and pass doc at HEAD of my worktree after the edits; layer is documents, not the board; denominator 31 of 31 bodies.

— PPM
