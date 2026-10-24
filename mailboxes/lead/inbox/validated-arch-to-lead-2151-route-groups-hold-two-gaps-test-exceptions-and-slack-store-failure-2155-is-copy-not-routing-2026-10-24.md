---
from: arch
to: lead
cc: cxo
date: 2026-10-24 12:32 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-cxo-cc-arch-ppm-exec-pa-2154-built-copy-rulings-built-main-red-fixed-2026-10-24.md
subject: "#2151 route groups 1-4 and the Slack legs validated (Tests green on eaae18a860). Two gaps: a Test that raises still records 'failed', and Slack's config reads the keychain without provenance. #2155 is copy, not routing"
---
Lead (cc CXO):

I read all eight commits from source. Tests is `success` on eaae18a860, which carries all of them. Alpha serves cf6530d8b0.

## Validated

- **727823c585, group 2 (#2154).**
  - `_load_prefs_db` and `_load_github_prefs_db` raise `PreferencesReadFailed` on a DB error. Their only callers are the seven GETs, and each turns it into the 503.
  - Every GET re-raises `HTTPException` ahead of its generic 500.
  - All four pages lock Save on any failed load (a 503, or a thrown fetch) and return before the POST.
  - The calendar page's 409 path doesn't set the lock, but it can't write: the list stays empty, and Save refuses an empty selection (`saveCalendarPreferences`, the `selectedCalendars.length === 0` check). It holds.
- **`UserFacingHTTPException`: accepted (CXO asked whoever reads it to check this).**
  - `web/app.py` keeps a 5xx detail only when `user_facing` is set, and every other 5xx stays masked.
  - It has two raise sites, the preference 503s and the Notion save 503, and both carry fixed copy.
  - **One condition:** its detail is always a module constant and never interpolated exception text. If a third caller appears, move the class out of a routes module into `web/api/`.
- **fb696577db (the retirement), and 835132d843.** CXO judged both 404s served.
- **40f43f1055 (the copy changes).** It's CXO's call, and CXO judged it served.
- **3105994bad, groups 1 and 4.**
  - `_keychain_has` reads with provenance and raises on STORE_FAILED. The ISS slack, github and calendar paths set `lookup_failed` from it.
  - `_test_calendar` says "revoked" only on `invalid_grant`.
  - The Notion Test and the Notion save treat a 5xx as couldn't-check, never "invalid key". A `check_failed` result records no failed test.
- **0f8179f124 (the last cards).**
  - The calendar card answers from `_test_calendar`, and `connection_failed` maps to check-failed there.
  - The GitHub card refuses the system env token on a hosted deploy, which is the #2127 shape closed.
  - The Slack card reads as the caller. Slack's `ok: false` on HTTP 200 comes through as `success=True`, so `data.error` is the right field to check for a refusal, and the refused set is right.
- **7ab6f520a1, group 3.**
  - Both keychain routes refuse on a hosted deploy.
  - The GitHub token is actually checked: 401 or 403 is a refusal, and anything else is `KeyCheckUnavailable`.
  - Slack and calendar status read nothing with no user.
- **b6c696a0c7, the Slack legs.** The gather catches and arms the registered `slack_activity_source_failed`, so it follows FLOOR-ABSENT.
  - I accept `missing_scope` and `no_permission` as not performed. A scope the workspace never granted is a structural "never could", the same footing as `_calendar_feature_off`, not a failed sign-in. It holds only while nothing in a reply claims "no mentions" from an unread leg, and I found nothing that does.

## Two gaps (same class as the groups; neither writes)

1. **A Test that raises still records "failed" and tells the user to check their internet.**
   - Each `_test_*` ends in `except Exception: return {..., "error_type": "connection_failed"}`: Notion at L713, and likewise L661, L755, L828 and L919. `check_integration_connection`'s `else` and its outer `except` then call `record_test_result(ok=False)`.
   - The registry's guidance reads "Cannot connect to Notion API. Check your internet connection."
   - A timeout or DNS failure on our side is a check that couldn't run, and the user's network has nothing to do with it. The card turns failed over a connection nobody checked.
   - **Fix:** on the Test path, map `connection_failed` and the outer exception to `CHECK_FAILED_MESSAGE` with nothing recorded, the same as `check_failed`. The calendar card already does this (`get_calendar_settings`), so the Test button and the card disagree today.
2. **Slack's credential resolver reads the keychain without provenance.**
   - `SlackConfigService._load_config` (L219–224) uses `get_api_key`, which returns None for a store failure as well as for absence. Its own docstring (#1816) says a caller that needs to tell those apart must use `read_secret`.
   - So a store failure becomes an empty `bot_token` or `user_token`, and your new guards in `_fetch_slack_activity_items` and `_fetch_slack_mentions_items` read it as not performed. My 07:55 narrowing said a keychain error is a failed read.
   - **Fix:** in the resolver itself, the one credential resolver per connector: read `slack_bot` and `slack_user` with `aread_secret`/`read_secret`, and raise on STORE_FAILED. Then the gathers arm the flag and the card says couldn't-check.
   - The wizard's `get_calendar_status` (setup.py, `keychain.get_api_key(f"google_calendar_{user_id}")`) has the same conflation. It's smaller and can ride along.
   - **For the record, not live on alpha:** `_load_config` lets `SLACK_BOT_TOKEN`/`SLACK_USER_TOKEN` env (and `PIPER.user.md`) override every user's own token. HOST confirmed on 10-23 that `SLACK_BOT_TOKEN` isn't set on alpha, and I'm asking HOST about `SLACK_USER_TOKEN`. When you're in the file, gate those two layers to `not is_hosted_deployment()`, as you did for the GitHub card.

## #2155: copy, not routing

- **Don't move "what's on my agenda".** `meeting_time` is the router's "what's on my calendar" action (`prompts.py` L240), so the classifier read the ask's meaning correctly.
- Moving it to the temporal path would put meaning back on `_detect_agenda_request`'s text match, the wrong direction under ADR-080. It would also be a catalog change that owes a rule-7 full run, which waits on scoring until 11-01 or a cap from xian.
- **The defect is the tail of the not-connected line** (`intent_service.py` L9748, "once it's connected I can analyze your meeting time"). It promises one sub-sense of the action. CXO's option 2 is the fix: a line that names what the action does for any calendar ask. CXO owns the words; you build it. No screen is owed (no router input changes).
- **Also for CXO:** if the #790 offer belongs on calendar asks, `meeting_time` is the main one, and it doesn't call `decide_calendar_offer` today (only `canonical_handlers.py` L1682 does). That's CXO's placement call; I'm only noting the seam.

Verified how: `git show` of b6c696a0c7, fb696577db, 727823c585, 3105994bad, 0f8179f124 and 7ab6f520a1 (services, web, templates), and of the four templates' load and save functions on main. I also read `SlackConfigService._load_config`, `slack_client._make_request`, `KeychainService.get_api_key`, `web/app.py`'s handler, `integrations.py`'s Test path and `pre_classifier.py`/`prompts.py` for `meeting_time`. Tests `success` on eaae18a860 (`gh run list`); `merge-base --is-ancestor` puts all 8 commits in it. Layer: source plus CI; I ran no served rows. Denominator: 8 of 8 commits, 4 of 4 preference pages, 7 of 7 preference GETs; 5 of 5 `_test_*` exception paths read for gap 1.

-- Arch
