# Proposal: an MVP onboarding to first value

**Author:** PPM, 2026-11-04. **Status:** proposal for xian's sprint-cadence talk (opened 11-03). Nothing here is scheduled; dates and sprints are xian's.
**Source:** xian's stated next focus from the 11-04 beta session by his advisor (Exec's memo, 11-04 13:14): before other plumbing, an onboarding that gets most new users to one valuable thing in their first session. Design it, build it, then test it with beta users.

## What the session showed

The first end-to-end beta attempt never reached a valuable thing. Each step that stopped it is now filed:

| Step a new person takes | What stopped it | Issue |
|---|---|---|
| Sign in | Email sign-in fails after a username is set | #2267 |
| Read the sign-in screen | A logo, nothing about what Piper does | #2275 |
| Add an AI key | No word that a Claude subscription excludes API access | #2274 |
| Run the wizard | Records a repo, doesn't connect GitHub | #2268 |
| Find where to connect | Settings, Integrations hard to find | #2273 |
| Connect GitHub | GitHub's page reads "Authorize mediajunkie" (the app owner) | #2266, plus xian's app-transfer decision and CXO's connect-card line |
| Ask about the repo | Routed to documents; an invented "link repo" command; a "yes" loop | #2270, #2269, #2271 |
| Understand project vs repo | Chat merges them; the page can't attach a repo | #2272 |

So the onboarding isn't a new feature first. It's this path made to work, then designed toward one valuable moment.

## The proposal

1. **Define first value per user type, before any build** (CXO designs, PPM sets the success criterion).
   - *The practicing PM who wants agentic help:* with GitHub connected, one useful read of their own work. A standup or "what changed" over their real repo, or a triage of its open issues.
   - *The person who needs product support but has no PM:* from a product idea, a short plan they keep (an artifact under their documents, PDR-102 C1), with no connector needed.
   - **Success criterion (proposed):** a new account reaches that moment in its first session, without help from us, and the person says it was useful. Measured on beta users, as a count of n of N sessions.
2. **Make the path work first.** In order: **#1551 at the head** (xian 11-04 16:06: the per-user isolation guard lands before any new invitation; its guard is on main c77eb9bbc2, with Arch's validation and per-site rulings owed); then #2261 (narrow the `repo` scope, through #2174's check) with #2178 (revoke at GitHub on Disconnect), both before invites (PPM 18:35); #2266's guard served (done 11-04 13:38), #2267, then #2268, #2273, #2274 and #2269, which are the steps between sign-in and a connected repo. #2270, #2271 and #2272 follow, because the first question after connecting hits them. #2275 comes with the design, since its prompts are the first-value prompts.
3. **Then build the designed flow.** The wizard leads to the user type's first-value moment and ends there, not at Settings.
4. **Then test it with beta users,** using scenarios with clear pass lines (the advisor's suggestions):
   - contributing to an existing open-source repo (PM type);
   - working backwards from a product idea to a plan (no-PM type);
   - an A/B: the same opening prompt in Piper and in plain Claude, judged for what Piper adds that Claude doesn't. A tie is a finding, not a failure.
   HOST runs the sessions; CXO judges the experience; PPM keeps the n of N.

## What it displaces

Proposed: this goes ahead of the remaining PUB plumbing that no new user would see in their first session. The Production plan's PUB, H and V rows on the path above stay. Others wait unless xian says they don't. Which rows move is a sprint question for xian; PPM will mark the candidates on the map once he picks the shape.

## CXO's design and PPM's answers to it (11-04 13:29)

CXO's first cut is `docs/internal/planning/onboarding-first-session-design-cxo-2026-11-04.md`. Path A (a PM with a repo) is written in five steps, each with a pass line. Path B waits on Lead: the shortest ask that ends in a saved plan, and whether it needs a connector.

PPM's answers to CXO's two product questions (acceptance criteria, so PPM's call; xian can overrule in the sprint talk):
1. **The wizard ends at the first ask (step 4), not at "Setup Complete".** The onboarding's acceptance is a served first-value reply, so its last page must be that reply.
2. **Skip is allowed at the connect step in beta.** Path B needs no repo, and GitHub-bearing invites are held until #2266's guard is served and the census is clean, so some beta accounts can't connect yet. A skip says plainly that Piper can't read a repo yet (#2268's line), then lands on Path B's first ask. Until Path B serves, it lands on an ask Lead confirms serves with no connector.

**Path B and the skip landing (Lead's answer and CXO's acceptance, 11-04; PPM 15:35):**
- **Path B's first value** is two asks that save with no connector: create a project, then add tasks to it. A plan the person keeps is a project with tasks in it.
- **The skip landing,** until Path B serves, is `Add a todo: review the deployment plan` (a required canonical row, serving today per Lead).
- **Both pass only when PA quotes them served on a fresh account with a clean reply** (CXO's condition). #2219 (todo replies repeat the item and call todos "reminders") is the known risk. If the todo reply still repeats, #2219 is fixed first, and nobody words around it. So #2219 joins the path in step 2, ahead of the designed flow.
- The "Connected as {login}" line on the card and in the connect reply is #2279 (on alpha 56f3d41bb2 at 16:41, awaiting Web's render check; filed 15:35), on the connect step beside #2266.

## xian's ruling, 11-04 19:31 (relayed by Exec)

- **No invitations of any kind** until the tenancy P0s are done. No design partners are lined up and no lawyer is lined up, so #2063 stays open and unscheduled.
- **P0, before any invite, in order:** #1551's served bar, then #2261 (narrow the GitHub scope, `public_repo` if D3 fails) with #2178 (revoke at GitHub on Disconnect). The Slack and Notion offer pin is done inside #1551.
- **P1, keeping their place:** #2157 (restore drill) and #2158 (manual purge). They aren't hold conditions.
- **For step 4 of the proposal:** the beta-user tests wait on invitations, so they run after the P0s. Until then the path is checked with existing test accounts (PA, Web), which needs no invitation. PPM 19:34.

## Questions for xian

1. Is this the next sprint, or a lane beside the current Production order?
2. Are the two first-value moments above the right ones, or should one user type go first?
3. The OAuth app transfer to an organization account (Exec has it in front of you) decides the connect step's words. Does it happen before the onboarding test? *Answered 11-04 15:43 (Exec): yes to the transfer, org name probably "Piper Morgan" (CXO recommends it, 15:47). Order (Arch 15:45): census first, then the transfer and Arch's four re-checks, then Web's check 1 on dinp-machine after a revoke. So the onboarding test runs after the transfer, and the connect step's words are judged on the org-owned page. PPM 15:50.*

## Not decided here

The flow and words (CXO), how it's built (Arch, Lead), dates and slips (xian). #2276 (feedback shortcut) helps the test sessions but isn't on the path. #2277 (Radar as the landing page) and #2278 (chat layout) are recorded and not proposed here.

Verified how: Exec's 11-04 13:14 memo read in full; the issue numbers are the ones PPM filed and placed by 13:18 (gh output); duplicate checks by `gh issue list --search` across 30 queries. Layer: mail and GitHub. Nothing served or measured.
