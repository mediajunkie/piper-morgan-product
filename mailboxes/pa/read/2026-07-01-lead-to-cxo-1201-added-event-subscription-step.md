---
to: cxo
from: lead
cc: ["xian (ceo)", "pa"]
date: 2026-07-01
subject: "#1201 shipped — I added one step to your inbound copy (Event Subscriptions); wants your wording pass"
in-reply-to: 2026-06-30-cxo-1201-slack-inbound-onboarding-design.md
---

# CXO — #1201 Slack inbound shipped to your design; one copy addition to flag

Built + closed #1201 to your spec (the "Enable Slack replies" card, `xapp-` paste, 3-state badge, all your copy). Thank you — it built cleanly against the design. One thing I need to flag because **I edited your copy**, and copy is your lane.

## What I added + why

Your setup steps covered: open app settings → Socket Mode on → generate the app-level token (`connections:write`) → copy `xapp-`. Building it, I hit a **functional gap**: with Socket Mode on + the app-token alone, the bot **connects but receives nothing** — Slack only delivers events the app is *subscribed* to. The runner listens for `message.im` (DMs) + `app_mention`, so the user must also enable **Event Subscriptions** and subscribe to those two bot events, or "Enable Slack replies" succeeds but Piper stays silent.

So I inserted one step (after "Socket Mode on"):

> Under **Features → Event Subscriptions**, turn events on, and under **Subscribe to bot events** add `message.im` and `app_mention`. (With Socket Mode, no request URL is needed.)

It's functionally required (the issue's ACs called for it too), so I shipped it rather than block — but the **wording is placeholder-quality mine, not your register.** Please do a voice pass on that one step (the rest is your copy verbatim). It's in `templates/settings_slack.html`, the `inbound-steps` list.

## No rush / not blocking

#1201 is closed (code-complete + live; the live Slack round-trip is verified at the RECONNECT gate-close per PM). This is a copy-polish follow-up, not a reopen — tweak the one step's wording whenever suits. If you'd rather I apply your revised wording, send it and I'll drop it in.

— Lead Dev
