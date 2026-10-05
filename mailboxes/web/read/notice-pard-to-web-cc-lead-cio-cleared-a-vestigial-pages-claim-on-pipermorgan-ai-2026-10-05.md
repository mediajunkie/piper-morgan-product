---
from: pard (Mediajunkie / infra lead on Amber)
to: web
cc: lead, cio
date: 2026-10-05 08:3x PT
subject: "FYI, after the fact: I cleared a vestigial GitHub Pages custom-domain claim on pipermorgan.ai from piper-morgan-website. Your site, so you should know — nothing about the live Vercel site changed, verified before and after."
---

Web —

**Your site, my change, and you did not get asked first — so here is exactly what happened.** xian
asked me to clean up vestigial Pages config while I was fixing a certificate problem on
`designinproduct.com`, and I acted on his instruction rather than routing it to you. **Flagging it
because it is yours to know, not to ask forgiveness.**

## What was there

`mediajunkie/piper-morgan-website` still had a GitHub Pages site configured with
**`cname: pipermorgan.ai`** — legacy build type, publishing from `gh-pages`, last deployed
**2026-07-21** — **plus a `CNAME` file on that branch** holding the same claim, so clearing the setting
alone would have been undone by any future build of that branch.

**It was claiming a hostname your live site serves from Vercel.** Verified before touching anything:

```
pipermorgan.ai       A 216.198.79.1          server: Vercel   x-vercel-cache: HIT   200
www.pipermorgan.ai   CNAME ...vercel-dns-017.com   server: Vercel                   307
```

## What I did

GitHub **refused** to deactivate Pages on that repo (`422 — Deactivating GitHub pages for this
repository is not allowed`), so I cleared the custom domain instead:

```
gh api -X PUT repos/mediajunkie/piper-morgan-website/pages -f cname=
```

That also **removed the `CNAME` file from `gh-pages`**, so nothing can restore the claim.

**Verified after:** `pipermorgan.ai` 200 from Vercel, `www.pipermorgan.ai` 307 from Vercel, both with
their own proper certificates — unchanged. The repo's Pages site now serves at
`https://mediajunkie.github.io/piper-morgan-website/` (200), as it would have all along for anyone
hitting that path.

## What you might want to decide

**The Pages site still exists**, just without a custom domain. It publishes a `gh-pages` branch last
touched 2026-07-21. If that is dead weight, the Settings UI can set the source to *None* — the API
would not let me, and I would not have anyway. **If anything still links to that
`mediajunkie.github.io/piper-morgan-website/` path, it keeps working either way.**

If you would rather I had asked first on something like this, say so and I will route the next one
through you even with xian's go-ahead. **The only reason I did not is that it touched a hostname
nothing was serving from, so the blast radius looked like zero — and it was, but "looked like zero" is
my judgement about your property, which is the part worth your objection if you have one.**

— Pard
