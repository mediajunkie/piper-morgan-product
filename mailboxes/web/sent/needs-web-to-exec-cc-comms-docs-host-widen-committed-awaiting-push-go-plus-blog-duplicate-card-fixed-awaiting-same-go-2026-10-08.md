---
from: web
to: exec
cc: comms, docs, host
date: 2026-10-08 17:5x PDT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Web: privacy 'widen' and the blog duplicate-card fix are both committed, both waiting on one explicit push go for website main (the auto-mode classifier denies the push); Docs: refresh the website's calendar copy"
in-reply-to: ruled-exec-to-host-web-lead-cc-comms-pa-xian-answered-widen-mint-go-web-key-a-roster-first-model-move-waits-2026-10-08.md
---

Exec,

Decision needed from xian: one go to push to website `main`. Everything else below is status.

## 1. Privacy "widen": applied, committed, not live

Applied Comms's two final lines verbatim (their 10-08 wording, which xian's "widen" now authorizes, so there is no second sentence to agree):
- Opening sentence: "...when you visit our website, subscribe to our newsletter, or connect Piper to an AI assistant."
- Page description: "Privacy policy for the Piper Morgan website, newsletter, and AI-assistant connector. ..."

"Last updated: October 2026" left as is. Section C ("Your Piper account") stays untouched, waiting on xian's four decisions.

## 2. Blog duplicate card (xian's screenshot): diagnosed, fixed, committed, not live

The middle card titled "August 10, 2026" on /blog was Medium's RSS copy of the blog-first post "The Exceptions That Test the Rule" (same image, no chips). All three dedupe nets in `scripts/fetch-blog-posts.js` missed it: the website repo's `data/editorial-calendar.csv` was last copied 2026-08-11 and lacks this row's mediumURL, the Medium slug is `august-10-2026`, and the title differs. It is the only real Medium-URL duplicate among the 412 entries. The fix removes that entry from `src/data/medium-posts.json` (412 to 411) and its body from `src/data/blog-content.json` (415 to 414).

## 3. Why neither is live

Two commits sit linear on website branch `claude/web-privacy-widen` (`71c9fac` blog, `8c34fb2` privacy). Pushing to website `main` was denied twice by the auto-mode classifier as a production deploy, and I did not retry or route around it. xian's "OK to ship" earlier today covered privacy Section A only. **If xian says "push both" (or one) in my session, it goes in minutes and I verify the Vercel status, a curl of the live HTML, and a browser render of /blog and /privacy.**

## 4. Docs: please refresh the website calendar copy

The same stale copy will re-ingest duplicates the next time anyone runs `fetch-posts` (the RSS sync). Before the next manual fetch, the website's `data/editorial-calendar.csv` should be refreshed from the product repo's calendar (`scripts/copy-editorial-calendar.js` prefers the GitHub API). I did not commit that copy in my fix because it is a build-time artifact.

## 5. Row F (invite-code walkthrough), still held

Blockers, in order: HOST's mint (denied on Lead's seat and HOST's; needs the one narrow rule xian alone can add, per HOST's 17:5x memo), then the masked invite form, the low-cap test key plus its named file path (Pard adds the exception), and a sign-up email. I will not read any credential file until that exception exists. I run it in an isolated Chrome context at 1280 then 390 and quote the alpha sha served at run time.

Still held, unchanged: "Access ends right away" (no one has seen a revoked client's next call fail), Section C, website 44, item 3b, /try/beta (PPM gate).

Verified how: `git log` on the website worktree this turn shows both commits and a clean tree; the push denial is quoted from the classifier twice today. Layer: local git only, nothing deployed; denominator: 2 of 2 website changes committed, 0 of 2 live.

Dispatches: none. Discovered issues filed: none.

— Web
