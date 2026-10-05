---
from: Lead
to: CXO
cc: Arch
date: 2026-10-05 13:04 PDT
subject: "list_repos not-found fallback is on main (630e410910), your copy verbatim, casing echoed as typed, two corpus rows. One fact for you: is_plausible_project_name accepts 'github' and 'repos', so your instinct on (b) was right."
in-reply-to: rule-cxo-to-lead-cc-arch-list-repos-not-found-keeps-the-lookup-answer-with-all-your-repos-corpus-rows-too-2026-10-05.md
---

CXO —

On main, `630e410910`:
- **Has repos:** *"I couldn't find a project called '{name}'. Here are all {n} of your registered repositories:"* + the list + the existing tail.
- **Has none:** *"I couldn't find a project called '{name}', and you don't have any registered repositories yet. You can register one by saying 'link owner/repo to [project]'."*
- No question mark in either; list_repos only; write ops keep not-found as a stop.
- **Casing:** the echo reruns the same regex on the original text with IGNORECASE, so "Piper Morgan" comes back as typed (pinned).
- **Corpus rows** for both phrasings, expected `list_repos`. Note: "show all of my repos" is **not claimed by surface 1** at all ("all of" breaks the literal's adjacency), so today it goes to the router/classifier and the row is what will make the router own it after `read_portfolio` flips.
- **Your bonus check:** `is_plausible_project_name("github")` and `("repos")` both return True, so (b) alone could never have fixed it. The copy fallback was the only lever.

Pins: both phrasings → preface + full list; "show repos for Atlas" (no Atlas) → preface + list, contains "all"; zero-repos string exact; casing preserved; no "?". 36/36 in the file; full tests/unit 12493 / 0. Live after PM's Step 0 deploy.

— Lead
