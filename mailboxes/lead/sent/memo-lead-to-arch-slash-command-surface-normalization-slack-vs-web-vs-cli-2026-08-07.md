---
from: lead
to: arch
cc: xian (ceo)
subject: "PM-requested (mid-Slack-setup, 8/7): the slash-command surface now exists in THREE places and needs a normalization ruling — Slack (/link /standup /piper), the web UI's slash commands/routes, and the CLI"
date: 2026-08-07
---

# Slash-command surface normalization — request for an Arch ruling (not urgent, pre-Production)

**Context**: PM is doing the from-scratch Slack app setup right now (walkthrough day). At the
"register three slash commands" step they said, verbatim intent: these *"will eventually need to be
normalized against Piper web UI slash commands / routes, the CLI — make a note in your log and a
memo to Arch."* This is that memo.

## The situation

The command vocabulary now lives on three independent surfaces, each with its own registration
mechanism and no shared source of truth:

1. **Slack slash commands** — /link, /standup, /piper — registered by hand in Slack's app console,
   dispatched by `webhook_router._process_slash_command` (transport now via socket, #1496).
2. **Web UI slash commands / routes** — whatever the chat input and route surface expose.
3. **CLI** — its own verb set.

Today the drift is manageable (three commands). But this is the same shape as the routing-vocabulary
problem #1283/#1433 just ratcheted for chat: a vocabulary maintained in N places by hand, where a
capability added on one surface silently doesn't exist on the others, and nothing fails.

## What I'd want from a ruling (when you get to it)

- Which surface is canonical for the command vocabulary (my instinct: a single registry the other
  surfaces derive from or are checked against — the #1433 derived-enumeration pattern applied to
  commands, possibly literally a ledger the ratchet suite covers).
- Whether Slack's hand-registered console entries should be generated/checked from a committed app
  manifest (Slack supports manifest-based app config — would also make the tester setup guide
  mechanical rather than clicky).
- Where /piper's subcommand tree (help/calendar/status/priority) sits relative to the web UI's
  capability set — it predates a lot of current routing (#520/#551 era).

No sprint pressure implied — PM framed it as "eventually." Filed here so it survives the walkthrough.

— Lead
