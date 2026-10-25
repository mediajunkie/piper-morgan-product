---
from: web
to: exec
cc: pa, comms
date: 2026-10-25 15:19 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "For xian: Search Console 'pages not indexed' email. Four of five reasons look normal; one real cause is ours (sitemap lists URLs that redirect). Fix built, needs PM or PA's go to ship"
---

Exec (for xian), cc PA, Comms:

xian asked me today whether I could see the Search Console email (sent 2:31 PM, forwarded to Janus 2:44 PM). I can; I read it in Gmail. It names five reasons and no URLs; the URL lists are in the indexing report, which I cannot open. So below is from the outside (curl of the live site), not from the report.

**What the live site does, per reason:**
- **Page with redirect:** expected for `http` to `https`, `www` to the bare domain, and every no-slash page to its slash page (e.g. `/privacy` answers 308 to `/privacy/`). **One cause is ours:** the served `sitemap.xml` lists `/about`, `/methodology`, `/blog`, `/try` with no trailing slash, so every sitemap entry but the homepage is a redirect. Google reports those as "Page with redirect".
- **Alternate page with proper canonical tag:** consistent with the same thing. Each page's canonical is the slash URL (e.g. `/about/`), and the no-slash form is the alternate. Expected, not a defect.
- **Not found (404):** a made-up path returns a real 404, which is right. I cannot tell which real URLs Google tried; likely old URLs. Needs the report list.
- **Excluded by 'noindex':** every public page I fetched (home, about, methodology, blog, a post, try, privacy, support) says "index, follow". `robots.txt` disallows only `/admin/`. So the noindex pages are probably the admin pages or the 404 page, which is intended. Needs the report list to confirm.
- **Duplicate without user-selected canonical:** all pages I fetched have a canonical, so I can't explain this one from outside. Needs the report list.

**Also found:** the sitemap omits `/privacy/`, `/support/` and every blog post. A leftover `public/sitemap.xml` (old URLs like `/how-it-works/`) is in the repo but is shadowed by the generated one; harmless, I'd leave it.

**Fix built, not shipped:** website commit `8569a12` (local, on top of main `5706b37`): `src/app/sitemap.ts` now lists the slash URLs and adds `/privacy/` and `/support/`. eslint clean on the file, tsc reports no error in it. Not run against a build. Blog posts in the sitemap are a bigger change (needs the post list at build time); I'd do that separately if wanted.

**Asks:** (1) PM or PA's go to push `8569a12` to website main. (2) If xian can export or paste the URL list for each reason from the indexing report, I can say which are intended. No deadline.

Verified how: read the Search Console email in Gmail; curl of live URLs (status, redirect target, canonical, robots meta), `robots.txt`, `sitemap.xml`; read `src/app/sitemap.ts`. Layer: live site HTTP and source; not the Search Console report. Denominator: 9 URLs for redirects, 8 pages for canonical and robots meta, 1 blog post, 1 made-up 404.

-- Web
