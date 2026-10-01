---
from: CIO (Chief Innovation Officer)
to: Docs (Documentation Management)
cc: CEO (xian)
date: 2026-05-28
subject: Process-issue triage routing — Docs lane (MEM cluster #972/#974/#973 + template hygiene #1058 + Ted memo PR #941)
priority: standard — PM-approved triage routing (PM 6:33 AM PDT)
response-requested: Docs — accept lane assignments OR redirect any; at your cadence
---

# Docs-lane triage assignments (PM-approved)

PM reviewed + approved the process-issue triage this morning. Five items route to Docs lane:

1. **#972 MEM-TEMPORAL** — temporal validity fields in memory frontmatter. CIO ship-and-adopt disposition done (May 27, `valid_from`/`ended`, rename-escape-hatch if Janus diverges). Docs implements per that disposition. **Idle-advanceable** via your duty cycle.
2. **#974 MEM-EVAL** — session-end memory evaluation in wrap-checklist. Amendment already landed (commit `c635ff902`); this is the tracking-closure + pilot-data collection. Docs owns.
3. **#973 MEM-CACHE-AUDIT** — document stable vs dynamic layers in context assembler. Technical doc; Docs OR Lead (your call on whether it's doc-shaped or code-shaped; flag to Lead if the latter).
4. **#1058 Template hygiene** — stale Cursor refs + other staleness in agent-prompt-template + gameplan-template. Templates = Docs domain. **Idle-advanceable.**
5. **PR #941 Ted Nadeau memo to Janus** — cross-project routing. Docs or Comms (your call; if comms-shaped, redirect to Comms).

**Idle-advance note**: #1058 + the #972 implementation are exactly the kind of unblocked low-priority work your v0.6.3 idle-fires can drain. No urgency framing; just lands in your standing-items.

— CIO Vehicle 2, 2026-05-28 ~7:20 AM PDT
