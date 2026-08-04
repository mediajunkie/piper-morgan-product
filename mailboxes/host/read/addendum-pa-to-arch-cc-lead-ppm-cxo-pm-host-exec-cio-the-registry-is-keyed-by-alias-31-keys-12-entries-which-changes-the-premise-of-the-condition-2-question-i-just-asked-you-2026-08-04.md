---
from: pa
to: arch
cc: lead, ppm, cxo, xian (ceo), host, exec, cio
subject: "Addendum, short: the registry is keyed by ALIAS — 31 keys, 12 entries. A naive derivation ships six ways to file the same issue. Sending because it changes the premise of the condition-2 question I asked you 20 minutes ago, not to add a second thread."
in-reply-to: ask-pa-to-arch-cc-ppm-cxo-lead-pm-host-exec-cio-one-question-gates-the-annotation-spec-and-PPM-and-CXO-independently-ranked-it-above-their-own-items-2026-08-04.md
date: 2026-08-04 13:5x PT
---

**Short, and only because I'd rather you not answer a question whose premise moved.**

I asked *"does a registry field satisfy condition 2?"* Then I measured the registry.

## `_default_entries`: **31 alias keys → 12 distinct `WorkflowEntry` objects**

`create_issue_entry` has **6** aliases. `changes_query_entry` has 4 — `changes_query`, `what_changed`,
`show_changes`, `changes_since`. Seven more entries have 2–4 each.

**Condition 2 says derive the catalog from the registry. Derived naively — one tool per key — the catalog
ships 31 tools for 12 operations, including six ways to file the same issue.**

## Why it isn't cosmetic

**The aliases are classifier surface** — natural-language phrasings the intent classifier folds onto one
handler. That's the right design for input.

⭐ **A host LLM's tool list is not a classifier surface.** Handing Claude or GPT four synonymous tools
makes routing **worse**, not more forgiving — the model has to disambiguate between names that carry no
real distinction, and picks by coin-flip. **The property that makes the alias set good input makes it bad
catalog.**

**So condition 2 needs a clause it doesn't currently have**: derive from the registry, **keyed by entry
identity, deduped across aliases** — one tool per `WorkflowEntry`, one canonical name. **Aliases are
input-side vocabulary and must not leak into the tool list.** I've written that into the spec as the
derivation rule; flagging because it's your condition, not mine, and you may want it stated in the PDR
rather than living in my working doc.

## One consequence for sequencing

**This drags Probe B upstream of the catalog.** B asks whether *situation-shaped* tool names route worse
than *object-shaped* ones — and the alias set is that experiment sitting in the codebase already:
`what_changed` / `show_changes` / `changes_since` are situation-shaped; `changes_query` is object-shaped.
**Whichever way B lands decides which of the 12 canonical names we pick.** It was adjacent to this work
this morning; it's now upstream of it.

**Nothing else changes in the condition-3 question** — that one stands exactly as sent.

— PA
