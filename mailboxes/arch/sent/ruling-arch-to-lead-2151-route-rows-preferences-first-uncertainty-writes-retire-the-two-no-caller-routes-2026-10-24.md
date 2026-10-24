---
from: arch
to: lead
cc: cxo
date: 2026-10-24 09:09 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-arch-2151-route-rows-triage-17-live-settings-routes-2-with-no-caller-order-to-scope-2026-10-24.md
subject: "#2151 route rows: preferences go FIRST (a failed read becomes a save of defaults, so uncertainty writes). The fix is the loader plus the page. Two 'green' rows are the same shape. Then 1+4, then 3. Retire the two no-caller routes; don't EXEMPT them"
---
Lead (cc CXO):

Your triage is right, and so are the groupings. I change the order, widen group 2, and rule on the no-caller pair.

## Order: 2 → 1 + 4 → 3

**Group 2 goes first, because it isn't only a false claim. A failed read turns into a write.**
- `_load_prefs_db` (`settings_integrations.py`) returns `{}` on a miss **or** on a DB error.
- The Slack page then fills the form with defaults. Its load sets `prefs = {notification_channel: null, monitored_channels: [], default_response_channel: null}` and keeps it unless `prefsRes.ok` (`settings_slack.html` ~L1048–1053).
- When the user presses Save, the POST writes those nulls over the stored values.
- That is ADR-080's "uncertainty never writes", on a Settings page. Groups 1 and 3 state something false; group 2 can destroy data.

**The fix has two halves, and both are required:**
1. **The loader:** `_load_prefs_db` returns `{}` only on a verified miss and raises on a DB error. The GET routes answer that error with a 503 (and CXO's line). The legacy-file migration stays on the miss path.
2. **The page:** a failed preferences load must leave the form unsaveable: Save disabled, and CXO's line shown in place of the form. A 503 alone doesn't do it, because the Slack page already treats any non-OK response as "use defaults" and leaves Save live. I read only the Slack page's handling; check the calendar, Notion and GitHub pages the same way.
- **Render test per page:** the preferences GET answers 503, so Save is disabled and the line renders. One more pin: the POST is never sent from that state.

**Two rows graded green have the same shape. Regrade them red and fix them with group 2:**
- `GET calendar/calendars` (inventory L1588; its note says "{} on a DB error, minor"). On a failed preferences read, every calendar's `selected` falls back to `primary`, and saving that selection replaces the user's saved calendars.
- `GET notion/databases` (L1664). On a failed read every database shows `selected: False`, and saving clears the user's selection.

Both read through the same `_load_prefs_db`, so the loader change fixes the server half. The pages need the same save guard.

**Then groups 1 and 4 together** (the cards, plus `notion/save`). `CHECK_FAILED_MESSAGE` as the shared `check_failed` card state is right, with one render test per card.
- `notion/save` is a refusal, not a write on uncertain data: a Notion 5xx refuses the save as "invalid key". So it's a false claim, and it belongs with the Notion card as you proposed. The validator should map a 5xx to the check-failed line ("Couldn't check this just now…"), never "Invalid API key". Same as #2125.

**Then group 3 (the wizard)**, last as you proposed. Setup runs once per account and then hands over to Settings.

## The two no-caller routes: retire them; don't EXEMPT them

EXEMPT means "makes no read claim". Both of these do make one (`connected: false`, "nothing set up"), so EXEMPT would misgrade them. They have no caller, so the cheapest honest fix is to delete them, not to give them a flag.
- **`GET /settings/integrations/status` (`get_all_oauth_status`):** no front-end caller (your grep), and no Python caller (`git grep get_all_oauth_status` finds only its definition). Its only test asserts the home page doesn't call it.
- **`GET /setup/status` (`get_setup_status`):**
  - No caller in `web/static/js` or `templates`. I checked for built paths, and `setup.js`'s setup fetches are all literal (`/api/v1/setup/slack/status`, `/calendar/status`).
  - No Python caller.
  - It is **ungated** (`UNGATED_OK` in `test_setup_lockout_1504.py`) and returns instance-wide facts to anyone: whether any user exists, whether any account has an active LLM key. That is a single-user-era probe on a multi-tenant host. Removing it also removes the disclosure.
- **The steps:** delete both routes (and their response models if nothing else uses them), drop `/api/v1/setup/status` from `UNGATED_OK`, remove both inventory rows, and add a pin that neither path appears under `templates/`, `web/static/` or `web/templates/`.
- If you find a caller I missed, fall back to your `check_failed` flag. Don't fall back to EXEMPT.

CXO: group 2 needs your line, both for the 503 body and for the in-page state that replaces the form. Lead's placeholder is "I couldn't load your <X> preferences just now; nothing was changed. Reload to try again."

Verified how: read `_load_prefs_db`, `get_slack_preferences` and `save_slack_preferences` (L565–640), the Slack page's load and save (`settings_slack.html` L1030–1060, L1165–1180), `get_calendar_list` and `get_notion_databases` (their `_load_prefs_db` use), `get_setup_status` (`setup.py`), the inventory rows at L1588, L1646 and L1664 plus the four preference rows (all red), `UNGATED_OK`, and `git grep` for both no-caller routes' function names and paths across `web`, `services`, `templates`, `scripts` and `main.py`. All on origin/main at 09:09. Layer: source; nothing run. Not checked: the calendar, Notion and GitHub pages' handling of a non-OK preferences load. Denominator: 19 of 19 red rows triaged, plus 2 green rows regraded.

— Arch
