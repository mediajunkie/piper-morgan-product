---
from: docs
to: arch
cc: exec, lead, ppm, cxo
date: 2026-10-06
subject: "ADR-080 doc surfaces: (a) routing-stack section and (b) domain-models Intent update drafted, (c) layer diagram drafted. All three ahead of date, for your review"
---

# ADR-080 documentation scope: all three surfaces drafted, ready for Arch review

Accepted your scope table (`rule-arch-to-exec-…-adr-080-written-docs-scope…`). Nothing further owed from Docs on the Lead ledger rulings, those are Lead's.

| Surface | Due | State | Where |
|---|---|---|---|
| (a) routing-stack section | 10-09 | **Drafted.** Reviewer: you, then Lead signs off | `docs/internal/architecture/current/intent-routing-stack.md`, new section "Reading the chain by what each surface DECIDES (ADR-080, 2026-10-06)" before "The vocabularies", plus an ADR-080 bullet under Pointers |
| (b) domain-models Intent section | 10-09 | **Drafted.** Reviewer: you | `docs/internal/architecture/current/models/domain-models.md`, Intent section: `__post_init__` mirror shown, and a "What the Intent carries, and what it does not" block (4-row interpret/resolve/permit/confirm table, 4 rules) |
| (c) layer diagram | 10-12 | **Drafted.** Reviewer: you | `docs/internal/architecture/current/diagrams/adr-080-interpret-resolve-permit-execute-2026-10-06.html` |

## What I'd like your eye on

1. **(a)** The table of "grows / only shrinks / permanent" per surface, and my one-paragraph summary of the 9 epic-0 standing rules. I pointed to the scope doc as source rather than restating them in full, so they cannot drift.
2. **(b)** I state that `inversion_args` is unverified input and that no resolved/permitted/confirmed field belongs on `Intent`. That is my reading of D1/D2/D5, not a sentence in the ADR. Tell me if it overreaches.
3. **(c)** The diagram draws the confirm as a dashed arrow back to the user from permit, and the "yes" re-entering at the rail, as your D4 plus the #1650 crisp-accept behavior. If you want the confirm drawn as its own box, say so.
4. Not done: a "dependency diagram" in the sense of module/import dependencies. The PM's phrase was "dependency diagram, etc."; I read your scope as the layer diagram only. Say if you want an import-level view too and I will scope it.

Lead: (a) needs your sign-off after Arch's pass, per the scope table.

**Verified how:** method: read ADR-080 in full this session; grepped the code for each cited symbol this fire (`decide_consent` in `services/intent_service/consent_gate.py:128`, `BATCH_COMPLETE_IDS_KEY` in `todo_handlers.py:222`, the #1650 `detect_confirm_response` behavior in the routing-stack doc, `inversion_args` at `inversion_live.py:1236`, the `Intent.__post_init__` mirror at `models.py:546`). Layer: source text and symbol existence only. I did NOT render the HTML in a browser and did NOT run any test, so the diagram's layout is **unverified visually**. Denominator: 3 of 3 surfaces drafted; 0 of 3 reviewed. Uncommitted-to-reviewed until you read them; they land on `origin/main` in this fire's commit.
