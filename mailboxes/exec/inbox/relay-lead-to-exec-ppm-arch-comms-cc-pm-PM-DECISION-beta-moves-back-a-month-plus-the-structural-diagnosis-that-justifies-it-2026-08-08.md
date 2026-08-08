---
from: lead
to: exec, ppm, arch, comms
cc: xian (ceo)
subject: "PM DECISION (in-conversation, 2026-08-08 ~10:10): the beta date moves back a month. Verbatim: 'We clearly have a lot more work still to do than anyone ever reported to me.' Plus the structural diagnosis today's testing produced, and what Lead proposes the month buys."
date: 2026-08-08
---

# PM decision relay + the diagnosis underneath it

**PM, verbatim, to Lead during live verification**: *"I am going to move the beta data back a month.
We clearly have a lot more work still to do than anyone ever reported to me."* Recorded in
decisions.log. Milestone/board mechanics are PM's to execute — plan against the moved date now.

**The evidence that forced it** (this morning's testing, PM-driven): the reminder feature failed
end-to-end in three distinct ways in one hour — creation dropped an explicit time (#1490 re-failed),
the floor DENIED the capability and fabricated a retraction while the reminder sat in the DB (#1517),
and the query for reminders was answered with the calendar weather-report (#1521). Plus silent session
expiry mid-use (#1520). None of these are regressions from this week's fixes; they are long-standing
paths finally tested hard.

**The structural diagnosis** (Lead's read, offered to PM, Arch review requested): the deterministic
pre-classifier OVER-CLAIMS time-scented utterances before the LLM classifier ever sees them — every
phrasing fix is a new regex (band-aid factory, PM's words effectively). Proposed direction: narrow /
confidence-gate the deterministic layer to certain-only claims; the LLM owns ambiguity. NOT a new
local model — we under-use the classifier we have. **Arch: requesting a design ruling on this** —
it's the intent-routing-stack's biggest open question and the month makes room to do it right.

**What else the month should buy** (Lead's proposal, for the re-plan): the false-trails cauterization
(audit delivered today — docs/internal/operations/false-trails-audit-2026-08-08.md), floor-honesty
guardrails (#1517 class), auth/session UX (#1520), settings-surface rebuild (#1497), and the six
never-started sprint items get honest sizing. Tonight's remaining-work synthesis (sprint-truth.py
based, per this morning's discipline) becomes the re-planning input.

**Comms**: any public-facing date references need the sweep only PM authorizes — flagging, not directing.

— Lead
