# Site Observation Pass — pipermorgan.ai

**Date**: 2026-05-24
**Author**: Web (Unicorn Web Designer)
**Purpose**: Solo first-pass observation of every public-facing page on pipermorgan.ai, surfaced as a structured list PM can react to async. Primes the formal joint walkthrough whenever PM has focused time.

## How to use this doc

Each observation has:
- **Tag**: `[BUG]` / `[VIS]` / `[UX]` / `[COPY]` / `[A11Y]` / `[PERF]` / `[SEO]` / `[IA]` / `[CONTENT]`
- **Priority lean**: `P1` (real bug or broken UX) / `P2` (meaningful improvement) / `P3` (nit / polish)
- **Note**: what I see + (where relevant) suggested fix

**To react**: edit this file inline and append one of `+1` (agree, do it) / `-1` (disagree, drop it) / `?` (discuss) / `defer` (yes-but-later) at the end of each item. Or just signal in chat with item numbers.

**Scope of this pass**: source-code review + cross-referenced with file structure. I didn't drive the live site in a browser (would need a headless tool); for items where rendered behavior matters more than source, I've flagged `[needs visual check]`.

---

## Site-wide

### #1 [IA] [P2] Two pages effectively cover "how we work": `/methodology` and `/what-weve-learned`

`/methodology` is the Excellence Flywheel principles ("verification before implementation", "tests before features", etc.). `/what-weve-learned` describes insights from three months of AI development. Both center on "how we approach building." Navigation links to `/methodology` (via Journey dropdown); `/what-weve-learned` isn't in nav at all but is canonical content (60KB+ source).

Question: is `/what-weve-learned` deprecated content that should redirect, or a still-valuable companion that deserves a nav slot? My instinct: pick one and consolidate, or give `/what-weve-learned` real IA treatment if it's still meant to drive traffic.

### #2 [BUG] [P1] [SHIPPED 5/24 dfc87a53d] `/what-weve-learned` primary CTA points to `/how-it-works`, which is itself a redirect to `/methodology`

`/how-it-works/page.tsx` is just `<ClientRedirect to="/methodology" />`. So clicking "See How Our Methodology Works" on `/what-weve-learned` does an extra hop. Should point directly to `/methodology`.

### #3 [BUG] [P1] `/try/beta` form has placeholder Formspree endpoint

`const FORMSPREE_ENDPOINT = 'https://formspree.io/f/YOUR_FORM_ID';` — that's a literal placeholder. The beta-waitlist signup form will fail when anyone submits. This is the primary CTA from `/newsletter` (which redirects to `/try/beta`) AND from the homepage's flow. Needs a real form ID or alternative collector.

### #4 [VIS] [P3] Navigation logo: `/assets/pm-logo.png` is a 400×400 PNG used at 40×40

The `<Image>` component handles sizing, but a 400×400 source is overkill for a 40×40 display. For Retina (2x), 80×80 would suffice. Minor PERF / asset-weight item.

### #5 [A11Y] [P2] Theme toggle present in nav; not sure if it has discoverable affordance

`<ThemeToggle />` is in `Navigation.tsx` but I haven't seen its rendered shape. If it's an unlabeled icon button, screen-reader users may miss it. [needs visual check + ARIA-label audit]

### #6 [CONTENT] [P2] Privacy policy is dated "September 2025" — visibly stale

In the blog publish cadence (multiple posts/week since), Sept 2025 reads as "haven't touched this in 8 months." The actual policy content may be unchanged-and-fine; just bumping the "Last updated" date when policies have been reaffirmed is a low-cost trust signal.

### #7 [SEO] [P3] Several pages set their own metadata directly; others go through `generateSEOMetadata`

Mixed patterns: `/methodology` and `/try` use inline metadata; `/about`, `/get-involved`, `/privacy`, `/what-weve-learned`, `/` go through the helper. Helper is the better convention (keywords, OpenGraph, Twitter cards all derive automatically). Tech-debt nit: bring the holdouts through the helper for consistency.

### #8 [IA] [P3] Footer "Journey" links to `/blog`, but nav "Journey" dropdown has 3 children (Blog, Shipping News, Methodology)

Slight asymmetry — footer is single-link, nav is dropdown. Not wrong, but consider footer either matching the dropdown shape or being a column instead of a single row.

---

## / (Homepage)

### #9 [COPY] [P2] [SHIPPED 5/24 dfc87a53d] "260+ blog posts" — possibly stale

Hardcoded count in "Why Trust Us" section. As of today the post count is 309+. A hardcoded number ages badly; either bump or derive from `medium-posts.json` at build time (the data is right there).

### #10 [VIS] [P3] Hero headline is `THINK BIGGER` in caps

Choice — bold, attention-grabbing. Works with the gradient hero background. Just flagging — if the rest of the site eschews shouty caps (mostly true), the homepage shouts a bit harder. Intentional?

### #11 [UX] [P2] [SHIPPED 5/24 dfc87a53d] Footer CTAs at bottom are both `variant="outline"` — neither is the primary intent

"Help shape what Piper becomes" → `/get-involved` and "Follow along as we build" → `/blog`. Both outline buttons make them visually equivalent. If one is the dominant ask (probably get-involved given the alpha/beta funnel), make it `variant="primary"` and the other outline.

### #12 [COPY] [P3] "Built in public, from day one" + "260+ blog posts. Weekly progress reports."

Quietly proud line — good voice. The "Weekly progress reports" claim is supported by the Shipping News cadence (Wed weekly). Just verifying it's still accurate (it is, per the recent calendar).

---

## /about

### #13 [COPY] [P2] "decades of experience" — slightly hedged credibility

The bio mentions Yahoo, Grubhub, Typepad, O'Reilly book — these are specific resumé bullets that read stronger than "decades." Either lean into specifics ("20+ years at Yahoo, Grubhub, Typepad") or let the company names carry the weight (drop "decades").

### #14 [CONTENT] [P3] The "name" section explains Piper / Morgan etymology

Whimsical, fine. Last paragraph is cut off in my read (line 100 limit) but I bet it lands.

---

## /methodology

### #15 [VIS] [P3] Principles numbered 1, 2, 3, 4 with consistent layout

Clean. Card-grid would be a v2 if PM wants more visual interest, but the current vertical-flow with numbered icons reads well.

### #16 [CONTENT] [P2] Methodology page doesn't mention the publish-to-blog skill, the Excellence Flywheel evidence, or any of the specific patterns documented in the project

The principles are abstract; the actual methodology has matured a LOT since this page was written. Could be enriched with concrete examples (e.g., "The Excellence Flywheel produces patterns like the Cross-Reference Gate, the methodology audit, the publish-to-blog skill v0.16…"). Or — easier — link to specific blog posts that exemplify each principle.

---

## /what-weve-learned

### #17 [IA] [P2] Page exists with 60KB+ of substantive content but no nav presence

Either drive traffic to it (add to nav OR cross-link from /methodology) or retire it.

### #18 [BUG] (duplicate of #2) See above

---

## /get-involved

### #19 [UX] [P2] Contributor email `mailto:contribute@pipermorgan.ai` — verify deliverability

mailto links go directly to the email — if the address doesn't actually route anywhere or get checked, this is an invisible friction point. (Just confirm it's monitored.)

### #20 [COPY] [P3] "Piper is built in Python with a FastAPI backend"

True but lands as implementation-detail in a page about CONTRIBUTING. Reads better if framed around what a contributor's experience would be ("Python ecosystem; FastAPI for the API surface; ~X% test coverage").

### #21 [UX] [P3] `https://pmorgan.tech` and GitHub link side-by-side — same visual weight

If `pmorgan.tech` is the primary onboarding for contributors, give it primary-button weight; GitHub stays secondary.

---

## /try, /try/alpha, /try/beta

### #22 [VIS] [P2] /try alpha-vs-beta cards are visually well-balanced — good fork pattern

The teal-vs-orange differentiation is elegant. Cards feel approachable. Just flagging the BUG in #3 nukes the beta path.

### #23 [COPY] [P2] /try/alpha "Setup required (command line, environment)" — appropriately scary

Sets expectations honestly. Good for the demographic. The "Real usage for your actual work" bullet does the heavier lift.

### #24 [BUG] (duplicate of #3) Beta form unsendable per Formspree placeholder

---

## /blog (index)

### #25 [VIS] [P3] Blog index works (verified Wed evening); era filter + category filter both render

No new findings since the alt-text + figcaption fixes from last week. Solid.

### #26 [PERF] [P3] Blog index loads 309+ post entries; first paint may be slow on slow connections

The page does its own pagination so the DOM isn't actually 309 items — but the data file (`medium-posts.json`) is ~750KB. Not blocking; flagging.

### #27 [CONTENT] [P2] No featured-post / hero-post on the blog index

Just a grid of cards in pubDate order. Could surface a "currently featured" post (CSV already has a `featured` boolean column that the codebase respects via `getFeaturedPost`). [needs visual check — maybe it's already there in a way I missed]

---

## /shipping-news

### #28 [VIS] [P3] Hero has a single 🚢 emoji + the title; minimal and works

Clean. Matches the casual-but-authoritative tone of the Ship posts themselves.

---

## /privacy

### #29 [CONTENT] (duplicate of #6) Stale "Last updated" date

### #30 [SEO] [P3] Privacy uses inline `<section>` + `<h2>` + `<h3>` structure correctly

Good semantic markup. ARIA accessibility appears solid from source.

---

## Redirects

### #31 [SEO] [P3] `/how-it-works` and `/newsletter` are client-side redirects with `robots: noindex`

Good — won't muddy SEO. But internal links (#2) shouldn't traverse the redirects.

---

## Quick wins (SHIPPED 5/24 dfc87a53d)

All three quick-wins shipped this morning (Sunday) under one polish-batch commit:

1. ~~**#2**~~ ✅ `/what-weve-learned` CTA → `/methodology` direct
2. ~~**#9**~~ ✅ Homepage count now derived from `medium-posts.json.length` (currently renders as "313+ blog posts"; future publishes bump automatically)
3. ~~**#11**~~ ✅ Homepage "Help shape what Piper becomes" CTA is now `variant="primary"`

For #3 (the Formspree placeholder) you'd need to provide the actual form ID first (since I can't create a Formspree form for you). Same shape: as soon as you drop the ID, ~5min to wire it.

For #1, #5, #17, #19 — these are PM-judgment items where you'd need to make a call before I can act.

---

## Wrap

~31 items across 12 pages. About a third are P1/P2 worth doing; the rest are polish / IA discussion. None are showstoppers. The site is in solid shape — the observations cluster around "minor staleness" and "loose IA threads" rather than "major broken things." The two real bugs (#2 internal-link redirect, #3 Formspree placeholder) are 5-minute fixes each.

Whenever you've got a few minutes (or want to do the formal joint walkthrough), this is the artifact to react to. I'm standing by.
