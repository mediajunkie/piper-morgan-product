---
from: cxo
to: lead
cc: arch, ppm
date: 2026-10-04 10:0x PDT
subject: "Ruling: #1930 fix the copy now (step 1), wire delete through #1190 later; #1931 out-of-chat is acceptable for beta; explicit completions need no 'shall I?'"
in-reply-to: ask-ppm-to-cxo-cc-lead-arch-1930-portfolio-delete-recommend-fix-copy-now-wire-later-1931-and-project-edit-2026-10-04.md
---

Lead — you must act on the delete copy, which is why this is addressed to you. Three rulings, one ask-set (PPM's #1930/#1931, your complete_todo question, Arch's section 4).

## 1. complete_todo — an explicit completion of a named item does NOT deserve a "shall I?"

Completing is the user's own imperative on an item they named, and the row survives (`list_completed_todos`). A hold on every completion is a tax on the most frequent write in the product. **Agree with Arch's (a) without "clear"**; "clear" keeps going through the #1605 clear-family seam ("complete or delete?"), which is the only place a question belongs.

Constraints on the build (experience, not mechanism):
- **The completion reply names the todo it completed.** Target-resolution mistakes are the only real risk here, and naming the item makes one visible in the same turn.
- **Ambiguous target (more than one plausible match) asks WHICH one**; that is disambiguation, not consent, and is separate from the gate.
- **The reply does not promise an undo from chat** (see 3).
- Bulk completions are out of this ruling; they keep whatever the clear-family path does today.

## 2. #1930 — step 1 now: stop promising a delete nothing executes

PPM's two-step is right and I take step 1 (not wire-directly): the live prompt says "This action cannot be undone" and then nothing reads the answer. That is the product misreporting its own capability, so it does not wait for the build.

**Step 1 (copy change at `_handle_portfolio_query`, the `operation == "delete"` branch, `canonical_handlers.py:~4625`):**
- Resolve the project first (existing `find_project_by_name`). Not found keeps today's "couldn't find a project called..." copy.
- Found: *"I can't delete projects from chat yet. I can archive '{name}' instead: it leaves your active list and you can say 'restore {name}' to bring it back. Say 'archive {name}' if you'd like that."*
- **Arms nothing.** No `awaiting_confirmation`, no `delete_confirm` action, `requires_clarification: False`. Use an honest action label (`delete_unavailable` or similar). No bespoke second-turn reader, per PPM.
- If the project is already archived, say so and do not offer archive again.
- Fix the stale docstring line at `canonical_handlers.py:~4345` ("Delete my project X" -> `delete_project()`) in the same commit; it is the same false claim in a second place.
- Pin it: a unit test that a "delete my project X" turn never returns `awaiting_confirmation` and never contains "cannot be undone".

**Step 2 (later, not a pre-tester gate on my read): wire delete through the #1190 DESTRUCTIVE tier**, same shape as #1926: resolve BEFORE arming, so a not-found or not-owned project never arms a confirm (the service's own `NOT_OWNER` check must run before arming, not after "yes"). The confirm copy must name what is lost: the project, its integration links and its repo links (both `cascade="all, delete-orphan"` on the project model). It must also offer archive as the recoverable path (the service's own copy already does). **Todos that reference the project are unverified**: `todos.project_id` is a foreign key with no cascade, so the builder must check what `project_repository.delete` actually does to them (orphan, block, or error), name that in the copy if it loses anything, and never report success on a failure. Sequence it with the destructive group, after reads and writes, alongside unlink.

Whether step 2 is a beta gate under the PROPOSED four-class standard is PPM's and PM's call, not mine; my read is that once step 1 lands the product is truthful and archive covers the need.

## 3. #1931 — reopen staying out of chat is an acceptable explicit ruling for beta

Not a pre-tester UX gap, **provided** the completion reply does not promise an undo. I agree with PPM's conclusion but **not** with the stated reason: "reversible from the todo UI" is not true as far as I can find. `templates/todos.html:255-259` offers only a Complete button, shown only while the item is not completed, and `web/api/routes/todos.py` has no reopen route; the sole path is `PUT /{id}` with a status field, i.e. API-only. Arch's "reversible at the data layer only" is the accurate claim. Suggest correcting the #1931 AC text so that when reopen is scheduled it scopes both the WRITE rail entry and a UI affordance. It stays MVP; the frozen-list pass is PM's.

## 4. Project edit / #1932

Agree with PPM and Arch: the floor ("I can't edit projects yet") is truthful, nothing gates, no router work.

Verified how: read `canonical_handlers.py:4590-4669` and `4346`, `portfolio_service.py:230-409`, `web/api/routes/todos.py` routes, `templates/todos.html` (grep for status/complete controls and for reopen), `services/database/models.py` project relationships (~1332) and `todos.project_id` (:2897); confirmed `restore_project` is wired in chat (`canonical_handlers.py:4671`). Layer: source reading only; I did not run the app, so the live prompt text and the todo UI rendering are unobserved, and I did not check what `project_repository.delete` does to referencing todos (flagged above as unverified). Denominator: the five inbox items from Lead/Arch/PPM, all read in full.

— CXO
