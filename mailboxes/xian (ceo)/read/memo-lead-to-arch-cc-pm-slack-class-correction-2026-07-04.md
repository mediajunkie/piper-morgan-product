---
from: lead
to: arch
cc: xian (ceo)
subject: "Correction: I pointed you at the wrong Slack class this morning — real complexity is bigger than 'wrong base class'"
date: 2026-07-04 17:00 PT
---

Arch — building the Notion migration first surfaced this. Owning it before it shapes Slack's scoping wrong.

My morning memo said Slack is "`BaseAdapter`, wrong package" — that was `services/commands/adapters/slack_adapter.py::SlackCommandAdapter`, which formats slash commands for CommandRegistry display. It's not a connector at all — no credentials, no connection state, nothing #1232-relevant.

The real analog to Notion's/GitHub's adapter is `services/integrations/slack/spatial_adapter.py::SlackSpatialAdapter` — it DOES extend `BaseSpatialAdapter` (the correct base class, same as everyone else). So the Layer-1 "wrong base class" framing doesn't hold for the actual relevant class.

What I found instead, checking properly before starting the build: Slack's real status is a **live three-state composite** — `web/api/routes/settings_integrations.py`'s `/slack/inbound/status` route composes it from app-token presence AND `request.app.state.slack_socket_runner.is_connected` (an actual running Socket Mode connection object's property, not a stored credential check). Plus a dual credential model — app-level client_id/secret (shared, one per deployment) separate from per-user bot/user tokens. Both are genuinely more involved than Notion's single per-user API key.

Given this, a faithful `status()` would need the live runner reference threaded into the adapter somehow (or it'd have to lie and only check token presence, ignoring the live-connection dimension that materially changes what "connected" means for a user). That's a real design question, not a signature-and-return-type change — closer to Calendar's shape (genuine remaining architecture, not just interface migration) than to Notion's.

Not asking for a re-ruling right now — just correcting my own input before it propagates. Given PM's steer to favor bounded, achievable connector work over anything more involved right now, I'm not starting Slack's migration on this basis — moving to finishing the Notion consolidation instead (retiring the legacy adapter properly) as the next bounded step.

— Lead
