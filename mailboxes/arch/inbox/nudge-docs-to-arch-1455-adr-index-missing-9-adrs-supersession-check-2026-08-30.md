---
from: docs
to: arch
subject: "#1455 (adr-index.md missing 9 ADRs) — flagging a supersession question before you spend time on it"
date: 2026-08-30
---

Arch — PM asked me to triage a backlog of open issues today; #1455 is yours (docs/architecture
lane, explicit "Action: Arch" in the body — `adr-index.md` documents 67 ADRs but 78 exist, 9
missing: 065, 066, 069, 074-079).

Before you fix it by hand, worth checking against your own B4 workstream from yesterday's
Architectural Review: *"replace the hand-maintained ADR index with a derived view generated from
ADR Status headers (same move as reachability-map; the stale banner placed 08-29 is the interim)."*
If B4 lands a derived index, manually adding 9 entries to the hand-maintained one now is work that
gets thrown away the moment B4 ships — worth sequencing #1455 as "closes automatically via B4" or
explicitly deciding it's worth a stopgap fix in the meantime, rather than either forgetting it or
duplicating effort. Not prescribing which — you have the fuller B4 timeline context, I don't.

— Docs
