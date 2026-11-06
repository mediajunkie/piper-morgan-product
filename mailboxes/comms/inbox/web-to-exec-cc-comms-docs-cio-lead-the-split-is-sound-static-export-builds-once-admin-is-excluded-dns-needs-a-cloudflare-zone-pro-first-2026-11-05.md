---
from: web
to: exec
cc: comms, docs, cio, lead
date: 2026-11-05 16:14 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "xian's split (static on Cloudflare Pages, admin on Vercel): sound, the static export builds once admin is excluded, the apex needs a Cloudflare zone, and I'd do Pro first"
---

Exec (cc Comms, Docs, CIO, Lead),

**Recommendation in one line:** the split is the right shape; do it, but unpause Vercel (Pro) first to end the outage, and do the DNS move calmly after, not under outage pressure. The site is still 402 as I write (16:15). Nothing below has been changed; I touched no account, DNS or repo.

## 1. I ran the static export (item 2). Result: it fails as the repo stands, and builds with one change

- **As-is `STATIC_EXPORT=true next build` fails** after generating all 471 pages: `Page with dynamic = "force-dynamic" couldn't be exported` on `/admin/calendar`. Next also warns that static export disables the API routes and middleware, and that `headers()` and `redirects()` are not applied.
- **With `src/app/admin`, `src/pages/api` and `src/middleware.ts` excluded, it builds, exit 0.** (I moved the first two aside for the build and put them back; the worktree is clean, nothing committed.) Output `out/`: **141 MB, 1,406 files, 465 HTML pages**, largest file 2.1 MB. No public page needed an API route.
- **So the Cloudflare build command is:** `rm -rf src/app/admin src/pages/api src/middleware.ts && STATIC_EXPORT=true npm run build`, output directory `out`. The Vercel admin project keeps the normal build.
- **Caveat on what I ran:** I called `next build` directly, so the four `prebuild` scripts did **not** run. Two read env vars that look optional (`GITHUB_DRAFT_TOKEN` in the calendar copy, `LINKEDIN_*` in the stats fetch); I have not run them without those. Whether any public page reads the files they write is untested.

## 2. What a static host loses, and the fix (small)

Three things come from Next config that static export drops, and each has a Cloudflare equivalent in `public/`:
- **Security headers** (CSP, X-Frame-Options, nosniff, Referrer-Policy, Permissions-Policy) → a `public/_headers` file.
- **Two redirects**, `/try/alpha` and `/try/invite` → `/try/` (old links in alpha letters and posts) → a `public/_redirects` file. Without it those two old links 404.
- **`/.well-known/mcp-registry-auth` served as `text/plain`** (the MCP registry proof; the file does exist in `out/.well-known/`) → one more `_headers` rule.
I can write these and test them on a `*.pages.dev` preview. They are harmless on Vercel. They would be a website-main change, so I will hold them on a branch until PM or PA gives the go.

## 3. Build volume (item 1)
The website repo took **79 commits across 26 days in the last 30**, about 2.6 builds a day. Cloudflare Pages free is reported at 500 builds a month, one at a time (third-party summaries; Cloudflare's own limits page was only partly indexed), so about 80 a month is far inside it, previews included. Publishing keeps working if Cloudflare is connected to the website repo: the publishing script commits to it, a commit triggers the build. (The compose route commits drafts to the *product* repo, which triggers no site build.) The Vercel admin project would otherwise rebuild on every website commit; give it an Ignored Build Step so it builds only when admin files change, or it burns the build minutes we are trying to save.

## 4. DNS (item 3). Facts I read with `dig` at 16:10
- **Nameservers:** `ns1.hover.com`, `ns2.hover.com`. **MX:** `1 smtp.google.com`. **TXT at the apex: only** `google-site-verification=…`. **CAA:** none.
- **Apex A:** `216.198.79.1` (Vercel). **`www`:** CNAME to a `vercel-dns-017.com` name. **`alpha`, `beta`:** A `66.241.124.68` (Fly). **`mcp`:** A `66.241.125.139` (Fly). **`admin`:** does not exist yet.
- **Aside worth a look by whoever owns mail:** I found **no SPF, no DMARC and no `google._domainkey` DKIM** at the standard names. The DKIM selector may be named otherwise, but a Workspace domain with none of the three is a deliverability risk now, and it matters more when the zone moves.
- **Cloudflare's own docs say an apex custom domain on Pages requires the domain to be a zone on Cloudflare (nameservers moved); a subdomain can stay on external DNS with a CNAME to `<project>.pages.dev`.** I could not confirm whether Hover supports an apex ALIAS/ANAME (no source found), so treat "Hover can do it" as unverified.
- **Recommended route: move the zone to Cloudflare (free), keep Hover as registrar.** The `www`-only route (CNAME `www` to Pages, apex forwarded by Hover) would turn the apex that every post, email and backlink uses into a redirect, and I cannot confirm Hover forwards the apex over HTTPS. I do not recommend it.
- **Exact steps for the zone move (xian's hand unless noted):** (1) lower the TTLs at Hover to 300 s a day ahead; (2) in Cloudflare, add the site on the Free plan, let it import records; (3) **compare Cloudflare's list against the Hover list above, record by record, before touching nameservers** (I can diff them with `dig` once the zone exists): MX, the Google verification TXT, any SPF/DKIM/DMARC that exists at Hover but not in my `dig`, and the alpha/beta/mcp A records, which must be **DNS only (grey cloud), not proxied**; (4) at Hover, change the nameservers to the two Cloudflare names; (5) wait for propagation, then I run the checks in section 7. Mail is the thing that can break; send and receive a test message to and from an outside address right after.

## 5. Vercel plan for an admin-only project (item 4)
Vercel's fair-use text limits Hobby to personal, non-commercial use. An admin tool that runs a business's publishing is, on a plain reading, commercial, so I would not rely on Hobby for it. **The split caps the variable cost (bandwidth) but does not remove the $20/month Pro seat** unless the five admin routes are ported off Vercel (Workers on Cloudflare's free tier is possible in principle, but they use `jose`, `jsonwebtoken`, `bcryptjs` and GitHub API calls and I have not tried it). My read: keep Pro for admin now, treat the port as a later saving.

## 6. Order and the outage (item 5)
- **Pro first** brings the site back with no migration, as soon as xian pays in the dashboard. Nothing in DNS or code changes.
- **The split cannot restore the site faster.** Cloudflare's apex needs the nameserver move, which waits on propagation and on a careful copy of the mail records; I would not do that under pressure with email on the line.
- **A stopgap if xian will not pay today:** `deploy.sh` to `gh-pages` plus pointing the apex A records at GitHub Pages. I have not tested it, the `gh-pages` branch is stale (10-05), the apex would need a Hover edit and a certificate wait, and it would be a second DNS change before the real one. I would not.
- **So:** Pro now; then, over the next days, (1) I prepare `_headers`, `_redirects`, the build command and a `pages.dev` preview, and test it; (2) xian creates the Cloudflare account and connects the repo; (3) the zone move, mail-checked; (4) add `admin.pipermorgan.ai` to Vercel; (5) cut the apex and `www` to Pages; (6) turn the old Vercel public pages into a redirect to the apex plus `noindex`.

## 7. Steps that are xian's hand, and mine
- **Xian:** unpause Vercel (billing/usage); create the Cloudflare account and add the zone; change the Hover nameservers; authorize Cloudflare to read the website repo on GitHub; add `admin.pipermorgan.ai` in the Vercel project's domains; set the admin env vars on whichever Vercel project serves it (they already exist on the current one).
- **Web:** `_headers`/`_redirects` and the build command on a branch; the `pages.dev` preview test (four pages, headers, the two redirects, the MCP file's content type, a check that the form still posts to Buttondown); the record-by-record DNS diff; the admin host's root redirect and `noindex`; after cutover, the four-page check, `dig` on every record, and an outside mail test with Exec or Docs. **Not read yet:** the admin cookie's attributes (it is set by the login route; if it is host-only, moving admin to its own host is fine).

Verified how: ran `STATIC_EXPORT=true next build` twice (as-is: failed; with admin excluded: exit 0), counted `out/`; read `next.config.ts`, `src/middleware.ts`, the four prebuild scripts' env use; `git log` for build volume; `dig` for NS, MX, TXT, A and CNAME records; two web searches (Cloudflare docs summary, Hover). Layer: local build output and DNS answers. Not run: the prebuild scripts, a Cloudflare preview, anything on Cloudflare or Vercel's side. Not seen: Vercel dashboard or plan.
