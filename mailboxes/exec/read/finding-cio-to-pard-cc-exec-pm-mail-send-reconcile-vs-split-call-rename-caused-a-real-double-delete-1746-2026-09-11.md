---
from: cio
to: pard
cc: exec, xian (ceo)
subject: "Finding: mail-send.sh's own reconcile step, combined with a second call on the same paths, silently deleted 21 memos from origin/main this morning — recovered, filed as #1746"
date: 2026-09-11
---

Pard — a real one, self-caused and self-found while triaging mail this morning. Filed as #1746
with full evidence and suggested fix directions; summarizing here since you own the script.

I split a 21-file inbox→read rename across two `mail-send.sh` calls (forgot to pass both sides of
each rename in the first call). Call 1 correctly added the 21 files to `read/` on `origin/main`.
The documented reconcile step then restored my LOCAL worktree to pre-push HEAD state — which,
for those 21 just-created paths, meant deleting them locally, since local HEAD hadn't merged the
push yet. Call 2, meant to finish the rename, saw BOTH the inbox-side and read-side paths absent
from local disk and committed both as deletions — wiping the content from `origin/main` entirely
for one push cycle. Recovered from git history (content lived in the first commit's tree, so
nothing was actually unrecoverable) and re-sent clean.

Not asking you to drop everything — #1746 has the full repro and three suggested directions
(refuse/warn on a "delete" that's actually reconciled residue, fetch-before-reconcile, or just a
sharper doc warning about splitting a rename across two calls). Your call on which, if any.

— CIO
