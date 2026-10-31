# Release Notes — v0.9.0.0 (private beta)

**Cut**: 2026-10-31 from `main` · **Type**: beta (the first 0.9 release; the MVP milestone closed
2026-10-30 17:03 PT on xian's GO) · **Hosting**: alpha.pipermorgan.ai and beta.pipermorgan.ai are
both served by Fly from the same cut; the beta invitations go out with this release.

> **Status of this file (2026-10-31 09:28 PT, Lead):** the version files and this skeleton land on
> main ahead of the morning's promotion so the promoted build reports 0.9.0.0. The prose sections
> marked *Docs* are written by Docs before the tag; the tag and the GitHub release follow PPM's
> re-check list on the served build (Exec's order, 09:14). Until the tag exists, the version
> mechanics below are the plan, not the record.

## Summary

0.9.0.0 closes the MVP milestone and opens the invitation-only private beta. Since v0.8.14.0
(2026-09-23) main took 1,138 code commits (`services/`, `web/`, `tests/`, `scripts/`, `alembic/`)
and 361 issues closed, including the whole of milestone 5 (MVP: 1,291 closed, 0 open). Seven
Alembic migrations ship in this range (listed under Upgrade). This release is about trust in what Piper tells you. Most of the 361 issues closed since v0.8.14.0 are cases where Piper said something that was not true or did not say something that was: a connection shown as healthy when it was not, an empty day that was really a failed calendar read, a delete that reported success and changed nothing, a first-time setup that ended in "Setup Failed". Each of those now has a fix, and many have a regression test pinned to the exact wording that failed. The setup path for an invited tester was rebuilt around the hosted app, and the Integrations page, the chat replies and the data controls were checked against what actually happens behind them. What remains open is listed under Known limitations.

## What's New (user-facing)

Each fix below has a regression test. PPM's re-check on the served build runs before the tag, and anything it turns up will be listed under Known limitations.

**Setup works for an invited tester**

- The setup wizard no longer ends in "Setup Failed" for an invited account. The account is created and your keys are stored (#2078).
- Step 1 of the wizard no longer blocks every new user, and the hosted app no longer shows the local System Requirements check for Docker, Postgres, Redis and Temporal (#1875, #2089).
- The wizard no longer shows Slack and Google Calendar app-credential forms to a new tester (#2176).
- A server-side encryption problem is no longer reported as a "Validation error" on your API key, and the key check no longer claims "claude-3.5 access confirmed" when it only checked the key (#2125, #2117).
- Current Anthropic keys are no longer refused by the key-format rule (#1978).
- A conversation you start before adding a key stays in your sidebar (#1913, #1838).

**Integrations say what is true**

- The Integrations Test for GitHub no longer reports "connection successful" on a revoked grant, and the GitHub settings page no longer shows Connected for a revoked grant (#2012, #2029).
- After a successful Test, the card updates its status, its "last checked" line and the "healthy" count instead of keeping "Not checked yet" (#2045, #2044, #2049).
- The Test result is now per account. One account's Test no longer changes what another account sees (#2071).
- An expired sign-in is no longer shown as an integration failure, and the page headline no longer says "All Systems Healthy" for an OAuth connection that has never been tested (#2067, #2075, #2068).
- A GitHub account with a dead connection can recover from Settings, and the Disconnect button works (#2018, #2017).
- Disconnect no longer reports success when a stored credential copy failed to clear (#2172).
- Calendar connect no longer says "Calendar Connected" when you left Google's consent screen without finishing (#2148).
- Chat now reads events from a Google Calendar that Settings reports as healthy, and "what's my agenda Thursday?" honors the weekday (#2092, #2091).
- GitHub reads in chat use your own account's grant, not a token set on the server (#2123, #1966).

**Piper tells you when it could not read something**

- A standup or radar view no longer shows a failed calendar or GitHub read as a free day or "no activity" (#2182, #1965, #2072).
- Plain focus and standup replies say when GitHub cannot be read with your current grant (#2076).
- Standup and radar no longer list every open GitHub issue as your own work when no GitHub username is set (#2173).
- "What changed since yesterday?" and "What changed in the past hour?" now explain the window they read (#2140, #2143).
- Replies no longer say "Your todo list is clear" or "nothing urgent" while overdue or pending todos exist (#1985, #1990, #1997, #1998).
- A GitHub 404 on an issue read no longer blames "GitHub's MCP server" (#2111).

**Todos, reminders, projects and lists**

- "Add three todos for the launch: draft brief, book venue, send invites" now works (#2094).
- "Delete that reminder" right after a reminder is saved targets that reminder, and deleting an upcoming reminder no longer fails after you confirm (#1987, #1975).
- Ordinal deletes such as "delete the first two reminders" explain what is needed when no list is on screen, and bulk todo deletes are capped at one item until soft delete exists (#2046, #2050, #2019).
- A project's Remove button and "delete my project" now do what they say (#1912, #1930).
- "Add a project called Baz with description ..." stores the description in the description field (#2069).
- The Lists page shows the right item count for a list that holds items (#2171).
- Reply wording is tidier: "1 days overdue" and "1 meetings" now read in the singular, and "(0 days overdue)" no longer appears (#2001, #1999, #2129).
- A reminder confirmation echoes the day you wrote, not "next Friday" when you wrote "on Friday" (#1958).

**GitHub issues in chat**

- A new user's first "Create an issue" no longer goes to an auto-picked oldest repository with issues disabled (#2205).
- Chat no longer adds an "enhancement" label nobody asked for (#2118).
- "Show me that issue" right after creating one shows it instead of asking for a number (#2115, #2114).
- Colon-and-quotes creates such as `Create a GitHub issue: "title" in repo` work, and in a pending draft, "change the title to X" changes the title (#2110, #2098).
- "Update issue" followed by a number is no longer sent to the Notion update path (#2113).
- Milestone questions get a milestone answer. The header "across all your repositories" no longer appears on every issue list, and an undated milestone no longer prints "due no due date" (#2198, #2199, #2194, #2200).
- A comment on an issue no longer reports "Successfully added comment" when the post failed (#2152).
- Closing a nonexistent issue says so and changes nothing (#1941, #1858).

**Standup and everyday conversation**

- The standup greeting no longer says "Good morning!" at every hour (#2079).
- A bare "cancel" with no standup running no longer claims a standup was cancelled (#2033, #2032).
- Standup suggestion chips such as "nothing" and "skip" now appear (#2027, #2028).
- A standup no longer invents a reason for an empty day (#2008).
- "thank you!" as a first message gets a short reply, not a todo briefing (#1986, #1989).
- Placeholders such as `<city>` in "set my timezone to <city>" now render (#1988, #1991, #1992).

**Feedback, privacy and your data**

- Send feedback is reachable from inside the app, including the setup wizard and error pages (#2096, #2156).
- You can hide or delete a chat, and Settings no longer promises Export and delete actions the page lacked (#2065).
- The privacy page's 14-day deletion promise now has an erasure path behind it (#2064).
- The API key Remove dialog states that backups keep a copy for a limited time, instead of saying the copy is destroyed immediately (#2167).
- Uploaded-file writes no longer fall back to plaintext when the server's encryption key is missing (#2061).
- The command palette's "Start private session" action no longer does nothing (#2108).

## Under the hood

**Routing stack**

- Understanding-Layer Inversion epic closed: one constrained LLM routing call does the understanding for a turn (#1595).
- Phase 3 deletion gate hardened: a corpus row's MATCH verdict can now see a different claimant, sub-threshold rows no longer earn credit, and zero claiming rows is not accepted as proof a lane is dead (#1971, #1969, #1973, #1933).
- Two-part turns no longer lose the second half when the router or surface 1 claims only one part (#1896, #1897, #1977).
- Unarmed offers: the floor can no longer offer an action it has not armed, and the unarmed-ask census now finds asks with a mid-line question mark (#1855, #2000).
- Tests and corpus brought current with the Phase 3 deletions and the 10-05 catalog growth (#1924, #1925, #1951, #1921).
- Intent cache no longer shares one mutable context across hits (#2054).
- Armed-carrier off-intent release: GitHub write commands release correctly (#1920).
- Principal handling: generic offer accept and repo-question answers no longer run under the wrong principal, and LLM calls for a user without a user_id no longer resolve the server's provider (#2223, #2222, #2131).
- Inversion and preclaim shadow calls spend the requesting user's own key (#2109).

**Hosted MCP server at mcp.pipermorgan.ai**

- Cross-caller state isolation for the hosted endpoint (#1458).
- The MCP server reads GitHub issues using the stored credential, and rows are backfilled for tokens saved before the dual write (#1982, #2090).
- The github-issues resource reports the real total instead of presenting a 30-item page as the full set (#2005).
- The profile resource no longer serves PIPER.md fallback projects over a failed read (#2212, #2218).
- The image build guard now covers gitignored local config files (#2240).
- The OAuth authorization server, the access-token tables and the `what_piper_knows_about_me` tool ship in this release as part of the hosted MCP epic (#1462, still open). The MCPB bundle and the MCP docs, registry listing and client tests also closed in this range (#957, #830, #831, #832). The MCP app serves its fixes on its own deploys, not on the web promotion: the profile-read honesty fix (#2218) and the oversized-payload and zero-form fixes (#2241, #2022) are served on the MCP app today.

**Screening harness**

- Test-account fault injection makes one source fail on demand so failure-path copy can be served and checked (#2234).
- The offline corpus and live scripts work after the per-user key change (#1861, #1865).

**CI, gates and ratchets**

- The mypy signature-drift ratchet was red for 41 consecutive runs and is green again, with transitive dependencies pinned (#1947, #1786, #1800, #1469).
- Link-checker, code-quality and spend-free canonical gates were repaired after tripping on main (#1894, #1892, #1929, #1993).
- Gate scripts fixed: `check_intent_bypasses.py` and `check_fullsuite_backlog.py` (#2058, #1928).
- Provider-agnosticism is enforced in code, not by a comment (#1829).
- Commit-message guard blocks GitHub auto-close keywords next to issue numbers (#1691, #1934).
- `requirements.lock` is installable again (#1936).

**Deploy, health and recovery**

- `/health` reports the real version, git SHA and environment, and now pings the database (#1839, #1849, #2083).
- Production Postgres restart policy and alerting after the 2026-10-19 outage (#2085).
- Alpha Postgres recovery dispatches from the health watch without waiting on two human approvals (#2146).
- Promotion to alpha deploys by the pushed digest, fixing the "manifest unknown" failure (#2177, #2181).
- Admin Invites page mints, lists (masked) and revokes invite codes (#2081).
- Invite codes removed from tracked logs and mailboxes (#1885, #1845).
- Privacy follow-through: Chroma telemetry off, log text matches the privacy copy, a user-erasure path exists (#2060, #2059, #2064).

## Known limitations (beta)

**Connectors**

- The connectors offered in this beta are GitHub and Google Calendar only. Other connectors are not offered in this beta.
- The MCP connector (Piper inside Claude and other MCP clients) is private-beta work and is not on the MVP path. Expect it to be rougher than the web app.

**Chat and data**

- "You have 261 open issues" can count issues assigned to you across all repositories, archived ones included, and "most recent" is not sorted (#2185).
- A question about a milestone's issues can be answered with the wrong issues, because no read lists a milestone's issues yet (#2184).
- "Delete todo 1 and 2" removes only the first, and the second is dropped without a message (#2025).
- A "show my todos" reply can strike through an open overdue todo, which makes it look done (#1961).
- Sharing a todo, list or project from the UI fails with an error (#2166).
- In a multi-part message, a write offer or a question from one part can be lost or shown as plain text (#2041, #2030).
- The learned-pattern execute route can report a failed action as a success (#2208).
- Preferences are not always applied on a cached reply (#2056).

**Interface**

- Switching between chats redraws the whole screen, which flashes (#1515).
- On iPad Safari in portrait, a new chat can show an empty gray panel with the composer pushed off screen (#1907).
- Deleting or archiving a conversation has no reachable control in the current navigation (#1516).
- "Start private session" in the History slide-out is a display toggle with no backend behavior. Do not rely on it (#1164).

**Not for beta use**

- The Slack settings page and the Slack socket-mode path are not beta features. The socket-mode path binds every sender to the connector owner (#1497, #1481).

For anything not listed, use Send feedback in the app. Each report with the exact wording becomes a test row.

## Version mechanics

- Version string `0.9.0.0`: the four-part form used since v0.8.9.2 (`v0.8.11.0` … `v0.8.14.0`);
  0.9 is the line reserved for the beta (milestone-gated on MVP, decisions.log 2026-08-30).
- `VERSION` and `pyproject.toml` at `0.9.0.0` (`scripts/check-version-consistency.py`: OK).
- Cut commit: the `main` commit carrying this bump; the tag `v0.9.0.0` goes on it, or on a later
  `main` tip if fixes land between the bump and the tag (the tag names the build PPM's re-checks
  passed on, not an earlier one).
- Deploys come from `origin/main`; `production` was retired 2026-09-29. Promotion to alpha and
  beta is xian's dispatch under the standing grant; the beta letters go first.
- Parity gate at the bump: `scripts/check-release-parity.sh origin/main` → PARITY OK (09:25).

## Upgrade

Hosted: nothing to do; the promotion carries it. `/health` on alpha, beta and the MCP app reports
`version: 0.9.0.0` once each is deployed from a commit at or after the bump.

Local: `git pull && alembic upgrade head`. Migrations since v0.8.14.0:
`a1599admin` (changed), `n1462mcpt_mcp_access_tokens`, `o1462oaut_mcp_oauth_as`,
`p1522drop_drop_action_humanizations`, `q2009nn_owner_id_not_null`,
`r2013kgnn_knowledge_owner_not_null`, `s2014items_base_item_has_list`.
