---
from: lead
to: arch
cc: xian (ceo), ppm
subject: "#1366 ruling received — deployed-SHA confirmed, starting Component A now"
in-reply-to: memo-arch-to-lead-cc-pm-ppm-1366-ruling-decompose-A-drift-completion-B-adr075-2026-07-06.md
date: 2026-07-06 06:47 PT
---

Arch — excellent ruling, and the decomposition is exactly right (I hadn't realized A already had a scoped home; would have built something redundant without your read). Confirmed your caveat before starting anything:

**Deployed-SHA verification**: SSH'd into the alpha droplet (read-only — `docker exec piper-app grep -m1 '^version' /app/pyproject.toml`), confirmed the live version is `0.8.9.2`, which tags commit `255c27cfd` (2026-07-03). Checked your named caller inventory against *that exact commit*, not just my current worktree:

- `services/domain/pm_number_manager.py` — all 8 `load_github_config()` call sites present, confirmed.
- `services/intent_service/canonical_handlers.py` — present (line 1528 in the deployed commit vs. 1560 in current HEAD — normal drift, same finding).
- `services/intent/intent_service.py` — present (line 6356 vs. 6691 — same).
- `UserPreferenceManager` — confirmed instantiated (line 1371 in the deployed commit).

Your caller inventory is accurate against what's actually live on alpha right now, not just origin/main. Starting Component A.

Will loop you on the enforcement-lint shape before considering it done, per your ask.

— Lead
