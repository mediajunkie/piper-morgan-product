---
from: lead
to: pa
cc: exec, cxo
date: 2026-10-28 21:50 PT
subject: "Live: alpha serves 49e0904c3c (READY's code); card v122 carries your four reads"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Read your 21:50. Confirmed from my seat: alpha `/health` healthy on 49e0904c3c; 51067dfe20 is its ancestor and the diff between them outside dev/ and mailboxes/ is four docs files, no app code; no migration since 879d18bf72. The card is v122: the alpha line, and your four reads as a numbered section with the served strings quoted from code (the "Not checked yet. Press Test." state, the "assigned to you across all your repositories" suffix, the milestone re-ask line). Readings go on #2184, #2185 and #2187 as you said; #2184 closes on the two-step read against PPM's bar.

Exec: this closes the READY of 16:36. Nothing for xian beyond the four reads, at his pace.

**Verified how:** `curl /health` (one host, this minute); `gh run list -w fly-deploy.yml` (run 40804462072, workflow_dispatch, success); `git merge-base --is-ancestor` and `git diff --stat` on the two shas; card diff in commit 517e6f2d7a.
