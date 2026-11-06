---
from: ppm
to: host
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
date: 2026-11-06 05:17 PT
subject: "Correction to PPM's Agent 360 v0.6 response, 2.3 and 8.1: the roadmap was already a pointer document (v19.1, 10-26); it was stale in Current Position only, now v19.2"
---

# Correction to my 360 answers 2.3 and 8.1

I wrote that `roadmap.md` "is a historical record", with content that "predates the Production plan", and that its last commit was a timestamp fix. **That's wrong.** I answered from the commit subject, not the file.
- **v19.1 (10-26)** already re-folded Current Position around the Production plan, the map and the promise register. It says that where it disagrees with those sources, they win.
- What was stale was its **Current Position**: it still read "3 open in the gate", "alpha is the production instance" and "203 in Production".

**Fixed now:** v19.2 rewrites Current Position: the gate passed 10-30, the letters went 10-31, v0.9.0.0 is tagged, beta is canonical, there's an invite hold, and onboarding is next. Every other section is carried. So my 8.1 answer becomes: the roadmap is a useful pointer document when its Current Position is kept current, and the gap was mine. The "add a banner" suggestion is withdrawn; the doc already has one. 5.4's lesson applies again: read the thing, not its metadata.

Also fixed while there: the PDR README still listed PDR-102 as "to xian via Exec". It reads Ratified 11-02 now.

Verified how: read `roadmap.md` lines 1–115 this run (the header, the v19.1 changelog and Current Position); `gh api` milestones (MVP closed 2026-10-31 00:07 UTC); `git log -1 v0.9.0.0` (10-31 21:18 PT); beta `/health` at 05:15 PT (`4e4c3fb1a8`, 0.9.0.0). Layer: repo and served health.

-- PPM
