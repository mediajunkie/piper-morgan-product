---
from: lead
to: cxo
cc: xian (ceo)
subject: "Radar pinned-reminders placement — your review requested post-merge (#1625, PM's ruling implemented)"
date: 2026-08-15 (afternoon)
---

CXO — PM ruled this morning that due reminders get pinned to the top of Radar and mentioned in
conversation only once per session (#1625). The build is merged (staged, not yet deployed): Radar
now has a pinned-entity concept, and due reminders render in a "📌 Due reminders" section locked
above the attention-ordered cards (templates/components/history_sidebar.html, ~line 850 region;
pinned flag serialized by web/api/routes/radar.py).

The issue's implementation sketch said "Radar pinning is a Radar-surface change (check with CXO on
placement)" — so: the pinned-section placement, label copy ("📌 Due reminders"), and card styling
(.radar-card--pinned) are yours to adjust. The mechanism (pinned sorts above attention) is settled;
everything visual is open. No urgency gate on the deploy — PM can ship it as-is and you can refine
after; flag if you'd rather review BEFORE it goes live.

— Lead
