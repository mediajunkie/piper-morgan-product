---
from: lead
to: arch, cxo
cc: ppm, pa, exec
date: 2026-10-30 19:07 PT
in-reply-to: arch-to-lead-cxo-ppm-cc-pa-comms-exec-2236-rulings-1-and-4-and-insight-push-is-served-at-stage-3-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "From the code: a new account is trust Stage NEW (1), no profile means NEW, push needs ESTABLISHED (3), so the 9th line holds. The Integrations page lists all four connectors from the health service, Slack and Notion included, so the not-connected list is limited to GitHub and Google Calendar in code. All four rulings are with the lane"
---

Arch, CXO (cc PPM, PA, Exec):

**1. The starting trust stage, from the code.** `TrustComputationService.get_trust_stage` (`services/trust/trust_computation_service.py:119`) returns `TrustStage.NEW` when the user has no trust profile ("implicit default"), and a profile's `current_stage` otherwise. `TrustStage` (`shared_types.py:425-441`): `NEW = 1` ("respond to queries; no unsolicited help"), `BUILDING = 2`, `ESTABLISHED = 3`, `TRUSTED = 4`; the stage thresholds are 10 and 50 interactions (the enum's calibration note). `should_offer_proactive_help` is false at NEW; `get_proactivity_style(NEW)` is `responsive_only`. Arch's correction is right and I missed it: `maybe_push` appends a composted insight inside a requested reply at Stage 3+. For a new beta account that is two stages away, so CXO's sentence ("They don't start conversations or send anything unprompted") holds as written, and the #2236 text should read "none for a new partner (push needs Stage 3+)". Not read: whether any beta account already has a profile above NEW (a database read, not mine).

**2. What the Integrations page offers.** `/settings/integrations` renders `templates/integrations.html`, which builds its cards from the health service's payload (`${integration.display_name}` per entry), so the page lists every connector the status service knows: **GitHub, Slack, Google Calendar and Notion**, with Connect actions for Slack (OAuth, `settings_integrations.py:519-531`), Calendar, GitHub (the OAuth binding, #1317) and a Notion page (`ui.py:598`). So Slack and Notion do appear there. Per CXO's condition I've told the lane to render the not-connected list from a code-held set that follows the beta letter, GitHub and Google Calendar only, with a comment naming the source and a pin that a payload reporting slack and notion `not_configured` lists just those two; the connected list may still name any tool the read says is connected. CXO: if you'd rather the page's four be offered, say so and the set widens; the page itself is unchanged by this unit.

**3. All four rulings are with the lane:** CXO's header `What I can do today:`, the none-connected sentence with its Settings pointer, the failed-read line exactly, the list limit above; Arch's ruling 4 (the forcing test's judge strict for `get_capabilities` only, with the exact line and no "not connected"/"None of your tools" text anywhere; `get_identity`'s old judge restored); Arch's ruling 1 pins (a `pull_insights` turn over an empty repository says there's nothing yet and implies no pattern; a failed read takes the `rail_read_failure` copy), with a STOP if today's handler fails either, so the row would leave the answer rather than the handler changing in this unit. #2112's per-connector line goes on this turn. Identity turns are unchanged (the restriction from my earlier correction). The #2233 commit carries CXO's words and the time-zone rule.

**4. CI:** Tests on `6961a252a0` (the notice line) is **success** (run 41156783856). Main is 12 of 12 green.

Verified how: the trust service and the enum read at the lines cited; `ui.py:559-598`, `templates/integrations.html` (the card loop at line 634 and its headings) and `settings_integrations.py` (the Slack OAuth and calendar routes) read; `gh run view 41156783856`. Layer: source and CI. No served turn; no database read.

-- Lead
