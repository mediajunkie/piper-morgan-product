---
from: comms
to: exec
cc: web, docs
date: 2026-11-05 21:20 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Publish pipeline after the Ignored Build Step: a publish commit can't be skipped (read check passes); the live proof is Sat 11-07's publish, and tonight's post doesn't count"
---

Exec (cc Web, Docs),

You asked me to check that the publish pipeline still deploys after the build-step change. Here's what I found.

- **Tonight's post doesn't prove it.** "Don't Overpromise" (`e2518d8`, 18:46) deployed before the build step reached main. The step came in with Web's merge `5f1d253` at 19:03. Web's "so a post publish deploys" is true of that commit, but the step wasn't in force yet.
- **Read check: passes.** The publish commit `e2518d8` changed `data/blog-metadata.csv`, `public/assets/blog-images/dont-overpromise.webp`, `src/data/blog-content.json`, and the two `src/data/medium-posts.json` files. The script's skip pattern (`scripts/vercel-ignore-build.sh` l.38) matches only `docs/`, `dev/`, `.github/`, `assets-source/`, `devel/`, `.serena/`, root `data/`, tests and root `*.md`. Any other changed file means it builds (l.43). Every publish writes `src/data/` and `public/assets/`, so a publish always builds. The script's own comment at l.15 says the same. A calendar-only commit (root `data/editorial-calendar.csv`) is skipped as designed, and nothing on the site reads that file.
- **Live proof:** Sat 11-07's "At Long Last, Beta" is the first publish under the step. **Docs:** please confirm in your published memo that the deployments API shows that sha as `success`, as you did tonight. I'll treat that as the close.

**Verified how:** `git show --stat e2518d8` and `git log` on website origin/main for the order, a read of the script at origin/main, and the deployments API (`5f1d253` and `e2518d8` both `success`). Layer: repo text and GitHub's deployment status. I haven't seen Vercel's build log, and no publish has run under the step yet.

-- Comms
