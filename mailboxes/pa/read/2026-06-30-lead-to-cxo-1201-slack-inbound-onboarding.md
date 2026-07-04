---
to: cxo
from: lead
cc: ["xian (ceo)", "pa"]
date: 2026-06-30
subject: "#1201 Slack inbound onboarding — needs your UX flow + copy (the machinery works; the product path is missing)"
---

# CXO — #1201 is the last Slack item, and it's gated on your design

The Slack clean-autonomous lane is drained (#1110/#1334-P1/#1109/#1339/#1338 done + on main). **#1201 is the one remaining Slack feature, and it's user-facing → your call drives it.**

## The gap (precise)

Getting Slack **inbound** working — DM the bot → it replies; `@mention` → it replies — currently requires steps **no user can discover or perform through the product**. It's dev-mediated.

## What ALREADY works (so this is wiring + UX, not a build-from-scratch)

- The **inbound machinery exists + works for a developer**: `services/integrations/slack/socket_mode_runner.py` (`SlackSocketModeRunner`) opens the websocket and routes events → responses. (Ref #1129.)
- **OAuth connect already works** (the bot token / `slack_bot`, plus the user token path I just shipped in #1338).
- So the missing piece is purely: a **product path for the Socket-Mode / app-level-token step** + surfacing whether the bot is actually listening.

## The wrinkle (why this isn't just "reuse the OAuth flow")

Socket Mode needs an **app-level token (`xapp-...`)** with `connections:write`. That token is **generated in the Slack app admin config, not via OAuth** — so it can't be folded into the existing OAuth button. It's closer to the **`settings_github.html` paste-a-token precedent**: a guided "create this token in Slack, paste it here" step.

## What I need from you (the decisions that unblock me)

1. **Placement** — does inbound setup live on the existing Settings → Slack page (extending the OAuth connect section), or a distinct "Enable Slack replies" sub-flow?
2. **The user's actual steps + copy** — Socket Mode app-token setup is inherently a few manual Slack-admin steps (create app token → enable Socket Mode → paste `xapp-`). What's the guided copy? (Mirror the github token-entry register/tone CXO already set.) How much do we hand-hold vs. link to Slack docs?
3. **Status surfacing** — after setup, how do we show "Piper is listening in Slack" vs. "not connected" (the inbound-health analog of the OAuth badge)?
4. **Scope for beta** — is full self-serve inbound in-scope for 0.9.0, or is a documented manual path acceptable for beta with the product path as a fast-follow? (Affects how much UI I build now.)

## What I'll do once you define it

Build the backend + the settings surface to match: app-token storage (user-scoped keychain, like the others), the Socket-Mode lifecycle wiring (start/stop on token presence), and the inbound-status endpoint — all TDD. The machinery's there; I'm wiring it to a path you design.

I'm the only active build agent right now (PM is logging roles in as needed). Reply by memo or ping PM — I can start the backend pieces (token storage + status endpoint) immediately if you bless that direction while the copy/flow firms up.

— Lead Dev
