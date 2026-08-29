# "No optional complexity" — a standing lens for PDR/gate-writing time

**Status**: Proposal, PA-authored, for PM's ratification. Not yet adopted as process.
**Origin**: PM's principle, named live during the 2026-08-26 BYOC/connector-architecture conversation
with PA (`dev/2026/08/26/2026-08-26-0712-pa-code-log.md`), applied that day to a real audit (Position 3
→ the beta/public-beta/production connector-gate review), and sharpened by a second, independent
finding on 2026-08-27 (this document).

## The principle, in PM's words

> "I have a principle: no optional complexity. It's a rule because it is so easy to forget. Repeatedly
> on this project the pull toward scope creep in the name of an ideal vision has weighed and slowed us
> down, wasting time on optional matters that aren't needed till a simpler case is proven."

## The test

**Single-case-first.** For any dimension of scope in a PDR, gate, or milestone — a connector, a
provider, a capability tier, a parallel implementation path — ask directly: **has one real case
already proven this is needed, or is it here because it seemed complete, symmetric, or future-proof?**
If no proven case exists, it's a candidate to cut or defer, not a candidate to build "just in case."

This is deliberately narrower than a general complexity audit. It doesn't ask "is this code good" — it
asks "does this scope item have a proven reason to exist yet."

## Why it needs to be a lens, not a one-off sweep

The 08-26 backlog read (all 60 open MVP-milestone issues) found this pattern barely shows up as
individual tickets — the backlog is dominated by real correctness defects, not breadth-of-scope. **That
was the right finding for a backlog sweep, and the wrong place to conclude the principle doesn't have
teeth.** The pattern doesn't live in the backlog; it lives in **PDRs and gates at the moment they're
written**, before the resulting scope items ever become individual tickets. A sweep after the fact
finds the tickets that already exist — it can't find the scope that a differently-written gate would
never have created. Applying the test at PDR/gate-authoring time is the only point where it can
actually prevent the pattern rather than just audit its aftermath.

## Two layers, not one — the second found today

The 08-26 audit applied one layer: **does a proven case exist for this scope item at all** (the
connector-gate review — GitHub yes, Slack no, Notion marginal, Calendar unclear). Today's follow-up
work surfaced a second, distinct layer that the first doesn't catch:

**Layer 2 — architecture-honesty check: does the abstraction's shape match what's actually underneath
it?** A component can pass Layer 1 (a proven case exists for having *some* Slack connector) while
failing a check Layer 1 never asks: is the thing built the way it should be, or does its interface
merely *look* like the current-best-practice shape while wrapping legacy bespoke work underneath?

**Concrete evidence, verified today, not assumed**: GitHub, Slack, and Notion all now ship official,
vendor-hosted remote MCP servers (`api.githubcopilot.com/mcp/`, `mcp.slack.com/mcp` — GA 2026-02-17,
`mcp.notion.com/mcp`) — the architecture PM described in this conversation ("support MCP connectors
broadly, enable specific ones") is real and available now, not aspirational. Checking Piper's own
`services/mcp/consumer/` adapters against it: `github_adapter.py` is mostly the real thing (8 live
`call_tool()` sites), but `slack_adapter.py` and `notion_adapter.py` are connector-**contract** shims
(`connect/status/resolve/degrade`, ADR-070 D5) with **zero** real MCP tool calls underneath — all
actual data operations still run through each vendor's bespoke REST API. The shim's presence can read
as "this connector is on the current architecture" when only the outer contract is; the migration
itself never happened for two of three.

**Why this matters for "no optional complexity" specifically**: #1572 was about to add new code
(`users.info.tz` capture) to exactly the bespoke Slack surface that Layer 2 flags as the most likely to
be replaced or deferred — investing further in code whose shape is already the wrong one to keep is a
sharper case of the same failure the principle names, not a separate problem.

## How to apply it (proposed)

At PDR-writing time and at gate-writing time — **before ratification**, not as a retrospective sweep:

1. **List each scope dimension separately** (each connector, each provider, each capability tier) —
   don't let a gate's prose bundle them ("all four core connectors") in a way that hides that they have
   different proof-of-need status.
2. **For each item, answer Layer 1**: what single case proves this is needed *now*, at this milestone —
   not eventually, not for completeness.
3. **For each item with real underlying code, answer Layer 2**: does its current implementation
   actually match the architecture the PDR claims, or does it only present that way? (Grep for the load-
   bearing call, don't trust the module docstring or class name — the same "source vocabulary is not
   source verification" discipline that's bitten this project before.)
4. **Write both answers into the gate/PDR text itself**, not into a side memo — so the next person
   reading the gate doesn't have to re-derive what's proven vs. assumed.

## Relationship to existing work

- **Distinct from #1522** (the PM-directed false-trails/dead-code audit) — that issue's scope is
  *accidental* complexity (dead code, parallel unused systems, things nobody meant to leave running).
  This principle is about *deliberate* premature breadth — scope someone chose to build ahead of proof.
  Different failure modes; cross-referenced in #1522's comments, not merged into it.
- **Feeds the connector-milestone decision** currently live with PM (Slack/Notion/GitHub/Calendar
  placement) — this document is the generalized version of that specific conversation, written so the
  next PDR doesn't have to rediscover the same shape of question from scratch.

## Recommendation

Adopt as a standing lens applied at PDR/gate-authoring time, not a one-time audit. If ratified, the
named principle itself ("no optional complexity," PM's exact words above) is worth a `decisions.log`
entry in its own right — distinct from this proposal, which is about *when and how* to apply it.

— PA, 2026-08-27
