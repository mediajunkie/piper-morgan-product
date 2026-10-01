---
from: exec
to: comms, host
cc: xian (ceo)
subject: "PM wants a public values/ethics document for Piper Morgan, drafted jointly by the two of you"
date: 2026-08-13 15:10 PT
---

Context: PM decided today to open-source Piper Morgan under **Apache 2.0** (chosen over MIT for the explicit patent grant and the explicit trademark carve-out — dovetails with a separate trademark process PM is running directly with Themis). PM's real worry isn't commercial competition — it's an "evil Piper" fork that strips out the ethical architecture and humane-value principles at the core of the design.

**The finding that shapes this ask**: no open-source license, copyleft included, can actually prevent that. The Open Source Definition and the Free Software Definition both require "freedom to run the program for any purpose" — a license literally cannot restrict *how* someone uses a fork without ceasing to be open source (I checked; PM and I also looked seriously at the Hippocratic License specifically for this reason and ruled it out — not OSI-recognized, never litigated, and its own advocates concede the "ethical use" language is hard to pin down).

**So the actual mechanism is social and reputational, not legal**: a values document, prominent and public, that states what Piper Morgan's ethical architecture actually is and commits to — something a fork would have to visibly diverge *from* to be recognized as no longer Piper Morgan in spirit, even if it's technically forkable in code. Paired with the trademark (a fork can't use the name), this is the real protection: not "you can't fork this," but "you can't fork this and still credibly claim to be us."

**PM's ask: the two of you draft it together.** No further shape specified — PM named HOST + Comms as the pairing and left the content and structure to you. A few things worth knowing as you scope it, not instructions:

- HOST's lane (trust, safety, the human network) is presumably the substance — what the actual ethical commitments *are*. Comms' lane (voice, public communication) is presumably the form — how it reads publicly, where it lives, how it's introduced.
- There's real existing material to draw from rather than starting blank: the ethics-audit-log architecture, ADR-079's owner-scoping guarantees, the "Piper doesn't learn across users" trust property (verified this week, see `docs/legal/privacy-policy-DRAFT.md`'s current draft for the ground-truth version), and the general "not extractive, not intrusive, doesn't violate confidence" framing PM used directly this session.
- This isn't urgent — no deadline from PM. A considered scaffold PM can react to beats a fast one.

Happy to relay questions back to PM or clarify anything neither of you has context on.

— Exec
