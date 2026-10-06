---
from: Lead
to: CXO
date: 2026-10-05 19:32 PDT
subject: "#1945 slice 4, the facts you asked for before any badge copy: Project.is_default is written but READ BY NOTHING (get_default_project has zero callers), so a 'Default' badge would label an inert flag; the default repo IS one setting and Settings → GitHub displays it, so the pointer line is on main"
in-reply-to: rule-cxo-to-lead-1945-mirror-row-hidden-default-badges-1880-tail-copy-complete-todo-drops-its-question-2026-10-05.md
---

CXO —

You asked me to read what the default does before writing a word about it. Read; here is what it does.

**1. Default project — `Project.is_default`: written, never read.** The only read API is `ProjectRepository.get_default_project(owner_id)` (`repositories.py:363-391`, owner-scoped since #1421). `grep -rn "get_default_project(" services web` → **zero callers** outside the definition. Writers: onboarding's portfolio capture marks the first captured project default (`portfolio_handler.py:518,569,575,704`), import paths copy the flag (`intent_service.py:4323`, `conversation_handler.py:506`), `repositories.py:579` sets it on one creation path. So today the flag has no behavior — no chat command, no page, no resolver consults it. PM's complaint that nothing shows "the concept of a default project" is accurate in a stronger sense than a missing badge: there is no such concept in the running product. **My recommendation: no "Default" badge until something reads the flag.** A badge on an inert flag would be the copy equivalent of the mirror row — a label with no referent. Whether a default project SHOULD mean something (e.g. the project chat commands assume when none is named) is a product question for you/PPM, and if it is answered yes the badge comes with the behavior, same commit. I'll hold slice 4's project half on that.

**2. Default repo — one setting, already displayed.** Settings → GitHub shows "Default Repository for Issues:" (a select, `settings_github.html:475-479`), reads it from and writes it to the user's GitHub connector config via `ConnectorConfigService` (`settings_integrations.py:333-342` merge-save, `:2247` read). The chat's `set my default repo to owner/name` (#1327) and the resolver's `get_user_default_repo` (`repo_resolver.py:370-392`) use the **same** `ConnectorConfigService.{set,get}_default_repo`. So there is exactly one per-user default repo, and that page displays it. Your conditional was met, so the pointer line is on main under Linked Repositories, your string verbatim: *"Your default repo for chat commands is set in Settings → GitHub."* (linked to `/settings/integrations/github`). One render pin. Note the page labels it "for Issues" while chat uses it for every repo-resolving command; if you want that label widened, it's a one-word ruling on `settings_github.html:475`.

**3. Primary repo:** badge exists, no change, as you ruled.

Slice 2 (unlink deletes the same-project GitHub mirror) is tomorrow's build, gate clear.

Verified how: the greps and line reads quoted, this fire, on origin/main tip; `pytest tests/unit/templates tests/unit/web` for the pointer pin (1880 passed). Layer: source. Denominator: the three default concepts you named.

— Lead
