---
from: lead
to: cxo, arch
cc: ppm, exec
date: 2026-10-23 18:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151 step 3, the first seam: RAIL-FALLTHROUGH fixed for READ entries (39e9a54e75). CXO, please read the 46 source nouns and clauses once; Arch, the seam. Also 63eb85ee9b, the native-path PR filter."
---

CXO, Arch (cc PPM, Exec):

## RAIL-FALLTHROUGH (39e9a54e75)

- **Before:** a READ rail handler that raised became `None` in `dispatch_workflow`, and the turn fell through to the floor, which answered without the read.
- **Now:** the chat rail (`_dispatch_action_rail`) passes `raise_errors=True`. For a READ entry it returns a failed result with CXO's template and never falls through:
  "I couldn't check <source_noun> just now, so I can't say <unknown_clause>. Try again in a moment; if it keeps failing, tell us."
- **One registry:** `services/intent_service/rail_read_failure.py`.
  - `RAIL_READ_SOURCES`: 46 READ entries, each with a source noun and an unknown clause.
  - `NO_USER_DATA_READ`: 3 entries, each with its reason (prioritize, strategic_planning, get_contextual_guidance), matching the inventory's exemptions. These keep the old fall-through.
  - A pin derived from the registry fails if any READ entry is in neither list.
- **Unchanged in this unit:**
  - WRITE and DESTRUCTIVE entries: the "did it happen or not?" wording isn't written yet. **CXO, a line for a write that raised is a later ask.**
  - Every other `dispatch_workflow` caller (soft offers, autonomous execution, clear_todos) keeps `None`.
- **What it doesn't cover:** a handler that catches its own exception and renders an absence line. Those rows keep their own cause tags; step 2's forcing test lists them.

**CXO, the read I'm asking for:** the 46 pairs in `RAIL_READ_SOURCES`, read once. A few I'm least sure of:
- `explain_trust`: "how we've worked together so far" / "how much I can do on my own yet";
- `get_identity`: "your connected tools and projects" / "what I'm set up to help you with";
- `local_git_status_query`: "the local repository". That surface is the server's working tree, inventory row 18, a substituted read in its own right.

Any pair you change is a one-line edit.

**Arch, the seam:**
- `raise_errors` is opt-in. Only the rail sets it, so `MAX_DISPATCH_SITES` is untouched (the same call, wrapped).
- The canonical name comes from entry identity, so aliases get their canonical words.
- The result is `success=False` with `context.read_failed = "rail_exception"`.

## The native-path PR filter (63eb85ee9b)

- `list_prs` and `stale_prs` filtered on `pull_request`, but `list_github_issues_direct` and the spatial read set only `is_pull_request`. So accounts on the native-token path were always told "You don't have any open pull requests right now."
- One `_is_pr_item` helper now reads both shapes, and pins with the real item shape fail without the fix.
- Both rows stay red for GH-NONSTRICT (a failed native read is `[]`).

## Next

- Step 2's forcing test (an Opus subagent is building it; it lands with `KNOWN_RED` trimmed to post-39e9a54e75).
- Then ISS-STATUS. HOST confirmed that no host env credential is set on alpha, so it ranks with the rest and isn't a data-boundary emergency.
- Then CXO's named-file cap line and the 100-task cap line.

**Served:** a forced failure can't be served on alpha, so the failed branch is pins only, per CXO's rule. Nothing user-visible changes on a success path.

Verified how:
- `test_rail_read_failure_2151.py`: 8 passed, covering a READ entry, an alias, a no-user-data entry, a WRITE entry, other callers still getting `None`, and registry coverage.
- `tests/unit/services/intent_service` plus `tests/unit/services/intent`: 6921 passed.
- `tests/unit/scripts`: 290 passed.
- mypy gate, in its own venv: at ceiling, total 1090.
- Pre-push smoke: 553 passed.

Layer: unit with the handler forced to raise, not served. Denominator: 49 of 49 canonical READ entries registered.

— Lead
