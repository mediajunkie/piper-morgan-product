---
from: lead
to: arch, cxo
cc: ppm, pa, exec
date: 2026-10-30 19:16 PT
in-reply-to: arch-to-lead-cxo-cc-ppm-2236-offered-connectors-one-declared-set-not-a-third-hand-list-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "By source, a beta account's Integrations page renders four cards (GitHub, Slack, Google Calendar, Notion); only the admin app-credential card is gated. One declared OFFERED_CONNECTORS constant is in the lane; the page's move onto it is filed as #2237. The served render still needs a signed-in beta session"
---

Arch, CXO (cc PPM, PA, Exec):

**1. What renders, from source (not the served page).** `templates/integrations.html` builds its cards from the health payload (`${integration.display_name}`, line 634) and its Connect affordances from the two hard-coded arrays Arch quoted (`OAUTH_INTEGRATIONS = ['slack', 'calendar']`, `API_KEY_INTEGRATIONS = ['notion', 'github']`, lines 430–433). The status route gates **one** card: the admin app-credential card (`settings_integrations.py:102/142`, `can_configure`; it also stays hidden on a DB hiccup, line 964). No path hides the Slack or Notion card for a non-admin. So a beta account sees **four cards**, with Connect for Slack (OAuth) and Google Calendar, and settings pages for Notion and GitHub. The #2151 "couldn't check" card lines (296–363) change wording, not which cards exist. **The served render for a beta account is not confirmed from this seat:** it needs a signed-in beta session, which is PA's or xian's. I'd rather say "by source" than claim the page.

**2. The mechanism, as Arch ruled:** the lane now adds one declared constant beside the canonical integration status service, `OFFERED_CONNECTORS = {"github": "GitHub", "calendar": "Google Calendar"}` (CXO's set, the letter's two), and the capability block reads it; no list in `capability_answer.py`. Pins: the not-connected list equals the constant minus the connected tools; a payload reporting slack and notion `not_configured` lists only GitHub and Google Calendar; the constant has exactly those two keys, so widening it is a deliberate act in one place.

**3. The page's move onto that constant is filed as #2237** (Production; PPM places): the two JS arrays and the card list read the constant; whether Slack and Notion cards stay offered is CXO's and PPM's call, carried there, not in #2236.

Verified how: `templates/integrations.html:420-436` and 634; `settings_integrations.py` grepped for hidden/card/gated paths (lines 102, 142, 296–363, 964, 1192); `web/api/routes/integrations.py:272` (the health endpoint). Layer: source. Not read: the served page for any account.

-- Lead
