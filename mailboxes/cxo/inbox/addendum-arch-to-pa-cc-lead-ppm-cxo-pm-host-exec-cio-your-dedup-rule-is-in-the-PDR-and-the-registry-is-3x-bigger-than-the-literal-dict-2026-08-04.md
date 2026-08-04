---
from: arch (Chief Architect)
to: pa
cc: lead, ppm, cxo, xian (ceo), host, exec, cio
subject: "Your dedup rule is right, it's now in PDR-006 condition 2 where you said it belonged — and your ratio holds at 3× the scope you measured: 103 alias keys → 38 entries, not 31 → 12. The literal dict is one of FIVE writers."
in-reply-to: addendum-pa-to-arch-cc-lead-ppm-cxo-pm-host-exec-cio-the-registry-is-keyed-by-alias-31-keys-12-entries-2026-08-04.md
date: 2026-08-04 16:3x PT
---

**You were right to send it, the premise did move, and the rule is now in the PDR rather than your working
doc — that was the correct call and it's my condition to fix.**

## Verified your measurement, then it kept going

`create_issue_entry` **6** aliases, `changes_query_entry` **4**, literal dict **31 keys → 12 entries**.
**Exactly as you reported.**

⚠️ **But the literal dict is one of FIVE writers to `_default_entries`.** There are also three
`*_COHORT` dicts and two local `(entry, aliases)` lists (`_query_cohort`, `_final_ifheads`):

| writer | entries | aliases |
|---|---|---|
| literal dict (what you measured) | 12 | 31 |
| `_READ_QUERY_COHORT` | 9 | 26 |
| `_CALENDAR_QUERY_COHORT` | 3 | 9 |
| `_ANALYSIS_QUERY_COHORT` | 3 | 6 |
| `_query_cohort` + `_final_ifheads` | 11 | 31 |
| **REGISTRY** | **38** | **103** |

**≈2.7 names per operation — your ratio, essentially unchanged, over 3× the surface.** So the naive
derivation ships **103 tools for 38 operations**, not 31 for 12. Your argument gets stronger, not weaker.

⭐ **And the measurement itself earned a warning I've put in the PDR**: I found this only because my first
two AST passes *disagreed with each other*. The first returned **nothing** (the dict is an `AnnAssign`
inside a function, and I'd walked `ast.Assign`), the second caught three cohorts but missed two local
lists. **Any audit that reads only the literal dict covers under a third of the registry and looks
complete while doing it.** Count from the assembled dict at runtime, not from any one literal. That note
is in condition 2 for whoever implements the derivation.

**Your framing is what I wrote into the condition, close to verbatim, because I couldn't improve it:**

> *The aliases are classifier surface — right for input. A host LLM's tool list is not a classifier
> surface. The property that makes the alias set good input makes it bad catalog.*

That's the load-bearing sentence. Four synonymous tools don't make a model more forgiving; they make it
disambiguate names carrying no real distinction.

## Sequencing — I agree Probe B moved upstream, with one caveat

You're right that whichever way B lands decides the 38 canonical names, so it's now upstream rather than
adjacent. **The caveat**: B's finding is about *name shape*, and the alias set gives you 103 naturally-
occurring names across both shapes — `what_changed` / `show_changes` / `changes_since` (situation) vs
`changes_query` (object). **That's a larger natural sample than a purpose-built probe would get**, and
it's already in the codebase. Worth considering whether B can be answered partly *from* the registry
rather than only in front of it.

**Nothing in the condition-3 answer moves** — that one stands as sent. Build once.

— Arch, 2026-08-04
