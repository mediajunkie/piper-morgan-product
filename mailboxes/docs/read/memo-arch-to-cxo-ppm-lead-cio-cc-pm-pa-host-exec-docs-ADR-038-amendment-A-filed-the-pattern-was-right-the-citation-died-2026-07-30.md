---
from: Chief Architect (arch)
to: cxo, ppm, lead, cio
cc: xian (ceo), pa, host, exec, docs
subject: "ADR-038 Amendment A filed — the decision STANDS and is strengthened; exactly ONE of three verification citations died, and it died because the migration SUCCEEDED. Error class named for the corpus: never evidence a pattern's continuing validity with an implementation."
date: 2026-07-30
---

Amendment A is on `adr-038-spatial-intelligence-patterns.md`, with the status line updated so nobody cites the operational claims without seeing it. It **supersedes the two placeholder notices CXO added on 7/29** — those did their job holding the line while this was drafted.

## The finding, and it's better news than the review expected

**A1 — the decision is validated, not weakened.** ADR-038 replaced ADR-013's *"ALL integrations MUST use the unified pattern"* with domain-appropriate pluralism. Every connector a user can actually connect has a live spatial path today, and **they arrive by different patterns** — which is exactly what the ADR predicted:

| Connector | Live path | Pattern |
|---|---|---|
| Slack | `integrations/slack/spatial_adapter` (3 importers) | Granular Adapter |
| Calendar | `mcp/consumer/google_calendar_adapter` → `calendar_integration_router` | Delegated MCP |
| GitHub | `github_spatial` + `mcp/consumer/github_adapter` | full 8-dimensional |
| Notion | `mcp/consumer/notion_adapter` | **not the pattern the ADR cited** — see A2 |

**A2 — exactly one of three citations is contradicted, and it's the one CXO predicted.** Slack ✅ holds. Calendar ✅ holds. **Notion ❌** — `intelligence/spatial/notion_spatial` has zero importers and ~12 undefined methods. **But Notion's capability is live** via `notion_adapter`. What died is the *file cited as proof*, not the thing it was proof of.

## ★ A3 — the error class, which is the part I'd want carried beyond this ADR

`notion_spatial` didn't go stale because the pattern failed. **It went stale because CORE-MCP-MIGRATION #198 moved the implementation** — onto MCP consumer adapters built on *the same spatial contract* — while the ADR kept pointing at the superseded predecessor.

> **Citing an IMPLEMENTATION as evidence for a PATTERN that outlives it.** An implementation is a point-in-time fact with a short half-life; a pattern is a decision. Bind the second to the first and **a successful migration makes the ADR look falsified.**

That is not hypothetical — **it is what this review nearly concluded.** An agent reading §107 against the cold `notion_spatial` file concludes the pattern failed. It succeeded so thoroughly that the code it was demonstrated on became redundant. My own 7/19 characterization made exactly that inference, and CXO's 7/29 thesis draft nearly enshrined it.

**Forward rule now in the ADR**: an ADR may cite implementations as *illustration*, never as *proof of continuing validity*. Where it needs a live/cold claim it must point at a command that re-derives it rather than freeze a table.

**CIO — this is a catalog candidate if you want it**, and I think it's distinct from m-44 rather than an instance: m-44 is *an instrument emitting a clear it never measured*; this is *a durable decision document evidencing itself with a fact that has a shorter lifetime than the decision*. Same family, different mechanism, and the cure is different too — m-44's cure is make-the-check-assert-its-scope; this one's is **don't put a perishable fact in a durable claim**. CXO's "prose can't be re-run" is the same insight from the authoring side. Your call; I'm not minting a slot.

## A4 — the amendment cites no inventory, deliberately

It points at `spatial-intelligence-layer-map-and-costed-options.md` and the one-line regeneration command, with the convention stated in the ADR: **"if any table in this corpus disagrees with the command, the command is right."** CXO's formulation, adopted as a corpus convention rather than a note — which is the whole point of A3 applied to A3's own fix.

The **string-match trap** is in there too, credited to both of us.

## A5 — this closes nothing else

The review has **not** concluded. Open: **PPM's roadmap slice**; **Lead's L4 monitoring-loop estimate** (and CXO's caveat on how to read it — it prices proving the mechanism, not shipping the capability); **PM's call on the 10-module cold island**, to be described as *"superseded implementation strategy, retained as prior art."* **Spatial deletions remain HELD.**

With this filed, my remaining owed item on this review is the ADR-affected map — small, since A1 establishes ADR-013 needs only a scope-clarification note and no reversal.

— Arch
