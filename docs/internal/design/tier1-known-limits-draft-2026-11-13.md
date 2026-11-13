# Tier 1 part (d): known limits, draft 1 in CXO's register

**Owner:** Docs (wording for CXO's pass). **Date:** 2026-11-13. **Source page:** `docs/ALPHA_KNOWN_ISSUES.md` (last updated 2026-10-31). **Manifest row:** `d-known-limits`. **Status:** DRAFT. Nothing here is approved, and nothing here has been re-checked against the served build. Every limit is carried from the page as written on 10-31 and is marked unverified.

> **Superseded in part, 11-13:** Arch and PPM ruled the split (01M7APG3SB, 01M7AP6MM5). The clean rows now live in `docs/known-limits.md`, the three unsupported workarounds below are cut, and the row-to-issue map moved to the manifest's `d-known-limits` notes. This file stays as the record of why.

## What changed from the page, and why

- **Issue numbers and internal labels are out of the answer text.** They sit in the mapping table at the end, which is for the team and is not corpus text (CXO's leak list, Arch's ruling 01M7ANVMYA).
- **The "Fixed in 0.9.0" section is deleted.** Arch: the list never says "fixed", a fixed limit is deleted in a commit that has the fix as an ancestor.
- **Two rows come out because they say what Piper does not offer.** "Only GitHub and Google Calendar are offered" and the Slack row belong to part (a) (generated from `capability_catalog()`) and to the connectors source `b-connectors`. A row that says "X isn't offered" is a defect in this list (Arch).
- **Fix status is never given.** No dates, no "we're working on it" (CXO rule 8). All 15 issues named in the page's open list read OPEN on GitHub when I asked this morning (`gh issue view`, 11-13). That says nothing about whether the build a person uses has a fix, so it is not claimed.
- **Questions for CXO and Arch below.**

## The rows (candidate text, first person, short)

1. **Counting issues.** "When you ask how many issues you have open, my number can be too high. I may be counting issues assigned to you in every repository, including archived ones, and 'most recent' may not be in date order. Tell me which repository you mean and I'll stick to that."
2. **Milestones.** "I can't reliably list the issues in a milestone yet. If you ask, I may show you the wrong ones. Check the milestone in GitHub before you rely on my list."
3. **Deleting several todos at once.** "If you ask me to delete two todos in one message, I may delete only the first and not tell you about the second. Ask me one at a time."
4. **Overdue todos.** "When I show your todos, an open overdue one can appear crossed out, which makes it look finished. It isn't. Trust the todo itself, not the line through it."
5. **Sharing.** "Sharing a todo, list or project from the screen fails for now, and you'll see an error. I can't do it yet."
6. **Several requests in one message.** "If you put more than one request in a message, I can lose an offer or a question from one part, or show it as plain text. Send them as separate messages."
7. **A failed action that looks like a success.** "For one kind of action, a learned pattern, I can say it worked when it didn't. If it matters, check the result yourself."
8. **Preferences on a repeated question.** "If you ask something I answered recently, I may reuse that answer and skip a preference you've set since."
9. **Switching chats.** "When you switch between chats the whole screen redraws and flashes. Nothing is lost."
10. **iPad in portrait.** "On an iPad in Safari held upright, a new chat can open as an empty gray panel with the message box pushed off the screen. Turn it sideways or use a desktop browser."
11. **Deleting or archiving a chat.** "I can't offer you a button to delete or archive a whole conversation right now. You can hide a chat from History."
12. **Private session.** "The 'Start private session' switch in History only changes how the page looks. It doesn't change what I keep. Don't rely on it for privacy."
13. **The Claude and MCP connection.** "Using me inside Claude or another MCP client is newer and rougher than the web app. Expect more rough edges there."

## Facts in the draft I could not stand behind and why

- **Row 11, "You can hide a chat from History."** The page says only that delete and archive controls are unreachable. The hide step comes from the page's "Needs Testing" table ("Hide or delete a chat"), which is a test target and not a confirmed capability. I have not seen it work. CXO: cut it, or I check it first.
- **Row 10, "Turn it sideways or use a desktop browser."** The page offers no workaround. I invented this one. Cut unless someone confirms it.
- **Row 1, "Tell me which repository you mean and I'll stick to that."** The page gives no workaround either. Treat as a placeholder. CXO rule 6 says claim only what is built.
- **Row 8** paraphrases a cache-hit cause from the issue title, which I read as a one-line title only.
- Every other row follows the page's wording closely, with the same limits, but carries the page's own date.

## Decisions the rows can't make

1. **Verification (Docs).** Each row needs a check on a served build (a hosted beta account, or a clean-clone local run) before it gets a verified date. I start no server and use no account, so this is owed and needs xian's rule-7 route for a key or an account, as for the guide's chat step.
2. **Sections that are not limits (CXO and Arch).** The page also holds "Needs Testing", "How to Report Issues" and "See Also". Arch made the whole file one manifest row, so those would be retrieved as Tier 1 text. "Needs Testing" is tester work and could mislead a user into thinking those features are in doubt. Options: (a) keep the file as the limits list only and move the tester sections into `ALPHA_TESTING_GUIDE.md`, (b) keep them and exclude them by heading in the row. I recommend (a). It means editing the tester page, which testers use today, so I will not do it without a yes.
3. **Rename (Docs, Arch said Docs' call).** "ALPHA" is wrong for a v0.9 private beta page, but the name appears in `cut-release` step 3d and other links. I recommend keeping the name until the Tier 1 build lands and renaming once, in one commit, with the 3d line.
4. **Whether the tester-facing page itself changes** to drop issue numbers. Testers report by number today. I would keep the numbers on the tester page and generate the corpus text from this draft, but Arch ruled one file, so this needs an answer.

## Mapping, team-only (not corpus text)

| Row | Issues | GitHub state read 11-13 |
|---|---|---|
| 1 | #2185 | OPEN |
| 2 | #2184 | OPEN |
| 3 | #2025 | OPEN |
| 4 | #1961 | OPEN |
| 5 | #2166 | OPEN |
| 6 | #2041, #2030 | OPEN |
| 7 | #2208 | OPEN |
| 8 | #2056 | OPEN |
| 9 | #1515 | OPEN |
| 10 | #1907 | OPEN |
| 11 | #1516 | OPEN |
| 12 | #1164 | OPEN |
| 13 | (no issue on the page) | n/a |
| removed | #1497, #1481 (Slack), plus the offered-set line | OPEN |


## Held rows after CXO's pass and PPM's calls (11-13), kept out of `docs/known-limits.md`

Moved here so they cannot be indexed before they pass.

- **Deleting several todos at once (#2025).** Held by CXO until PA's served check in both shapes (a list shown, and "delete todo 1 and 2" with none). Arch: ADR-083 D5 may have fixed the shown-list half. Keep only the half that still fails, delete the row if both pass. Text if it survives: "If you ask me to delete two todos in one message, I may delete only the first and not tell you about the second. Ask me one at a time."
- **Deleting or archiving a chat (#1516).** Held by PPM until PA's read, because the tester page's Needs Testing table says hide or delete works from History. CXO had passed the wording. One of the two documents is wrong.
- **A failed action that looks like a success (#2208).** CXO returned it: "a learned pattern" is internal. Facts I read in the issue (not served): a suggested action that creates a GitHub issue can be reported as done when it failed, through the learned-pattern execute route. I do not know how a person meets that route in the screens, so I cannot name the action in a user's words yet. Needs a reader of the Learning page or a code read, and PA's served read. CXO's kept line: "I can say it worked when it didn't. Check the result."
- **Preferences on a repeated question (#2056).** CXO: re-check that it still happens on the served build before passing. If it does: "If you ask me something I answered recently, I may repeat the old answer and miss a preference you changed since."
- **The Claude and MCP connection.** Off the list under PPM's rule (b) and CXO. If a specific limit meets (a) to (c) it gets its own row. The example named is a "Connection closed" on the first request after a long gap, held until the count on #2342 rows 2 and 3 is read.
