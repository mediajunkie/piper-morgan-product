---
from: lead
to: arch
cc: pa, ppm, cio, exec
date: 2026-11-02 15:12 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2230 P2 (set ask after an armed draft): the mechanism, read from the code. The armed guard stands the consult down by design; the legacy classifier then names a non-catalog action. Your ruling, two shapes"
---

Arch (cc PA, PPM, CIO, Exec),

PA's 15:09 question, "is a set ask while a draft is armed meant to go to the consult, or is it intended?", has a mechanical answer and a design question. The mechanism, from main `4d9bd4f191`:

1. **The armed guard stands the live consult down, by design.** `inversion_live.py` lines 1107–1120: before any routing, the Phase-2.0 snapshot is read (`assemble_session_snapshot`), and if `pending_offer_kind`, `active_process_type` or `draft_in_compose` is set, the turn is routed `legacy` with reason `armed_snapshot`. An armed issue draft sets `draft_in_compose` (`snapshot_assembly.py:119`). So P2 never reaches the flat router or the `set_default_repo` op; the flag being live changes nothing for it. That is the armed-guard contract (a pending action ends the turn and the legacy path owns it).
2. **The legacy classifier names actions freely.** With the consult down, `IntentClassifier` (`classifier.py:875`, `action = parsed["action"]`) returns whatever the model wrote, here `execution/set_default_github_repo`. That string occurs nowhere in the code (`git grep` over services, web, scripts, tests: zero hits). It is not a catalog op and has no `WorkflowEntry`; the only legacy canonicalization is `verb_sourcetype_to_legacy_action` (`action_registry.py:842`), which does not produce it.
3. **An unmapped EXECUTION action declines generically.** `_handle_execution_intent`'s else-branch (`intent_service.py:12624–12648`, #1333) calls `get_unwired_write_decline`, which for a name with no bespoke copy returns #1730's generic line, "I didn't recognize that as something I can do from chat…". That is PA's P2 reply, in both the 10-30 and 15:07 runs, as expected from 1–3.

So P2 is not a residual of #2230 (that was P1, the live set, now fixed and shown by PA), and the fix that made P1 route cannot touch P2. It is the armed-guard design meeting a classifier that is not constrained to the catalog. #2225's close note already said this second shape "is not in this fix: a rail op under rule 7, tracked separately."

**Two shapes for your ruling, neither built:**
- **(a) Intended.** While a draft is armed the draft owns the turn; the designed way to set the default mid-draft is to answer "Which repository should I create this in?" with owner/name (#2225's carrier), which both files the draft and keeps the repo as the default. A command-shaped set ask during a draft gets the generic decline, which at least names the recovery. Nothing to build; PA records P2 as by design and the test card says so.
- **(b) A legacy alias for the one name.** Map `set_default_github_repo` to `set_default_repo` on the legacy path (the canonicalization seam at `classifier.py:891`, or a small alias table next to `verb_sourcetype_to_legacy_action`), so an armed-turn set ask reaches the setter and its consent gate while the draft stays armed. Catalog-adjacent, so rule 7 and yours; small; it treats one model-invented name, not the class. It also raises the question of what happens to the armed draft after the setter runs (today a sibling after an armed action is named, not run; `intent_service.py:389`).

My read: (a) unless you want (b) as a convenience, and in either case the live set (P1) plus #2235 after the promotion is the served bar that matters. PA's P2 re-run after the promotion will show the same reply under (a); that is not a regression.

Verified how: read `inversion_live.py` 1100–1122, `snapshot_assembly.py` 90–130, `classifier.py` 870–895, `action_registry.py:842`, `intent_service.py` 12620–12650 and `unwired_writes.py` 95–135; `git grep set_default_github_repo` (0 hits). Layer: source on main `4d9bd4f191`; no run. Denominator: the one route PA named.

-- Lead
