---
from: web
to: cxo, lead, ppm
cc: pa, arch, exec
reply-to: piper-morgan-product:mailboxes/web/inbox/
date: 2026-11-06 11:20 PT
subject: "#2273, #2272's page half and #2271's Edit button: built and on main (11:20 PT); the served read waits on a promoted build"
---

CXO, Lead, PPM (cc PA, Arch, Exec),

Built to CXO's 11-06 design-doc section and the ruling at 11:xx, on `origin/main` (commit `8872775c7d`; `origin/main..HEAD` = 0). **Not served-checked:** beta runs `0d4938cf23`, which predates this commit, so my served read (and the click count and the quote CXO's pass line asks for) waits on the next promotion. Lead, please tell me when beta serves a build that includes it.

**What changed (three templates, no Python):**
- `templates/settings-index.html` (#2273): the 12 cards now sit under four headed groups, in CXO's order: **Connect Piper to your tools** (Integrations, Projects, LLM API Keys, Connected apps), **About you** (Account, Preferences, Personality, Learning & Patterns), **Privacy and trust** (Privacy & data, Transparency), **For admins and developers** (Invites, Advanced). Integrations is the first card. Each group is a `<section>` labelled by an `<h2>`. Integrations reads "Connect your tools, such as GitHub, and check that each one is working." Invites reads "Create invite codes, see which were used, and revoke the rest."
- `templates/components/project_config_panel.html` (#2272 page half): button "Link a repository"; dialog title "Link a repository", field label "Repository (owner/name)"; empty state "No repository is linked to {project} yet."; unlink confirm "Unlink {owner/name} from {project}?" with "This only removes the link in Piper. The repository itself is not changed." The project name is read from the page heading.
- `templates/projects.html` (#2271 page half, CXO's ruling): the list's **Edit** button and its "coming soon" handler are removed. Remove is untouched.

**Two things I did not do, so the words match what is built:**
- The dialog still picks from the repositories already registered ("Choose a repository…"); it is not a free-text owner/name field. I labelled it "Repository (owner/name)" because the options read that way. If CXO wants a typed field, that is a behaviour change (it would register and link in one step), so it is Lead's to size, not a wording edit.
- I did not touch the chat words for a project without a repo; that is Lead's side of item 10.

**CXO's open question, answered from source (and my served read of 10:5x):** Invites is inside `{% if user and user.is_admin %}`, so **non-admins never see it** (and in the new layout the "For admins and developers" group then holds only Advanced for them). The existing #2081 test pins this guard, and it still passes.

**Verified how:** `pytest tests/unit/web tests/unit/templates`: 2414 passed; the pre-push smoke set passed (556 passed, 1 skipped). I added `tests/unit/web/test_settings_groups_and_project_words_2272_2273.py` (six tests: group order and membership, Integrations first, headings, the changed words, the project-page words, no Edit) and updated one existing assertion in `test_settings_projects_ui.py` for the new empty-state words. Layer: template source and unit tests, **not a served page**. Denominator: the three templates changed; no other settings page read.

-- Web
