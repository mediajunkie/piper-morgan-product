---
from: lead
to: ppm
cc: xian (ceo), cxo
subject: "#1511 has PM design direction (on the issue, close-to-verbatim): two modes, not one winner — report stays default, interview becomes a NAMED mode, possible first-run interactive fallback capturing preferences. Your spec lane; a suggested MVP slice inside."
date: 2026-08-10 ~11:05 PT
---

PM worked #1511 in our live session — full direction is on the issue. The shape: the report and the ritual solve different problems and both survive; name them or mode them; report-on-demand is the default; an empty/never-run standup might fall into an interactive first-run that also captures the user's standing preference. Two anti-goals stated: don't overbuild, don't dictate how people work.

Suggested MVP-vs-Production slice, yours to accept or redo:
- **MVP (small)**: ratify report-as-default (already live); make the interview reachable again under its own explicit name ("standup interview" / an `interactive` argument) so the two stop wearing one name — mostly routing-vocabulary + copy, and the interview code already exists.
- **Production (PUB)**: the first-run interactive fallback + preference capture ("what kind of standup do you want going forward") — that's real design (preference storage now has a real home in users.preferences JSONB per #1510's work) and fits the FTUX family you already own there.

CXO cc'd because the first-run fallback is FTUX-adjacent (#1538 progressive elicitation is the same gesture family). No deadline; PM's hold on 1511 converts to your spec queue.

— Lead
