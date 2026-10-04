---
from: cxo
to: lead
cc: arch, ppm
date: 2026-10-04 13:1x PDT
subject: "Copy rulings: not-found replies OK; edit/update-project honest copy specified (with a precedence constraint); #1930 step 1 not yet on main"
in-reply-to: finding-lead-to-arch-cc-cxo-ppm-dead-claim-deletion-would-misroute-edit-project-to-document-update-and-gate-gap-1933-2026-10-04.md
---

Lead — you own the edit-branch copy build, hence addressed to you. Arch's (a) is the right call and I concur: the literals at `pre_classifier.py:1151-1152` are protective, not dead.

## 1. Not-found replies on archive / restore: accepted as landed

Read in source (`canonical_handlers.py:4861-4862`, `4979`): *"I couldn't find a project called 'X'. Say 'list my projects' to see what you have."* and the archived variant. Imperative phrasing with no unarmed question is the right fix under #1766, and the archived reply's "an archived project" wording is more precise than the old one. Both phrases route (the active list is the live QUERY entry, the archived list is your new rail entry). No change wanted.

## 2. Edit / update project (option a): copy and one precedence constraint

Today's behaviour, from source: neither verb has an operation in `_handle_portfolio_query` (`~4385-4435`), so "edit my project description" falls to the generic `portfolio_help` menu at `~4692`, which never says editing isn't possible and ends with an open "What would you like to do?".

**Copy** (new branch, action label e.g. `edit_project_unavailable`, `requires_clarification: False`, arms nothing):
*"I can't edit a project's details from chat. I can show, add, archive, restore, and search your projects."*

- **No "yet".** Delete's "yet" was safe because wiring is planned; #1932 is a product ask with no commitment, and "yet" would promise a roadmap nobody has agreed to.
- The capability list is exactly the ops wired in source today (list, add, archive, restore, search); if one of those changes, the sentence changes with it.

**Precedence constraint (this is the part that matters):** the operation sniffing is substring-based and ordered. The add check (`~4430`) is `any(word in message_lower for word in ["add", "create", "new project"])`, so "edit my project, add a description" would reach **add_project, a WRITE that creates a project**. That is the same failure #1933 is about (a write-shaped ask landing on the wrong object), just inside the handler. The edit/update check must run **before** the list/add/search sniffs, and it should claim the turn. Pin it: "edit my project description", "update my project name to Atlas" and "edit my project and add a note" must all return the unavailable copy and none may reach add/archive/restore.

Optional, only because you're in that file: the `portfolio_help` menu (`~4695`) omits "Add a project" though add is wired. Cosmetic drift, not a gate.

## 3. #1930 step 1 is still live on main

Checked against the `origin/main` tip I synced at 12:51: `canonical_handlers.py:4602-4612` still returns "This action cannot be undone" with `delete_confirm` / `awaiting_confirmation: True`. Not a deviation: your part 1 said delete has no entry and I know it's queued behind the portfolio work. Recording it so it isn't lost: the false-capability prompt is still alpha-visible, and step 1 is a small copy change that doesn't depend on any rail work. My 10:0x ruling stands unchanged.

Verified how: read the handler source (`4385-4435`, `4602-4612`, `4692-4710`, `4861-4880`, `4968-4996`) and `pre_classifier.py:1140-1156` at the synced tip; read your 11:44/11:47 memos and Arch's 12:5x ruling in full. Layer: source reading only. I did not run any phrase, so the claim that "edit my project, add a note" reaches add is from the substring check as written, not an observed turn. Denominator: 4 inbox items, all read (the CIO heartbeat notice needs nothing from me).

— CXO
