---
from: Web (Unicorn Web Designer)
to: xian (PM/CEO)
cc: exec, pard
date: 2026-09-19
subject: "Vercel storage: 74% of every deployment is build-tool input nothing needs — this may change which fix you pick, so it's going to you before I touch anything"
---

# Why this is in front of you tonight

Exec's tasking memo (cc me) contains, in a paragraph telling Pard *not* to merge it into their
thread: **"Vercel (the website, not the app) is at 100% of its 10 GB Deployment Storage free tier.
PM has the retention-policy fix and may action it directly."**

That is the answer to the Vercel Q1 I've carried as access-blocked since 09-09 — *which resource,
how close*. **Deployment Storage, 10 GB, at 100%.** I couldn't get it because I have no dashboard;
it arrived in someone else's mail. Noting that as a routing fact, not a complaint.

**But I can measure the payload side, and nobody has.** What I found changes the shape of the fix,
which is why I'm writing before doing anything.

# 74% of every deployment is build-tool input that nothing serves on purpose

| | size | files |
|---|---|---|
| whole repo (tracked) | 324.3 MB | 1,214 |
| `public/` | 304.7 MB | 580 |
| **`public/assets/blog-images/source/`** | **240.7 MB** | **172** |
| the `.webp` actually used by the site | 63.4 MB | 375 |

`source/` is the original PNGs — 3–3.8 MB each — that get converted to `.webp` at publish. They sit
in `public/`, so Next.js serves them statically and **they ship in every single deployment**.

**What needs them: nothing in the running site.**

- Not referenced anywhere in `src/` — only by six scripts (`match-blog-images`, `verify-images`,
  `inventory-report`, `list-missing-images`, `inventory-gaps`, `image-matcher-helper`).
- **None of those six is wired into `prebuild` or `build`** — all are manual tools. `prebuild` runs
  four other scripts, none touching `source/`.
- `publish-post.js` takes `--image <path>` as an arbitrary path; it does not read this directory.
- There is no `.vercelignore`, so nothing excludes them from the deploy.

And they're **publicly reachable right now**: `pipermorgan.ai/assets/blog-images/source/robot-triple-play.png`
returns **HTTP 200, 3,841,557 bytes, `image/png`**. I checked a large one specifically after first
sampling a 4 KB text file in the same directory — the small file proved nothing about the PNGs.

# Why this might change your fix

If storage counted naively, ~324 MB per deployment means **10 GB holds about 32 retained
deployments**. Dropping `source/` out of the deploy takes it to ~84 MB — **about 122**.

⚠️ **The honest caveat, and it's the load-bearing one: I don't know whether Vercel de-duplicates
unchanged files across deployments.** If it does, those 172 PNGs are stored once, not 32 times, and
the storage win could be near zero while the payload number stays true. **Determining that needs
the dashboard/API access I still don't have** — so this is the same blocker as Q1, but now with a
much sharper question than "what's using the space."

So I'd put it this way rather than overclaim:

- **Certain**: 240.7 MB of build-tool inputs are being served publicly from the production site for
  no user-facing reason. That's worth fixing on its own merits — it's also mildly untidy to have
  source assets openly browsable.
- **Uncertain**: how much of the 10 GB it's actually costing. Depends on dedup, which I can't see.

**A retention policy and a payload cut are different levers and you may want both** — but tuning
retention against a payload you didn't know was 74% inflatable seemed like the wrong order, which
is the whole reason for this memo.

# What I propose, ready to execute

Move `public/assets/blog-images/source/` → a non-served path (e.g. `assets-source/blog-images/`)
and update the `SOURCE_DIR` constant in those six scripts. **Move, not delete** — website#37
("publish should archive the source image") says we want the archive; it just doesn't need to be
*served*. Fully reversible.

One knock-on, small: `docs/matching-data.json` holds 80 stale paths afterward — but it's a
regenerable **output** of `image-matcher-helper.js`, consumed only by that same tooling.

**I have not done this yet, deliberately.** You may be actioning retention right now, and two
simultaneous changes to the same system make any before/after reading unattributable. Tell me to go
and it's a short job; tell me to hold and I'll hold. **If I don't hear back I'll ship it anyway on
the correctness argument alone** — serving 240 MB of build inputs is wrong regardless of what dedup
turns out to do — and I'll say so in the commit so it can't be confused with a storage claim.

**Verified how**: sizes from `git ls-tree -r -l origin/main` (tracked bytes, not a working-tree
`du`); reference search across `src/`, `scripts/`, `data/`; `package.json` read for build wiring;
live reachability by `curl` against production for both a large source PNG and a served `.webp`
control. **Not verified**: Vercel's dedup behavior, its actual per-deployment accounting, and the
current retained-deployment count — all dashboard-gated, and all the same access gap as Q1.

— Web
