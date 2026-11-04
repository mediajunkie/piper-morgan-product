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
| 3. Connect GitHub (new last step, before "Open Piper") | A card with Connect, the line about GitHub's page, and a Skip | "GitHub will ask you to approve Piper Morgan Alpha. Its page may show the name of the account that owns the app, which is Piper's and not yours. Piper only gets access to the GitHub account you approve there." After: "GitHub is connected as {login}." Skip: "You can connect GitHub later in Settings, under Integrations. Until then I can't read your repo." | Web quotes the card and the post-connect line on a non-owner login. |
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
