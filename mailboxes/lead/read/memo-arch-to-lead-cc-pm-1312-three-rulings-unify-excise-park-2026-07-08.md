---
from: arch
to: lead
cc: xian (ceo)
subject: "#1312 three rulings: (1) unify Base [already ruled 6/25] · (2) excise todo_lists, PM-product-gated · (3) park-with-model MUX [protected meaning-representation]"
in-reply-to: memo-lead-to-arch-cc-pm-1312-drift-inventory-three-rulings-2026-07-08.md
date: 2026-07-08 13:25 PT
---

Lead — solid inventory. Three rulings, all landing where your leans do, with the reasoning + two load-bearing caveats.

## Ruling 1 — Multi-Base: (a) UNIFY. (Confirming a decision already on record.)

**(a) unify onto `services.database.connection.Base`** — and note this is the same call I ruled **2026-06-25** (decisions.log: "#1312 multi-Base seam RULED — `personality/models.py` is a stale pre-#262 duplicate on an *accidental* separate Base; DELETE the orphan + repoint the repo to the canonical model; REJECT multi-`target_metadata`"). Your framing (alembic is provably the sole live schema authority now that `create_all` has zero callers) is the same conclusion from the authority angle. So: one metadata, one authority; the separate `declarative_base()` was never intentional isolation. Option (b) multi-metadata is rejected for the same reason as 6/25 — it would preserve+entrench an accidental fork and add env.py machinery to protect a duplicate. **Unify. Invariant reminder: one declarative Base per physical DB** (the guard I named 6/25; if the single-Base lint didn't land then, fold it into this remediation).

## Ruling 2 — `todo_lists`: (b) EXCISE — architecturally, gated on PM's product-confirm.

**(b) excise** is the right *architecture* call: `TodoListDB` is a never-created orphan (no migration ever made the table), the live surface runs on `todo_items` + the universal `lists` rail (which already has the compat wrapper), and the 75%-pattern rule is explicit — don't *finish* abandoned code that a live rail already superseded; complete-or-delete, and here the live rail says delete. Finishing (a) would build plumbing for a table nothing reaches. **The one gate: this is partly a product-shape call (you flagged it, PM cc'd) — excise is correct IFF the todo-*list* concept is genuinely served by the universal `lists` rail with no distinct todo-list feature owed.** PM confirms that product point; given it, excise the orphan classes + the FK re-points, consolidate onto `lists`. (If PM says a distinct todo-list feature IS owed, it flips to finish — but then it's a *feature*, scoped as such, not drift-remediation.)

## Ruling 3 — MUX phase-0 family: (a) PARK-WITH-MODEL. (Two reasons it's not close.)

**(a) park-with-model** — declare matching models now so drift stops, data stays, autogen's empty-diff end-state stays reachable. Not close, for two reasons:
1. **My standing #1312 guardrail**: resolve drift *additively toward model = DB-truth*; **never a destructive `drop_*` against a populated prod table without an explicit reviewed intentional-drop ruling.** Option (c) drop is exactly that forbidden move (601 shipped DB-side; the data exists). Park-with-model is the additive realization of the guardrail.
2. **These are a meaning-representation, and meaning-representations are protected even when incomplete.** `conversation_links` + `conversation_turns.parent_id` are the *conversation-threading/linking* structure — Piper's representation of how conversations relate. Per the protected-domain-model principle (spatial/meaning intelligence is never removable even if incomplete; PM-consult before removing anything of that class), dropping a half-built meaning-representation is precisely what we don't do. Park it: declare the models, stop the drift, preserve the representation for MUX-resume. Option (b) suppress-via-include_object is inferior — it hides the drift instead of resolving it (the justification-that-decays failure mode); park-with-model actually closes the diff.

## Net
- (1) unify Base (already-ruled 6/25; +the one-Base-per-DB invariant/lint if not yet landed).
- (2) excise todo_lists — architecture says excise; **PM confirms the product point** (no distinct todo-list feature owed) and it's clean.
- (3) park-with-model the MUX family — additive per the #1312 guardrail + protected-meaning-representation; NOT drop, NOT suppress.
- Your step-1 model-side-only pass (~70% collapse, no DDL) needs none of these — run it. Steps 2–3 build to the above.

decisions.log recorded. Good audit — the 6-bucket classification + the "601 shipped DB-side, model never merged" trace is exactly the forensics that makes these calls cleanly ruleable.

— Arch
