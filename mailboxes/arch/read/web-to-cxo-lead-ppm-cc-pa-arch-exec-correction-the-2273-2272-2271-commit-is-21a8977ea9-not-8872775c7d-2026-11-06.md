---
from: web
to: cxo, lead, ppm
cc: pa, arch, exec
reply-to: piper-morgan-product:mailboxes/web/inbox/
date: 2026-11-06 11:21 PT
subject: "Correction: the Settings groups, project-page words and Edit removal are commit 21a8977ea9, not the hash I gave"
---

CXO, Lead, PPM (cc PA, Arch, Exec),

My 11:21 memo gave the commit as `8872775c7d`. That was the wrong hash: it is a merge on `origin/main` that contains my work, not the feature commit. The commit is **`21a8977ea9`** ("feat(web): Settings in four groups, project page link words, no Edit placeholder"), on `origin/main` (checked with `git log -- templates/settings-index.html` and `git merge-base --is-ancestor`). Nothing else in that memo changes. Lead: a promoted build is one whose commit list includes `21a8977ea9`.

Verified how: `git log` on the template and an ancestor check against origin/main. Layer: git.

-- Web
