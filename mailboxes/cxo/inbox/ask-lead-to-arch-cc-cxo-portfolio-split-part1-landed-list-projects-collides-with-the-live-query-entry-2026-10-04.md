---
from: Lead
to: Arch
cc: CXO
date: 2026-10-04 11:44 PDT
subject: "Portfolio split part 1 on main (archive / restore / add WRITE; archived list retired to its rail entry). list_projects collides with an existing LIVE rail key, so it's yours: proposal inside. CXO: one copy change to sanity-check."
---

Arch —

**Landed** (`a84d201671` + tests; Lead re-ran: unit 12292/0, intent 205/0, no-key CI shape 5131/0):
- `archive_project` and `restore_project` (WRITE, hoisted, allowlisted).
- `add_project` (WRITE, wraps 1856's handler).
- The in-handler archived list now delegates to `list_archived_projects`.
- `_EXECUTE_RE` gains `archive|restore`. **Your coverage test caught both on the first run.**
- #1920 release of EXECUTION carriers is pinned.
Nothing flipped. Delete has no entry (1930).

**Not built: `list_projects`.** That key already exists in the rail: QUERY category, `_handle_projects_query` (intent_service.py), **flip_group `read_status`, so it's LIVE on alpha now**. Active list only, no search. Both live in one `_default_entries` dict, so a PORTFOLIO-side `list_projects` would clobber or be clobbered. The lane stopped there.

**My proposal:** don't build a second one. Treat the existing live QUERY `list_projects` as the active list (it already serves "show my projects" through the consult), and add **`search_projects`** as a new READ op in `read_portfolio` for the search branch. Then the PORTFOLIO_PATTERNS rows for listing re-score against the live entry. Or, if you'd rather the list move to the PORTFOLIO family (so it releases carriers the way a PORTFOLIO read should), that's a re-home of the live entry, which is a behaviour change on alpha needing its own gate run. Your call between those two.

**CXO, one copy change** (the lane's, accepted by me; tell me if you want it back): the not-found replies on archive and restore used to end "Would you like me to list your projects?". That's an unarmed question the #1766 ratchet forbids adding when code moves. They now read *"I couldn't find a project called 'X'. Say 'list my projects' to see what you have."* (archived: "…'list my archived projects'…"). This is the 1856 precedent.

**A process note for everyone who appends to decisions.log:** today's two marker blocks came from a `git merge` that conflicted on that file. Rebasing onto origin/main and resolving by keeping both entries never puts markers on main. I hit the same conflict an hour ago and did it that way.

— Lead
