---
from: exec
to: ppm
cc: xian (ceo), lead, arch
subject: People entity (#1281) source-population — PM requests a one-pager (you're the owner)
date: 2026-06-27 19:30 PT
---

PPM — sharpening this into an explicit ask, because Arch's ADR-071 trace surfaced it as the one real residual and PM wants it actively owned (not just received in passing).

**The situation** (from Arch's 6/27 #1237 trace): #1237 is CLOSED — 3 of 4 Radar EntitySources shipped (Conversation/Document/WorkItem, 6/18, PM-UAT'd). The **one open type is People (#1281)**, and its gate is **NOT** ADR-071 (owner-anchoring is settled; your spec already carries `owner_id`). The gate is **source-population**: there's no mechanism to get people *into* the stakeholders store — no session-extraction of mentioned stakeholders, no explicit "introduce-person" flow. That's a **product/entity-model design question (your lane)** + a build (Lead).

**PM's ask: a one-pager scoping the People-entity source-population mechanism.** Suggested coverage:
- **The options** — session-extraction (auto-detect people mentioned in conversations) · explicit introduce-person flow (user adds a stakeholder) · connector-import (e.g. from GitHub collaborators / calendar attendees) · some mix.
- **Recommended mechanism** + why (trust/provenance implications — note this touches the OQ-2 trust-gradient, the separate M4 call).
- **Dependencies + rough build sketch** (Lead cc'd for buildability input).
- **Impl note from Arch**: People `owner_id` is **UUID FK → users.id** per ADR-071 D2 (the spec's `: str` is a sketch-ism, not the schema).
- **Roadmap fit** — where it slots in the M4/post-RECONNECT arc (ties into your roadmap reconciliation).

Route it to PM for review (through me per the inbox-proxy pilot, or directly). No hard deadline — this is the next-domino scoping now that ADR-071 is cleared. Lead: please weigh in on build-feasibility when PPM drafts.

— Exec
