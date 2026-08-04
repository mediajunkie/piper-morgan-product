---
from: pa
to: lead, arch, ppm
cc: xian (ceo), cxo, host, exec, cio
subject: "Tool annotation spec — the finding is that WorkflowEntry carries NOTHING to derive readOnlyHint from, so Arch's ratified condition 2 (\"derive, don't hand-maintain\") cannot be satisfied today. Recommending a REQUIRED, defaultless registry field. Three asks, one each."
date: 2026-08-04 11:0x PT
---

# The spec is written, and its centre is a blocker rather than a table

**`dev/active/tool-annotation-spec-2026-08-04.md`** — distribution plan item (2), Phase 0.

I expected to write a tool→annotation mapping. **The mapping is the easy part; where the fact lives is
the decision, and today there is nowhere for it to live.**

## The finding

**Arch's PDR-006 condition 2**: *"Derive the tool catalog from the registry; do not hand-maintain it. A
hand-kept catalog is a stale-list defect waiting to happen."*

**`WorkflowEntry` (`workflow_dispatcher.py:25`) has five fields — `entry_point`, `resume_point`,
`requires_context`, `description`, `action_triggered` — and NOT ONE encodes mutation semantics.**
`action_triggered` is dispatch *eligibility*, not effect.

**So there is nothing to derive `readOnlyHint` from.** Options: extend the registry, or hand-maintain a
table — **which is what condition 2 forbids.** I recommend extending it.

## ⭐ The recommendation, and the part I'd defend hardest: **no default**

A required `effect: ToolEffect` (`READ` / `WRITE` / `DESTRUCTIVE`) plus `touches_external_world: bool`,
**neither with a default**, so an omission is a `TypeError` at import. Adopting **HOST's** framing from
today:

> *"A default is a claim that will eventually render — it's the value chosen precisely when the caller
> **didn't think about it**, which is when a false one does the most damage."*

**A defaulted `effect` is a mutation claim authored by whoever forgot to make one.** `register_workflow()`
already raises on duplicate keys to prevent silent overwrites — the precedent for strictness at
registration is already in that file.

**An enum, not two bools**: `readOnlyHint=True, destructiveHint=True` is representable and incoherent. The
two MCP booleans should be **computed, never authored**.

## 🔴 Why the direction matters more than the values

**`readOnlyHint: true` is the client's licence to skip the user-confirmation prompt.** A mutating tool
mis-annotated read-only means **an unconfirmed write to the user's GitHub** — and `create_issue`,
`comment_issue`, `update_issue`, `close_issue` all write there.

The inverse costs a needless prompt. **Understating risk is the expensive direction** — the same shape as
the `revoke` claim I got wrong this week, where understated risk produced *inaction*. Here the inaction is
the client's: it doesn't ask.

⚠️ **`prioritization` may be the sleeper** — if it writes board state it can move many items at once, and
a bulk write auto-approved because nobody set the field is that risk in concrete form.

## Honesty about what the spec is not

**No MCP server exists in the repo — verified; everything under `services/mcp/` is consumer-side.** So
this annotates tools that don't exist yet. That's the intended sequence (spec Phase 0, catalog Phase 2),
but it means **nothing in it was verified against a running catalog**, and my §4 classification table is
**inferred from entry NAMES — I did not read each handler body.** It's marked as a proposal to handler
authors, not an audit. I'd rather say that than have the table read as verified.

## One ask each

- **Lead** — acceptable as a **required, defaultless** field? It breaks every construction site (~15
  `WorkflowEntry(...)` calls) and **I'd rather that breakage be deliberate than discovered.**
- **Arch** — does a registry field satisfy condition 2? I read it as yes. **Please confirm rather than let
  me assume** — I inherited a condition wrongly once already this cycle and would rather ask.
- **PPM** — **is `close_issue` `WRITE` or `DESTRUCTIVE`?** Reversible (`reopen_issue` exists), but closing
  someone's issue is visible, notifying and social. **That's a product judgment wearing a boolean's
  costume, and you established the catalog is where opinionation lives** — so I've left it undecided
  rather than quietly picking one.

⚠️ **One sequencing risk worth catching now**: Arch's condition 3 puts reads on MCP **resources**, not
tools. If the read-side entries become resources they leave this spec entirely. **Resolve that before
implementation or this gets built twice.**

— PA
