---
from: Web (Unicorn Web Designer)
to: xian (PM/CEO)
cc: exec, comms
date: 2026-09-20
subject: "Signup-options audit — the gap is one question: does anything actually get sent to Buttondown subscribers today?"
---

Your ask, via Exec: *"make sure the options we offer when people sign up now align with what we
offer today and if there is a gap we clarify it."* Done. **Most of the gap collapses to one question
only you can answer**, so that's first.

# 🔴 The question

**Does anything get sent to Buttondown subscribers today, and how often?**

I can't determine it from here, and the surrounding evidence points at "no automated path":

- **Signup works** — it POSTs to `buttondown.com/api/emails/embed-subscribe/pipermorgan`, so
  subscribers *are* being collected.
- **I find no send mechanism in either repo** — nothing publishes to Buttondown from
  `piper-morgan-website` or `piper-morgan-product`.
- **The weekly runbook's newsletter step is LinkedIn**, not Buttondown: *"Step 9 · Share in the
  LinkedIn newsletter."*

⚠️ **Absence of a mechanism in the repos is not proof nothing is sent** — you may send manually from
Buttondown's UI, which I'd have no way to see. That's exactly why this is a question rather than a
finding.

**If the answer is "nothing is sent regularly," then people are consenting to "delivered weekly" and
receiving a confirmation email and then silence** — which is the gap worth clarifying, and it's a
trust issue more than a copy issue.

# The three signup surfaces, and what each promises

| surface | promise |
|---|---|
| **`/blog`** | *"Get systematic excellence insights **delivered weekly**"* + 5 benefit bullets + *"Join **576+** PM professionals"* (twice) |
| **`/try/beta`** | waitlist — *"First access when beta opens"*, *"**Weekly updates** on what we're building"*, *"We'll email you directly — no mass-blast"* |
| **`/newsletter`** | client-side redirect to `/blog`, `noindex` — so effectively the same surface |

# Promise-by-promise

| claim | what I measured |
|---|---|
| *"delivered weekly"* | **See the question above.** |
| *"Weekly methodology insights"* | We publish **~4.9 posts/week** (21 in the last 30 days). So either this means a weekly *digest* — which doesn't exist as an artifact — or it understates the cadence by ~5×. |
| *"Early access to new systematic frameworks and tools"* | Early access to the **product** is the `/try/beta` waitlist — a *different* signup. A blog subscriber gets nothing extra. Ambiguous as written. |
| *"Practical templates and patterns you can immediately apply"* | **The subject matter is real** — 98 posts mention "template", 78 mention "framework". Whether we ship *applicable artifacts* vs *write about them* is your judgment call, not a factual gap. |
| *"Join 576+ PM professionals"* (hardcoded, 2 places) | **Unverifiable from my seat** — the Vercel token doesn't cover Buttondown. A hardcoded count in marketing copy goes stale silently; if you can read the real number I'll update or de-number it. |

# What I'd suggest, once you answer the question

- **If nothing is sent**: soften to what's true — *"Get notified when we publish"* — or wire up a
  real send. **I'd avoid "weekly" either way**, since it's wrong in both directions right now.
- **If you do send manually**: the copy is closer to right; I'd still fix *"early access"* (it points
  at a different signup) and replace the hardcoded 576 with either a live figure or no figure.
- **Small, separate**: `/newsletter` is a *client-side* redirect returning HTTP 200. It works and is
  `noindex`, so no SEO harm — but a server 301 would be cleaner. Not part of the gap; noting it since
  I was in there.

# Two checks of mine that were wrong, caught before they reached you

1. **"0 posts about templates."** My first pass searched post *titles* — zero hits — which would have
   been a clean-looking false finding. Content search found **98**. A titles-only check cannot
   distinguish "we don't cover this" from "we don't say it in titles."
2. **"`/newsletter` changed."** It returns HTTP 200, and I briefly read that as a real page
   contradicting my own notes. It's a client-side redirect; **200 is expected**. My notes were right.

**Verified how**: signup endpoint and all promise strings read from `NewsletterSignup.tsx` and both
call sites; third surface confirmed by reading `newsletter/page.tsx`; cadence computed from
`blog-metadata.csv` (21 posts / 30 days); template/framework counts from `blog-content.json` (401
posts); runbook step 9 quoted from `weekly-cycle-runbook.md`; live render of `/newsletter` in a
browser. **Not verified**: whether you send manually from Buttondown, the real subscriber count, and
whether any Buttondown-side automation exists outside these repos.

— Web
