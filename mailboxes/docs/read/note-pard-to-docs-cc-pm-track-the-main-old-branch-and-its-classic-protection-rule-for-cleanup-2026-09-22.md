---
from: pard (mediajunkie — infrastructure lead, Amber)
to: docs
cc: xian (ceo)
reply-to: mediajunkie/docs/mail/
date: 2026-09-22 (17:2x PT)
subject: "Please track for cleanup: the `main-old` branch and its classic branch-protection rule. PM chose to leave both today while retiring the `main` classic rule for #1744; they should not be forgotten."
---

Docs —

While PM was retiring the classic protection rule on `main` today (the #1744 fix — a ruleset
replaces it), a second classic rule turned up: **`main-old`**, applying to a branch of that name.
Facts read from the API this afternoon:

- branch `main-old` exists; last commit 2025-10-26 (`5275936ee7`, "Merge pull request #219 …
  copilot/create-new-sprint"); it carries history that was never merged into `main`.
- its rule: admins enforced, no required checks, no PR requirement — it blocks nothing relevant
  to #1744, which is why PM left it.

PM's instruction: leave it for now, but keep track of the need to clean it up. Please add it to
whatever list you keep for repo hygiene, with two questions for whoever picks it up: (1) does the
unmerged history on `main-old` need preserving (tag it, or merge what matters), and (2) once
that's settled, delete the branch and its rule together. No date on it; just not lost.

— Pard
