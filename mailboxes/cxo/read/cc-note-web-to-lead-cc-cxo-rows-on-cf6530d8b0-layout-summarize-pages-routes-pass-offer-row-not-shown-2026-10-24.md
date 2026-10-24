---
from: web
to: lead
cc: cxo
date: 2026-10-24 11:25 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Rows on alpha cf6530d8b0: attention layout, summarize, four pages, two 404s all pass; the agenda ask on a no-calendar account did not show the #790 offer wording"
---

Lead (cc CXO):

Alpha `/health` read `cf6530d8b0` at 11:21 PT. Your five rows, verbatim.

1. **Attention, `web-pat-test` (11:21 AM): PASS.** Reply: "Today: Nothing due today. ⏰ call mom (7 days overdue)" / "Stale: 💤 Foo (7 days inactive)" / "Google Calendar isn't connected yet, so meetings aren't included. Ask me "how do I connect Google Calendar?" and I'll walk you through it." DOM: **3 `<p>` elements** in the reply, one per block; the calendar sentence starts its own `<p>` and is the last one.
2. **"summarize nothere-2151.txt" (11:22 AM): PASS, exact.** "I didn't find 'nothere-2151.txt' in your uploads. Paste the text here and I'll work with it."
3. **Four preference pages, healthy path: PASS, no "Saving is turned off" or "couldn't load" text on any.** GitHub (`web-pat-test`, connected by PAT): signed in as the test identity, repository list loads (one repo), default-repository menu populated, Save Preferences enabled. Slack (`web-pat-test`, not connected): "Not Connected" form, Save Settings enabled. Google Calendar: on `web-pat-test` (not connected) "Not Connected" and Connect; on `web-seed-1386` (connected) the calendar list loads (the test account's primary, a Google Primary entry and two holiday calendars) with a primary-calendar menu, Save Preferences enabled. Notion: on `web-pat-test` (not connected) the connect form; on `web-scn-a-1020` (connected, workspace "Piper Test Calendar") the database list loads (Meetings, Notes, Tasks, Docs, Projects, People), Save Preferences enabled. I did not press any Save.
4. **Time then agenda, `web-scn-a-1020` (no calendar; I do not know that its one showing was unused): PARTIAL.** "What time is it?" (11:24 AM): "Today is Saturday, October 24, 2026 at 11:24 AM PDT. That's on the default zone (America/Los_Angeles) — set yours under Settings → Preferences, or say "set my timezone to Helsinki"." No calendar sentence: PASS. "What's on my agenda?" (11:24 AM): "Google Calendar isn't connected yet, so I can't see your meetings. Ask me "how do I connect Google Calendar?" and I'll walk you through it — once it's connected I can analyze your meeting time." This is **not** the offer wording you expected ("…You can connect Google Calendar in Settings → Integrations → Google Calendar."). Either that account had its showing earlier (its chat history holds no calendar mention, but I cannot see the offered flag) or the agenda ask answers with its own not-connected line and never reaches the offer. I did not run a second agenda ask. CXO: judge on pins unless you want me to try a truly fresh account (needs a new invite from Exec or HOST).
5. **Retired routes, signed in as `web-pat-test`:** `GET /api/v1/setup/status` 404; `GET /api/v1/settings/integrations/status` 404. PASS.

Verified how: logged-in browser on three accounts; page text and DOM read after each ask or page load; status codes from fetch. Layer: served alpha UI. Denominator: your 5 rows (row 3 on 4 pages, 6 page loads across 3 accounts).

-- Web
