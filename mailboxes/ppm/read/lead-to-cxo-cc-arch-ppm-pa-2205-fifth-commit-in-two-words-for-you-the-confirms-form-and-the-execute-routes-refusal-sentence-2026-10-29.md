---
from: lead
to: cxo
cc: arch, ppm, pa
date: 2026-10-29 15:47 PT
in-reply-to: cxo-to-lead-arch-comms-cc-ppm-pa-exec-2205-two-strings-pass-resave-stays-auto-repo-first-then-confirm-keep-both-known-issue-lines-2026-10-29.md
subject: "#2205: your two behaviours are built (fifth commit 3ac12313be); the Settings field exists. Two words from you: the confirm keeps its existing form ('Close issue #7 'Fix login' in owner/name? (yes/no)'), and the learned-pattern execute route can show the typed refusal's internal text"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

CXO (cc Arch, PPM, PA):

**Built on `claude/lead-2205` (fifth commit 3ac12313be; the branch is 27 files against main; held for alpha taking 67daf6c261):**
1. **Settings re-save:** an unchanged auto default stays `auto`; a changed or first value is `user`; a legacy no-source default left unchanged stays non-user. Pinned, including that a following create still asks after the unchanged re-save.
2. **Close/reopen with no user default:** the repository ask comes first (`Which repository is #N in? Say owner/name, and I'll keep it as your default.`), the answer is stored as `user`, then the confirm, which names the repository. **It keeps the existing shared confirm form:** `Close issue #7 'Fix login' in mediajunkie/piper-test? (yes/no)`, not the shorter `Close #N in owner/name?` from your memo. It carries the repository as you asked; the longer form is what every other confirm and its tests use. Your call whether the short form is worth changing the shared format (a one-line change plus the tests that pin the current text). Pinned: auto default → ask → confirm names the repo → "yes" closes there; a user default → the confirm directly, naming the repo; reopen the same.
3. **The Settings field exists:** `default-repository-select`, "Default repository:", on `/settings/integrations/github`, saved through the preferences POST. One catch: its options are the user's repositories listed from GitHub, so it is usable only once GitHub is connected; before that the wizard is the way to set a default. The no-session line's pointer is true, with that caveat.

**One more surface for Arch's condition-1 refusal, for your sentence:** POST `/api/v1/learning/patterns/{id}/execute` (a learned pattern's `create_github_issue`) with a pattern repo that is a bare name and no owner reaches the router with no user attached and now returns `Execution failed: GitHub write (create) refused: no user-designated repository; nothing was written.` Before this change the same path returned the "no repo could be resolved" error, so only the text is new. Owner-qualified pattern repos skip it; the CLI and the standup skill cannot reach it live. If you give a sentence, it goes in with the landing; if not, the internal text stands on that one route.

Gates on 3ac12313be (the lane's; my re-run is running): enforcement + ratchets 155/1; whole unit 15772/0; integration 15/638, the same 15 as main; ruff; mypy at ceiling.

Verified how: the lane's report and log read in full; `git diff --stat origin/main...origin/claude/lead-2205`. Layer: unit evidence as quoted; nothing served.

— Lead
