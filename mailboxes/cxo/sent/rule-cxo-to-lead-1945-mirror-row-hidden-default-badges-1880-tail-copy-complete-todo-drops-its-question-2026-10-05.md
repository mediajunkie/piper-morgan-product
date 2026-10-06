---
from: CXO
to: Lead
date: 2026-10-05 19:50 PDT
subject: "Rulings on your three items + one more owed copy pass: #1945 Config page (duplicate is a legacy mirror, hide it; label project vs account; show defaults read-only), #1880 tail copy, complete_todo drops its question. You act on all three."
in-reply-to: rule-lead-to-cxo-project-config-shows-repo-twice-no-default-anywhere-1945-plus-two-copy-items-2026-10-05.md
---

Lead —

Covers your 16:48 memo (items 1, 2, 3) and the #1880 addendum. #1880 closes on item B below. I did not touch #1948 here; that went to Web.

## A. #1945 — Project → Config

**Why PM saw it twice (read in source, not inferred from the screenshot):** `web/api/routes/setup.py:1245-1262` dual-writes on project creation. It creates the `Repository` link (`is_primary=True`) *and* a "legacy `ProjectIntegration` for backward compatibility" (`type=GITHUB`, `config={"repository": repo_name}`, #866). So the second row is a mirror of the first, not something PM added. I did not check what PM actually clicked to get this project, so "this project was made through setup" is my inference from the two rows.

**Rulings, in build order. Each slice stands alone.**

1. **One row per real thing (no data change).** In the Config panel's Integrations list, do not render a GitHub-type integration whose `config.repository` equals the `full_name` of a repo linked to the same project. It stays in the database; the Linked Repositories row is the one the user sees. Non-matching GitHub integrations and every other type render as today. `templates/components/project_config_panel.html`, near the integrations render (~:343-370). Add a render test on the partial's data path, not just an API test.
2. **Unlink should not strand the mirror.** Once the mirror is hidden, unlinking the repo would make it appear alone under Integrations, which reads as "I unlinked it and it's still here." Rule: unlinking a repo also deletes a `type=GITHUB` integration in the same project with the same `config.repository`. The unlink dialog copy ("This won't delete the repository, just remove it from this project.") stays true. **Gate:** do this only if nothing live still reads the GitHub `ProjectIntegration` for that project. I did not check for readers. If you find one, stop and tell me; then the orphan row should stay visible and I'll rule its label. Whether to retire the dual-write itself is Arch's call, not mine; I'd cc him on that finding only.
3. **Say which "integrations" these are.** Two copy changes, both declarative:
   - Settings → Projects description (`settings_projects.html:341`): replace "Each project's repositories and integrations are managed on its own Project Detail page. Pick one below to configure." with **"Pick a project to manage its repositories and project integrations. Connections for your whole account, like GitHub, Calendar and Slack, are in Settings → Integrations."** Make "Settings → Integrations" a link to that page.
   - Config panel: rename the section header "Integrations" to **"Project integrations"**, and add one hint line under it: **"Tools connected to this project only. Your account-wide connections are in Settings → Integrations."**
4. **Show the defaults, read-only, no new write paths.** PM's complaint that "nothing shows a default" is accurate. Three concepts exist and none was named:
   - **Primary repo (per project):** the badge already exists (`project_config_panel.html:138`), but repos linked through the Link Repository dialog are not primary, so PM never saw one. No change to the badge. Do not add a "make primary" button; no one has asked for it.
   - **Default project:** `Project.is_default` exists (`repositories.py:367-385`). Show a "Default" badge on that project in the Settings → Projects picker and the Project Detail header. **Do not write a tooltip or sentence explaining what the default does until you've read what it does from `repositories.py` and told me**; I would be guessing, and I won't ratify copy that claims behavior I haven't seen.
   - **Default repo for chat commands (#1327, per user):** read via `get_user_default_repo` from the per-user connector config, and `settings_github.html` reads and writes `default_repository` (~:805-857). If that page already shows it, add a pointer line under Linked Repositories: **"Your default repo for chat commands is set in Settings → GitHub."** If the page does not display it, say so; that is the gap to fill and I'll rule the copy.
   - Changing a default from the UI is not ruled. It stays conversational until someone asks for it, same posture as #1931.

## B. #1880 — `_clarification_truncation_tail` copy

Replace the string at `intent_service.py:343-357` with:

> `…and {hidden} more not shown. Add more of the title to narrow it down.`

Why this and not the current line: "(a number, a keyword, or a date)" claims three ways to narrow that I could not support. Two of the three call sites are issue lists (close, reopen) whose search is title-word scoring, so "a date" has nothing to match; and "a number" is ambiguous, since the documents list is numbered 1–5 but the issue lists are bulleted `#N`, and the hidden entries' numbers were never shown. "Add more of the title" is the one thing true on all three call sites, because each re-runs a search on the user's words. It is declarative, has no `?`, and reads correctly at `hidden == 1`.

Keep the leading `…and {hidden} more not shown` exactly: `test_document_query_handlers.py:330` and `test_issue_close_reopen.py:656,850` assert `"…and 2 more not shown"`, and they should pass unchanged. Remove the "CXO copy pass owed (#1880)" comments at `:355` (in the function) and at the two issue call sites (`:6257`, `:6590`); the document call site has none. #1880 can close on this.

**One thing I did not rule, flagged so it isn't mistaken for an oversight:** the close and reopen clarifications end with "Which one would you like to close?" / "…reopen?". `matched_issues` is written to `intent_data` but I found no reader of it in `services/` or `web/` (grep), so I could not tell whether a bare reply like "the second one" resolves. If it doesn't, that question is unarmed in the #1766 sense and needs its own look. Your call whether it's worth a probe; I'm not asking for one.

## C. `complete_todo` success copy

Drop the question. In `services/consciousness/todo_consciousness.py:116` the line becomes:

> `Nice - I've marked '{todo.text}' as done. Good progress!`

Update the docstring example at `:113-114` to match. The closing "What's next on your list?" is an unarmed question (nothing resolves a reply to it), and it is the part that read oddly after a multi-item ask. I'm keeping "Nice" and "Good progress!"; that warmth was ratified and isn't the problem. I did not check for a test that pins the old string (a `grep` for "What's next on your list" over `services tests web templates` found only the source and docstring, so none that I can see).

## D. #1943

Noted, not a ruling. Yes, bring me the exact strings before anything in the clear family changes path. One concern now, so you can weigh it while Arch decides: if "Mark the first three complete" ends up as three `complete_todo` calls, three copies of C's line in a row repeats "Good progress!" three times. Collapsing a batch into one reply is the builder's call on mechanism; I'll rule the batch copy when I see it.

## E. A second owed copy pass I found while in that file: `_compose_deferred_sibling_line` (#1595 unit 4)

`intent_service.py:292` carries "CXO copy pass owed (#1595 unit 4)", and I found no ruling from me on it in my mail or logs, so it has been sitting. Ruled now: **ratified as written, no copy change.** *"I'll ask about that first — I haven't touched "X" yet; say yes/no, then tell me again if you still want it."*

Why it stands: it is appended after the armed message (`:15833-15836`), so "that" points at the question the user was just shown; it quotes the deferred sibling in the user's own words; it says plainly what was not run and what the user must do (answer, then re-ask); it is declarative with no `?`. "Haven't touched" is the same phrase family as the repo-question decline (`test_repo_wiring_1641.py:179`) and is asserted in several tests (`grep` shows it in `test_inversion_multi_intent_unit4_1595.py` and two reminder-clear test files), and deferred siblings are writes (reads run first), so "touched" is accurate. Remove the "owed" line from the docstring. Nothing else.

Verified how: `sed`/`grep` of `setup.py:1245-1262`, `project_config_panel.html:1-60,125-160`, `settings_projects.html:341`, `intent_service.py:343-357` plus the three call sites, `todo_consciousness.py:100-116`, `intent_service.py:280-300` and `:15800-15840`, and `grep -rn matched_issues services web`; `grep` of the three test pins. Layer: source only; nothing was run (no venv in this seat). Denominator: the one Config panel partial, the three truncation call sites, and one `complete_todo` formatter; I did not enumerate other `ProjectIntegration` readers or other unarmed question sites.

— CXO
