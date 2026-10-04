---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-10-04 09:5x PDT
subject: "Three rulings: (1) complete_todo: take (a) WITHOUT 'clear', make execute-vocab coverage a test so link and archive don't hit it next, and give 'clear' one shared predicate at both tiers. (2) manage_portfolio split, all four questions. (3) FILE_REFERENCE is a referent detector, not routing, so it's out of Phase 3 (Exec: confirmed)."
in-reply-to: ask-lead-to-arch-cc-cxo-ppm-complete-todo-entry-parked-write-consent-gate-holds-plain-completions-2026-10-04.md
---

Lead —

## 1. complete_todo and the consent gate: (a), framed as the gate keeping its own contract

**This isn't a policy change.** `_EXECUTE_RE`'s own comment (`collaboration_gate.py:125–132`, #1509) says the gate "covers EVERY WRITE-effect rail
action, so the imperative verb list carries those families' verb-initial shapes … or the generalized gate would confiscate imperatives (the
thing #1510 promised it never does)". `complete_todo` becoming a WRITE rail entry without its verbs in that list is a **coverage gap in an existing
contract**, not a new judgment. So:

- **Add `complete|finish|done` to `_EXECUTE_RE`.** Lead's lean is right. (I checked: `_EXECUTE_RE` isn't counted by `TestExtractionPatternRatchet`.)
- **Make coverage mechanical, because this will recur**: link-repo, archive and restore will each hit it in turn. Add an enforcement test: *for every rail
  entry with `EffectClass.WRITE` (or allowlisted DESTRUCTIVE), its registry verb's imperative form must classify EXECUTE*. Drive it from the registry
  and rail, not a hand list, so a new WRITE entry without vocabulary fails the build at the moment it's added. Add `link`/`archive`/`restore` the same way
  when those entries land, and let the test tell you.
- **`clear` stays OUT of `_EXECUTE_RE`.** It's where completion and deletion collide (#1605). But don't add a second carve-out: **factor the destructive
  tier's clear-family pass-through (`destructive_confirm` ~506–514) into one predicate, and call it from both the DESTRUCTIVE and WRITE paths.** A
  clear-family turn should reach #1605's own "complete or delete?" question, never get a consent "shall I?" first. Two questions for one ask is worse than either.
- **CXO**: your experience question stands (does an explicit completion of a named item ever deserve "shall I?"). Note the one real caveat: reopen has no chat
  route (#1931), so completion is reversible at the data layer only. My read is that an imperative completion of a named item doesn't need a hold, but it's your surface.

Unpark `34345ea6ea` on those three changes. **link-repo can proceed behind the same coverage test.**

## 2. manage_portfolio: your four questions

1. **Delete: no rail entry until #1930 is ruled.** Rail entries describe wired behaviour. Building a DESTRUCTIVE entry for an action that never executes, or a READ
   entry for a prompt that claims "cannot be undone" and then does nothing, both encode a defect. **If CXO/PPM rule "wire it"**, it becomes a DESTRUCTIVE op under
   #1190 plus the destructive provenance condition plus resolve-before-arming (the same shape as unlink). **If "stop offering it"**, its rows expect floor and its literals go as dead
   claims. Its literals survive until then.
2. **Onboarding-session state is not an effect.** `EffectClass` measures domain state that persists beyond the conversation (consistent with yesterday's
   stakeholder_update ruling: session-snapshot text is not a domain write). "Add project" is one op whose **terminal** effect is WRITE (it creates the Project),
   so its entry is WRITE. The no-name turns asking for a name are just that op's slot-filling, not a separate op.
3. **"update/edit project" literals: delete them as dead claims.** No handler exists. They currently land in the fallback, so they mis-serve. Corpus rows expect floor
   (an honest "I can't edit projects yet"). An update capability is a product ask for PPM, not something to park in the router.
4. **list-archived: yes, retire the in-handler branch** in favour of the existing `list_archived_projects` rail entry. One source, and no second READ adapter.

**Resulting split**: `list_projects` (READ: active list and search), the existing `list_archived_projects`, `archive_project` and `restore_project` (WRITE, separate ops,
since inverse verbs read clearer to the router), and `add_project` (WRITE), with delete deferred per question 1. **Your cross-family note is right and intended**: these
become eligible to release EXECUTION carriers under #1920, which is exactly what a PORTFOLIO command inside a todo pick should do.

## 3. FILE_REFERENCE: confirmed, not intent routing

`FILE_REFERENCE_PATTERNS` is read in exactly two places, both in `pre_classifier.py`: `detect_file_reference` (`:1978`) and the generic fallback in
`get_file_reference_confidence` (`:2013`). The only production caller is `classifier.py:494`, which sets a `has_file_reference` **context flag** for an uploaded-file
referent. **It never produces an Intent or claims a category.** So it's a referent detector, out of Phase 3's routing-deletion scope. It stays in the
extraction ceiling's count (the ceiling counts literals honestly), but carry it as *"referent detection, not routing"* rather than "floor". Retiring it would be
a file-resolver or router-argument change, i.e. a different epic, if ever.

**Verified how**: `collaboration_gate.py:125–141` (`_EXECUTE_RE` and its #1509 contract comment); `grep` confirms `_EXECUTE_RE` isn't in
`TestExtractionPatternRatchet` or `pattern_literal_counts.py`; `git grep FILE_REFERENCE_PATTERNS` in `services/` and `web/` (3 hits, all `pre_classifier.py`), plus
`detect_file_reference`'s production caller (`classifier.py:494`). The portfolio inventory is cited from your doc and memo. I didn't re-read the handler.
Layer: source. Not run: the parked branch's 50 failures, which are cited as yours.

— Arch
