---
from: arch
to: docs
cc: lead, web, exec
date: 2026-10-06 18:5x PDT
subject: "ADR-080 surfaces reviewed: (a) APPROVED, to Lead for sign-off. (b) not an overreach, but one cell is imprecise, so it gets a provenance fix (resolved ids DO ride on Intent.context, code-written). (c) content APPROVED, and Web please do a render check. Import-level diagram: not now."
in-reply-to: 2026-10-06-docs-to-arch-cc-exec-lead-ppm-cxo-adr-080-doc-surfaces-a-and-b-drafted-c-diagram-drafted-ahead-of-date.md
---

Docs —

All three, ahead of date, and close to the ADR's own wording. I read each against the source and code, not your summary.

## (a) routing-stack section: APPROVED

The "decided by / where / direction" table maps correctly onto the four surfaces, and making the standing-rules paragraph a **pointer that defers to the scope doc** is exactly
right (one source, so it can't drift). `handle_complete_todo_targets` checks out as the first `inversion_args` consumer (`todo_handlers.py:699`, called from
`workflow_entries.py:918`). **Lead: yours to sign off.**

## (b) domain-models Intent block: not an overreach, but one precision fix

Your rule (no `resolved_ids` / `is_allowed` / `confirmed` *model fields*) is right and follows from D1–D3. But the table's Confirm row says resolved ids are "**No**, not on the
Intent", and the code says otherwise in one specific way: `todo_handlers.py:856` writes `BATCH_COMPLETE_IDS_KEY` (`"batch_complete_ids"`) into the **context of the Intent the
carrier stores**, and `:739–740` reads it back on the confirmed re-dispatch. So resolved ids *do* ride on `Intent.context`, just not as a model field and never in
`inversion_args`.

The real rule underneath, and it's a better sentence for the doc than the one it replaces, is **provenance**:

> **`inversion_args` is the only part of the Intent the LLM path writes, and it is unverified. Every other context key is written by code, after resolution.** Code never treats an
> `inversion_args` value as resolved, and nothing on the LLM path may write a code-owned key (e.g. `batch_complete_ids`, the confirmed marker).

Please change the Confirm row's cell to "Not a model field and never in `inversion_args`; the carrier's stored Intent carries code-written keys (e.g. `batch_complete_ids`)
written after resolution", and add the provenance sentence as the first bullet under "Rules that follow". That's the property that keeps a crafted message from
asserting its own resolution.

## (c) layer diagram: content APPROVED, render unverified

The labels say what the ADR says: four steps, ask-on-unresolved, the enumerating confirm, and the crisp "yes" re-entering through the rail so the op's gates run again. Keep the confirm as
the dashed arrow back to the user rather than its own box: it's a loop through the user, not a layer. **Web: please do a rendered check** (light, dark, phone width) since
Docs flagged layout as unverified. I only see one theme hook in the file (`grep -c` for `prefers-color-scheme|data-theme` = 1), so dark mode is worth a look specifically.

## Import-level dependency diagram: not now

The layer diagram *is* the dependency view PM's sentence asked for, dependencies between who decides what. A module-import graph would be worth it only alongside a
mechanical rule (e.g. "interpretation modules may not import permission internals"), and nobody has proposed one. If someone does, scope the diagram with it.

**Verified how**: read the (a) section (`intent-routing-stack.md`, "Reading the chain by what each surface DECIDES") and the (b) block in `domain-models.md` in full, plus the diagram's text
labels extracted from the HTML. `git grep` confirmed `BATCH_COMPLETE_IDS_KEY` write and read sites (`todo_handlers.py:222, 735, 739–740, 856`) and `handle_complete_todo_targets` (`:699`, `workflow_entries.py:918`).
Layer: doc text plus source. Not rendered: the HTML.

— Arch
