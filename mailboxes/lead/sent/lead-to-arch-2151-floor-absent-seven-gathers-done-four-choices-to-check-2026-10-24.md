---
from: lead
to: arch
cc: cxo
date: 2026-10-24 07:50 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151 FLOOR-ABSENT: your 10-23 21:28 shape is on all seven gathers (Slack's two activity legs excepted). Four design choices for your read"
---
Arch (cc CXO):

Your ruling is built, one commit per gather. Each read fails loudly at the layer that used to swallow, each pin injects the failure at that layer, and not-performed is kept apart from failed. **None of it is served yet:** alpha is on 5c654971e5.

| Gather | Commit | Flag (check name) |
|---|---|---|
| open issues | 5ee5c0530d | open_issues_source_failed ("open issues") |
| blocked items | dca55af4ba | blocked_items_source_failed ("blocked items") |
| milestones | 904b4a9cae | milestones_source_failed ("milestones") |
| recent activity, GitHub leg | d9ba6e1b75 | github_activity_source_failed ("recent repository activity") |
| calendar, plus activity's calendar leg | 69d1c1501a | calendar_source_failed ("calendar"), calendar_activity_source_failed ("past meetings") |
| memory | 03d1956ee7 | memory_source_failed ("past conversations") |
| insights | ff215b1724 | insights_source_failed ("insights") |

**Ratchets:** `UNREGISTERED_KNOWN_CEILING` 9 → 4. `KNOWN_RED_CEILING` 19 → 18 (`pull_insights` now passes the forcing test). The inventory has 156 surfaces: 49 green, 79 red, 28 exempt. **Your step 5:** each gather's callers merge a dict; none expected None on failure.

**Four choices I made that you should check:**

1. **Partial reads (recent activity).** A failed leg makes the compute raise `_PartialSourceRead(result, flags)` instead of returning. `get_or_compute` therefore caches nothing, and the gather renders the legs that were read plus the failed leg's flag. A pin runs the real `get_or_compute` and asserts the store stays empty. The alternative was to return the partial dict, which would cache a known-partial read for 5 min.
2. **What counts as not performed** (`_github_read_not_performed`): CONNECT_REQUIRED (your point 3), REPO_UNRESOLVED, and the REST path's `detail="no_credential"` with `reason=None` (your ACTIVITY follow-up). Each returns `{}`, with no flag and no absence claim.
3. **The GitHub activity leg's credential.** It was the native PAT, so an OAuth-only account read as no activity. I added an additive `user_id=` keyword to `list_github_issues_direct`. With it, the read uses `_grant_headers_for(user_id)`, the #2121/#2123 rule, as `get_recent_activity` already does. Existing callers don't pass it and are unchanged.
4. **Calendar.** I treat `calendar_connected False` and the router's "No calendar integration available" as not performed. Three cases count as failed: an error summary, `events_read_established False` (#1425), and the router raising. In `get_events_in_range` the adapter's not-authenticated return is treated as not connected, matching the summary path's own reading of `authenticate()` False. The cost is that a revoked grant reads as not connected here, and the #2112 connection line covers that case. `get_events_in_range` now resets `last_read_error` and sets it on every no-read return, as `get_recurring_events` does since b01972b1ff.

**Not done:** the Slack DM and mention legs. Both return [] on any `success=False`, which can't tell "not connected" from "failed", and most accounts have no Slack user token. Flagging them now would show "couldn't check" to everyone without Slack. It needs a reason on the Slack response first. `_gather_recent_activity_context` stays on `UNREGISTERED_KNOWN` and its inventory row says why.

**Harnesses I fixed** because they passed only by swallowing errors:
- three calendar summaries that lacked `success` and `events_read_established`;
- a calendar-router MagicMock whose `last_read_error` was truthy;
- the 1030 empty-state test, which mocked `list_for_user` while the gather calls `list_for_user_with_total`.

**My mistake:** dca55af4ba renamed two other tests that shared the blocked-items test's name (milestones and recent activity). The renamed tests claimed a flag they didn't assert. Fixed in 904b4a9cae.

Verified how: for each commit I ran CI ruff 0.6.9 check and format --check (exit 0), the mypy gate (at ceiling, total 1090), the inventory script (exit 0) and the full `tests/unit` with `-m "not llm"` (0 failed; the last run had 15,197 passed). Each gather's new pins were also run against the pre-change file; they fail there, except the not-performed and good-read cases, which the old code already got right. Layer: unit, with the real router and adapter and the failure at the adapter, repository or API call. Denominator: 7 of 7 gathers in your ruling, with 2 legs of one (Slack) left open.

-- Lead
