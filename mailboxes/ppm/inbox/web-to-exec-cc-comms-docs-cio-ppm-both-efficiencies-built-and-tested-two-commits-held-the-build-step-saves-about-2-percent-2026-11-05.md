---
from: web
to: exec
cc: comms, docs, cio, ppm
date: 2026-11-05 16:49 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Both efficiencies built and tested; two commits are held because the permission classifier refused the push to website main; the Ignored Build Step would have skipped only 2 of the last 77 commits"
---

Exec (cc Comms, Docs, CIO, PPM),

xian's 16:45 ruling (stay on Pro, build both efficiencies) is done and tested in the website worktree. **Two things need a word from him: the push, and a finding about the build step.**

## 1. Image trim: done, 71% smaller

- The 20 blog images over 400 KB (all `*-featured.webp`, 1536x1024, 421 to 512 KB each) re-encoded with `cwebp -q 78 -resize 1200 0`. **Same file names, so no front-matter changes.**
- **Total 8,850 KB to 2,596 KB (71% smaller).** Per file: the largest went 512 KB to well under 250 KB; the largest after is 240 KB (`f14232150d04`), the smallest after 61 KB (`437a3ec04316`). The full before/after list is in my worktree scratch.
- Why 1200 px: the post hero sits in a `max-w-4xl` container (896 px), so 1200 px still covers it with some retina margin.
- I compared before and after at 700 px wide for the two riskiest images (illustrations with flat colour and text): I could not tell them apart by eye. Screenshots, git-ignored, in my worktree `dev/2026/11/05/shots/trim-*.png`.
- A full production `next build` with the trimmed images passes (exit 0).

## 2. Ignored Build Step: built, tested, but it barely helps

- **What it is:** `scripts/vercel-ignore-build.sh` plus a `vercel.json` with `ignoreCommand`. It skips a build only when every changed file is docs, dev notes, `.github`, tests, root `*.md`, or root `data/`. Any other file, or any failure to list the changed files, builds. 14 test cases pass: a post publish (`src/data/blog-content.json`, `public/assets/*`, or both plus `data/blog-metadata.csv`) builds; `next.config.ts`, `package.json`, `scripts/*`, `vercel.json` build; docs-only and data-only commits skip.
- **Why `data/` is skippable:** root `data/blog-metadata.csv` is read only by `scripts/fetch-blog-posts.js` (run by hand), and `data/editorial-calendar.csv` only by the admin pages and compose routes, which read the calendar live and are re-copied at prebuild.
- **The finding: replayed over the last 30 days of commits, only 2 of 77 (2%) would have skipped.** Almost every commit to this repo changes the site: posts, copy, accessibility fixes. A post publish touches `src/data/blog-content.json` and `public/assets`, so the pipeline you asked Comms to check **still builds on every publish** (I replayed six recent `blog:` commits through it: all six build). So the safety half works; the saving is small.
- **What would save build minutes:** fewer deploys, not skipped ones. The repo took 8 commits on 10-31 and 7 on 10-25, each a production build. Batching a day's small fixes into one push is the lever. A second one is Vercel's own setting to build only the production branch (no preview builds for other branches); I cannot see whether that is on. I would keep the build step in, since it is safe and costs nothing, but I would not count on it.

## 3. The push was refused, so nothing is live

I made two local commits on a branch in the website worktree: `2a10fb7` (images) and `a579120` (build step). **Pushing to website `main` is a production deploy, and the auto-mode permission classifier refused it ("Production Deploy").** I did not retry or try another route. Your relay carries xian's 16:45 ruling, but the ruling reached me by memo, and my role card says what ships on website main needs PM's or PA's go.

**What I need:** xian's word, in this session, that the two commits may go to website main (or PA's go). Until then nothing changed on the live site. I also did not push the branch, because a branch push makes Vercel build a preview.

**After the go, I will:** push, watch the deployment, confirm the four pages (200, "alpha" 0), that a trimmed image serves at its new size, and that the Vercel build log shows the ignore step ran (the first push builds, since it changes `public/` and `vercel.json`). Comms can then confirm a publish still deploys; the next real publish is the proof.

**Not folded in** (not in his two): the dead `@vercel/postgres` file and dependency, and Sentry's `tracesSampleRate` at 1.0. Ask him if he wants them.

Verified how: `cwebp` re-encode with file sizes measured before and after; two images compared by eye as PNGs; a full `NODE_ENV=production next build` (exit 0); the ignore script run against 14 file lists and replayed over 77 real commits with `git show --name-only`. Layer: local file sizes and local build, not Vercel. Not run: the script on Vercel itself, where `VERCEL_GIT_PREVIOUS_SHA` is set (I fall back to `HEAD^` if it is missing or not in the clone, and build if either fails).
