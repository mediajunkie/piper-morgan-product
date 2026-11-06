# First-session design: from sign-in to one valuable thing

**Author:** CXO, 2026-11-04 13:26 PT. **Status:** first cut, for PPM's proposal and xian's sprint talk. It is a design, not a ruling on sprint order. Nothing here is built or served.
**Reads from:** PPM's proposal (`onboarding-to-first-value-proposal-2026-11-04.md`), `templates/setup.html` (steps 1 to 5), and the twelve filed findings (#2267 to #2278).

## What the wizard does today, and where it stops

Intro, invite code, system check, "Connect Your AI", account, "Your Projects" (a name and an optional repo), then "Setup Complete: You're all set. Open Piper." The wizard ends at an empty app. A new person has been asked for an AI key and a repo, and has been given nothing back. That is the gap: the session ends before anything valuable happens.

## The principle

Every step either gets the person closer to one thing they can use, or says plainly what it did not do. No step claims a state the code has not reached (a recorded repo is not a connected GitHub). Every step has a pass line that is a quoted page or a served reply, never a unit test.

## Path A: the practicing PM with a repo (first value: a real read of their own work)

| Step | What the person sees | Words (CXO) | Pass line |
|---|---|---|---|
| 0. Sign-in screen (#2275) | The logo, one line about Piper, three prompts that serve today | PPM's line, fitted: "Piper Morgan is a product-management colleague. It works with your GitHub issues and projects, can write your standup, and helps you decide what to do next." | Web quotes the served page. Each example prompt is run served first. |
| 1. AI key (#2274) | Provider, key, and a sentence before the field | "A Claude subscription (Pro or Max) doesn't include API access. Piper needs an API key from the Anthropic Console, which is billed separately from your subscription." | Web quotes the step with the link. |
| 2. Project and repo (#2268) | Name and repo, then a line that depends on the GitHub binding | Not connected: "I've noted {repo} for this project. GitHub isn't connected yet, so I can't read it." Connected: "{repo} is linked to this project." | Web quotes both states. |
| 3. Connect GitHub (new last step, before "Open Piper") | A card with Connect, the line about GitHub's page, and a Skip | "GitHub will ask you to approve Piper Morgan. Its page names the account that owns the app, which is Piper's and not yours, and says which of your GitHub accounts it wants to access. Check that account is the one you mean. Piper only gets access to the account you approve there." (Final text per #2286, 11-06. It supersedes the "Alpha" wording written before the OAuth app transfer. No owner name or host is hard-coded.) After: "GitHub is connected as {login}." Skip: "You can connect GitHub later in Settings, under Integrations. Until then I can't read your repo." | Web quotes the card and the post-connect line on a non-owner login. |
| 4. First value (the landing) | Chat opens with one suggested ask, as a button | The ask is "Show my open issues" or "What changed in my tasks and projects this week?" Whichever Lead confirms serves cleanly on a fresh account with a connected repo. | PA quotes the served reply on a fresh account. |

**Cut order if time is short:** 0 and 1 are words only. 4 is the first value and must not be cut. 3 is the only large build.

## Path B: the person with no PM and no repo (first value: an idea turned into a plan they keep)

I cannot write this path honestly yet. It depends on two facts I have not confirmed with Lead:
- whether chat can produce a plan and save it as a document under the person's documents (the 11-02 reply "I can't update documents from chat yet" suggests a limit on editing, not on creating);
- which prompt does it and what the person reads.
Until Lead confirms the capability and a served reply exists, this path stays a hypothesis. **Ask for Lead:** the shortest ask that ends in a saved plan, and whether it needs a connector.

## Where the failure was, by step

Step 3 failed on the authorize page (#2266). Step 4 failed on routing (#2270), the invented command (#2269) and the "yes" loop (#2271). The design does not fix those. It makes them visible as the steps a person reaches next, so they get fixed in the order a person meets them.

## Success line

n of N new accounts reach step 4's served reply in their first session, without help from us, and say it was useful. PPM keeps the count. HOST runs the sessions. I judge the experience on each person's quoted screens.

## Open questions

1. Does the wizard end at step 3 (connect) or at step 4 (the first ask)? I propose step 4: the wizard's last page is the first value, not "Setup Complete".
2. Skip at step 3: Path A's value needs GitHub, so a skip ends in an honest "I can't read your repo yet". Is a skip allowed in beta? Product call (PPM, xian).
3. Path B's prompt and capability (Lead).
4. The OAuth app transfer (xian) changes only the middle sentence of step 3's line if at all.

## Answered by PPM (2026-11-04, acceptance criteria; xian can overrule in the sprint talk)

- The wizard ends at step 4, the first ask, not at "Setup Complete". Step 4 is never cut.
- Skip is allowed at step 3 in beta. A skip says plainly that Piper can't read a repo yet, then lands on Path B's first ask, or until Path B serves, on an ask that serves with no connector (Lead names it).
- The fitted positioning line ("can write your standup") is accepted and on #2275.

## Path B (no PM, no repo): rows added 2026-11-06

Answered by Lead (11-04) and taken by PPM (11-04). I add the pass lines.

| Step | What the person sees | Pass line |
|---|---|---|
| B1. First ask | Chat offers `Create a project called ...`, then `Add a task to it: ...` | PA quotes both served on a fresh account: the project is created and named in the reply, the task is added, neither reply repeats an item or calls a todo a reminder (#2219). |
| B2. Skip landing (Path A skipped at step 3) | After Skip, Piper says it cannot read a repo yet (the Skip line above) and offers `Add a todo: review the deployment plan` | PA quotes the todo reply served: one item, no repeat, `todo` not `reminder`. |

Both pass on a quoted served reply from PA or Web, not on a unit pin. #2219's list and ordinal rows are part of B1 and B2 and are being judged separately (see the 11-06 log).

## Settings, project and repo, and the sign-in prompts: 2026-11-06 (item 10 of the first two-week sprint)

Sources read: `templates/settings-index.html` (12 cards in one flat grid, Integrations ninth), `templates/settings_projects.html` line 348, the issues #2273, #2272 and #2275. Not read: the app shell's way into Settings, the project page, and any served page. Everything below is a proposal until Web serves it.

### #2273: Settings, and the path to Integrations

Today the 12 cards sit in one grid in this order: Personality, Learning & Patterns, Privacy & data, Preferences, Account, Connected apps, Transparency, LLM API Keys, Integrations, Projects, Invites, Advanced. A person looking for where to connect GitHub meets eight cards about something else first, and the Integrations card reads "Monitor health and test connections", which is about checking and not about connecting.

**Four headed groups, in this order, same cards:**

| Group heading | Cards |
|---|---|
| **Connect Piper to your tools** | Integrations, Projects, LLM API Keys, Connected apps |
| **About you** | Account, Preferences, Personality, Learning & Patterns |
| **Privacy and trust** | Privacy & data, Transparency |
| **For admins and developers** | Invites, Advanced |

- Integrations is the first card on the page.
- **Integrations card description:** `Connect your tools, such as GitHub, and check that each one is working.` It names GitHub because that is the connector this beta is about, and it lists no other service, because I have not confirmed which are offered in this beta (Slack is hidden).
- **Invites card:** `Mint alpha invite codes…` becomes `Create invite codes, see which were used, and revoke the rest.` (the host and the word are beta now). Whether non-admins see this card at all is Web's to check. I have not.
- **Settings subtitle:** unchanged.
- **Path from chat:** every reply that sends a person to Settings says `Settings, under Integrations`, as the dead-grant reply does. That matches the group, so no change.
- **Pass line:** Web walks from a fresh sign-in to the Integrations page and quotes the page. Integrations is the first card, and the first step of that walk (reaching Settings from the app shell) takes at most two clicks. Web counts the clicks, because I have not read the shell.

### #2272: the project and repo model a person sees (revised 2026-11-06 11:05 after Lead's source read)

Lead confirmed from source that linking a repo to a project writes one record, and the only reader of it is the chat answer to "which repos are on project X". Issue reads do not use it (the project-scoped resolver was retired, #1315). GitHub reads use the repo the person names, else their default repo. My first paragraph claimed the link makes Piper read the repo's issues for that project. That was untrue as built, and it is withdrawn.

**The paragraph (for the issue's first box):** A project is a piece of work you track in Piper. A repository is a GitHub repo. A project can have no repository, one, or several. Linking a repository to a project records that it belongs there, and Piper shows it when you ask which repositories a project has. It does not change which repository Piper reads: Piper uses the one you name, or your default.

**Page words (use the page's own verb, "link"; nothing built):**
- Button: `Link a repository`. Field: `owner/name`.
- Empty state on a project with none: `No repository is linked to {project} yet.` It says nothing about what a link does for reads.
- Unlink beside each repo: `Unlink`. Confirm: `Unlink {owner/name} from {project}? This only removes the link in Piper. The repository itself is not changed.` (Lead: true as built, no GitHub call.)

**Chat words:** when a project has no repo: `{project} has no repository linked yet. You can link one on its project page.` No chat phrase is offered while #2271's loop exists.

**If the product wants linking to mean "read this project's issues from this repo,"** that is a build and an Arch question (#1315 retired it on purpose). Until then no copy says it.

### #2275: the sign-in screen's prompts

The line is accepted and on the issue (PPM's, fitted: "can write your standup"). The prompt picks, from asks Lead says serve with no connector:
1. ~~`What changed in my tasks and projects this week?`~~ **Replaced 2026-11-06 11:13** by `Show my todos`. PA's preview showed a count (7) over three names, and on a fresh account it would answer "nothing new", a poor first impression.
2. `Add a todo: review the deployment plan` (clean on PA's preview quote)
3. ~~`Show my open GitHub issues`~~ **Dropped 2026-11-06.** Lead: what a fresh connected account gets depends on a default repo, and the connect step doesn't set one (#2268's family), so even a tagged prompt may promise more than it gives. The screen shows prompts 1 and 2 only, until a default repo is set at connect.

- **Lead to confirm** that 1 and 2 serve cleanly on a fresh account with no connector, and that 3 does not promise more than it gives before the connect. Otherwise the screen shows only 1 and 2.
- The #2219 rows being judged on the todo reply are the reason 2 is on the list.
- **Pass line:** Web quotes the sign-in screen on alpha with the line and the prompts.
