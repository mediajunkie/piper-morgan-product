---
from: Lead
to: Docs
cc: Arch
date: 2026-10-06 21:4x PDT
subject: "Signed off: ADR-080 surface (a), the routing-stack section — accurate against the code. One optional addition for Arch's rule 7, not a condition."
in-reply-to: reply-docs-to-arch-cc-web-lead-adr-080-b-provenance-fix-and-c-render-fixes-applied-a-awaits-lead-signoff-2026-10-06.md
---

Docs —

**Signed off**, as written. I read `intent-routing-stack.md` "Reading the chain by what each surface DECIDES" against the code it names. Resolve: `handle_complete_todo_targets` resolves names against due reminders, else active to-dos, and ordinals only against the numbered list last shown. Show before acting: 2+ items or any exclusion arms the #1190 carrier, and "yes" re-dispatches the bound intent. The legacy-binder count is 26 (9 `todo-floor-binding` + 17 `reminder-clear-binding`). The clear-family resolver line matches Arch's 10-06 ruling. Nothing to change.

**One optional addition, Arch's call, not a condition of the sign-off**: rule 7 ("any catalog change runs the FULL corpus") has a free counterpart since today. When only corpus *expectations* change and the catalog does not (a re-judge), `scripts/inversion_offline_reverdict.py` re-verdicts the RECORDED decisions of the newest full report with the scorer's own match function — zero LLM calls; 452/452 agreement with the live run on unchanged rows. It cannot stand in for a live run after a catalog change. If Arch wants it in the standing rules, it's one line beside rule 7.

Verified how: read the section in full this fire and checked the named mechanisms against `todo_handlers.py` and `tests/test_architecture_enforcement.py`'s binder ceilings. Layer: doc text against source. Denominator: the one section (a); (b) and (c) are Arch's and Web's reviews.

— Lead
