---
from: lead
to: arch
cc: xian (ceo), pa
subject: "RECONNECT connector alignment — slack/notion/gitbook don't share github/calendar's model; PM asked for your ruling"
date: 2026-07-04 11:00 PT
---

Arch — PM just refocused RECONNECT: the sprint succeeds or fails on getting all 8 connectors onto one contract with the old bespoke models deprecated, worked one connector at a time (github first, fully done, then calendar, then the next). PM asked me to bring you the architectural-divergence findings from today's #1317 audit cascade, with the explicit goal: **bring everything in line with the same domain model and architectural planning, and only allow exceptions when they're justified by something specific about that connector's nature or job-to-be-done** — not accumulated inconsistency.

Full audit is on [#1317](https://github.com/mediajunkie/piper-morgan-product/issues/1317#issuecomment-4883222991). The pieces that look like they need your ruling rather than mine:

**1. Slack doesn't share the contract's base class or credential model.** `services/commands/adapters/slack_adapter.py` extends `BaseAdapter`, not `BaseSpatialAdapter` — it isn't even matched by the `*_adapter.py` glob the #1232 m-41 guard scans in `services/mcp/consumer/`. It uses the keychain credential model (ADR-058), not the `Binding`/`ConnectResult` model the #1232 contract assumes. Question: does the 4-method contract (`connect`/`status`/`resolve`/`degrade`) get adapted to accommodate a keychain-backed connector, or does Slack's credential model migrate to match the binding model? Or is keychain-vs-binding a legitimate permanent split (e.g. if it tracks a real difference in how those services authenticate) — and if so, should the *contract itself* grow a variant for that case rather than treating it as an exception?

**2. Notion's `connect()` already has an incompatible signature.** `services/integrations/mcp/notion_adapter.py`: `connect(self, integration_token: Optional[str] = None) -> bool` — different args, different return type, than the contract's `connect(self, user_id: str) -> ConnectResult`. Same keychain-model question as Slack.

**3. GitBook has two adapter copies.** `services/mcp/consumer/gitbook_adapter.py` (unported, same shape as cicd/devenvironment/linear) and an older `services/integrations/mcp/gitbook_adapter.py`. Didn't dig into which one is canonical — flagging the duplication rather than guessing.

**4. There's a live duplicate spatial tree.** `services/intelligence/spatial/` (2 files: `gitbook_spatial.py`, `notion_spatial.py`) overlaps with `services/integrations/spatial/`'s equivalents. The `intelligence/` copy isn't dead — `cli/commands/notion.py` and `services/features/notion_queries.py` import it live. So this is real duplication between two parallel trees, not one dead one. Untangling which is canonical wasn't attempted today (out of scope for the audit pass) — flagging for whoever ends up owning that connector's port.

**Context, not a request**: PM confirmed separately that cicd/devenvironment/gitbook/linear having no live MCP server today is expected — creating/connecting those servers is itself part of the sprint's point, not a blocker to flag. Not asking you to weigh in on that; just didn't want the absence of a server to read as a surprise finding when you look at #1317.

**On timing**: per PM's new sequencing, I'm heads-down on finishing github (connector #1) completely before touching calendar or anything else, so I'm not blocked waiting on your ruling here — this is queued for whenever you get to it, not gating my next steps. Whatever you decide will shape how connector #3+ get scoped once calendar's done.

— Lead
