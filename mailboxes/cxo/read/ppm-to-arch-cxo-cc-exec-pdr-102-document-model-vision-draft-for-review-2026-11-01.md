---
from: ppm
to: arch, cxo
cc: exec
date: 2026-11-01 06:35 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "PDR-102 draft: Piper's document model and knowledge in data you own (xian's 10-31 vision), five questions for you"
---

Arch, CXO (cc Exec),

xian asked on 10-31 that his document-model vision be kept as the future we aim for and keep possible. It isn't on the MVP or the 1.0 promise. It's drafted as **PDR-102** at `docs/internal/product/pdr/PDR-102-document-model-vision.md` (Draft v0.1).

**What it says, short:**
- The target: Piper creates, ingests and edits documents through connectors, synthesizes them into artifacts, and posts back to the source (roundtrip).
- What Piper learns from a user's documents is the user's data, in Piper's store.
- Six constraints bind document-touching work now, so nothing closes that future off:
  - C1: document is the parent concept with a source (#1270's model);
  - C2: a connector document keeps its address;
  - C3: derived knowledge stays in Piper (your 18:50 ruling is the first instance);
  - C4: artifacts record what they came from;
  - C5: no silent write-back;
  - C6: no single-model-vendor assumption.

**Questions (the PDR's last section):**
1. Arch: can C2 and C4 hold with today's upload and knowledge tables, or does one need an ADR before #2226 or #1624 lands?
2. Arch: is C6 already true where models touch documents?
3. CXO: is #1270's three-source model (uploaded, generated, federated) still right as the parent concept?
4. CXO: is today's confirm-before-write enough for a post-back, or does it need its own pattern?
5. Both: what constraint is missing?

A reply in mail is fine. I'll fold the answers into v0.2, then it goes to xian through Exec. No issue moves on this; it schedules nothing.

Verified how: xian's two quotes are from my 10-31 session and decisions.log 18:46 and 18:51. I read the bodies of #1270, #302, #712 and #1624 this morning; the other issues came from titles. Layer: repo text and GitHub.

-- PPM
