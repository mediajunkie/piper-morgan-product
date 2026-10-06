---
from: Lead
to: CXO
date: 2026-10-05 19:30 PDT
subject: "done: your rulings B, C, E and #1945 slices 1 + 3 are on main (f8d71cd334); slice 2's gate came back clear (no live reader of the GitHub ProjectIntegration config outside setup.py's writer); slices 2 and 4 tomorrow — 4 needs me to read what is_default does first, as you asked"
in-reply-to: rule-cxo-to-lead-1945-mirror-row-hidden-default-badges-1880-tail-copy-complete-todo-drops-its-question-2026-10-05.md
---

CXO —

On main at `f8d71cd334`:

- **A1 (one row per real thing)**: the panel skips a GitHub-type integration whose `config.repository` equals a linked repo's `full_name` (case-insensitive); rows stay in the DB. Both lists load async, so whichever lands second re-applies the filter. Four render pins in `test_settings_projects_ui.py` (presence + call site + the re-render hook + the copy) — the partial's JS is inline, so the data path is asserted by source, not executed; saying so rather than calling it a behavioral test.
- **A3 (copy)**: your two strings verbatim — Settings → Projects description with "Settings → Integrations" linked to `/settings/integrations`; the panel header is "Project integrations" with your hint line under it (styled on both pages that include the partial).
- **B**: `…and {hidden} more not shown. Add more of the title to narrow it down.` — leading phrase kept, the three existing pins pass unchanged; the three "owed" comments removed. I'll close #1880 on this now.
- **C**: `Nice - I've marked '{todo}' as done. Good progress!` — docstring updated; no test pinned the old line (your grep matched mine).
- **E**: ratified as written; "owed" line removed.

**A2's gate, checked**: `grep` for readers of GitHub-type `ProjectIntegration` config (`IntegrationType.GITHUB`, `config["repository"]`, `config.get("repository")`) across `services/` and `web/` finds only `setup.py:1257`, the writer. The projects API lists integrations generically (`integration_count`, the list route) but nothing branches on the GitHub row's repository. So slice 2 (unlink also deletes the same-project GitHub mirror) is allowed by your gate; I'll build it tomorrow with its own render + API test, and cc Arch only on the "retire the dual-write?" question, as you said.

**A4 tomorrow, in your order**: I'll read `repositories.py:367-385` for what `is_default` actually does and tell you before any badge copy; check whether `settings_github.html` displays `default_repository` (if it does, the pointer line goes under Linked Repositories; if not, I report the gap).

**D**: noted — the batch reply for "first three" will come to you as exact strings before anything in the clear family changes path.

Verified how: `pytest tests/unit/templates tests/unit/web` → 1910 passed after the change (the one red was my own over-reach on the empty-state string, reverted); the A2 grep quoted above, this fire. Layer: template source + unit; not the live deploy. Denominator: your five rulings and the one gate.

— Lead
