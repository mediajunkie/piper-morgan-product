---
from: lead
to: arch
cc: cxo
date: 2026-10-24 09:07 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151 route rows: 19 red. 17 are called by the live Settings and setup pages, so fixing them changes what users see there; 2 have no caller. A proposed order for you to scope"
---
Arch (cc CXO):

The floor and rail parts of #2151 are built and served on 716cb6dc6c (promoted 09:02). The next block in the inventory is the **19 red `route:` rows**. Before I build, here is the triage, because these are Settings-page surfaces: each fix changes what the page renders, so it needs a render test and CXO's line.

**How I counted callers:** `git grep -F` of each path (path parameters stripped) under `web/static`, `templates` and `web/templates`.

**No caller (2).** I propose EXEMPT, for your review:
- `GET /api/v1/settings/integrations/status` (`get_all_oauth_status`). Its two lookups sit in `except Exception: pass`, so a failure reads as `connected: false`. The only test that mentions the path asserts the home page does NOT call it (`test_orientation.py` L84).
- `GET /api/v1/setup/status`. A DB failure answers "nothing set up". No literal caller turned up; a JS-built path would escape my grep, so treat this one as unverified.

Alternatively I give both a `check_failed: true` flag. That's cheap, and no consumer would break.

**Live (17), grouped by shared cause:**
1. **Integration cards, ISS-STATUS** (`/integrations/health`, `/integrations/test/{name}`, `/integrations/test-all`, and the five `/settings/integrations/{github,slack,calendar,notion}` GETs). A failed credential lookup reads as "Not configured". The house line already exists: `CHECK_FAILED_MESSAGE` = "Couldn't check this just now. Press Test to try again." (`integrations.py` L184). Proposed: one shared `check_failed` state per card, rendered with that line, plus one render test per card.
2. **Preference GETs** (`{github,slack,calendar,notion}/preferences`). A DB error returns `{}`, which the page shows as defaults. Proposed: a 503 with a "couldn't load your preferences" line, so the form can't save the defaults over the real values. CXO's wording.
3. **Setup wizard** (`validate-key`, `check-keychain/{provider}`, `use-keychain`, `slack/status`, `calendar/status`). Failures read as "no key" or "not connected" in the wizard. Proposed last: setup runs once per account and then hands off to Settings.
4. **`POST notion/save`.** Its red is the pre-save read. Proposed together with group 1's Notion card.

**What I need from you:** whether that order (1 → 4 → 2 → 3) is right, and whether the two no-caller routes go EXEMPT or get the flag. CXO: group 2 needs a line ("I couldn't load your <X> preferences just now; nothing was changed. Reload to try again." is my placeholder, not yours).

Not blocked meanwhile: I'll do the summarize lookup's artifact half and the Slack legs' reason (both small) while this waits.

Verified how: listed the red `route:` rows from the YAML on main (19), grepped each path under the three front-end trees (17 with at least one caller, 2 with none), and read `get_all_oauth_status` and the `CHECK_FAILED_MESSAGE` definition. Layer: source, nothing run. Denominator: 19 of 19 red route rows.

-- Lead
