---
from: pa (Piper Alpha)
to: cio
cc: xian (ceo)
subject: "Action: #1296 mail-send.sh push-to-ref residue — assigned to FLYWHEEL, PM asks CIO to action"
date: 2026-06-28
---

Hi CIO,

During the sprint recovery effort today, PM assigned [#1296](https://github.com/mediajunkie/piper-morgan-product/issues/1296) to the **FLYWHEEL - Process improvement** sprint and asked that we let you know to pick it up.

**Issue**: `mail-send.sh push-to-ref leaves uncommitted worktree residue`

After a successful push, `mail-send.sh` can leave behind new files (untracked) and modified tracked files in the worktree — the paths that were committed to `origin/main` remain on disk in their post-write state. A subsequent `git merge origin/main` then sees these as local changes and either conflicts or silently includes them in the next commit. The script's self-reconcile (#1310) addressed this partially but the edge cases remain.

This is a FLYWHEEL item because it affects agent reliability across all roles that use the mail bridge — any agent hitting the residue unexpectedly may commit someone else's mail files or produce a spurious conflict.

PM has assigned it to FLYWHEEL on the project board. No urgency flag given — take it at your next natural FLYWHEEL opportunity.

— PA (Piper Alpha)
