---
from: cxo
to: lead, web
cc: arch, ppm
date: 2026-10-24 09:32 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "716cb6dc6c: seven rows judged (six pass; time row's offer is the old #790 offer, true). Three not-connected lines approved. Preferences-failed words for group 2"
---

Lead, Web (cc Arch, PPM):

## 1. Web's seven rows on `716cb6dc6c`, `web-pat-test`

- **Row 1, attention: pass.** Quoted: "Google Calendar isn't connected yet, so meetings aren't included. Ask me "how do I connect Google Calendar?" and I'll walk you through it." Right line, true for this account. The "Nothing from your flagged todos…" variant didn't apply (the account has a todo and a stale project), so that variant stays pinned, not served. **One layout ask:** Web read the calendar sentence running on straight after the Stale line. Please look at the rendered page (a screenshot or the line breaks in the DOM, not text alone). If it runs on, the calendar sentence wants its own paragraph. If the page text collapsed the break, nothing to fix.
- **Row 2, time: pass, and not a deviation from this build.** Quoted: "I noticed your calendar isn't connected yet — would you like help setting that up? You can connect Google Calendar at /settings/integrations/calendar." That is the #790 offer in `calendar_offer_policy.py` (PM-approved 2026-05-03 "as drafted", file unchanged by any #2151 commit I can see in `git log`). It is true. I expected "unchanged" and it is unchanged. I did not read whether it repeats on every reply or only once; if Web sees it on a second time ask in the same chat, tell me. Not a gate. A calendar upsell under a time answer is not what I'd have designed, so I'd take a ticket to offer it only on calendar-related asks, but it is not this sweep's.
- **Row 3, connect offer: pass.** "Google Calendar isn't connected yet. Connect it in Settings → Integrations → Google Calendar." The "No," is gone.
- **Row 4, "is google calendar connected?": pass.** "No, Google Calendar isn't connected. …" is the right shape for a yes/no question.
- **Rows 5 to 7: pass.** No false "couldn't check" on an account that is fine, which is the false alarm I most wanted ruled out. Row 7's "Nothing yet, honestly — …" is chat copy from the model; I'd drop "honestly" in anything we write ourselves, and it is not a gate.

## 2. Lead's three not-connected lines: approved as written

1. "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can look at your repository activity."
2. "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its milestones."
3. "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can show you what shipped."

They say what is true (nothing stored), name the place, and match the served connect-offer wording. One condition: they appear only on an account with no stored credential. A broken token takes the "couldn't check" template. Lead says the pins cover that split; fine.

## 3. Group 2, preferences failed to load: words (Arch asked for the 503 body and the in-page state)

One sentence for both, with the product name in place of X:

> "I couldn't load your {X} preferences just now, so Saving is turned off to keep your saved settings as they are. Reload to try again; if it keeps failing, tell us."

- {X} is "Slack", "GitHub", "Google Calendar" or "Notion". For the two regraded routes: "your saved calendar choices" (calendars list) and "your saved database choices" (Notion databases) in place of "{X} preferences".
- The form is **not rendered** in this state (the line replaces it), Save is disabled, and the POST is never sent. A disabled Save under a visible form of defaults still invites the user to retype everything.
- I dropped Lead's "nothing was changed". It is true, but the user's worry is "will I lose my settings?", and the new clause answers that.
- Class: this is class 1 (a failed read becoming a write), so served rows for the success branch (preferences load as before) are Web's, and the failed branch is pinned only, said so at close.

## 4. Arch's route-row order, no-caller routes

No objection to 2 → 1+4 → 3, or to retiring the two no-caller routes. Nothing in either is copy I own except the `check_failed` card line, which stays "Couldn't check this just now. Press Test to try again." (already served on the integration cards).

Verified how: read Web's quoted replies and Lead's and Arch's memos this turn; `git grep` and `git log` on `calendar_offer_policy.py`. Did not run any row (no alpha account). Layer: served UI as quoted; source for the offer's age. Denominator: 7 of 7 rows judged, 1 account; 3 of 3 lines; the group-2 words cover all four preference pages plus two regraded routes.

-- CXO
