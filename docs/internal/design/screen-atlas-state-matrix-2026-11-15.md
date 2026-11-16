# Screen atlas: state matrix and navigation tree (DRAFT 1, CXO, 2026-11-15)

For #2381. Purpose: one list of what a person can see on each settings page, in each state that matters, so a served read can be judged without asking xian for a screenshot. Draft 1 comes from the Settings index template (`templates/settings-index.html`) and from the states already ruled this week. It is not verified against served pages: 11-15's #2375 read showed that source predicted a label the page did not show. Web adds the states the served page actually has, and corrects anything here that the page contradicts.

Each atlas row records: URL, state, sha from `/health`, time (PT), page text as served, image name. Images follow HOST's conditions (seeded test account only in the public repo, otherwise private, with a name-free pointer here).

## Navigation tree (from the Settings index, 11-15)

Settings (`/settings`)
- Integrations (`/settings/integrations`) → GitHub (`/settings/integrations/github`), Slack, Notion, Calendar, others by card
- Projects (`/settings/projects`)
- LLM API Keys (`/settings/llm-keys`)
- Connected apps (`/settings/connected-apps`)
- GitHub repositories link, as served 11-15 (`/settings/integrations/github#repositories`): floating text link under Connected apps; ruled FAIL, becomes a card (#2375)
- Preferences (`/settings/preferences`)
- Privacy & data (`/settings/privacy`)
- Invites (`/settings/invites`) (admin)
- Account flags (`/settings/account-flags`) (admin, operations reader)
- Advanced (`/settings/advanced`)

## Account states used below

- **S0** signed out
- **S1** signed in, nothing connected
- **S2** GitHub: App connected, installed nowhere
- **S3** GitHub: App connected, installed on one or more repositories
- **S4** GitHub: App connected, personal token also on file
- **S5** GitHub: no App connection (classic OAuth, App mode off, or personal token only)
- **S6** GitHub: connection stale or unreachable
- **A** admin / operations reader (Account flags, Invites)

## Matrix

| Page | States to capture | What to quote |
|---|---|---|
| Settings index | S1, S3, A | every card title and line; where the GitHub repositories entry sits |
| Integrations, GitHub card | S1, S2, S3, S5, S6 | status line, "Last checked", every button label, whether the label request has settled |
| GitHub page, connection | S1, S2, S3, S4, S5, S6 | headings, connected line, buttons, personal-token section (form, stored-token line, Remove, or nothing) |
| GitHub page, repository section | S2, S3, S6 | install-step line, list, default-repository control, Install on GitHub / Add another repository, Refresh |
| LLM API Keys | per provider: none, one saved, saved and failing | provider list, key-step help lines (#2274, #2366), save and remove lines |
| Preferences, Projects, Privacy, Advanced | S1 | headings and any empty-state line |
| Invites, Account flags | A and non-admin | page words, the non-admin line |
| Chat, GitHub turns | S1, S2, S3, S6 | the reply to: my open issues; my repos; open issues in a named repository the app is on / is not on |

## Open for Web

- Which states above the served pages do not have, and any state they have that is missing here.
- Slack, Notion, Calendar integration pages: states not drafted.
- Where the images live (HOST point 5) and the first set.
