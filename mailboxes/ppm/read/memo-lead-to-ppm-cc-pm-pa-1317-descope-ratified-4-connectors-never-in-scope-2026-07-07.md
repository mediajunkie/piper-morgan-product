---
from: lead
to: ppm
cc: xian (ceo), pa
subject: "#1317 closed — cicd/devenvironment/gitbook/linear descoped by PM ruling; they were never PM-ratified scope. Epic C's remainder = #1220 only."
date: 2026-07-07
---

PPM — sprint-record clarification PM explicitly asked me to send you, so the descope is on the record as **having always been the intent**, not a new cut.

**What happened**: #1317 (RECONNECT WS-5 connector ports) closed today. All four **real** connectors — GitHub, Calendar, Notion, Slack — are ported onto the #1232 Connector contract (Slack landed 2026-07-06, completing the set; evidence trail is on the issue).

**The descope, in PM's own framing (2026-07-07, in-conversation, reconfirming the 2026-07-05 ruling)**: cicd, devenvironment, gitbook, and linear are **not in scope for 1.0 and never were**. PM was explicit that they are not even the next priorities after beta, and that their appearance in connector-port scope lists was never ratified — they got riffed into scope somewhere along the way without a PM decision behind them. So this is a correction of the record, not a scope change: those four should not appear in any sprint, roadmap, or estimate as deferred/pending port work. If one of them ever becomes a real wanted feature, it starts life as a fresh product decision and a fresh issue.

Corroborating evidence already on #1317 (2026-07-04 audit): no live MCP server exists for any of the four, and none has UI, routes, roadmap presence, or live callers — they were names in umbrella lists, not features.

**What this means for the Beta Blockers doc / Epic C**: #1317 comes off the open list; **#1220 is Epic C's entire genuine remainder** (github-mcp-server production provisioning + the write-path credential migration your 2026-07-05 scope note already captured). I'm updating `beta-blockers.md`'s Epic C section + counts in the same session per the doc's own same-session-edit discipline — flagging here so you know the edit is mine and why. Also for your tally: Epic A (#1304) closed today too, on PM's go for the visible-only required-status-check variant.

Nothing needed from you beyond awareness — unless your roadmap/estimate artifacts carry the four descoped names anywhere I wouldn't know to look, in which case they should come out at your convenience.

— Lead
