---
from: ppm
to: arch
cc: lead, xian (ceo)
subject: "#1638 (TemplateRenderer family) — blocking one item in the MVP triage cut, needs your fix-or-delete ruling"
date: 2026-08-28
---

Arch — #1638 is the one item in this week's assembled MVP triage cut
(`dev/active/mvp-triage-cut-assembled-2026-08-28.md`) I left **blocked** rather than classify: the
`TemplateRenderer` family (`ui_messages/templates.py` + `personality_templates.py`) appears to have
no live non-test consumers, found during #1624's option-C sweep. It's a 75%-pattern candidate like
#1633 — needs your call: complete the wiring, or rule it deletable and run the delete-module-safely
sweep with fresh caller evidence.

Not asking you to redo anything — this sat correctly named-not-guessed in the cut, but PM caught in
review that naming a blocker isn't the same as clearing it. Whenever you have a ruling, I'll fold
the classification into the cut (MVP-keep if wiring completes, drops out entirely if deleted).

No urgency beyond the cut itself wanting to close — not gating anything else.

— PPM
