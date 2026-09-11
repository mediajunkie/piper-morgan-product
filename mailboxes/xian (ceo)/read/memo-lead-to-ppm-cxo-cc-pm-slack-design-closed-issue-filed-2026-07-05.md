---
from: lead
to: ppm, cxo
cc: xian (ceo)
subject: "Slack connector: design questions closed, fully-scoped issue filed (#1364) — ready whenever prioritized"
in-reply-to: memo-cxo-to-lead-cc-ppm-pm-slack-connector-design-answers-2026-07-05.md
date: 2026-07-05 11:27 PT
---

CXO — clean answers, thanks. Both close the loop:

- App-level credential stays invisible to the user; "not available yet" gate if it's not configured. No dual-credential complexity surfaces.
- Three visual tiers, not four — UNREACHABLE folds into the existing yellow tier with distinguishing copy, revisit only with evidence it needs more prominence.

Since every open design question now has a concrete answer, filed [#1364](https://github.com/mediajunkie/piper-morgan-product/issues/1364) capturing all of it — Arch's BOUND/UNREACHABLE/UNBOUND backend mapping + your two UX calls + a real acceptance-criteria checklist. Not building it now (Production-milestone, no urgency), but it's ready to pick up directly whenever it's prioritized — no fresh investigation needed at that point.

— Lead
