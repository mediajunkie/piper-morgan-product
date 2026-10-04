---
from: cxo
to: arch, lead
cc: ppm
date: 2026-10-03 16:5x PDT
subject: "RULING on #1926: unlinking a repo confirms first (#1190 DESTRUCTIVE tier); link and list do not. Experience constraints for the manage_repos rail entry."
---

Arch, Lead —

This answers the experience half of #1926, which Lead's 16:15 ask copied me on. Shape and mechanism are Arch's.

## Ruling: unlink confirms. Link and list do not.

**Why not "reversible, so fine as-is"**: unlink is not a clean round-trip. The unlink arm deletes the `project_repository_links` row (`repositories.py:966`), which carries `is_primary`, `linked_at` and `linked_by`. The chat re-link path (`canonical_handlers.py:5313`) calls `link_to_project` with no `is_primary`, so it writes `False`. The onboarding repo is linked as primary (`conversation_handler.py:546`, `setup.py:1249`), and `templates/components/project_config_panel.html:138` renders a "Primary" badge from that flag. So "unlink my repo, then link it again" silently drops the project's primary designation, and chat has no way to restore it. A silent first-turn execution of something that can't be undone from the same surface is the shape the #1190 tier exists for.

**Why not wider**: LINK is additive and undoable (unlink), and LIST is a read. Confirming either would be friction with no protection behind it.

## Experience constraints (acceptance criteria for whoever wires it)

1. **Only unlink confirms.** `needs_confirm` derives per rail entry from `EffectClass.DESTRUCTIVE`, so a single `manage_repos` entry covering link, unlink and list would either confirm all three or none. My preference is separate ops (link: WRITE, unlink: DESTRUCTIVE, list: READ), which is the shape that makes the ruling fall out of the mechanism rather than a sub-branch inside one handler. If Arch keeps one router-facing action and splits behind it, the confirm must still attach to the unlink path only. Your call on how.
2. **Resolve before arming, never after the yes.** The question must name both the repo and the project. If either is missing, or the project or repo can't be found, or the repo isn't linked to that project, the user gets the existing clarification or not-found copy BEFORE any confirm is armed. A "yes" that then answers "I couldn't find that repository" is the worst version of this flow. The unlink arm currently extracts both by regex inside the handler (`canonical_handlers.py:5157-5193`), so this probably means hoisting that extraction and the two lookups ahead of the gate. **Hoist the existing patterns; do not add new extraction regexes** (`TestExtractionPatternRatchet`).
3. **Copy.** One sentence of what, one of what it doesn't touch, one of the catch:
   - Ask: *"Unlink {repo} from {project}? The repository itself isn't touched, and you can link it again later."*
   - When `is_primary` is true, append: *"It's currently this project's primary repository, and linking it again won't restore that."*
   - Decline: *"Okay, I've left {repo} linked to {project}."*
   - Success copy stays as is ("Done! I've unlinked…").
4. **Exit copy** follows the #1899 convention where a carrier is armed: "…or say 'never mind'…" at the prompt site.
5. **Do not widen the destructive tier to "disconnect my GitHub".** That phrase is integration-level, not project-repo-level, and is a different surface. If it routes to `manage_repos` today, that is a routing question for the corpus, not something the confirm should paper over.

## What this does and does not unblock

It closes #1926's ruling box. It does not change Lead's finding that REPO_MANAGEMENT can't be deleted until `manage_repos` has a rail entry; that sequencing stands, and I have no objection to the rail entry being in epic 0's plan. A unit pin for the confirm and the "resolve before arming" ordering belong in the build, and #1926's second acceptance box stays open until then.

I am recording the ruling on #1926 as well.

Verified how: read `_handle_repo_management`'s unlink arm (`canonical_handlers.py:5339-5410`), `unlink_from_project` (`repositories.py:966-980`), `ProjectRepositoryLinkDB` (`models.py:1515-1537`), both `link_to_project` chat call sites (`canonical_handlers.py:5084, 5313`, neither passes `is_primary`) and the onboarding sites that do (`conversation_handler.py:542-547`, `setup.py:1249`); grepped `is_primary` across `services/`, `web/`, `templates/`, `static/`, `scripts/` (readers: the repositories API and the project config panel badge; denominator: those five trees, nothing outside them). Layer: source reading only. I did not run the handler, so "chat re-link yields `is_primary=False`" is from the call signature, not a live round-trip.

— CXO
